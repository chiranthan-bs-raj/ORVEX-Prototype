"""Second half of the ORVEX demo API: dashboard, datasets, variants, evidence, reviews, investigations, distribution, quality, models, upload, report."""
import os, io, json, glob, subprocess, math
import numpy as np, pandas as pd
from fastapi import Depends, HTTPException, UploadFile, File, Query
from fastapi.responses import Response
from pydantic import BaseModel
from main import *
import main as MN

def src_registry(): return pd.read_csv(os.path.join(ROOT, "data", "manifests", "source_registry.csv"), encoding="utf-8-sig")
def read_json(p): return json.load(open(os.path.join(ROOT, p), encoding="utf-8"))

@app.get("/api/summary")
def summary(u=Depends(user)):
    m, L, V, E, P, led, o = M(), LOCAL(), VAR(), EDGES(), PAIRS(), LEDGER(), OBS()
    d = db(); s = SPLITS()
    ex = pd.read_csv(os.path.join(TAB, "experiment_registry.csv"), encoding="utf-8-sig")
    return dict(media_records=len(m), local_files=len(L), natural_local=int((L.source_dataset_id.isin(["RW-01", "RW-02"])).sum()), commons_local=int((L.source_dataset_id == "RW-01").sum()), anakin_local=int((L.source_dataset_id == "RW-02").sum()),
        variants_passed=len(V), variants_records=len(VAR()) + 2, datasets=int(m.source_dataset_id.nunique()), pairs=len(P), pairs_in_splits=int((P.split != "excluded").sum()), edges=len(E), edges_local=int(E.media_available_locally.sum()),
        families=int(s.source_family_id.nunique()), evidence=len(led), evidence_by_type=led.evidence_type.value_counts().to_dict(), observations=len(o), clusters=len(pd.read_csv(os.path.join(TAB, "campaign_candidate_clusters.csv"), encoding="utf-8-sig")),
        relationship_classes=P.relationship_class.value_counts().to_dict(), pair_splits=P.split.value_counts().to_dict(), by_dataset=m.groupby("source_dataset_id").size().to_dict(), local_by_dataset=L.groupby("source_dataset_id").size().to_dict(),
        transformation_counts=V.transformation_name.value_counts().to_dict(), investigations=d.execute("select count(*) from investigations").fetchone()[0], reviews=d.execute("select count(*) from reviews").fetchone()[0],
        activity=[dict(r) for r in d.execute("select ts,actor,action,inv_id from history order by id desc limit 8")], experiments=ex[["experiment_id", "metric_name", "metric_value", "split_version"]].to_dict("records"),
        data_gb=17.24, budget_gb=30)

@app.get("/api/datasets")
def datasets(q: str = "", status: str = "", u=Depends(user)):
    r = src_registry(); m = M(); L = LOCAL(); cnt = m.groupby("source_dataset_id").size().to_dict(); loc = L.groupby("source_dataset_id").size().to_dict()
    if q: r = r[r.title.fillna("").str.contains(q, case=False) | r.source_dataset_id.str.contains(q, case=False)]
    if status: r = r[r.inclusion_status == status]
    out = []
    for x in r.itertuples():
        out.append(clean(dict(id=x.source_dataset_id, title=x.title, creator=x.creator, license=x.license_terms, inclusion_status=x.inclusion_status, tasks=x.tasks_supported, native_task=x.native_task, labels=x.native_labels,
            records_in_tables=int(cnt.get(x.source_dataset_id, 0)), local_media_files=int(loc.get(x.source_dataset_id, 0)), local_bytes=x.actual_local_bytes, limitations=x.limitations, verification=x.verification_level, derivative=x.derivative_use_status, training=x.training_use_status, url=x.official_url)))
    return {"items": out, "statuses": src_registry().inclusion_status.value_counts().to_dict()}
