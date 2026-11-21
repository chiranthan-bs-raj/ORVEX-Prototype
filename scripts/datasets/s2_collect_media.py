# -*- coding: utf-8 -*-
"""Gate 2: obtain authorised real-world media.
A) Wikimedia Commons: only files whose machine-readable licence is CC0 / Public domain / CC BY / CC BY-SA (derivatives + redistribution permitted with attribution).
B) ANAKIN (cc-by-4.0 per its official card): stratified subset of (trimmed, edited[, masks]) pairs - real human-edited videos.
Budget-guarded; resumable; every attempt logged."""
import os, sys, re, json, html, time, hashlib, requests, pandas as pd
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(__file__))
from common import *

CMN_DIR = os.path.join(RWMEDIA, "commons"); ANK_DIR = os.path.join(RWMEDIA, "anakin"); CMN_META = os.path.join(RWMETA, "commons")
API = "https://commons.wikimedia.org/w/api.php"
OK_LIC = re.compile(r"^(CC0|Public domain|CC BY(?!-NC)(?!-ND)|CC BY-SA)", re.I); BAD = re.compile(r"(-NC|-ND| NC| ND)", re.I)
QUERIES = [("speech", "speech"), ("speech", "address to the nation"), ("interview", "interview"), ("press", "press conference"), ("news", "news report"),
 ("lecture", "lecture"), ("protest", "protest march"), ("street", "street scene"), ("traffic", "traffic"), ("market", "market"), ("wildlife", "wildlife"),
 ("animals", "animals zoo"), ("sports", "football match"), ("sports", "athletics"), ("music", "concert"), ("festival", "festival parade"), ("cooking", "cooking"),
 ("science", "experiment"), ("space", "NASA"), ("nature", "waterfall"), ("transport", "train"), ("city", "timelapse city"), ("workshop", "craft workshop"),
 ("education", "classroom"), ("ceremony", "ceremony"), ("disaster", "flood"), ("tutorial", "tutorial"), ("history", "archival footage 1960s")]
def clean(s): return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()

def search(kw, off):
    p = dict(action="query", format="json", generator="search", gsrnamespace=6, gsrsearch=f"filetype:video {kw}", gsrlimit=50, gsroffset=off,
             prop="imageinfo|categories", iiprop="url|size|mime|extmetadata|timestamp|sha1|user|comment",
             iiextmetadatafilter="LicenseShortName|LicenseUrl|UsageTerms|Artist|Credit|AttributionRequired|DateTimeOriginal|ImageDescription", cllimit="max")
    for i in range(4):
        try:
            r = requests.get(API, params=p, headers=UA, timeout=60); r.raise_for_status()
            AccessLog.add(source_dataset_id="RW-01", media_or_file_id=f"search:{kw}:{off}", url=r.url[:300], http_status=200, result_category="ok", bytes=len(r.content), sha256="", final_status="downloaded_authorized", retry_count=i, method="api", note="")
            return list(r.json().get("query", {}).get("pages", {}).values())
        except Exception as e: time.sleep(5 * (i + 1))
    return []

def cand(pg):
    ii = (pg.get("imageinfo") or [None])[0]
    if not ii: return None
    em = ii.get("extmetadata", {}); lic = clean(em.get("LicenseShortName", {}).get("value", ""))
    if not lic or not OK_LIC.match(lic) or BAD.search(lic): return None
    if ii["mime"] not in ("video/webm", "video/ogg", "application/ogg", "video/mp4"): return None
    if not (300_000 <= ii["size"] <= 45_000_000): return None
    return dict(pageid=pg["pageid"], title=pg["title"], url=ii["url"].split("?")[0], page_url=ii["descriptionurl"], mime=ii["mime"], size=ii["size"], uploaded=ii.get("timestamp", ""),
                uploader=ii.get("user", ""), upload_comment=ii.get("comment", ""), commons_sha1=ii.get("sha1", ""), license=lic, license_url=clean(em.get("LicenseUrl", {}).get("value", "")),
                author=clean(em.get("Artist", {}).get("value", "")), credit=clean(em.get("Credit", {}).get("value", "")), attribution_required=clean(em.get("AttributionRequired", {}).get("value", "")),
                description=clean(em.get("ImageDescription", {}).get("value", ""))[:400], categories=[c["title"].replace("Category:", "") for c in pg.get("categories", [])][:12])

