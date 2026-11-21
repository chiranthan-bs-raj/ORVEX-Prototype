"""ORVEX demo API. Reads the real dataset tables under data/ (nothing is invented); SQLite (data/app/orvex_app.db) stores
users, investigations, reviews and notes. Run from <repo>:  python -m uvicorn main:app --app-dir src/orvex/api --port 8000"""
import os, json, io, glob, hashlib, secrets, sqlite3, subprocess, time, shutil, logging, datetime as dt
from functools import lru_cache
import numpy as np, pandas as pd, jwt
from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Header, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse, JSONResponse, Response
from pydantic import BaseModel

ROOT = os.environ.get("ORVEX_ROOT") or os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
TAB = os.path.join(ROOT, "data", "derived", "tables"); FEAT = os.path.join(ROOT, "data", "derived", "features")
APPD = os.environ.get("ORVEX_APP_DIR") or os.path.join(ROOT, "data", "app"); os.makedirs(os.path.join(APPD, "thumbs"), exist_ok=True); os.makedirs(os.path.join(APPD, "uploads"), exist_ok=True)
_local_ff = glob.glob(os.path.join(ROOT, "tools", "ffmpeg-*", "bin", "ffmpeg.exe"))
FF = os.environ.get("ORVEX_FFMPEG") or shutil.which("ffmpeg") or (_local_ff[0] if _local_ff else "ffmpeg")   # system FFmpeg in Docker, bundled one on the dev laptop
FP = os.environ.get("ORVEX_FFPROBE") or shutil.which("ffprobe") or FF.replace("ffmpeg.exe", "ffprobe.exe")
MEDIA_BASE = os.environ.get("ORVEX_MEDIA_BASE", "").rstrip("/")   # e.g. https://huggingface.co/datasets/<user>/<repo>/resolve/main  (videos not on local disk are read from here)
logging.basicConfig(level=os.environ.get("ORVEX_LOG", "INFO"), format="%(asctime)s %(levelname)s %(name)s: %(message)s")
log = logging.getLogger("orvex")
DBP = os.path.join(APPD, "orvex_app.db")
SECRET_F = os.path.join(APPD, ".secret")
if not os.environ.get("ORVEX_SECRET") and not os.path.exists(SECRET_F): open(SECRET_F, "w").write(secrets.token_hex(32))
SECRET = os.environ.get("ORVEX_SECRET") or open(SECRET_F).read().strip()   # token-signing key: set ORVEX_SECRET in production, never commit it

app = FastAPI(title="ORVEX demo API", version="0.1")
app.add_middleware(CORSMiddleware, allow_origins=[o.strip() for o in os.environ.get("ORVEX_CORS", "*").split(",")], allow_methods=["*"], allow_headers=["*"])
@app.exception_handler(Exception)
async def _unhandled(request, exc):
    log.exception("unhandled error on %s", request.url.path); return JSONResponse({"detail": "internal server error"}, status_code=500)
@app.get("/api/health")
def health(): return {"status": "ok", "service": "ORVEX Prototype API", "media_mode": "remote" if MEDIA_BASE else "local", "ffmpeg": bool(shutil.which(FF) or os.path.exists(FF))}

# ------------------------------------------------------------------ SQLite (application state)
def db():
    c = sqlite3.connect(DBP); c.row_factory = sqlite3.Row; return c
def pw(p, salt=None):
    salt = salt or secrets.token_hex(8); return salt + "$" + hashlib.pbkdf2_hmac("sha256", p.encode(), salt.encode(), 120000).hex()
