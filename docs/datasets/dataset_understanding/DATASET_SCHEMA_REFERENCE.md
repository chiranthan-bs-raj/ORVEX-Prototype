# Dataset Schema Reference

Every field of every structured file (64 files, 1269 fields) is in `COMPLETE_COLUMN_DICTIONARY.csv`; 813 nested/undocumented fields are flagged `UNKNOWN SEMANTICS`. This page lists each file's columns; statistics are in the dictionary.

### `LOOP-MIND_Novelty_Independent_Verification_2_4_5.xlsx#Literature Review` (DS-037; 20 fields)
`Novelty and Theme`, `Paper Title`, `Year`, `Authors`, `Research Objective`, `Detailed Abstract (Paraphrased)`, `Technical Stack / Methods`, `Dataset and Evaluation`, `Main Findings`, `Conclusion`, `Drawbacks / Limitations`, `Similarity to LOOP-MIND`, `How LOOP-MIND Improves the Limitation`, `Research Gap / Contribution Angle`, `Novelty Status`, `Last Verification`, `Verification Evidence`, `What to Tell the Jury`, `Technical Stack / Methods (of my project LOOP-MIND)`, `Dataset and Evaluation (of my project LOOP-MIND)`

### `ORVEX_Literature/ORVEX_Literature_Review_10_1.xlsx#Feasibility` (DS-035; 6 fields)
`Area`, `Rating`, `Assessment`, `Evidence from literature / machine`, `Main risk`, `Mitigation / decision`

### `ORVEX_Literature/ORVEX_Literature_Review_10_1.xlsx#Literature Review` (DS-035; 20 fields)
`Novelty and Theme`, `Paper Title`, `Year`, `Authors`, `Research Objective`, `Detailed Abstract (Paraphrased)`, `Technical Stack / Methods`, `Dataset and Evaluation`, `Main Findings`, `Conclusion`, `Drawbacks / Limitations`, `Similarity to ORVEX`, `How ORVEX Improves the Limitation`, `Research Gap / Contribution Angle`, `Novelty Status`, `Last Verification`, `Verification Evidence`, `What to Tell the Jury`, `Technical Stack / Methods (of my project ORVEX)`, `Dataset and Evaluation (of my project ORVEX)`

### `ORVEX_Literature/ORVEX_Literature_Review_10_1.xlsx#Novelty Verdict` (DS-035; 7 fields)
`ORVEX claim (spec §)`, `Closest prior work in this review`, `What already exists`, `What was NOT found in this review`, `Verdict`, `Safe wording for report / jury`, `Evidence needed from experiments`

### `ORVEX_Literature/ORVEX_Literature_Review_10_1.xlsx#Open Items` (DS-035; 3 fields)
`#`, `Item`, `Why / suggested next step`

### `ORVEX_Literature/ORVEX_Literature_Review_10_1.xlsx#Paper Register` (DS-035; 9 fields)
`#`, `Theme`, `Paper`, `Year`, `Venue / source`, `Link`, `Local file`, `Access`, `Verification level`

### `ORVEX_Literature/ORVEX_Literature_Review_10_1.xlsx#Research Summary` (DS-035; 2 fields)
`Topic`, `Summary`

### `ORVEX_Literature/ORVEX_Literature_Review_10_1.xlsx#Search Log` (DS-035; 4 fields)
`#`, `Query / method`, `Source`, `Outcome`

### `data/derived/features/audio_fingerprint.jsonl` (DS-022; 4 fields)
`$`, `$.media_id`, `$.audio_md5_8k`, `$.audio_env_1s`

### `data/derived/features/visual_dhash24.jsonl` (DS-021; 6 fields)
`$`, `$.media_id`, `$.dhash24`, `$.dhash24[]`, `$.frame_indices`, `$.frame_indices[]`

### `data/derived/splits/split_manifest.csv` (DS-025; 10 fields)
`split_version`, `source_family_id`, `source_dataset_id`, `split`, `assignment_method`, `seed`, `domain_stratum`, `n_family_items`, `n_native_edges`, `heldout_transformations_in_family`

### `data/derived/tables/campaign_candidate_clusters.csv` (DS-029; 12 fields)
`cluster_id`, `observation_ids`, `media_ids`, `account_pseudonyms`, `time_window_start_utc`, `time_window_end_utc`, `common_media_signals`, `posting_pattern_signals`, `independent_coordination_evidence`, `candidate_status`, `reviewer`, `limitations`

