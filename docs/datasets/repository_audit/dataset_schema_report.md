# Dataset-by-Dataset Schema Report

Audit date 2026-10-27. Schemas were read from the actual files (64 structured files/sheets, 1269 columns/fields). Example values of personal fields are masked.

## A. Conventions and consistency
| topic | observed | consequence |
|---|---|---|
| Identifier conventions | ORVEX ids: RW-<source>-..., CV-P<pageid>-Vnn, EV-..., REL-...; native ids retained in native_* columns; native files use their own ids (cascade_id, uuid, video-id, youtube id, pageid) | mixed by design; crosswalk in data/manifests/native_id_crosswalk.csv |
| Timestamp formats | {"real_world_media_master.published_time_utc": {"blank": 251293, "ISO-like without timezone": 881, "ISO-8601 with Z": 96}, "platform_observations.publish_time_utc": {"ISO-8601 with Z": 257422, "blank": 94399, "ISO-like without timezone": 881}, "platform_observations.observation_time_utc": {"blank": 352282, "ISO-like without timezone": 420}} | ORVEX *_utc columns hold three patterns (Commons/tweets with Z; COVID/FVC-derived without timezone; blank); precision recorded in time_precision |
| Boolean encoding | ANAKIN raw: TRUE/FALSE; ORVEX CSVs: True/False; masters store as text | normalise on read |
| Null handling | ORVEX tables use empty strings; raw sources use blank cells; JSON uses null/empty list | documented as null + missingness_note |
| Label vocabularies | FVC native: fake/real/uncertain/debunked/parody; FIVR: ND/DS/CS/IS; ANAKIN manipulation types; ORVEX normalised relation types differ per source; IS not normalised | see findings F-003 (FIVR IS) and F-005 (FVC labels) |
| Units | durations in seconds; VCSL segment units assumed seconds (not verified); bytes decimal | VCSL unit unverified |
| Column naming | ORVEX snake_case; raw files use hyphens/spaces/camel (video-id, Type of Manipulation, InVID_id) | kept verbatim to preserve native fields |

## B. Files and schemas

### `LOOP-MIND_Novelty_Independent_Verification_2_4_5.xlsx#Literature Review`  (DS-037; xlsx)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| Novelty and Theme | str | 0.0 | 3 | Authored | documentation | Unreferenced in project code |
| Paper Title | str | 0.0 | 9 | Authored | documentation | Unreferenced in project code |
| Year | int | 0.0 | 5 | Authored | documentation | Unreferenced in project code |
| Authors | str | 0.0 | 9 | Authored | documentation | Unreferenced in project code |
| Research Objective | str | 0.0 | 9 | Authored | documentation | Unreferenced in project code |
| Detailed Abstract (Paraphrased) | str | 0.0 | 9 | Authored | documentation | Unreferenced in project code |
| Technical Stack / Methods | str | 0.0 | 9 | Authored | documentation | Unreferenced in project code |
| Dataset and Evaluation | str | 0.0 | 9 | Authored | documentation | Unreferenced in project code |
| Main Findings | str | 0.0 | 9 | Authored | documentation | Unreferenced in project code |
| Conclusion | str | 0.0 | 9 | Authored | documentation | Unreferenced in project code |
| Drawbacks / Limitations | str | 0.0 | 9 | Authored | documentation | Unreferenced in project code |
| Similarity to LOOP-MIND | str | 0.0 | 9 | Authored | documentation | Unreferenced in project code |
| How LOOP-MIND Improves the Limitation | str | 0.0 | 9 | Authored | documentation | Unreferenced in project code |
| Research Gap / Contribution Angle | str | 0.0 | 9 | Authored | documentation | Unreferenced in project code |
| Novelty Status | str | 0.0 | 1 | Authored | documentation | Unreferenced in project code |
| Last Verification | str | 0.0 | 2 | Authored | documentation | Unreferenced in project code |
| Verification Evidence | str | 0.0 | 9 | Authored | documentation | Unreferenced in project code |
| What to Tell the Jury | str | 0.0 | 9 | Authored | documentation | Unreferenced in project code |
| Technical Stack / Methods (of my project LOOP-MIND) | str | 0.0 | 9 | Authored | documentation | Unreferenced in project code |
| Dataset and Evaluation (of my project LOOP-MIND) | str | 0.0 | 9 | Authored | documentation | Unreferenced in project code |

### `ORVEX_Literature/ORVEX_Literature_Review_10_1.xlsx#Feasibility`  (DS-035; xlsx)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| Area | str | 0.0 | 12 | Authored | documentation | Unreferenced in project code |
| Rating | str | 0.0 | 6 | Authored | documentation | Unreferenced in project code |
| Assessment | str | 0.0 | 12 | Authored | documentation | Unreferenced in project code |
| Evidence from literature / machine | str | 8.33 | 11 | Authored | documentation | Unreferenced in project code |
| Main risk | str | 0.0 | 12 | Authored | documentation | Unreferenced in project code |
| Mitigation / decision | str | 0.0 | 12 | Authored | documentation | Unreferenced in project code |

### `ORVEX_Literature/ORVEX_Literature_Review_10_1.xlsx#Literature Review`  (DS-035; xlsx)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| Novelty and Theme | str | 0.0 | 8 | Authored | documentation | Unreferenced in project code |
| Paper Title | str | 0.0 | 32 | Authored | documentation | Unreferenced in project code |
| Year | int | 0.0 | 10 | Authored | documentation | Unreferenced in project code |
| Authors | str | 0.0 | 31 | Authored | documentation | Unreferenced in project code |
| Research Objective | str | 0.0 | 32 | Authored | documentation | Unreferenced in project code |
| Detailed Abstract (Paraphrased) | str | 0.0 | 32 | Authored | documentation | Unreferenced in project code |
| Technical Stack / Methods | str | 0.0 | 32 | Authored | documentation | Unreferenced in project code |
| Dataset and Evaluation | str | 0.0 | 32 | Authored | documentation | Unreferenced in project code |
| Main Findings | str | 0.0 | 32 | Authored | documentation | Unreferenced in project code |
| Conclusion | str | 0.0 | 32 | Authored | documentation | Unreferenced in project code |
| Drawbacks / Limitations | str | 0.0 | 32 | Authored | documentation | Unreferenced in project code |
| Similarity to ORVEX | str | 0.0 | 32 | Authored | documentation | Unreferenced in project code |
| How ORVEX Improves the Limitation | str | 0.0 | 32 | Authored | documentation | Unreferenced in project code |
| Research Gap / Contribution Angle | str | 0.0 | 32 | Authored | documentation | Unreferenced in project code |
| Novelty Status | str | 0.0 | 4 | Authored | documentation | Unreferenced in project code |
| Last Verification | str | 0.0 | 1 | Authored | documentation | Unreferenced in project code |
| Verification Evidence | str | 0.0 | 23 | Authored | documentation | Unreferenced in project code |
| What to Tell the Jury | str | 0.0 | 32 | Authored | documentation | Unreferenced in project code |
| Technical Stack / Methods (of my project ORVEX) | str | 0.0 | 8 | Authored | documentation | Unreferenced in project code |
| Dataset and Evaluation (of my project ORVEX) | str | 0.0 | 8 | Authored | documentation | Unreferenced in project code |

### `ORVEX_Literature/ORVEX_Literature_Review_10_1.xlsx#Novelty Verdict`  (DS-035; xlsx)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| ORVEX claim (spec §) | str | 0.0 | 7 | Authored | documentation | Unreferenced in project code |
| Closest prior work in this review | str | 0.0 | 7 | Authored | documentation | Unreferenced in project code |
| What already exists | str | 0.0 | 7 | Authored | documentation | Unreferenced in project code |
| What was NOT found in this review | str | 0.0 | 7 | Authored | documentation | Unreferenced in project code |
| Verdict | str | 0.0 | 7 | Authored | documentation | Unreferenced in project code |
| Safe wording for report / jury | str | 0.0 | 7 | Authored | documentation | Unreferenced in project code |
| Evidence needed from experiments | str | 0.0 | 7 | Authored | documentation | Unreferenced in project code |

### `ORVEX_Literature/ORVEX_Literature_Review_10_1.xlsx#Open Items`  (DS-035; xlsx)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| # | int | 0.0 | 9 | Authored | documentation | Unreferenced in project code |
| Item | str | 0.0 | 9 | Authored | documentation | Unreferenced in project code |
| Why / suggested next step | str | 0.0 | 9 | Authored | documentation | Unreferenced in project code |

### `ORVEX_Literature/ORVEX_Literature_Review_10_1.xlsx#Paper Register`  (DS-035; xlsx)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| # | int | 0.0 | 32 | Authored | documentation | Unreferenced in project code |
| Theme | str | 0.0 | 8 | Authored | documentation | Unreferenced in project code |
| Paper | str | 0.0 | 32 | Authored | documentation | Unreferenced in project code |
| Year | int | 0.0 | 10 | Authored | documentation | Unreferenced in project code |
| Venue / source | str | 0.0 | 32 | Authored | documentation | Unreferenced in project code |
| Link | str | 0.0 | 32 | Authored | documentation | Used by downstream code |
| Local file | str | 0.0 | 32 | Authored | documentation | Unreferenced in project code |
| Access | str | 0.0 | 2 | Authored | documentation | Unreferenced in project code |
| Verification level | str | 0.0 | 1 | Authored | documentation | Unreferenced in project code |

### `ORVEX_Literature/ORVEX_Literature_Review_10_1.xlsx#Research Summary`  (DS-035; xlsx)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| Topic | str | 0.0 | 9 | Authored | documentation | Unreferenced in project code |
| Summary | str | 0.0 | 9 | Authored | documentation | Unreferenced in project code |

### `ORVEX_Literature/ORVEX_Literature_Review_10_1.xlsx#Search Log`  (DS-035; xlsx)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| # | int | 0.0 | 14 | Authored | documentation | Unreferenced in project code |
| Query / method | str | 0.0 | 14 | Authored | documentation | Unreferenced in project code |
| Source | str | 0.0 | 3 | Authored | documentation | Unreferenced in project code |
| Outcome | str | 0.0 | 14 | Authored | documentation | Unreferenced in project code |

### `data/derived/features/audio_fingerprint.jsonl`  (DS-022; 1727 rows)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| $ | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.media_id | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.audio_md5_8k | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.audio_env_1s | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |

### `data/derived/features/visual_dhash24.jsonl`  (DS-021; 1727 rows)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| $ | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.media_id | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.dhash24 | list | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.dhash24[] | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.frame_indices | list | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.frame_indices[] | int | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |

### `data/derived/splits/split_manifest.csv`  (DS-025; 305 rows)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| split_version | str | 0.0 | 1 | added by ORVEX | metadata | Used by downstream code |
| source_family_id | str | 0.0 | 305 | added by ORVEX | metadata | Referenced by audit/docs/tests only |
| source_dataset_id | str | 0.0 | 2 | added by ORVEX | metadata | Used by downstream code |
| split | str | 0.0 | 3 | added by ORVEX | derived metadata/feature | Used by downstream code |
| assignment_method | str | 0.0 | 1 | added by ORVEX | metadata | Used by downstream code |
| seed | str | 0.0 | 1 | added by ORVEX | metadata | Used by downstream code |
| domain_stratum | str | 0.0 | 26 | added by ORVEX | metadata | Referenced by audit/docs/tests only |
| n_family_items | int | 0.0 | 4 | added by ORVEX | derived metadata/feature | Referenced by audit/docs/tests only |
| n_native_edges | int | 0.0 | 2 | added by ORVEX | derived metadata/feature | Referenced by audit/docs/tests only |
| heldout_transformations_in_family | str | 81.97 | 2 | added by ORVEX | derived metadata/feature | Referenced by audit/docs/tests only |

### `data/derived/tables/campaign_candidate_clusters.csv`  (DS-029; 0 rows)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| cluster_id | empty | 0.0 | 0 | added by ORVEX | metadata | Referenced by audit/docs/tests only |
| observation_ids | empty | 0.0 | 0 | added by ORVEX | metadata | Referenced by audit/docs/tests only |
| media_ids | empty | 0.0 | 0 | added by ORVEX | metadata | Referenced by audit/docs/tests only |
| account_pseudonyms | empty | 0.0 | 0 | added by ORVEX | derived metadata/feature | Referenced by audit/docs/tests only |
| time_window_start_utc | empty | 0.0 | 0 | added by ORVEX | metadata | Referenced by audit/docs/tests only |
| time_window_end_utc | empty | 0.0 | 0 | added by ORVEX | metadata | Referenced by audit/docs/tests only |
| common_media_signals | empty | 0.0 | 0 | added by ORVEX | metadata | Referenced by audit/docs/tests only |
| posting_pattern_signals | empty | 0.0 | 0 | added by ORVEX | metadata | Referenced by audit/docs/tests only |
| independent_coordination_evidence | empty | 0.0 | 0 | added by ORVEX | metadata | Referenced by audit/docs/tests only |
| candidate_status | empty | 0.0 | 0 | added by ORVEX | metadata | Referenced by audit/docs/tests only |
| reviewer | empty | 0.0 | 0 | added by ORVEX | derived metadata/feature | Referenced by audit/docs/tests only |
| limitations | empty | 0.0 | 0 | added by ORVEX | metadata | Used by downstream code |

### `data/derived/tables/controlled_variant_registry.csv`  (DS-014; 1133 rows)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| variant_media_id | str | 0.0 | 1133 | added by ORVEX | metadata | Used by downstream code |
| direct_parent_media_id | str | 0.0 | 385 | added by ORVEX | ground truth (controlled lineage) | Used by downstream code |
| root_source_media_id | str | 0.0 | 55 | added by ORVEX | ground truth (controlled lineage) | Used by downstream code |
| ancestor_chain | str | 0.0 | 385 | added by ORVEX | ground truth (controlled lineage) | Referenced by audit/docs/tests only |
| video_source_media_id | str | 0.0 | 55 | added by ORVEX | metadata | Referenced by audit/docs/tests only |
| audio_source_media_id | str | 91.26 | 33 | added by ORVEX | metadata | Used by downstream code |
| caption_text_source_media_id | str | 90.29 | 30 | added by ORVEX | metadata | Used by downstream code |
| caption_text | str | 90.29 | 30 | original source field | metadata | Used by downstream code |
| caption_text_origin_field | str | 90.29 | 1 | added by ORVEX | metadata | Referenced by audit/docs/tests only |
| transformation_id | str | 0.0 | 14 | added by ORVEX | ground truth (controlled lineage) | Used by downstream code |
| transformation_name | str | 0.0 | 14 | added by ORVEX | ground truth (controlled lineage) | Used by downstream code |
| transformation_family | str | 0.0 | 6 | added by ORVEX | metadata | Referenced by audit/docs/tests only |
| parameters_json | json-in-string | 0.0 | 260 | added by ORVEX | ground truth (controlled lineage) | Used by downstream code |
| tool_name | str | 0.0 | 1 | added by ORVEX | metadata | Used by downstream code |
| tool_version | str | 0.0 | 1 | added by ORVEX | derived metadata/feature | Used by downstream code |
| run_id | str | 0.0 | 1133 | added by ORVEX | metadata | Used by downstream code |
| seed | str | 0.0 | 55 | added by ORVEX | metadata | Used by downstream code |
| created_utc | datetime | 0.0 | 1008 | added by ORVEX | metadata | Used by downstream code |
| local_path | str | 0.18 | 1131 | added by ORVEX | metadata | Used by downstream code |
| sha256 | str | 0.18 | 1131 | added by ORVEX | derived metadata/feature | Used by downstream code |
| bytes | int | 0.0 | 1132 | added by ORVEX | derived metadata/feature | Used by downstream code |
| duration_s | float | 0.0 | 380 | added by ORVEX | derived metadata/feature | Used by downstream code |
| width | int | 0.0 | 25 | added by ORVEX | derived metadata/feature | Used by downstream code |
| height | int | 0.0 | 23 | added by ORVEX | derived metadata/feature | Used by downstream code |
| fps | float | 0.0 | 49 | added by ORVEX | derived metadata/feature | Used by downstream code |
| has_audio | bool | 0.0 | 2 | added by ORVEX | derived metadata/feature | Used by downstream code |
| generation_depth | int | 0.0 | 3 | added by ORVEX | derived metadata/feature | Used by downstream code |
| chain_id | str | 66.02 | 5 | added by ORVEX | metadata | Used by downstream code |
| permission_basis | str | 0.0 | 41 | added by ORVEX | derived metadata/feature | Referenced by audit/docs/tests only |
| root_license | str | 0.0 | 7 | original source field | metadata | Referenced by audit/docs/tests only |
| validation_status | str | 0.0 | 2 | added by ORVEX | derived metadata/feature | Used by downstream code |
| validation_checks_json | json-in-string | 0.0 | 1051 | added by ORVEX | derived metadata/feature | Referenced by audit/docs/tests only |
| failure_reason | str | 99.82 | 1 | added by ORVEX | metadata | Referenced by audit/docs/tests only |
| media_origin | str | 0.0 | 1 | added by ORVEX | metadata | Used by downstream code |
| record_origin | str | 0.0 | 1 | added by ORVEX | metadata | Used by downstream code |
| transformation_status | str | 0.0 | 2 | added by ORVEX | metadata | Referenced by audit/docs/tests only |
| usable_for_training | bool | 0.0 | 2 | added by ORVEX | derived metadata/feature | Used by downstream code |
| source_split | str | 0.0 | 3 | added by ORVEX | derived metadata/feature | Used by downstream code |

