# ORVEX Dataset Ecosystem Guide

Source of truth: the repository at `<repo>`, verified live (2133 files, 17927214201 bytes). Prior audit used as navigation, re-verified (`verification_against_prior_audit.json`).

## The problem in plain words
ORVEX investigates a reference video: find related media, decide whether others are derived from it (trim, crop, caption, audio swap, recompress...), keep evidence, draw a relationship graph and, only with real account/time evidence, flag possible coordinated campaigns. The authoritative source is `ORVEX_Complete_Project_Specification.pdf` (no spec.md/phase.md exists).
**Reality check:** the repository contains a data pipeline (`scripts/datasets/s1..s9`), tests, and one non-learned baseline. There is **no ORVEX application, trained model, OCR/ASR output or embedding**. So data readiness is far ahead of implementation readiness.

## A. Original source data
- **DS-001** 96 real Wikimedia Commons videos (13.46 h; 55 usable) - the only naturally occurring media; rights-cleared per file.
- **DS-003** 250 ANAKIN pairs (real clips + human edits, 500 videos); **DS-004** 89 unused mask zips (untracked).

## B. External datasets and metadata (no media locally)
DS-006 FVC 2018 (5,579 URL rows, cascades, labels), DS-007 FVC v2.0, DS-008 FVC v1.0 (superseded), DS-009 FIVR-200K (225,960 ids; ND/DS/CS/IS relations), DS-010 VCSL (9,207 URLs; 166,146 labelled pairs, 278,885 segments), DS-011 COVID spread (8,122 videos; 257,326 tweet ids, 81,159 Facebook ids; no sharer accounts). Their media rights belong to platforms/uploaders, so they stay metadata-only.

## C. Controlled variants
DS-013: 1131 validated FFmpeg variants (14 transformation types, chains to depth 3) from the 55 usable Commons originals; audio comes from another real recording, captions from another real record's title. They are constructed experiments, never natural posts. By type: {'recompress_low': 220, 'watermark_overlay': 165, 'crop_center': 110, 'caption_burn_in': 110, 'reencode_hq': 55, 'trim_middle': 55, 'trim_head': 55, 'trim_tail': 55, 'audio_replace': 55, 'mirror_color_shift': 55, 'speed_change': 55, 'reupload_sim': 55, 'audio_noise_mix': 44, 'audio_mute': 42}.

## D. Labels and relationship records
Native labels are kept verbatim; controlled lineage labels are ground truth by construction; negatives come from a sampling rule and are labelled `uncertain`. 40 audit IDs; 299,875 edges (DS-017); 13,659 pairs (DS-023).

## E. Derived features
Only 24-frame dHash and audio md5/envelope fingerprints exist for all 1,727 local media (DS-021/022). Embeddings, OCR, ASR, transcripts: `not_computed`.

## F. Training and evaluation data
split-v2 by source family: {'test': {'RW-01': 7, 'RW-02': 36}, 'train': {'RW-01': 40, 'RW-02': 175}, 'val': {'RW-01': 8, 'RW-02': 39}}; pairs {'train': 6878, 'excluded': 3731, 'test': 1721, 'val': 1329}. Four held-out transformation types are test-only. Only a non-learned baseline was evaluated (AUC 0.8307).

## G. Unused / unregistered data
ANAKIN masks (89 zips, 129 MB); `FVC_text_queries.csv` (multilingual event titles, never read); DS-024 group examples (no consumer); one failed-variant file on disk; stray `nul` file.

## H. Missing evidence
Per-post account + time evidence (campaign); media for natural datasets; OCR/ASR/embeddings; learned model + calibration; time-to-detection.

## I. End-to-end usage
| stage | status |
|---|---|
| Reference ingestion/discovery/UI | NOT implemented |
| Dataset collection, QC, dedupe, variants, features, pairs, splits | IMPLEMENTED (scripts) |
| Pair scoring | baseline only |
| Learned relationship model, confidence, graph builder, reports, campaign analysis, latency | NOT implemented / BLOCKED |

