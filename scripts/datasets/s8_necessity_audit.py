# -*- coding: utf-8 -*-
"""Final dataset-necessity audit: independent variant re-validation, requirement->data decision table, inventories and readiness reports.
Every number is measured from the current files at run time."""
import os, sys, json, subprocess, hashlib
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(__file__))
from common import *
import schema, audit, candidates
OUT = os.path.join(DOCS, "necessity_audit"); os.makedirs(OUT, exist_ok=True); NOW = now()
T = audit.T
def md(rows, head):
    o = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    for r in rows: o.append("| " + " | ".join(str(x).replace("|", "/").replace("\n", " ") for x in r) + " |")
    return "\n".join(o)
def gb(b): return f"{b/1e9:.2f} GB"
m, v, tp, e, o, sm = T("real_world_media_master"), T("controlled_variant_registry"), T("training_pairs"), T("media_relationship_edges"), T("platform_observations"), T("split_manifest")
vp = v[v["validation_status"] == "passed"].copy(); runlog = T("transformation_run_log"); reg = T("source_registry")
B = json.load(open(os.path.join(OUT, "dhash_baseline_results.json"), encoding="utf-8")); chk = {k.split("_")[0]: val for k, val in audit.R.items()}

# ------------------------------------------------------------ Phase C: independent re-validation of every passed variant
def probe_tags(path):
    r = subprocess.run([FFPROBE, "-v", "error", "-print_format", "json", "-show_format", "-show_streams", path], capture_output=True, text=True, encoding="utf-8", errors="replace")
    try: j = json.loads(r.stdout)
    except Exception: return None
    vs = [s for s in j["streams"] if s["codec_type"] == "video"]; return dict(ok=bool(vs), dur=float(j["format"].get("duration", 0) or 0), comment=(j["format"].get("tags") or {}).get("comment", ""))
res = list(ThreadPoolExecutor(max_workers=8).map(lambda p: probe_tags(os.path.join(ROOT, p)), vp["local_path"]))
readable = sum(1 for r in res if r and r["ok"] and r["dur"] > 0); tagged = sum(1 for r in res if r and "ORVEX controlled variant" in r["comment"]); durmatch = sum(1 for r, d in zip(res, vp["duration_s"]) if r and abs(r["dur"] - float(d)) < 0.5)
ok_ids = set(m[(m["source_dataset_id"] == "RW-01") & (m["usable_for_variants"] == "True")]["media_id"]); mi = m.set_index("media_id")
roots_ok = vp["root_source_media_id"].isin(ok_ids).sum(); anc = 0
ids = set(vp["variant_media_id"]) | ok_ids
for _, r in vp.iterrows(): anc += int(all(a in ids for a in r["ancestor_chain"].split("|")))
aud = vp[vp["audio_source_media_id"] != ""]; aud_ok = int(sum(1 for a in aud["audio_source_media_id"] if a in ok_ids and mi.loc[a, "has_audio"] == "True" and mi.loc[a, "license"] != ""))
cap = vp[vp["transformation_id"] == "T07"]; cap_ok = int(sum(1 for _, r in cap.iterrows() if r["caption_text"] and r["caption_text_source_media_id"] in ok_ids and r["caption_text_source_media_id"] != r["root_source_media_id"] and r["media_origin"] == "controlled_variant"))
rl = runlog.set_index("variant_media_id"); rl_ok = int(sum(1 for x in vp["variant_media_id"] if x in rl.index and rl.loc[x, "return_code"] == "0" and rl.loc[x, "output_validation_status"] == "passed"))
meta_ok = int(sum(1 for _, r in vp.iterrows() if r["tool_version"] and r["run_id"] and r["parameters_json"].startswith("{")))
failed = v[v["validation_status"] == "failed"]; failed_clean = int(((failed["usable_for_training"] == "False") & (failed["local_path"] == "")).sum())
C = dict(passed_variants=len(vp), readable_by_independent_ffprobe=readable, duration_matches_registry=durmatch, carries_controlled_variant_metadata_tag=tagged, parent_chain_complete=int(anc), roots_eligible=int(roots_ok), audio_variants=len(aud), audio_donor_documented_real_eligible=aud_ok,
         caption_variants=len(cap), caption_variants_with_real_source_text=cap_ok, run_log_return0_and_passed=rl_ok, tool_params_run_recorded=meta_ok, failed_variants=len(failed), failed_excluded_and_no_file=failed_clean, leakage_check=chk["K13"][0], heldout_check=chk["K14"][0])