@app.get("/api/datasets/{did}/records")
def ds_records(did: str, limit: int = 25, offset: int = 0, q: str = "", u=Depends(user)):
    m = M(); d = m[m.source_dataset_id == did]
    if q: d = d[d.title.fillna("").str.contains(q, case=False) | d.media_id.str.contains(q, case=False)]
    cols = ["media_id", "title", "platform", "published_time_utc", "duration_s", "width", "height", "access_status", "native_manipulation_type", "license", "local_path"]
    return {"total": len(d), "items": [clean(r) for r in d[cols].iloc[offset:offset + limit].to_dict("records")]}

@app.get("/api/variants")
def variants(transformation: str = "", depth: int = 0, root: str = "", q: str = "", limit: int = 40, offset: int = 0, u=Depends(user)):
    V = VAR(); d = V
    if transformation: d = d[d.transformation_name == transformation]
    if depth: d = d[d.generation_depth == depth]
    if root: d = d[d.root_source_media_id == root]
    if q: d = d[d.variant_media_id.str.contains(q, case=False)]
    cols = ["variant_media_id", "direct_parent_media_id", "root_source_media_id", "transformation_name", "generation_depth", "duration_s", "width", "height", "source_split", "usable_for_training", "validation_status"]
    return {"total": len(d), "items": [clean(r) for r in d[cols].iloc[offset:offset + limit].to_dict("records")], "all_registry_records": 1133, "failed": 2}
@app.get("/api/variants/{vid}")
def variant(vid: str, u=Depends(user)):
    V = VAR()
    if vid not in V.index: raise HTTPException(404, "not a validated variant")
    r = V.loc[vid]; chain = [x for x in str(r.ancestor_chain).split("|") if x]; log = pd.read_csv(os.path.join(TAB, "transformation_run_log.csv"), encoding="utf-8-sig")
    lg = log[log.variant_media_id == vid] if "variant_media_id" in log else log.head(0)
    E = EDGES(); e = E[E.child_media_id == vid]
    steps = [dict(id=c, transformation=V.loc[c].transformation_name if c in V.index else "original source", depth=int(V.loc[c].generation_depth) if c in V.index else 0) for c in chain + [vid]]
    return dict(record=clean(r.to_dict()), steps=steps, run_log=[clean(x) for x in lg.to_dict("records")], edges=[clean(x) for x in e.to_dict("records")],
        label_provenance="ground truth: produced by a logged FFmpeg operation (label_source = controlled_transformation_log); not a naturally collected relationship and not a model prediction")

@app.get("/api/evidence")
def evidence(q: str = "", type: str = "", subject: str = "", limit: int = 40, offset: int = 0, u=Depends(user)):
    d = LEDGER()
    if type: d = d[d.evidence_type == type]
    if subject: d = d[d.subject_id.fillna("").str.contains(subject, case=False)]
    if q: d = d[d.claim_supported.fillna("").str.contains(q, case=False) | d.evidence_id.str.contains(q, case=False)]
    rv = {r["evidence_id"]: r for r in map(dict, db().execute("select evidence_ids,decision,note from reviews"))} if False else {}
    return {"total": len(d), "types": LEDGER().evidence_type.value_counts().to_dict(), "items": [clean(r) for r in d.iloc[offset:offset + limit].to_dict("records")]}
@app.get("/api/evidence/{eid}")
def evidence_one(eid: str, u=Depends(user)):
    d = LEDGER(); r = d[d.evidence_id == eid]
    if r.empty: raise HTTPException(404, "unknown evidence id")
    r = clean(r.iloc[0].to_dict()); E = EDGES(); lin = E[E.evidence_id == eid].head(10)
    reviews = [dict(x) for x in db().execute("select * from reviews where evidence_ids like ? order by id desc", (f"%{eid}%",))]
    return dict(record=r, edges=[clean(x) for x in lin.to_dict("records")], reviews=reviews, subject=media(r["subject_id"]) if r.get("subject_type") == "media" and r.get("subject_id") else None)

