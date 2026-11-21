# -*- coding: utf-8 -*-
"""Generate schema contract, data dictionary, column lineage, catalog, selection/budget doc, requirement matrix, QA report from the REAL tables."""
import os, sys, json, csv, glob
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from common import *
import schema, audit, candidates
from transformations import CATALOGUE, CHAINS
T = audit.T
ORIG = {"a": "copied from a named source field", "b": "normalized/renamed from a named source field", "c": "derived by an explicit deterministic rule from named fields",
        "d": "computed from the actual media/files by a named tool", "e": "annotated/decided by a human analyst with stated evidence", "f": "new ORVEX bookkeeping/administrative column"}
VOC_BY_COL = {"access_status": "access_status", "direction_status": "direction_status", "label_status": "label_status", "split": "split", "validation_status": "validation_status", "media_origin": "media_origin",
              "record_origin": "record_origin", "transformation_status": "transformation_status", "inclusion_status": "inclusion_status"}
def unit(n, typ):
    if n.endswith("_utc"): return "UTC ISO-8601 (precision in time_precision)"
    if typ == "datetime": return "ISO-8601; timezone per time_precision"
    if n.endswith("_s") or n == "duration_s": return "seconds"
    if n.endswith("bytes") or n == "bytes": return "bytes"
    if n == "fps": return "frames/second"
    if n in ("width", "height"): return "pixels"
    return "-"
KW = {"fvc": "RW-03/04/05", "fivr": "RW-06", "vcsl": "RW-07", "anakin": "RW-02", "commons": "RW-01", "covid": "RW-31"}
def srcds(lin):
    h = sorted({v for k, v in KW.items() if k in lin.lower()}); return ";".join(h) if h else "ORVEX (no source-dataset field)"
def md_table(rows, head):
    o = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    for r in rows: o.append("| " + " | ".join(str(x).replace("|", "\\|").replace("\n", " ") for x in r) + " |")
    return "\n".join(o)
def fmt(b): return f"{b:,} B ({b/1e9:.3f} GB / {b/2**30:.3f} GiB)"

# ---------------------------------------------------------------- schema contract + lineage csv + dictionary
contract = {t: dict(path=d["path"], purpose=d["purpose"], phase=d["phase"], columns=[dict(name=c[0], type=c[1], nullable=bool(c[2]), origin=c[3], lineage=c[4], description=c[5]) for c in d["cols"]]) for t, d in schema.TABLES.items()}
json.dump(dict(origin_codes=ORIG, vocabularies=schema.VOC, tables=contract), open(os.path.join(DOCS, "schema_contract.json"), "w", encoding="utf-8"), indent=1)
LN = []; dd = ["# ORVEX Data Dictionary", "", f"Generated {now()} from `scripts/datasets/schema.py` (the machine-readable contract: `docs/datasets/schema_contract.json`). All {len(schema.TABLES)} tables and {sum(len(d['cols']) for d in schema.TABLES.values())} columns are described. Examples and distinct values are read from the real files.", "",
      "Origin codes: " + "; ".join(f"**{k}** = {v}" for k, v in ORIG.items()), "", "Controlled vocabularies:", ""]
for k, v in schema.VOC.items(): dd.append(f"- `{k}`: {', '.join(v)}")
dd.append("")
for t, d in schema.TABLES.items():
    df = T(t); dd += [f"## {t}", f"- File: `{d['path']}` — rows: **{len(df):,}** — phase: {d['phase']}", f"- Purpose: {d['purpose']}", ""]
    rows = []
    for name, typ, nul, org, lin, desc in d["cols"]:
        col = df[name] if name in df else pd.Series(dtype=str); nn = col[col != ""] if len(col) else col
        ex = (str(nn.iloc[0])[:60] if len(nn) else "(none — see missingness)"); allowed = ", ".join(schema.VOC[VOC_BY_COL[name]]) if name in VOC_BY_COL else ""
        if not allowed and typ == "str" and len(nn) and nn.nunique() <= 8: allowed = "observed: " + ", ".join(sorted(map(str, nn.unique()))[:8])
        valid = "contract header + non-null check (K01,K02)" + ("; vocabulary" if name in VOC_BY_COL else "")
        rows.append((name, typ, unit(name, typ), "yes" if nul else "no", org, lin, desc, allowed, ex, valid))
        in_src = "no (ORVEX-added)" if org in ("c", "d", "f", "e") else "yes"
        LN.append(dict(table=t, column=name, source_datasets=srcds(lin), type=typ, nullable="yes" if nul else "no", origin_code=org, origin_meaning=ORIG[org], source_field_or_rule=lin, present_in_source_dataset=in_src, description=desc, allowed_values=allowed, validation=valid,
                       rationale="kept to preserve native field/label" if org in ("a", "b") else "added by ORVEX to support relationship learning/evidence/audit"))
    dd += [md_table(rows, ["column", "type", "unit / timezone", "nullable", "origin", "lineage (source field / rule)", "definition", "allowed values", "example", "validation"]), ""]