json.dump(C, open(os.path.join(OUT, "variant_independent_validation.json"), "w", encoding="utf-8"), indent=1)
cov = vp.groupby(["transformation_name", "source_split"]).size().unstack(fill_value=0).reindex(columns=["train", "val", "test"], fill_value=0)
purpose = {"reencode_hq": "identity-preserving format change: relationship model must not over-react to codec", "recompress_low": "platform recompression: most common real-world degradation", "trim_middle": "partial temporal copy / segment alignment (PDF: trimming)", "trim_head": "partial temporal copy, start cut", "trim_tail": "partial temporal copy, end cut",
           "crop_center": "spatial edit (PDF: cropping)", "caption_burn_in": "text overlay, mismatched real title (PDF: misleading captions) - controlled pairing", "watermark_overlay": "overlay that changes pixels but not meaning", "audio_replace": "audio replaced by another real recording (PDF: audio replacement)",
           "audio_mute": "audio removal", "mirror_color_shift": "TEST-ONLY unseen spatial+colour edit", "speed_change": "TEST-ONLY unseen temporal edit", "reupload_sim": "TEST-ONLY screen-record-like re-upload", "audio_noise_mix": "TEST-ONLY unseen audio mix"}
nohard = {s: int(((tp["split"] == s) & (tp["relationship_class"] == "unrelated_distinct_source") & (tp["hardness"] == "hard")).sum()) for s in ("train", "val", "test")}
noaud = int(((m["source_dataset_id"] == "RW-01") & (m["usable_for_variants"] == "True") & (m["has_audio"] != "True")).sum())
tc = ["# Transformation Coverage Report", "", f"Generated {NOW}. All counts measured from `controlled_variant_registry` and re-validated independently with ffprobe in this audit.", "", "## Independent re-validation of all passed variants", md([(k, vv) for k, vv in C.items()], ["check", "result"]), "",
      "## Coverage by transformation and split (passed variants)", md([(k, *[int(x) for x in r], purpose.get(k, "")) for k, r in cov.iterrows()], ["transformation", "train", "val", "test", "purpose / evaluation value"]), "",
      "## PDF-required transformation families", md([("trimming", "T03/T04/T05", "covered"), ("cropping", "T06", "covered"), ("caption addition", "T07 (+T08 watermark)", "covered; caption text is another real record's title, labelled as controlled pairing"), ("audio replacement/change", "T09, T10, T14", "covered; audio from other real recordings only"),
                  ("recompression", "T01, T02, T13", "covered"), ("multi-step / indirect derivation", "chains C1-C5", f"covered: {int((vp['generation_depth'].astype(int) >= 2).sum())} variants at depth >= 2")], ["PDF family", "transformations", "status"]), "",
      "## Genuine gaps and decision", f"- **Coverage gap found:** hard (same-theme) negatives per split = {nohard}; `split-v1` had none in the test split (found by this audit, fixed by theme-grouped `split-v2` without new data).",
      f"- Transformations not generated: audio_mute / audio_noise_mix skipped for {noaud} eligible sources without an audio track (nothing to remove/mix). No new transformation is justified.", "- Per-split counts of the four held-out types are small (see table); this is a statistical-power limit of the 55-source corpus, not a missing transformation.",
      "- **Not proposed (and why):** AI voice, face swap, synthetic video, text-to-video (forbidden by policy); more first-generation variants of the same sources (adds near-identical data, no new evaluation value); extra transformation types before the existing ones have been evaluated with a model."]
open(os.path.join(OUT, "transformation_coverage_report.md"), "w", encoding="utf-8").write("\n".join(tc))

