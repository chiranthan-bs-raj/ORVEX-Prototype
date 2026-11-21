# ORVEX Column Lineage

Machine-readable: `docs/datasets/column_lineage.csv` (306 columns). Origin a/b = from a named source field; c = derived by rule; d = computed from media; e = analyst; f = ORVEX bookkeeping.

## Columns by origin
| code | meaning | columns |
|---|---|---|
| a | copied from a named source field | 41 |
| b | normalized/renamed from a named source field | 6 |
| c | derived by an explicit deterministic rule from named fields | 42 |
| d | computed from the actual media/files by a named tool | 44 |
| e | annotated/decided by a human analyst with stated evidence | 7 |
| f | new ORVEX bookkeeping/administrative column | 166 |

## Source-native fields mapped into ORVEX (kept verbatim or normalised)

| source | native field(s) | ORVEX target | treatment |
|---|---|---|---|
| FVC 2018 FVC.csv / FVC_dup.csv | cascade_id | event_or_cascade_id / native_record_id | copied |
|  | video_url | source_url, native_media_id (+canonical_url, platform, platform_media_id derived) | copied + derived |
|  | label | native_authenticity_label, native_misleading_label (verbatim) | copied |
| FVC v2.0 TSV | InVID_id, Link, Title, Type of Manipulation, Comments, Discussed, Appeared, Timestamp, Channel, Description | native_record_id, source_url, title, native_manipulation_type, description_caption, publisher_account_id; **Discussed, Appeared, Timestamp, Official channel, Subscriptions kept only in raw file** (not in normalised master) | partly normalised; loss documented |
| FVC v1.0 TSV | InVID_id, Link, Title, Comments, Discussed, Appeared | same as v2.0; Discussed/Appeared kept only in raw file | partly normalised |
| FIVR-200K | youtube_ids.txt | native_media_id/platform_media_id | copied |
|  | annotation.json (ND/DS/CS lists) | media_relationship_edges.native_label (verbatim) | copied |
|  | events.json (headline, text, topic, href, youtube) | event_or_cascade_id (index only); **headline/text/topic/href kept only in raw file** | loss documented |
| VCSL | videos_url_uuid.csv | source_url, native_record_id | copied |
|  | label_file_uuid_total.json | media_relationship_edges a/b_segment_start/end_s | copied |
|  | video_categories.json | title ('VCSL category: …') | normalised |
|  | pair_file_*.csv, split_meta_pairs.json | raw only (benchmark splits not reused: ORVEX splits by source family) | kept raw |
| ANAKIN metadata.csv | video-id, start-time, end-time, url, has-masks, task, manipulation-type, editor-id, full-available | native_record_id, edges a_segment_start/end_s, source_url (full), description_caption, native_manipulation_type, publisher_account_id (editor id); has-masks and full-available kept raw/edges | copied/normalised |
| Wikimedia Commons API | pageid, title, imageinfo (url, size, mime, sha1, timestamp, user, comment), extmetadata (LicenseShortName, LicenseUrl, Artist, Credit, AttributionRequired, ImageDescription), categories, globalusage | native_record_id, title, source_url, published_time_utc, publisher_account_id, license*, attribution, description_caption; **categories, upload comment, commons sha1 kept in commons_candidates.json only** | partly normalised |

## Extra columns NOT present in any source dataset (ORVEX-added: origin c/d/e/f)