open(os.path.join(DOCS, "ORVEX_DATA_DICTIONARY.md"), "w", encoding="utf-8").write("\n".join(dd))
pd.DataFrame(LN).to_csv(os.path.join(DOCS, "column_lineage.csv"), index=False, encoding="utf-8-sig")
for l in LN: l["source_dataset_release"] = "see ORVEX_COLUMN_LINEAGE.md source-mapping table (release per dataset in source_registry)" if l["origin_code"] in "ab" else ""
extra = [l for l in LN if l["present_in_source_dataset"].startswith("no")]
ll = ["# ORVEX Column Lineage", "", f"Machine-readable: `docs/datasets/column_lineage.csv` ({len(LN)} columns). Origin a/b = from a named source field; c = derived by rule; d = computed from media; e = analyst; f = ORVEX bookkeeping.", "",
      "## Columns by origin", md_table([(k, ORIG[k], sum(1 for l in LN if l["origin_code"] == k)) for k in ORIG], ["code", "meaning", "columns"]), "",
      "## Source-native fields mapped into ORVEX (kept verbatim or normalised)", "",
      md_table([("FVC 2018 FVC.csv / FVC_dup.csv", "cascade_id", "event_or_cascade_id / native_record_id", "copied"), ("", "video_url", "source_url, native_media_id (+canonical_url, platform, platform_media_id derived)", "copied + derived"), ("", "label", "native_authenticity_label, native_misleading_label (verbatim)", "copied"),
                ("FVC v2.0 TSV", "InVID_id, Link, Title, Type of Manipulation, Comments, Discussed, Appeared, Timestamp, Channel, Description", "native_record_id, source_url, title, native_manipulation_type, description_caption, publisher_account_id; **Discussed, Appeared, Timestamp, Official channel, Subscriptions kept only in raw file** (not in normalised master)", "partly normalised; loss documented"),
                ("FVC v1.0 TSV", "InVID_id, Link, Title, Comments, Discussed, Appeared", "same as v2.0; Discussed/Appeared kept only in raw file", "partly normalised"),
                ("FIVR-200K", "youtube_ids.txt", "native_media_id/platform_media_id", "copied"), ("", "annotation.json (ND/DS/CS lists)", "media_relationship_edges.native_label (verbatim)", "copied"), ("", "events.json (headline, text, topic, href, youtube)", "event_or_cascade_id (index only); **headline/text/topic/href kept only in raw file**", "loss documented"),
                ("VCSL", "videos_url_uuid.csv", "source_url, native_record_id", "copied"), ("", "label_file_uuid_total.json", "media_relationship_edges a/b_segment_start/end_s", "copied"), ("", "video_categories.json", "title ('VCSL category: …')", "normalised"), ("", "pair_file_*.csv, split_meta_pairs.json", "raw only (benchmark splits not reused: ORVEX splits by source family)", "kept raw"),
                ("ANAKIN metadata.csv", "video-id, start-time, end-time, url, has-masks, task, manipulation-type, editor-id, full-available", "native_record_id, edges a_segment_start/end_s, source_url (full), description_caption, native_manipulation_type, publisher_account_id (editor id); has-masks and full-available kept raw/edges", "copied/normalised"),
                ("Wikimedia Commons API", "pageid, title, imageinfo (url, size, mime, sha1, timestamp, user, comment), extmetadata (LicenseShortName, LicenseUrl, Artist, Credit, AttributionRequired, ImageDescription), categories, globalusage", "native_record_id, title, source_url, published_time_utc, publisher_account_id, license*, attribution, description_caption; **categories, upload comment, commons sha1 kept in commons_candidates.json only**", "partly normalised")],
               ["source", "native field(s)", "ORVEX target", "treatment"]), "",
      "## Extra columns NOT present in any source dataset (ORVEX-added: origin c/d/e/f)", "",
      md_table([(l["table"], l["column"], l["origin_code"], l["source_field_or_rule"]) for l in extra], ["table", "column", "origin", "rule / tool / reason"])]
open(os.path.join(DOCS, "ORVEX_COLUMN_LINEAGE.md"), "w", encoding="utf-8").write("\n".join(ll))