### `data/derived/tables/controlled_variant_registry.csv` (DS-014; 38 fields)
`variant_media_id`, `direct_parent_media_id`, `root_source_media_id`, `ancestor_chain`, `video_source_media_id`, `audio_source_media_id`, `caption_text_source_media_id`, `caption_text`, `caption_text_origin_field`, `transformation_id`, `transformation_name`, `transformation_family`, `parameters_json`, `tool_name`, `tool_version`, `run_id`, `seed`, `created_utc`, `local_path`, `sha256`, `bytes`, `duration_s`, `width`, `height`, `fps`, `has_audio`, `generation_depth`, `chain_id`, `permission_basis`, `root_license`, `validation_status`, `validation_checks_json`, `failure_reason`, `media_origin`, `record_origin`, `transformation_status`, `usable_for_training`, `source_split`

### `data/derived/tables/duplicate_map.csv` (DS-026; 6 fields)
`duplicate_id`, `canonical_media_id`, `duplicate_media_id`, `duplicate_type`, `evidence`, `resolution`

### `data/derived/tables/evidence_ledger.csv` (DS-019; 18 fields)
`evidence_id`, `evidence_type`, `source_dataset_id`, `subject_type`, `subject_id`, `source_url`, `source_record_ref`, `claim_supported`, `claim_status`, `observed_fact_vs_inference`, `verification_method`, `evidence_time_utc`, `temporal_precision`, `file_sha256`, `reviewer_status`, `permission_status`, `confidence_basis`, `limitations`

### `data/derived/tables/experiment_registry.csv` (DS-030; 12 fields)
`experiment_id`, `dataset_versions`, `split_version`, `label_map_version`, `model_version`, `feature_version`, `metric_name`, `metric_value`, `protocol`, `heldout_policy`, `report_path`, `leakage_test_result`

### `data/derived/tables/feature_manifest.csv` (DS-020; 15 fields)
`feature_record_id`, `media_id`, `feature_type`, `extraction_status`, `tool_name`, `tool_version`, `parameters_json`, `sample_timestamps`, `feature_format`, `storage_path`, `storage_bytes`, `feature_sha256`, `extracted_utc`, `error`, `permission_status`

### `data/derived/tables/group_examples.csv` (DS-024; 13 fields)
`group_id`, `source_family_id`, `member_media_ids`, `n_members`, `family_member_ids`, `distractor_ids`, `truth_edges`, `n_truth_edges`, `split`, `split_version`, `label_origin`, `evidence_id`, `created_utc`

### `data/derived/tables/media_relationship_edges.csv` (DS-017; 29 fields)
`relationship_id`, `source_dataset_id`, `relation_scope`, `evidence_id`, `media_a_id`, `media_b_id`, `native_media_a_id`, `native_media_b_id`, `native_label`, `normalized_relation_type`, `direction_status`, `parent_media_id`, `child_media_id`, `a_segment_start_s`, `a_segment_end_s`, `b_segment_start_s`, `b_segment_end_s`, `overlap_ratio`, `transformation_type`, `label_source`, `label_status`, `evidence_status`, `confidence_status`, `reviewer`, `method_version`, `created_utc`, `media_available_locally`, `conflict_flag`, `notes`

### `data/derived/tables/platform_observations.csv` (DS-018; 22 fields)
`observation_id`, `media_id`, `observation_type`, `coordination_status`, `platform`, `platform_post_id`, `post_url`, `account_id_pseudonym`, `account_id_source_field`, `publish_time_utc`, `observation_time_utc`, `time_precision`, `caption_text`, `hashtags`, `engagement_refs`, `metadata_source`, `collection_method`, `order_in_cascade`, `cascade_id`, `access_status`, `evidence_id`, `limitations`

### `data/derived/tables/real_world_media_master.csv` (DS-016; 49 fields)
`media_id`, `source_dataset_id`, `release_version`, `native_record_id`, `native_media_id`, `platform`, `platform_media_id`, `source_url`, `canonical_url`, `title`, `description_caption`, `publisher_account_id`, `event_or_cascade_id`, `published_time_utc`, `observed_time_utc`, `collected_time_utc`, `time_precision`, `duration_s`, `width`, `height`, `fps`, `video_codec`, `audio_codec`, `has_audio`, `container`, `file_bytes`, `local_path`, `sha256`, `access_status`, `playable_status`, `rights_status`, `license`, `license_url`, `attribution`, `record_origin`, `media_origin`, `native_authenticity_label`, `native_misleading_label`, `native_manipulation_type`, `normalized_authenticity_status`, `normalized_misleading_status`, `coordination_status`, `evidence_id`, `perceptual_hash_ref`, `annotation_status`, `qc_flags`, `duplicate_of_media_id`, `usable_for_variants`, `missingness_note`