### `data/derived/tables/duplicate_map.csv`  (DS-026; 378 rows)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| duplicate_id | str | 0.0 | 378 | added by ORVEX | metadata | Referenced by audit/docs/tests only |
| canonical_media_id | str | 0.0 | 313 | added by ORVEX | metadata | Used by downstream code |
| duplicate_media_id | str | 0.0 | 378 | added by ORVEX | metadata | Used by downstream code |
| duplicate_type | str | 0.0 | 4 | added by ORVEX | derived metadata/feature | Used by downstream code |
| evidence | str | 0.0 | 312 | added by ORVEX | derived metadata/feature | Used by downstream code |
| resolution | str | 0.0 | 4 | added by ORVEX | metadata | Referenced by audit/docs/tests only |

### `data/derived/tables/evidence_ledger.csv`  (DS-019; 1237 rows)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| evidence_id | str | 0.0 | 1237 | added by ORVEX | metadata | Used by downstream code |
| evidence_type | str | 0.0 | 5 | added by ORVEX | metadata | Used by downstream code |
| source_dataset_id | str | 0.0 | 9 | added by ORVEX | metadata | Used by downstream code |
| subject_type | str | 0.0 | 3 | added by ORVEX | metadata | Used by downstream code |
| subject_id | str | 0.0 | 1237 | added by ORVEX | metadata | Used by downstream code |
| source_url | str | 91.67 | 103 | original source field | metadata | Used by downstream code |
| source_record_ref | str | 0.0 | 1236 | added by ORVEX | metadata | Used by downstream code |
| claim_supported | str | 0.0 | 1149 | added by ORVEX | metadata | Used by downstream code |
| claim_status | str | 0.0 | 3 | added by ORVEX | metadata | Used by downstream code |
| observed_fact_vs_inference | str | 0.0 | 3 | added by ORVEX | metadata | Used by downstream code |
| verification_method | str | 0.0 | 8 | added by ORVEX | metadata | Used by downstream code |
| evidence_time_utc | datetime | 0.0 | 1010 | added by ORVEX | metadata | Used by downstream code |
| temporal_precision | str | 0.0 | 2 | added by ORVEX | metadata | Used by downstream code |
| file_sha256 | str | 0.24 | 1234 | added by ORVEX | derived metadata/feature | Used by downstream code |
| reviewer_status | str | 0.0 | 2 | added by ORVEX | metadata | Used by downstream code |
| permission_status | str | 0.0 | 7 | added by ORVEX | derived metadata/feature | Used by downstream code |
| confidence_basis | str | 0.0 | 3 | added by ORVEX | metadata | Used by downstream code |
| limitations | str | 8.33 | 2 | added by ORVEX | metadata | Used by downstream code |

### `data/derived/tables/experiment_registry.csv`  (DS-030; 8 rows)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| experiment_id | str | 0.0 | 8 | added by ORVEX | computed metric (non-learned baseline) | Referenced by audit/docs/tests only |
| dataset_versions | str | 0.0 | 1 | added by ORVEX | computed metric (non-learned baseline) | Referenced by audit/docs/tests only |
| split_version | str | 0.0 | 1 | added by ORVEX | computed metric (non-learned baseline) | Used by downstream code |
| label_map_version | str | 0.0 | 1 | added by ORVEX | computed metric (non-learned baseline) | Referenced by audit/docs/tests only |
| model_version | str | 0.0 | 1 | added by ORVEX | computed metric (non-learned baseline) | Referenced by audit/docs/tests only |
| feature_version | str | 0.0 | 1 | added by ORVEX | computed metric (non-learned baseline) | Referenced by audit/docs/tests only |
| metric_name | str | 0.0 | 8 | added by ORVEX | computed metric (non-learned baseline) | Referenced by audit/docs/tests only |
| metric_value | float | 0.0 | 7 | added by ORVEX | computed metric (non-learned baseline) | Referenced by audit/docs/tests only |
| protocol | str | 0.0 | 8 | added by ORVEX | computed metric (non-learned baseline) | Referenced by audit/docs/tests only |
| heldout_policy | str | 0.0 | 1 | added by ORVEX | computed metric (non-learned baseline) | Referenced by audit/docs/tests only |
| report_path | str | 0.0 | 1 | added by ORVEX | computed metric (non-learned baseline) | Referenced by audit/docs/tests only |
| leakage_test_result | str | 0.0 | 1 | added by ORVEX | computed metric (non-learned baseline) | Referenced by audit/docs/tests only |

### `data/derived/tables/feature_manifest.csv`  (DS-020; 5187 rows)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| feature_record_id | str | 0.0 | 5187 | added by ORVEX | feature (computed) / feature index | Referenced by audit/docs/tests only |
| media_id | str | 0.0 | 1728 | added by ORVEX | feature (computed) / feature index | Used by downstream code |
| feature_type | str | 0.0 | 9 | added by ORVEX | feature (computed) / feature index | Used by downstream code |
| extraction_status | str | 0.0 | 2 | added by ORVEX | feature (computed) / feature index | Used by downstream code |
| tool_name | str | 0.12 | 1 | added by ORVEX | feature (computed) / feature index | Used by downstream code |
| tool_version | str | 0.12 | 1 | added by ORVEX | feature (computed) / feature index | Used by downstream code |
| parameters_json | json-in-string | 0.12 | 1 | added by ORVEX | feature (computed) / feature index | Used by downstream code |
| sample_timestamps | str | 66.72 | 415 | added by ORVEX | feature (computed) / feature index | Referenced by audit/docs/tests only |
| feature_format | str | 0.12 | 3 | added by ORVEX | feature (computed) / feature index | Referenced by audit/docs/tests only |
| storage_path | str | 0.12 | 2 | added by ORVEX | feature (computed) / feature index | Referenced by audit/docs/tests only |
| storage_bytes | int | 10.16 | 83 | added by ORVEX | feature (computed) / feature index | Used by downstream code |
| feature_sha256 | str | 10.16 | 3637 | added by ORVEX | feature (computed) / feature index | Used by downstream code |
| extracted_utc | datetime | 0.12 | 1 | added by ORVEX | feature (computed) / feature index | Referenced by audit/docs/tests only |
| error | str | 89.84 | 3 | added by ORVEX | feature (computed) / feature index | Used by downstream code |
| permission_status | str | 0.0 | 1 | added by ORVEX | feature (computed) / feature index | Used by downstream code |

### `data/derived/tables/group_examples.csv`  (DS-024; 110 rows)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| group_id | str | 0.0 | 110 | added by ORVEX | metadata | Referenced by audit/docs/tests only |
| source_family_id | str | 0.0 | 55 | added by ORVEX | derived metadata/feature | Referenced by audit/docs/tests only |
| member_media_ids | str | 0.0 | 110 | added by ORVEX | metadata | Referenced by audit/docs/tests only |
| n_members | int | 0.0 | 1 | added by ORVEX | derived metadata/feature | Referenced by audit/docs/tests only |
| family_member_ids | str | 0.0 | 110 | added by ORVEX | metadata | Referenced by audit/docs/tests only |
| distractor_ids | str | 0.0 | 110 | added by ORVEX | metadata | Referenced by audit/docs/tests only |
| truth_edges | str | 58.18 | 46 | added by ORVEX | derived metadata/feature | Referenced by audit/docs/tests only |
| n_truth_edges | int | 0.0 | 4 | added by ORVEX | derived metadata/feature | Referenced by audit/docs/tests only |
| split | str | 0.0 | 3 | added by ORVEX | derived metadata/feature | Used by downstream code |
| split_version | str | 0.0 | 1 | added by ORVEX | metadata | Used by downstream code |
| label_origin | str | 0.0 | 1 | added by ORVEX | metadata | Referenced by audit/docs/tests only |
| evidence_id | str | 0.0 | 1 | added by ORVEX | metadata | Used by downstream code |
| created_utc | datetime | 0.0 | 1 | added by ORVEX | metadata | Used by downstream code |

