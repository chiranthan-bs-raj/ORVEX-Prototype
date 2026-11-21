# ORVEX Complete Dataset Audit (repository-wide, read-only)

**Audit date:** 2026-10-27  |  **Repository inspected:** `<repo>` (the only repository available; no network access used; no data downloaded or generated)

**Note on the request:** the audit prompt was truncated at question 20 ("Which datasets support OCR, ASR, visual embe..."). Questions 1-19 are answered in full and 20 in the part that is visible; any later questions were not received.

## 1. Scope and method
- Walked every file (2,133 files, 17.93 GB; audit output folder and `__pycache__` excluded) and mapped each file to a stable audit ID (`DS-001`...`DS-040`); sizes reconcile exactly to the repository total.
- Re-probed all 1,728 media files with ffprobe; re-hashed all Commons + ANAKIN media and 200 random variants against `data/manifests/checksums.sha256`.
- Read the schema of 64 structured files/sheets from the actual data (not READMEs) and computed per-column null/distinct/type statistics for all 1269 columns/fields.
- Traced code usage by AST/regex over `scripts/` and `tests/` (project code only; the audit scripts exclude themselves).
- Specification: `ORVEX_Complete_Project_Specification.pdf` re-read in this audit (13 pages, sha256 55cbb2d8118d992d…; Modules found [1, 2, 3, 4, 5, 6, 7, 8, 9]; Phase 1/2 (True, True); §10.2-10.4 True). **No spec.md, phase.md or README.md exists** (none found); there is **no Git repository** (no history to inspect).
- Evidence hierarchy used exactly as defined in the request; anything not established is marked NOT VERIFIED.

## 2. Headline numbers (all measured, definitions stated)
| measure | value |
|---|---|
| Audit IDs (data-bearing datasets / non-dataset assets) | 40 (33 / 7) |
| Verified datasets (inspected, usable for at least one use) | 27 |
| Metadata-only datasets (no media locally) | 6 (DS-006..DS-011) |
| Unverified (downloaded, integrity/contents not checked) | 1 (DS-004 ANAKIN masks) |
| Datasets with verified code use (preprocessing/evaluation/test) | 31 |
| Referenced-only or unused datasets | 2 |
| Used for TRAINING | 0 (no model exists) |
| Used for EVALUATION (non-learned baseline only) | 8 |
| Used by RUNTIME modules | 0 (no application exists) |
| Derived datasets/artefacts (have a parent dataset) | 20 |
| Real media readable / discovered | 1727 / 1728 |
| Controlled variants on disk / passed / failed | 1132 / 1131 / 2 |
| Labelled pairs (in a split / total) | 9928 / 13659 |
| Dataset payload (`data/`) | 17241741313 bytes = 17.242 GB; limit 30 GB; remaining 12.758 GB |
| Findings (High/Medium/Low/Info) | 24 (Medium 11, Low 7, Info 5, High 1) |