### `data/derived/tables/training_pairs.csv` (DS-023; 23 fields)
`example_id`, `media_a_id`, `media_b_id`, `relationship_id`, `label_binary_related`, `relationship_class`, `native_label`, `normalized_label`, `label_origin`, `label_status`, `evidence_id`, `feature_refs`, `source_family_id`, `event_or_cascade_group_id`, `split`, `split_version`, `sampling_method`, `negative_rationale`, `hardness`, `leakage_flag`, `exclusion_reason`, `includes_heldout_transform`, `created_utc`

### `data/derived/tables/transformation_run_log.csv` (DS-015; 15 fields)
`run_id`, `variant_media_id`, `input_media_ids`, `tool_name`, `tool_version`, `command_config`, `parameters_json`, `started_utc`, `return_code`, `output_validation_status`, `output_bytes`, `storage_delta_bytes`, `error`, `deterministic_notes`, `seed`

### `data/manifests/_build/access_log.jsonl` (DS-032; 14 fields)
`$`, `$.attempt_time_utc`, `$.method`, `$.retry_count`, `$.terms_decision`, `$.source_dataset_id`, `$.media_or_file_id`, `$.url`, `$.http_status`, `$.result_category`, `$.bytes`, `$.sha256`, `$.final_status`, `$.note`

### `data/manifests/_build/eligible_titles.txt` (DS-032; 1 fields)
`eligible_titles.txt`

### `data/manifests/_build/variants/*.json` (DS-032; 21 fields)
`$`, `$.recs`, `$.recs[]`, `$.recs[].<key>`, `$.logs`, `$.logs[]`, `$.logs[].run_id`, `$.logs[].variant_media_id`, `$.logs[].input_media_ids`, `$.logs[].tool_name`, `$.logs[].tool_version`, `$.logs[].command_config`, `$.logs[].parameters_json`, `$.logs[].started_utc`, `$.logs[].return_code`, `$.logs[].output_validation_status`, `$.logs[].output_bytes`, `$.logs[].storage_delta_bytes`, `$.logs[].error`, `$.logs[].deterministic_notes`, `$.logs[].seed`

### `data/manifests/attribution.csv` (DS-031; 9 fields)
`media_id`, `title`, `author_or_credit`, `license`, `license_url`, `file_page_url`, `attribution_required`, `used_as_variant_source`, `retrieved`

### `data/manifests/checksums.sha256` (DS-031; 1 fields)
`checksums.sha256`

### `data/manifests/download_access_attempt_log.csv` (DS-028; 14 fields)
`attempt_id`, `source_dataset_id`, `media_or_file_id`, `url`, `attempt_time_utc`, `method`, `http_status`, `result_category`, `terms_decision`, `retry_count`, `bytes`, `sha256`, `final_status`, `note`

### `data/manifests/native_id_crosswalk.csv` (DS-031; 9 fields)
`source_dataset_id`, `release_version`, `native_record_id`, `native_media_id`, `platform`, `platform_media_id`, `source_url`, `canonical_url`, `media_id`

### `data/manifests/selection_plan.json` (DS-031; 34 fields)
`$`, `$.generated`, `$.search_date`, `$.search_terms`, `$.search_terms[]`, `$.candidates_considered`, `$.commons`, `$.commons.queries`, `$.commons.queries[]`, `$.commons.queries[][]`, `$.commons.per_query_max_new_files`, `$.commons.file_size_bytes`, `$.commons.file_size_bytes[]`, `$.commons.licence_gate`, `$.commons.stem_dedupe`, `$.commons.qc`, `$.anakin`, `$.anakin.rule`, `$.anakin.selected_pairs`, `$.variants`, `$.variants.transformations`, `$.variants.chains`, `$.variants.donor_and_caption_pick`, `$.variants.test_only_types`, `$.variants.test_only_types[]`, `$.splits`, `$.splits.unit`, `$.splits.pattern`, `$.splits.seed`, `$.splits.version`, `$.negatives`, `$.negatives.easy`, `$.negatives.hard`, `$.negatives.within`

### `data/manifests/source_registry.csv` (DS-027; 30 fields)
`source_dataset_id`, `title`, `creator`, `release_version`, `official_url`, `download_url`, `paper_doi_or_url`, `accessed_date`, `license_terms`, `license_evidence_url`, `bytes_or_urls_provided`, `derivative_use_status`, `training_use_status`, `redistribution_status`, `real_world_eligibility`, `native_task`, `native_labels`, `media_origin_characterization`, `release_size_bytes`, `planned_download_bytes`, `actual_local_bytes`, `record_count_local`, `auth_required`, `overlap_with`, `inclusion_status`, `inclusion_reason`, `tasks_supported`, `evidence_links`, `limitations`, `verification_level`

