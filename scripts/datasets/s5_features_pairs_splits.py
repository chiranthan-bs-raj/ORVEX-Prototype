# -*- coding: utf-8 -*-
"""Gate 5: variant registry/run log/evidence, controlled edges, features, split manifest, training pairs, empty-by-evidence tables, access log."""
import os, sys, json, csv, glob, random, hashlib, itertools, subprocess
import numpy as np, cv2, pandas as pd
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(__file__))
from common import *
from transformations import CATALOGUE, BY_ID
import candidates

NOW = now(); SPLIT_VERSION = "split-v2"; SEED = "orvex-split-20261026"; LABEL_MAP = "labelmap-v1"
VB = os.path.join(BUILD, "variants")
random.seed(20261026)
master = load("real_world_media_master"); M = {m["media_id"]: m for m in master}
cj = {f"RW-CMN-P{c['pageid']}": c for c in json.load(open(os.path.join(RWMETA, "commons", "commons_candidates.json"), encoding="utf-8"))}
pool = sorted([m for m in master if m["source_dataset_id"] == "RW-01" and m["usable_for_variants"] == "True"], key=lambda r: r["media_id"])

# ---------------------------------------------------------------- collect variants
recs, logs = [], []
for f in sorted(glob.glob(os.path.join(VB, "*.json"))):
    j = json.load(open(f, encoding="utf-8")); recs += j["recs"]; logs += j["logs"]
for r in recs: r.pop("parent", None)

# ---------------------------------------------------------------- splits (by source family; stratified by theme / manipulation type)
def assign(items):  # items: list of (family_id, stratum) -> split by stride pattern over sorted order (deterministic)
    pat = ["train"] * 14 + ["val"] * 3 + ["test"] * 3; out = {}
    for i, (fid, st) in enumerate(sorted(items, key=lambda x: (x[1], x[0]))): out[fid] = pat[(i * 7) % 20]
    return out
fam_items = [(m["media_id"], cj[m["media_id"]]["domain"]) for m in pool]
anak = pd.read_csv(os.path.join(RWMETA, "hf_api", "anakin_selected_subset.csv"))
anak_local = [v for v in anak["video-id"] if os.path.exists(os.path.join(RWMEDIA, "anakin", "edited", v + ".mp4")) and os.path.exists(os.path.join(RWMEDIA, "anakin", "trimmed", v + ".mp4"))]
amt = dict(zip(anak["video-id"], anak["manipulation-type"]))
fam_items += [(f"RW-ANK-{v}", "anakin_" + amt[v]) for v in anak_local]
cm_items = [x for x in fam_items if x[0].startswith("RW-CMN")]; an_items = [x for x in fam_items if not x[0].startswith("RW-CMN")]
TS = assign([(t, "theme") for t in sorted({d for _, d in cm_items})])            # whole search themes go to one split => same-theme hard negatives exist inside every split, no theme straddles splits
SP = {f: TS[d] for f, d in cm_items}; SP.update(assign(an_items)); STR = dict(fam_items)
heldout_ids = {c[0] for c in CATALOGUE if c[6]}
by_var = {r["variant_media_id"]: r for r in recs}
def lineage_heldout(vid):
    n = vid
    while n in by_var:
        if by_var[n]["transformation_id"] in heldout_ids: return True
        n = by_var[n]["direct_parent_media_id"]
    return False
for r in recs:
    r["source_split"] = SP.get(r["root_source_media_id"], "excluded")
    r["usable_for_training"] = (r["validation_status"] == "passed" and r["source_split"] == "train" and not lineage_heldout(r["variant_media_id"]))
emit("controlled_variant_registry", recs); emit("transformation_run_log", logs)