## 3. What exists and where (summary; full detail in `dataset_inventory.csv`)
| ID | dataset | availability | path | files | records | size | necessity |
|---|---|---|---|---|---|---|---|
| DS-001 | Wikimedia Commons CC/PD video originals | Local files | data/real_world/media/commons | 96 | 96 | 1687143702 B | Essential |
| DS-002 | Commons source metadata (candidate records) | Local files | data/real_world/raw_metadata/commons/commons_candidates.json | 1 | 96 | 139714 B | Essential |
| DS-003 | ANAKIN subset: trimmed + edited videos | Local files | data/real_world/media/anakin | 500 | 250 | 2392113142 B | Useful and justified |
| DS-004 | ANAKIN subset: edit masks | Local files | data/real_world/media/anakin/masks | 89 | 89 | 128979239 B | Underutilized |
| DS-005 | ANAKIN metadata and official listing | Local files | data/real_world/raw_metadata/hf_api | 5 | 1023 | 1033853 B | Essential |
| DS-006 | InVID Fake Video Corpus 2018 (v3): URLs and labels | Metadata only (no media) | data/real_world/raw_metadata/invid_fvc_2018 | 5 | 5579 | 650024 B | Conditionally useful |
| DS-007 | InVID Fake Video Corpus v2.0: URLs, labels, manipulation types | Metadata only (no media) | data/real_world/raw_metadata/invid_fvc_v2 | 4 | 227 | 74758 B | Conditionally useful |
| DS-008 | InVID Fake Video Corpus v1.0: URLs and annotations | Metadata only (no media) | data/real_world/raw_metadata/invid_fvc_v1 | 3 | 59 | 27904 B | Redundant |
| DS-009 | FIVR-200K: YouTube ids, events, relation annotations | Metadata only (no media) | data/real_world/raw_metadata/invid_fivr200k | 5 | 225960 | 17873355 B | Conditionally useful |
| DS-010 | VCSL: video URLs, copied-segment labels, pair/split files | Metadata only (no media) | data/real_world/raw_metadata/vcsl | 9 | 9207 | 42201384 B | Conditionally useful |
| DS-011 | COVID-related misinformation videos and their spread (RW-31) | Metadata only (no media) | data/real_world/raw_metadata/covid_misinfo_4557828/covid-misinfo-videos.csv.gz | 1 | 8122 | 4198098 B | Useful and justified |
| DS-012 | Official record snapshots (Zenodo API, GitHub READMEs/licence) | Local files | data/real_world/raw_metadata | 11 | 11 | 61057 B | Essential |
| DS-013 | Controlled variant media | Local files | data/controlled_variants/media | 1132 | 1132 | 12500690021 B | Essential |
| DS-014 | Controlled variant registry | Local files | data/derived/tables/controlled_variant_registry.csv | 1 | 1133 | 1094515 B | Essential |
| DS-015 | Transformation run log | Local files | data/derived/tables/transformation_run_log.csv | 1 | 1133 | 954337 B | Useful and justified |
| DS-016 | Real-world media master | Local files | data/derived/tables/real_world_media_master.csv | 1 | 252270 | 148756771 B | Essential |
| DS-017 | Media relationship edges | Local files | data/derived/tables/media_relationship_edges.csv | 1 | 299875 | 149867390 B | Essential |
| DS-018 | Platform observations | Local files | data/derived/tables/platform_observations.csv | 1 | 352702 | 110755040 B | Useful and justified |
| DS-019 | Evidence ledger | Local files | data/derived/tables/evidence_ledger.csv | 1 | 1237 | 670524 B | Useful and justified |
| DS-020 | Feature manifest | Local files | data/derived/tables/feature_manifest.csv | 1 | 5187 | 2252894 B | Useful and justified |
| DS-021 | Visual 24-frame dHash features | Local files | data/derived/features/visual_dhash24.jsonl | 1 | 1727 | 1133311 B | Essential |
| DS-022 | Audio fingerprint features | Local files | data/derived/features/audio_fingerprint.jsonl | 1 | 1727 | 216956 B | Useful and justified |
| DS-023 | Training pairs | Local files | data/derived/tables/training_pairs.csv | 1 | 13659 | 4719493 B | Essential |
| DS-024 | Group examples (5-6 videos) | Local files | data/derived/tables/group_examples.csv | 1 | 110 | 37349 B | Underutilized |
| DS-025 | Split manifest (split-v2) | Local files | data/derived/splits/split_manifest.csv | 1 | 305 | 72085 B | Essential |
| DS-026 | Duplicate map | Local files | data/derived/tables/duplicate_map.csv | 1 | 378 | 78429 B | Useful and justified |
| DS-027 | Source registry | Local files | data/manifests/source_registry.csv | 1 | 31 | 23226 B | Useful and justified |
| DS-028 | Download/access attempt log | Local files | data/manifests/download_access_attempt_log.csv | 1 | 729 | 215252 B | Useful and justified |
| DS-029 | Campaign candidate clusters | Local file, 0 records | data/derived/tables/campaign_candidate_clusters.csv | 1 | 0 | 219 B | Required but unavailable |
| DS-030 | Experiment registry | Local files | data/derived/tables/experiment_registry.csv | 1 | 8 | 3979 B | Useful and justified |
| DS-031 | Manifests (checksums, crosswalk, attribution, selection plan, storage budget, protocol) | Local files | data/manifests | 6 | 6 | 41965067 B | Useful and justified |
| DS-032 | Build intermediates and run logs | Local files | data/manifests | 72 | 72 | 3706024 B | Redundant |
| DS-033 | Acceptance and QA report artefacts | Local files | data/reports | 3 | 3 | 32201 B | Useful and justified |
| DS-034 | Dataset documentation corpus (docs/datasets, incl. necessity_audit) | Local files | docs/datasets | 21 | 21 | 412378 B | Useful and justified |
| DS-035 | ORVEX_Literature corpus (35 PDFs, text, review workbook) | Local files | ORVEX_Literature | 77 | 77 | 240494329 B | Unused |
| DS-036 | ORVEX_Complete_Project_Specification.pdf | Local files | ORVEX_Complete_Project_Specification.pdf | 1 | 1 | 251692 B | Essential |
| DS-037 | LOOP-MIND novelty verification workbook | Local files | LOOP-MIND_Novelty_Independent_Verification_2_4_5.xlsx | 1 | 1 | 20779 B | Unsuitable for intended use |
| DS-038 | Tools: portable FFmpeg 9.0.2 | Local files | tools | 47 | 47 | 443989875 B | Useful and justified |
| DS-039 | Pipeline code and tests | Local files |  | 25 | 25 | 303686 B | Useful and justified |
| DS-040 | Root-level miscellaneous files | Local files |  | 2 | 2 | 149 B | Unused |