### `data/manifests/storage_budget.csv` (DS-031; 8 fields)
`kind`, `name`, `bytes`, `GB_decimal`, `GiB`, `allocation_bytes`, `within_allocation`, `source`

### `data/real_world/raw_metadata/commons/commons_candidates.json` (DS-002; 25 fields)
`$`, `$[]`, `$[].pageid`, `$[].title`, `$[].url`, `$[].page_url`, `$[].mime`, `$[].size`, `$[].uploaded`, `$[].uploader`, `$[].upload_comment`, `$[].commons_sha1`, `$[].license`, `$[].license_url`, `$[].author`, `$[].credit`, `$[].attribution_required`, `$[].description`, `$[].categories`, `$[].categories[]`, `$[].domain`, `$[].query`, `$[].global_usage_count`, `$[].media_id`, `$[].local_file`

### `data/real_world/raw_metadata/covid_misinfo_4557828/covid-misinfo-videos.csv.gz` (DS-011; 14 fields)
`youtube_link`, `video_title`, `video_description`, `view_count`, `channel_id`, `subscriber_count`, `removal_timestamp`, `published_timestamp`, `archive_url`, `facebook_graph_reactions`, `facebook_graph_comments`, `facebook_graph_shares`, `twitter_post_ids`, `facebook_post_ids`

### `data/real_world/raw_metadata/hf_api/anakin.json` (DS-005; 29 fields)
`$`, `$._id`, `$.id`, `$.author`, `$.sha`, `$.lastModified`, `$.private`, `$.gated`, `$.disabled`, `$.tags`, `$.tags[]`, `$.citation`, `$.description`, `$.downloads`, `$.likes`, `$.cardData`, `$.cardData.license`, `$.cardData.task_categories`, `$.cardData.task_categories[]`, `$.cardData.language`, `$.cardData.language[]`, `$.cardData.pretty_name`, `$.cardData.size_categories`, `$.cardData.size_categories[]`, `$.siblings`, `$.siblings[]`, `$.siblings[].rfilename`, `$.createdAt`, `$.usedStorage`

### `data/real_world/raw_metadata/hf_api/anakin_blobs.json` (DS-005; 35 fields)
`$`, `$._id`, `$.id`, `$.author`, `$.sha`, `$.lastModified`, `$.private`, `$.gated`, `$.disabled`, `$.tags`, `$.tags[]`, `$.citation`, `$.description`, `$.downloads`, `$.likes`, `$.cardData`, `$.cardData.license`, `$.cardData.task_categories`, `$.cardData.task_categories[]`, `$.cardData.language`, `$.cardData.language[]`, `$.cardData.pretty_name`, `$.cardData.size_categories`, `$.cardData.size_categories[]`, `$.siblings`, `$.siblings[]`, `$.siblings[].rfilename`, `$.siblings[].blobId`, `$.siblings[].size`, `$.siblings[].lfs`, `$.siblings[].lfs.sha256`, `$.siblings[].lfs.size`, `$.siblings[].lfs.pointerSize`, `$.createdAt`, `$.usedStorage`

### `data/real_world/raw_metadata/hf_api/anakin_metadata.csv` (DS-005; 9 fields)
`video-id`, `start-time`, `end-time`, `url`, `has-masks`, `task`, `manipulation-type`, `editor-id`, `full-available`

### `data/real_world/raw_metadata/hf_api/anakin_selected_subset.csv` (DS-005; 9 fields)
`video-id`, `start-time`, `end-time`, `url`, `has-masks`, `task`, `manipulation-type`, `editor-id`, `full-available`

### `data/real_world/raw_metadata/invid_fivr200k/extracted/annotation.json` (DS-009; 10 fields)
`$`, `$.<key>`, `$.<key>.CS`, `$.<key>.CS[]`, `$.<key>.ND`, `$.<key>.ND[]`, `$.<key>.DS`, `$.<key>.DS[]`, `$.<key>.IS`, `$.<key>.IS[]`

### `data/real_world/raw_metadata/invid_fivr200k/extracted/events.json` (DS-009; 11 fields)
`$`, `$[]`, `$[].headline`, `$[].text`, `$[].text[]`, `$[].youtube`, `$[].youtube[]`, `$[].topic`, `$[].href`, `$[].href[]`, `$[].date`