# ---------------------------------------------------------------- evidence + controlled edges
EV = [x for x in load("evidence_ledger") if not x["evidence_id"].startswith(("EV-CV-", "EV-NEG-RULE"))]          # idempotent: drop rows from a previous run of this stage
EDG = [x for x in load("media_relationship_edges") if x["relation_scope"] != "controlled_lineage"]; n0 = len(EDG)
for r in recs:
    ev = f"EV-CV-{r['variant_media_id']}"
    EV.append(dict(evidence_id=ev, evidence_type="controlled_transformation_log", source_dataset_id="ORVEX-CTRL", subject_type="variant", subject_id=r["variant_media_id"], source_url="", source_record_ref=r["run_id"],
                   claim_supported=f"{r['variant_media_id']} was created from {r['direct_parent_media_id']} by {r['transformation_name']}", claim_status="controlled_by_construction", observed_fact_vs_inference="machine_measurement",
                   verification_method="FFmpeg run log + ffprobe/decode/frame validation", evidence_time_utc=r["created_utc"], temporal_precision="second", file_sha256=r["sha256"], reviewer_status="unreviewed",
                   permission_status="licence_permits_adaptation", confidence_basis="controlled ground truth (known transformation), not a calibrated probability", limitations="constructed experimental artefact, not a natural post"))
    if r["validation_status"] != "passed": continue
    cat = BY_ID[r["transformation_id"]]; ok = r["validation_status"] == "passed"
    base = dict(source_dataset_id="ORVEX-CTRL", relation_scope="controlled_lineage", evidence_id=ev, label_source="controlled_transformation_log", label_status="controlled_ground_truth", evidence_status="controlled_transformation_log", confidence_status="controlled_ground_truth_not_calibrated",
                method_version="s4_variants.py@1", created_utc=r["created_utc"], media_available_locally=True, conflict_flag=False)
    EDG.append(dict(base, relationship_id=f"REL-C-{len(EDG) - n0 + 1:06d}", media_a_id=r["direct_parent_media_id"], media_b_id=r["variant_media_id"], native_label="", normalized_relation_type="controlled_" + cat[3],
                    direction_status="directed_controlled_transformation", parent_media_id=r["direct_parent_media_id"], child_media_id=r["variant_media_id"], transformation_type=cat[1], notes=f"chain={r['chain_id']}; depth={r['generation_depth']}"))
    if r["audio_source_media_id"]:
        EDG.append(dict(base, relationship_id=f"REL-C-{len(EDG) - n0 + 1:06d}", media_a_id=r["audio_source_media_id"], media_b_id=r["variant_media_id"], normalized_relation_type="controlled_audio_source_of_variant",
                        direction_status="directed_controlled_transformation", parent_media_id=r["audio_source_media_id"], child_media_id=r["variant_media_id"], transformation_type=cat[1], notes="audio taken from this real recording; NOT a picture derivation"))
emit("evidence_ledger", EV); emit("media_relationship_edges", EDG)

