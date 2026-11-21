# -*- coding: utf-8 -*-
"""Gate 3: normalise native schemas -> ORVEX schema, QC, dedupe, native edges, observations, evidence, registry.
Native files are never modified: they stay in data/real_world/raw_metadata/. Nulls are used (with missingness_note) instead of guessed values."""
import os, sys, re, csv, json, hashlib, urllib.parse, itertools
import datetime
import numpy as np, pandas as pd, cv2
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(__file__))
from common import *
import candidates

NOW = now(); M = []; OBS = []; EV = []; EDGES = []; DUP = []
CMN_DIR = os.path.join(RWMEDIA, "commons"); ANK_DIR = os.path.join(RWMEDIA, "anakin"); X = os.path.join(RWMETA)
SEARCH_DATE = "2026-10-26"

def host(u):
    try: h = urllib.parse.urlparse(u).netloc.lower().replace("www.", "")
    except Exception: return None
    return {"youtube.com": "youtube", "youtu.be": "youtube", "facebook.com": "facebook", "twitter.com": "twitter", "x.com": "twitter", "vimeo.com": "vimeo", "bilibili.com": "bilibili"}.get(h, h or None)
def pid_from_url(u):
    try:
        p = urllib.parse.urlparse(u); q = urllib.parse.parse_qs(p.query)
        if "v" in q: return q["v"][0]
        m = re.search(r"/(videos?|status|watch)/(\d+)", p.path) or re.search(r"/(\d{6,})/?$", p.path) or re.search(r"/(BV[A-Za-z0-9]+)", p.path)
        if m: return m.group(m.lastindex)
        return p.path.strip("/").split("/")[-1] or None
    except Exception: return None
def canon(u):
    try:
        p = urllib.parse.urlparse(u.strip()); q = urllib.parse.parse_qs(p.query); h = host(u) or p.netloc
        if h == "youtube" and "v" in q: return f"https://youtube.com/watch?v={q['v'][0]}"
        return f"https://{p.netloc.lower().replace('www.', '')}{p.path.rstrip('/')}"
    except Exception: return u
def mrow(**k):
    base = dict(release_version="", native_record_id="", native_media_id="", platform="", platform_media_id="", source_url="", canonical_url="", title="", description_caption="", publisher_account_id="",
                event_or_cascade_id="", published_time_utc="", observed_time_utc="", collected_time_utc=NOW, time_precision="unknown", duration_s="", width="", height="", fps="", video_codec="", audio_codec="",
                has_audio="", container="", file_bytes="", local_path="", sha256="", access_status="metadata_only", playable_status="not_checked", rights_status="", license="", license_url="", attribution="",
                record_origin="real_world_source_record", media_origin="not_applicable_metadata_only", native_authenticity_label="", native_misleading_label="", native_manipulation_type="",
                normalized_authenticity_status="unknown", normalized_misleading_status="not_assessed", annotation_status="none", qc_flags="", duplicate_of_media_id="", usable_for_variants=False, missingness_note="", coordination_status="not_assessed", evidence_id="", perceptual_hash_ref="")
    base.update(k); return base

def evid(eid, etype, ds, stype, sid, url, ref, claim, status, fact, method, path=None, perm="", basis="source_curated_annotation_no_calibrated_confidence", lim=""):
    EV.append(dict(evidence_id=eid, evidence_type=etype, source_dataset_id=ds, subject_type=stype, subject_id=sid, source_url=url, source_record_ref=ref, claim_supported=claim, claim_status=status,
                   observed_fact_vs_inference=fact, verification_method=method, evidence_time_utc=NOW, temporal_precision="date", file_sha256=sha256(path) if path and os.path.exists(path) else "",
                   reviewer_status="source_curated" if etype.startswith("source") else "unreviewed", permission_status=perm or "per_source_licence", confidence_basis=basis, limitations=lim))
def edge(ds, ev, a, b, na, nb, nl, ntype, direction, **k):
    e = dict(relationship_id=f"REL-{len(EDGES) + 1:07d}", source_dataset_id=ds, relation_scope="real_native", evidence_id=ev, media_a_id=a, media_b_id=b, native_media_a_id=na, native_media_b_id=nb, native_label=nl,
             normalized_relation_type=ntype, direction_status=direction, label_source="source_annotation", label_status="source_ground_truth", evidence_status="source_annotation", confidence_status="source_ground_truth_not_calibrated",
             method_version="s3_normalize.py@1", created_utc=NOW, media_available_locally=False, conflict_flag=False)
    e.update(k); EDGES.append(e)