# ---------------------------------------------------------------- sizes
cat = {"real-world raw metadata/annotations": dir_bytes(RWMETA), "real-world media (Commons)": dir_bytes(os.path.join(RWMEDIA, "commons")), "real-world media (ANAKIN subset)": dir_bytes(os.path.join(RWMEDIA, "anakin")),
       "controlled variants (media)": dir_bytes(CVMEDIA), "derived tables": dir_bytes(TAB), "derived features": dir_bytes(FEAT), "derived splits": dir_bytes(SPL), "manifests/logs": dir_bytes(MAN), "reports": dir_bytes(REP), "temp/build (donor wav etc.)": dir_bytes(BUILD)}
tot = payload_bytes()

# ---------------------------------------------------------------- catalogue + selection/budget
reg = T("source_registry"); m = T("real_world_media_master"); v = T("controlled_variant_registry"); e = T("media_relationship_edges"); tp = T("training_pairs")
A = [(r["source_dataset_id"], r["title"], r["release_version"], r["inclusion_status"], r["bytes_or_urls_provided"], r["license_terms"][:70], f"{int(float(r['record_count_local'] or 0)):,}", fmt(int(float(r['actual_local_bytes'] or 0))), r["tasks_supported"][:70], r["verification_level"]) for _, r in reg.iterrows()]
cat_md = ["# ORVEX Dataset Catalogue", "", f"Generated {now()}. **Layer A = real-world data** (`data/real_world/`); **Layer B = ORVEX-created derivatives** (`data/controlled_variants/`, `data/derived/`). Search date 2026-10-26.", "",
          "## A. Real-world datasets considered (all)", "", md_table(A, ["id", "dataset", "release", "decision", "bytes or URLs", "licence / terms", "records held locally", "local size", "supports", "verification"]), "",
          "## B. ORVEX-created datasets", ""]
CB = []
for t, d in schema.TABLES.items():
    df = T(t); org = {c[3] for c in d["cols"]}; added = [c[0] for c in d["cols"] if c[3] in "cdef"]
    srcs = {"controlled_variant_registry": "RW-01 (media files, titles for captions, audio of other records)", "transformation_run_log": "RW-01", "media_relationship_edges": "RW-02, RW-03, RW-06, RW-07 native relations + ORVEX-CTRL lineage from RW-01",
            "real_world_media_master": "RW-01, RW-02, RW-03, RW-04, RW-05, RW-06, RW-07 (metadata normalised; Commons+ANAKIN also media)", "platform_observations": "RW-01 (upload records), RW-03 (cascade order)", "evidence_ledger": "all included sources + ORVEX run logs",
            "feature_manifest": "computed from RW-01/RW-02 media and CD variants", "training_pairs": "RW-01 via variants; RW-02 native edit pairs", "group_examples": "RW-01 via variants", "split_manifest": "RW-01, RW-02", "source_registry": "census of all candidates",
            "duplicate_map": "RW-01, RW-03/04/05, cross-source YouTube ids", "download_access_attempt_log": "all", "campaign_candidate_clusters": "none (blocked: no authorised account+time evidence)", "experiment_registry": "computed from CD features (non-learned baseline only)"}.get(t, "")
    CB.append((t, d["purpose"][:90], srcs, "media files + metadata" if t in ("controlled_variant_registry", "feature_manifest", "training_pairs", "group_examples", "real_world_media_master") else "metadata/tables", f"{len(df):,}", len(d["cols"]), len(added), ", ".join(added[:10]) + ("…" if len(added) > 10 else ""), fmt(os.path.getsize(os.path.join(ROOT, d["path"]))) if os.path.exists(os.path.join(ROOT, d["path"])) else "", d["phase"]))
cat_md += [md_table(CB, ["table", "purpose", "derived from (source dataset ids)", "uses", "records", "columns", "ORVEX-added columns", "added columns (first 10)", "size", "phase"]), "",
           f"Controlled variant media files: **{(v['validation_status']=='passed').sum():,}** passed / {(v['validation_status']=='failed').sum():,} failed — {fmt(cat['controlled variants (media)'])}. All columns of each created table are in `ORVEX_DATA_DICTIONARY.md`; origin of every column in `column_lineage.csv`.", "",
           "## C. Required for the ORVEX problem statement", "",
           md_table([("RW-01 Wikimedia Commons CC/PD pool", "REQUIRED (core)", "only open, per-file licensed source with media bytes eligible for controlled variants"), ("RW-02 ANAKIN subset", "REQUIRED for real edit-pair evaluation", "real human edits with parent/child + manipulation type"),
                     ("RW-03 FVC 2018 (+RW-04 v2.0)", "REQUIRED (metadata)", "real repost cascades with fake/real labels"), ("RW-06 FIVR-200K", "REQUIRED (metadata)", "same-incident vs copy labels for hard negatives"), ("RW-07 VCSL", "REQUIRED (metadata)", "real segment-level partial-copy annotations"),
                     ("RW-05 FVC v1.0", "NOT NEEDED", "superseded; kept only for duplicate mapping"), ("RW-08..RW-30", "OPTIONAL / excluded", "see selection document")], ["real-world dataset", "level", "why"]), "",
           md_table([("controlled_variant_registry + media", "REQUIRED Phase 1"), ("media_relationship_edges", "REQUIRED both"), ("real_world_media_master", "REQUIRED both"), ("training_pairs, group_examples, split_manifest", "REQUIRED Phase 1"), ("feature_manifest (+features)", "REQUIRED both"),
                     ("evidence_ledger, transformation_run_log, download_access_attempt_log, duplicate_map, source_registry", "REQUIRED both (traceability)"), ("platform_observations", "REQUIRED Phase 2 (partial data)"), ("campaign_candidate_clusters", "BLOCKED — not_supported_by_available_evidence"), ("experiment_registry", "holds only the non-learned dHash sanity baseline BASE-DHASH-v1 (no ORVEX model trained)")], ["created dataset", "level"])]