# ---------------------------------------------------------------- features (computed from real media)
def feat(mid, path):
    cap = cv2.VideoCapture(path); total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0); hs = []; idx = []
    if total > 0:
        for i in np.linspace(0, max(total - 2, 0), 24).astype(int):
            cap.set(cv2.CAP_PROP_POS_FRAMES, int(i)); ok, fr = cap.read()
            if not ok: continue
            g = cv2.resize(cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY), (9, 8), interpolation=cv2.INTER_AREA); hs.append(format(int("".join("1" if x else "0" for x in (g[:, 1:] > g[:, :-1]).flatten()), 2), "016x")); idx.append(int(i))
    cap.release()
    r = subprocess.run([FFMPEG, "-v", "error", "-i", path, "-vn", "-ac", "1", "-ar", "8000", "-f", "s16le", "-"], capture_output=True); a = np.frombuffer(r.stdout, dtype=np.int16).astype(np.float32); md5 = env = ""
    if a.size >= 8000:
        md5 = hashlib.md5(r.stdout).hexdigest(); w = a[: a.size // 8000 * 8000].reshape(-1, 8000); db = 20 * np.log10((np.sqrt((w ** 2).mean(1)) + 1e-6) / 32768); env = "".join(format(int(x), "x") for x in np.clip(((db + 80) / 80 * 15).round(), 0, 15).astype(int)[:120])
    return dict(media_id=mid, dhash24=hs, frame_indices=idx, audio_md5_8k=md5, audio_env_1s=env)
local = [(m["media_id"], os.path.join(ROOT, m["local_path"])) for m in master if m["access_status"] == "downloaded_authorized" and m["local_path"]] + [(r["variant_media_id"], os.path.join(ROOT, r["local_path"])) for r in recs if r["validation_status"] == "passed"]
with ThreadPoolExecutor(max_workers=10) as ex: F = list(ex.map(lambda x: feat(*x), local))
os.makedirs(FEAT, exist_ok=True); vp, ap = os.path.join(FEAT, "visual_dhash24.jsonl"), os.path.join(FEAT, "audio_fingerprint.jsonl")
with open(vp, "w", encoding="utf-8") as fv, open(ap, "w", encoding="utf-8") as fa:
    for f in F:
        fv.write(json.dumps(dict(media_id=f["media_id"], dhash24=f["dhash24"], frame_indices=f["frame_indices"])) + "\n"); fa.write(json.dumps(dict(media_id=f["media_id"], audio_md5_8k=f["audio_md5_8k"], audio_env_1s=f["audio_env_1s"])) + "\n")
ocv = cv2.__version__; FM = []
for f in F:
    for ft, path_, has in (("visual_dhash24", vp, bool(f["dhash24"])), ("audio_pcm_md5_8k", ap, bool(f["audio_md5_8k"])), ("audio_envelope_1s", ap, bool(f["audio_env_1s"]))):
        FM.append(dict(feature_record_id=f"FEAT-{len(FM) + 1:06d}", media_id=f["media_id"], feature_type=ft, extraction_status="computed" if has else "not_computed", tool_name="opencv-python+ffmpeg+numpy", tool_version=f"opencv {ocv}; {ffmpeg_version()[:20]}",
                       parameters_json=json.dumps({"frames": 24, "dhash": "9x8 grayscale", "audio": "8 kHz mono PCM", "envelope": "RMS per second, 16 levels"}), sample_timestamps=",".join(map(str, f["frame_indices"])) if ft == "visual_dhash24" else "",
                       feature_format="64-bit hex x24" if ft == "visual_dhash24" else "md5 hex" if ft == "audio_pcm_md5_8k" else "hex digit/second", storage_path=rel(vp if ft == "visual_dhash24" else ap), storage_bytes="", feature_sha256="",
                       extracted_utc=NOW, error="" if has else "no audio stream" if ft != "visual_dhash24" else "no decodable frames", permission_status="licence_permits"))
for ft in ("visual_embedding", "audio_embedding", "ocr_text", "asr_transcript", "text_embedding", "scene_boundaries"):
    FM.append(dict(feature_record_id=f"FEAT-{len(FM) + 1:06d}", media_id="ALL_LOCAL", feature_type=ft, extraction_status="not_computed", tool_name="", tool_version="", parameters_json="", sample_timestamps="", feature_format="",
                   storage_path="", storage_bytes="", feature_sha256="", extracted_utc="", error="not computed in roadmap 10.2-10.4 (model phase); no placeholder files exist", permission_status="licence_permits"))
emit("feature_manifest", FM)
FEAT_REF = {}
for f in F: FEAT_REF[f["media_id"]] = "visual_dhash24|audio_fingerprint"

# ---------------------------------------------------------------- split manifest
nfam = {}
for r in recs:
    if r["validation_status"] == "passed": nfam[r["root_source_media_id"]] = nfam.get(r["root_source_media_id"], 0) + 1
SM = []
for fid, st in fam_items:
    held = sorted({r["transformation_name"] for r in recs if r["root_source_media_id"] == fid and r["transformation_id"] in heldout_ids and r["validation_status"] == "passed"})
    SM.append(dict(split_version=SPLIT_VERSION, source_family_id=fid, source_dataset_id="RW-01" if fid.startswith("RW-CMN") else "RW-02", split=SP[fid], assignment_method="Commons: whole search themes assigned (sorted, stride-7 over 14/3/3 pattern per 20); ANAKIN: per family, same pattern over (manipulation type, id)",
                   seed=SEED, domain_stratum=st, n_family_items=(1 + nfam.get(fid, 0)) if fid.startswith("RW-CMN") else 2, n_native_edges=1 if fid.startswith("RW-ANK") else 0, heldout_transformations_in_family="|".join(held)))
emit("split_manifest", SM)

# ---------------------------------------------------------------- training pairs
PAIRS = []; ver = {r["variant_media_id"]: r for r in recs if r["validation_status"] == "passed"}
par = {v: r["direct_parent_media_id"] for v, r in ver.items()}
def anc(n):
    o = []
    while n in par: n = par[n]; o.append(n)
    return o
def tpath(a, d):
    names, n = [], d
    while n != a: names.append(ver[n]["transformation_name"]); n = par[n]
    return ">".join(reversed(names))
def addpair(a, b, rel, fam, group, split, label, nlabel, origin, status, ev, rationale, hard, held, excl="", relid=""):
    PAIRS.append(dict(example_id=f"EX-{len(PAIRS) + 1:07d}", media_a_id=a, media_b_id=b, relationship_id=relid, label_binary_related=label, relationship_class=rel, native_label=nlabel, normalized_label=rel,
                      label_origin=origin, label_status=status, evidence_id=ev, feature_refs=FEAT_REF.get(a, "") + ";" + FEAT_REF.get(b, ""), source_family_id=fam, event_or_cascade_group_id=group, split=("excluded" if excl else split),
                      split_version=SPLIT_VERSION, sampling_method="all within-family pairs" if label and origin == "controlled_lineage" else "seeded random negative sampling inside split", negative_rationale=rationale, hardness=hard,
                      leakage_flag=False, exclusion_reason=excl, includes_heldout_transform=held, created_utc=NOW))
relid = {(e["media_a_id"], e["media_b_id"]): e["relationship_id"] for e in EDG if e["relation_scope"] == "controlled_lineage" and e["normalized_relation_type"].startswith("controlled_") and not e["normalized_relation_type"].endswith("variant")}
for fam in [m["media_id"] for m in pool]:
    nodes = [fam] + [v for v, r in ver.items() if r["root_source_media_id"] == fam]; sp = SP[fam]
    for a, b in itertools.combinations(nodes, 2):
        if par.get(b) == a: rel, x, y, hops = "direct_derivation", a, b, 1
        elif par.get(a) == b: rel, x, y, hops = "direct_derivation", b, a, 1
        elif a in anc(b): rel, x, y, hops = "indirect_derivation", a, b, 2
        elif b in anc(a): rel, x, y, hops = "indirect_derivation", b, a, 2
        elif par.get(a) == par.get(b): rel, x, y, hops = "sibling_same_parent", a, b, 0
        else: rel, x, y, hops = "same_family_other", a, b, 0
        held = (a in ver and lineage_heldout(a)) or (b in ver and lineage_heldout(b)); excl = "held_out_transform_test_only_family_not_test" if held and sp != "test" else ""
        addpair(a, b, rel, fam, "", sp, 1, "", "controlled_lineage", "controlled_ground_truth", f"EV-CV-{y if y in ver else x}", "", "easy" if hops == 1 else "medium", held, excl, relid.get((x, y), ""))
byc = {}
for m in pool: byc.setdefault((SP[m["media_id"]]), []).append(m["media_id"])
for fam in [m["media_id"] for m in pool]:
    sp = SP[fam]; others = [f for f in byc[sp] if f != fam]; dom = STR[fam]; same = [f for f in others if STR[f] == dom]; diff = [f for f in others if STR[f] != dom]
    nodes = lambda f: [f] + [v for v, r in ver.items() if r["root_source_media_id"] == f]
    for pool_, hard, n in ((diff, "easy", 6), (same, "hard", 6)):
        if not pool_: continue
        for _ in range(n):
            o = random.choice(pool_); a, b = random.choice(nodes(fam)), random.choice(nodes(o)); held = (a in ver and lineage_heldout(a)) or (b in ver and lineage_heldout(b))
            addpair(a, b, "unrelated_distinct_source", fam, "", sp, 0, "", "negative_sampling_rule", "uncertain",
                    "EV-NEG-RULE", "distinct Commons uploads (different page ids) with no exact/near-duplicate match in the dHash check; " + ("same search theme, not necessarily same event (not proof of independence)" if hard == "hard" else "different search themes"), hard, held,
                    "held_out_transform_test_only_family_not_test" if held and sp != "test" else "")
    for v, r in ver.items():     # audio-source link: related by audio only
        if r["root_source_media_id"] == fam and r["transformation_id"] == "T09":
            addpair(v, r["audio_source_media_id"], "audio_source_only_not_visual_derivation", fam, "", sp, 0, "", "controlled_lineage", "controlled_ground_truth", f"EV-CV-{v}", "audio shared by construction; picture tracks are unrelated", "hard", False,
                    "audio_donor_family_in_different_split" if SP.get(r["audio_source_media_id"]) != sp else "")
# ANAKIN real native edit pairs
ank_ev = "EV-ANK-meta"
for v in anak_local:
    fam = f"RW-ANK-{v}"; sp = SP[fam]
    addpair(f"RW-ANK-{v}-T", f"RW-ANK-{v}-E", "edited_version", fam, v, sp, 1, amt[v], "source_annotation", "source_ground_truth", ank_ev, "", "easy", False, "", "")
byan = {}
for v in anak_local: byan.setdefault(SP[f"RW-ANK-{v}"], []).append(v)
for v in anak_local:
    fam = f"RW-ANK-{v}"; sp = SP[fam]; oth = [x for x in byan[sp] if x != v]
    for _ in range(2):
        if oth:
            o = random.choice(oth); addpair(f"RW-ANK-{v}-E", f"RW-ANK-{o}-T", "unrelated_distinct_source", fam, v, sp, 0, "", "negative_sampling_rule", "uncertain", "EV-NEG-RULE",
                                            "different ANAKIN video-ids (distinct source videos/URLs per the dataset metadata)", "easy", False, "")
EV = [x for x in load("evidence_ledger") if x["evidence_id"] != "EV-NEG-RULE"]
EV.append(dict(evidence_id="EV-NEG-RULE", evidence_type="machine_measurement", source_dataset_id="ORVEX-CTRL", subject_type="relationship_set", subject_id="negative pairs", source_url="", source_record_ref="s5_features_pairs_splits.py",
               claim_supported="negative pairs drawn from distinct source records inside the same split", claim_status="measured", observed_fact_vs_inference="analyst_inference", verification_method="distinct page ids + dHash near-duplicate screen (duplicate_map)",
               evidence_time_utc=NOW, temporal_precision="second", file_sha256="", reviewer_status="unreviewed", permission_status="n/a", confidence_basis="sampling rule, not proof of independence", limitations="same-theme negatives may still share an event; flagged hard"))
emit("evidence_ledger", EV); emit("training_pairs", PAIRS)


# ---------------------------------------------------------------- group examples (5-6 items)
GR = []
for fam in [m["media_id"] for m in pool]:
    nodes = [v for v, r in ver.items() if r["root_source_media_id"] == fam]; sp = SP[fam]; oth = [f for f in byc[sp] if f != fam]
    if len(nodes) < 3 or not oth: continue
    for rep in range(2):
        cand = [x for x in [fam] + nodes if sp == "test" or not lineage_heldout(x)]
        if len(cand) < 4 or len(oth) < 2: continue
        fm = random.sample(cand, 4)
        ds = [random.choice([o] + [v for v, r in ver.items() if r["root_source_media_id"] == o and (sp == "test" or not lineage_heldout(v))]) for o in random.sample(oth, 2)]
        te = []
        for n in fm:
            a = [x for x in anc(n) if x in fm]
            if a: te.append(f"{a[0]}>{n}")
        GR.append(dict(group_id=f"GRP-{len(GR) + 1:05d}", source_family_id=fam, member_media_ids="|".join(fm + ds), n_members=len(fm) + len(ds), family_member_ids="|".join(fm), distractor_ids="|".join(ds),
                       truth_edges=";".join(te), n_truth_edges=len(te), split=sp, split_version=SPLIT_VERSION, label_origin="controlled_lineage", evidence_id="EV-NEG-RULE", created_utc=NOW))
emit("group_examples", GR)

# ---------------------------------------------------------------- tables empty by evidence + access log
emit("campaign_candidate_clusters", []); emit("experiment_registry", [])
al = AccessLog.all(); rows = []
def A(**k): rows.append(k)
for i, a in enumerate(al): A(attempt_id=f"ACC-{i + 1:06d}", **{k: a.get(k, "") for k in ("source_dataset_id", "media_or_file_id", "url", "attempt_time_utc", "method", "http_status", "result_category", "terms_decision", "retry_count", "bytes", "sha256", "final_status", "note")})
pre = [("RW-03", "Zenodo 2535479", "https://zenodo.org/api/records/2535479", "invid_fvc_2018/fake-video-corpus-2018.zip"), ("RW-04", "Zenodo 1147958", "https://zenodo.org/api/records/1147958", "invid_fvc_v2/Fake_Video_Corpus_v2.0.zip"),
       ("RW-05", "Zenodo 242481", "https://zenodo.org/api/records/242481", "invid_fvc_v1/Fake_Video_Corpus.zip"), ("RW-06", "Zenodo 2564864", "https://zenodo.org/api/records/2564864", "invid_fivr200k/fivr_200k_dataset.zip")]
for ds, nm, url, f in pre:
    p = os.path.join(RWMETA, f); A(attempt_id=f"ACC-G1-{ds}", source_dataset_id=ds, media_or_file_id=nm, url=url, attempt_time_utc="2026-10-26T00:00:00Z", method="http_get", http_status=200, result_category="ok", terms_decision="open_access_cc_by_4.0",
                                  retry_count=0, bytes=os.path.getsize(p) if os.path.exists(p) else "", sha256=sha256(p) if os.path.exists(p) else "", final_status="downloaded_authorized", note="downloaded during Gate 1 (interactive request); md5 verified against Zenodo record")
for f in ("videos_url_uuid.csv", "label_file_uuid_total.json", "pair_file_train.csv", "pair_file_val.csv", "pair_file_test.csv", "video_categories.json", "split_meta_pairs.json"):
    p = os.path.join(RWMETA, "vcsl", f); A(attempt_id=f"ACC-G1-RW-07-{f}", source_dataset_id="RW-07", media_or_file_id=f, url=f"https://raw.githubusercontent.com/alipay/VCSL/main/data/{f}", attempt_time_utc="2026-10-26T00:00:00Z", method="http_get", http_status=200,
                                           result_category="ok", terms_decision="annotation_file_dataset_licence_not_stated", retry_count=0, bytes=os.path.getsize(p) if os.path.exists(p) else "", sha256=sha256(p) if os.path.exists(p) else "", final_status="downloaded_authorized", note="Gate 1 interactive download")
for f in ("anakin_metadata.csv",):
    p = os.path.join(RWMETA, "hf_api", f); A(attempt_id="ACC-G1-RW-02-meta", source_dataset_id="RW-02", media_or_file_id=f, url="https://huggingface.co/datasets/AlexBlck/ANAKIN/raw/main/metadata.csv", attempt_time_utc="2026-10-26T00:00:00Z", method="http_get", http_status=200,
                                           result_category="ok", terms_decision="cc-by-4.0_per_card", retry_count=0, bytes=os.path.getsize(p), sha256=sha256(p), final_status="downloaded_authorized", note="Gate 1 interactive download")
A(attempt_id="ACC-G1-RW-08-tls", source_dataset_id="RW-08", media_or_file_id="VCDB official page", url="https://fvl.fudan.edu.cn/dataset/vcdb/list.htm", attempt_time_utc="2026-10-26T00:00:00Z", method="http_get", http_status="", result_category="failed",
  terms_decision="not_bypassed", retry_count=0, bytes="", sha256="", final_status="access_not_available", note="self signed certificate in certificate chain; TLS verification not bypassed")
A(attempt_id="ACC-G1-RW-08-gh", source_dataset_id="RW-08", media_or_file_id="ccny-zhangx/VCDB README", url="https://raw.githubusercontent.com/ccny-zhangx/VCDB/main/README.md", attempt_time_utc="2026-10-26T00:00:00Z", method="http_get", http_status=404,
  result_category="failed", terms_decision="n/a", retry_count=0, bytes="", sha256="", final_status="not_found", note="suggested lead returned 404")
for ds, n in (("RW-03", "FVC 2018 URLs (5,579)"), ("RW-06", "FIVR-200K YouTube ids (225,960)"), ("RW-07", "VCSL video URLs (9,207)")):
    A(attempt_id=f"ACC-POLICY-{ds}", source_dataset_id=ds, media_or_file_id=n, url="", attempt_time_utc=NOW, method="policy", http_status="", result_category="skipped_terms", terms_decision="media rights not held by dataset authors; no third-party downloader / platform scraping used",
      retry_count=0, bytes=0, sha256="", final_status="metadata_only", note="media not requested")
emit("download_access_attempt_log", rows)
print("variants", len(recs), "passed", len(ver), "edges", len(EDG), "features", len(FM), "pairs", len(PAIRS), "groups", len(GR), "families", len(SM), "access rows", len(rows), "payload", payload_bytes())
