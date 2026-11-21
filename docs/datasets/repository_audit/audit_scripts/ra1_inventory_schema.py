# -*- coding: utf-8 -*-
"""READ-ONLY. (1) file manifest of the whole repository, (2) independent ffprobe of every media file, (3) hash verification vs checksums manifest,
(4) schema + per-column statistics of every structured file, (5) column dictionary rows."""
import sys, os, json, re, time, random, collections
sys.path.insert(0, os.path.dirname(__file__))
from ra_common import *
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, str(ROOT / "scripts" / "datasets"))
import schema as PSCHEMA

# ------------------------------------------------------------------ 1. file manifest
rows = []
for r, ds, fs in os.walk(ROOT):
    if os.sep + "__pycache__" in r or os.sep + "repository_audit" in r: continue
    for f in fs:
        p = Path(r) / f
        try: st = p.stat()
        except OSError: continue
        rows.append(dict(path=rel(p), bytes=st.st_size, ext=p.suffix.lower(), top=rel(p).split("/")[0], symlink=os.path.islink(p), mtime=time.strftime("%Y-%m-%d %H:%M", time.localtime(st.st_mtime))))
FM = pd.DataFrame(rows); FM.to_csv(safe_out("repository_file_manifest.csv"), index=False, encoding="utf-8-sig")
print("files in repository (excluding audit output and __pycache__):", len(FM), "bytes", FM["bytes"].sum())

# ------------------------------------------------------------------ 2. independent ffprobe of all media
MEDIA_EXT = {".mp4", ".webm", ".ogv", ".ogg", ".mkv", ".mov"}
media = FM[FM["ext"].isin(MEDIA_EXT) & FM["path"].str.startswith("data/")]
def comp(p):
    if p.startswith("data/real_world/media/commons/"): return "commons_originals"
    if p.startswith("data/real_world/media/anakin/trimmed/"): return "anakin_trimmed"
    if p.startswith("data/real_world/media/anakin/edited/"): return "anakin_edited"
    if p.startswith("data/controlled_variants/media/"): return "controlled_variants"
    return "other_media"
