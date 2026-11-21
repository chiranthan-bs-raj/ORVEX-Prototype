# ORVEX Final Dataset Necessity Audit

Date: 2026-10-27. Everything below was measured from the current files (not from earlier reports). Validation: **38 tests passed, 34/34 acceptance checks passed**; requirement status **27 PASS, 11 PARTIAL, 2 BLOCKED, 0 FAIL** (40 requirements). Payload **17.24 GB** (cap 30 GB).

## The direct answer

**Can the complete ORVEX project proceed using the existing real-world datasets and the controlled variants derived from them, or is any additional dataset genuinely necessary?**

**It can proceed. No additional dataset is necessary to build and evaluate Phase 1 (relationship learning) or the Phase 2 discovery pipeline on the local corpus.** The 17.24 GB package already contains eligible real media (96 Commons videos, 55 usable sources; 250 real human-edited ANAKIN pairs), 1,131 validated controlled variants with complete lineage, 299,875 relationship edges, 13,659 labelled pairs, 110 groups, source-family splits and evidence records.

What is *not* achievable with the existing data — and cannot be fixed by downloading more:
1. **Module 7 (campaign detection) is BLOCKED.** No open real dataset provides per-post account + time evidence. This needs authorised access (Twitter/X IO archive, TikTok Research API or similar), not more files.
2. **Time-to-detection (R36) is BLOCKED** until an end-to-end pipeline exists (software, not data).
3. **Natural-media evaluation on circulating videos is conditional:** FVC, FIVR-200K, VCSL and RW-31 provide URLs/IDs only; their videos can only be used after lawful platform access.

Everything else outstanding is **computation, software or human review** (embeddings, OCR, ASR, dense frame sampling, model training and calibration, graph store, report agent, spot-check of source footage). One optional, evidence-based data expansion exists (more Commons sources for statistical power, below), but it is not a prerequisite.

## What this audit found and changed

| # | Finding (measured) | Type | Action |
|---|---|---|---|
| 1 | `split-v1` test split had **0 same-theme hard negatives** (126 easy, 2 audio-link). Hard-negative evaluation was impossible. | schema/split gap, **not a data gap** | Re-split by theme groups (`split-v2`): hard negatives now train 157+ / val 29 / test 36; leakage and held-out checks still pass. |
| 2 | Stage `s5` was not idempotent (a re-run duplicated controlled edges/evidence); run logs were counted as dataset files in the checksum check | pipeline bug | Fixed; edges back to 299,875, 0 duplicate IDs; logs excluded from checksums. |
| 3 | `experiment_registry` was empty although the features can already be tested | missing computation | Ran a **non-learned dHash baseline** (BASE-DHASH-v1); 8 metric rows recorded; clearly labelled not the ORVEX model. |
| 4 | All 1,131 variants independently re-validated (ffprobe readable 1,131; metadata tag 1,131; parent chain 1,131; audio donors real/eligible 99 of 99; caption text real for 110 of 110; run log passed 1,131; failed 2 excluded, no file kept) | validation | No regeneration needed. |
| 5 | No data was downloaded and no variant was generated in this audit | — | Existing package was sufficient. |

## Deliverable 1 — Full-project requirement-to-data coverage matrix
`docs/datasets/necessity_audit/requirement_data_decision_table.csv` (40 requirements × required capability, existing support, evidence, gap, gap type, additional data necessary yes/no/conditional, recommended source/transformation, permission constraints, estimated storage, acceptance test, status). Decision counts: **34 "no additional data", 6 "conditional"** (R10, R11, R12, R26, R27, R40 — all external-access or statistical-power items). Non-PASS requirements:

| ID | Status | Reason (gap type) |
|---|---|---|
| R06 | PARTIAL | OCR/ASR/embeddings not computed; tools not installed (computation + software) |
| R07 | PARTIAL | no relationship model or calibrated confidence (computation) |
| R10 | PARTIAL | no live platform connector; real times only Commons + RW-31 (external access) |
| R11 | **BLOCKED** | no authorised account+time data (external access) |
| R12 | PARTIAL | only a non-learned baseline run; 7 Commons test families (computation + statistical power) |
| R15 | PARTIAL | unseen types are FFmpeg edits; ANAKIN gives real human edits |
| R19 | PARTIAL | only four held-out types; extend only if evaluation shows blind spots |
| R20 | PARTIAL | text evidence needs OCR/ASR (computation) |
| R26 | PARTIAL | real times only for Commons uploads and part of RW-31 (external access) |
| R27 | PARTIAL | natural-media candidate pools are URL-only (external access) |
| R35 | PARTIAL | RAG index/report agent not built (software) |
| R36 | **BLOCKED** | no end-to-end system to time (software) |
| R40 | PARTIAL | tweet times derived from ids; no sharer accounts; Facebook ids only (external access) |

## Deliverable 2 — Inventory of datasets
`docs/datasets/necessity_audit/dataset_inventory.csv`. Real-world (31 candidates) by decision status: 2 media subsets downloaded and verified (RW-01 Commons, RW-02 ANAKIN); 5 metadata/annotations only (FVC 2018, FVC v2.0, FIVR-200K, VCSL, RW-31); 9 research leads left unverified; 6 excluded as not real-world (DFDC, FaceForensics++, Celeb-DF, FakeAVCeleb, AV-Deepfake1M, NewsCLIPpings); 3 duplicate versions; 3 excluded for licence/rights (HMDB51, UCF101, Kinetics); 2 inaccessible (Twitter/X IO, TikTok API); 1 legal review (YFCC100M). In total 15 entries have verification level `research_lead_unverified` (official terms not read), including some of the excluded ones. ORVEX-created: 15 tables + 1,131 variant media files. Search scope: 14 query themes + 3 Zenodo API searches on 2026-10-26; coverage is systematic, not exhaustive.