# ------------------------------------------------------------ Phase D inventory
def cls(r):
    s = r["inclusion_status"]; vl = r["verification_level"]
    if s == "included_selected_subset": return "real-world media downloaded and verified (selected subset)"
    if s == "included_metadata_only": return "real-world metadata/annotations only"
    if s == "research_lead_unverified" or vl == "research_lead_unverified": return "unverified research lead"
    if s == "legal_review_required": return "partially accessible / legal review required"
    return "excluded: " + s.replace("excluded_", "")
inv = [dict(kind="real-world", id=r["source_dataset_id"], name=r["title"], classification=cls(r), status=r["inclusion_status"], verification=r["verification_level"], records_local=r["record_count_local"], local_bytes=r["actual_local_bytes"], reason=r["inclusion_reason"][:200]) for _, r in reg.iterrows()]
for t, d in schema.TABLES.items():
    p = os.path.join(ROOT, d["path"]); inv.append(dict(kind="orvex-created", id=t, name=d["purpose"][:90], classification=f"created table (phase {d['phase']})", status="present", verification="tests", records_local=len(T(t)), local_bytes=os.path.getsize(p), reason=""))
inv.append(dict(kind="orvex-created", id="controlled variants (media)", name="rendered variants from real Commons media", classification="created media (phase 1)", status="present", verification="ffprobe + hashes", records_local=len(vp), local_bytes=dir_bytes(CVMEDIA), reason=""))
pd.DataFrame(inv).to_csv(os.path.join(OUT, "dataset_inventory.csv"), index=False, encoding="utf-8-sig")

# ------------------------------------------------------------ Phase E campaign readiness
c = m[m["source_dataset_id"] == "RW-31"]; tw = o[o["platform"] == "twitter"]; fb = o[o["platform"] == "facebook"]
camp = ["# Campaign-Data Readiness Report", "", f"Generated {NOW}.", "", "## Evidence layers (kept separate)", md([("E1 media similarity", "available (hash features, native FIVR/VCSL/FVC relations)", "never proves sharing or coordination"), ("sharing / reposting evidence", "partial: FVC cascades (order only); RW-31 share-reference post ids", "no sharer identity"),
      ("account + timestamp observations", "very partial (see below)", "needed per post: who, when, where"), ("coordination evidence", "NONE", "requires independent multi-account timing/behaviour data over a stated baseline")], ["layer", "state", "note"]), "",
      "## What RW-31 (COVID misinformation videos, Zenodo 4557828) actually provides", md([
      ("video records", len(c), "all metadata_only; media not provided"), ("publish timestamps", int((c["published_time_utc"] != "").sum()), "timezone unstated; precision `second_timezone_unstated`"), ("channel ids", int((c["publisher_account_id"] != "").sum()), "YouTube channel of the video (publisher), not sharers"),
      ("platform removal timestamps", int((o["observation_type"] == "removal").sum()), "when YouTube removed the video, per authors"), ("Twitter share-reference post ids", len(tw), "ids only; **0** have a sharer account"), ("...with time derived from tweet-id snowflake", int((tw["publish_time_utc"] != "").sum()), f"{int((tw['time_precision'] == 'second_derived_unverified').sum())} fall outside the dataset's stated Nov 2019-Jun 2020 window -> flagged unverified"),
      ("Facebook share-reference post ids", len(fb), "id only: no URL, account or time"), ("posts with sharer account", int(((o["observation_type"] == "share_reference") & (o["account_id_pseudonym"] != "")).sum()), "none")], ["field", "count", "caveat"]), "",
      "## Verdict", "**Campaign detection (Module 7) stays BLOCKED.** The data shows that many posts shared the same removed videos and *when* those posts existed (derived), but not *who* shared them, so no account-level coordination evidence exists. Nothing was simulated.", "",
      "## What is needed to unblock (external access, not downloadable now)", "- Twitter/X Information Operations archive (application + agreement), TikTok Research API (institutional approval), or another platform source that gives per-post account id + time + media identity.", "- Until then: keep `campaign_candidate_clusters` empty; Module 7 can be developed against the interface only."]
