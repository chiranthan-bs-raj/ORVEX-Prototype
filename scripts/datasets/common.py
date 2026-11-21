# -*- coding: utf-8 -*-
import os, sys, json, csv, hashlib, subprocess, datetime, glob, time
sys.path.insert(0, os.path.dirname(__file__))
import schema

ROOT = os.environ.get("ORVEX_ROOT") or os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))   # repository root (was a fixed laptop path)
DATA = os.path.join(ROOT, "data")
RW = os.path.join(DATA, "real_world"); RWMETA = os.path.join(RW, "raw_metadata"); RWMEDIA = os.path.join(RW, "media")
CV = os.path.join(DATA, "controlled_variants"); CVMEDIA = os.path.join(CV, "media")
TAB = os.path.join(DATA, "derived", "tables"); FEAT = os.path.join(DATA, "derived", "features"); SPL = os.path.join(DATA, "derived", "splits")
MAN = os.path.join(DATA, "manifests"); REP = os.path.join(DATA, "reports"); DOCS = os.path.join(ROOT, "docs", "datasets")
BUILD = os.path.join(DATA, "manifests", "_build")
FFBIN = glob.glob(os.path.join(ROOT, "tools", "ffmpeg-*", "bin"))
FFMPEG = os.path.join(FFBIN[0], "ffmpeg.exe") if FFBIN else "ffmpeg"; FFPROBE = os.path.join(FFBIN[0], "ffprobe.exe") if FFBIN else "ffprobe"
UA = {"User-Agent": "ORVEX-research/0.1 (academic prototype; contact: %s)" % os.environ.get("ORVEX_CONTACT", "set ORVEX_CONTACT")}
FONT = "C\\:/Windows/Fonts/arial.ttf"

# ---- storage budget (bytes). Dataset payload = everything under data/ (media, variants, features, manifests, reports, tables, temp)
GB = 10 ** 9
CAP_HARD, CAP_TARGET, CAP_STOP = 30 * GB, 27 * GB, 29 * GB
ALLOC = dict(real_world_metadata=0.4 * GB, commons_media=3.0 * GB, anakin_subset=3.0 * GB, controlled_variants=14.0 * GB, derived_features_tables=1.0 * GB)

def now(): return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
def dir_bytes(p):
    t = 0
    for r, _, fs in os.walk(p):
        for f in fs:
            try: t += os.path.getsize(os.path.join(r, f))
            except OSError: pass
    return t
def payload_bytes(): return dir_bytes(DATA)
def budget_ok(extra=0): return payload_bytes() + extra < CAP_STOP
def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""): h.update(c)
    return h.hexdigest()
def rel(p): return os.path.relpath(p, ROOT).replace("\\", "/")

def probe(path):
    r = subprocess.run([FFPROBE, "-v", "error", "-print_format", "json", "-show_format", "-show_streams", path], capture_output=True, text=True, encoding="utf-8", errors="replace")
    try: j = json.loads(r.stdout)
    except Exception: return None
    v = next((s for s in j.get("streams", []) if s.get("codec_type") == "video"), None); a = next((s for s in j.get("streams", []) if s.get("codec_type") == "audio"), None)
    def fr(s):
        try: n, d = s.split("/"); return round(float(n) / float(d), 3) if float(d) else 0.0
        except Exception: return 0.0
    try: dur = round(float(j["format"].get("duration")), 3)
    except Exception: dur = None
    return dict(duration_s=dur, width=v and v.get("width"), height=v and v.get("height"), fps=v and fr(v.get("avg_frame_rate", "0/1")), video_codec=v and v.get("codec_name"),
                has_audio=a is not None, audio_codec=a and a.get("codec_name"), container=j["format"].get("format_name"))
def decode_errors(path):
    r = subprocess.run([FFMPEG, "-v", "error", "-i", path, "-f", "null", "-"], capture_output=True, text=True, errors="replace"); return (r.stderr or "").strip()[:200]
def ffmpeg_version():
    r = subprocess.run([FFMPEG, "-version"], capture_output=True, text=True); return (r.stdout.splitlines() or ["unknown"])[0]
def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace"); return r.returncode, (r.stderr or "")[-400:]

def conform(table, rows):
    cols = schema.cols(table); out = []
    for r in rows:
        extra = set(r) - set(cols)
        if extra: raise ValueError(f"{table}: columns not in contract: {sorted(extra)}")
        out.append({c: r.get(c, "") for c in cols})
    return out
def emit(table, rows, path=None):
    p = path or os.path.join(ROOT, schema.TABLES[table]["path"]); os.makedirs(os.path.dirname(p), exist_ok=True)
    rows = conform(table, rows); cols = schema.cols(table)
    with open(p, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
    return p
def load(table):
    p = os.path.join(ROOT, schema.TABLES[table]["path"])
    return list(csv.DictReader(open(p, encoding="utf-8-sig"))) if os.path.exists(p) else []

class AccessLog:
    """Append-only log of every download/access attempt (flushed into download_access_attempt_log)."""
    path = os.path.join(BUILD, "access_log.jsonl")
    @classmethod
    def add(cls, **kw):
        os.makedirs(BUILD, exist_ok=True)
        rec = dict(attempt_time_utc=now(), method="http_get", retry_count=0, terms_decision="permitted_by_licence_or_open_access"); rec.update(kw)
        with open(cls.path, "a", encoding="utf-8") as f: f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    @classmethod
    def all(cls):
        return [json.loads(l) for l in open(cls.path, encoding="utf-8")] if os.path.exists(cls.path) else []

def http_get(url, dest, source_dataset_id, item_id="", retries=4, timeout=180):
    """Download with retries, log every attempt. Returns (ok, bytes)."""
    import requests
    for i in range(retries):
        try:
            r = requests.get(url, headers=UA, timeout=timeout); sc = r.status_code
            if sc == 200:
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                with open(dest, "wb") as f: f.write(r.content)
                AccessLog.add(source_dataset_id=source_dataset_id, media_or_file_id=item_id, url=url, http_status=sc, result_category="ok", bytes=len(r.content),
                              sha256=hashlib.sha256(r.content).hexdigest(), final_status="downloaded_authorized", retry_count=i, note="")
                return True, len(r.content)
            AccessLog.add(source_dataset_id=source_dataset_id, media_or_file_id=item_id, url=url, http_status=sc, result_category="failed", bytes=0, sha256="",
                          final_status="not_found" if sc == 404 else "access_not_available", retry_count=i, note=f"HTTP {sc}")
            if sc in (403, 404, 410): return False, 0
        except Exception as e:
            AccessLog.add(source_dataset_id=source_dataset_id, media_or_file_id=item_id, url=url, http_status="", result_category="failed", bytes=0, sha256="",
                          final_status="retry_pending", retry_count=i, note=str(e)[:150])
        time.sleep(6 * (i + 1))
    return False, 0