### `data/real_world/raw_metadata/invid_fivr200k/extracted/youtube_ids.txt` (DS-009; 1 fields)
`youtube_ids.txt`

### `data/real_world/raw_metadata/invid_fvc_2018/extracted/FVC.csv` (DS-006; 3 fields)
`cascade_id`, `video_url`, `label`

### `data/real_world/raw_metadata/invid_fvc_2018/extracted/FVC_dup.csv` (DS-006; 3 fields)
`cascade_id`, `video_url`, `label`

### `data/real_world/raw_metadata/invid_fvc_2018/extracted/FVC_text_queries.csv` (DS-006; 21 fields)
`cascade_id`, `video_url`, `label`, `event_title`, `french`, `spanish`, `russian`, `arabic`, `(unnamed trailing field 9)`, `(unnamed trailing field 10)`, `(unnamed trailing field 11)`, `(unnamed trailing field 12)`, `(unnamed trailing field 13)`, `(unnamed trailing field 14)`, `(unnamed trailing field 15)`, `(unnamed trailing field 16)`, `(unnamed trailing field 17)`, `(unnamed trailing field 18)`, `(unnamed trailing field 19)`, `(unnamed trailing field 20)`, `(unnamed trailing field 21)`

### `data/real_world/raw_metadata/invid_fvc_v1/extracted/Fake Video Corpus/fake_video_corpus.tsv` (DS-008; 6 fields)
`InVID_id`, `Link`, `Title`, `Comments`, `Discussed`, `Appeared`

### `data/real_world/raw_metadata/invid_fvc_v2/extracted/Fake Video Corpus v2.0/fake-video-corpus - fake-videos.tsv` (DS-007; 8 fields)
`InVID_id`, `Link`, `Title`, `Type of Manipulation`, `Comments`, `Discussed`, `Appeared`, `Timestamp`

### `data/real_world/raw_metadata/invid_fvc_v2/extracted/Fake Video Corpus v2.0/fake-video-corpus - real-videos.tsv` (DS-007; 8 fields)
`InVID_id`, `Link`, `Title`, `Comments`, `Channel`, `Official channel`, `Subscriptions`, `Description`

### `data/real_world/raw_metadata/vcsl/label_file_uuid_total.json` (DS-010; 4 fields)
`$`, `$.<key>`, `$.<key>[]`, `$.<key>[][]`

### `data/real_world/raw_metadata/vcsl/pair_file_test.csv` (DS-010; 2 fields)
`query_id`, `reference_id`

### `data/real_world/raw_metadata/vcsl/pair_file_train.csv` (DS-010; 2 fields)
`query_id`, `reference_id`

### `data/real_world/raw_metadata/vcsl/pair_file_val.csv` (DS-010; 2 fields)
`query_id`, `reference_id`