def commons(max_total=96, per_query=4):
    os.makedirs(CMN_DIR, exist_ok=True); os.makedirs(CMN_META, exist_ok=True)
    mp = os.path.join(CMN_META, "commons_candidates.json")
    if os.path.exists(mp): chosen = json.load(open(mp, encoding="utf-8"))
    else:
        chosen, seen, stems = [], set(), set()
        for dom, kw in QUERIES:
            got = 0
            for off in (0, 50):
                for pg in search(kw, off):
                    c = cand(pg)
                    if not c or c["pageid"] in seen: continue
                    stem = re.sub(r"[\d\W_]+", "", c["title"].lower())[:18]
                    if stem in stems: continue
                    seen.add(c["pageid"]); stems.add(stem); c.update(domain=dom, query=kw); chosen.append(c); got += 1
                    if got >= per_query: break
                if got >= per_query: break
                time.sleep(0.5)
            if len(chosen) >= max_total: break
        # global usage (real reuse signal) in batches
        ids = [str(c["pageid"]) for c in chosen]; gu = {}
        for i in range(0, len(ids), 40):
            try:
                r = requests.get(API, params=dict(action="query", format="json", pageids="|".join(ids[i:i + 40]), prop="globalusage", gulimit="max"), headers=UA, timeout=60)
                for pid, pg in r.json().get("query", {}).get("pages", {}).items(): gu[pid] = len(pg.get("globalusage", []))
            except Exception: pass
            time.sleep(0.5)
        for c in chosen: c["global_usage_count"] = gu.get(str(c["pageid"]), "")
        json.dump(chosen, open(mp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    def dl(c):
        ext = os.path.splitext(c["url"])[1].lower() or ".webm"; c["media_id"] = f"RW-CMN-P{c['pageid']}"; c["local_file"] = f"{c['media_id']}{ext}"
        dest = os.path.join(CMN_DIR, c["local_file"])
        if os.path.exists(dest): return
        if not budget_ok(c["size"]): AccessLog.add(source_dataset_id="RW-01", media_or_file_id=c["media_id"], url=c["url"], http_status="", result_category="skipped_budget", bytes=0, sha256="", final_status="retry_pending", note="budget guard"); return
        http_get(c["url"], dest, "RW-01", c["media_id"]); time.sleep(0.4)
    with ThreadPoolExecutor(max_workers=3) as ex: list(ex.map(dl, chosen))
    for c in chosen:
        ext = os.path.splitext(c["url"])[1].lower() or ".webm"; c["media_id"] = f"RW-CMN-P{c['pageid']}"; c["local_file"] = f"{c['media_id']}{ext}"
    json.dump(chosen, open(mp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("commons candidates", len(chosen), "files", len(os.listdir(CMN_DIR)))

def anakin(per_type=50, max_bytes=ALLOC["anakin_subset"]):
    os.makedirs(os.path.join(ANK_DIR, "trimmed"), exist_ok=True); os.makedirs(os.path.join(ANK_DIR, "edited"), exist_ok=True); os.makedirs(os.path.join(ANK_DIR, "masks"), exist_ok=True)
    meta = pd.read_csv(os.path.join(RWMETA, "hf_api", "anakin_metadata.csv")); blobs = json.load(open(os.path.join(RWMETA, "hf_api", "anakin_blobs.json"), encoding="utf-8"))
    size = {x["rfilename"]: x.get("size") or 0 for x in blobs["siblings"]}
    meta["h"] = meta["video-id"].map(lambda v: hashlib.sha256(("orvex-anakin-v1" + v).encode()).hexdigest())
    meta = meta[meta.apply(lambda r: f"edited/{r['video-id']}.mp4" in size and f"trimmed/{r['video-id']}.mp4" in size, axis=1)]
    sel = meta.sort_values("h").groupby("manipulation-type").head(per_type)
    tot = 0; keep = []
    for _, r in sel.sort_values("h").iterrows():
        v = r["video-id"]; b = size[f"edited/{v}.mp4"] + size[f"trimmed/{v}.mp4"] + (size.get(f"masks/{v}.zip", 0) if r["has-masks"] else 0)
        if tot + b > max_bytes: continue
        tot += b; keep.append(v)
    sel = sel[sel["video-id"].isin(keep)]; sel.drop(columns=["h"]).to_csv(os.path.join(RWMETA, "hf_api", "anakin_selected_subset.csv"), index=False)
    print("anakin selected", len(sel), "planned bytes", tot)
    base = "https://huggingface.co/datasets/AlexBlck/ANAKIN/resolve/main/"
    jobs = []
    for _, r in sel.iterrows():
        v = r["video-id"]; jobs += [(f"RW-ANK-{v}-T", base + f"trimmed/{v}.mp4", os.path.join(ANK_DIR, "trimmed", v + ".mp4")), (f"RW-ANK-{v}-E", base + f"edited/{v}.mp4", os.path.join(ANK_DIR, "edited", v + ".mp4"))]
        if r["has-masks"]: jobs.append((f"RW-ANK-{v}-M", base + f"masks/{v}.zip", os.path.join(ANK_DIR, "masks", v + ".zip")))
    def dl(j):
        mid, url, dest = j
        if os.path.exists(dest) and os.path.getsize(dest) > 0: return
        if not budget_ok(): return
        http_get(url, dest, "RW-02", mid, timeout=300)
    with ThreadPoolExecutor(max_workers=4) as ex: list(ex.map(dl, jobs))
    print("anakin files", sum(len(fs) for _, _, fs in os.walk(ANK_DIR)))

if __name__ == "__main__":
    print("payload before:", payload_bytes())
    commons(); anakin()
    print("payload after:", payload_bytes())