def init():
    c = db()
    c.executescript("""create table if not exists users(id integer primary key, email text unique, name text, role text, pw text, created text);
    create table if not exists resets(token text primary key, email text, expires real);
    create table if not exists investigations(id integer primary key, title text, reference_id text, status text, owner text, created text, summary text, hypothesis text);
    create table if not exists history(id integer primary key, inv_id integer, ts text, actor text, action text);
    create table if not exists reviews(id integer primary key, inv_id integer, edge_key text, decision text, note text, evidence_ids text, actor text, ts text);
    create table if not exists uploads(id text primary key, name text, path text, meta text, owner text, ts text);""")
    if not c.execute("select 1 from users").fetchone():
        c.execute("insert into users(email,name,role,pw,created) values(?,?,?,?,?)", ("demo.investigator@orvex.local", "Demo Investigator", "admin", pw("OrvexDemo!2026"), now()))
        c.execute("insert into users(email,name,role,pw,created) values(?,?,?,?,?)", ("demo.reviewer@orvex.local", "Demo Reviewer", "reviewer", pw("OrvexDemo!2026"), now()))
    c.commit(); c.close()
def now(): return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
init()
class Creds(BaseModel): email: str; password: str; name: str = ""
class Reset(BaseModel): email: str = ""; token: str = ""; password: str = ""
def user(authorization: str = Header(default="")):
    try: return jwt.decode(authorization.replace("Bearer ", ""), SECRET, algorithms=["HS256"])
    except Exception: raise HTTPException(401, "not signed in")
def token(u): return jwt.encode({"email": u["email"], "name": u["name"], "role": u["role"], "exp": time.time() + 86400}, SECRET, algorithm="HS256")

@app.post("/api/auth/login")
def login(c: Creds):
    r = db().execute("select * from users where email=?", (c.email.lower(),)).fetchone()
    if not r or pw(c.password, r["pw"].split("$")[0]) != r["pw"]: raise HTTPException(401, "wrong e-mail or password")
    return {"token": token(r), "user": {"email": r["email"], "name": r["name"], "role": r["role"]}}
@app.post("/api/auth/register")
def register(c: Creds):
    if len(c.password) < 8: raise HTTPException(400, "password needs 8 or more characters")
    try:
        d = db(); d.execute("insert into users(email,name,role,pw,created) values(?,?,?,?,?)", (c.email.lower(), c.name or c.email, "investigator", pw(c.password), now())); d.commit()
    except sqlite3.IntegrityError: raise HTTPException(409, "e-mail already registered")
    return login(c)
@app.post("/api/auth/forgot")
def forgot(r: Reset):
    t = secrets.token_urlsafe(12); d = db()
    if d.execute("select 1 from users where email=?", (r.email.lower(),)).fetchone():
        d.execute("insert into resets values(?,?,?)", (t, r.email.lower(), time.time() + 900)); d.commit()
        return {"sent": True, "demo_token": t, "note": "Demo mode: no e-mail server is configured, so the reset token is shown here instead of being e-mailed."}
    return {"sent": True, "note": "If the address is registered a reset token would be sent."}
@app.post("/api/auth/reset")
def reset(r: Reset):
    d = db(); x = d.execute("select * from resets where token=?", (r.token,)).fetchone()
    if not x or x["expires"] < time.time() or len(r.password) < 8: raise HTTPException(400, "invalid or expired token, or password too short")
    d.execute("update users set pw=? where email=?", (pw(r.password), x["email"])); d.execute("delete from resets where token=?", (r.token,)); d.commit(); return {"ok": True}
@app.get("/api/auth/users")
def users(u=Depends(user)):
    return [dict(x) for x in db().execute("select email,name,role,created from users")] if u["role"] == "admin" else [dict(x) for x in db().execute("select email,name,role,created from users where email=?", (u["email"],))]

# ------------------------------------------------------------------ data layer (real tables)
def rd(name, **k): return pd.read_csv(os.path.join(TAB, name + ".csv"), low_memory=False, encoding="utf-8-sig", **k)
@lru_cache
def M():
    m = rd("real_world_media_master"); return m
@lru_cache
def LOCAL():
    m = M(); m = m[m.local_path.notna()].copy(); return m.set_index("media_id", drop=False)