def probe(p):
    r = subprocess.run([FFPROBE, "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(ROOT / p)], capture_output=True, text=True, encoding="utf-8", errors="replace")
    try: j = json.loads(r.stdout)
    except Exception: return dict(path=p, readable=False)
    v = next((s for s in j.get("streams", []) if s["codec_type"] == "video"), None); a = next((s for s in j.get("streams", []) if s["codec_type"] == "audio"), None)
    try: d = float(j["format"].get("duration", 0) or 0)
    except Exception: d = 0.0
    def fr(s):
        try: n, dd = s.split("/"); return round(float(n) / float(dd), 3) if float(dd) else 0.0
        except Exception: return 0.0
    return dict(path=p, readable=bool(v) and d > 0, duration_s=round(d, 3), width=v and v.get("width"), height=v and v.get("height"), fps=v and fr(v.get("avg_frame_rate", "0/1")), vcodec=v and v.get("codec_name"), has_audio=a is not None, container=j["format"].get("format_name"))
with ThreadPoolExecutor(max_workers=8) as ex: PR = list(ex.map(probe, media["path"]))
MP = pd.DataFrame(PR).merge(media[["path", "bytes"]], on="path"); MP["component"] = MP["path"].map(comp); MP.to_csv(safe_out("media_probe_results.csv"), index=False, encoding="utf-8-sig")
print(MP.groupby("component").agg(files=("path", "size"), readable=("readable", "sum"), hours=("duration_s", lambda s: round(s.sum() / 3600, 2))).to_string())

# ------------------------------------------------------------------ 3. hash verification against checksums manifest
exp = {}
for l in open(ROOT / "data/manifests/checksums.sha256", encoding="utf-8"):
    h, _, p = l.rstrip("\n").partition("  ")
    if p: exp[p] = h
random.seed(20261027)
pick = [p for p in media["path"] if comp(p) in ("commons_originals", "anakin_trimmed", "anakin_edited")]
var = [p for p in media["path"] if comp(p) == "controlled_variants"]; pick += random.sample(var, min(200, len(var)))
def chk(p): return p, (sha256_file(ROOT / p) == exp.get(p)) if p in exp else None
with ThreadPoolExecutor(max_workers=6) as ex: HV = list(ex.map(chk, pick))
hv = dict(checked=len(HV), match=sum(1 for _, ok in HV if ok is True), mismatch=sum(1 for _, ok in HV if ok is False), not_in_manifest=sum(1 for _, ok in HV if ok is None), manifest_lines=len(exp),
          scope="all Commons + ANAKIN media files and a seeded random sample of 200 controlled variants (re-hashed now)", mismatches=[p for p, ok in HV if ok is False][:10])
manifest_files = set(exp); disk_files = set(FM[FM["path"].str.startswith(("data/real_world", "data/controlled_variants", "data/derived", "data/manifests"))]["path"]) - {"data/manifests/checksums.sha256"}
disk_files = {p for p in disk_files if "/_build/" not in p and not re.search(r"_run\d*\.log$", p)}
hv["on_disk_not_in_manifest"] = sorted(disk_files - manifest_files)[:20]; hv["in_manifest_not_on_disk"] = sorted(manifest_files - set(FM["path"]))[:20]
json.dump(hv, open(WORK / "hash_verification.json", "w"), indent=1); print("hash verification:", hv)

# ------------------------------------------------------------------ 4. schema inspection
SENS = {"publisher_account_id", "uploader", "uploader_username", "channel_id", "author", "credit", "author_or_credit", "Channel", "editor-id", "account_id_pseudonym"}
ISO = re.compile(r"^\d{4}-\d{2}-\d{2}([T ]\d{1,2}:\d{2}(:\d{2})?)?Z?$")
def infer(vals):
    if len(vals) == 0: return "empty"
    s = pd.Series(vals)
    if s.str.fullmatch(r"-?\d+").all(): return "int"
    if s.str.fullmatch(r"-?\d+(\.\d+)?([eE][-+]?\d+)?").all(): return "float"
    if s.isin(["True", "False", "TRUE", "FALSE", "true", "false"]).all(): return "bool"
    if s.str.match(ISO).all(): return "datetime"
    if s.str.match(r"^[\[{]").all(): return "json-in-string"
    return "str"
def col_stats(df):
    out = {}
    for c in df.columns:
        s = df[c].astype(str); nn = s[(s != "") & (s != "nan") & (s != "None")]
        ex = nn.iloc[0][:50] if len(nn) else ""
        out[c] = dict(rows=len(df), null_count=int(len(df) - len(nn)), null_pct=round((len(df) - len(nn)) / max(len(df), 1) * 100, 2), distinct=int(nn.nunique()), inferred_type=infer(nn.head(5000).tolist()) if len(nn) else "empty",
                      example="[masked]" if c in SENS and ex else ex, min=None, max=None)
    return out
def json_schema(obj, path="$", acc=None, depth=0, cap=200):
    acc = acc if acc is not None else collections.defaultdict(lambda: dict(types=collections.Counter(), example=None, count=0))
    a = acc[path]; a["types"][type(obj).__name__] += 1; a["count"] += 1
    if a["example"] is None and not isinstance(obj, (dict, list)): a["example"] = str(obj)[:50]
    if depth > 6: return acc
    if isinstance(obj, dict):
        ks = list(obj)
        if len(ks) > 30:
            acc[path + ".<key>"]["count"] += len(ks)
            for k in ks[:cap]: json_schema(obj[k], path + ".<key>", acc, depth + 1, cap)
        else:
            for k in ks: json_schema(obj[k], f"{path}.{k}", acc, depth + 1, cap)
    elif isinstance(obj, list):
        for x in obj[:cap]: json_schema(x, path + "[]", acc, depth + 1, cap)
    return acc
FILES = []   # structured files to inspect
for p in FM["path"]:
    low = p.lower()
    if low.startswith(("data/", "docs/datasets/", "orvex_literature/")) or low.endswith(".xlsx"):
        if low.endswith((".csv", ".tsv", ".csv.gz", ".json", ".jsonl", ".xlsx", ".sha256")) or low.endswith(("youtube_ids.txt", "done_sources.txt", "eligible_titles.txt")): FILES.append(p)
    elif low.endswith(".xlsx"): FILES.append(p)
SCH = {}; COLS = []
GROUPS = {}   # group homogeneous JSON files
for p in sorted(set(FILES)):
    full = ROOT / p; low = p.lower(); ent = dict(path=p, bytes=full.stat().st_size)
    try:
        if low.endswith((".csv", ".tsv", ".csv.gz")):
            df = read_table(full); ent.update(kind="tabular", rows=len(df), columns=list(df.columns), stats=col_stats(df))
            ent["dup_rows"] = int(df.duplicated().sum()) if len(df) < 400000 else None
            const = [c for c in df.columns if df[c].nunique() <= 1]; ent["constant_cols"] = const
            seen = {}; dups = []
            if len(df) < 400000 and len(df.columns) < 80:
                for c in df.columns:
                    k = hash(tuple(df[c].head(3000)))
                    if k in seen and df[c].equals(df[seen[k]]): dups.append((c, seen[k]))
                    seen.setdefault(k, c)
            ent["duplicate_cols"] = dups
        elif low.endswith(".jsonl"):
            n = 0; sample = []
            for l in open(full, encoding="utf-8"):
                n += 1
                if len(sample) < 500: sample.append(json.loads(l))
            acc = None
            for o in sample: acc = json_schema(o, "$", acc)
            ent.update(kind="jsonl", records=n, schema={k: dict(types=dict(v["types"]), example=v["example"], count=v["count"]) for k, v in acc.items()})
        elif low.endswith(".json"):
            if "/_build/variants/" in p:
                GROUPS.setdefault("data/manifests/_build/variants/*.json", []).append(p); continue
            if "/zenodo_api/" in p:
                GROUPS.setdefault("data/real_world/raw_metadata/zenodo_api/*.json", []).append(p); continue
            obj = json.load(open(full, encoding="utf-8")); acc = json_schema(obj)
            ent.update(kind="json", schema={k: dict(types=dict(v["types"]), example=v["example"], count=v["count"]) for k, v in acc.items()}, top_level=type(obj).__name__, top_len=len(obj) if hasattr(obj, "__len__") else None)
        elif low.endswith(".xlsx"):
            import openpyxl
            wb = openpyxl.load_workbook(full, read_only=True, data_only=True); sheets = {}
            for ws in wb.worksheets:
                rws = list(ws.iter_rows(values_only=True)); head = max(range(min(8, len(rws))), key=lambda i: sum(1 for c in rws[i] if c not in (None, ""))) if rws else 0
                hdr = [str(c) for c in rws[head] if c not in (None, "")] if rws else []; body = rws[head + 1:]
                st = {}
                for j, h in enumerate(hdr):
                    vals = [str(r[j]) for r in body if j < len(r) and r[j] not in (None, "")]; st[h] = dict(rows=len(body), null_count=len(body) - len(vals), null_pct=round((len(body) - len(vals)) / max(len(body), 1) * 100, 2), distinct=len(set(vals)), inferred_type=infer(vals[:2000]) if vals else "empty", example=(vals[0][:50] if vals else ""))
                sheets[ws.title] = dict(header_row=head + 1, rows=len(body), columns=hdr, stats=st)
            ent.update(kind="xlsx", sheets=sheets)
        else:   # plain lists / hash manifest
            lines = [l.rstrip("\n") for l in open(full, encoding="utf-8")]; ent.update(kind="text-list", rows=len(lines), example=lines[0][:70] if lines else "")
        SCH[p] = ent
    except Exception as e:
        SCH[p] = dict(path=p, kind="error", error=str(e)[:150])
for g, ps in GROUPS.items():
    acc = None; n = 0
    for p in ps:
        o = json.load(open(ROOT / p, encoding="utf-8")); acc = json_schema(o, "$", acc); n += 1
    SCH[g] = dict(path=g, kind="json-group", files=n, bytes=sum((ROOT / p).stat().st_size for p in ps), schema={k: dict(types=dict(v["types"]), example=v["example"], count=v["count"]) for k, v in acc.items()})
json.dump(SCH, open(WORK / "schema_inspection.json", "w"), indent=1, default=str); print("structured files inspected:", len(SCH), "errors:", [k for k, v in SCH.items() if v["kind"] == "error"])