open(os.path.join(DOCS, "ORVEX_DATASET_CATALOG.md"), "w", encoding="utf-8").write("\n".join(cat_md))

sel = ["# ORVEX Dataset Selection and Storage Budget", "", f"Generated {now()}. Size definition: **decimal bytes under `<repo>\\data\\`** (media, variants, features, tables, manifests, logs, build/temp). Installed tools (FFmpeg, ~0.4 GB) are outside `data/` and reported separately.", "",
       "## Budget plan (set before large downloads)", md_table([("real-world raw metadata", "0.4 GB"), ("Commons real media", "3.0 GB"), ("ANAKIN subset (trimmed+edited+masks)", "3.0 GB (planned 2.52 GB from API sizes)"), ("controlled variants", "14.0 GB"), ("features + tables + logs", "1.0 GB"), ("total allocation", "21.4 GB; hard cap 30 GB, target <=27 GB, stop 29 GB")], ["category", "allocation"]), "",
       "Selection rules: ANAKIN — deterministic sort by sha256('orvex-anakin-v1'+id), first 50 per manipulation type, only while cumulative planned bytes <= 3 GB (full-length videos, 44.6 GB, excluded). Commons — 28 themed queries, <=4 new files per query, files 0.3-45 MB, licence gate, stem de-duplication.", "",
       "## Measured sizes", md_table([(k, fmt(b)) for k, b in cat.items()] + [("**TOTAL dataset payload**", fmt(tot)), ("cap / target", "30 GB / 27 GB"), ("cap respected", "YES" if tot < CAP_HARD and tot <= CAP_TARGET else "NO")], ["category", "measured"]), "",
       "## Source-by-source decision", md_table([(r["source_dataset_id"], r["title"], r["inclusion_status"], r["inclusion_reason"], r["limitations"]) for _, r in reg.iterrows()], ["id", "dataset", "decision", "reason", "limitations"])]
sel += ["", "## Portfolio coverage of the required capability areas", md_table([
    ("(a) video-copy / partial-segment matching", "RW-07 VCSL (metadata), controlled trims T03-T05 (RW-01)", "annotations + controlled ground truth; native media not local"),
    ("(b) near-duplicate discovery vs same-event", "RW-06 FIVR-200K (ND/DS/CS), controlled variants", "metadata only for FIVR; same-incident labels never used as copy labels"),
    ("(c) naturally occurring manipulated/misleading video + evidence", "RW-03/04 FVC, RW-31 COVID removed videos, RW-02 ANAKIN (human edits)", "FVC/COVID metadata only; ANAKIN has media (commissioned edits)"),
    ("(d) repost / cascade / timeline evidence", "RW-03 FVC cascades (order), RW-31 (publish, removal, 257k tweet share times, 81k Facebook post ids)", "no sharer accounts"),
    ("(e) authorised real media for controlled variants", "RW-01 Commons (55 usable sources)", "per-file CC/PD licences"),
    ("(f) campaign-related metadata", "RW-31 (video-level spread), RW-01 uploads", "INSUFFICIENT for coordination claims (no multi-account time evidence); Twitter IO / TikTok API inaccessible")], ["area", "datasets", "coverage / caveat"]),
    "", "## Cap by dataset and by variant type", "Per-dataset allocations are in the budget table above. Variants have one total cap (14 GB, enforced by the generator guard before every encode) and no per-type cap; measured per-type sizes are in `ORVEX_DATASET_QA_REPORT.md` and `data/manifests/storage_budget.csv`.", "", "Machine-readable plan: `data/manifests/selection_plan.json`; storage log: `data/manifests/storage_budget.csv`; checksums: `data/manifests/checksums.sha256`; ID crosswalk: `data/manifests/native_id_crosswalk.csv`; attribution: `ORVEX_ATTRIBUTION.md`; protocol: `ORVEX_EVALUATION_PROTOCOL.md`."]