## 4. Most important findings (full list: `dataset_audit_findings.md`)
- **F-001 [High]** Requirement matrices list PASS for capabilities (graph, manipulation analysis, reporting) — No application/model code, notebooks, checkpoints or databases exist (no package.json/pyproject/backend/frontend; 0 model artifacts); only data pipeline scripts s1-s9 and one non-learned baseline
- **F-002 [Medium]** Completion report/QA: failed variants have 'no file kept'; registry local_path blank — File data/controlled_variants/media/P87190658/CV-P87190658-V10.mp4 (3091227 bytes) exists on disk for failed variant ['CV-P87190658-V10']; 1,132 files on disk vs 1,131 passed; the file is also listed in checksums.sha256
- **F-003 [Medium]** source_registry/candidates/policy: FIVR annotation has ND/DS/CS (IS implicit) — annotation.json holds IS labels: {'ND': 1327, 'DS': 5839, 'CS': 1855, 'IS': 3543}; 3543 edges have normalized_relation_type 'IS' (not normalised)
- **F-004 [Medium]** edges reference existing media — 61 RW-06 edges point to candidate ids absent from youtube_ids.txt (59 such ids in the source); no master rows exist for them
- **F-005 [Medium]** policy/dictionary: FVC labels are fake or real — FVC files contain label values {'fake': 2920, 'real': 2164, 'uncertain': 340, 'debunked': 89, 'parody': 66}; 495 master rows normalised to not_assessed
- **F-006 [Medium]** Dataset documented as FVC.csv + FVC_dup.csv only — Archive also contains FVC_text_queries.csv: event titles in English, French, Spanish, Russian, Arabic; header has 8 fields but rows have up to 21 (ragged); no ORVEX code reads it
- **F-007 [Medium]** inventory/registry list ANAKIN media as trimmed+edited — 89 mask zips (128979239 bytes) are on disk, absent from the media master, registry, features and evidence, not opened by any code, integrity unchecked
- **F-008 [Medium]** Splits: all descendants/near-duplicates of a source in one split — 9 near-duplicate original pairs (>=45% frame match) lie in different splits, e.g. [['RW-CMN-P145557116', 'RW-ANK-71d1y7-T', 0.54, 'val', 'train'], ['RW-ANK-95w389-T', 'RW-ANK-72y089-T', 0.71, 'train', 'test']]; ANAKIN selected cli
- **F-009 [Medium]** Negative pairs are 'unrelated' — 952 negatives; same-family: 0; touching duplicate records: 0; hard (same-theme) negatives by split: {'test': 36, 'train': 157, 'val': 29}; labelled uncertain
- **F-010 [Medium]** Licence register — VCSL dataset licence not stated (code MIT only); ANAKIN Vimeo source rights unverified; 25 Public-domain Commons files lack a licence URL; 2 files have no author stated
- **F-011 [Medium]** Reproducibility — 7 one-off scripts (patch_round2.py, patch_round3.py, patch_round4.py...) rewrote code and documents in place; no single runner documents the order; Gate-1 downloads were interactive (s1 only re-verifies)
- **F-012 [Medium]** Git provenance — No .git directory; .gitignore exists; no spec.md, phase.md or README.md; only the PDF states requirements