## Deliverable 3 — Missing datasets vs missing computations/software
- **Missing datasets (none necessary).** Conditional only: (a) authorised per-post account+time data for Module 7; (b) lawful media access for URL-only natural datasets; (c) ~25 more Commons sources *if* experiments show confidence intervals are too wide (7 Commons test families, 36 ANAKIN test pairs; +25 sources ≈ +6.1 GB → 23.4 GB).
- **Missing computations:** visual/audio embeddings, ASR, OCR, dense (1 fps) frame hashes, temporal alignment refinement, relationship scoring and calibration, experiments.
- **Missing software:** PyTorch ≥ 2.4 (installed 2.3.1 disables transformers), ASR and OCR engines, graph store, RAG/report agent, evaluation harness.
- **Human review:** spot-check eligible sources for non-real footage (screening was title/category based), reviewer sign-off on the policy and uncertain negatives.

## Deliverable 4 — Do **not** add
ANAKIN full-length videos (44.6 GB, over cap); any deepfake/synthetic benchmark (DFDC, FaceForensics++, Celeb-DF, FakeAVCeleb, AV-Deepfake1M) for the natural collection; HMDB51/UCF101/Kinetics (rights/licence unclear, no relationship labels); more variants of the same 55 sources; AI voice, face swap, text-to-video or simulated campaigns/accounts/timelines; extra transformation types before the existing 14 have been evaluated with a model.

## Deliverable 5 — Transformation coverage
`transformation_coverage_report.md` + `variant_independent_validation.json`. All PDF families covered (trim ×3, crop, caption, audio replace/mute/mix, recompress ×3, multi-step chains: 385 variants at depth ≥ 2). No new transformation is justified. Measured coverage of the baseline: hashes detect recompression/caption/watermark/audio edits at 96–99% but crop only 3.6%, mirror 14%, trims 67–80% — evidence that learned embeddings (computation) are needed, not more variants.

## Deliverable 6 — Feature and evaluation readiness
`feature_evaluation_readiness_report.md`. Computed: 24-frame dHash, audio PCM md5, audio envelope for all 1,727+ local media (4,660 hashed feature records). Baseline on the test split: **zero false matches** (all 150 negatives score exactly 0 — which is why hard-only, easy-only and overall AUC are identical, 0.8307), but 34% of positives also score 0, so AUC = 0.83 (0.85 without held-out lineage, 0.79 for held-out lineage). Trim start estimated with MAE 0.076 of duration (24 sampled frames limit resolution). Pair-scoring latency 0.019 ms (not time-to-detection). Not done: embeddings, OCR, ASR, calibration, any learned model.

## Deliverable 7 — Campaign-data readiness
`campaign_data_readiness_report.md`. RW-31 supplies: 8,122 video records (metadata only), 881 publish timestamps (timezone unstated), 935 channel ids (video publishers, not sharers), 420 removal timestamps, 257,326 Twitter post ids (times *derived* from the id snowflake; 2,236 outside the dataset's stated window flagged `second_derived_unverified`; **0 sharer accounts**), 83,222 Facebook post ids (no URL/account/time). It evidences *that* posts existed and *when* (derived), not *who* shared. Coordination status is `not_assessed` everywhere; the campaign table stays empty.

## Deliverable 8 — Storage budget
`storage_budget_report.md`, `data/manifests/storage_budget.csv`. 17.24 GB measured (variants 12.50, ANAKIN 2.52, Commons 1.69, tables 0.42, raw metadata 0.07, manifests 0.05); peak recorded 17.24 GB; headroom 12.76 GB to the cap. Conditional additions cost < 0.5 GB (computations) or ≈ 6.1 GB (+25 sources).

## Deliverable 9 — Modifications made in this audit (with validation)
- Modified code: `scripts/datasets/s5_features_pairs_splits.py` (theme-grouped `split-v2`; idempotent edges/evidence), `s7_manifests.py`, `audit.py` (boolean coercion, checksum rule), `s6_docs.py`/`schema.py` (experiment registry wording), policy `docs/datasets/ORVEX_DATA_USE_AND_EVIDENCE_POLICY.md` (split rule).
- New: `s8_necessity_audit.py`, `s9_feature_baseline.py`, `patch_round5.py`, `patch_round6.py`, `docs/datasets/necessity_audit/*` (this report, decision table, inventory, coverage/feature/campaign/storage reports, baseline JSON, variant validation JSON).
- Regenerated from the scripts: `split_manifest`, `training_pairs` (13,659; train 6,878 / val 1,329 / test 1,721 / excluded 3,731), `group_examples` (110), `controlled_variant_registry` (`source_split`, `usable_for_training`: 673 trainable), `media_relationship_edges`, `evidence_ledger`, `feature_manifest`, `experiment_registry` (8 rows), manifests/checksums. **Variants, source media and the PDF were not touched; no data was downloaded.**
- Validation after changes: `python -m pytest tests/test_dataset_package.py` → **38 passed**; acceptance checks **34/34**; leakage K13 and held-out K14 pass on `split-v2`.

## Deliverable 10 — Final status per requirement
All 40 statuses with evidence and test ids are in `requirement_data_decision_table.csv` (`status_now`, `evidence_it_works`, `acceptance_test`). **PASS (27)** means the check ran against the actual files and passed, not merely that a file exists. **Do not read PASS as "capability implemented"**: R08/R09/R35-type capabilities need the computation/software above.

## Remaining blockers
1. Module 7 campaign detection — authorised per-post account+time data (external).
2. Time-to-detection — requires a built pipeline.
3. Natural-media evaluation on FVC/FIVR/VCSL/RW-31 videos — lawful media access (external).
4. Human spot-check of source footage and policy sign-off.
