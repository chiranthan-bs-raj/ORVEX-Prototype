# ORVEX Dataset Catalogue

Generated 2026-10-26T18:48:15Z. **Layer A = real-world data** (`data/real_world/`); **Layer B = ORVEX-created derivatives** (`data/controlled_variants/`, `data/derived/`). Search date 2026-10-26.

## A. Real-world datasets considered (all)

| id | dataset | release | decision | bytes or URLs | licence / terms | records held locally | local size | supports | verification |
|---|---|---|---|---|---|---|---|---|---|
| RW-01 | Wikimedia Commons CC/PD video pool (ORVEX selection) | API snapshot 2026-10-26 | included_selected_subset | media_bytes | Per file (machine-readable): CC0 / Public domain / CC BY / CC BY-SA on | 96 | 1,687,283,416 B (1.687 GB / 1.571 GiB) | Phase1: controlled variants, relationship ground truth, feature extrac | verified_api |
| RW-02 | ANAKIN: manipulated videos and mask annotations (incl. VideoSham edited videos) | HF dataset, last modified 2023-09-21 | included_selected_subset | media_bytes (edited, trimmed, masks, full) + metadata.csv with Vimeo URLs | cc-by-4.0 (dataset card) | 3,020 | 2,522,126,234 B (2.522 GB / 2.349 GiB) | Modules 3,4,5,9 (real edited pairs, manipulation types) | verified_api |
| RW-03 | InVID Fake Video Corpus 2018 (v3) | 2018-10-04 (Zenodo 2535479) | included_metadata_only | metadata_urls_only | cc-by-4.0 (Zenodo record) | 5,579 | 650,024 B (0.001 GB / 0.001 GiB) | Modules 3,6,7 (repost cascades, authenticity/misleading labels); evalu | verified_api |
| RW-04 | InVID Fake Video Corpus v2.0 | 2018-01-15 (Zenodo 1147958) | included_metadata_only | metadata_urls_only | cc-by-4.0 | 227 | 74,758 B (0.000 GB / 0.000 GiB) | Modules 4 (manipulation type evidence), 6 | verified_api |
| RW-05 | InVID Fake Video Corpus v1.0 | 2017-01-13 (Zenodo 242481) | excluded_duplicate_version | metadata_urls_only | cc-by-4.0 | 59 | 27,904 B (0.000 GB / 0.000 GiB) | n/a (superseded) | verified_api |
| RW-06 | InVID FIVR-200K (Fine-grained Incident Video Retrieval) | 2019-02-14 (Zenodo 2564864) | included_metadata_only | metadata_urls_only | cc-by-4.0 (Zenodo record) | 225,960 | 17,873,355 B (0.018 GB / 0.017 GiB) | Modules 3 (hard negatives: same-incident-not-copy), evaluation | verified_api |
| RW-07 | VCSL (Video Copy Segment Localization) | GitHub main (updates through 2023-12-20) | included_metadata_only | metadata_urls_only | Code: MIT. Dataset licence: not stated in README/LICENSE | 9,207 | 42,201,384 B (0.042 GB / 0.039 GiB) | Modules 3,4 (partial temporal copy), evaluation | verified_api |
| RW-08 | VCDB (Video Copy Detection Benchmark) | ECCV 2014 | research_lead_unverified | unverified | not read | 0 | 0 B (0.000 GB / 0.000 GiB) | would support partial copy evaluation | research_lead_unverified |
| RW-09 | A corpus of debunked and verified user-generated videos (journal paper record) | 2019-01-08 (Zenodo 2535495) | excluded_duplicate_version | paper PDF only | cc-by-4.0 | 0 | 0 B (0.000 GB / 0.000 GiB) |  | verified_api |
| RW-10 | WildDeepfake | 2021 | research_lead_unverified | unverified | not stated in search results | 0 | 0 B (0.000 GB / 0.000 GiB) | optional separate authenticity detector | research_lead_unverified |
| RW-11 | DFDC (DeepFake Detection Challenge) dataset | 2020 | excluded_not_real_world_for_scope | media_bytes | not read | 0 | 0 B (0.000 GB / 0.000 GiB) |  | verified_official_page |
| RW-12 | FaceForensics++ | 2019 | excluded_not_real_world_for_scope | media_bytes after approval | FaceForensics Terms of Use (request form) | 0 | 0 B (0.000 GB / 0.000 GiB) |  | verified_official_page |
| RW-13 | Celeb-DF / Celeb-DF++ | v2 / ++ 2025 | excluded_not_real_world_for_scope | media_bytes after approval | Terms to Use Celeb-DF (request form) | 0 | 0 B (0.000 GB / 0.000 GiB) |  | verified_official_page |
| RW-14 | FakeAVCeleb | 2021 | excluded_not_real_world_for_scope | media_bytes after approval | Request form; link sent after acceptance | 0 | 0 B (0.000 GB / 0.000 GiB) |  | verified_official_page |
| RW-15 | AV-Deepfake1M | ACM MM 2024 | excluded_not_real_world_for_scope | unverified | not read | 0 | 0 B (0.000 GB / 0.000 GiB) |  | verified_official_page |
| RW-16 | Deepfake-Eval-2024 | 2025 | research_lead_unverified | unverified | not read | 0 | 0 B (0.000 GB / 0.000 GiB) | optional separate authenticity detector | research_lead_unverified |
| RW-17 | VSC 2022/2023 Video Similarity Challenge dataset | 2023 | research_lead_unverified | unverified | Built from YFCC100M videos with CC licences allowing derivatives (pape | 0 | 0 B (0.000 GB / 0.000 GiB) | evaluation (visual) | research_lead_unverified |
| RW-18 | YFCC100M (video subset) | 2015 | legal_review_required | unverified | Per-item CC licence; metadata under Yahoo Webscope data-sharing agreem | 0 | 0 B (0.000 GB / 0.000 GiB) | scale-up source pool | research_lead_unverified |
| RW-19 | CC_WEB_VIDEO | 2007 | research_lead_unverified | unverified | not read | 0 | 0 B (0.000 GB / 0.000 GiB) |  | research_lead_unverified |
| RW-20 | SVD (Short Video Dataset) | ICCV 2019 | research_lead_unverified | unverified | not read | 0 | 0 B (0.000 GB / 0.000 GiB) |  | research_lead_unverified |
| RW-21 | NIST Nimble / Media Forensics Challenge data | NC2017 / MFC18 | research_lead_unverified | unverified | NIST registration terms (not read) | 0 | 0 B (0.000 GB / 0.000 GiB) | graph metric design | research_lead_unverified |
| RW-22 | Twitter/X Information Operations archive | 2018-2023 | excluded_inaccessible | unverified | Application + data agreement for unhashed data (per citing paper) | 0 | 0 B (0.000 GB / 0.000 GiB) | Module 7 (if access obtained) | research_lead_unverified |
| RW-23 | Pushshift Telegram dataset | 2020 | research_lead_unverified | unverified | not read | 0 | 0 B (0.000 GB / 0.000 GiB) | Module 6/7 prototype | research_lead_unverified |
| RW-24 | TikTok Research API (2024 US election videos, Luceri et al.) | 2025 | excluded_inaccessible | API only | Approved academic researchers only (per vendor blog; unverified) | 0 | 0 B (0.000 GB / 0.000 GiB) | Module 7 | research_lead_unverified |
| RW-25 | VideoSham | 2022 | excluded_duplicate_version | unverified | not read | 0 | 0 B (0.000 GB / 0.000 GiB) |  | verified_api |
| RW-26 | HMDB51 | 2011 | excluded_license | media_bytes | Authors label dataset CC BY 4.0; clips mostly from movies (rights of f | 0 | 0 B (0.000 GB / 0.000 GiB) |  | verified_official_page |
| RW-27 | UCF101 | 2012 | excluded_license | media_bytes | Conflicting third-party statements (CC0 / non-commercial / unknown); o | 0 | 0 B (0.000 GB / 0.000 GiB) |  | research_lead_unverified |
| RW-28 | Kinetics | 400/600/700 | excluded_license | metadata_urls_only | Conflicting: CC BY 4.0 (secondary catalogue) vs not specified/uploader | 0 | 0 B (0.000 GB / 0.000 GiB) |  | research_lead_unverified |
| RW-29 | NewsCLIPpings | EMNLP 2021 | excluded_not_real_world_for_scope | unverified | not read | 0 | 0 B (0.000 GB / 0.000 GiB) |  | research_lead_unverified |
| RW-30 | Datasets for coordinated behaviour (Pacheco 2021, Nizzoli 2021, Indiana coordinated-reply datasheet) | various | research_lead_unverified | unverified | platform terms (not read) | 0 | 0 B (0.000 GB / 0.000 GiB) | Module 7 method validation | research_lead_unverified |
| RW-31 | A dataset of Covid-related misinformation videos and their spread on social media | 2021-02-23 (Zenodo 4557828) | included_metadata_only | metadata_urls_only | cc-by-4.0 (Zenodo record) | 8,122 | 4,198,098 B (0.004 GB / 0.004 GiB) | Module 6 (post timeline), Module 7 (insufficient alone), Phase 2 timel | verified_api |

## B. ORVEX-created datasets

| table | purpose | derived from (source dataset ids) | uses | records | columns | ORVEX-added columns | added columns (first 10) | size | phase |
|---|---|---|---|---|---|---|---|---|---|
| source_registry | Every dataset/source considered, with official source, terms, access, size and decision. | census of all candidates | metadata/tables | 31 | 30 | 17 | source_dataset_id, accessed_date, derivative_use_status, training_use_status, redistribution_status, real_world_eligibility, media_origin_characterization, planned_download_bytes, actual_local_bytes, record_count_local… | 23,226 B (0.000 GB / 0.000 GiB) | both |
| real_world_media_master | Normalized master of every real-world media record (downloaded or metadata-only). Controll | RW-01, RW-02, RW-03, RW-04, RW-05, RW-06, RW-07 (metadata normalised; Commons+ANAKIN also media) | media files + metadata | 252,270 | 49 | 33 | media_id, source_dataset_id, platform_media_id, canonical_url, observed_time_utc, collected_time_utc, time_precision, duration_s, width, height… | 148,756,771 B (0.149 GB / 0.139 GiB) | both |
| controlled_variant_registry | Every controlled variant rendered by ORVEX from eligible real-world media. Never mixed wit | RW-01 (media files, titles for captions, audio of other records) | media files + metadata | 1,133 | 38 | 36 | variant_media_id, direct_parent_media_id, root_source_media_id, ancestor_chain, video_source_media_id, audio_source_media_id, caption_text_source_media_id, caption_text_origin_field, transformation_id, transformation_name… | 1,094,515 B (0.001 GB / 0.001 GiB) | phase1 |
| media_relationship_edges | Relationship edges: source-provided native relations (kept with original label) and contro | RW-02, RW-03, RW-06, RW-07 native relations + ORVEX-CTRL lineage from RW-01 | metadata/tables | 299,875 | 29 | 22 | relationship_id, source_dataset_id, relation_scope, evidence_id, media_a_id, media_b_id, normalized_relation_type, direction_status, parent_media_id, child_media_id… | 149,867,390 B (0.150 GB / 0.140 GiB) | both |
| platform_observations | Real posts/observations of media on platforms as provided by the sources (no invented post | RW-01 (upload records), RW-03 (cascade order) | metadata/tables | 352,702 | 22 | 16 | observation_id, media_id, observation_type, coordination_status, platform_post_id, account_id_pseudonym, account_id_source_field, observation_time_utc, time_precision, hashtags… | 110,755,040 B (0.111 GB / 0.103 GiB) | phase2 |
| evidence_ledger | Evidence records supporting labels, relations and rights decisions. | all included sources + ORVEX run logs | metadata/tables | 1,237 | 18 | 17 | evidence_id, evidence_type, source_dataset_id, subject_type, subject_id, source_record_ref, claim_supported, claim_status, observed_fact_vs_inference, verification_method… | 670,524 B (0.001 GB / 0.001 GiB) | both |
| feature_manifest | What features actually exist (and which are not computed). | computed from RW-01/RW-02 media and CD variants | media files + metadata | 5,187 | 15 | 15 | feature_record_id, media_id, feature_type, extraction_status, tool_name, tool_version, parameters_json, sample_timestamps, feature_format, storage_path… | 2,252,894 B (0.002 GB / 0.002 GiB) | both |
| training_pairs | Model examples (related/unrelated/uncertain pairs) with local media only, split by source  | RW-01 via variants; RW-02 native edit pairs | media files + metadata | 13,659 | 23 | 21 | example_id, media_a_id, media_b_id, relationship_id, label_binary_related, relationship_class, normalized_label, label_origin, label_status, evidence_id… | 4,719,493 B (0.005 GB / 0.004 GiB) | phase1 |
| campaign_candidate_clusters | Candidate clusters for human review. EMPTY: no authorised account+time evidence is availab | none (blocked: no authorised account+time evidence) | metadata/tables | 0 | 12 | 12 | cluster_id, observation_ids, media_ids, account_pseudonyms, time_window_start_utc, time_window_end_utc, common_media_signals, posting_pattern_signals, independent_coordination_evidence, candidate_status… | 219 B (0.000 GB / 0.000 GiB) | phase2 |
| transformation_run_log | One row per transformation execution. | RW-01 | metadata/tables | 1,133 | 15 | 15 | run_id, variant_media_id, input_media_ids, tool_name, tool_version, command_config, parameters_json, started_utc, return_code, output_validation_status… | 954,337 B (0.001 GB / 0.001 GiB) | phase1 |
| download_access_attempt_log | Every download/access attempt. | all | metadata/tables | 729 | 14 | 14 | attempt_id, source_dataset_id, media_or_file_id, url, attempt_time_utc, method, http_status, result_category, terms_decision, retry_count… | 215,252 B (0.000 GB / 0.000 GiB) | both |
| split_manifest | Source-family level split assignment. | RW-01, RW-02 | metadata/tables | 305 | 10 | 10 | split_version, source_family_id, source_dataset_id, split, assignment_method, seed, domain_stratum, n_family_items, n_native_edges, heldout_transformations_in_family | 72,085 B (0.000 GB / 0.000 GiB) | phase1 |
| experiment_registry | Evaluation registry. Holds only the non-learned dHash sanity baseline (BASE-DHASH-v1); no  | computed from CD features (non-learned baseline only) | metadata/tables | 8 | 12 | 12 | experiment_id, dataset_versions, split_version, label_map_version, model_version, feature_version, metric_name, metric_value, protocol, heldout_policy… | 3,979 B (0.000 GB / 0.000 GiB) | phase1 |
| duplicate_map | Exact/near duplicates and cross-version repeats; canonical record kept. | RW-01, RW-03/04/05, cross-source YouTube ids | metadata/tables | 378 | 6 | 6 | duplicate_id, canonical_media_id, duplicate_media_id, duplicate_type, evidence, resolution | 78,429 B (0.000 GB / 0.000 GiB) | both |
| group_examples | Groups of 6 videos (4 related family members + 2 distractors) with ground-truth edges (Mod | RW-01 via variants | media files + metadata | 110 | 13 | 13 | group_id, source_family_id, member_media_ids, n_members, family_member_ids, distractor_ids, truth_edges, n_truth_edges, split, split_version… | 37,349 B (0.000 GB / 0.000 GiB) | phase1 |

Controlled variant media files: **1,131** passed / 2 failed — 12,500,690,021 B (12.501 GB / 11.642 GiB). All columns of each created table are in `ORVEX_DATA_DICTIONARY.md`; origin of every column in `column_lineage.csv`.

## C. Required for the ORVEX problem statement

| real-world dataset | level | why |
|---|---|---|
| RW-01 Wikimedia Commons CC/PD pool | REQUIRED (core) | only open, per-file licensed source with media bytes eligible for controlled variants |
| RW-02 ANAKIN subset | REQUIRED for real edit-pair evaluation | real human edits with parent/child + manipulation type |
| RW-03 FVC 2018 (+RW-04 v2.0) | REQUIRED (metadata) | real repost cascades with fake/real labels |
| RW-06 FIVR-200K | REQUIRED (metadata) | same-incident vs copy labels for hard negatives |
| RW-07 VCSL | REQUIRED (metadata) | real segment-level partial-copy annotations |
| RW-05 FVC v1.0 | NOT NEEDED | superseded; kept only for duplicate mapping |
| RW-08..RW-30 | OPTIONAL / excluded | see selection document |

| created dataset | level |
|---|---|
| controlled_variant_registry + media | REQUIRED Phase 1 |
| media_relationship_edges | REQUIRED both |
| real_world_media_master | REQUIRED both |
| training_pairs, group_examples, split_manifest | REQUIRED Phase 1 |
| feature_manifest (+features) | REQUIRED both |
| evidence_ledger, transformation_run_log, download_access_attempt_log, duplicate_map, source_registry | REQUIRED both (traceability) |
| platform_observations | REQUIRED Phase 2 (partial data) |
| campaign_candidate_clusters | BLOCKED — not_supported_by_available_evidence |
| experiment_registry | holds only the non-learned dHash sanity baseline BASE-DHASH-v1 (no ORVEX model trained) |