## 5. Requirement coverage and necessity
- `dataset_requirement_matrix.csv`: 34 dataset-to-requirement mappings; implementation references verified in code: 33 (the one unverified row is the masks dataset, which has no code). `module_data_coverage_matrix.csv`: groups A-H.
- Necessity decisions: {'Useful and justified': 16, 'Essential': 12, 'Conditionally useful': 4, 'Underutilized': 2, 'Redundant': 2, 'Unused': 2, 'Required but unavailable': 1, 'Unsuitable for intended use': 1}. No dataset is recommended for deletion; `DS-040`'s stray `nul` file and the failed variant file need approval before removal.
- **Missing evidence (not solvable by more videos):** per-post account + time evidence for campaign analysis; media bytes for natural datasets; OCR/ASR/embedding outputs; a learned model and its evaluation; time-to-detection.

## 6. Direct answers to the questions

**1. What datasets do I currently have?** 33 data-bearing datasets (DS-001..DS-033): real-world sources DS-001..DS-012 (Wikimedia Commons media+metadata, ANAKIN media/masks/metadata, FVC 2018/v2.0/v1.0, FIVR-200K, VCSL, COVID spread, official record snapshots) and ORVEX-created DS-013..DS-033 (variants, 15 tables, features, manifests, build artefacts, reports); plus 7 non-dataset assets (docs, literature, spec, LOOP-MIND workbook, FFmpeg, code, root misc).

**2. Physically present vs only referenced?** Physically present: all 33. Of the real-world datasets, media bytes are present only for DS-001 and DS-003 (+ masks DS-004); DS-006..DS-011 are metadata-only. Referenced only (in `source_registry.csv`, not present locally): 23 of 31 census candidates (e.g. RW-08, RW-09, RW-10, RW-11, RW-12, RW-13, RW-14, RW-15).

**3. Original source?** Commons: Wikimedia Commons contributors via the Commons API; ANAKIN: Hugging Face AlexBlck/ANAKIN (Black et al.); FVC/FIVR/COVID: Zenodo records 2535479, 1147958, 242481, 2564864, 4557828; VCSL: GitHub alipay/VCSL. Source = official URL recorded in the inventory; verification = repository snapshots (DS-012), **not re-fetched in this audit**. Created datasets originate in this repository's scripts.

**4. Where is each stored?** `Repository Path` column of `dataset_inventory.csv` (e.g. `data/real_world/media/commons`, `data/real_world/raw_metadata/<source>/`, `data/controlled_variants/media/`, `data/derived/tables/*.csv`, `data/derived/features/*.jsonl`, `data/manifests/`).

**5. What does each contain?** See `File Count`/`Record Count`/`Usable Data Count`: e.g. DS-001 96 videos; DS-003 250 pairs (500 videos); DS-013 1132 files; DS-016 252270 records; DS-017 299875 edges; DS-023 13659 pairs; DS-010 278885 labelled segments.