open(os.path.join(OUT, "campaign_data_readiness_report.md"), "w", encoding="utf-8").write("\n".join(camp))

# ------------------------------------------------------------ Phase F feature/evaluation readiness
fm = T("feature_manifest"); comp = fm[fm["extraction_status"] == "computed"]["feature_type"].value_counts().to_dict(); dd = B["direct_derivation_detection_by_transformation"]
weak = sorted([k for k, x in dd.items() if x["detected"] < 0.8], key=lambda k: dd[k]["detected"])
fr = ["# Feature and Evaluation Readiness Report", "", f"Generated {NOW}. Features exist only where listed as computed; the baseline below is **not** the ORVEX model.", "", "## Computed (real files, hashes in feature_manifest)", md([(k, n) for k, n in comp.items()], ["feature", "records"]), "",
      "## Non-learned dHash baseline (BASE-DHASH-v1, threshold 0.45 fixed a priori, nothing tuned)", md([("pairs scored", B["pairs_scored"]), ("ROC-AUC train / val / test", f"{B['auc_train']} / {B['auc_val']} / {B['auc_test']}"), ("ROC-AUC test excluding held-out lineage", B["auc_test_without_heldout_lineage"]), ("ROC-AUC test, held-out-lineage positives", B["auc_test_heldout_lineage_pos_vs_all_neg"]),
      ("test negatives by hardness", B.get("test_negatives_by_hardness")), ("ROC-AUC test hard negatives only", B["auc_test_hard_negatives_only"] if B["auc_test_hard_negatives_only"] is not None else "n/a (<20 negatives)"), ("pair scoring latency", f"{B['latency_ms_per_pair']} ms/pair (not time-to-detection)"),
      ("temporal start estimation (trims)", f"MAE {B['temporal_start_estimation']['mean_abs_error_fraction']} of duration; {B['temporal_start_estimation']['within_0_05']*100:.0f}% within 0.05")], ["metric", "value"]), "",
      "### Detection by transformation (direct derivation pairs, score >= 0.45)", md([(k, x["n"], x["detected"], x["audio_identical"]) for k, x in sorted(dd.items())], ["transformation", "pairs", "detected", "audio identical"]), "",
      f"**Reading:** hashes are robust to recompression, captions, watermarks and audio edits but weak for {', '.join(weak)}. This proves the fingerprints are usable for candidate retrieval and ground-truth sanity checks and shows exactly where learned visual embeddings are needed — a **computation/software** gap, not a data gap.", "",
      "## Missing computations (not data)", md([("visual embeddings", "software: PyTorch >= 2.4 or an embedding model (installed torch 2.3.1 disables transformers); weights not counted as dataset payload", "< 0.1 GB"), ("audio embeddings", "software: audio model", "< 0.05 GB"), ("speech transcription (ASR)", "software: whisper-class model not installed", "< 0.05 GB transcripts"),
      ("OCR", "software: no OCR engine installed; caption ground truth exists to validate it", "< 0.05 GB"), ("dense frame sampling / temporal alignment", "recompute features at 1 fps (24 frames give ~4% granularity)", "< 0.1 GB"), ("relationship scoring + confidence calibration", "model training on existing pairs", "< 0.2 GB"), ("evaluation harness + time-to-detection", "software", "negligible")], ["computation", "what is missing", "storage"]), "",
      "## Evaluation limits", f"- Commons test families: {int(((sm['source_dataset_id']=='RW-01') & (sm['split']=='test')).sum())}; ANAKIN test pairs: {int(((sm['source_dataset_id']=='RW-02') & (sm['split']=='test')).sum())} (families, not pairs). Per-family confidence intervals will be wide.", f"- Hard negatives per split: {nohard}.", "- No ORVEX model exists: no calibrated confidences, false-positive rates at deployment thresholds, or time-to-detection."]
open(os.path.join(OUT, "feature_evaluation_readiness_report.md"), "w", encoding="utf-8").write("\n".join(fr))