# ===================================================================== Commons (RW-01)
SYN = re.compile(r"computer[- ]generated|animation|animated|simulat|artist.?s impression|visuali[sz]ation|SVS\d*|rendering|CGI|3D model|screencast|cartoon|diagram|cutaway", re.I)
MANUAL_NOT_REAL = {"RW-CMN-P75686004": "produced NASA JPL show mixing animation/CGI with footage", "RW-CMN-P3522226": "NASA/JPL cutaway movie (computer graphics)"}
def qc_commons():
    cands = json.load(open(os.path.join(RWMETA, "commons", "commons_candidates.json"), encoding="utf-8")); rows, H = [], {}
    def work(c):
        path = os.path.join(CMN_DIR, c["local_file"])
        if not os.path.exists(path): return c, None
        p = probe(path) or {}; err = decode_errors(path); cap = cv2.VideoCapture(path); total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0); hs = []; lum = []
        if total > 0:
            for i in np.linspace(0, max(total - 2, 0), 24).astype(int):
                cap.set(cv2.CAP_PROP_POS_FRAMES, int(i)); ok, fr = cap.read()
                if not ok: continue
                g = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY); lum.append(float(g.mean())); s = cv2.resize(g, (9, 8), interpolation=cv2.INTER_AREA)
                hs.append(int("".join("1" if x else "0" for x in (s[:, 1:] > s[:, :-1]).flatten()), 2))
        cap.release(); return c, dict(p=p, err=err, hs=hs, lum=float(np.mean(lum)) if lum else 0.0, sha=sha256(path), bytes=os.path.getsize(path))
    with ThreadPoolExecutor(max_workers=8) as ex: res = list(ex.map(work, cands))
    ham = lambda a, b: bin(a ^ b).count("1")
    ok = [(c, r) for c, r in res if r]; drop = {}
    for (c1, r1), (c2, r2) in itertools.combinations(ok, 2):
        exact = r1["sha"] == r2["sha"]; sc = 0
        if r1["hs"] and r2["hs"] and not exact:
            sc = max(sum(1 for x in r1["hs"] if min(ham(x, y) for y in r2["hs"]) <= 8) / len(r1["hs"]), sum(1 for y in r2["hs"] if min(ham(x, y) for x in r1["hs"]) <= 8) / len(r2["hs"]))
        if exact or sc >= 0.45:
            a1 = (r1["p"].get("width") or 0) * (r1["p"].get("height") or 0); a2 = (r2["p"].get("width") or 0) * (r2["p"].get("height") or 0)
            keep, oth = (c1, c2) if a1 >= a2 else (c2, c1)
            if oth["media_id"] not in drop:
                drop[oth["media_id"]] = keep["media_id"]
                DUP.append(dict(duplicate_id=f"DUP-{len(DUP) + 1:05d}", canonical_media_id=keep["media_id"], duplicate_media_id=oth["media_id"], duplicate_type="exact_hash" if exact else "near_duplicate_perceptual",
                                evidence="sha256 equal" if exact else f"dHash24 frame match {sc:.2f} (threshold 0.45)", resolution="excluded_from_variants_original_file_kept"))
    for c, r in res:
        mid = c["media_id"]
        if not r:
            rows.append(mrow(media_id=mid, source_dataset_id="RW-01", native_record_id=str(c["pageid"]), native_media_id=c["title"], platform="wikimedia_commons", source_url=c["page_url"], canonical_url=canon(c["page_url"]),
                             title=c["title"], access_status="retry_pending", rights_status="licence_permits", license=c["license"], license_url=c["license_url"], missingness_note="file not downloaded (budget guard or network failure)")); continue
        p = r["p"]; fl = []; d = p.get("duration_s") or 0
        if not p.get("width"): fl.append("no_video_stream")
        if d < 8: fl.append("too_short(<8s)")
        if d > 120: fl.append("too_long(>120s)")
        if (p.get("height") or 0) < 240: fl.append("low_resolution(<240p)")
        if r["err"]: fl.append("decode_errors")
        if r["lum"] < 12: fl.append("mostly_black")
        if len(set(r["hs"])) <= 2 and len(r["hs"]) > 5: fl.append("static_content")
        if not p.get("has_audio"): fl.append("no_audio")
        if mid in drop: fl.append("duplicate")
        if SYN.search(c["title"] + " " + " ".join(c["categories"]) + " " + c["description"]) or mid in MANUAL_NOT_REAL: fl.append("non_real_world_synthetic_or_cgi")
        hard = {"no_video_stream", "too_short(<8s)", "too_long(>120s)", "low_resolution(<240p)", "decode_errors", "mostly_black", "static_content", "duplicate", "non_real_world_synthetic_or_cgi"}
        use = not (set(fl) & hard)
        rows.append(mrow(media_id=mid, source_dataset_id="RW-01", native_record_id=str(c["pageid"]), native_media_id=c["title"], platform="wikimedia_commons", platform_media_id=str(c["pageid"]), source_url=c["page_url"],
                         canonical_url=canon(c["page_url"]), title=c["title"], description_caption=c["description"], publisher_account_id=c["uploader"], event_or_cascade_id="", published_time_utc=c["uploaded"], time_precision="second",
                         duration_s=d, width=p.get("width"), height=p.get("height"), fps=p.get("fps"), video_codec=p.get("video_codec"), audio_codec=p.get("audio_codec"), has_audio=p.get("has_audio"), container=p.get("container"),
                         file_bytes=r["bytes"], local_path=rel(os.path.join(CMN_DIR, c["local_file"])), sha256=r["sha"], access_status="downloaded_authorized", playable_status="unplayable" if (r["err"] or not r["hs"] or not d) else "playable",
                         rights_status="licence_permits_storage_transformation_redistribution_with_attribution", license=c["license"], license_url=c["license_url"], attribution=(c["author"] or c["credit"])[:300],
                         media_origin="naturally_collected_real_world", qc_flags="|".join(fl), duplicate_of_media_id=drop.get(mid, ""), usable_for_variants=use,
                         annotation_status="none", missingness_note="no native relationship/authenticity labels in source"))
        evid(f"EV-CMN-{c['pageid']}", "license_record", "RW-01", "media", mid, c["page_url"], f"Commons API extmetadata pageid={c['pageid']}", f"licence {c['license']} permits storage/transformation with attribution",
             "source_asserted", "source_annotation", "Commons API machine-readable licence", path=os.path.join(CMN_DIR, c["local_file"]), perm="licence_permits")
        OBS.append(dict(observation_id=f"OBS-CMN-{c['pageid']}", media_id=mid, platform="wikimedia_commons", platform_post_id=str(c["pageid"]), post_url=c["page_url"],
                        account_id_pseudonym=hashlib.sha256(("orvex-pseudonym-v1" + c["uploader"]).encode()).hexdigest()[:12] if c["uploader"] else "", account_id_source_field="commons_uploader_username",
                        publish_time_utc=c["uploaded"], observation_time_utc="", time_precision="second", caption_text=c["description"], hashtags="", engagement_refs=f"commons_global_usage_count={c.get('global_usage_count', '')}",
                        metadata_source="RW-01", collection_method="official_api", order_in_cascade="", cascade_id="", access_status="downloaded_authorized", evidence_id=f"EV-CMN-{c['pageid']}",
                        limitations="upload event only; not a social-media distribution trace"))
    return rows