@lru_cache
def VAR():
    v = rd("controlled_variant_registry"); v = v[v.validation_status == "passed"].copy(); return v.set_index("variant_media_id", drop=False)
@lru_cache
def EDGES(): return rd("media_relationship_edges")
@lru_cache
def LEDGER(): return rd("evidence_ledger")
@lru_cache
def PAIRS(): return rd("training_pairs")
@lru_cache
def OBS(): return rd("platform_observations")
@lru_cache
def SPLITS(): return pd.read_csv(os.path.join(ROOT, "data", "derived", "splits", "split_manifest.csv"), encoding="utf-8-sig")
@lru_cache
def HASH():
    h = {}
    for l in open(os.path.join(FEAT, "visual_dhash24.jsonl"), encoding="utf-8"):
        j = json.loads(l); h[j["media_id"]] = np.array([int(x, 16) for x in j["dhash24"]], dtype=np.uint64)
    return h
@lru_cache
def AUD():
    a = {}
    for l in open(os.path.join(FEAT, "audio_fingerprint.jsonl"), encoding="utf-8"):
        j = json.loads(l); a[j["media_id"]] = (j["audio_md5_8k"], j["audio_env_1s"])
    return a
def nn(x):
    if x is None: return None
    if isinstance(x, float) and np.isnan(x): return None
    if isinstance(x, (np.integer,)): return int(x)
    if isinstance(x, (np.floating,)): return None if np.isnan(x) else float(x)
    if isinstance(x, (np.bool_,)): return bool(x)
    return x
def clean(d): return {k: nn(v) for k, v in d.items()}
def frac(a, b):
    if len(a) == 0 or len(b) == 0: return None
    d = np.bitwise_count(a[:, None] ^ b[None, :]); return float((d.min(1) <= 8).mean())   # same rule as scripts/datasets/s9
def sims(a, b):
    H, A = HASH(), AUD(); out = {}
    if a in H and b in H:
        f1, f2 = frac(H[a], H[b]), frac(H[b], H[a]); out["dhash_match_fraction"] = max(f1, f2)
    if a in A and b in A:
        out["audio_md5_identical"] = A[a][0] == A[b][0]
        ea, eb = A[a][1], A[b][1]; n = min(len(ea), len(eb))
        if n >= 5: out["audio_envelope_agreement"] = float(np.mean([x == y for x, y in zip(ea[:n], eb[:n])]))
    return out