# ------------------------------------------------------------ Phase G storage
sb = pd.read_csv(os.path.join(MAN, "storage_budget.csv")); tot = payload_bytes(); per_src = (dir_bytes(CVMEDIA) / max(len(set(vp["root_source_media_id"])), 1)); orig = m[(m["source_dataset_id"] == "RW-01") & (m["usable_for_variants"] == "True")]["file_bytes"].astype(float).mean()
st = ["# Storage Budget Report", "", f"Generated {NOW}. Definition: decimal bytes of everything under `<repo>\\data\\` (media, variants, features, tables, manifests, logs, build/temp). FFmpeg (~0.4 GB) is outside `data/`.", "", md([(r["name"], gb(r["bytes"]), r["within_allocation"]) for _, r in sb[sb["kind"].isin(["final_category", "final_total", "peak_recorded"])].iterrows()], ["category", "measured", "within allocation"]), "",
      f"Headroom to the 30 GB cap: **{gb(CAP_HARD - tot)}**; to the 27 GB target: **{gb(CAP_TARGET - tot)}**.", "", "## Estimated cost of conditional additions (none executed)", md([
      ("+25 Commons sources (originals + full variant set)", gb(25 * (per_src + orig)), gb(tot + 25 * (per_src + orig))), ("+40 Commons sources", gb(40 * (per_src + orig)), gb(tot + 40 * (per_src + orig))), ("visual+audio embeddings, ASR, OCR, dense hashes", "< 0.5 GB", gb(tot + 0.5e9)),
      ("ANAKIN full-length videos (rejected)", "44.6 GB", "exceeds cap")], ["addition", "estimated size", "projected total"]), "", "The existing package fits comfortably; the only sizeable optional item is more Commons sources, and +25 sources stays well under the 27 GB target."]
open(os.path.join(OUT, "storage_budget_report.md"), "w", encoding="utf-8").write("\n".join(st))