# ===================================================================== ANAKIN (RW-02)
def anakin_rows():
    meta = pd.read_csv(os.path.join(RWMETA, "hf_api", "anakin_metadata.csv")); sel = set(pd.read_csv(os.path.join(RWMETA, "hf_api", "anakin_selected_subset.csv"))["video-id"])
    base = "https://huggingface.co/datasets/AlexBlck/ANAKIN/resolve/main/"; rows = []
    evid("EV-ANK-meta", "source_metadata", "RW-02", "relationship_set", "ANAKIN metadata.csv", "https://huggingface.co/datasets/AlexBlck/ANAKIN/raw/main/metadata.csv", "metadata.csv", "trimmed->edited pairs, manipulation types, trim bounds",
         "source_asserted", "source_annotation", "dataset card + metadata file read", path=os.path.join(RWMETA, "hf_api", "anakin_metadata.csv"), perm="cc-by-4.0_per_card")
    for _, r in meta.iterrows():
        v = r["video-id"]; local = v in sel
        for suf, folder, kind in (("T", "trimmed", "trimmed_source_clip"), ("E", "edited", "edited")):
            path = os.path.join(ANK_DIR, folder, v + ".mp4"); have = local and os.path.exists(path); p = probe(path) if have else {}
            row = mrow(media_id=f"RW-ANK-{v}-{suf}", source_dataset_id="RW-02", native_record_id=v, native_media_id=f"{folder}/{v}.mp4", platform="huggingface_dataset", platform_media_id=v, source_url=base + f"{folder}/{v}.mp4",
                       canonical_url=base + f"{folder}/{v}.mp4", title=("" if suf == "T" else str(r["task"])), description_caption=("" if suf == "T" else str(r["task"])), publisher_account_id=("" if suf == "T" else str(r["editor-id"])),
                       event_or_cascade_id=v, access_status="downloaded_authorized" if have else "metadata_only", rights_status="cc-by-4.0_per_dataset_card_underlying_rights_unverified", license="cc-by-4.0", license_url="https://creativecommons.org/licenses/by/4.0/",
                       attribution="ANAKIN (Black et al.) https://huggingface.co/datasets/AlexBlck/ANAKIN", media_origin="real_world_human_edited_dataset" if suf == "E" else "naturally_collected_real_world",
                       native_manipulation_type=("" if suf == "T" else str(r["manipulation-type"])), normalized_authenticity_status="manipulated_human_edit_documented" if suf == "E" else "unmodified_clip_of_source_per_dataset",
                       annotation_status="source_annotation", usable_for_variants=False,
                       missingness_note=("" if have else "not selected under the budget plan (available upstream)") + ("; no per-clip publish time in source" if True else ""))
            if have:
                row.update(duration_s=p.get("duration_s"), width=p.get("width"), height=p.get("height"), fps=p.get("fps"), video_codec=p.get("video_codec"), audio_codec=p.get("audio_codec"), has_audio=p.get("has_audio"), container=p.get("container"),
                           file_bytes=os.path.getsize(path), local_path=rel(path), sha256=sha256(path), playable_status="playable" if not decode_errors(path) else "unplayable")
            rows.append(row)
        if str(r["full-available"]).upper() == "TRUE":
            rows.append(mrow(media_id=f"RW-ANK-{v}-F", source_dataset_id="RW-02", native_record_id=v, native_media_id=v, platform="vimeo", platform_media_id=pid_from_url(r["url"]), source_url=r["url"], canonical_url=canon(r["url"]),
                             event_or_cascade_id=v, access_status="metadata_only", rights_status="not_cleared_vimeo_uploader_rights", media_origin="naturally_collected_real_world", annotation_status="source_annotation",
                             missingness_note="full-length source not downloaded (44.6 GB, excluded_over_budget; Vimeo rights not cleared)"))
        has_edit_local = local and os.path.exists(os.path.join(ANK_DIR, "edited", v + ".mp4"))
        edge("RW-02", "EV-ANK-meta", f"RW-ANK-{v}-T", f"RW-ANK-{v}-E", v, v, str(r["manipulation-type"]), "edited_version_of_trimmed_clip", "directed_supported_by_source", parent_media_id=f"RW-ANK-{v}-T", child_media_id=f"RW-ANK-{v}-E",
             transformation_type=str(r["manipulation-type"]), media_available_locally=bool(has_edit_local), notes=f"editor task: {r['task']}")
        if str(r["full-available"]).upper() == "TRUE":
            edge("RW-02", "EV-ANK-meta", f"RW-ANK-{v}-F", f"RW-ANK-{v}-T", v, v, "trimmed_from_full", "trimmed_segment_of_full_video", "directed_supported_by_source", parent_media_id=f"RW-ANK-{v}-F", child_media_id=f"RW-ANK-{v}-T",
                 a_segment_start_s=r["start-time"], a_segment_end_s=r["end-time"], transformation_type="temporal_trim", media_available_locally=False, notes="segment bounds are positions inside the full Vimeo video")
    return rows