class Review(BaseModel): inv_id: int = 0; edge_key: str; decision: str; note: str = ""; evidence_ids: list[str] = []
@app.post("/api/reviews")
def add_review(r: Review, u=Depends(user)):
    if r.decision not in ("accepted", "rejected", "uncertain", "note"): raise HTTPException(400, "bad decision")
    d = db(); d.execute("insert into reviews(inv_id,edge_key,decision,note,evidence_ids,actor,ts) values(?,?,?,?,?,?,?)", (r.inv_id, r.edge_key, r.decision, r.note, ",".join(r.evidence_ids), u["email"], now()))
    d.execute("insert into history(inv_id,ts,actor,action) values(?,?,?,?)", (r.inv_id, now(), u["email"], f"{r.decision} {r.edge_key}")); d.commit(); return {"ok": True}
@app.get("/api/reviews")
def get_reviews(inv_id: int = 0, edge_key: str = "", u=Depends(user)):
    q = "select * from reviews where 1=1" + (" and inv_id=%d" % inv_id if inv_id else "") + (" and edge_key=?" if edge_key else "") + " order by id desc"
    return [dict(x) for x in db().execute(q, (edge_key,) if edge_key else ())]

class Inv(BaseModel): title: str; reference_id: str; summary: str = ""; hypothesis: str = ""; status: str = "open"
@app.get("/api/investigations")
def invs(u=Depends(user)): return [dict(x) for x in db().execute("select * from investigations order by id desc")]
@app.post("/api/investigations")
def new_inv(i: Inv, u=Depends(user)):
    media(i.reference_id); d = db()
    c = d.execute("insert into investigations(title,reference_id,status,owner,created,summary,hypothesis) values(?,?,?,?,?,?,?)", (i.title, i.reference_id, "open", u["email"], now(), i.summary, i.hypothesis))
    d.execute("insert into history(inv_id,ts,actor,action) values(?,?,?,?)", (c.lastrowid, now(), u["email"], f"created investigation with reference {i.reference_id}")); d.commit(); return {"id": c.lastrowid}
@app.put("/api/investigations/{iid}")
def upd_inv(iid: int, i: Inv, u=Depends(user)):
    d = db(); d.execute("update investigations set title=?,status=?,summary=?,hypothesis=? where id=?", (i.title, i.status, i.summary, i.hypothesis, iid))
    d.execute("insert into history(inv_id,ts,actor,action) values(?,?,?,?)", (iid, now(), u["email"], f"updated (status {i.status})")); d.commit(); return {"ok": True}
@app.get("/api/investigations/{iid}")
def inv(iid: int, u=Depends(user)):
    d = db(); r = d.execute("select * from investigations where id=?", (iid,)).fetchone()
    if not r: raise HTTPException(404, "no such investigation")
    return dict(r, history=[dict(x) for x in d.execute("select * from history where inv_id=? order by id desc", (iid,))], reviews=[dict(x) for x in d.execute("select * from reviews where inv_id=? order by id desc", (iid,))])

@app.post("/api/upload")
async def upload(f: UploadFile = File(...), u=Depends(user)):
    uid = "UP-" + secrets.token_hex(4); p = os.path.join(APPD, "uploads", uid + os.path.splitext(f.filename)[1].lower()); open(p, "wb").write(await f.read())
    r = subprocess.run([FP, "-v", "error", "-print_format", "json", "-show_format", "-show_streams", p], capture_output=True, text=True)
    try: j = json.loads(r.stdout); v = [s for s in j["streams"] if s["codec_type"] == "video"][0]
    except Exception: os.remove(p); raise HTTPException(400, "not a readable video file")
    meta = dict(duration=float(j["format"].get("duration", 0)), width=v["width"], height=v["height"], bytes=int(j["format"].get("size", 0)), has_audio=any(s["codec_type"] == "audio" for s in j["streams"]), source_dataset="UPLOAD")
    d = db(); d.execute("insert into uploads values(?,?,?,?,?,?)", (uid, f.filename, os.path.relpath(p, ROOT), json.dumps(meta), u["email"], now())); d.commit(); return media_get(uid)