### `data/real_world/raw_metadata/vcsl/split_meta_pairs.json` (DS-010; 68 fields)
`$`, `$.train`, `$.train.<key>`, `$.train.<key>[]`, `$.val`, `$.val.<key>`, `$.val.<key>[]`, `$.test`, `$.test.4f35a9a73d354cac8653eda43ccf8d8e`, `$.test.4f35a9a73d354cac8653eda43ccf8d8e[]`, `$.test.88a654aa1cc84ad2b9703d0a5521e43f`, `$.test.88a654aa1cc84ad2b9703d0a5521e43f[]`, `$.test.a372bb16d435449d8c089fcdaaf90ae4`, `$.test.a372bb16d435449d8c089fcdaaf90ae4[]`, `$.test.f2998a313d9c4eadb1723fef854f9614`, `$.test.f2998a313d9c4eadb1723fef854f9614[]`, `$.test.d71408e317c64ce9bd3fd1139e3d5c0c`, `$.test.d71408e317c64ce9bd3fd1139e3d5c0c[]`, `$.test.4bfb654708444cc48ddda9c4de532aab`, `$.test.4bfb654708444cc48ddda9c4de532aab[]`, `$.test.166195baa824427a8d82a285c56adc00`, `$.test.166195baa824427a8d82a285c56adc00[]`, `$.test.ac92d0ea6e11418788887bf8b2df38b3`, `$.test.ac92d0ea6e11418788887bf8b2df38b3[]`, `$.test.ff79943ea3cd44588f4da316a29a8e63`, `$.test.ff79943ea3cd44588f4da316a29a8e63[]`, `$.test.05cb0d3087284ae9970a999baf6cb48a`, `$.test.05cb0d3087284ae9970a999baf6cb48a[]`, `$.test.71b46673cae14e238ccebb966ba7fd86`, `$.test.71b46673cae14e238ccebb966ba7fd86[]`, `$.test.b6c84b3f8b1e4c3280d4634c745e516c`, `$.test.b6c84b3f8b1e4c3280d4634c745e516c[]`, `$.test.78cb6c2d559c4de9a605042afa4d2bcb`, `$.test.78cb6c2d559c4de9a605042afa4d2bcb[]`, `$.test.7133109c1db64ad5b3c726df4462b470`, `$.test.7133109c1db64ad5b3c726df4462b470[]`, `$.test.88200e0f267d414aaadaf2bcd6e6ecfd`, `$.test.88200e0f267d414aaadaf2bcd6e6ecfd[]`, `$.test.dd44c4be9fdc4c95bdf075e7e756294e`, `$.test.dd44c4be9fdc4c95bdf075e7e756294e[]`, `$.test.06d224d87ea14fa5aec57903e8be37a0`, `$.test.06d224d87ea14fa5aec57903e8be37a0[]`, `$.test.d54a1f1d31a94f5c92496b22bc6dc4b4`, `$.test.d54a1f1d31a94f5c92496b22bc6dc4b4[]`, `$.test.e45b9eec5ea54e00a2d6e6689cd5fe92`, `$.test.e45b9eec5ea54e00a2d6e6689cd5fe92[]`, `$.test.aa2783f15e994ccc853f85460ad0ad20`, `$.test.aa2783f15e994ccc853f85460ad0ad20[]`, `$.test.2d500266205d4adc8638d2fea37a00b7`, `$.test.2d500266205d4adc8638d2fea37a00b7[]`, `$.test.0ed7c63b71e446baaa27e351133f5726`, `$.test.0ed7c63b71e446baaa27e351133f5726[]`, `$.test.574f2f0aac6749999fdfb41e630c1d51`, `$.test.574f2f0aac6749999fdfb41e630c1d51[]`, `$.test.146c67ab895744e6b6b54dabeea4b64f`, `$.test.146c67ab895744e6b6b54dabeea4b64f[]`, `$.test.ecfe5a8b0cd54cb8b0e51da72dca9f1e`, `$.test.ecfe5a8b0cd54cb8b0e51da72dca9f1e[]`, `$.test.029d0980e5e04c75b6defd03070f251f`, `$.test.029d0980e5e04c75b6defd03070f251f[]`, … (+8 more)

### `data/real_world/raw_metadata/vcsl/video_categories.json` (DS-010; 23 fields)
`$`, `$.variety show`, `$.variety show[]`, `$.games`, `$.games[]`, `$.music videos`, `$.music videos[]`, `$.news`, `$.news[]`, `$.sports`, `$.sports[]`, `$.daily life`, `$.daily life[]`, `$.TV series`, `$.TV series[]`, `$.kichiku`, `$.kichiku[]`, `$.advertisement`, `$.advertisement[]`, `$.animation`, `$.animation[]`, `$.movies`, `$.movies[]`

### `data/real_world/raw_metadata/vcsl/videos_url_uuid.csv` (DS-010; 2 fields)
`url`, `uuid`

### `data/real_world/raw_metadata/zenodo_api/*.json` (DS-012; 128 fields)
`$`, `$.created`, `$.modified`, `$.id`, `$.conceptrecid`, `$.doi`, `$.conceptdoi`, `$.doi_url`, `$.metadata`, `$.metadata.title`, `$.metadata.doi`, `$.metadata.publication_date`, `$.metadata.description`, `$.metadata.access_right`, `$.metadata.creators`, `$.metadata.creators[]`, `$.metadata.creators[].name`, `$.metadata.creators[].affiliation`, `$.metadata.keywords`, `$.metadata.keywords[]`, `$.metadata.version`, `$.metadata.references`, `$.metadata.references[]`, `$.metadata.language`, `$.metadata.resource_type`, `$.metadata.resource_type.title`, `$.metadata.resource_type.type`, `$.metadata.license`, `$.metadata.license.id`, `$.metadata.grants`, `$.metadata.grants[]`, `$.metadata.grants[].code`, `$.metadata.grants[].internal_id`, `$.metadata.grants[].funder`, `$.metadata.grants[].funder.name`, `$.metadata.grants[].funder.doi`, `$.metadata.grants[].funder.acronym`, `$.metadata.grants[].title`, `$.metadata.grants[].acronym`, `$.metadata.grants[].program`, `$.metadata.grants[].url`, `$.metadata.communities`, `$.metadata.communities[]`, `$.metadata.communities[].id`, `$.metadata.relations`, `$.metadata.relations.version`, `$.metadata.relations.version[]`, `$.metadata.relations.version[].index`, `$.metadata.relations.version[].is_last`, `$.metadata.relations.version[].parent`, `$.metadata.relations.version[].parent.pid_type`, `$.metadata.relations.version[].parent.pid_value`, `$.title`, `$.links`, `$.links.self`, `$.links.self_html`, `$.links.preview_html`, `$.links.doi`, `$.links.self_doi`, `$.links.self_doi_html`, … (+68 more)