# ===================================================================== InVID FVC (RW-03/04/05)
def fvc_rows():
    rows = []; d = os.path.join(X, "invid_fvc_2018", "extracted")
    evid("EV-FVC18", "source_annotation", "RW-03", "relationship_set", "FVC.csv+FVC_dup.csv", "https://zenodo.org/records/2535479", "FVC.csv, FVC_dup.csv", "cascade membership and fake/real labels (debunked/verified)", "source_asserted", "source_annotation",
         "Zenodo record + files read (md5 verified)", path=os.path.join(X, "invid_fvc_2018", "fake-video-corpus-2018.zip"), perm="cc-by-4.0_annotations")
    lab = {"fake": ("fake", "debunked_misleading"), "real": ("real", "verified_not_misleading")}
    heads = list(csv.DictReader(open(os.path.join(d, "FVC.csv"), encoding="utf-8-sig"))); dups = list(csv.DictReader(open(os.path.join(d, "FVC_dup.csv"), encoding="utf-8-sig")))
    head_id = {}; ordc = {}
    for i, r in enumerate(heads):
        mid = f"RW-FVC18-{r['cascade_id']}-0"; head_id[r["cascade_id"]] = mid; ordc[r["cascade_id"]] = 0
        rows.append(mrow(media_id=mid, source_dataset_id="RW-03", release_version="2018", native_record_id=r["cascade_id"], native_media_id=r["video_url"], platform=host(r["video_url"]), platform_media_id=pid_from_url(r["video_url"]),
                         source_url=r["video_url"], canonical_url=canon(r["video_url"]), event_or_cascade_id=r["cascade_id"], native_authenticity_label=r["label"], native_misleading_label=r["label"],
                         normalized_misleading_status=lab.get(r["label"], ("", "not_assessed"))[1], annotation_status="source_annotation", rights_status="media_not_provided_by_source", license="cc-by-4.0 (annotations)",
                         license_url="https://creativecommons.org/licenses/by/4.0/", attribution="InVID Fake Video Corpus 2018, Papadopoulou et al., Zenodo 2535479", missingness_note="media bytes not provided; no timestamps in source (cascade order only)"))
        OBS.append(dict(observation_id=f"OBS-FVC18-{r['cascade_id']}-0", media_id=mid, platform=host(r["video_url"]), platform_post_id=pid_from_url(r["video_url"]), post_url=r["video_url"], order_in_cascade=0, cascade_id=r["cascade_id"],
                        metadata_source="RW-03", collection_method="dataset_file", access_status="metadata_only", evidence_id="EV-FVC18", time_precision="unknown", limitations="no timestamp or account in source; order is the authors' cascade order"))
    for r in dups:
        c = r["cascade_id"]; ordc[c] = ordc.get(c, 0) + 1; n = ordc[c]; mid = f"RW-FVC18-{c}-{n}"
        rows.append(mrow(media_id=mid, source_dataset_id="RW-03", release_version="2018", native_record_id=c, native_media_id=r["video_url"], platform=host(r["video_url"]), platform_media_id=pid_from_url(r["video_url"]),
                         source_url=r["video_url"], canonical_url=canon(r["video_url"]), event_or_cascade_id=c, native_authenticity_label=r["label"], native_misleading_label=r["label"],
                         normalized_misleading_status=lab.get(r["label"], ("", "not_assessed"))[1], annotation_status="source_annotation", rights_status="media_not_provided_by_source", license="cc-by-4.0 (annotations)",
                         license_url="https://creativecommons.org/licenses/by/4.0/", attribution="InVID Fake Video Corpus 2018, Papadopoulou et al., Zenodo 2535479", missingness_note="media bytes not provided; no timestamps in source (cascade order only)"))
        OBS.append(dict(observation_id=f"OBS-FVC18-{c}-{n}", media_id=mid, platform=host(r["video_url"]), platform_post_id=pid_from_url(r["video_url"]), post_url=r["video_url"], order_in_cascade=n, cascade_id=c,
                        metadata_source="RW-03", collection_method="dataset_file", access_status="metadata_only", evidence_id="EV-FVC18", time_precision="unknown", limitations="no timestamp or account in source; order is the authors' cascade order"))
        if c in head_id:
            edge("RW-03", "EV-FVC18", head_id[c], mid, c, r["video_url"], r["label"], "same_cascade_repost_or_near_duplicate", "unknown_direction", notes="membership of the same cascade as published; direction not provided")
    # older versions (mapped by canonical URL to 2018)
    c18 = {}
    for m in rows: c18.setdefault(m["canonical_url"], m["media_id"])
    for ver, ds, files in (("v2.0", "RW-04", [("invid_fvc_v2/extracted/Fake Video Corpus v2.0/fake-video-corpus - fake-videos.tsv", "fake"), ("invid_fvc_v2/extracted/Fake Video Corpus v2.0/fake-video-corpus - real-videos.tsv", "real")]),
                           ("v1.0", "RW-05", [("invid_fvc_v1/extracted/Fake Video Corpus/fake_video_corpus.tsv", "fake")])):
        evid(f"EV-FVC-{ver}", "source_annotation", ds, "relationship_set", f"FVC {ver}", f"https://zenodo.org/records/{'1147958' if ver == 'v2.0' else '242481'}", "tsv", "fake/real labels with debunk URLs", "source_asserted", "source_annotation",
             "Zenodo record + files read (md5 verified)", path=os.path.join(X, "invid_fvc_v2", "Fake_Video_Corpus_v2.0.zip") if ver == "v2.0" else os.path.join(X, "invid_fvc_v1", "Fake_Video_Corpus.zip"), perm="cc-by-4.0_annotations")
        for f, lbl in files:
            for r in csv.DictReader(open(os.path.join(X, f), encoding="utf-8-sig"), delimiter="\t"):
                url = r.get("Link", ""); mid = f"RW-FVC{ver.replace('.', '')}-{r['InVID_id']}"; cu = canon(url)
                rows.append(mrow(media_id=mid, source_dataset_id=ds, release_version=ver, native_record_id=r["InVID_id"], native_media_id=url, platform=host(url), platform_media_id=pid_from_url(url), source_url=url, canonical_url=cu,
                                 title=r.get("Title", ""), description_caption=(r.get("Comments") or r.get("Description") or "")[:500], publisher_account_id=r.get("Channel", ""), native_authenticity_label=lbl, native_misleading_label=lbl,
                                 native_manipulation_type=r.get("Type of Manipulation", ""), normalized_misleading_status=lab[lbl][1], annotation_status="source_annotation", rights_status="media_not_provided_by_source",
                                 license="cc-by-4.0 (annotations)", license_url="https://creativecommons.org/licenses/by/4.0/", attribution=f"InVID Fake Video Corpus {ver}", duplicate_of_media_id=c18.get(cu, ""),
                                 missingness_note="media bytes not provided"))
                if cu in c18:
                    DUP.append(dict(duplicate_id=f"DUP-{len(DUP) + 1:05d}", canonical_media_id=c18[cu], duplicate_media_id=mid, duplicate_type="same_url_across_versions", evidence=f"canonical URL equal: {cu}", resolution="canonical=FVC2018 record; older version kept for its extra native fields"))
    return rows