| table | column | origin | rule / tool / reason |
|---|---|---|---|
| source_registry | source_dataset_id | f | ORVEX id (RW-xx) |
| source_registry | accessed_date | f | date of verification |
| source_registry | derivative_use_status | c | licence text |
| source_registry | training_use_status | c | licence text |
| source_registry | redistribution_status | c | licence text |
| source_registry | real_world_eligibility | e | analyst decision with evidence |
| source_registry | media_origin_characterization | e | analyst decision |
| source_registry | planned_download_bytes | f | selection plan |
| source_registry | actual_local_bytes | d | du of local folder |
| source_registry | record_count_local | d | row count of local files |
| source_registry | overlap_with | e | analyst comparison |
| source_registry | inclusion_status | f | controlled vocabulary |
| source_registry | inclusion_reason | e | analyst decision |
| source_registry | tasks_supported | f | mapping to ORVEX modules |
| source_registry | evidence_links | f | URLs consulted |
| source_registry | limitations | e | analyst notes |
| source_registry | verification_level | f | see policy |
| real_world_media_master | media_id | f | ORVEX id |
| real_world_media_master | source_dataset_id | f | source_registry |
| real_world_media_master | platform_media_id | c | parsed from URL |
| real_world_media_master | canonical_url | c | normalized source_url |
| real_world_media_master | observed_time_utc | f | n/a |
| real_world_media_master | collected_time_utc | f | ORVEX run |
| real_world_media_master | time_precision | f | n/a |
| real_world_media_master | duration_s | d | ffprobe |
| real_world_media_master | width | d | ffprobe |
| real_world_media_master | height | d | ffprobe |
| real_world_media_master | fps | d | ffprobe |
| real_world_media_master | video_codec | d | ffprobe |
| real_world_media_master | audio_codec | d | ffprobe |
| real_world_media_master | has_audio | d | ffprobe |
| real_world_media_master | container | d | ffprobe |
| real_world_media_master | file_bytes | d | os.stat |
| real_world_media_master | local_path | f | ORVEX |
| real_world_media_master | sha256 | d | hashlib SHA-256 |
| real_world_media_master | access_status | f | VOC.access_status |
| real_world_media_master | playable_status | d | ffmpeg decode check |
| real_world_media_master | rights_status | c | licence |
| real_world_media_master | record_origin | f | VOC.record_origin |
| real_world_media_master | media_origin | f | VOC.media_origin |
| real_world_media_master | normalized_authenticity_status | c | mapping rule in policy |
| real_world_media_master | normalized_misleading_status | c | mapping rule |
| real_world_media_master | coordination_status | f | ORVEX policy |
| real_world_media_master | evidence_id | f | evidence_ledger |
| real_world_media_master | perceptual_hash_ref | d | feature_manifest visual_dhash24 |
| real_world_media_master | annotation_status | f | ORVEX |
| real_world_media_master | qc_flags | c | ORVEX QC rules |
| real_world_media_master | duplicate_of_media_id | c | duplicate_map |
| real_world_media_master | usable_for_variants | c | rights + QC rules |
| real_world_media_master | missingness_note | f | ORVEX |
| controlled_variant_registry | variant_media_id | f | ORVEX id |
| controlled_variant_registry | direct_parent_media_id | f | ORVEX transformation plan |
| controlled_variant_registry | root_source_media_id | f | media master |
| controlled_variant_registry | ancestor_chain | c | parent links |
| controlled_variant_registry | video_source_media_id | f | media master |
| controlled_variant_registry | audio_source_media_id | f | media master |
| controlled_variant_registry | caption_text_source_media_id | f | media master |
| controlled_variant_registry | caption_text_origin_field | f | n/a |
| controlled_variant_registry | transformation_id | f | catalogue |
| controlled_variant_registry | transformation_name | f | catalogue |
| controlled_variant_registry | transformation_family | f | catalogue |
| controlled_variant_registry | parameters_json | f | ORVEX |
| controlled_variant_registry | tool_name | f | ORVEX |
| controlled_variant_registry | tool_version | d | ffmpeg -version |
| controlled_variant_registry | run_id | f | ORVEX |
| controlled_variant_registry | seed | f | ORVEX |
| controlled_variant_registry | created_utc | f | ORVEX |
| controlled_variant_registry | local_path | f | ORVEX |
| controlled_variant_registry | sha256 | d | hashlib |
| controlled_variant_registry | bytes | d | os.stat |
| controlled_variant_registry | duration_s | d | ffprobe |
| controlled_variant_registry | width | d | ffprobe |
| controlled_variant_registry | height | d | ffprobe |
| controlled_variant_registry | fps | d | ffprobe |
| controlled_variant_registry | has_audio | d | ffprobe |
| controlled_variant_registry | generation_depth | c | chain length |
| controlled_variant_registry | chain_id | f | catalogue |
| controlled_variant_registry | permission_basis | c | root licence |
| controlled_variant_registry | validation_status | d | ffprobe checks |
| controlled_variant_registry | validation_checks_json | d | ffprobe |
| controlled_variant_registry | failure_reason | f | ORVEX |
| controlled_variant_registry | media_origin | f | VOC |
| controlled_variant_registry | record_origin | f | VOC |
| controlled_variant_registry | transformation_status | f | VOC |
| controlled_variant_registry | usable_for_training | c | validation + split + held-out rule |
| controlled_variant_registry | source_split | c | split_manifest |
| media_relationship_edges | relationship_id | f | ORVEX |
| media_relationship_edges | source_dataset_id | f | source_registry |
| media_relationship_edges | relation_scope | f | ORVEX |
| media_relationship_edges | evidence_id | f | evidence_ledger |
| media_relationship_edges | media_a_id | f | media master/variant registry |
| media_relationship_edges | media_b_id | f | media master/variant registry |
| media_relationship_edges | normalized_relation_type | c | mapping table |
| media_relationship_edges | direction_status | c | VOC |
| media_relationship_edges | parent_media_id | c | only when direction supported |
| media_relationship_edges | child_media_id | c | only when direction supported |
| media_relationship_edges | overlap_ratio | c | segment durations / duration |
| media_relationship_edges | transformation_type | f | catalogue / ANAKIN manipulation-type |
| media_relationship_edges | label_source | f | ORVEX |
| media_relationship_edges | label_status | f | VOC |
| media_relationship_edges | evidence_status | f | policy |
| media_relationship_edges | confidence_status | f | policy |
| media_relationship_edges | reviewer | e | human reviewer |
| media_relationship_edges | method_version | f | ORVEX |
| media_relationship_edges | created_utc | f | ORVEX |
| media_relationship_edges | media_available_locally | d | file exists |
| media_relationship_edges | conflict_flag | c | cross-source check |
| media_relationship_edges | notes | f | ORVEX |
| platform_observations | observation_id | f | ORVEX |
| platform_observations | media_id | f | media master |
| platform_observations | observation_type | f | ORVEX |
| platform_observations | coordination_status | f | policy |
| platform_observations | platform_post_id | c | parsed from URL |
| platform_observations | account_id_pseudonym | c | SHA-256 prefix of public account name |
| platform_observations | account_id_source_field | f | n/a |
| platform_observations | observation_time_utc | f | n/a |
| platform_observations | time_precision | f | n/a |
| platform_observations | hashtags | f | n/a |
| platform_observations | metadata_source | f | source_registry |
| platform_observations | collection_method | f | ORVEX |
| platform_observations | order_in_cascade | c | row order inside FVC cascade |
| platform_observations | access_status | f | VOC |
| platform_observations | evidence_id | f | evidence_ledger |
| platform_observations | limitations | f | ORVEX |
| evidence_ledger | evidence_id | f | ORVEX |
| evidence_ledger | evidence_type | f | ORVEX |
| evidence_ledger | source_dataset_id | f | source_registry |
| evidence_ledger | subject_type | f | ORVEX |
| evidence_ledger | subject_id | f | ORVEX |
| evidence_ledger | source_record_ref | f | file path / record key |
| evidence_ledger | claim_supported | f | ORVEX |
| evidence_ledger | claim_status | f | policy |
| evidence_ledger | observed_fact_vs_inference | f | policy |
| evidence_ledger | verification_method | f | ORVEX |
| evidence_ledger | evidence_time_utc | f | ORVEX |
| evidence_ledger | temporal_precision | f | n/a |
| evidence_ledger | file_sha256 | d | hashlib |
| evidence_ledger | reviewer_status | f | policy |
| evidence_ledger | permission_status | c | licence |
| evidence_ledger | confidence_basis | f | policy |
| evidence_ledger | limitations | f | ORVEX |
| feature_manifest | feature_record_id | f | ORVEX |
| feature_manifest | media_id | f | media master / variants |
| feature_manifest | feature_type | f | ORVEX |
| feature_manifest | extraction_status | d | script result |
| feature_manifest | tool_name | f | ORVEX |
| feature_manifest | tool_version | d | tool |
| feature_manifest | parameters_json | f | ORVEX |
| feature_manifest | sample_timestamps | d | frame indices |
| feature_manifest | feature_format | f | ORVEX |
| feature_manifest | storage_path | f | ORVEX |
| feature_manifest | storage_bytes | d | os.stat |
| feature_manifest | feature_sha256 | d | hashlib |
| feature_manifest | extracted_utc | f | ORVEX |
| feature_manifest | error | f | ORVEX |
| feature_manifest | permission_status | c | licence |
| training_pairs | example_id | f | ORVEX |
| training_pairs | media_a_id | f | master/variants |
| training_pairs | media_b_id | f | master/variants |
| training_pairs | relationship_id | f | edges |
| training_pairs | label_binary_related | c | relationship_class |
| training_pairs | relationship_class | c | edge types |
| training_pairs | normalized_label | c | mapping |
| training_pairs | label_origin | f | ORVEX |
| training_pairs | label_status | f | VOC |
| training_pairs | evidence_id | f | ledger |
| training_pairs | feature_refs | f | feature_manifest |
| training_pairs | source_family_id | c | root source |
| training_pairs | split | c | split_manifest |
| training_pairs | split_version | f | ORVEX |
| training_pairs | sampling_method | f | ORVEX |
| training_pairs | negative_rationale | f | ORVEX |
| training_pairs | hardness | c | rule |
| training_pairs | leakage_flag | c | leakage test |
| training_pairs | exclusion_reason | f | ORVEX |
| training_pairs | includes_heldout_transform | c | lineage |
| training_pairs | created_utc | f | ORVEX |
| campaign_candidate_clusters | cluster_id | f | ORVEX |
| campaign_candidate_clusters | observation_ids | f | observations |
| campaign_candidate_clusters | media_ids | f | master |
| campaign_candidate_clusters | account_pseudonyms | c | observations |
| campaign_candidate_clusters | time_window_start_utc | f | observations |
| campaign_candidate_clusters | time_window_end_utc | f | observations |
| campaign_candidate_clusters | common_media_signals | f | edges |
| campaign_candidate_clusters | posting_pattern_signals | f | observations |
| campaign_candidate_clusters | independent_coordination_evidence | f | evidence |
| campaign_candidate_clusters | candidate_status | f | policy |
| campaign_candidate_clusters | reviewer | e | human |
| campaign_candidate_clusters | limitations | f | ORVEX |
| transformation_run_log | run_id | f | ORVEX |
| transformation_run_log | variant_media_id | f | variant registry |
| transformation_run_log | input_media_ids | f | ORVEX |
| transformation_run_log | tool_name | f | ORVEX |
| transformation_run_log | tool_version | d | ffmpeg |
| transformation_run_log | command_config | f | ORVEX |
| transformation_run_log | parameters_json | f | ORVEX |
| transformation_run_log | started_utc | f | ORVEX |
| transformation_run_log | return_code | d | process |
| transformation_run_log | output_validation_status | d | ffprobe |
| transformation_run_log | output_bytes | d | os.stat |
| transformation_run_log | storage_delta_bytes | d | os.stat |
| transformation_run_log | error | f | process |
| transformation_run_log | deterministic_notes | f | ORVEX |
| transformation_run_log | seed | f | ORVEX |
| download_access_attempt_log | attempt_id | f | ORVEX |
| download_access_attempt_log | source_dataset_id | f | registry |
| download_access_attempt_log | media_or_file_id | f | ORVEX |
| download_access_attempt_log | url | f | ORVEX |
| download_access_attempt_log | attempt_time_utc | f | ORVEX |
| download_access_attempt_log | method | f | ORVEX |
| download_access_attempt_log | http_status | d | response |
| download_access_attempt_log | result_category | f | ORVEX |
| download_access_attempt_log | terms_decision | f | policy |
| download_access_attempt_log | retry_count | f | ORVEX |
| download_access_attempt_log | bytes | d | response |
| download_access_attempt_log | sha256 | d | hashlib |
| download_access_attempt_log | final_status | f | VOC.access_status |
| download_access_attempt_log | note | f | ORVEX |
| split_manifest | split_version | f | ORVEX |
| split_manifest | source_family_id | f | master |
| split_manifest | source_dataset_id | f | registry |
| split_manifest | split | c | hash rule |
| split_manifest | assignment_method | f | ORVEX |
| split_manifest | seed | f | ORVEX |
| split_manifest | domain_stratum | f | search theme / manipulation type |
| split_manifest | n_family_items | d | count |
| split_manifest | n_native_edges | d | count |
| split_manifest | heldout_transformations_in_family | c | lineage |
| experiment_registry | experiment_id | f | ORVEX |
| experiment_registry | dataset_versions | f | ORVEX |
| experiment_registry | split_version | f | ORVEX |
| experiment_registry | label_map_version | f | ORVEX |
| experiment_registry | model_version | f | ORVEX |
| experiment_registry | feature_version | f | ORVEX |
| experiment_registry | metric_name | f | ORVEX |
| experiment_registry | metric_value | f | ORVEX |
| experiment_registry | protocol | f | ORVEX |
| experiment_registry | heldout_policy | f | ORVEX |
| experiment_registry | report_path | f | ORVEX |
| experiment_registry | leakage_test_result | f | ORVEX |
| duplicate_map | duplicate_id | f | ORVEX |
| duplicate_map | canonical_media_id | f | master |
| duplicate_map | duplicate_media_id | f | master |
| duplicate_map | duplicate_type | c | rule |
| duplicate_map | evidence | d | hash/dHash/URL |
| duplicate_map | resolution | f | ORVEX |
| group_examples | group_id | f | ORVEX |
| group_examples | source_family_id | c | root source |
| group_examples | member_media_ids | f | master/variants |
| group_examples | n_members | d | count |
| group_examples | family_member_ids | f | variants |
| group_examples | distractor_ids | f | other families in same split |
| group_examples | truth_edges | c | controlled lineage |
| group_examples | n_truth_edges | d | count |
| group_examples | split | c | split_manifest |
| group_examples | split_version | f | ORVEX |
| group_examples | label_origin | f | ORVEX |
| group_examples | evidence_id | f | ledger |
| group_examples | created_utc | f | ORVEX |