# ------------------------------------------------------------------ distribution
@app.get("/api/distribution/top")
def dist_top(u=Depends(user)):
    o = OBS(); s = o[o.observation_type == "share_reference"].groupby("media_id").size().sort_values(ascending=False).head(25)
    m = M().set_index("media_id", drop=False)
    return [dict(media_id=k, shares=int(v), title=nn(m.loc[k].title) if k in m.index else None) for k, v in s.items()]
@app.get("/api/distribution/video/{mid}")
def dist_video(mid: str, u=Depends(user)):
    o = OBS(); d = o[o.media_id == mid]
    if d.empty: raise HTTPException(404, "no platform observations")
    tw = d[(d.platform == "twitter") & d.publish_time_utc.notna()].copy(); tw["day"] = tw.publish_time_utc.str[:10]
    hist = tw.groupby("day").size().reset_index(name="n").to_dict("records")
    ev = d[d.observation_type.isin(["publish", "removal"])]
    return dict(media_id=mid, total=len(d), by_platform=d.groupby("platform").size().to_dict(), by_type=d.groupby("observation_type").size().to_dict(), histogram=hist,
        events=[clean(r) for r in ev[["observation_type", "platform", "publish_time_utc", "observation_time_utc", "time_precision", "account_id_pseudonym", "limitations"]].to_dict("records")],
        sample=[clean(r) for r in d[d.observation_type == "share_reference"].sort_values("publish_time_utc").head(15)[["platform_post_id", "post_url", "publish_time_utc", "time_precision"]].to_dict("records")],
        coordination_status=d.coordination_status.value_counts().to_dict(),
        facts="Observed: each row is a share reference; tweet times are derived from tweet-id snowflakes (they say when a post existed, not who posted it). No sharer accounts are provided.")
@app.get("/api/distribution/accounts")
def dist_accounts(min_videos: int = 4, u=Depends(user)):
    o = OBS(); y = o[(o.platform == "youtube") & o.account_id_pseudonym.notna() & (o.observation_type == "publish")]
    g = y.groupby("account_id_pseudonym").media_id.nunique().sort_values(ascending=False); g = g[g >= min_videos].head(6)
    nodes, edges = [], []
    for a, n in g.items():
        nodes.append(dict(id=a, type="account", label=a[:6], n=int(n)))
        for mid in y[y.account_id_pseudonym == a].media_id.unique()[:8]:
            nodes.append(dict(id=mid, type="video", label=mid.replace("RW-COVID-", ""))); edges.append(dict(source=a, target=mid, label="published (channel field)"))
    seen = set(); nodes = [n for n in nodes if not (n["id"] in seen or seen.add(n["id"]))]
    return dict(nodes=nodes, edges=edges, accounts=len(g), note="Channels are pseudonymised. A channel publishing several videos in this dataset is an observed fact, not evidence of coordination: every record has coordination_status = not_assessed and campaign_candidate_clusters is empty.")

# ------------------------------------------------------------------ quality, models
_QC = {}
@app.get("/api/quality")
def quality(u=Depends(user)):
    if "v" not in _QC: _QC["v"] = _quality()
    return _QC["v"]