### `data/derived/tables/media_relationship_edges.csv`  (DS-017; 299875 rows)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| relationship_id | str | 0.0 | 299875 | added by ORVEX | metadata | Used by downstream code |
| source_dataset_id | str | 0.0 | 5 | added by ORVEX | metadata | Used by downstream code |
| relation_scope | str | 0.0 | 2 | added by ORVEX | metadata | Used by downstream code |
| evidence_id | str | 0.0 | 1135 | added by ORVEX | metadata | Used by downstream code |
| media_a_id | str | 0.0 | 7320 | added by ORVEX | metadata | Used by downstream code |
| media_b_id | str | 0.0 | 25220 | added by ORVEX | metadata | Used by downstream code |
| native_media_a_id | str | 0.41 | 5961 | original source field | source annotation (ground truth as publi | Referenced by audit/docs/tests only |
| native_media_b_id | str | 0.41 | 23108 | original source field | source annotation (ground truth as publi | Referenced by audit/docs/tests only |
| native_label | str | 0.41 | 16 | original source field | source annotation (ground truth as publi | Used by downstream code |
| normalized_relation_type | str | 0.0 | 19 | added by ORVEX | ground truth label (source or controlled | Used by downstream code |
| direction_status | str | 0.0 | 4 | added by ORVEX | ground truth label (source or controlled | Used by downstream code |
| parent_media_id | str | 98.92 | 2382 | added by ORVEX | ground truth label (source or controlled | Used by downstream code |
| child_media_id | str | 98.92 | 3128 | added by ORVEX | ground truth label (source or controlled | Used by downstream code |
| a_segment_start_s | int | 6.67 | 1880 | original source field | metadata | Referenced by audit/docs/tests only |
| a_segment_end_s | int | 6.67 | 1597 | original source field | metadata | Referenced by audit/docs/tests only |
| b_segment_start_s | int | 7.0 | 2170 | original source field | metadata | Referenced by audit/docs/tests only |
| b_segment_end_s | int | 7.0 | 1878 | original source field | metadata | Referenced by audit/docs/tests only |
| overlap_ratio | empty | 100.0 | 0 | added by ORVEX | derived metadata/feature | Referenced by audit/docs/tests only |
| transformation_type | str | 5.92 | 21 | added by ORVEX | metadata | Used by downstream code |
| label_source | str | 0.0 | 2 | added by ORVEX | metadata | Used by downstream code |
| label_status | str | 0.0 | 2 | added by ORVEX | ground truth label (source or controlled | Used by downstream code |
| evidence_status | str | 0.0 | 2 | added by ORVEX | ground truth label (source or controlled | Used by downstream code |
| confidence_status | str | 0.0 | 2 | added by ORVEX | metadata | Used by downstream code |
| reviewer | empty | 100.0 | 0 | added by ORVEX | derived metadata/feature | Referenced by audit/docs/tests only |
| method_version | str | 0.0 | 2 | added by ORVEX | metadata | Used by downstream code |
| created_utc | datetime | 0.0 | 1008 | added by ORVEX | metadata | Used by downstream code |
| media_available_locally | bool | 0.0 | 2 | added by ORVEX | derived metadata/feature | Used by downstream code |
| conflict_flag | bool | 0.0 | 1 | added by ORVEX | derived metadata/feature | Used by downstream code |
| notes | str | 0.0 | 924 | added by ORVEX | metadata | Used by downstream code |

### `data/derived/tables/platform_observations.csv`  (DS-018; 352702 rows)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| observation_id | str | 0.0 | 352308 | added by ORVEX | metadata | Used by downstream code |
| media_id | str | 0.0 | 13797 | added by ORVEX | metadata | Used by downstream code |
| observation_type | str | 0.0 | 5 | added by ORVEX | metadata | Used by downstream code |
| coordination_status | str | 0.0 | 1 | added by ORVEX | normalised label / policy status (not mo | Used by downstream code |
| platform | str | 0.0 | 4 | original source field | metadata | Used by downstream code |
| platform_post_id | str | 0.0 | 350932 | added by ORVEX | derived metadata/feature | Used by downstream code |
| post_url | str | 23.01 | 269923 | original source field | metadata | Used by downstream code |
| account_id_pseudonym | str | 99.71 | 791 | added by ORVEX | derived metadata/feature | Referenced by audit/docs/tests only |
| account_id_source_field | str | 99.71 | 2 | added by ORVEX | metadata | Referenced by audit/docs/tests only |
| publish_time_utc | datetime | 26.76 | 249753 | original source field | metadata | Used by downstream code |
| observation_time_utc | datetime | 99.88 | 420 | added by ORVEX | metadata | Referenced by audit/docs/tests only |
| time_precision | str | 0.0 | 4 | added by ORVEX | metadata | Used by downstream code |
| caption_text | str | 99.97 | 91 | original source field | metadata | Used by downstream code |
| hashtags | empty | 100.0 | 0 | added by ORVEX | metadata | Referenced by audit/docs/tests only |
| engagement_refs | str | 97.67 | 7763 | original source field | metadata | Referenced by audit/docs/tests only |
| metadata_source | str | 0.0 | 3 | added by ORVEX | metadata | Referenced by audit/docs/tests only |
| collection_method | str | 0.0 | 2 | added by ORVEX | metadata | Referenced by audit/docs/tests only |
| order_in_cascade | int | 98.42 | 224 | added by ORVEX | derived metadata/feature | Referenced by audit/docs/tests only |
| cascade_id | str | 98.42 | 380 | original source field | metadata | Referenced by audit/docs/tests only |
| access_status | str | 0.0 | 2 | added by ORVEX | metadata | Used by downstream code |
| evidence_id | str | 0.0 | 98 | added by ORVEX | metadata | Used by downstream code |
| limitations | str | 0.0 | 7 | added by ORVEX | metadata | Used by downstream code |

### `data/derived/tables/real_world_media_master.csv`  (DS-016; 252270 rows)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| media_id | str | 0.0 | 252270 | added by ORVEX | metadata | Used by downstream code |
| source_dataset_id | str | 0.0 | 8 | added by ORVEX | metadata | Used by downstream code |
| release_version | int | 1.24 | 6 | original source field | metadata | Used by downstream code |
| native_record_id | str | 0.0 | 244997 | original source field | source annotation (ground truth as publi | Used by downstream code |
| native_media_id | str | 0.0 | 252001 | original source field | source annotation (ground truth as publi | Used by downstream code |
| platform | str | 0.0 | 7 | original source field | metadata | Used by downstream code |
| platform_media_id | str | 0.0 | 250856 | added by ORVEX | derived metadata/feature | Used by downstream code |
| source_url | str | 0.0 | 251879 | original source field | metadata | Used by downstream code |
| canonical_url | str | 0.0 | 251879 | added by ORVEX | derived metadata/feature | Used by downstream code |
| title | str | 94.52 | 8367 | original source field | metadata | Used by downstream code |
| description_caption | str | 96.77 | 7671 | original source field | metadata | Referenced by audit/docs/tests only |
| publisher_account_id | str | 99.14 | 888 | original source field | metadata | Referenced by audit/docs/tests only |
| event_or_cascade_id | str | 7.02 | 5742 | original source field | metadata | Referenced by audit/docs/tests only |
| published_time_utc | datetime | 99.61 | 240 | original source field | metadata | Used by downstream code |
| observed_time_utc | empty | 100.0 | 0 | added by ORVEX | metadata | Referenced by audit/docs/tests only |
| collected_time_utc | datetime | 0.0 | 1 | added by ORVEX | metadata | Used by downstream code |
| time_precision | str | 0.0 | 3 | added by ORVEX | metadata | Used by downstream code |
| duration_s | float | 99.76 | 200 | added by ORVEX | derived metadata/feature | Used by downstream code |
| width | int | 99.76 | 28 | added by ORVEX | derived metadata/feature | Used by downstream code |
| height | int | 99.76 | 29 | added by ORVEX | derived metadata/feature | Used by downstream code |
| fps | float | 99.76 | 26 | added by ORVEX | derived metadata/feature | Used by downstream code |
| video_codec | str | 99.76 | 5 | added by ORVEX | derived metadata/feature | Used by downstream code |
| audio_codec | str | 99.78 | 4 | added by ORVEX | derived metadata/feature | Used by downstream code |
| has_audio | bool | 99.76 | 2 | added by ORVEX | derived metadata/feature | Used by downstream code |
| container | str | 99.76 | 3 | added by ORVEX | derived metadata/feature | Used by downstream code |
| file_bytes | int | 99.76 | 584 | added by ORVEX | derived metadata/feature | Referenced by audit/docs/tests only |
| local_path | str | 99.76 | 596 | added by ORVEX | metadata | Used by downstream code |
| sha256 | str | 99.76 | 596 | added by ORVEX | derived metadata/feature | Used by downstream code |
| access_status | str | 0.0 | 2 | added by ORVEX | metadata | Used by downstream code |
| playable_status | str | 0.0 | 3 | added by ORVEX | derived metadata/feature | Used by downstream code |
| rights_status | str | 0.0 | 5 | added by ORVEX | derived metadata/feature | Referenced by audit/docs/tests only |
| license | str | 0.39 | 13 | original source field | metadata | Used by downstream code |
| license_url | str | 4.05 | 9 | original source field | metadata | Used by downstream code |
| attribution | str | 0.39 | 92 | original source field | metadata | Referenced by audit/docs/tests only |
| record_origin | str | 0.0 | 1 | added by ORVEX | metadata | Used by downstream code |
| media_origin | str | 0.0 | 3 | added by ORVEX | metadata | Used by downstream code |
| native_authenticity_label | str | 97.68 | 5 | original source field | source annotation (ground truth as publi | Used by downstream code |
| native_misleading_label | str | 94.46 | 6 | original source field | source annotation (ground truth as publi | Referenced by audit/docs/tests only |
| native_manipulation_type | str | 99.58 | 8 | original source field | source annotation (ground truth as publi | Used by downstream code |
| normalized_authenticity_status | str | 0.0 | 3 | added by ORVEX | normalised label / policy status (not mo | Referenced by audit/docs/tests only |
| normalized_misleading_status | str | 0.0 | 4 | added by ORVEX | normalised label / policy status (not mo | Used by downstream code |
| coordination_status | str | 0.0 | 1 | added by ORVEX | normalised label / policy status (not mo | Used by downstream code |
| evidence_id | str | 0.0 | 103 | added by ORVEX | metadata | Used by downstream code |
| perceptual_hash_ref | str | 99.76 | 1 | added by ORVEX | derived metadata/feature | Used by downstream code |
| annotation_status | str | 0.0 | 2 | added by ORVEX | metadata | Used by downstream code |
| qc_flags | str | 99.98 | 11 | added by ORVEX | derived metadata/feature | Used by downstream code |
| duplicate_of_media_id | str | 99.9 | 207 | added by ORVEX | derived metadata/feature | Used by downstream code |
| usable_for_variants | bool | 0.0 | 2 | added by ORVEX | derived metadata/feature | Used by downstream code |
| missingness_note | str | 0.0 | 9 | added by ORVEX | metadata | Used by downstream code |

### `data/derived/tables/training_pairs.csv`  (DS-023; 13659 rows)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| example_id | str | 0.0 | 13659 | added by ORVEX | metadata | Referenced by audit/docs/tests only |
| media_a_id | str | 0.0 | 1645 | added by ORVEX | metadata | Used by downstream code |
| media_b_id | str | 0.0 | 1635 | added by ORVEX | metadata | Used by downstream code |
| relationship_id | str | 91.72 | 1131 | added by ORVEX | metadata | Used by downstream code |
| label_binary_related | int | 0.0 | 2 | added by ORVEX | ground truth (controlled lineage / sourc | Used by downstream code |
| relationship_class | str | 0.0 | 7 | added by ORVEX | ground truth (controlled lineage / sourc | Used by downstream code |
| native_label | str | 98.17 | 5 | original source field | source annotation (ground truth as publi | Used by downstream code |
| normalized_label | str | 0.0 | 7 | added by ORVEX | ground truth (controlled lineage / sourc | Referenced by audit/docs/tests only |
| label_origin | str | 0.0 | 3 | added by ORVEX | metadata | Referenced by audit/docs/tests only |
| label_status | str | 0.0 | 3 | added by ORVEX | metadata | Used by downstream code |
| evidence_id | str | 0.0 | 1133 | added by ORVEX | metadata | Used by downstream code |
| feature_refs | str | 0.0 | 1 | added by ORVEX | metadata | Referenced by audit/docs/tests only |
| source_family_id | str | 0.0 | 305 | added by ORVEX | derived metadata/feature | Referenced by audit/docs/tests only |
| event_or_cascade_group_id | str | 94.51 | 250 | original source field | metadata | Referenced by audit/docs/tests only |
| split | str | 0.0 | 4 | added by ORVEX | derived metadata/feature | Used by downstream code |
| split_version | str | 0.0 | 1 | added by ORVEX | metadata | Used by downstream code |
| sampling_method | str | 0.0 | 2 | added by ORVEX | metadata | Referenced by audit/docs/tests only |
| negative_rationale | str | 91.24 | 4 | added by ORVEX | metadata | Referenced by audit/docs/tests only |
| hardness | str | 0.0 | 3 | added by ORVEX | derived metadata/feature | Used by downstream code |
| leakage_flag | bool | 0.0 | 1 | added by ORVEX | derived metadata/feature | Referenced by audit/docs/tests only |
| exclusion_reason | str | 72.68 | 2 | added by ORVEX | metadata | Referenced by audit/docs/tests only |
| includes_heldout_transform | bool | 0.0 | 2 | added by ORVEX | derived metadata/feature | Used by downstream code |
| created_utc | datetime | 0.0 | 1 | added by ORVEX | metadata | Used by downstream code |

### `data/derived/tables/transformation_run_log.csv`  (DS-015; 1133 rows)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| run_id | str | 0.0 | 1133 | added by ORVEX | metadata | Used by downstream code |
| variant_media_id | str | 0.0 | 1133 | added by ORVEX | metadata | Used by downstream code |
| input_media_ids | str | 0.0 | 440 | added by ORVEX | metadata | Referenced by audit/docs/tests only |
| tool_name | str | 0.0 | 1 | added by ORVEX | metadata | Used by downstream code |
| tool_version | str | 0.0 | 1 | added by ORVEX | derived metadata/feature | Used by downstream code |
| command_config | str | 0.0 | 1133 | added by ORVEX | metadata | Referenced by audit/docs/tests only |
| parameters_json | json-in-string | 0.0 | 260 | added by ORVEX | metadata | Used by downstream code |
| started_utc | datetime | 0.0 | 1008 | added by ORVEX | metadata | Referenced by audit/docs/tests only |
| return_code | int | 0.0 | 1 | added by ORVEX | derived metadata/feature | Referenced by audit/docs/tests only |
| output_validation_status | str | 0.0 | 2 | added by ORVEX | derived metadata/feature | Referenced by audit/docs/tests only |
| output_bytes | int | 0.0 | 1133 | added by ORVEX | derived metadata/feature | Referenced by audit/docs/tests only |
| storage_delta_bytes | int | 0.0 | 1133 | added by ORVEX | derived metadata/feature | Referenced by audit/docs/tests only |
| error | empty | 100.0 | 0 | added by ORVEX | metadata | Used by downstream code |
| deterministic_notes | str | 0.0 | 1 | added by ORVEX | metadata | Referenced by audit/docs/tests only |
| seed | str | 0.0 | 55 | added by ORVEX | metadata | Used by downstream code |

### `data/manifests/_build/access_log.jsonl`  (DS-032; 712 rows)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| $ | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.attempt_time_utc | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.method | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.retry_count | int | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.terms_decision | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.source_dataset_id | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.media_or_file_id | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.url | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.http_status | int | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.result_category | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.bytes | int | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.sha256 | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.final_status | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.note | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |

### `data/manifests/_build/eligible_titles.txt`  (DS-032; 59 rows)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| eligible_titles.txt | str | 0 | 59 | see file | metadata | Unreferenced in project code |

### `data/manifests/_build/variants/*.json`  (DS-032; json-group)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| $ | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.recs | list | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.recs[] | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.recs[].<key> | str/int/float/bool | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.logs | list | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.logs[] | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.logs[].run_id | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.logs[].variant_media_id | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.logs[].input_media_ids | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.logs[].tool_name | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.logs[].tool_version | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.logs[].command_config | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.logs[].parameters_json | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.logs[].started_utc | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.logs[].return_code | int | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.logs[].output_validation_status | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.logs[].output_bytes | int | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.logs[].storage_delta_bytes | int | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.logs[].error | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.logs[].deterministic_notes | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.logs[].seed | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |

### `data/manifests/attribution.csv`  (DS-031; 96 rows)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| media_id | str | 0.0 | 96 | Unknown | metadata (unverified meaning) | Used by downstream code |
| title | str | 0.0 | 96 | Unknown | metadata (unverified meaning) | Used by downstream code |
| author_or_credit | str | 0.0 | 86 | Unknown | metadata (unverified meaning) | Used by downstream code |
| license | str | 0.0 | 9 | Unknown | metadata (unverified meaning) | Used by downstream code |
| license_url | str | 0.0 | 9 | Unknown | metadata (unverified meaning) | Used by downstream code |
| file_page_url | str | 0.0 | 96 | Unknown | metadata (unverified meaning) | Used by downstream code |
| attribution_required | bool | 0.0 | 2 | Unknown | metadata (unverified meaning) | Used by downstream code |
| used_as_variant_source | bool | 0.0 | 2 | Unknown | metadata (unverified meaning) | Used by downstream code |
| retrieved | datetime | 0.0 | 1 | Unknown | metadata (unverified meaning) | Used by downstream code |

### `data/manifests/checksums.sha256`  (DS-031; 1883 rows)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| checksums.sha256 | str | 0 | 1883 | see file | metadata | Used by downstream code |

### `data/manifests/download_access_attempt_log.csv`  (DS-028; 729 rows)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| attempt_id | str | 0.0 | 729 | added by ORVEX | metadata | Used by downstream code |
| source_dataset_id | str | 0.0 | 8 | added by ORVEX | metadata | Used by downstream code |
| media_or_file_id | str | 0.0 | 729 | added by ORVEX | metadata | Used by downstream code |
| url | str | 0.41 | 726 | added by ORVEX | metadata | Used by downstream code |
| attempt_time_utc | datetime | 0.0 | 587 | added by ORVEX | metadata | Used by downstream code |
| method | str | 0.0 | 3 | added by ORVEX | metadata | Used by downstream code |
| http_status | int | 0.55 | 2 | added by ORVEX | derived metadata/feature | Used by downstream code |
| result_category | str | 0.0 | 3 | added by ORVEX | metadata | Used by downstream code |
| terms_decision | str | 0.0 | 7 | added by ORVEX | metadata | Used by downstream code |
| retry_count | int | 0.0 | 1 | added by ORVEX | metadata | Used by downstream code |
| bytes | int | 0.27 | 713 | added by ORVEX | derived metadata/feature | Used by downstream code |
| sha256 | str | 4.39 | 697 | added by ORVEX | derived metadata/feature | Used by downstream code |
| final_status | str | 0.0 | 4 | added by ORVEX | metadata | Used by downstream code |
| note | str | 97.67 | 5 | added by ORVEX | metadata | Used by downstream code |

### `data/manifests/native_id_crosswalk.csv`  (DS-031; 252270 rows)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| source_dataset_id | str | 0.0 | 8 | Unknown | metadata (unverified meaning) | Used by downstream code |
| release_version | int | 1.24 | 6 | Unknown | metadata (unverified meaning) | Used by downstream code |
| native_record_id | str | 0.0 | 244997 | Unknown | metadata (unverified meaning) | Used by downstream code |
| native_media_id | str | 0.0 | 252001 | Unknown | metadata (unverified meaning) | Used by downstream code |
| platform | str | 0.0 | 7 | Unknown | metadata (unverified meaning) | Used by downstream code |
| platform_media_id | str | 0.0 | 250856 | Unknown | metadata (unverified meaning) | Used by downstream code |
| source_url | str | 0.0 | 251879 | Unknown | metadata (unverified meaning) | Used by downstream code |
| canonical_url | str | 0.0 | 251879 | Unknown | metadata (unverified meaning) | Used by downstream code |
| media_id | str | 0.0 | 252270 | Unknown | metadata (unverified meaning) | Used by downstream code |

### `data/manifests/selection_plan.json`  (DS-031; json)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| $ | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.generated | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.search_date | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.search_terms | list | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.search_terms[] | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.candidates_considered | int | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.commons | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.commons.queries | list | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.commons.queries[] | list | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.commons.queries[][] | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.commons.per_query_max_new_files | int | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.commons.file_size_bytes | list | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.commons.file_size_bytes[] | int | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.commons.licence_gate | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.commons.stem_dedupe | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.commons.qc | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.anakin | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.anakin.rule | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.anakin.selected_pairs | int | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.variants | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.variants.transformations | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.variants.chains | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.variants.donor_and_caption_pick | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.variants.test_only_types | list | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.variants.test_only_types[] | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.splits | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.splits.unit | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.splits.pattern | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.splits.seed | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.splits.version | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.negatives | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.negatives.easy | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.negatives.hard | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.negatives.within | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |

### `data/manifests/source_registry.csv`  (DS-027; 31 rows)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| source_dataset_id | str | 0.0 | 31 | added by ORVEX | metadata | Used by downstream code |
| title | str | 0.0 | 31 | original source field | metadata | Used by downstream code |
| creator | str | 0.0 | 30 | original source field | metadata | Used by downstream code |
| release_version | str | 0.0 | 28 | original source field | metadata | Used by downstream code |
| official_url | str | 3.23 | 30 | original source field | metadata | Used by downstream code |
| download_url | str | 67.74 | 10 | original source field | metadata | Used by downstream code |
| paper_doi_or_url | str | 25.81 | 23 | original source field | metadata | Used by downstream code |
| accessed_date | datetime | 0.0 | 1 | added by ORVEX | metadata | Referenced by audit/docs/tests only |
| license_terms | str | 0.0 | 19 | original source field | metadata | Used by downstream code |
| license_evidence_url | str | 48.39 | 16 | original source field | metadata | Used by downstream code |
| bytes_or_urls_provided | str | 0.0 | 7 | original source field | metadata | Used by downstream code |
| derivative_use_status | str | 0.0 | 10 | added by ORVEX | derived metadata/feature | Used by downstream code |
| training_use_status | str | 0.0 | 10 | added by ORVEX | derived metadata/feature | Used by downstream code |
| redistribution_status | str | 0.0 | 11 | added by ORVEX | derived metadata/feature | Used by downstream code |
| real_world_eligibility | str | 0.0 | 31 | added by ORVEX | derived metadata/feature | Used by downstream code |
| native_task | str | 3.23 | 24 | original source field | source annotation (ground truth as publi | Used by downstream code |
| native_labels | str | 22.58 | 19 | original source field | source annotation (ground truth as publi | Used by downstream code |
| media_origin_characterization | str | 0.0 | 28 | added by ORVEX | derived metadata/feature | Used by downstream code |
| release_size_bytes | int | 70.97 | 9 | original source field | metadata | Used by downstream code |
| planned_download_bytes | int | 0.0 | 8 | added by ORVEX | metadata | Referenced by audit/docs/tests only |
| actual_local_bytes | int | 0.0 | 9 | added by ORVEX | derived metadata/feature | Referenced by audit/docs/tests only |
| record_count_local | int | 0.0 | 9 | added by ORVEX | derived metadata/feature | Referenced by audit/docs/tests only |
| auth_required | str | 0.0 | 8 | original source field | metadata | Used by downstream code |
| overlap_with | str | 64.52 | 11 | added by ORVEX | derived metadata/feature | Used by downstream code |
| inclusion_status | str | 0.0 | 8 | added by ORVEX | metadata | Used by downstream code |
| inclusion_reason | str | 0.0 | 31 | added by ORVEX | derived metadata/feature | Used by downstream code |
| tasks_supported | str | 41.94 | 17 | added by ORVEX | metadata | Used by downstream code |
| evidence_links | str | 0.0 | 31 | added by ORVEX | metadata | Used by downstream code |
| limitations | str | 70.97 | 9 | added by ORVEX | derived metadata/feature | Used by downstream code |
| verification_level | str | 0.0 | 3 | added by ORVEX | metadata | Used by downstream code |

### `data/manifests/storage_budget.csv`  (DS-031; 19 rows)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| kind | str | 0.0 | 4 | Unknown | metadata (unverified meaning) | Used by downstream code |
| name | str | 0.0 | 19 | Unknown | metadata (unverified meaning) | Used by downstream code |
| bytes | int | 0.0 | 18 | Unknown | metadata (unverified meaning) | Used by downstream code |
| GB_decimal | float | 0.0 | 17 | Unknown | metadata (unverified meaning) | Used by downstream code |
| GiB | float | 0.0 | 17 | Unknown | metadata (unverified meaning) | Used by downstream code |
| allocation_bytes | int | 42.11 | 6 | Unknown | metadata (unverified meaning) | Used by downstream code |
| within_allocation | str | 0.0 | 1 | Unknown | metadata (unverified meaning) | Used by downstream code |
| source | str | 0.0 | 7 | Unknown | metadata (unverified meaning) | Used by downstream code |

### `data/real_world/raw_metadata/commons/commons_candidates.json`  (DS-002; json)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| $ | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $[] | dict | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $[].pageid | int | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $[].title | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $[].url | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $[].page_url | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $[].mime | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $[].size | int | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $[].uploaded | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $[].uploader | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $[].upload_comment | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $[].commons_sha1 | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $[].license | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $[].license_url | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $[].author | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $[].credit | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $[].attribution_required | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $[].description | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $[].categories | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $[].categories[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $[].domain | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $[].query | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $[].global_usage_count | int | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $[].media_id | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $[].local_file | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |

### `data/real_world/raw_metadata/covid_misinfo_4557828/covid-misinfo-videos.csv.gz`  (DS-011; 8122 rows)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| youtube_link | str | 0.0 | 8104 | original source field | metadata | Used by downstream code |
| video_title | str | 10.93 | 7120 | original source field | metadata | Used by downstream code |
| video_description | str | 16.36 | 6544 | original source field | metadata | Used by downstream code |
| view_count | int | 88.49 | 914 | original source field | metadata | Used by downstream code |
| channel_id | str | 88.49 | 712 | original source field | metadata | Used by downstream code |
| subscriber_count | int | 89.28 | 614 | original source field | metadata | Unreferenced in project code |
| removal_timestamp | datetime | 94.83 | 420 | original source field | source annotation | Used by downstream code |
| published_timestamp | datetime | 89.15 | 144 | original source field | metadata | Used by downstream code |
| archive_url | str | 88.49 | 934 | original source field | metadata | Unreferenced in project code |
| facebook_graph_reactions | int | 0.0 | 2480 | original source field | metadata (engagement) | Used by downstream code |
| facebook_graph_comments | int | 0.0 | 1822 | original source field | metadata (engagement) | Used by downstream code |
| facebook_graph_shares | int | 0.0 | 2248 | original source field | metadata (engagement) | Used by downstream code |
| twitter_post_ids | json-in-string | 35.79 | 5201 | original source field | metadata (share reference) | Used by downstream code |
| facebook_post_ids | json-in-string | 5.26 | 7678 | original source field | metadata (share reference) | Used by downstream code |

### `data/real_world/raw_metadata/hf_api/anakin.json`  (DS-005; json)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| $ | dict | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $._id | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.id | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.author | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.sha | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.lastModified | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.private | bool | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.gated | bool | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.disabled | bool | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.tags | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.tags[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.citation | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.description | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.downloads | int | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.likes | int | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.cardData | dict | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.cardData.license | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.cardData.task_categories | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.cardData.task_categories[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.cardData.language | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.cardData.language[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.cardData.pretty_name | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.cardData.size_categories | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.cardData.size_categories[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.siblings | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.siblings[] | dict | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.siblings[].rfilename | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.createdAt | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.usedStorage | int | n/a | n/a | Original source field | metadata | Unreferenced in project code |

### `data/real_world/raw_metadata/hf_api/anakin_blobs.json`  (DS-005; json)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| $ | dict | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $._id | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.id | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.author | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.sha | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.lastModified | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.private | bool | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.gated | bool | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.disabled | bool | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.tags | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.tags[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.citation | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.description | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.downloads | int | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.likes | int | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.cardData | dict | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.cardData.license | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.cardData.task_categories | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.cardData.task_categories[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.cardData.language | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.cardData.language[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.cardData.pretty_name | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.cardData.size_categories | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.cardData.size_categories[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.siblings | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.siblings[] | dict | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.siblings[].rfilename | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.siblings[].blobId | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.siblings[].size | int | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.siblings[].lfs | dict | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.siblings[].lfs.sha256 | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.siblings[].lfs.size | int | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.siblings[].lfs.pointerSize | int | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.createdAt | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.usedStorage | int | n/a | n/a | Original source field | metadata | Unreferenced in project code |

### `data/real_world/raw_metadata/hf_api/anakin_metadata.csv`  (DS-005; 1023 rows)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| video-id | str | 0.0 | 1023 | original source field | metadata | Used by downstream code |
| start-time | int | 0.0 | 104 | original source field | source annotation | Used by downstream code |
| end-time | int | 0.0 | 109 | original source field | source annotation | Used by downstream code |
| url | str | 0.0 | 1013 | original source field | metadata | Used by downstream code |
| has-masks | bool | 0.0 | 2 | original source field | metadata | Used by downstream code |
| task | str | 0.0 | 911 | original source field | source annotation | Used by downstream code |
| manipulation-type | str | 0.0 | 5 | original source field | source annotation (ground truth) | Used by downstream code |
| editor-id | str | 0.0 | 10 | original source field | metadata | Used by downstream code |
| full-available | bool | 0.0 | 2 | original source field | metadata | Used by downstream code |

### `data/real_world/raw_metadata/hf_api/anakin_selected_subset.csv`  (DS-005; 250 rows)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| video-id | str | 0.0 | 250 | original source field | metadata | Used by downstream code |
| start-time | int | 0.0 | 60 | original source field | source annotation | Used by downstream code |
| end-time | int | 0.0 | 64 | original source field | source annotation | Used by downstream code |
| url | str | 0.0 | 250 | original source field | metadata | Used by downstream code |
| has-masks | bool | 0.0 | 2 | original source field | metadata | Used by downstream code |
| task | str | 0.0 | 230 | original source field | source annotation | Used by downstream code |
| manipulation-type | str | 0.0 | 5 | original source field | source annotation (ground truth) | Used by downstream code |
| editor-id | str | 0.0 | 10 | original source field | metadata | Used by downstream code |
| full-available | bool | 0.0 | 2 | original source field | metadata | Used by downstream code |

### `data/real_world/raw_metadata/invid_fivr200k/extracted/annotation.json`  (DS-009; json)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| $ | dict | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.<key> | dict | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.<key>.CS | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.<key>.CS[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.<key>.ND | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.<key>.ND[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.<key>.DS | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.<key>.DS[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.<key>.IS | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.<key>.IS[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |

### `data/real_world/raw_metadata/invid_fivr200k/extracted/events.json`  (DS-009; json)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| $ | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $[] | dict | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $[].headline | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $[].text | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $[].text[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $[].youtube | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $[].youtube[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $[].topic | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $[].href | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $[].href[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $[].date | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |

### `data/real_world/raw_metadata/invid_fivr200k/extracted/youtube_ids.txt`  (DS-009; 225960 rows)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| youtube_ids.txt | str | 0 | 225960 | see file | metadata | Used by downstream code |

### `data/real_world/raw_metadata/invid_fvc_2018/extracted/FVC.csv`  (DS-006; 380 rows)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| cascade_id | str | 0.0 | 380 | added by ORVEX | FVC (Zenodo) | Used by downstream code |
| video_url | str | 0.0 | 380 | original source field | metadata | Used by downstream code |
| label | str | 0.0 | 2 | added by ORVEX | FVC (Zenodo) | Used by downstream code |

### `data/real_world/raw_metadata/invid_fvc_2018/extracted/FVC_dup.csv`  (DS-006; 5199 rows)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| cascade_id | str | 0.0 | 322 | added by ORVEX | FVC (Zenodo) | Used by downstream code |
| video_url | str | 0.0 | 5192 | original source field | metadata | Used by downstream code |
| label | str | 0.0 | 5 | added by ORVEX | FVC (Zenodo) | Used by downstream code |

### `data/real_world/raw_metadata/invid_fvc_2018/extracted/FVC_text_queries.csv`  (DS-006; 380 rows)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| cascade_id | str | 0.0 | 380 | added by ORVEX | FVC (Zenodo) | Used by downstream code |
| video_url | str | 0.0 | 380 | original source field | metadata | Used by downstream code |
| label | str | 0.0 | 2 | added by ORVEX | FVC (Zenodo) | Used by downstream code |
| event_title | str | 0.0 | 371 | original source field | source annotation (text query) | Unreferenced in project code |
| french | str | 0.0 | 372 | original source field | source annotation (translation) | Unreferenced in project code |
| spanish | str | 0.0 | 372 | original source field | source annotation (translation) | Unreferenced in project code |
| russian | str | 0.0 | 372 | original source field | source annotation (translation) | Unreferenced in project code |
| arabic | str | 0.26 | 370 | original source field | source annotation (translation) | Unreferenced in project code |
| (unnamed trailing field 9) | str | 83.68 | 60 | Unknown | metadata (unverified meaning) | Unreferenced in project code |
| (unnamed trailing field 10) | str | 92.63 | 28 | Unknown | metadata (unverified meaning) | Unreferenced in project code |
| (unnamed trailing field 11) | str | 92.89 | 27 | Unknown | metadata (unverified meaning) | Unreferenced in project code |
| (unnamed trailing field 12) | str | 93.95 | 23 | Unknown | metadata (unverified meaning) | Unreferenced in project code |
| (unnamed trailing field 13) | str | 98.42 | 6 | Unknown | metadata (unverified meaning) | Unreferenced in project code |
| (unnamed trailing field 14) | str | 98.42 | 6 | Unknown | metadata (unverified meaning) | Unreferenced in project code |
| (unnamed trailing field 15) | str | 98.42 | 6 | Unknown | metadata (unverified meaning) | Unreferenced in project code |
| (unnamed trailing field 16) | str | 98.68 | 5 | Unknown | metadata (unverified meaning) | Unreferenced in project code |
| (unnamed trailing field 17) | str | 99.47 | 2 | Unknown | metadata (unverified meaning) | Unreferenced in project code |
| (unnamed trailing field 18) | str | 99.74 | 1 | Unknown | metadata (unverified meaning) | Unreferenced in project code |
| (unnamed trailing field 19) | str | 99.74 | 1 | Unknown | metadata (unverified meaning) | Unreferenced in project code |
| (unnamed trailing field 20) | str | 99.74 | 1 | Unknown | metadata (unverified meaning) | Unreferenced in project code |
| (unnamed trailing field 21) | str | 99.74 | 1 | Unknown | metadata (unverified meaning) | Unreferenced in project code |

### `data/real_world/raw_metadata/invid_fvc_v1/extracted/Fake Video Corpus/fake_video_corpus.tsv`  (DS-008; 59 rows)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| InVID_id | str | 0.0 | 59 | original source field | metadata | Used by downstream code |
| Link | str | 0.0 | 59 | original source field | metadata | Used by downstream code |
| Title | str | 0.0 | 59 | original source field | metadata | Used by downstream code |
| Comments | str | 0.0 | 47 | original source field | metadata | Used by downstream code |
| Discussed | str | 0.0 | 55 | original source field | source annotation | Unreferenced in project code |
| Appeared | str | 71.19 | 14 | original source field | source annotation | Unreferenced in project code |

### `data/real_world/raw_metadata/invid_fvc_v2/extracted/Fake Video Corpus v2.0/fake-video-corpus - fake-videos.tsv`  (DS-007; 117 rows)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| InVID_id | str | 0.0 | 117 | original source field | metadata | Used by downstream code |
| Link | str | 0.0 | 117 | original source field | metadata | Used by downstream code |
| Title | str | 0.0 | 117 | original source field | metadata | Used by downstream code |
| Type of Manipulation | str | 70.09 | 3 | original source field | source annotation | Used by downstream code |
| Comments | str | 0.85 | 88 | original source field | metadata | Used by downstream code |
| Discussed | str | 11.97 | 86 | original source field | source annotation | Unreferenced in project code |
| Appeared | str | 87.18 | 14 | original source field | source annotation | Unreferenced in project code |
| Timestamp | str | 73.5 | 25 | original source field | source annotation | Unreferenced in project code |

### `data/real_world/raw_metadata/invid_fvc_v2/extracted/Fake Video Corpus v2.0/fake-video-corpus - real-videos.tsv`  (DS-007; 110 rows)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| InVID_id | str | 0.0 | 110 | original source field | metadata | Used by downstream code |
| Link | str | 0.0 | 110 | original source field | metadata | Used by downstream code |
| Title | str | 0.0 | 109 | original source field | metadata | Used by downstream code |
| Comments | str | 95.45 | 5 | original source field | metadata | Used by downstream code |
| Channel | str | 0.0 | 87 | original source field | metadata | Used by downstream code |
| Official channel | str | 57.27 | 1 | original source field | metadata | Unreferenced in project code |
| Subscriptions | str | 0.0 | 87 | original source field | metadata | Unreferenced in project code |
| Description | str | 44.55 | 32 | original source field | metadata | Used by downstream code |

### `data/real_world/raw_metadata/vcsl/label_file_uuid_total.json`  (DS-010; json)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| $ | dict | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.<key> | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.<key>[] | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.<key>[][] | int | n/a | n/a | Original source field | metadata | Unreferenced in project code |

### `data/real_world/raw_metadata/vcsl/pair_file_test.csv`  (DS-010; 54630 rows)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| query_id | str | 0.0 | 925 | original source field | benchmark pair (source split) | Unreferenced in project code |
| reference_id | str | 0.0 | 1066 | original source field | benchmark pair (source split) | Unreferenced in project code |

### `data/real_world/raw_metadata/vcsl/pair_file_train.csv`  (DS-010; 97033 rows)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| query_id | str | 0.0 | 2422 | original source field | benchmark pair (source split) | Unreferenced in project code |
| reference_id | str | 0.0 | 2687 | original source field | benchmark pair (source split) | Unreferenced in project code |

### `data/real_world/raw_metadata/vcsl/pair_file_val.csv`  (DS-010; 41798 rows)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| query_id | str | 0.0 | 1221 | original source field | benchmark pair (source split) | Unreferenced in project code |
| reference_id | str | 0.0 | 1332 | original source field | benchmark pair (source split) | Unreferenced in project code |

### `data/real_world/raw_metadata/vcsl/split_meta_pairs.json`  (DS-010; json)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| $ | dict | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.train | dict | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.train.<key> | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.train.<key>[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.val | dict | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.val.<key> | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.val.<key>[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test | dict | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.4f35a9a73d354cac8653eda43ccf8d8e | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.4f35a9a73d354cac8653eda43ccf8d8e[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.88a654aa1cc84ad2b9703d0a5521e43f | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.88a654aa1cc84ad2b9703d0a5521e43f[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.a372bb16d435449d8c089fcdaaf90ae4 | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.a372bb16d435449d8c089fcdaaf90ae4[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.f2998a313d9c4eadb1723fef854f9614 | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.f2998a313d9c4eadb1723fef854f9614[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.d71408e317c64ce9bd3fd1139e3d5c0c | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.d71408e317c64ce9bd3fd1139e3d5c0c[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.4bfb654708444cc48ddda9c4de532aab | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.4bfb654708444cc48ddda9c4de532aab[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.166195baa824427a8d82a285c56adc00 | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.166195baa824427a8d82a285c56adc00[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.ac92d0ea6e11418788887bf8b2df38b3 | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.ac92d0ea6e11418788887bf8b2df38b3[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.ff79943ea3cd44588f4da316a29a8e63 | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.ff79943ea3cd44588f4da316a29a8e63[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.05cb0d3087284ae9970a999baf6cb48a | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.05cb0d3087284ae9970a999baf6cb48a[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.71b46673cae14e238ccebb966ba7fd86 | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.71b46673cae14e238ccebb966ba7fd86[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.b6c84b3f8b1e4c3280d4634c745e516c | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.b6c84b3f8b1e4c3280d4634c745e516c[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.78cb6c2d559c4de9a605042afa4d2bcb | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.78cb6c2d559c4de9a605042afa4d2bcb[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.7133109c1db64ad5b3c726df4462b470 | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.7133109c1db64ad5b3c726df4462b470[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.88200e0f267d414aaadaf2bcd6e6ecfd | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.88200e0f267d414aaadaf2bcd6e6ecfd[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.dd44c4be9fdc4c95bdf075e7e756294e | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.dd44c4be9fdc4c95bdf075e7e756294e[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.06d224d87ea14fa5aec57903e8be37a0 | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.06d224d87ea14fa5aec57903e8be37a0[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.d54a1f1d31a94f5c92496b22bc6dc4b4 | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.d54a1f1d31a94f5c92496b22bc6dc4b4[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.e45b9eec5ea54e00a2d6e6689cd5fe92 | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.e45b9eec5ea54e00a2d6e6689cd5fe92[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.aa2783f15e994ccc853f85460ad0ad20 | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.aa2783f15e994ccc853f85460ad0ad20[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.2d500266205d4adc8638d2fea37a00b7 | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.2d500266205d4adc8638d2fea37a00b7[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.0ed7c63b71e446baaa27e351133f5726 | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.0ed7c63b71e446baaa27e351133f5726[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.574f2f0aac6749999fdfb41e630c1d51 | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.574f2f0aac6749999fdfb41e630c1d51[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.146c67ab895744e6b6b54dabeea4b64f | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.146c67ab895744e6b6b54dabeea4b64f[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.ecfe5a8b0cd54cb8b0e51da72dca9f1e | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.ecfe5a8b0cd54cb8b0e51da72dca9f1e[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.029d0980e5e04c75b6defd03070f251f | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.029d0980e5e04c75b6defd03070f251f[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.9e55757ab2f046a281dd1a25c6b247b5 | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.9e55757ab2f046a281dd1a25c6b247b5[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.5b74e41445984be9bff4dbc9f7356306 | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.5b74e41445984be9bff4dbc9f7356306[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.ff20c83f1e554f479e7c6d270e00d3ce | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.ff20c83f1e554f479e7c6d270e00d3ce[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.6c7d9a037f794846a0b79f8efeeee977 | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.test.6c7d9a037f794846a0b79f8efeeee977[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |

### `data/real_world/raw_metadata/vcsl/video_categories.json`  (DS-010; json)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| $ | dict | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.variety show | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.variety show[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.games | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.games[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.music videos | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.music videos[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.news | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.news[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.sports | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.sports[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.daily life | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.daily life[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.TV series | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.TV series[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.kichiku | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.kichiku[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.advertisement | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.advertisement[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.animation | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.animation[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.movies | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.movies[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |

### `data/real_world/raw_metadata/vcsl/videos_url_uuid.csv`  (DS-010; 9207 rows)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| url | str | 0.0 | 9207 | original source field | metadata | Used by downstream code |
| uuid | str | 0.0 | 9207 | original source field | metadata | Unreferenced in project code |

### `data/real_world/raw_metadata/zenodo_api/*.json`  (DS-012; json-group)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| $ | dict | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.created | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.modified | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.id | int | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.conceptrecid | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.doi | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.conceptdoi | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.doi_url | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata | dict | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata.title | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata.doi | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata.publication_date | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata.description | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata.access_right | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata.creators | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata.creators[] | dict | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata.creators[].name | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata.creators[].affiliation | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata.keywords | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata.keywords[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata.version | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata.references | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata.references[] | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata.language | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata.resource_type | dict | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata.resource_type.title | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata.resource_type.type | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata.license | dict | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata.license.id | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata.grants | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata.grants[] | dict | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata.grants[].code | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata.grants[].internal_id | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata.grants[].funder | dict | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata.grants[].funder.name | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata.grants[].funder.doi | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata.grants[].funder.acronym | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata.grants[].title | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata.grants[].acronym | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata.grants[].program | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata.grants[].url | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata.communities | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata.communities[] | dict | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata.communities[].id | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata.relations | dict | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata.relations.version | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata.relations.version[] | dict | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata.relations.version[].index | int | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata.relations.version[].is_last | bool | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata.relations.version[].parent | dict | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata.relations.version[].parent.pid_type | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata.relations.version[].parent.pid_value | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.title | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.links | dict | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.links.self | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.links.self_html | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.links.preview_html | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.links.doi | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.links.self_doi | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.links.self_doi_html | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.links.reserve_doi | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.links.parent | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.links.parent_html | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.links.parent_doi | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.links.parent_doi_html | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.links.self_iiif_manifest | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.links.self_iiif_sequence | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.links.files | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.links.media_files | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.links.latest | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.links.latest_html | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.links.versions | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.links.draft | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.links.access_links | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.links.access_grants | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.links.access_users | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.links.access_request | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.links.access | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.links.communities | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.links.communities-suggestions | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.links.request_deletion | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.links.file_modification | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.links.quota_increase | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.links.requests | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.updated | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.recid | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.revision | int | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.files | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.files[] | dict | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.files[].id | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.files[].key | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.files[].size | int | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.files[].checksum | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.files[].links | dict | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.files[].links.self | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.swh | dict | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.owners | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.owners[] | dict | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.owners[].id | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.status | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.stats | dict | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.stats.downloads | int | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.stats.unique_downloads | int | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.stats.views | int | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.stats.unique_views | int | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.stats.version_downloads | int | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.stats.version_unique_downloads | int | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.stats.version_unique_views | int | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.stats.version_views | int | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.state | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.submitted | bool | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata.creators[].orcid | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata.resource_type.subtype | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.links.thumbnails | dict | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.links.thumbnails.10 | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.links.thumbnails.50 | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.links.thumbnails.100 | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.links.thumbnails.250 | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.links.thumbnails.750 | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.links.thumbnails.1200 | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata.related_identifiers | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata.related_identifiers[] | dict | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata.related_identifiers[].identifier | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata.related_identifiers[].relation | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata.related_identifiers[].scheme | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata.alternate_identifiers | list | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata.alternate_identifiers[] | dict | n/a | n/a | Original source field | metadata | Unreferenced in project code |
| $.metadata.alternate_identifiers[].identifier | str | n/a | n/a | Original source field | metadata | Unreferenced in project code |

### `data/reports/acceptance_checks.json`  (DS-033; json)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| $ | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.<key> | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.<key>.ok | bool | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.<key>.evidence | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |

### `docs/datasets/ORVEX_REQUIREMENT_COVERAGE_MATRIX.csv`  (DS-034; 40 rows)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| requirement_id | str | 0.0 | 40 | Unknown | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| pdf_reference | str | 0.0 | 35 | Unknown | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| requirement | str | 0.0 | 40 | Unknown | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| modules | str | 0.0 | 16 | Unknown | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| phase | str | 0.0 | 4 | Unknown | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| artifacts | str | 0.0 | 40 | Unknown | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| checks | str | 0.0 | 38 | Unknown | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| status | str | 0.0 | 3 | Unknown | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| evidence | str | 0.0 | 38 | Unknown | metadata (unverified meaning) | Used by downstream code |
| limitation_or_blocker | str | 52.5 | 19 | Unknown | metadata (unverified meaning) | Referenced by audit/docs/tests only |

### `docs/datasets/column_lineage.csv`  (DS-034; 306 rows)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| table | str | 0.0 | 15 | Unknown | metadata (unverified meaning) | Used by downstream code |
| column | str | 0.0 | 243 | Unknown | metadata (unverified meaning) | Used by downstream code |
| source_datasets | str | 0.0 | 11 | Unknown | metadata (unverified meaning) | Used by downstream code |
| type | str | 0.0 | 6 | Unknown | metadata (unverified meaning) | Used by downstream code |
| nullable | str | 0.0 | 2 | Unknown | metadata (unverified meaning) | Used by downstream code |
| origin_code | str | 0.0 | 6 | Unknown | metadata (unverified meaning) | Used by downstream code |
| origin_meaning | str | 0.0 | 6 | Unknown | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| source_field_or_rule | str | 0.0 | 132 | Unknown | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| present_in_source_dataset | str | 0.0 | 2 | Unknown | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| description | str | 0.0 | 271 | Unknown | metadata (unverified meaning) | Used by downstream code |
| allowed_values | str | 62.09 | 103 | Unknown | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| validation | str | 0.0 | 2 | Unknown | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| rationale | str | 0.0 | 2 | Unknown | metadata (unverified meaning) | Referenced by audit/docs/tests only |

### `docs/datasets/necessity_audit/dataset_inventory.csv`  (DS-034; 47 rows)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| kind | str | 0.0 | 2 | Unknown | metadata (unverified meaning) | Used by downstream code |
| id | str | 0.0 | 47 | Unknown | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| name | str | 0.0 | 47 | Unknown | metadata (unverified meaning) | Used by downstream code |
| classification | str | 0.0 | 10 | Unknown | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| status | str | 0.0 | 9 | Unknown | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| verification | str | 0.0 | 5 | Unknown | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| records_local | int | 0.0 | 23 | Unknown | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| local_bytes | int | 0.0 | 25 | Unknown | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| reason | str | 34.04 | 31 | Unknown | metadata (unverified meaning) | Referenced by audit/docs/tests only |

### `docs/datasets/necessity_audit/dhash_baseline_results.json`  (DS-034; json)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| $ | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.threshold_fixed_a_priori | float | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.pairs_scored | int | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.latency_ms_per_pair | float | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.auc_train | float | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.auc_val | float | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.auc_test | float | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.test_negatives_by_hardness | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.test_negatives_by_hardness.easy | int | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.test_negatives_by_hardness.hard | int | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.auc_test_hard_negatives_only | float | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.auc_test_easy_negatives_only | float | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.auc_test_without_heldout_lineage | float | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.auc_test_heldout_lineage_pos_vs_all_neg | float | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.detection_rate_threshold | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.detection_rate_threshold.audio_source_only_not_visual_derivation | float | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.detection_rate_threshold.direct_derivation | float | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.detection_rate_threshold.edited_version | float | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.detection_rate_threshold.indirect_derivation | float | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.detection_rate_threshold.same_family_other | float | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.detection_rate_threshold.sibling_same_parent | float | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.detection_rate_threshold.unrelated_distinct_source | float | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.audio_mute | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.audio_mute.n | int | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.audio_mute.detected | float | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.audio_mute.audio_identical | float | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.audio_noise_mix | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.audio_noise_mix.n | int | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.audio_noise_mix.detected | float | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.audio_noise_mix.audio_identical | float | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.audio_replace | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.audio_replace.n | int | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.audio_replace.detected | float | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.audio_replace.audio_identical | float | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.caption_burn_in | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.caption_burn_in.n | int | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.caption_burn_in.detected | float | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.caption_burn_in.audio_identical | float | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.crop_center | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.crop_center.n | int | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.crop_center.detected | float | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.crop_center.audio_identical | float | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.mirror_color_shift | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.mirror_color_shift.n | int | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.mirror_color_shift.detected | float | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.mirror_color_shift.audio_identical | float | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.recompress_low | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.recompress_low.n | int | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.recompress_low.detected | float | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.recompress_low.audio_identical | float | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.reencode_hq | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.reencode_hq.n | int | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.reencode_hq.detected | float | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.reencode_hq.audio_identical | float | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.reupload_sim | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.reupload_sim.n | int | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.reupload_sim.detected | float | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.reupload_sim.audio_identical | float | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.speed_change | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.speed_change.n | int | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.speed_change.detected | float | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.speed_change.audio_identical | float | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.trim_head | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.trim_head.n | int | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.trim_head.detected | float | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.trim_head.audio_identical | float | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.trim_middle | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.trim_middle.n | int | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.trim_middle.detected | float | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.trim_middle.audio_identical | float | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.trim_tail | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.trim_tail.n | int | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.trim_tail.detected | float | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.trim_tail.audio_identical | float | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.watermark_overlay | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.watermark_overlay.n | int | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.watermark_overlay.detected | float | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.watermark_overlay.audio_identical | float | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.temporal_start_estimation | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.temporal_start_estimation.n | int | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.temporal_start_estimation.mean_abs_error_fraction | float | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.temporal_start_estimation.within_0_05 | float | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.temporal_start_estimation.first_frame_matched | float | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.temporal_start_estimation.per_type | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.temporal_start_estimation.per_type.trim_head | float | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.temporal_start_estimation.per_type.trim_middle | float | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.temporal_start_estimation.per_type.trim_tail | float | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.temporal_start_estimation.note | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |

### `docs/datasets/necessity_audit/requirement_data_decision_table.csv`  (DS-034; 40 rows)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| requirement_id | str | 0.0 | 40 | Unknown | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| required_capability | str | 0.0 | 40 | Unknown | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| existing_support | str | 0.0 | 40 | Unknown | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| evidence_it_works | str | 0.0 | 37 | Unknown | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| gap | str | 0.0 | 20 | Unknown | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| gap_type | str | 0.0 | 12 | Unknown | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| additional_data_necessary | str | 0.0 | 2 | Unknown | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| recommended_source_or_transformation | str | 0.0 | 17 | Unknown | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| permission_constraints | str | 0.0 | 8 | Unknown | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| est_additional_storage_gb | float | 0.0 | 7 | Unknown | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| acceptance_test | str | 0.0 | 37 | Unknown | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| status_now | str | 0.0 | 3 | Unknown | metadata (unverified meaning) | Referenced by audit/docs/tests only |

### `docs/datasets/necessity_audit/variant_independent_validation.json`  (DS-034; json)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| $ | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.passed_variants | int | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.readable_by_independent_ffprobe | int | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.duration_matches_registry | int | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.carries_controlled_variant_metadata_tag | int | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.parent_chain_complete | int | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.roots_eligible | int | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.audio_variants | int | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.audio_donor_documented_real_eligible | int | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.caption_variants | int | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.caption_variants_with_real_source_text | int | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.run_log_return0_and_passed | int | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tool_params_run_recorded | int | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.failed_variants | int | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.failed_excluded_and_no_file | int | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.leakage_check | bool | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.heldout_check | bool | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |

### `docs/datasets/schema_contract.json`  (DS-034; json)
| column / path | type | null % | distinct | original/added | role | usage |
|---|---|---|---|---|---|---|
| $ | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.origin_codes | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.origin_codes.a | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.origin_codes.b | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.origin_codes.c | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.origin_codes.d | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.origin_codes.e | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.origin_codes.f | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.vocabularies | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.vocabularies.record_origin | list | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.vocabularies.record_origin[] | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.vocabularies.media_origin | list | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.vocabularies.media_origin[] | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.vocabularies.transformation_status | list | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.vocabularies.transformation_status[] | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.vocabularies.access_status | list | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.vocabularies.access_status[] | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.vocabularies.direction_status | list | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.vocabularies.direction_status[] | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.vocabularies.label_status | list | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.vocabularies.label_status[] | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.vocabularies.inclusion_status | list | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.vocabularies.inclusion_status[] | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.vocabularies.split | list | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.vocabularies.split[] | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.vocabularies.validation_status | list | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.vocabularies.validation_status[] | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.source_registry | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.source_registry.path | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.source_registry.purpose | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.source_registry.phase | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.source_registry.columns | list | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.source_registry.columns[] | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.source_registry.columns[].name | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.source_registry.columns[].type | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.source_registry.columns[].nullable | bool | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.source_registry.columns[].origin | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.source_registry.columns[].lineage | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.source_registry.columns[].description | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.real_world_media_master | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.real_world_media_master.path | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.real_world_media_master.purpose | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.real_world_media_master.phase | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.real_world_media_master.columns | list | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.real_world_media_master.columns[] | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.real_world_media_master.columns[].name | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.real_world_media_master.columns[].type | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.real_world_media_master.columns[].nullable | bool | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.real_world_media_master.columns[].origin | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.real_world_media_master.columns[].lineage | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.real_world_media_master.columns[].description | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.controlled_variant_registry | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.controlled_variant_registry.path | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.controlled_variant_registry.purpose | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.controlled_variant_registry.phase | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.controlled_variant_registry.columns | list | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.controlled_variant_registry.columns[] | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.controlled_variant_registry.columns[].name | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.controlled_variant_registry.columns[].type | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.controlled_variant_registry.columns[].nullable | bool | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.controlled_variant_registry.columns[].origin | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.controlled_variant_registry.columns[].lineage | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.controlled_variant_registry.columns[].description | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.media_relationship_edges | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.media_relationship_edges.path | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.media_relationship_edges.purpose | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.media_relationship_edges.phase | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.media_relationship_edges.columns | list | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.media_relationship_edges.columns[] | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.media_relationship_edges.columns[].name | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.media_relationship_edges.columns[].type | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.media_relationship_edges.columns[].nullable | bool | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.media_relationship_edges.columns[].origin | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.media_relationship_edges.columns[].lineage | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.media_relationship_edges.columns[].description | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.platform_observations | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.platform_observations.path | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.platform_observations.purpose | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.platform_observations.phase | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.platform_observations.columns | list | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.platform_observations.columns[] | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.platform_observations.columns[].name | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.platform_observations.columns[].type | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.platform_observations.columns[].nullable | bool | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.platform_observations.columns[].origin | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.platform_observations.columns[].lineage | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.platform_observations.columns[].description | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.evidence_ledger | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.evidence_ledger.path | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.evidence_ledger.purpose | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.evidence_ledger.phase | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.evidence_ledger.columns | list | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.evidence_ledger.columns[] | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.evidence_ledger.columns[].name | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.evidence_ledger.columns[].type | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.evidence_ledger.columns[].nullable | bool | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.evidence_ledger.columns[].origin | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.evidence_ledger.columns[].lineage | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.evidence_ledger.columns[].description | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.feature_manifest | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.feature_manifest.path | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.feature_manifest.purpose | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.feature_manifest.phase | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.feature_manifest.columns | list | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.feature_manifest.columns[] | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.feature_manifest.columns[].name | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.feature_manifest.columns[].type | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.feature_manifest.columns[].nullable | bool | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.feature_manifest.columns[].origin | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.feature_manifest.columns[].lineage | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.feature_manifest.columns[].description | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.training_pairs | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.training_pairs.path | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.training_pairs.purpose | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.training_pairs.phase | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.training_pairs.columns | list | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.training_pairs.columns[] | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.training_pairs.columns[].name | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.training_pairs.columns[].type | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.training_pairs.columns[].nullable | bool | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.training_pairs.columns[].origin | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.training_pairs.columns[].lineage | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.training_pairs.columns[].description | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.campaign_candidate_clusters | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.campaign_candidate_clusters.path | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.campaign_candidate_clusters.purpose | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.campaign_candidate_clusters.phase | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.campaign_candidate_clusters.columns | list | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.campaign_candidate_clusters.columns[] | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.campaign_candidate_clusters.columns[].name | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.campaign_candidate_clusters.columns[].type | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.campaign_candidate_clusters.columns[].nullable | bool | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.campaign_candidate_clusters.columns[].origin | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.campaign_candidate_clusters.columns[].lineage | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.campaign_candidate_clusters.columns[].description | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.transformation_run_log | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.transformation_run_log.path | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.transformation_run_log.purpose | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.transformation_run_log.phase | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.transformation_run_log.columns | list | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.transformation_run_log.columns[] | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.transformation_run_log.columns[].name | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.transformation_run_log.columns[].type | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.transformation_run_log.columns[].nullable | bool | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.transformation_run_log.columns[].origin | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.transformation_run_log.columns[].lineage | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.transformation_run_log.columns[].description | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.download_access_attempt_log | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.download_access_attempt_log.path | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.download_access_attempt_log.purpose | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.download_access_attempt_log.phase | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.download_access_attempt_log.columns | list | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.download_access_attempt_log.columns[] | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.download_access_attempt_log.columns[].name | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.download_access_attempt_log.columns[].type | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.download_access_attempt_log.columns[].nullable | bool | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.download_access_attempt_log.columns[].origin | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.download_access_attempt_log.columns[].lineage | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.download_access_attempt_log.columns[].description | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.split_manifest | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.split_manifest.path | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.split_manifest.purpose | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.split_manifest.phase | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.split_manifest.columns | list | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.split_manifest.columns[] | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.split_manifest.columns[].name | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.split_manifest.columns[].type | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.split_manifest.columns[].nullable | bool | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.split_manifest.columns[].origin | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.split_manifest.columns[].lineage | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.split_manifest.columns[].description | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.experiment_registry | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.experiment_registry.path | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.experiment_registry.purpose | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.experiment_registry.phase | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.experiment_registry.columns | list | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.experiment_registry.columns[] | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.experiment_registry.columns[].name | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.experiment_registry.columns[].type | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.experiment_registry.columns[].nullable | bool | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.experiment_registry.columns[].origin | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.experiment_registry.columns[].lineage | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.experiment_registry.columns[].description | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.duplicate_map | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.duplicate_map.path | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.duplicate_map.purpose | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.duplicate_map.phase | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.duplicate_map.columns | list | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.duplicate_map.columns[] | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.duplicate_map.columns[].name | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.duplicate_map.columns[].type | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.duplicate_map.columns[].nullable | bool | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.duplicate_map.columns[].origin | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.duplicate_map.columns[].lineage | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.duplicate_map.columns[].description | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.group_examples | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.group_examples.path | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.group_examples.purpose | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.group_examples.phase | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.group_examples.columns | list | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.group_examples.columns[] | dict | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.group_examples.columns[].name | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.group_examples.columns[].type | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.group_examples.columns[].nullable | bool | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.group_examples.columns[].origin | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.group_examples.columns[].lineage | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |
| $.tables.group_examples.columns[].description | str | n/a | n/a | Added by ORVEX (generated artefact) | metadata | Unreferenced in project code |

## C. Field lineage of ORVEX-added fields (columns not copied from a source field)
| table | column | kind | source/parent | producer |
|---|---|---|---|---|
| split_manifest | split_version | bookkeeping/administrative | ORVEX | scripts/datasets/s5_features_pairs_splits.py:assign (lines 25-28) |
| split_manifest | source_family_id | bookkeeping/administrative | master | scripts/datasets/s5_features_pairs_splits.py:assign (lines 25-28) |
| split_manifest | source_dataset_id | bookkeeping/administrative | registry | scripts/datasets/s5_features_pairs_splits.py:assign (lines 25-28) |
| split_manifest | split | derived by deterministic rule/inferred | hash rule | scripts/datasets/s5_features_pairs_splits.py:assign (lines 25-28) |
| split_manifest | assignment_method | bookkeeping/administrative | ORVEX | scripts/datasets/s5_features_pairs_splits.py:assign (lines 25-28) |
| split_manifest | seed | bookkeeping/administrative | ORVEX | scripts/datasets/s5_features_pairs_splits.py:assign (lines 25-28) |
| split_manifest | domain_stratum | bookkeeping/administrative | search theme / manipulation type | scripts/datasets/s5_features_pairs_splits.py:assign (lines 25-28) |
| split_manifest | n_family_items | computed from media/files by a tool | count | scripts/datasets/s5_features_pairs_splits.py:assign (lines 25-28) |
| split_manifest | n_native_edges | computed from media/files by a tool | count | scripts/datasets/s5_features_pairs_splits.py:assign (lines 25-28) |
| split_manifest | heldout_transformations_in_family | derived by deterministic rule/inferred | lineage | scripts/datasets/s5_features_pairs_splits.py:assign (lines 25-28) |
| campaign_candidate_clusters | cluster_id | bookkeeping/administrative | ORVEX | scripts/datasets/s5_features_pairs_splits.py (module level) |
| campaign_candidate_clusters | observation_ids | bookkeeping/administrative | observations | scripts/datasets/s5_features_pairs_splits.py (module level) |
| campaign_candidate_clusters | media_ids | bookkeeping/administrative | master | scripts/datasets/s5_features_pairs_splits.py (module level) |
| campaign_candidate_clusters | account_pseudonyms | derived by deterministic rule/inferred | observations | scripts/datasets/s5_features_pairs_splits.py (module level) |
| campaign_candidate_clusters | time_window_start_utc | bookkeeping/administrative | observations | scripts/datasets/s5_features_pairs_splits.py (module level) |
| campaign_candidate_clusters | time_window_end_utc | bookkeeping/administrative | observations | scripts/datasets/s5_features_pairs_splits.py (module level) |
| campaign_candidate_clusters | common_media_signals | bookkeeping/administrative | edges | scripts/datasets/s5_features_pairs_splits.py (module level) |
| campaign_candidate_clusters | posting_pattern_signals | bookkeeping/administrative | observations | scripts/datasets/s5_features_pairs_splits.py (module level) |
| campaign_candidate_clusters | independent_coordination_evidence | bookkeeping/administrative | evidence | scripts/datasets/s5_features_pairs_splits.py (module level) |
| campaign_candidate_clusters | candidate_status | bookkeeping/administrative | policy | scripts/datasets/s5_features_pairs_splits.py (module level) |
| campaign_candidate_clusters | reviewer | analyst/human decision | human | scripts/datasets/s5_features_pairs_splits.py (module level) |
| campaign_candidate_clusters | limitations | bookkeeping/administrative | ORVEX | scripts/datasets/s5_features_pairs_splits.py (module level) |
| controlled_variant_registry | variant_media_id | bookkeeping/administrative | ORVEX id | scripts/datasets/s4_variants.py:process (lines 68-118) |
| controlled_variant_registry | direct_parent_media_id | bookkeeping/administrative | ORVEX transformation plan | scripts/datasets/s4_variants.py:process (lines 68-118) |
| controlled_variant_registry | root_source_media_id | bookkeeping/administrative | media master | scripts/datasets/s4_variants.py:process (lines 68-118) |
| controlled_variant_registry | ancestor_chain | derived by deterministic rule/inferred | parent links | scripts/datasets/s4_variants.py:process (lines 68-118) |
| controlled_variant_registry | video_source_media_id | bookkeeping/administrative | media master | scripts/datasets/s4_variants.py:process (lines 68-118) |
| controlled_variant_registry | audio_source_media_id | bookkeeping/administrative | media master | scripts/datasets/s4_variants.py:process (lines 68-118) |
| controlled_variant_registry | caption_text_source_media_id | bookkeeping/administrative | media master | scripts/datasets/s4_variants.py:process (lines 68-118) |
| controlled_variant_registry | caption_text_origin_field | bookkeeping/administrative | n/a | scripts/datasets/s4_variants.py:process (lines 68-118) |
| controlled_variant_registry | transformation_id | bookkeeping/administrative | catalogue | scripts/datasets/s4_variants.py:process (lines 68-118) |
| controlled_variant_registry | transformation_name | bookkeeping/administrative | catalogue | scripts/datasets/s4_variants.py:process (lines 68-118) |
| controlled_variant_registry | transformation_family | bookkeeping/administrative | catalogue | scripts/datasets/s4_variants.py:process (lines 68-118) |
| controlled_variant_registry | parameters_json | bookkeeping/administrative | ORVEX | scripts/datasets/s4_variants.py:process (lines 68-118) |
| controlled_variant_registry | tool_name | bookkeeping/administrative | ORVEX | scripts/datasets/s4_variants.py:process (lines 68-118) |
| controlled_variant_registry | tool_version | computed from media/files by a tool | ffmpeg -version | scripts/datasets/s4_variants.py:process (lines 68-118) |
| controlled_variant_registry | run_id | bookkeeping/administrative | ORVEX | scripts/datasets/s4_variants.py:process (lines 68-118) |
| controlled_variant_registry | seed | bookkeeping/administrative | ORVEX | scripts/datasets/s4_variants.py:process (lines 68-118) |
| controlled_variant_registry | created_utc | bookkeeping/administrative | ORVEX | scripts/datasets/s4_variants.py:process (lines 68-118) |
| controlled_variant_registry | local_path | bookkeeping/administrative | ORVEX | scripts/datasets/s4_variants.py:process (lines 68-118) |
| controlled_variant_registry | sha256 | computed from media/files by a tool | hashlib | scripts/datasets/s4_variants.py:process (lines 68-118) |
| controlled_variant_registry | bytes | computed from media/files by a tool | os.stat | scripts/datasets/s4_variants.py:process (lines 68-118) |
| controlled_variant_registry | duration_s | computed from media/files by a tool | ffprobe | scripts/datasets/s4_variants.py:process (lines 68-118) |
| controlled_variant_registry | width | computed from media/files by a tool | ffprobe | scripts/datasets/s4_variants.py:process (lines 68-118) |
| controlled_variant_registry | height | computed from media/files by a tool | ffprobe | scripts/datasets/s4_variants.py:process (lines 68-118) |
| controlled_variant_registry | fps | computed from media/files by a tool | ffprobe | scripts/datasets/s4_variants.py:process (lines 68-118) |
| controlled_variant_registry | has_audio | computed from media/files by a tool | ffprobe | scripts/datasets/s4_variants.py:process (lines 68-118) |
| controlled_variant_registry | generation_depth | derived by deterministic rule/inferred | chain length | scripts/datasets/s4_variants.py:process (lines 68-118) |
| controlled_variant_registry | chain_id | bookkeeping/administrative | catalogue | scripts/datasets/s4_variants.py:process (lines 68-118) |
| controlled_variant_registry | permission_basis | derived by deterministic rule/inferred | root licence | scripts/datasets/s4_variants.py:process (lines 68-118) |
| controlled_variant_registry | validation_status | computed from media/files by a tool | ffprobe checks | scripts/datasets/s4_variants.py:process (lines 68-118) |
| controlled_variant_registry | validation_checks_json | computed from media/files by a tool | ffprobe | scripts/datasets/s4_variants.py:process (lines 68-118) |
| controlled_variant_registry | failure_reason | bookkeeping/administrative | ORVEX | scripts/datasets/s4_variants.py:process (lines 68-118) |
| controlled_variant_registry | media_origin | bookkeeping/administrative | VOC | scripts/datasets/s4_variants.py:process (lines 68-118) |
| controlled_variant_registry | record_origin | bookkeeping/administrative | VOC | scripts/datasets/s4_variants.py:process (lines 68-118) |
| controlled_variant_registry | transformation_status | bookkeeping/administrative | VOC | scripts/datasets/s4_variants.py:process (lines 68-118) |
| controlled_variant_registry | usable_for_training | derived by deterministic rule/inferred | validation + split + held-out rule | scripts/datasets/s4_variants.py:process (lines 68-118) |
| controlled_variant_registry | source_split | derived by deterministic rule/inferred | split_manifest | scripts/datasets/s4_variants.py:process (lines 68-118) |
| duplicate_map | duplicate_id | bookkeeping/administrative | ORVEX | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| duplicate_map | canonical_media_id | bookkeeping/administrative | master | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| duplicate_map | duplicate_media_id | bookkeeping/administrative | master | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| duplicate_map | duplicate_type | derived by deterministic rule/inferred | rule | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| duplicate_map | evidence | computed from media/files by a tool | hash/dHash/URL | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| duplicate_map | resolution | bookkeeping/administrative | ORVEX | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| evidence_ledger | evidence_id | bookkeeping/administrative | ORVEX | scripts/datasets/s3_normalize.py:evid (lines 42-45) |
| evidence_ledger | evidence_type | bookkeeping/administrative | ORVEX | scripts/datasets/s3_normalize.py:evid (lines 42-45) |
| evidence_ledger | source_dataset_id | bookkeeping/administrative | source_registry | scripts/datasets/s3_normalize.py:evid (lines 42-45) |
| evidence_ledger | subject_type | bookkeeping/administrative | ORVEX | scripts/datasets/s3_normalize.py:evid (lines 42-45) |
| evidence_ledger | subject_id | bookkeeping/administrative | ORVEX | scripts/datasets/s3_normalize.py:evid (lines 42-45) |
| evidence_ledger | source_record_ref | bookkeeping/administrative | file path / record key | scripts/datasets/s3_normalize.py:evid (lines 42-45) |
| evidence_ledger | claim_supported | bookkeeping/administrative | ORVEX | scripts/datasets/s3_normalize.py:evid (lines 42-45) |
| evidence_ledger | claim_status | bookkeeping/administrative | policy | scripts/datasets/s3_normalize.py:evid (lines 42-45) |
| evidence_ledger | observed_fact_vs_inference | bookkeeping/administrative | policy | scripts/datasets/s3_normalize.py:evid (lines 42-45) |
| evidence_ledger | verification_method | bookkeeping/administrative | ORVEX | scripts/datasets/s3_normalize.py:evid (lines 42-45) |
| evidence_ledger | evidence_time_utc | bookkeeping/administrative | ORVEX | scripts/datasets/s3_normalize.py:evid (lines 42-45) |
| evidence_ledger | temporal_precision | bookkeeping/administrative | n/a | scripts/datasets/s3_normalize.py:evid (lines 42-45) |
| evidence_ledger | file_sha256 | computed from media/files by a tool | hashlib | scripts/datasets/s3_normalize.py:evid (lines 42-45) |
| evidence_ledger | reviewer_status | bookkeeping/administrative | policy | scripts/datasets/s3_normalize.py:evid (lines 42-45) |
| evidence_ledger | permission_status | derived by deterministic rule/inferred | licence | scripts/datasets/s3_normalize.py:evid (lines 42-45) |
| evidence_ledger | confidence_basis | bookkeeping/administrative | policy | scripts/datasets/s3_normalize.py:evid (lines 42-45) |
| evidence_ledger | limitations | bookkeeping/administrative | ORVEX | scripts/datasets/s3_normalize.py:evid (lines 42-45) |
| experiment_registry | experiment_id | bookkeeping/administrative | ORVEX | scripts/datasets/s9_feature_baseline.py (module level) |
| experiment_registry | dataset_versions | bookkeeping/administrative | ORVEX | scripts/datasets/s9_feature_baseline.py (module level) |
| experiment_registry | split_version | bookkeeping/administrative | ORVEX | scripts/datasets/s9_feature_baseline.py (module level) |
| experiment_registry | label_map_version | bookkeeping/administrative | ORVEX | scripts/datasets/s9_feature_baseline.py (module level) |
| experiment_registry | model_version | bookkeeping/administrative | ORVEX | scripts/datasets/s9_feature_baseline.py (module level) |
| experiment_registry | feature_version | bookkeeping/administrative | ORVEX | scripts/datasets/s9_feature_baseline.py (module level) |
| experiment_registry | metric_name | bookkeeping/administrative | ORVEX | scripts/datasets/s9_feature_baseline.py (module level) |
| experiment_registry | metric_value | bookkeeping/administrative | ORVEX | scripts/datasets/s9_feature_baseline.py (module level) |
| experiment_registry | protocol | bookkeeping/administrative | ORVEX | scripts/datasets/s9_feature_baseline.py (module level) |
| experiment_registry | heldout_policy | bookkeeping/administrative | ORVEX | scripts/datasets/s9_feature_baseline.py (module level) |
| experiment_registry | report_path | bookkeeping/administrative | ORVEX | scripts/datasets/s9_feature_baseline.py (module level) |
| experiment_registry | leakage_test_result | bookkeeping/administrative | ORVEX | scripts/datasets/s9_feature_baseline.py (module level) |
| feature_manifest | feature_record_id | bookkeeping/administrative | ORVEX | scripts/datasets/s5_features_pairs_splits.py:feat (lines 71-82) |
| feature_manifest | media_id | bookkeeping/administrative | media master / variants | scripts/datasets/s5_features_pairs_splits.py:feat (lines 71-82) |
| feature_manifest | feature_type | bookkeeping/administrative | ORVEX | scripts/datasets/s5_features_pairs_splits.py:feat (lines 71-82) |
| feature_manifest | extraction_status | computed from media/files by a tool | script result | scripts/datasets/s5_features_pairs_splits.py:feat (lines 71-82) |
| feature_manifest | tool_name | bookkeeping/administrative | ORVEX | scripts/datasets/s5_features_pairs_splits.py:feat (lines 71-82) |
| feature_manifest | tool_version | computed from media/files by a tool | tool | scripts/datasets/s5_features_pairs_splits.py:feat (lines 71-82) |
| feature_manifest | parameters_json | bookkeeping/administrative | ORVEX | scripts/datasets/s5_features_pairs_splits.py:feat (lines 71-82) |
| feature_manifest | sample_timestamps | computed from media/files by a tool | frame indices | scripts/datasets/s5_features_pairs_splits.py:feat (lines 71-82) |
| feature_manifest | feature_format | bookkeeping/administrative | ORVEX | scripts/datasets/s5_features_pairs_splits.py:feat (lines 71-82) |
| feature_manifest | storage_path | bookkeeping/administrative | ORVEX | scripts/datasets/s5_features_pairs_splits.py:feat (lines 71-82) |
| feature_manifest | storage_bytes | computed from media/files by a tool | os.stat | scripts/datasets/s5_features_pairs_splits.py:feat (lines 71-82) |
| feature_manifest | feature_sha256 | computed from media/files by a tool | hashlib | scripts/datasets/s5_features_pairs_splits.py:feat (lines 71-82) |
| feature_manifest | extracted_utc | bookkeeping/administrative | ORVEX | scripts/datasets/s5_features_pairs_splits.py:feat (lines 71-82) |
| feature_manifest | error | bookkeeping/administrative | ORVEX | scripts/datasets/s5_features_pairs_splits.py:feat (lines 71-82) |
| feature_manifest | permission_status | derived by deterministic rule/inferred | licence | scripts/datasets/s5_features_pairs_splits.py:feat (lines 71-82) |
| group_examples | group_id | bookkeeping/administrative | ORVEX | scripts/datasets/s5_features_pairs_splits.py (module level) |
| group_examples | source_family_id | derived by deterministic rule/inferred | root source | scripts/datasets/s5_features_pairs_splits.py (module level) |
| group_examples | member_media_ids | bookkeeping/administrative | master/variants | scripts/datasets/s5_features_pairs_splits.py (module level) |
| group_examples | n_members | computed from media/files by a tool | count | scripts/datasets/s5_features_pairs_splits.py (module level) |
| group_examples | family_member_ids | bookkeeping/administrative | variants | scripts/datasets/s5_features_pairs_splits.py (module level) |
| group_examples | distractor_ids | bookkeeping/administrative | other families in same split | scripts/datasets/s5_features_pairs_splits.py (module level) |
| group_examples | truth_edges | derived by deterministic rule/inferred | controlled lineage | scripts/datasets/s5_features_pairs_splits.py (module level) |
| group_examples | n_truth_edges | computed from media/files by a tool | count | scripts/datasets/s5_features_pairs_splits.py (module level) |
| group_examples | split | derived by deterministic rule/inferred | split_manifest | scripts/datasets/s5_features_pairs_splits.py (module level) |
| group_examples | split_version | bookkeeping/administrative | ORVEX | scripts/datasets/s5_features_pairs_splits.py (module level) |
| group_examples | label_origin | bookkeeping/administrative | ORVEX | scripts/datasets/s5_features_pairs_splits.py (module level) |
| group_examples | evidence_id | bookkeeping/administrative | ledger | scripts/datasets/s5_features_pairs_splits.py (module level) |
| group_examples | created_utc | bookkeeping/administrative | ORVEX | scripts/datasets/s5_features_pairs_splits.py (module level) |
| media_relationship_edges | relationship_id | bookkeeping/administrative | ORVEX | scripts/datasets/s3_normalize.py:edge (lines 46-50) |
| media_relationship_edges | source_dataset_id | bookkeeping/administrative | source_registry | scripts/datasets/s3_normalize.py:edge (lines 46-50) |
| media_relationship_edges | relation_scope | bookkeeping/administrative | ORVEX | scripts/datasets/s3_normalize.py:edge (lines 46-50) |
| media_relationship_edges | evidence_id | bookkeeping/administrative | evidence_ledger | scripts/datasets/s3_normalize.py:edge (lines 46-50) |
| media_relationship_edges | media_a_id | bookkeeping/administrative | media master/variant registry | scripts/datasets/s3_normalize.py:edge (lines 46-50) |
| media_relationship_edges | media_b_id | bookkeeping/administrative | media master/variant registry | scripts/datasets/s3_normalize.py:edge (lines 46-50) |
| media_relationship_edges | normalized_relation_type | derived by deterministic rule/inferred | mapping table | scripts/datasets/s3_normalize.py:edge (lines 46-50) |
| media_relationship_edges | direction_status | derived by deterministic rule/inferred | VOC | scripts/datasets/s3_normalize.py:edge (lines 46-50) |
| media_relationship_edges | parent_media_id | derived by deterministic rule/inferred | only when direction supported | scripts/datasets/s3_normalize.py:edge (lines 46-50) |
| media_relationship_edges | child_media_id | derived by deterministic rule/inferred | only when direction supported | scripts/datasets/s3_normalize.py:edge (lines 46-50) |
| media_relationship_edges | overlap_ratio | derived by deterministic rule/inferred | segment durations / duration | scripts/datasets/s3_normalize.py:edge (lines 46-50) |
| media_relationship_edges | transformation_type | bookkeeping/administrative | catalogue / ANAKIN manipulation-type | scripts/datasets/s3_normalize.py:edge (lines 46-50) |
| media_relationship_edges | label_source | bookkeeping/administrative | ORVEX | scripts/datasets/s3_normalize.py:edge (lines 46-50) |
| media_relationship_edges | label_status | bookkeeping/administrative | VOC | scripts/datasets/s3_normalize.py:edge (lines 46-50) |
| media_relationship_edges | evidence_status | bookkeeping/administrative | policy | scripts/datasets/s3_normalize.py:edge (lines 46-50) |
| media_relationship_edges | confidence_status | bookkeeping/administrative | policy | scripts/datasets/s3_normalize.py:edge (lines 46-50) |
| media_relationship_edges | reviewer | analyst/human decision | human reviewer | scripts/datasets/s3_normalize.py:edge (lines 46-50) |
| media_relationship_edges | method_version | bookkeeping/administrative | ORVEX | scripts/datasets/s3_normalize.py:edge (lines 46-50) |
| media_relationship_edges | created_utc | bookkeeping/administrative | ORVEX | scripts/datasets/s3_normalize.py:edge (lines 46-50) |
| media_relationship_edges | media_available_locally | computed from media/files by a tool | file exists | scripts/datasets/s3_normalize.py:edge (lines 46-50) |
| media_relationship_edges | conflict_flag | derived by deterministic rule/inferred | cross-source check | scripts/datasets/s3_normalize.py:edge (lines 46-50) |
| media_relationship_edges | notes | bookkeeping/administrative | ORVEX | scripts/datasets/s3_normalize.py:edge (lines 46-50) |
| platform_observations | observation_id | bookkeeping/administrative | ORVEX | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| platform_observations | media_id | bookkeeping/administrative | media master | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| platform_observations | observation_type | bookkeeping/administrative | ORVEX | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| platform_observations | coordination_status | bookkeeping/administrative | policy | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| platform_observations | platform_post_id | derived by deterministic rule/inferred | parsed from URL | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| platform_observations | account_id_pseudonym | derived by deterministic rule/inferred | SHA-256 prefix of public account name | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| platform_observations | account_id_source_field | bookkeeping/administrative | n/a | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| platform_observations | observation_time_utc | bookkeeping/administrative | n/a | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| platform_observations | time_precision | bookkeeping/administrative | n/a | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| platform_observations | hashtags | bookkeeping/administrative | n/a | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| platform_observations | metadata_source | bookkeeping/administrative | source_registry | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| platform_observations | collection_method | bookkeeping/administrative | ORVEX | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| platform_observations | order_in_cascade | derived by deterministic rule/inferred | row order inside FVC cascade | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| platform_observations | access_status | bookkeeping/administrative | VOC | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| platform_observations | evidence_id | bookkeeping/administrative | evidence_ledger | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| platform_observations | limitations | bookkeeping/administrative | ORVEX | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| real_world_media_master | media_id | bookkeeping/administrative | ORVEX id | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| real_world_media_master | source_dataset_id | bookkeeping/administrative | source_registry | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| real_world_media_master | platform_media_id | derived by deterministic rule/inferred | parsed from URL | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| real_world_media_master | canonical_url | derived by deterministic rule/inferred | normalized source_url | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| real_world_media_master | observed_time_utc | bookkeeping/administrative | n/a | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| real_world_media_master | collected_time_utc | bookkeeping/administrative | ORVEX run | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| real_world_media_master | time_precision | bookkeeping/administrative | n/a | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| real_world_media_master | duration_s | computed from media/files by a tool | ffprobe | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| real_world_media_master | width | computed from media/files by a tool | ffprobe | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| real_world_media_master | height | computed from media/files by a tool | ffprobe | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| real_world_media_master | fps | computed from media/files by a tool | ffprobe | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| real_world_media_master | video_codec | computed from media/files by a tool | ffprobe | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| real_world_media_master | audio_codec | computed from media/files by a tool | ffprobe | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| real_world_media_master | has_audio | computed from media/files by a tool | ffprobe | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| real_world_media_master | container | computed from media/files by a tool | ffprobe | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| real_world_media_master | file_bytes | computed from media/files by a tool | os.stat | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| real_world_media_master | local_path | bookkeeping/administrative | ORVEX | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| real_world_media_master | sha256 | computed from media/files by a tool | hashlib SHA-256 | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| real_world_media_master | access_status | bookkeeping/administrative | VOC.access_status | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| real_world_media_master | playable_status | computed from media/files by a tool | ffmpeg decode check | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| real_world_media_master | rights_status | derived by deterministic rule/inferred | licence | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| real_world_media_master | record_origin | bookkeeping/administrative | VOC.record_origin | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| real_world_media_master | media_origin | bookkeeping/administrative | VOC.media_origin | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| real_world_media_master | normalized_authenticity_status | derived by deterministic rule/inferred | mapping rule in policy | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| real_world_media_master | normalized_misleading_status | derived by deterministic rule/inferred | mapping rule | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| real_world_media_master | coordination_status | bookkeeping/administrative | ORVEX policy | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| real_world_media_master | evidence_id | bookkeeping/administrative | evidence_ledger | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| real_world_media_master | perceptual_hash_ref | computed from media/files by a tool | feature_manifest visual_dhash24 | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| real_world_media_master | annotation_status | bookkeeping/administrative | ORVEX | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| real_world_media_master | qc_flags | derived by deterministic rule/inferred | ORVEX QC rules | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| real_world_media_master | duplicate_of_media_id | derived by deterministic rule/inferred | duplicate_map | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| real_world_media_master | usable_for_variants | derived by deterministic rule/inferred | rights + QC rules | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| real_world_media_master | missingness_note | bookkeeping/administrative | ORVEX | scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_ |
| training_pairs | example_id | bookkeeping/administrative | ORVEX | scripts/datasets/s5_features_pairs_splits.py:addpair (lines 125-129) |
| training_pairs | media_a_id | bookkeeping/administrative | master/variants | scripts/datasets/s5_features_pairs_splits.py:addpair (lines 125-129) |
| training_pairs | media_b_id | bookkeeping/administrative | master/variants | scripts/datasets/s5_features_pairs_splits.py:addpair (lines 125-129) |
| training_pairs | relationship_id | bookkeeping/administrative | edges | scripts/datasets/s5_features_pairs_splits.py:addpair (lines 125-129) |
| training_pairs | label_binary_related | derived by deterministic rule/inferred | relationship_class | scripts/datasets/s5_features_pairs_splits.py:addpair (lines 125-129) |
| training_pairs | relationship_class | derived by deterministic rule/inferred | edge types | scripts/datasets/s5_features_pairs_splits.py:addpair (lines 125-129) |
| training_pairs | normalized_label | derived by deterministic rule/inferred | mapping | scripts/datasets/s5_features_pairs_splits.py:addpair (lines 125-129) |
| training_pairs | label_origin | bookkeeping/administrative | ORVEX | scripts/datasets/s5_features_pairs_splits.py:addpair (lines 125-129) |
| training_pairs | label_status | bookkeeping/administrative | VOC | scripts/datasets/s5_features_pairs_splits.py:addpair (lines 125-129) |
| training_pairs | evidence_id | bookkeeping/administrative | ledger | scripts/datasets/s5_features_pairs_splits.py:addpair (lines 125-129) |
| training_pairs | feature_refs | bookkeeping/administrative | feature_manifest | scripts/datasets/s5_features_pairs_splits.py:addpair (lines 125-129) |
| training_pairs | source_family_id | derived by deterministic rule/inferred | root source | scripts/datasets/s5_features_pairs_splits.py:addpair (lines 125-129) |
| training_pairs | split | derived by deterministic rule/inferred | split_manifest | scripts/datasets/s5_features_pairs_splits.py:addpair (lines 125-129) |
| training_pairs | split_version | bookkeeping/administrative | ORVEX | scripts/datasets/s5_features_pairs_splits.py:addpair (lines 125-129) |
| training_pairs | sampling_method | bookkeeping/administrative | ORVEX | scripts/datasets/s5_features_pairs_splits.py:addpair (lines 125-129) |
| training_pairs | negative_rationale | bookkeeping/administrative | ORVEX | scripts/datasets/s5_features_pairs_splits.py:addpair (lines 125-129) |
| training_pairs | hardness | derived by deterministic rule/inferred | rule | scripts/datasets/s5_features_pairs_splits.py:addpair (lines 125-129) |
| training_pairs | leakage_flag | derived by deterministic rule/inferred | leakage test | scripts/datasets/s5_features_pairs_splits.py:addpair (lines 125-129) |
| training_pairs | exclusion_reason | bookkeeping/administrative | ORVEX | scripts/datasets/s5_features_pairs_splits.py:addpair (lines 125-129) |
| training_pairs | includes_heldout_transform | derived by deterministic rule/inferred | lineage | scripts/datasets/s5_features_pairs_splits.py:addpair (lines 125-129) |
| training_pairs | created_utc | bookkeeping/administrative | ORVEX | scripts/datasets/s5_features_pairs_splits.py:addpair (lines 125-129) |
| transformation_run_log | run_id | bookkeeping/administrative | ORVEX | scripts/datasets/s4_variants.py:process (lines 68-118) |
| transformation_run_log | variant_media_id | bookkeeping/administrative | variant registry | scripts/datasets/s4_variants.py:process (lines 68-118) |
| transformation_run_log | input_media_ids | bookkeeping/administrative | ORVEX | scripts/datasets/s4_variants.py:process (lines 68-118) |
| transformation_run_log | tool_name | bookkeeping/administrative | ORVEX | scripts/datasets/s4_variants.py:process (lines 68-118) |
| transformation_run_log | tool_version | computed from media/files by a tool | ffmpeg | scripts/datasets/s4_variants.py:process (lines 68-118) |
| transformation_run_log | command_config | bookkeeping/administrative | ORVEX | scripts/datasets/s4_variants.py:process (lines 68-118) |
| transformation_run_log | parameters_json | bookkeeping/administrative | ORVEX | scripts/datasets/s4_variants.py:process (lines 68-118) |
| transformation_run_log | started_utc | bookkeeping/administrative | ORVEX | scripts/datasets/s4_variants.py:process (lines 68-118) |
| transformation_run_log | return_code | computed from media/files by a tool | process | scripts/datasets/s4_variants.py:process (lines 68-118) |
| transformation_run_log | output_validation_status | computed from media/files by a tool | ffprobe | scripts/datasets/s4_variants.py:process (lines 68-118) |
| transformation_run_log | output_bytes | computed from media/files by a tool | os.stat | scripts/datasets/s4_variants.py:process (lines 68-118) |
| transformation_run_log | storage_delta_bytes | computed from media/files by a tool | os.stat | scripts/datasets/s4_variants.py:process (lines 68-118) |
| transformation_run_log | error | bookkeeping/administrative | process | scripts/datasets/s4_variants.py:process (lines 68-118) |
| transformation_run_log | deterministic_notes | bookkeeping/administrative | ORVEX | scripts/datasets/s4_variants.py:process (lines 68-118) |
| transformation_run_log | seed | bookkeeping/administrative | ORVEX | scripts/datasets/s4_variants.py:process (lines 68-118) |
| download_access_attempt_log | attempt_id | bookkeeping/administrative | ORVEX | scripts/datasets/common.py:AccessLog (lines 76-86) |
| download_access_attempt_log | source_dataset_id | bookkeeping/administrative | registry | scripts/datasets/common.py:AccessLog (lines 76-86) |
| download_access_attempt_log | media_or_file_id | bookkeeping/administrative | ORVEX | scripts/datasets/common.py:AccessLog (lines 76-86) |
| download_access_attempt_log | url | bookkeeping/administrative | ORVEX | scripts/datasets/common.py:AccessLog (lines 76-86) |
| download_access_attempt_log | attempt_time_utc | bookkeeping/administrative | ORVEX | scripts/datasets/common.py:AccessLog (lines 76-86) |
| download_access_attempt_log | method | bookkeeping/administrative | ORVEX | scripts/datasets/common.py:AccessLog (lines 76-86) |
| download_access_attempt_log | http_status | computed from media/files by a tool | response | scripts/datasets/common.py:AccessLog (lines 76-86) |
| download_access_attempt_log | result_category | bookkeeping/administrative | ORVEX | scripts/datasets/common.py:AccessLog (lines 76-86) |
| download_access_attempt_log | terms_decision | bookkeeping/administrative | policy | scripts/datasets/common.py:AccessLog (lines 76-86) |
| download_access_attempt_log | retry_count | bookkeeping/administrative | ORVEX | scripts/datasets/common.py:AccessLog (lines 76-86) |
| download_access_attempt_log | bytes | computed from media/files by a tool | response | scripts/datasets/common.py:AccessLog (lines 76-86) |
| download_access_attempt_log | sha256 | computed from media/files by a tool | hashlib | scripts/datasets/common.py:AccessLog (lines 76-86) |
| download_access_attempt_log | final_status | bookkeeping/administrative | VOC.access_status | scripts/datasets/common.py:AccessLog (lines 76-86) |
| download_access_attempt_log | note | bookkeeping/administrative | ORVEX | scripts/datasets/common.py:AccessLog (lines 76-86) |
| source_registry | source_dataset_id | bookkeeping/administrative | ORVEX id (RW-xx) | scripts/datasets/s3_normalize.py:build_registry (lines 270-280) |
| source_registry | accessed_date | bookkeeping/administrative | date of verification | scripts/datasets/s3_normalize.py:build_registry (lines 270-280) |
| source_registry | derivative_use_status | derived by deterministic rule/inferred | licence text | scripts/datasets/s3_normalize.py:build_registry (lines 270-280) |
| source_registry | training_use_status | derived by deterministic rule/inferred | licence text | scripts/datasets/s3_normalize.py:build_registry (lines 270-280) |
| source_registry | redistribution_status | derived by deterministic rule/inferred | licence text | scripts/datasets/s3_normalize.py:build_registry (lines 270-280) |
| source_registry | real_world_eligibility | analyst/human decision | analyst decision with evidence | scripts/datasets/s3_normalize.py:build_registry (lines 270-280) |
| source_registry | media_origin_characterization | analyst/human decision | analyst decision | scripts/datasets/s3_normalize.py:build_registry (lines 270-280) |
| source_registry | planned_download_bytes | bookkeeping/administrative | selection plan | scripts/datasets/s3_normalize.py:build_registry (lines 270-280) |
| source_registry | actual_local_bytes | computed from media/files by a tool | du of local folder | scripts/datasets/s3_normalize.py:build_registry (lines 270-280) |
| source_registry | record_count_local | computed from media/files by a tool | row count of local files | scripts/datasets/s3_normalize.py:build_registry (lines 270-280) |
| source_registry | overlap_with | analyst/human decision | analyst comparison | scripts/datasets/s3_normalize.py:build_registry (lines 270-280) |
| source_registry | inclusion_status | bookkeeping/administrative | controlled vocabulary | scripts/datasets/s3_normalize.py:build_registry (lines 270-280) |
| source_registry | inclusion_reason | analyst/human decision | analyst decision | scripts/datasets/s3_normalize.py:build_registry (lines 270-280) |
| source_registry | tasks_supported | bookkeeping/administrative | mapping to ORVEX modules | scripts/datasets/s3_normalize.py:build_registry (lines 270-280) |
| source_registry | evidence_links | bookkeeping/administrative | URLs consulted | scripts/datasets/s3_normalize.py:build_registry (lines 270-280) |
| source_registry | limitations | analyst/human decision | analyst notes | scripts/datasets/s3_normalize.py:build_registry (lines 270-280) |
| source_registry | verification_level | bookkeeping/administrative | see policy | scripts/datasets/s3_normalize.py:build_registry (lines 270-280) |

## D. Missing, constant, duplicated and unused fields
- Columns that are 100% blank: 5: [('data/derived/tables/media_relationship_edges.csv', 'overlap_ratio'), ('data/derived/tables/media_relationship_edges.csv', 'reviewer'), ('data/derived/tables/platform_observations.csv', 'hashtags'), ('data/derived/tables/real_world_media_master.csv', 'observed_time_utc'), ('data/derived/tables/transformation_run_log.csv', 'error')]
- Constant columns (one distinct value): 50; first 12: ['split_manifest.csv.split_version', 'split_manifest.csv.assignment_method', 'split_manifest.csv.seed', 'controlled_variant_registry.csv.caption_text_origin_field', 'controlled_variant_registry.csv.tool_name', 'controlled_variant_registry.csv.tool_version', 'controlled_variant_registry.csv.failure_reason', 'controlled_variant_registry.csv.media_origin', 'controlled_variant_registry.csv.record_origin', 'experiment_registry.csv.dataset_versions', 'experiment_registry.csv.split_version', 'experiment_registry.csv.label_map_version']
- ORVEX-added columns referenced only by their producer or nowhere in project code: 0 of 259; examples: []
- ORVEX-added columns used by downstream pipeline code: 174
- Duplicate columns within a table: 15