def vlabel(t, d): return {"caption_burn_in": "Caption added", "watermark_overlay": "Watermark added", "trim_middle": "Trimmed (middle)", "trim_head": "Trimmed (head)", "trim_tail": "Trimmed (tail)", "crop_center": "Cropped", "recompress_low": "Recompressed (low)", "reencode_hq": "Re-encoded (HQ)", "audio_replace": "Audio replaced", "audio_mute": "Audio muted", "audio_noise_mix": "Noise mixed into audio", "mirror_color_shift": "Mirrored + colour shift", "speed_change": "Speed changed", "reupload_sim": "Re-upload simulation"}.get(t, t)
def media(mid):
    L, V = LOCAL(), VAR()
    if mid in V.index:
        r = V.loc[mid]; root = r.root_source_media_id; rr = M().set_index("media_id", drop=False).loc[root] if root in M().media_id.values else None
        chain = [x for x in str(r.ancestor_chain).split("|") if x]
        return clean(dict(id=mid, kind="variant", title=f"{vlabel(r.transformation_name, 0)} of {root}", source="Controlled variant (ORVEX)", source_dataset="ORVEX-CTRL", duration=r.duration_s, width=r.width, height=r.height, bytes=r.bytes,
            fps=r.fps, has_audio=r.has_audio, path=r.local_path, created_utc=r.created_utc, transformation=r.transformation_name, transformation_family=r.transformation_family, parent=r.direct_parent_media_id,
            root=root, ancestors=chain, depth=int(r.generation_depth), params=r.parameters_json, caption_text=r.caption_text, audio_source=r.audio_source_media_id, sha256=r.sha256, license=r.root_license, split=r.source_split,
            usable_for_training=r.usable_for_training, published=nn(rr.published_time_utc) if rr is not None else None, tool=f"{r.tool_name} {r.tool_version}", run_id=r.run_id))
    if mid in L.index:
        r = L.loc[mid]
        return clean(dict(id=mid, kind="natural", title=r.title, source={"RW-01": "Wikimedia Commons", "RW-02": "ANAKIN (Vimeo-sourced, CC BY 4.0 card)"}.get(r.source_dataset_id, r.source_dataset_id), source_dataset=r.source_dataset_id,
            duration=r.duration_s, width=r.width, height=r.height, bytes=r.file_bytes, fps=r.fps, has_audio=r.has_audio, path=r.local_path, published=r.published_time_utc, observed=r.observed_time_utc, collected=r.collected_time_utc,
            license=r.license, attribution=r.attribution, native_manipulation_type=r.native_manipulation_type, url=r.source_url, sha256=r.sha256, event=r.event_or_cascade_id))
    up = db().execute("select * from uploads where id=?", (mid,)).fetchone()
    if up: m = json.loads(up["meta"]); return dict(id=mid, kind="upload", title=up["name"], source="Local upload", path=up["path"], created_utc=up["ts"], **m)
    r = M().set_index("media_id", drop=False)
    if mid in r.index:
        x = r.loc[mid]; return clean(dict(id=mid, kind="metadata_only", title=x.title, source=x.platform, source_dataset=x.source_dataset_id, published=x.published_time_utc, url=x.source_url, path=None, note="Metadata only: the media file is not stored locally."))
    raise HTTPException(404, "unknown media id")
def abspath(m): return os.path.join(ROOT, m["path"]) if m.get("path") and not os.path.isabs(m["path"]) else m.get("path")
def media_src(m):
    """Where the bytes of a video are: a local file if it exists, otherwise a URL under ORVEX_MEDIA_BASE (same relative path), otherwise None."""
    p = abspath(m)
    if p and os.path.exists(p): return p
    if MEDIA_BASE and m.get("path") and m.get("kind") != "upload": return MEDIA_BASE + "/" + str(m["path"]).replace("\\", "/")
    return None
def vtype(m): return "reference" if m.get("depth", 0) == 0 and m["kind"] != "variant" else ("direct" if m.get("depth") == 1 else "indirect")

@app.get("/api/media/{mid}")
def media_get(mid: str): m = media(mid); m["thumb"] = f"/api/media/{mid}/frame"; m["stream"] = f"/api/media/{mid}/stream"; return m
@app.get("/api/media/{mid}/stream")
def stream(mid: str):
    p = media_src(media(mid))
    if not p: raise HTTPException(404, "no media file for this id")
    if p.startswith("http"): return RedirectResponse(p, status_code=307)   # the browser streams (and seeks) straight from object storage
    return FileResponse(p, media_type="video/mp4" if p.endswith(".mp4") else "video/webm" if p.endswith(".webm") else "video/ogg" if p.endswith((".ogv", ".ogg")) else None)
@app.get("/api/media/{mid}/frame")
def frame(mid: str, t: float = 1.0, w: int = 480):
    m = media(mid); p = media_src(m)
    if not p: raise HTTPException(404, "no media file for this id")
    t = min(max(t, 0), max((m.get("duration") or 1) - 0.1, 0)); o = os.path.join(APPD, "thumbs", f"{mid}_{t:.1f}_{w}.jpg")
    if not os.path.exists(o): subprocess.run([FF, "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", p, "-frames:v", "1", "-vf", f"scale={w}:-2", o], capture_output=True, timeout=60)   # p may be an https URL: FFmpeg then reads only the bytes it needs
    if not os.path.exists(o): raise HTTPException(500, "frame extraction failed")
    return FileResponse(o, media_type="image/jpeg", headers={"Cache-Control": "max-age=86400"})