def _quality():
    checks = read_json("data/reports/acceptance_checks.json"); L = LOCAL(); V = VAR()
    mf = os.path.join(ROOT, "data", "media_manifest.csv"); remote = set(pd.read_csv(mf)["path"]) if (MEDIA_BASE and os.path.exists(mf)) else set()   # files published to object storage
    have = lambda p: os.path.exists(os.path.join(ROOT, p)) or p.replace("\\", "/") in remote
    miss = [p for p in L.local_path.tolist() if not have(p)]; vmiss = [p for p in V.local_path.tolist() if not have(p)]
    E, m = EDGES(), set(M().media_id); dang = int((~E.media_a_id.isin(m) | ~E.media_b_id.isin(m)).sum())
    f = pd.read_csv(os.path.join(ROOT, "docs/datasets/repository_audit/dataset_audit_findings.csv"), encoding="utf-8-sig"); dm = pd.read_csv(os.path.join(TAB, "duplicate_map.csv"), encoding="utf-8-sig")
    txt = open(os.path.join(ROOT, "data/reports/pytest_summary.txt"), encoding="utf-8", errors="ignore").read().strip().splitlines()[-1]
    return dict(checks=[dict(id=k, ok=v["ok"], evidence=v["evidence"]) for k, v in checks.items()], pytest=txt, missing_natural=len(miss), missing_variant=len(vmiss), dangling_edges=dang, duplicates=len(dm), labels_conflict=int(E.conflict_flag.fillna(False).sum()),
        no_license=int(L.license.isna().sum()), hashes=len(HASH()), audio_fp=len(AUD()), local_files=len(L) + len(V), findings=[clean(r) for r in f[["id", "severity", "dataset", "conflicting_claims", "recommended_correction"]].to_dict("records")],
        coverage=dict(dhash=len(HASH()), audio=len(AUD()), local=len(L) + len(V), ocr=0, asr=0, embeddings=0))
@app.get("/api/models")
def models(u=Depends(user)):
    ex = pd.read_csv(os.path.join(TAB, "experiment_registry.csv"), encoding="utf-8-sig"); fm = pd.read_csv(os.path.join(TAB, "feature_manifest.csv"), encoding="utf-8-sig")
    return dict(experiments=[clean(r) for r in ex.to_dict("records")], features=fm.groupby(fm.columns[1]).size().to_dict() if len(fm.columns) > 1 else {}, feature_columns=fm.columns.tolist(),
        implemented=dict(name="dhash24-frame-match v1 (non-learned baseline)", threshold=0.45, rule="24 sampled frames per video; a frame matches if any frame of the other video is within 8 of 64 dHash bits; score = max directional matched fraction; related if score >= 0.45", script="scripts/datasets/s9_feature_baseline.py",
            audio="audio_md5_8k and a 1-second envelope string (data/derived/features/audio_fingerprint.jsonl)", metadata="duration, width, height, fps, has_audio from the registries"),
        specified=dict(encoder="frozen DINOv2 ViT-B/14 frame encoder (working choice; bake-off pending)", head="similarity-matrix CNN, multi-task: relatedness, 7 classes, direction, aligned segment, transformation tags", calibration="temperature scaling; statuses likely / uncertain / unverified", params=1310547, source="ORVEX_Requirements_and_System_Design.docx, section 8"))
@app.get("/api/evaluation")
def evaluation(u=Depends(user)):
    r = read_json("docs/datasets/necessity_audit/dhash_baseline_results.json"); ex = pd.read_csv(os.path.join(TAB, "experiment_registry.csv"), encoding="utf-8-sig")
    return dict(results=r, experiments=[clean(x) for x in ex.to_dict("records")], note="All numbers are from the non-learned dHash baseline (BASE-DHASH-v1, split-v1 label in the registry). No trained ORVEX model exists, so there is no trained-model metric, ROC curve or confusion matrix. Per-class detection rates at the fixed 0.45 threshold are shown instead.")