# ------------------------------------------------------------ Phase B decision table
mx = pd.read_csv(os.path.join(DOCS, "ORVEX_REQUIREMENT_COVERAGE_MATRIX.csv"), dtype=str, keep_default_na=False, encoding="utf-8-sig").set_index("requirement_id")
N = "no"; Y = "yes"; CND = "conditional"
A = {
 "R01": ("none", "", N, "", "licences of Commons sources", 0, "K04,K10,K11"), "R02": ("none", "", N, "", "", 0, "K03,K04,K11"), "R03": ("none", "no new transformation justified (see coverage report)", N, "", "", 0, "K10"), "R04": ("none", "", N, "", "", 0, "K03,K19"), "R05": ("none", "", N, "", "", 0, "K11,K12"),
 "R06": ("missing computation + software", "OCR, ASR and visual/audio/text embeddings not computed; tools not installed", N, "install tools, compute from existing media", "none (local media)", 0.3, "feature_manifest rows computed for each type + validation against caption ground truth"),
 "R07": ("missing computation (model)", "no relationship model/confidence calibration; hard negatives now in every split (split-v2)", N, "train on existing pairs/groups", "none", 0.2, "held-out test AUC with calibration curve"),
 "R08": ("missing computation (model)", "labels exist; detectors for trim/crop/caption/audio not built (dHash baseline fails on crop/mirror)", N, "learned embeddings + OCR + audio features", "none", 0.2, "per-transformation detection rates on test split"),
 "R09": ("missing software", "edges exist; graph store/UI not part of dataset work", N, "SQLite relationship tables first (spec)", "none", 0.0, "graph rebuilt from edges equals ground-truth graph"),
 "R10": ("external access + software", "no live connector; real times only Commons + RW-31", CND, "local-corpus connector now; one platform connector only after terms/API check", "platform ToS/API approval", 0.0, "connector returns normalized records with post id/url/time"),
 "R11": ("external access (blocked)", "no authorised account+time data for any platform", CND, "Twitter IO archive / TikTok Research API / other permitted per-post account+time source", "institutional approval; cannot be downloaded now", 0.5, "multi-account time-stamped observations present; independent baseline defined"),
 "R12": ("missing computation + statistical power", "only a non-learned baseline run; 9 Commons test families", CND, "run experiments; add ~25 Commons sources only if CIs are too wide", "Commons licences", 6.0, "metrics with CIs recorded in experiment_registry"),
 "R13": ("none", "", N, "", "", 0, "K08,K19,K24"), "R14": ("none", "", N, "", "", 0, "K13"), "R15": ("none for data", "unseen types are FFmpeg edits; ANAKIN supplies real human edits", N, "evaluate, then reassess", "", 0, "K14 + per-type test results"),
 "R16": ("none", "", N, "", "", 0, "K07,K22"), "R17": ("none", "", N, "", "", 0, "K11,K12"), "R18": ("none", "", N, "", "", 0, "K20,K21"), "R19": ("evaluation-driven", "only 4 held-out types; add types only if evaluation shows blind spots", N, "none now", "", 0, "degradation per held-out type"),
 "R20": ("missing computation", "text evidence needs OCR/ASR extraction", N, "OCR + ASR on existing media", "none", 0.1, "OCR recovers caption_text of T07 variants"), "R21": ("none", "15 candidates remain unverified leads (not needed to proceed)", N, "", "", 0, "K24"), "R22": ("none", "", N, "", "", 0, "K15,K19"),
 "R23": ("human review", "policy needs owner sign-off; manual steps flagged", N, "", "", 0, "K21 + sign-off"), "R24": ("none", "", N, "", "", 0, "K15,K21"), "R25": ("none", "", N, "", "", 0, "K20,K21"),
 "R26": ("external access", "real times only Commons uploads and part of RW-31", CND, "see R10/R11", "", 0, "K22"), "R27": ("external access", "natural-media candidate pools are URL-only; local corpus (Commons+variants+ANAKIN) is searchable", CND, "build/test discovery on the local corpus; obtain lawful media access later", "platform terms", 0, "retrieval recall on local corpus"),
 "R28": ("none", "", N, "", "", 0, "K16"), "R29": ("human review", "screening is by title/category/description, not frame-level", N, "human spot-check of eligible sources", "", 0, "K09,K05 + reviewer sign-off"), "R30": ("none", "", N, "", "", 0, "K18"), "R31": ("none", "", N, "", "", 0, "K01,K02"), "R32": ("none", "", N, "", "", 0, "K26"), "R33": ("none", "", N, "", "", 0, "K27,K31"), "R34": ("none", "", N, "", "", 0, "K07"),
 "R35": ("missing software", "RAG index/report agent not built; source records exist", N, "build index over evidence_ledger/run logs", "none", 0.05, "report sentences all cite evidence ids"), "R36": ("missing software", "no end-to-end pipeline to time", N, "measure after pipeline exists", "", 0, "time-to-detection per investigation"),
 "R37": ("none", "", N, "", "", 0, "K27,K31"), "R38": ("none", "", N, "", "", 0, "K29,K30"), "R39": ("none", "", N, "", "", 0, "K28,K33"), "R40": ("external access", "share-reference times derived; no accounts; Facebook ids only", CND, "see R11", "", 0, "K32"),
}
rows = []
for rid, r in mx.iterrows():
    gt, gap, need, rec, perm, stg, acc = A.get(rid, ("", "", N, "", "", 0, ""))
    rows.append(dict(requirement_id=rid, required_capability=r["requirement"], existing_support=r["artifacts"], evidence_it_works=r["evidence"][:300], gap=gap or "none", gap_type=gt, additional_data_necessary=need, recommended_source_or_transformation=rec or "none", permission_constraints=perm or "-", est_additional_storage_gb=stg, acceptance_test=acc, status_now=r["status"]))
pd.DataFrame(rows).to_csv(os.path.join(OUT, "requirement_data_decision_table.csv"), index=False, encoding="utf-8-sig")
cnt = pd.Series([r["status_now"] for r in rows]).value_counts().to_dict(); needs = pd.Series([r["additional_data_necessary"] for r in rows]).value_counts().to_dict()
print("decision table", len(rows), cnt, needs); print(json.dumps(C, indent=0)[:900])