@app.get("/api/media")
def media_list(q: str = "", kind: str = "", source: str = "", transformation: str = "", limit: int = 60, offset: int = 0):
    L, V = LOCAL(), VAR(); rows = []
    if kind in ("", "natural"):
        d = L
        if source: d = d[d.source_dataset_id == source]
        if q: d = d[d.title.fillna("").str.contains(q, case=False) | d.media_id.str.contains(q, case=False)]
        rows += [dict(id=r.media_id, kind="natural", title=r.title, source_dataset=r.source_dataset_id, duration=nn(r.duration_s), width=nn(r.width), height=nn(r.height)) for r in d.itertuples()]
    if kind in ("", "variant"):
        d = V
        if transformation: d = d[d.transformation_name == transformation]
        if q: d = d[d.variant_media_id.str.contains(q, case=False) | d.root_source_media_id.str.contains(q, case=False)]
        rows += [dict(id=r.variant_media_id, kind="variant", title=vlabel(r.transformation_name, 0), source_dataset="ORVEX-CTRL", duration=nn(r.duration_s), width=nn(r.width), height=nn(r.height), root=r.root_source_media_id, transformation=r.transformation_name) for r in d.itertuples()]
    return {"total": len(rows), "items": rows[offset:offset + limit]}

# ------------------------------------------------------------------ families and graph
@lru_cache
def families():
    V = VAR(); g = V.groupby("root_source_media_id"); out = []
    for root, d in g:
        if root not in LOCAL().index: continue
        r = LOCAL().loc[root]; out.append(dict(root=root, title=r.title, n_variants=len(d), max_depth=int(d.generation_depth.max()), n_transformations=int(d.transformation_name.nunique()), duration=nn(r.duration_s), kind="commons"))
    out.sort(key=lambda x: (-x["max_depth"], -x["n_transformations"], -x["n_variants"])); return out
@app.get("/api/families")
def fam(): return families()
def unrelated_for(root, ids, k=1):
    V, P = VAR(), PAIRS(); mem = set(V[V.root_source_media_id == root].variant_media_id) | {root}
    d = P[(P.relationship_class == "unrelated_distinct_source") & (P.media_a_id.isin(mem) | P.media_b_id.isin(mem))]
    rows = []
    for r in d.itertuples():
        mine, other = (r.media_a_id, r.media_b_id) if r.media_a_id in mem else (r.media_b_id, r.media_a_id)
        if other in mem or (other not in LOCAL().index and other not in V.index): continue
        rows.append((0 if mine in ids else 1, {"hard": 0, "medium": 1, "easy": 2}.get(r.hardness, 3), mine, other, r))
    rows.sort(key=lambda x: x[:4]); return [(m, o, r) for _, _, m, o, r in rows[:k]]