# ===================================================================== FIVR-200K (RW-06)
def fivr_rows():
    d = os.path.join(X, "invid_fivr200k", "extracted"); ev = json.load(open(os.path.join(d, "events.json"), encoding="utf-8")); ann = json.load(open(os.path.join(d, "annotation.json"), encoding="utf-8"))
    ids = [l.strip() for l in open(os.path.join(d, "youtube_ids.txt"), encoding="utf-8") if l.strip()]; emap = {}
    for i, e in enumerate(ev):
        for y in e.get("youtube", []): emap.setdefault(y, f"fivr_event_{i}")
    evid("EV-FIVR", "source_annotation", "RW-06", "relationship_set", "annotation.json", "https://zenodo.org/records/2564864", "annotation.json", "ND/DS/CS relations between query and candidate videos", "source_asserted", "source_annotation",
         "Zenodo record read (md5 verified); label definitions read in the FIVR paper", path=os.path.join(X, "invid_fivr200k", "fivr_200k_dataset.zip"), perm="cc-by-4.0_annotations")
    rows = [mrow(media_id=f"RW-FIVR-{y}", source_dataset_id="RW-06", release_version="2019", native_record_id=y, native_media_id=y, platform="youtube", platform_media_id=y, source_url=f"https://www.youtube.com/watch?v={y}",
                 canonical_url=f"https://youtube.com/watch?v={y}", event_or_cascade_id=emap.get(y, ""), annotation_status="source_annotation" if y in ann else "none", rights_status="media_not_provided_by_source", license="cc-by-4.0 (annotations)",
                 license_url="https://creativecommons.org/licenses/by/4.0/", attribution="InVID FIVR-200K, Kordopatis-Zilos et al., Zenodo 2564864", missingness_note="media bytes not provided; no timestamps/titles in release") for y in ids]
    NT = {"ND": "near_duplicate", "DS": "duplicate_scene_same_camera_footage", "CS": "complementary_scene_different_camera_same_incident"}
    for q, lab in ann.items():
        for L, vids in lab.items():
            for v in vids:
                edge("RW-06", "EV-FIVR", f"RW-FIVR-{q}", f"RW-FIVR-{v}", q, v, L, NT.get(L, L), "non_directional" if L != "ND" else "unknown_direction", notes="FIVR labels are scene/incident relations; DS/CS/IS are not proof of derivation")
    return rows