open(os.path.join(DOCS, "ORVEX_DATASET_SELECTION_AND_BUDGET.md"), "w", encoding="utf-8").write("\n".join(sel))

# ---------------------------------------------------------------- requirement coverage matrix
REQS = [  # id, pdf ref, requirement, modules, phase, artifacts, checks, ceiling, limitation
 ("R01", "p2 §2; p4 §5 Phase 1", "Create a controlled dataset from real source videos, generate manipulated versions and record their relationships", "M1,M3", "1", "controlled_variant_registry, media_relationship_edges", ["K04", "K10", "K11"], "PASS", ""),
 ("R02", "p4 §5", "Every video has a unique ID; each manipulated version has parent ID, transformation label and relationship record", "M1,M5", "1", "media_id, variant_media_id, direct_parent_media_id, transformation_name, relationship_id", ["K03", "K04", "K11"], "PASS", ""),
 ("R03", "p4 §5", "Variants: trimmed, misleading captions, replaced audio, recompressed, new edit derived from a variant", "M1,M4", "1", "controlled_variant_registry (T01-T14, chains C1-C5)", ["K10"], "PASS", "captions are mismatched real titles (constructed), not invented claims; audio is another real recording"),
 ("R04", "p5 M1", "Import source videos; identify duplicates; assign unique IDs to originals", "M1", "1", "real_world_media_master, duplicate_map", ["K03", "K19", "K08"], "PASS", ""),
 ("R05", "p5 M1", "Record transformation types and parent IDs; save known relationships", "M1,M5", "1", "media_relationship_edges", ["K11", "K12"], "PASS", ""),
 ("R06", "p5 M2", "Extract frames, audio, text/captions/OCR; generate visual, audio, text representations; store fingerprints", "M2", "1,2", "feature_manifest + features/*.jsonl", ["K17"], "PARTIAL", "dHash + audio fingerprints computed; OCR, ASR, text/visual/audio embeddings NOT computed (model phase)"),
 ("R07", "p5-6 M3; p4 §5", "Compare two videos and groups of 5-6; direct/indirect derivation; separate likely from uncertain; confidence and supporting evidence", "M3", "1", "training_pairs, group_examples, evidence_ledger", ["K15", "K25"], "PARTIAL", "ground-truth pairs/groups exist; no relationship model, so no predicted confidences"),
 ("R08", "p6 M4", "Manipulation analysis: trimming/cropping, caption/text changes, audio replacement", "M4", "1", "controlled variants + ANAKIN native manipulation types", ["K10", "K12"], "PASS", "data support only; detectors not built here"),
 ("R09", "p6 M5", "Graph: media nodes, relationship edges, parent-child, manipulation type per edge", "M5", "1,2", "media_relationship_edges (parent_media_id, child_media_id, transformation_type)", ["K11", "K12"], "PASS", "graph storage/UI not part of 10.2-10.4"),
 ("R10", "p6 M6; p10 §8.6", "Platform data: post IDs, URLs, timestamps, account ids, normalised format; tracking of access", "M6", "2", "platform_observations, download_access_attempt_log, real_world_media_master", ["K07", "K22"], "PARTIAL", "no live platform connector; timestamps/accounts only for Commons uploads; FVC has order but no time"),
 ("R11", "p6 M7; p11 §9.5", "Campaign detection: candidate clusters from posting times/accounts/cross-posting, separate from media similarity", "M7", "2", "campaign_candidate_clusters", ["K20"], "BLOCKED", "no authorised multi-account time-stamped distribution data locally (Twitter IO / TikTok API need approval); table is empty by design; nothing simulated"),
 ("R12", "p7 M9; p8 step 7", "Evaluation: precision/recall, false positives, unseen manipulation methods", "M9", "1", "split_manifest, training_pairs, experiment_registry", ["K13", "K14"], "PARTIAL", "evaluation data/protocol ready; only a non-learned dHash sanity baseline (BASE-DHASH-v1) has been run; no ORVEX model trained"),
 ("R13", "p8 §7 step 1-2; p12 10.2", "Collect real source videos from authorised datasets; check duplicates", "M1", "1", "source_registry, real_world_media_master", ["K08", "K19", "K24"], "PASS", ""),
 ("R14", "p12 10.3", "Split train/test by original source video", "M9", "1", "split_manifest", ["K13"], "PASS", ""),
 ("R15", "p8 step 7; p11 §9.6", "Test on unseen source videos and unseen transformation types", "M9", "1", "split_manifest.heldout_transformations_in_family; T11-T14 test-only", ["K14", "K13"], "PARTIAL", "unseen types are other FFmpeg edits; AI-generated/unseen real-world manipulations only via ANAKIN eval subset"),
 ("R16", "p3 §4.5; p10 §8.6", "Do not assume platforms allow search/download; respect access rules", "M6", "2", "source_registry, access log, policy", ["K07", "K22", "K24"], "PASS", ""),
 ("R17", "p3 §4.4; p11 §9.2", "Relationship labels with parent IDs, not only real/fake labels", "M1,M3", "1", "media_relationship_edges, controlled_variant_registry", ["K11", "K12", "K27"], "PASS", ""),
 ("R18", "p3 §4.6", "Analyse media relationships and account coordination separately", "M3,M7", "2", "policy §5; campaign table separate", ["K20", "K21"], "PASS", ""),
 ("R19", "p3 §4.7", "Robustness to unfamiliar manipulation methods", "M9", "1", "T11-T14 held out", ["K14"], "PARTIAL", "limited to four FFmpeg transformations"),
 ("R20", "p11 §9.4", "Cross-modal evidence (visual + audio + text)", "M2,M4", "1,2", "variants (audio/caption), feature_manifest", ["K17", "K10"], "PARTIAL", "text evidence = ground-truth caption; no OCR/ASR extraction yet"),
 ("R21", "p12 10.2", "Permitted sources, licence/access/metadata check, starter set preserved, dataset register", "-", "1", "source_registry, source licence columns, originals read-only hashes", ["K08", "K18", "K24", "K06"], "PASS", ""),
 ("R22", "p12 10.3", "Remove exact duplicates, flag unusable, choose transformations, generate variants with ID/parent/transformation, related and unrelated examples", "M1", "1", "duplicate_map, qc_flags, registry, training_pairs", ["K19", "K10", "K15"], "PASS", ""),
 ("R23", "p12 10.4", "Define data-use and evidence rules; likely/uncertain/unverified; keep similarity separate from coordination", "-", "1,2", "ORVEX_DATA_USE_AND_EVIDENCE_POLICY.md", ["K21"], "PASS", "numeric confidence deliberately undefined until calibration"),
 ("R24", "p4 §5 note; p5 M3", "Similarity is not proof of derivation; uncertain relationships marked for review", "M3", "1,2", "label_status vocabulary, uncertain negatives, policy §5/§8", ["K15", "K21"], "PASS", ""),
 ("R25", "p3 §3", "Do not automatically declare a person guilty/account malicious", "-", "2", "policy §5/§10; pseudonymised accounts", ["K21", "K20"], "PASS", ""),
 ("R26", "p2 §2 step 7", "Show where content was found and when it was observed, when available", "M6,M8", "2", "platform_observations, media master times", ["K22"], "PARTIAL", "real upload times only for Commons"),
 ("R27", "p2 §2 Phase 2", "Search supported platforms/datasets for related candidate videos", "M6", "2", "FIVR/VCSL/FVC metadata pools (metadata_only)", ["K07", "K12"], "PARTIAL", "candidate pools are metadata-only; media not local"),
 ("R28", "prompt §2.2", "Dataset payload under 30 GB (target <=27 GB)", "-", "-", "data/", ["K16"], "PASS", ""),
 ("R29", "prompt §2.1", "Real-world sources only; created data only from real media; separated; no generative AI", "-", "-", "all", ["K05", "K09", "K04"], "PASS", ""),
 ("R30", "prompt §4 gate 3", "Preserve native fields/annotations; document every mapping and loss", "-", "-", "raw_metadata, ORVEX_COLUMN_LINEAGE.md", ["K18", "K01"], "PASS", "loss list in column lineage document"),
 ("R31", "prompt §4 gate 7", "Every column has dictionary + lineage; schema validated programmatically", "-", "-", "schema_contract.json, data dictionary, column_lineage.csv", ["K01", "K02"], "PASS", ""),
 ("R32", "prompt §4 gate 4", "Failed variants excluded from training; outputs validated beyond exit code", "M4", "1", "validation_checks_json, usable_for_training", ["K26", "K10"], "PASS", ""),
 ("R33", "prompt §2.4", "Authenticity, misleading, relation labels stored separately; native kept verbatim", "M3", "1,2", "media master vs edges columns", ["K27"], "PASS", ""),
 ("R34", "prompt §4 gate 2", "metadata_only items never claimed as downloaded", "-", "-", "access_status", ["K07"], "PASS", ""),
 ("R35", "p9 §8.4 RAG", "RAG retrieves investigation records, media metadata, transformation logs and supporting evidence for reports", "M8", "2", "evidence_ledger, transformation_run_log, real_world_media_master, platform_observations", ["K03", "K22", "K31"], "PARTIAL", "all retrievable records exist as tables; no retrieval index or report generator built here"),
 ("R36", "p7 M9", "Measure time-to-detection; record model versions and experiment results", "M9", "1,2", "experiment_registry", ["K20"], "BLOCKED", "needs an end-to-end system; only per-pair scoring latency of the non-learned baseline is recorded (not time-to-detection)"),
 ("R37", "prompt §2.4", "Label dimensions authenticity/misleading/relationship/direction/transformation/coordination/evidence kept separate", "M3", "1,2", "master + edges + observations columns", ["K27", "K31"], "PASS", ""),
 ("R38", "prompt §2.2/§5", "Manifests: checksums, storage budget, selection plan, ID crosswalk, attribution, evaluation protocol", "-", "-", "data/manifests/*", ["K29", "K30"], "PASS", "checksums are SHA-256 of every file under data/ except build temp and the checksum file"),
 ("R39", "prompt §4 gate 2", "Raw data kept read-only; no zero-byte/truncated files", "-", "-", "Layer A", ["K28", "K33"], "PASS", ""),
 ("R40", "p6 M6; p7 Phase 2", "Real source/post timeline: publish, removal and share-reference times", "M6", "2", "platform_observations (RW-31, RW-01)", ["K32", "K22"], "PARTIAL", "share-reference tweet times derived from tweet-id snowflake; sharer accounts not provided; Facebook posts have id only"),
]
AR = {k.split("_")[0]: v for k, v in audit.R.items()}
mat = []
for rid, ref, txt, mods, ph, art, cks, ceil, lim in REQS:
    oks = [AR[c][0] for c in cks]; ev = "; ".join(f"{c}: {AR[c][1]}" for c in cks)
    status = "FAIL" if not all(oks) and ceil != "BLOCKED" else ceil
    if ceil == "BLOCKED": status = "BLOCKED" if AR[cks[0]][0] else "FAIL"
    mat.append(dict(requirement_id=rid, pdf_reference=ref, requirement=txt, modules=mods, phase=ph, artifacts=art, checks="|".join(cks), status=status, evidence=ev, limitation_or_blocker=lim))