@app.get("/api/graph/{root}")
def graph(root: str, limit: int = 9, show_all: bool = Query(False, alias="all"), transformation: str = ""):
    V = VAR(); fam_ = V[V.root_source_media_id == root]
    if fam_.empty: raise HTTPException(404, "no controlled variants for this root")
    if transformation: fam_ = fam_[fam_.transformation_name == transformation]
    if not show_all:
        deep = fam_[fam_.generation_depth >= 2].sort_values("generation_depth", ascending=False).head(3)
        d1 = fam_[fam_.generation_depth == 1].drop_duplicates("transformation_name").head(max(limit - len(deep), 1))
        keep = pd.concat([d1, deep]); need = set(keep.variant_media_id)
        for vid in list(need):   # keep ancestors so every edge has a visible parent
            for a in str(V.loc[vid].ancestor_chain).split("|"):
                if a in V.index: need.add(a)
        fam_ = fam_[fam_.variant_media_id.isin(need)] if not transformation else fam_
    E, led = EDGES(), LEDGER(); nodes = [dict(media(root), role="reference", label="Reference")]; edges = []
    for r in fam_.itertuples():
        m = media(r.variant_media_id); role = "direct" if r.generation_depth == 1 else "indirect"
        nodes.append(dict(m, role=role, label="Direct derivative" if role == "direct" else "Indirect derivative"))
        e = E[(E.child_media_id == r.variant_media_id) & (E.parent_media_id == r.direct_parent_media_id) & (E.relation_scope == "controlled_lineage")]
        ev = led[(led.subject_id == r.variant_media_id)].evidence_id.tolist()
        edges.append(dict(id=f"{r.direct_parent_media_id}>{r.variant_media_id}", source=r.direct_parent_media_id, target=r.variant_media_id, label=r.transformation_name, role=role, directed=True,
            relationship_id=e.relationship_id.iloc[0] if len(e) else None, normalized_relation_type=e.normalized_relation_type.iloc[0] if len(e) else None, label_source="controlled_transformation_log", evidence_ids=ev, sims=sims(r.direct_parent_media_id, r.variant_media_id)))
    for mine, o, pr in unrelated_for(root, {n["id"] for n in nodes}):
        if mine not in {n["id"] for n in nodes}: nodes.append(dict(media(mine), role="direct" if media(mine).get("depth") == 1 else "indirect", label="Family member"))
        nodes.append(dict(media(o), role="unrelated", label="Unrelated"))
        edges.append(dict(id=f"{mine}~{o}", source=mine, target=o, label="no relation", role="unrelated", directed=False, relationship_id=pr.example_id, normalized_relation_type="unrelated_distinct_source", label_source=f"{pr.label_origin} ({pr.hardness} negative, {pr.split} split)", evidence_ids=[], sims=sims(mine, o)))
    ids = {n["id"] for n in nodes}; assert all(e["source"] in ids and e["target"] in ids for e in edges)
    return {"root": root, "nodes": nodes, "edges": edges, "total_variants": int(len(V[V.root_source_media_id == root])),
            "note": "Edges are ground-truth controlled-lineage records (transformation log), not model predictions. Similarity fields are dHash/audio-fingerprint measurements from data/derived/features. Same-incident (FIVR) relations are metadata-only in this repository, so no local video can be shown as 'same incident'."}
@app.get("/api/transformations")
def transformations():
    V = VAR(); out = []
    for t, d in V.groupby("transformation_name"):
        r = d.iloc[0]; ex = d.iloc[0].variant_media_id
        out.append(dict(name=t, label=vlabel(t, 0), family=r.transformation_family, n=len(d), heldout=bool(t in ("mirror_color_shift", "speed_change", "reupload_sim", "audio_noise_mix")), example=ex, example_root=r.root_source_media_id, params=r.parameters_json))
    base = json.load(open(os.path.join(ROOT, "docs", "datasets", "necessity_audit", "dhash_baseline_results.json"))).get("direct_derivation_detection_by_transformation", {})
    for o in out: o["baseline"] = base.get(o["name"])
    return out