# ===================================================================== VCSL (RW-07)
def vcsl_rows():
    d = os.path.join(X, "vcsl"); urls = list(csv.reader(open(os.path.join(d, "videos_url_uuid.csv"), encoding="utf-8-sig")))[1:]; cat = json.load(open(os.path.join(d, "video_categories.json"), encoding="utf-8"))
    ucat = {u: c for c, us in cat.items() for u in us}; lab = json.load(open(os.path.join(d, "label_file_uuid_total.json"), encoding="utf-8"))
    evid("EV-VCSL", "source_annotation", "RW-07", "relationship_set", "label_file_uuid_total.json", "https://github.com/alipay/VCSL", "data/label_file_uuid_total.json", "manually annotated copied segment pairs", "source_asserted", "source_annotation",
         "GitHub raw files read; dataset licence not stated", path=os.path.join(d, "label_file_uuid_total.json"), perm="dataset_licence_not_stated_annotations_used_as_metadata_only")
    rows = [mrow(media_id=f"RW-VCSL-{u}", source_dataset_id="RW-07", release_version="main@2026-10-26", native_record_id=u, native_media_id=u, platform=host(url), platform_media_id=pid_from_url(url), source_url=url, canonical_url=canon(url),
                 title=f"VCSL category: {ucat.get(u, '')}" if ucat.get(u) else "", annotation_status="source_annotation", rights_status="dataset_licence_not_stated_media_not_downloaded", license="not stated (code MIT)",
                 attribution="VCSL, He et al., CVPR 2022", missingness_note="media bytes not downloaded: rights not cleared, platform terms") for url, u in urls]
    n = 0
    for key, segs in lab.items():
        a, b = key.split("-")
        for s in segs:
            edge("RW-07", "EV-VCSL", f"RW-VCSL-{a}", f"RW-VCSL-{b}", a, b, "copied_segment", "partial_temporal_copy", "unknown_direction", a_segment_start_s=s[0], a_segment_end_s=s[1], b_segment_start_s=s[2], b_segment_end_s=s[3],
                 transformation_type="partial_copy", notes="segment units as published (1 fps frame index per README); direction of copying not annotated")
    return rows