**6. How much raw data?** Real media: Commons 13.46 h (96 files), ANAKIN 0.94 h (500 files), variants 11.32 h; metadata-only sources hold 225,960 FIVR ids, 9,207 VCSL videos, 5,579 FVC URL rows, 8,122 COVID videos.

**7. How much is usable?** Commons 55 of 96 usable as variant sources; ANAKIN 250 pairs usable; variants 1131 passed (673 trainable); pairs 9928 in splits; native metadata rows are usable only as metadata (no media).

**8-9. Exact columns and meaning?** `dataset_column_dictionary.csv` (1269 rows, every column/nested path of 64 files, with type, null %, distinct count, example, role, usage) and `dataset_schema_report.md`; ORVEX table semantics come from `scripts/datasets/schema.py` (300 contract columns), raw-source semantics from their READMEs/cards; undocumented fields are flagged 'Unknown'.

**10-11. Original vs ORVEX-added columns, and how generated?** In the 15 ORVEX tables: 47 columns are original source fields (copied/normalised) and 259 are added by ORVEX (derived by rule, computed from media with ffprobe/OpenCV/FFmpeg/hashlib, analyst decisions, or bookkeeping). Producer functions with line ranges are in the dictionary (`Transformation Logic / Producer`) and `dataset_lineage.csv`.

**12. Provenance of labels/annotations/features/predictions?** Native labels (FVC fake/real/uncertain/debunked/parody, FIVR ND/DS/CS/IS, VCSL segments, ANAKIN manipulation types) = source annotations kept verbatim; controlled-lineage labels = ground truth by construction (run log); negatives = sampling rule (labelled uncertain); features = computed from media (dHash, audio fingerprints); **model predictions: none stored** (only aggregate non-learned baseline metrics).

**13. Naturally occurring real-world media?** Only DS-001 (user-uploaded Commons videos). DS-003 clips are real but commissioned human edits; DS-006..DS-011 describe naturally circulating videos but contain no media.

**14. Controlled variants from real media?** DS-013 (+ DS-014 registry, DS-015 run log): 1131 passed variants; all parent chains end in an eligible real source (1131 chains verified in this audit). One failed variant's file also remains on disk (F-002).

**15. URL/ID/metadata-only datasets?** DS-006 FVC 2018, DS-007 FVC v2.0, DS-008 FVC v1.0, DS-009 FIVR-200K, DS-010 VCSL, DS-011 COVID spread.

**16. Usable source-parent relationships?** Controlled lineage (DS-014/DS-017: 1131 direct edges, complete chains); ANAKIN trimmed->edited (250 local, 1,023 in metadata; directed per source); FVC cascades (membership only, no direction), FIVR (non-directional), VCSL (copy segments, direction unknown).

**17. Reliable transformation labels?** Controlled variants: 14 types with parameters, tool version, run id (reliable by construction); ANAKIN: 5 manipulation types (source annotation, commissioned edits); VCSL: partial copy only; FVC v2.0: manipulation type for 117 fake videos (metadata only).

**18. Video-copy / derivative-media detection?** With media: DS-013/014/023 (+ DS-003). Baseline evidence: non-learned dHash gives test ROC-AUC 0.8307 (zero false matches on 952 negatives but 34% of positives score 0). VCSL/FIVR/FVC supply labels without media.

**19. Robustness (crop, mirror, caption, watermark, recompression, trim, audio)?** DS-013 covers all: by type {'recompress_low': 220, 'watermark_overlay': 165, 'crop_center': 110, 'caption_burn_in': 110, 'reencode_hq': 55, 'trim_middle': 55, 'trim_head': 55, 'trim_tail': 55, 'audio_replace': 55, 'mirror_color_shift': 55, 'speed_change': 55, 'reupload_sim': 55, 'audio_noise_mix': 44, 'audio_mute': 42}; test split holds 143 variants from 7 Commons families (thin). Baseline detection: audio_replace 0.964, caption_burn_in 0.982, crop_center 0.036, mirror_color_shift 0.143, recompress_low 0.986, trim_middle 0.673, watermark_overlay 0.988.