### `data/reports/acceptance_checks.json` (DS-033; 4 fields)
`$`, `$.<key>`, `$.<key>.ok`, `$.<key>.evidence`

### `docs/datasets/ORVEX_REQUIREMENT_COVERAGE_MATRIX.csv` (DS-034; 10 fields)
`requirement_id`, `pdf_reference`, `requirement`, `modules`, `phase`, `artifacts`, `checks`, `status`, `evidence`, `limitation_or_blocker`

### `docs/datasets/column_lineage.csv` (DS-034; 13 fields)
`table`, `column`, `source_datasets`, `type`, `nullable`, `origin_code`, `origin_meaning`, `source_field_or_rule`, `present_in_source_dataset`, `description`, `allowed_values`, `validation`, `rationale`

### `docs/datasets/necessity_audit/dataset_inventory.csv` (DS-034; 9 fields)
`kind`, `id`, `name`, `classification`, `status`, `verification`, `records_local`, `local_bytes`, `reason`

### `docs/datasets/necessity_audit/dhash_baseline_results.json` (DS-034; 89 fields)
`$`, `$.threshold_fixed_a_priori`, `$.pairs_scored`, `$.latency_ms_per_pair`, `$.auc_train`, `$.auc_val`, `$.auc_test`, `$.test_negatives_by_hardness`, `$.test_negatives_by_hardness.easy`, `$.test_negatives_by_hardness.hard`, `$.auc_test_hard_negatives_only`, `$.auc_test_easy_negatives_only`, `$.auc_test_without_heldout_lineage`, `$.auc_test_heldout_lineage_pos_vs_all_neg`, `$.detection_rate_threshold`, `$.detection_rate_threshold.audio_source_only_not_visual_derivation`, `$.detection_rate_threshold.direct_derivation`, `$.detection_rate_threshold.edited_version`, `$.detection_rate_threshold.indirect_derivation`, `$.detection_rate_threshold.same_family_other`, `$.detection_rate_threshold.sibling_same_parent`, `$.detection_rate_threshold.unrelated_distinct_source`, `$.direct_derivation_detection_by_transformation`, `$.direct_derivation_detection_by_transformation.audio_mute`, `$.direct_derivation_detection_by_transformation.audio_mute.n`, `$.direct_derivation_detection_by_transformation.audio_mute.detected`, `$.direct_derivation_detection_by_transformation.audio_mute.audio_identical`, `$.direct_derivation_detection_by_transformation.audio_noise_mix`, `$.direct_derivation_detection_by_transformation.audio_noise_mix.n`, `$.direct_derivation_detection_by_transformation.audio_noise_mix.detected`, `$.direct_derivation_detection_by_transformation.audio_noise_mix.audio_identical`, `$.direct_derivation_detection_by_transformation.audio_replace`, `$.direct_derivation_detection_by_transformation.audio_replace.n`, `$.direct_derivation_detection_by_transformation.audio_replace.detected`, `$.direct_derivation_detection_by_transformation.audio_replace.audio_identical`, `$.direct_derivation_detection_by_transformation.caption_burn_in`, `$.direct_derivation_detection_by_transformation.caption_burn_in.n`, `$.direct_derivation_detection_by_transformation.caption_burn_in.detected`, `$.direct_derivation_detection_by_transformation.caption_burn_in.audio_identical`, `$.direct_derivation_detection_by_transformation.crop_center`, `$.direct_derivation_detection_by_transformation.crop_center.n`, `$.direct_derivation_detection_by_transformation.crop_center.detected`, `$.direct_derivation_detection_by_transformation.crop_center.audio_identical`, `$.direct_derivation_detection_by_transformation.mirror_color_shift`, `$.direct_derivation_detection_by_transformation.mirror_color_shift.n`, `$.direct_derivation_detection_by_transformation.mirror_color_shift.detected`, `$.direct_derivation_detection_by_transformation.mirror_color_shift.audio_identical`, `$.direct_derivation_detection_by_transformation.recompress_low`, `$.direct_derivation_detection_by_transformation.recompress_low.n`, `$.direct_derivation_detection_by_transformation.recompress_low.detected`, `$.direct_derivation_detection_by_transformation.recompress_low.audio_identical`, `$.direct_derivation_detection_by_transformation.reencode_hq`, `$.direct_derivation_detection_by_transformation.reencode_hq.n`, `$.direct_derivation_detection_by_transformation.reencode_hq.detected`, `$.direct_derivation_detection_by_transformation.reencode_hq.audio_identical`, `$.direct_derivation_detection_by_transformation.reupload_sim`, `$.direct_derivation_detection_by_transformation.reupload_sim.n`, `$.direct_derivation_detection_by_transformation.reupload_sim.detected`, `$.direct_derivation_detection_by_transformation.reupload_sim.audio_identical`, `$.direct_derivation_detection_by_transformation.speed_change`, … (+29 more)