## Dataset cards
| id | name | source | path | records | size | usage | necessity |
|---|---|---|---|---|---|---|---|
| DS-001 | Wikimedia Commons CC/PD video originals | https://commons.wikimedia.org (file pages listed in DS-002) | data/real_world/media/commons | 96 | 1687143702 B | Preprocessing use verified; Evaluation use verified (feature | Essential |
| DS-002 | Commons source metadata (candidate records) | https://commons.wikimedia.org/w/api.php | data/real_world/raw_metadata/commons/commons_candi | 96 | 139714 B | Preprocessing use verified | Essential |
| DS-003 | ANAKIN subset: trimmed + edited videos | https://huggingface.co/datasets/AlexBlck/ANAKIN | data/real_world/media/anakin | 250 | 2392113142 B | Preprocessing use verified; Evaluation use verified (baselin | Useful and justified |
| DS-004 | ANAKIN subset: edit masks | https://huggingface.co/datasets/AlexBlck/ANAKIN | data/real_world/media/anakin/masks | 89 | 128979239 B | Reference only (downloaded by s2, never read) | Underutilized |
| DS-005 | ANAKIN metadata and official listing | https://huggingface.co/datasets/AlexBlck/ANAKIN | data/real_world/raw_metadata/hf_api | 1023 | 1033853 B | Preprocessing use verified | Essential |
| DS-006 | InVID Fake Video Corpus 2018 (v3): URLs and labels | https://zenodo.org/records/2535479 | data/real_world/raw_metadata/invid_fvc_2018 | 5579 | 650024 B | Preprocessing use verified | Conditionally useful |
| DS-007 | InVID Fake Video Corpus v2.0: URLs, labels, manipulation types | https://zenodo.org/records/1147958 | data/real_world/raw_metadata/invid_fvc_v2 | 227 | 74758 B | Preprocessing use verified | Conditionally useful |
| DS-008 | InVID Fake Video Corpus v1.0: URLs and annotations | https://zenodo.org/records/242481 | data/real_world/raw_metadata/invid_fvc_v1 | 59 | 27904 B | Preprocessing use verified | Redundant |
| DS-009 | FIVR-200K: YouTube ids, events, relation annotations | https://zenodo.org/records/2564864 | data/real_world/raw_metadata/invid_fivr200k | 225960 | 17873355 B | Preprocessing use verified | Conditionally useful |
| DS-010 | VCSL: video URLs, copied-segment labels, pair/split files | https://github.com/alipay/VCSL | data/real_world/raw_metadata/vcsl | 9207 | 42201384 B | Preprocessing use verified | Conditionally useful |
| DS-011 | COVID-related misinformation videos and their spread (RW-31) | https://zenodo.org/records/4557828 | data/real_world/raw_metadata/covid_misinfo_4557828 | 8122 | 4198098 B | Preprocessing use verified | Useful and justified |
| DS-012 | Official record snapshots (Zenodo API, GitHub READMEs/licence) | N/A (generated in this repository) | data/real_world/raw_metadata | 11 | 61057 B | Preprocessing use verified (provenance/licence evidence read | Essential |
| DS-013 | Controlled variant media | N/A (generated in this repository) | data/controlled_variants/media | 1132 | 12500690021 B | Preprocessing use verified; Evaluation use verified (baselin | Essential |
| DS-014 | Controlled variant registry | N/A (generated in this repository) | data/derived/tables/controlled_variant_registry.cs | 1133 | 1094515 B | Preprocessing + Evaluation use verified | Essential |
| DS-015 | Transformation run log | N/A (generated in this repository) | data/derived/tables/transformation_run_log.csv | 1133 | 954337 B | Test-only use (audit/tests) plus s4 writer | Useful and justified |
| DS-016 | Real-world media master | N/A (generated in this repository) | data/derived/tables/real_world_media_master.csv | 252270 | 148756771 B | Preprocessing use verified | Essential |
| DS-017 | Media relationship edges | N/A (generated in this repository) | data/derived/tables/media_relationship_edges.csv | 299875 | 149867390 B | Preprocessing use verified | Essential |
| DS-018 | Platform observations | N/A (generated in this repository) | data/derived/tables/platform_observations.csv | 352702 | 110755040 B | Test/audit use only downstream of s3 | Useful and justified |
| DS-019 | Evidence ledger | N/A (generated in this repository) | data/derived/tables/evidence_ledger.csv | 1237 | 670524 B | Preprocessing use verified | Useful and justified |
| DS-020 | Feature manifest | N/A (generated in this repository) | data/derived/tables/feature_manifest.csv | 5187 | 2252894 B | Preprocessing use verified | Useful and justified |
| DS-021 | Visual 24-frame dHash features | N/A (generated in this repository) | data/derived/features/visual_dhash24.jsonl | 1727 | 1133311 B | Evaluation use verified (baseline) | Essential |
| DS-022 | Audio fingerprint features | N/A (generated in this repository) | data/derived/features/audio_fingerprint.jsonl | 1727 | 216956 B | Evaluation use verified (baseline) | Useful and justified |
| DS-023 | Training pairs | N/A (generated in this repository) | data/derived/tables/training_pairs.csv | 13659 | 4719493 B | Evaluation use verified (baseline) | Essential |
| DS-024 | Group examples (5-6 videos) | N/A (generated in this repository) | data/derived/tables/group_examples.csv | 110 | 37349 B | Test/audit use only (no experiment) | Underutilized |
| DS-025 | Split manifest (split-v2) | N/A (generated in this repository) | data/derived/splits/split_manifest.csv | 305 | 72085 B | Preprocessing use verified (pairs/variants splits) | Essential |
| DS-026 | Duplicate map | N/A (generated in this repository) | data/derived/tables/duplicate_map.csv | 378 | 78429 B | Test/audit use only downstream of s3 | Useful and justified |
| DS-027 | Source registry | N/A (generated in this repository) | data/manifests/source_registry.csv | 31 | 23226 B | Test/audit use only downstream of s3 | Useful and justified |
| DS-028 | Download/access attempt log | N/A (generated in this repository) | data/manifests/download_access_attempt_log.csv | 729 | 215252 B | Preprocessing use verified (writer) / Test-audit use | Useful and justified |
| DS-029 | Campaign candidate clusters | N/A (generated in this repository) | data/derived/tables/campaign_candidate_clusters.cs | 0 | 219 B | Test/audit use only (empty) | Required but unavailable |
| DS-030 | Experiment registry | N/A (generated in this repository) | data/derived/tables/experiment_registry.csv | 8 | 3979 B | Evaluation use verified (written by s9) | Useful and justified |
| DS-031 | Manifests (checksums, crosswalk, attribution, selection plan, storage budget, protocol) | N/A (generated in this repository) | data/manifests | 6 | 41965067 B | Test/audit use | Useful and justified |
| DS-032 | Build intermediates and run logs | N/A (generated in this repository) | data/manifests | 72 | 3706024 B | Pipeline resume use verified | Redundant |
| DS-033 | Acceptance and QA report artefacts | N/A (generated in this repository) | data/reports | 3 | 32201 B | N/A | Useful and justified |
| DS-034 | Dataset documentation corpus (docs/datasets, incl. necessity_audit) | N/A (generated in this repository) | docs/datasets | 21 | 412378 B | N/A | Useful and justified |
| DS-035 | ORVEX_Literature corpus (35 PDFs, text, review workbook) | arXiv/CVF/EURASIP open copies (see ORVEX_Literature) | ORVEX_Literature | 77 | 240494329 B | Documented/reference | Unused |
| DS-036 | ORVEX_Complete_Project_Specification.pdf | N/A (generated in this repository) | ORVEX_Complete_Project_Specification.pdf | 1 | 251692 B | Documented/reference | Essential |
| DS-037 | LOOP-MIND novelty verification workbook | N/A (generated in this repository) | LOOP-MIND_Novelty_Independent_Verification_2_4_5.x | 1 | 20779 B | N/A | Unsuitable for intended use |
| DS-038 | Tools: portable FFmpeg 9.0.2 | N/A (generated in this repository) | tools | 47 | 443989875 B | N/A | Useful and justified |
| DS-039 | Pipeline code and tests | N/A (generated in this repository) |  | 25 | 303686 B | N/A | Useful and justified |
| DS-040 | Root-level miscellaneous files | N/A (generated in this repository) |  | 2 | 149 B | N/A | Unused |

## Answers to the 36 questions
**Q1-2.** 33 data-bearing datasets + 7 other assets; exact names in `DATASET_PROVENANCE_INVENTORY.csv`.

**Q3-4.** Provenance and entry method per dataset: provenance inventory columns `original_source`, `how_entered_project`, `provenance_category`.

**Q5.** `path` column of the inventory.

**Q6.** Media present only for DS-001, DS-003 (+DS-004 masks) and DS-013; DS-006..DS-011 are URL/ID/metadata-only.

**Q7-9.** `COMPLETE_COLUMN_DICTIONARY.csv`: 1269 fields, 813 flagged UNKNOWN SEMANTICS.

**Q10-11.** Dictionary columns `Original or Added`, `Derivation Kind`, `Transformation Logic / Producer`.

**Q12-13.** Inventory `records`, `usable`, `size` columns.

**Q14.** Lineage report + join keys.

**Q15.** DS-001 (natural), DS-003 (human-edited).

**Q16.** DS-013/DS-014.

**Q17.** Controlled variants (recorded), ANAKIN (source-annotated); FVC/FIVR/VCSL give non-directional or direction-unknown relations.

**Q18-19.** Training labels: DS-023 (controlled + ANAKIN); evaluation ground truth: same, with split-v2; natural-media ground truth lacks media.

**Q20.** `DATASET_TO_PROBLEM_STATEMENT_MATRIX.csv` (34 verified mappings).

**Q21-24.** `DATASET_TO_IMPLEMENTATION_MAP.csv` (227 code references) and the model/experiment map.

**Q25.** Limitations report and licensing (`repository_audit/dataset_licensing_and_access.csv`): VCSL licence not stated; ANAKIN Vimeo rights unverified.

**Q26.** Necessity report.

**Q27.** Gaps report.

**Q28.** Yes for controlled relationship learning and robustness (pairs, held-out types), but only 7 Commons test families and no model yet.

**Q29.** Partly: natural media absent; only the local corpus is searchable.

**Q30.** No: 0 sharer accounts; authorised external evidence required.

**Q31.** 813 fields undocumented; defects F-001..F-012.

**Q32.** Yes: 61 dangling edges, 1 failed-variant file, 9 cross-split near-duplicate candidates; 0 hash duplicates.

**Q33.** 17241741313 bytes data/ (17.242 GB; 12.758 GB under the 30 GB limit); repo 17927214201 bytes.

**Q34.** Retain everything for now; see retention column.

**Q35.** Compute embeddings/OCR/ASR on existing media, train and evaluate a learned model on split-v2, fix the table defects first.

**Q36.** See gaps report: external re-verification, mask integrity, URL liveness, footage review, Git history.