**20. (partial) Which datasets support OCR, ASR, visual embe[ddings]...?** No dataset currently holds OCR, ASR/transcript or embedding outputs (feature_manifest marks them `not_computed`). The media needed to compute them exist in DS-001/DS-003/DS-013; caption ground truth for 110 variants can validate OCR; DS-006's unused `FVC_text_queries.csv` (multilingual titles) could support text comparison. Tools are not installed (PyTorch 2.3.1 disables transformers; no OCR/ASR engine).

## 7. Quality-control checklist (section 24)
| item | status |
|---|---|
| Complete accessible repository inspected | DONE (2,133 files mapped; sizes reconcile) |
| Authoritative spec read | DONE (PDF re-read; no spec.md/phase.md exists) |
| Every dataset has a stable ID and status | DONE (DS-001..DS-040) |
| Every relevant structured file's schema inspected | DONE (64 files; 1 ragged file handled by fallback) |
| Every column accounted for | DONE (1269 rows; descriptions for raw nested paths are 'not individually documented' where the repository has none) |
| Provenance assessed | DONE for repository evidence; external provenance NOT re-verified (no network) |
| Lineage mappings | DONE (1151 rows; no orphans except the failed-variant file) |
| Raw vs usable counts separated | DONE |
| Actual vs planned usage separated | DONE (`dataset_implementation_usage.csv`, `experiment_dataset_mapping.csv`) |
| Necessity/redundancy reasoning | DONE |
| Licensing/access | DONE from repository snapshots; legal review not performed |
| Storage vs 30 GB | DONE (measured) |
| Outputs agree with each other | DONE (`audit_consistency_check.json`: all_consistent=True) |
| No project data/code modified | VERIFIED: 0 existing files changed since the audit snapshot; 0 new files outside the audit folder |
| No datasets downloaded/created | VERIFIED (no network used; outputs only in docs/datasets/repository_audit/) |
| Existing reports not overwritten | VERIFIED (this folder is new; earlier `necessity_audit/` files untouched) |

### Not verified / limits
- External provenance and licence text were read from stored snapshots, not re-fetched. - Zip integrity of ANAKIN masks and platform URL liveness were not tested. - Column descriptions for nested raw JSON are inferred from structure where no documentation exists. - Per-frame content review of source footage (e.g. non-real material) was not performed. - Git history is unavailable.

## 8. Audit artefacts (exact paths)
- `docs/datasets/repository_audit/ORVEX_COMPLETE_DATASET_AUDIT.md`
- `docs/datasets/repository_audit/audit_consistency_check.json`
- `docs/datasets/repository_audit/dataset_audit_findings.csv`
- `docs/datasets/repository_audit/dataset_audit_findings.md`
- `docs/datasets/repository_audit/dataset_audit_summary.json`
- `docs/datasets/repository_audit/dataset_column_dictionary.csv`
- `docs/datasets/repository_audit/dataset_implementation_usage.csv`
- `docs/datasets/repository_audit/dataset_inventory.csv`
- `docs/datasets/repository_audit/dataset_licensing_and_access.csv`
- `docs/datasets/repository_audit/dataset_lineage.csv`
- `docs/datasets/repository_audit/dataset_necessity_assessment.csv`
- `docs/datasets/repository_audit/dataset_overlap_matrix.csv`
- `docs/datasets/repository_audit/dataset_quality_and_split_audit.md`
- `docs/datasets/repository_audit/dataset_requirement_matrix.csv`
- `docs/datasets/repository_audit/dataset_schema_report.md`
- `docs/datasets/repository_audit/dataset_storage_audit.md`
- `docs/datasets/repository_audit/experiment_dataset_mapping.csv`
- `docs/datasets/repository_audit/media_probe_results.csv`
- `docs/datasets/repository_audit/module_data_coverage_matrix.csv`
- `docs/datasets/repository_audit/repository_file_manifest.csv`
- `docs/datasets/repository_audit/audit_scripts/` (read-only audit code) and `_work/` (intermediate JSON).