### `docs/datasets/necessity_audit/requirement_data_decision_table.csv` (DS-034; 12 fields)
`requirement_id`, `required_capability`, `existing_support`, `evidence_it_works`, `gap`, `gap_type`, `additional_data_necessary`, `recommended_source_or_transformation`, `permission_constraints`, `est_additional_storage_gb`, `acceptance_test`, `status_now`

### `docs/datasets/necessity_audit/variant_independent_validation.json` (DS-034; 17 fields)
`$`, `$.passed_variants`, `$.readable_by_independent_ffprobe`, `$.duration_matches_registry`, `$.carries_controlled_variant_metadata_tag`, `$.parent_chain_complete`, `$.roots_eligible`, `$.audio_variants`, `$.audio_donor_documented_real_eligible`, `$.caption_variants`, `$.caption_variants_with_real_source_text`, `$.run_log_return0_and_passed`, `$.tool_params_run_recorded`, `$.failed_variants`, `$.failed_excluded_and_no_file`, `$.leakage_check`, `$.heldout_check`

### `docs/datasets/schema_contract.json` (DS-034; 208 fields)
`$`, `$.origin_codes`, `$.origin_codes.a`, `$.origin_codes.b`, `$.origin_codes.c`, `$.origin_codes.d`, `$.origin_codes.e`, `$.origin_codes.f`, `$.vocabularies`, `$.vocabularies.record_origin`, `$.vocabularies.record_origin[]`, `$.vocabularies.media_origin`, `$.vocabularies.media_origin[]`, `$.vocabularies.transformation_status`, `$.vocabularies.transformation_status[]`, `$.vocabularies.access_status`, `$.vocabularies.access_status[]`, `$.vocabularies.direction_status`, `$.vocabularies.direction_status[]`, `$.vocabularies.label_status`, `$.vocabularies.label_status[]`, `$.vocabularies.inclusion_status`, `$.vocabularies.inclusion_status[]`, `$.vocabularies.split`, `$.vocabularies.split[]`, `$.vocabularies.validation_status`, `$.vocabularies.validation_status[]`, `$.tables`, `$.tables.source_registry`, `$.tables.source_registry.path`, `$.tables.source_registry.purpose`, `$.tables.source_registry.phase`, `$.tables.source_registry.columns`, `$.tables.source_registry.columns[]`, `$.tables.source_registry.columns[].name`, `$.tables.source_registry.columns[].type`, `$.tables.source_registry.columns[].nullable`, `$.tables.source_registry.columns[].origin`, `$.tables.source_registry.columns[].lineage`, `$.tables.source_registry.columns[].description`, `$.tables.real_world_media_master`, `$.tables.real_world_media_master.path`, `$.tables.real_world_media_master.purpose`, `$.tables.real_world_media_master.phase`, `$.tables.real_world_media_master.columns`, `$.tables.real_world_media_master.columns[]`, `$.tables.real_world_media_master.columns[].name`, `$.tables.real_world_media_master.columns[].type`, `$.tables.real_world_media_master.columns[].nullable`, `$.tables.real_world_media_master.columns[].origin`, `$.tables.real_world_media_master.columns[].lineage`, `$.tables.real_world_media_master.columns[].description`, `$.tables.controlled_variant_registry`, `$.tables.controlled_variant_registry.path`, `$.tables.controlled_variant_registry.purpose`, `$.tables.controlled_variant_registry.phase`, `$.tables.controlled_variant_registry.columns`, `$.tables.controlled_variant_registry.columns[]`, `$.tables.controlled_variant_registry.columns[].name`, `$.tables.controlled_variant_registry.columns[].type`, … (+148 more)