# ------------------------------------------------------------------ report
@app.get("/api/report/{iid}")
def report(iid: int, token: str = ""):
    import jwt as _j
    try: _j.decode(token, SECRET, algorithms=["HS256"])
    except Exception: raise HTTPException(401, "not signed in")
    from reportlab.lib.pagesizes import A4; from reportlab.lib import colors; from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    d = db(); r = d.execute("select * from investigations where id=?", (iid,)).fetchone()
    if not r: raise HTTPException(404, "no such investigation")
    ref = media(r["reference_id"]); root = ref.get("root") or ref["id"]
    try: g = graph(root)
    except HTTPException: g = dict(nodes=[ref], edges=[])
    revs = [dict(x) for x in d.execute("select * from reviews where inv_id=? order by id", (iid,))]
    S = getSampleStyleSheet(); H1 = ParagraphStyle("h", parent=S["Heading2"], textColor=colors.HexColor("#252C5C"), spaceBefore=10); N = ParagraphStyle("n", parent=S["BodyText"], fontSize=9, leading=12); sm = ParagraphStyle("s", parent=N, fontSize=7.5, leading=9)
    def tbl(rows, widths, head=True):
        t = Table(rows, colWidths=widths, repeatRows=1 if head else 0)
        t.setStyle(TableStyle([("FONTSIZE", (0, 0), (-1, -1), 7.5), ("GRID", (0, 0), (-1, -1), .3, colors.HexColor("#C9CCE0")), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#252C5C") if head else colors.white), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white if head else colors.black), ("VALIGN", (0, 0), (-1, -1), "TOP")])); return t
    P = lambda s, st=N: Paragraph(str(s).replace("&", "&amp;").replace("<", "&lt;"), st)
    colmap = {"reference": "#2563EB", "direct": "#DC2626", "indirect": "#F59E0B", "unrelated": "#6B7280", "same": "#7C3AED"}
    fig, ax = plt.subplots(figsize=(7, 4.2)); ids = [n["id"] for n in g["nodes"]]; pos = {ids[0]: (0, 0)}
    for i, n in enumerate(ids[1:]): a = 2 * math.pi * i / max(len(ids) - 1, 1); pos[n] = (math.cos(a) * 2.2, math.sin(a) * 1.6)
    for e in g["edges"]:
        (x1, y1), (x2, y2) = pos[e["source"]], pos[e["target"]]; ax.annotate("", (x2, y2), (x1, y1), arrowprops=dict(arrowstyle="->" if e["directed"] else "-", color=colmap[e["role"]], lw=1.2, linestyle="-" if e["directed"] else "--"))
        ax.text((x1 + x2) / 2, (y1 + y2) / 2, e["label"], fontsize=5.5, ha="center", color=colmap[e["role"]], bbox=dict(fc="white", ec="none", pad=.5))
    for n in g["nodes"]: ax.scatter(*pos[n["id"]], s=420, color=colmap[n["role"]], zorder=3); ax.text(*pos[n["id"]], n["id"][-6:], fontsize=5, ha="center", va="center", color="white", zorder=4)
    ax.axis("off"); b = io.BytesIO(); fig.savefig(b, format="png", dpi=170, bbox_inches="tight"); plt.close(fig); b.seek(0)
    out = io.BytesIO(); doc = SimpleDocTemplate(out, pagesize=A4, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36, title=f"ORVEX investigation {iid}")
    s = [Paragraph("ORVEX investigation report", S["Title"]), P(f"Generated {now()} from repository data. Ground-truth lineage and dataset measurements only; no ORVEX model predictions.", sm), Paragraph("1. Investigation information", H1),
         tbl([["Field", "Value"], ["Investigation", f"#{iid}: {r['title']}"], ["Owner", r["owner"]], ["Created", r["created"]], ["Status", r["status"]], ["Reference video", ref["id"]]], [110, 420]), Paragraph("2. Reference video", H1)]
    try:
        fr = os.path.join(APPD, "thumbs", f"{ref['id']}_1.0_480.jpg"); frame(ref["id"]); s.append(Image(fr, width=240, height=240 * (ref.get("height") or 9) / (ref.get("width") or 16)))
    except Exception: pass
    s.append(tbl([["Title", ref["title"]], ["Source", ref["source"]], ["Published (source field)", ref.get("published")], ["Duration / resolution", f"{ref.get('duration')} s, {ref.get('width')}x{ref.get('height')}"], ["Licence", ref.get("license")]], [110, 420], head=False))
    s += [Paragraph("3. Candidate videos and 5. Provenance", H1), tbl([["ID", "Role", "Transformation", "Parent", "Duration", "Resolution"]] + [[n["id"], n["label"], n.get("transformation") or "-", n.get("parent") or "-", n.get("duration"), f"{n.get('width')}x{n.get('height')}"] for n in g["nodes"]], [105, 80, 85, 105, 40, 55]),
          Paragraph("4. Relationship graph", H1), Image(b, width=470, height=282), P("Edges are controlled-lineage ground truth (transformation log). Arrows point from parent to derived video. The dashed grey edge is a sampled negative pair from training_pairs.", sm)]
    s.append(Paragraph("6. Video comparison and 7. Transformation findings", H1))
    rows = [["Parent", "Child", "Transformation", "dHash matched frames", "Audio MD5 identical"]]
    for e in g["edges"][:14]: rows.append([e["source"][-14:], e["target"][-14:], e["label"], f"{e['sims'].get('dhash_match_fraction', 0):.2f}" if "dhash_match_fraction" in e["sims"] else "-", str(e["sims"].get("audio_md5_identical", "-"))])
    s += [tbl(rows, [100, 100, 100, 110, 110]), P("dHash matched fraction: share of 24 sampled frames with a frame within 8 of 64 bits in the other video (measurement from data/derived/features; not a model score). Editing is not synthetic-media manipulation: these variants are FFmpeg edits.", sm), Paragraph("8. Evidence ledger", H1)]
    led = LEDGER(); evs = sorted({x for e in g["edges"] for x in e["evidence_ids"]})[:20]
    s.append(tbl([["Evidence ID", "Type", "Claim supported", "Status"]] + [[x.evidence_id, x.evidence_type, x.claim_supported, x.claim_status] for x in led[led.evidence_id.isin(evs)].itertuples()] if evs else [["Evidence", "none linked"]], [95, 100, 255, 80]))
    o = OBS(); oo = o[o.media_id == root]
    s += [Paragraph("9. Distribution timeline and 10. Campaign analysis", H1), P("Platform observations for the reference: " + ("; ".join(f"{x.platform} {x.observation_type} {x.publish_time_utc or x.observation_time_utc}" for x in oo.itertuples()) or "none") + ". Campaign analysis: not assessed. No account-level coordination data exists for this video and campaign_candidate_clusters is empty.")]
    s += [Paragraph("11. Investigator observations", H1), tbl([["When", "Reviewer", "Edge / item", "Decision", "Note"]] + [[x["ts"], x["actor"], x["edge_key"], x["decision"], x["note"]] for x in revs], [85, 90, 140, 55, 160]) if revs else P("No review decisions recorded for this investigation."),
          Paragraph("12. Uncertainty and limitations", H1), P("Relationships come from the controlled transformation log, so they are certain by construction for these variants, but say nothing about natural, unlabelled copies. The only measured detector is the non-learned dHash baseline (test AUC 0.83). No trained ORVEX model, OCR, speech or embedding evidence exists yet. Similarity is not proof of derivation, and derivation is not proof of coordination."),
          Paragraph("13. Final investigator conclusion", H1), P(r["summary"] or "No conclusion has been recorded by the investigator."), P("Investigator hypothesis (not a finding): " + (r["hypothesis"] or "none recorded"), sm)]
    doc.build(s); return Response(out.getvalue(), media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename=ORVEX_investigation_{iid}.pdf"})

import threading
def _warm():
    for f in (M, LOCAL, VAR, EDGES, LEDGER, PAIRS, OBS, HASH, AUD, families): f()
    media("RW-CMN-P10491224"); _QC.setdefault("v", _quality())
threading.Thread(target=_warm, daemon=True).start()