@app.get("/api/compare")
def compare(a: str, b: str):
    ma, mb = media(a), media(b); E = EDGES(); rel = E[((E.media_a_id == a) & (E.media_b_id == b)) | ((E.media_a_id == b) & (E.media_b_id == a))]
    P = PAIRS(); pr = P[((P.media_a_id == a) & (P.media_b_id == b)) | ((P.media_a_id == b) & (P.media_b_id == a))]
    relation = None
    if mb.get("parent") == a or ma.get("parent") == b or a in (mb.get("ancestors") or []) or b in (ma.get("ancestors") or []):
        child = mb if mb.get("parent") == a or a in (mb.get("ancestors") or []) else ma
        relation = dict(type="derivation (controlled lineage)", parent=a if child is mb else b, child=child["id"], transformation=child.get("transformation"), source="controlled_variant_registry")
    elif ma.get("root") and ma.get("root") == mb.get("root"): relation = dict(type="siblings in the same source family", source="controlled_variant_registry", root=ma["root"])
    elif len(pr): relation = dict(type=pr.iloc[0].relationship_class, source="training_pairs", hardness=nn(pr.iloc[0].hardness), split=pr.iloc[0].split)
    return {"a": ma, "b": mb, "sims": sims(a, b), "relation": relation, "edge_records": [clean(r) for r in rel.head(5).to_dict("records")],
            "evidence": LEDGER()[LEDGER().subject_id.isin([a, b])][["evidence_id", "evidence_type", "claim_supported"]].to_dict("records"),
            "note": "dhash_match_fraction = share of 24 sampled frames with a frame in the other video within 8 bits (rule from scripts/datasets/s9). It is a measurement, not an ORVEX model score. No OCR/ASR/embedding features exist yet."}
@app.get("/api/provenance/{mid}")
def provenance(mid: str):
    m = media(mid); root = m.get("root") or mid; V = VAR(); fam_ = V[V.root_source_media_id == root]
    nodes = [dict(media(root), role="reference")] + [dict(media(i), role="direct" if d == 1 else "indirect") for i, d in zip(fam_.variant_media_id, fam_.generation_depth)]
    edges = [dict(source=p, target=c, label=t, chain=nn(ch)) for c, p, t, ch in zip(fam_.variant_media_id, fam_.direct_parent_media_id, fam_.transformation_name, fam_.chain_id)]
    return {"root": root, "selected": mid, "nodes": nodes, "edges": edges}
@app.get("/api/timeline/{root}")
def timeline(root: str):
    r = media(root); ev = []
    if r.get("published"): ev.append(dict(date=r["published"], type="original_publication", label=f"{root} published (source field published_time_utc)", media=root))
    if r.get("observed"): ev.append(dict(date=r["observed"], type="platform_observation", label="observed on platform", media=root))
    o = OBS(); oo = o[(o.media_id == root) & (o.observation_type == "upload")]
    for x in oo.itertuples():
        if isinstance(x.observation_time_utc, str) or isinstance(x.publish_time_utc, str): ev.append(dict(date=x.observation_time_utc if isinstance(x.observation_time_utc, str) else x.publish_time_utc, type="platform_observation", label=f"{x.platform} {x.observation_type} record {x.observation_id}", media=root))
    if r.get("collected"): ev.append(dict(date=r["collected"], type="dataset_collection", label="downloaded into the ORVEX dataset", media=root))
    V = VAR(); fam_ = V[V.root_source_media_id == root]
    for x in fam_.itertuples(): ev.append(dict(date=x.created_utc, type="variant_creation", label=f"{x.variant_media_id} generated ({x.transformation_name})", media=x.variant_media_id))
    return sorted(ev, key=lambda e: e["date"] or "")

import routes2  # noqa: E402,F401  (registers the remaining routes)

# Production: serve the built React app from this server, so the browser talks to one origin (no CORS, relative /api URLs).
DIST = os.environ.get("ORVEX_DIST") or os.path.join(ROOT, "frontend", "dist")
if os.path.isdir(os.path.join(DIST, "assets")):
    from fastapi.staticfiles import StaticFiles
    app.mount("/assets", StaticFiles(directory=os.path.join(DIST, "assets")), name="assets")
    @app.get("/{full_path:path}", include_in_schema=False)
    def spa(full_path: str):
        if full_path.startswith("api/"): raise HTTPException(404, "not found")
        f = os.path.abspath(os.path.join(DIST, full_path))
        ok = full_path != "" and f.startswith(os.path.abspath(DIST) + os.sep) and os.path.isfile(f)
        return FileResponse(f if ok else os.path.join(DIST, "index.html"))   # page refresh on /graph, /evidence ... returns index.html