pd.DataFrame(mat).to_csv(os.path.join(DOCS, "ORVEX_REQUIREMENT_COVERAGE_MATRIX.csv"), index=False, encoding="utf-8-sig")
json.dump(audit.summary(), open(os.path.join(REP, "acceptance_checks.json"), "w", encoding="utf-8"), indent=1)

# ---------------------------------------------------------------- QA report
qa = ["# ORVEX Dataset QA Report", "", f"Generated {now()} by running real checks on the real files (`data/reports/acceptance_checks.json`).", "", "## Acceptance checks run", md_table([(k, "PASS" if ok else "FAIL", ev) for k, (ok, ev) in audit.R.items()], ["check", "result", "measured evidence"]), "",
      "## Records", md_table([(t, f"{len(T(t)):,}") for t in schema.TABLES], ["table", "rows"]), "",
      "## Real-world media master by source", md_table([(k, f"{n:,}") for k, n in m["source_dataset_id"].value_counts().items()], ["source", "records"]), "",
      md_table([(k, f"{n:,}") for k, n in m["access_status"].value_counts().items()], ["access status", "records"]), "",
      "## QC flags on downloaded Commons media", md_table([(k, n) for k, n in pd.Series([f for s in m[m['source_dataset_id'] == 'RW-01']['qc_flags'] for f in s.split('|') if f]).value_counts().items()], ["flag", "files"]), "",
      f"Usable as variant sources: {int((m['usable_for_variants']=='True').sum())} of {int((m['source_dataset_id']=='RW-01').sum())} downloaded Commons files.", "",
      "## Controlled variants", md_table([(k, n) for k, n in v[v['validation_status'] == 'passed']['transformation_name'].value_counts().items()], ["transformation (passed)", "count"]), "",
      f"Failed variants: {int((v['validation_status']=='failed').sum())}. Transformations not generated because the parent had no audio (T10/T14): see run log counts below.", "",
      "## Splits and pairs", md_table([(k, n) for k, n in T('split_manifest')['split'].value_counts().items()], ["split (families)", "count"]), "", md_table([(k, n) for k, n in tp['relationship_class'].value_counts().items()], ["pair class", "count"]), "",
      md_table([(k, n) for k, n in tp['split'].value_counts().items()], ["pair split", "count"]), "",
      "## Native relationship edges", md_table([(f"{a} / {b}", n) for (a, b), n in e[e['relation_scope'] == 'real_native'].groupby(['source_dataset_id', 'normalized_relation_type']).size().items()], ["source / normalised type", "edges"]), "",
      "## Duplicates", md_table([(k, n) for k, n in T('duplicate_map')['duplicate_type'].value_counts().items()], ["type", "records"]), "",
      "## Missingness (columns with >50% blanks in the media master)", md_table([(c, f"{(m[c]=='').mean()*100:.0f}%") for c in m.columns if (m[c] == '').mean() > 0.5], ["column", "blank"]), "",
      "## Known limitations", "- Only Commons media (RW-01) are source material for controlled variants; ANAKIN is evaluation-only.", "- FVC/FIVR/VCSL media bytes are not available to ORVEX (metadata only).", "- OCR/ASR/embeddings are not computed.", "- Campaign clusters cannot be created honestly from available data.",
      "- Hard negatives share a search theme, not a verified event; labelled `uncertain`.", "- VCDB, WildDeepfake, Deepfake-Eval-2024, VSC, CC_WEB_VIDEO, SVD, NIST, Pushshift are unverified leads."]