# ===================================================================== COVID misinformation videos (RW-31)
def covid_rows():
    p = os.path.join(X, "covid_misinfo_4557828", "covid-misinfo-videos.csv.gz"); df = pd.read_csv(p, compression="gzip", dtype=str, keep_default_na=False, low_memory=False); rows = []; seen = {}
    evid("EV-COVID", "source_annotation", "RW-31", "relationship_set", "covid-misinfo-videos.csv.gz", "https://zenodo.org/records/4557828", "all rows", "videos removed by YouTube for false COVID information and the post ids that shared them",
         "source_asserted", "source_annotation", "Zenodo record + file read (md5 verified)", path=p, perm="cc-by-4.0_metadata")
    iso = lambda s: s.strip().replace(" ", "T") if s.strip() else ""
    for _, r in df.iterrows():
        url = r["youtube_link"]; yt = pid_from_url(url); mid = f"RW-COVID-{yt}"; dup = ""
        if mid in seen:
            seen[mid] += 1; dup = mid; mid = f"{mid}-d{seen[dup]}"
            DUP.append(dict(duplicate_id=f"DUP-{len(DUP) + 1:05d}", canonical_media_id=dup, duplicate_media_id=mid, duplicate_type="same_url_within_source", evidence="repeated youtube_link in the source file",
                            resolution="canonical = first occurrence; repeat kept for its own metadata"))
        else: seen[mid] = 1
        tw = re.findall(r"\d{10,}", r["twitter_post_ids"]); fb = re.findall(r"\d{6,}", r["facebook_post_ids"]); prec = "second_timezone_unstated" if r["published_timestamp"].strip() else "unknown"
        rows.append(mrow(media_id=mid, source_dataset_id="RW-31", release_version="2021-02-23", native_record_id=yt, native_media_id=url, platform="youtube", platform_media_id=yt, source_url=url, canonical_url=canon(url),
                         title=r["video_title"][:300], description_caption=r["video_description"][:500], publisher_account_id=r["channel_id"], published_time_utc=iso(r["published_timestamp"]), time_precision=prec,
                         access_status="metadata_only", rights_status="media_not_provided_by_source", license="cc-by-4.0 (metadata)", license_url="https://creativecommons.org/licenses/by/4.0/", attribution="Knuutila, Zenodo 4557828",
                         native_misleading_label="removed_by_youtube_for_false_information (dataset definition)", normalized_misleading_status="removed_by_platform_for_false_information_per_source",
                         annotation_status="source_annotation", duplicate_of_media_id=dup, missingness_note="media not provided; timestamps/channel only for part of the videos"))
        pa = hashlib.sha256(("orvex-pseudonym-v1" + r["channel_id"]).encode()).hexdigest()[:12] if r["channel_id"] else ""
        eng = f"fb_reactions={r['facebook_graph_reactions']};fb_comments={r['facebook_graph_comments']};fb_shares={r['facebook_graph_shares']};views={r['view_count']};n_twitter_posts={len(tw)};n_facebook_posts={len(fb)}"
        tag = mid[len("RW-COVID-"):]
        OBS.append(dict(observation_id=f"OBS-COVID-{tag}-pub", observation_type="publish", media_id=mid, platform="youtube", platform_post_id=yt, post_url=url, account_id_pseudonym=pa,
                        account_id_source_field="channel_id" if pa else "", publish_time_utc=iso(r["published_timestamp"]), time_precision=prec, engagement_refs=eng, metadata_source="RW-31", collection_method="dataset_file",
                        access_status="metadata_only", evidence_id="EV-COVID", limitations="publish time/channel present only for part of the videos"))
        if r["removal_timestamp"].strip():
            OBS.append(dict(observation_id=f"OBS-COVID-{tag}-rem", observation_type="removal", media_id=mid, platform="youtube", platform_post_id=yt, post_url=url, observation_time_utc=iso(r["removal_timestamp"]),
                            time_precision="second_timezone_unstated", metadata_source="RW-31", collection_method="dataset_file", access_status="metadata_only", evidence_id="EV-COVID",
                            limitations="removal time as stated by the dataset authors (when YouTube removed the video)"))
        for t in tw:
            ms = (int(t) >> 22) + 1288834974657; ts = datetime.datetime.fromtimestamp(ms / 1000, datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            out = ts < "2019-11-01" or ts > "2020-07-01"
            OBS.append(dict(observation_id=f"OBS-COVID-{tag}-tw{t}", observation_type="share_reference", media_id=mid, platform="twitter", platform_post_id=t, post_url=f"https://twitter.com/i/web/status/{t}", publish_time_utc=ts,
                            time_precision="second_derived_unverified" if out else "second", metadata_source="RW-31", collection_method="dataset_file", access_status="metadata_only", evidence_id="EV-COVID",
                            limitations=("derived time is OUTSIDE the dataset's stated sharing window (Nov 2019-Jun 2020): treat as unverified; " if out else "") + "time derived from the tweet-id snowflake; sharing account not provided in the source"))
        for f in fb:
            OBS.append(dict(observation_id=f"OBS-COVID-{tag}-fb{f}", observation_type="share_reference", media_id=mid, platform="facebook", platform_post_id=f, time_precision="unknown", metadata_source="RW-31",
                            collection_method="dataset_file", access_status="metadata_only", evidence_id="EV-COVID", limitations="only a post id is provided: no URL, account or time"))
    return rows

def build_registry(master):
    cnt = {};
    for m in master: cnt[m["source_dataset_id"]] = cnt.get(m["source_dataset_id"], 0) + 1
    folders = {"RW-01": [os.path.join(RWMEDIA, "commons"), os.path.join(RWMETA, "commons")], "RW-02": [os.path.join(RWMEDIA, "anakin"), os.path.join(RWMETA, "hf_api")], "RW-03": [os.path.join(RWMETA, "invid_fvc_2018")],
               "RW-04": [os.path.join(RWMETA, "invid_fvc_v2")], "RW-05": [os.path.join(RWMETA, "invid_fvc_v1")], "RW-06": [os.path.join(RWMETA, "invid_fivr200k")], "RW-07": [os.path.join(RWMETA, "vcsl")], "RW-31": [os.path.join(RWMETA, "covid_misinfo_4557828")]}
    rows = []
    for c in candidates.C:
        s = c["source_dataset_id"]; ab = sum(dir_bytes(f) for f in folders.get(s, []))
        plan = {"RW-01": ALLOC["commons_media"], "RW-02": ALLOC["anakin_subset"]}.get(s, ab if c["inclusion_status"].startswith("included") or s in folders else 0)
        r = dict(c); r.update(accessed_date=SEARCH_DATE, planned_download_bytes=int(plan), actual_local_bytes=ab, record_count_local=cnt.get(s, 0)); rows.append(r)
    return rows

if __name__ == "__main__":
    master = qc_commons() + anakin_rows() + fvc_rows() + fivr_rows() + vcsl_rows() + covid_rows()
    EVMAP = {"RW-02": "EV-ANK-meta", "RW-03": "EV-FVC18", "RW-04": "EV-FVC-v2.0", "RW-05": "EV-FVC-v1.0", "RW-06": "EV-FIVR", "RW-07": "EV-VCSL", "RW-31": "EV-COVID"}
    for m in master:
        m["evidence_id"] = f"EV-CMN-{m['native_record_id']}" if m["source_dataset_id"] == "RW-01" and m["access_status"] == "downloaded_authorized" else EVMAP.get(m["source_dataset_id"], "")
        if m["local_path"]: m["perceptual_hash_ref"] = "data/derived/features/visual_dhash24.jsonl"
    for o in OBS:
        o.setdefault("observation_type", "upload" if o["observation_id"].startswith("OBS-CMN") else "cascade_member"); o["coordination_status"] = "not_assessed"
    # cross-source overlap (same platform id in different datasets): recorded, both kept (distinct native annotations)
    byplat = {}
    for m in master:
        if m["platform"] == "youtube" and m["platform_media_id"]: byplat.setdefault(m["platform_media_id"], []).append(m)
    ov = 0
    for k, ms in byplat.items():
        ds = {m["source_dataset_id"] for m in ms}
        if len(ds) > 1:
            can = sorted(ms, key=lambda m: m["source_dataset_id"])[0]
            for m in ms:
                if m is not can and m["source_dataset_id"] != can["source_dataset_id"] and not m["duplicate_of_media_id"]:
                    DUP.append(dict(duplicate_id=f"DUP-{len(DUP) + 1:05d}", canonical_media_id=can["media_id"], duplicate_media_id=m["media_id"], duplicate_type="same_platform_id_across_sources",
                                    evidence=f"youtube id {k} appears in {can['source_dataset_id']} and {m['source_dataset_id']}", resolution="both records kept (distinct native annotations); linked, not double counted in statistics")); ov += 1
    emit("real_world_media_master", master); emit("media_relationship_edges", EDGES); emit("platform_observations", OBS); emit("evidence_ledger", EV); emit("duplicate_map", DUP)
    reg = build_registry(master); emit("source_registry", reg)
    print("media", len(master), "edges", len(EDGES), "obs", len(OBS), "evidence", len(EV), "dups", len(DUP), "cross-source overlaps", ov)