# --- cross-check additions
dm = T("duplicate_map"); mi = m.set_index("media_id")
cf = []
for _, d in dm[dm["duplicate_type"] == "same_url_across_versions"].iterrows():
    a, b = mi.loc[d["canonical_media_id"]], mi.loc[d["duplicate_media_id"]]
    if a["native_authenticity_label"] != b["native_authenticity_label"]: cf.append((d["canonical_media_id"], a["native_authenticity_label"], d["duplicate_media_id"], b["native_authenticity_label"], d["evidence"][:60]))
nat = e[e["relation_scope"] == "real_native"]
roots = set(v[v["validation_status"] == "passed"]["root_source_media_id"]); mute = set(v[(v["validation_status"] == "passed") & (v["transformation_name"] == "audio_mute")]["root_source_media_id"]); mix = set(v[(v["validation_status"] == "passed") & (v["transformation_name"] == "audio_noise_mix")]["root_source_media_id"])
vb = v[v["validation_status"] == "passed"].copy(); vb["bytes"] = vb["bytes"].astype(int)
qa += ["", "## Cross-check additions", "### Native label distributions (kept verbatim)", md_table([(a, b, n) for (a, b), n in m[m["native_authenticity_label"] != ""].groupby(["source_dataset_id", "native_authenticity_label"]).size().items()] +
        [(a, b, n) for (a, b), n in m[m["native_manipulation_type"] != ""].groupby(["source_dataset_id", "native_manipulation_type"]).size().items()], ["source", "native label / manipulation type", "records"]), "",
       md_table([(a, b, n) for (a, b), n in nat.groupby(["source_dataset_id", "native_label"]).size().items()], ["source", "native relation label", "edges"]), "",
       "### Conflicting source labels across versions (same canonical URL)", f"{len(cf)} conflicts found among {int((dm['duplicate_type'] == 'same_url_across_versions').sum())} cross-version URL matches." + ("" if not cf else "\n\n" + md_table(cf[:20], ["canonical", "label", "duplicate", "label", "URL"])), "",
       "### Transformations not generated (and why)", f"- audio_mute (T10): {len(roots - mute)} of {len(roots)} sources skipped (2 more failed validation) — parent has no audio track or failed validation.", f"- audio_noise_mix (T14): {len(roots - mix)} of {len(roots)} sources skipped — parent has no audio track.",
       "- Voice cloning, face swap, TTS, text-to-video: **intentionally not generated** (no generative AI rule). Audio replacement uses only real recordings.", "", "### Variant storage by transformation type (measured)",
       md_table([(k, int(r["n"]), fmt(int(r["b"]))) for k, r in vb.groupby("transformation_name").agg(n=("bytes", "size"), b=("bytes", "sum")).iterrows()], ["transformation", "files", "size"]), "",
       "### Per-source-dataset field completeness", md_table([(k, len(g), f"{(g['source_url']=='').mean()*100:.0f}%", f"{(g['platform_media_id']=='').mean()*100:.0f}%", f"{(g['published_time_utc']=='').mean()*100:.0f}%", f"{(g['local_path']!='').sum()}") for k, g in m.groupby("source_dataset_id")], ["source", "records", "blank source_url", "blank platform id", "blank publish time", "local files"]), "",
       "### Not assessed", "- Liveness of source URLs (broken/deleted videos) was **not** checked: requesting platform URLs for 240k records would breach the no-hammering/no-scraping rule; those records stay `metadata_only`.", "- Truncated-file detection is limited to ffprobe/ffmpeg decode errors and zero duration."]
open(os.path.join(DOCS, "ORVEX_DATASET_QA_REPORT.md"), "w", encoding="utf-8").write("\n".join(qa))
print("docs written; checks failing:", [k for k, (ok, _) in audit.R.items() if not ok]); print("matrix:", pd.Series([x["status"] for x in mat]).value_counts().to_dict())
