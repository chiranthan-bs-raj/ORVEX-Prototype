# -*- coding: utf-8 -*-
"""ORVEX dataset schema contract (single source of truth for tables, data dictionary, column lineage and tests).
Origin codes: a=copied from named source field | b=normalized/renamed from source field | c=derived by deterministic rule from named fields |
d=computed from media by named tool | e=human-annotated with evidence | f=ORVEX bookkeeping/administrative."""
S, I, F, B, DT, J = "str", "int", "float", "bool", "datetime", "json"
TABLES = {}
def T(name, path, purpose, phase, cols): TABLES[name] = dict(path=path, purpose=purpose, phase=phase, cols=cols)

VOC = dict(
 record_origin=["real_world_source_record", "orvex_normalized_record", "orvex_controlled_variant_record", "orvex_computed_record"],
 media_origin=["naturally_collected_real_world", "real_world_human_edited_dataset", "controlled_variant", "not_applicable_metadata_only"],
 transformation_status=["none_source_unmodified", "controlled_transformation_applied", "controlled_transformation_failed", "not_applicable"],
 access_status=["downloaded_authorized", "metadata_only", "not_found", "private_or_deleted", "blocked_by_terms", "access_not_available", "retry_pending"],
 direction_status=["directed_supported_by_source", "directed_controlled_transformation", "unknown_direction", "non_directional"],
 label_status=["source_ground_truth", "controlled_ground_truth", "uncertain", "unknown", "not_assessed"],
 inclusion_status=["included_media_and_metadata", "included_metadata_only", "included_selected_subset", "excluded_license", "excluded_not_real_world_for_scope",
                   "excluded_duplicate_version", "excluded_inaccessible", "excluded_over_budget", "research_lead_unverified", "legal_review_required"],
 split=["train", "val", "test", "excluded"],
 validation_status=["passed", "failed", "not_run"],
)

# ---------------------------------------------------------------- 1 source registry
T("source_registry", "data/manifests/source_registry.csv", "Every dataset/source considered, with official source, terms, access, size and decision.", "both", [
 ("source_dataset_id", S, 0, "f", "ORVEX id (RW-xx)", "Stable ORVEX id of the real-world source dataset."),
 ("title", S, 0, "a", "official dataset page/paper title", "Full title."),
 ("creator", S, 1, "a", "official record creators", "Creators/authors."),
 ("release_version", S, 1, "a", "official release/version", "Release or version label."),
 ("official_url", S, 1, "a", "official landing page", "Official landing URL."),
 ("download_url", S, 1, "a", "official download/repository URL", "Where files come from."),
 ("paper_doi_or_url", S, 1, "a", "paper/DOI", "Associated paper."),
 ("accessed_date", S, 0, "f", "date of verification", "Date the page/API was accessed."),
 ("license_terms", S, 1, "a", "licence field on official page", "Licence/terms exactly as stated (or 'not stated')."),
 ("license_evidence_url", S, 1, "a", "URL where the licence was read", "Evidence link."),
 ("bytes_or_urls_provided", S, 0, "a", "official description", "media_bytes / metadata_urls_only / mixed / unverified."),
 ("derivative_use_status", S, 0, "c", "licence text", "permitted / not_stated / not_permitted / unverified."),
 ("training_use_status", S, 0, "c", "licence text", "permitted / not_stated / unverified."),
 ("redistribution_status", S, 0, "c", "licence text", "Whether files may be redistributed (with conditions)."),
 ("real_world_eligibility", S, 0, "e", "analyst decision with evidence", "Eligible / not eligible for the strict real-world collection and why."),
 ("native_task", S, 1, "a", "official description", "Task the source was built for."),
 ("native_labels", S, 1, "a", "official description", "Native labels/annotations."),
 ("media_origin_characterization", S, 0, "e", "analyst decision", "How the media came to exist (user-uploaded, circulated, professionally edited...)."),
 ("release_size_bytes", I, 1, "a", "official file sizes", "Total official release size when known."),
 ("planned_download_bytes", I, 0, "f", "selection plan", "Budgeted bytes."),
 ("actual_local_bytes", I, 0, "d", "du of local folder", "Measured local bytes."),
 ("record_count_local", I, 0, "d", "row count of local files", "Records held locally."),
 ("auth_required", S, 0, "a", "official access docs", "none / account / agreement / API."),
 ("overlap_with", S, 1, "e", "analyst comparison", "Other sources it overlaps."),
 ("inclusion_status", S, 0, "f", "controlled vocabulary", "Decision."),
 ("inclusion_reason", S, 0, "e", "analyst decision", "Why."),
 ("tasks_supported", S, 1, "f", "mapping to ORVEX modules", "ORVEX modules/tasks supported."),
 ("evidence_links", S, 1, "f", "URLs consulted", "Pipe-separated URLs."),
 ("limitations", S, 1, "e", "analyst notes", "Known limitations."),
 ("verification_level", S, 0, "f", "see policy", "verified_official_page / verified_api / research_lead_unverified."),
])

# ---------------------------------------------------------------- 2 real-world media master
T("real_world_media_master", "data/derived/tables/real_world_media_master.csv",
  "Normalized master of every real-world media record (downloaded or metadata-only). Controlled variants are NOT here.", "both", [
 ("media_id", S, 0, "f", "ORVEX id", "Stable internal id (RW-<src>-...)."),
 ("source_dataset_id", S, 0, "f", "source_registry", "Source dataset."),
 ("release_version", S, 1, "a", "source release", "Release/version of source."),
 ("native_record_id", S, 1, "a", "FVC cascade_id / FIVR query+id / VCSL uuid / ANAKIN video-id / Commons pageid", "Native id of the record."),
 ("native_media_id", S, 1, "a", "platform video id or file title", "Native media id."),
 ("platform", S, 1, "b", "host of source URL / 'wikimedia_commons' / 'vimeo'", "Platform normalized to lowercase name."),
 ("platform_media_id", S, 1, "c", "parsed from URL", "Platform video id."),
 ("source_url", S, 1, "a", "FVC video_url / VCSL url / ANAKIN url / Commons descriptionurl", "Source URL as published."),
 ("canonical_url", S, 1, "c", "normalized source_url", "Canonical URL (scheme/host lowercased, tracking removed)."),
 ("title", S, 1, "a", "Commons title / ANAKIN task text", "Title if the source has one."),
 ("description_caption", S, 1, "a", "Commons ImageDescription / ANAKIN task", "Caption/description."),
 ("publisher_account_id", S, 1, "b", "Commons uploader username (public) ", "Publisher account as published; pseudonymise in reports."),
 ("event_or_cascade_id", S, 1, "a", "FVC cascade_id / FIVR event id / ANAKIN video-id", "Group the record belongs to."),
 ("published_time_utc", DT, 1, "b", "Commons upload timestamp", "Publish time (only when the source provides one)."),
 ("observed_time_utc", DT, 1, "f", "n/a", "Observation time if provided by source (rare)."),
 ("collected_time_utc", DT, 0, "f", "ORVEX run", "When ORVEX collected/registered the record."),
 ("time_precision", S, 1, "f", "n/a", "second / unknown."),
 ("duration_s", F, 1, "d", "ffprobe", "Duration (downloaded media only)."),
 ("width", I, 1, "d", "ffprobe", "Width."), ("height", I, 1, "d", "ffprobe", "Height."), ("fps", F, 1, "d", "ffprobe", "Frame rate."),
 ("video_codec", S, 1, "d", "ffprobe", "Video codec."), ("audio_codec", S, 1, "d", "ffprobe", "Audio codec."),
 ("has_audio", B, 1, "d", "ffprobe", "Audio stream present."), ("container", S, 1, "d", "ffprobe", "Container."),
 ("file_bytes", I, 1, "d", "os.stat", "File size."), ("local_path", S, 1, "f", "ORVEX", "Relative path of local file."),
 ("sha256", S, 1, "d", "hashlib SHA-256", "File hash (locally computed)."),
 ("access_status", S, 0, "f", "VOC.access_status", "Access status."), ("playable_status", S, 1, "d", "ffmpeg decode check", "playable / unplayable / not_checked."),
 ("rights_status", S, 0, "c", "licence", "Rights decision for storage/processing."),
 ("license", S, 1, "a", "Commons LicenseShortName / dataset licence", "Licence."), ("license_url", S, 1, "a", "Commons LicenseUrl", "Licence URL."),
 ("attribution", S, 1, "a", "Commons Artist/Credit / dataset citation", "Attribution string."),
 ("record_origin", S, 0, "f", "VOC.record_origin", "Origin of the record."), ("media_origin", S, 0, "f", "VOC.media_origin", "Origin of the media."),
 ("native_authenticity_label", S, 1, "a", "FVC label (fake/real)", "Native label exactly as published."),
 ("native_misleading_label", S, 1, "a", "FVC label", "Native label (same field) kept separately."),
 ("native_manipulation_type", S, 1, "a", "ANAKIN manipulation-type", "Native manipulation type."),
 ("normalized_authenticity_status", S, 0, "c", "mapping rule in policy", "unknown unless the native label states it; 'fake' in FVC = debunked, NOT AI-generated."),
 ("normalized_misleading_status", S, 0, "c", "mapping rule", "debunked_misleading / verified_not_misleading / not_assessed."),
 ("coordination_status", S, 0, "f", "ORVEX policy", "not_assessed for every record: no independent account/time coordination evidence exists locally."),
 ("evidence_id", S, 1, "f", "evidence_ledger", "Evidence record backing the source annotation / licence of this record."),
 ("perceptual_hash_ref", S, 1, "d", "feature_manifest visual_dhash24", "Reference to the computed 24-frame dHash features (local media only)."),
 ("annotation_status", S, 0, "f", "ORVEX", "source_annotation / none."),
 ("qc_flags", S, 1, "c", "ORVEX QC rules", "Flags (too_short, no_audio, decode_errors...)."),
 ("duplicate_of_media_id", S, 1, "c", "duplicate_map", "Canonical media id if this is a duplicate."),
 ("usable_for_variants", B, 0, "c", "rights + QC rules", "Eligible as source for controlled variants."),
 ("missingness_note", S, 1, "f", "ORVEX", "Why fields are null."),
])

# ---------------------------------------------------------------- 3 controlled variants
T("controlled_variant_registry", "data/derived/tables/controlled_variant_registry.csv",
  "Every controlled variant rendered by ORVEX from eligible real-world media. Never mixed with naturally collected media.", "phase1", [
 ("variant_media_id", S, 0, "f", "ORVEX id", "Id of the created video (CV-...)."),
 ("direct_parent_media_id", S, 0, "f", "ORVEX transformation plan", "Immediate parent (real source or earlier variant)."),
 ("root_source_media_id", S, 0, "f", "media master", "Real-world root source."),
 ("ancestor_chain", S, 0, "c", "parent links", "Pipe-separated ancestors up to the root."),
 ("video_source_media_id", S, 0, "f", "media master", "Real-world source of the picture track."),
 ("audio_source_media_id", S, 1, "f", "media master", "Real-world source of replaced/mixed audio."),
 ("caption_text_source_media_id", S, 1, "f", "media master", "Real-world record the caption text came from."),
 ("caption_text", S, 1, "b", "title of the caption-source record (ASCII-normalised)", "Caption burned in."),
 ("caption_text_origin_field", S, 1, "f", "n/a", "Field of the source record used (commons_title)."),
 ("transformation_id", S, 0, "f", "catalogue", "T01-T14."), ("transformation_name", S, 0, "f", "catalogue", "Name."),
 ("transformation_family", S, 0, "f", "catalogue", "Family."), ("parameters_json", J, 0, "f", "ORVEX", "Exact parameters."),
 ("tool_name", S, 0, "f", "ORVEX", "ffmpeg."), ("tool_version", S, 0, "d", "ffmpeg -version", "Tool version."),
 ("run_id", S, 0, "f", "ORVEX", "Run id."), ("seed", S, 1, "f", "ORVEX", "Deterministic selection key."),
 ("created_utc", DT, 0, "f", "ORVEX", "Creation time."), ("local_path", S, 1, "f", "ORVEX", "Path of the created file (blank for failed variants: no file retained)."),
 ("sha256", S, 1, "d", "hashlib", "Output hash (blank for failed variants)."), ("bytes", I, 0, "d", "os.stat", "Output size."),
 ("duration_s", F, 1, "d", "ffprobe", "Output duration."), ("width", I, 1, "d", "ffprobe", "Width."), ("height", I, 1, "d", "ffprobe", "Height."),
 ("fps", F, 1, "d", "ffprobe", "fps."), ("has_audio", B, 1, "d", "ffprobe", "Audio present."),
 ("generation_depth", I, 0, "c", "chain length", "Edits from the real root."), ("chain_id", S, 1, "f", "catalogue", "Chain id."),
 ("permission_basis", S, 0, "c", "root licence", "Why the transformation is permitted."),
 ("root_license", S, 0, "a", "media master license", "Licence of root."),
 ("validation_status", S, 0, "d", "ffprobe checks", "passed/failed/not_run."), ("validation_checks_json", J, 0, "d", "ffprobe", "Checks and results."),
 ("failure_reason", S, 1, "f", "ORVEX", "Reason if failed."),
 ("media_origin", S, 0, "f", "VOC", "Always controlled_variant."), ("record_origin", S, 0, "f", "VOC", "Always orvex_controlled_variant_record."),
 ("transformation_status", S, 0, "f", "VOC", "controlled_transformation_applied / failed."),
 ("usable_for_training", B, 0, "c", "validation + split + held-out rule", "True only if passed, train split and no held-out transform in lineage."),
 ("source_split", S, 0, "c", "split_manifest", "Split of the root source family."),
])

# ---------------------------------------------------------------- 4 relationship edges
T("media_relationship_edges", "data/derived/tables/media_relationship_edges.csv",
  "Relationship edges: source-provided native relations (kept with original label) and controlled-transformation lineage.", "both", [
 ("relationship_id", S, 0, "f", "ORVEX", "Edge id."), ("source_dataset_id", S, 0, "f", "source_registry", "Where the relation comes from (or ORVEX-CTRL)."),
 ("relation_scope", S, 0, "f", "ORVEX", "real_native / controlled_lineage."), ("evidence_id", S, 0, "f", "evidence_ledger", "Evidence record."),
 ("media_a_id", S, 0, "f", "media master/variant registry", "First item."), ("media_b_id", S, 0, "f", "media master/variant registry", "Second item."),
 ("native_media_a_id", S, 1, "a", "native ids", "Native id of A."), ("native_media_b_id", S, 1, "a", "native ids", "Native id of B."),
 ("native_label", S, 1, "a", "FIVR ND/DS/CS/IS; VCSL label_file; FVC label; ANAKIN manipulation-type", "Label exactly as published."),
 ("normalized_relation_type", S, 0, "c", "mapping table", "e.g. near_duplicate, partial_temporal_copy, same_scene_not_copy, same_incident_not_copy, edited_version, controlled_*."),
 ("direction_status", S, 0, "c", "VOC", "Direction support."),
 ("parent_media_id", S, 1, "c", "only when direction supported", "Parent."), ("child_media_id", S, 1, "c", "only when direction supported", "Child."),
 ("a_segment_start_s", F, 1, "a", "VCSL label_file", "Copied segment start in A."), ("a_segment_end_s", F, 1, "a", "VCSL label_file", "End in A."),
 ("b_segment_start_s", F, 1, "a", "VCSL label_file", "Start in B."), ("b_segment_end_s", F, 1, "a", "VCSL label_file", "End in B."),
 ("overlap_ratio", F, 1, "c", "segment durations / duration", "Copied-duration ratio when measurable."),
 ("transformation_type", S, 1, "f", "catalogue / ANAKIN manipulation-type", "Transformation type."),
 ("label_source", S, 0, "f", "ORVEX", "source_annotation / controlled_transformation_log."),
 ("label_status", S, 0, "f", "VOC", "Label status."), ("evidence_status", S, 0, "f", "policy", "kind of evidence behind the label: source_annotation / controlled_transformation_log (separate from label status)."), ("confidence_status", S, 0, "f", "policy", "No numeric confidence: source_ground_truth / controlled_ground_truth."),
 ("reviewer", S, 1, "e", "human reviewer", "Reviewer id (none yet)."), ("method_version", S, 0, "f", "ORVEX", "Script version."),
 ("created_utc", DT, 0, "f", "ORVEX", "Creation time."), ("media_available_locally", B, 0, "d", "file exists", "Both media bytes present locally."),
 ("conflict_flag", B, 0, "c", "cross-source check", "Conflicting labels between sources."), ("notes", S, 1, "f", "ORVEX", "Notes."),
])

# ---------------------------------------------------------------- 5 platform observations
T("platform_observations", "data/derived/tables/platform_observations.csv",
  "Real posts/observations of media on platforms as provided by the sources (no invented posts).", "phase2", [
 ("observation_id", S, 0, "f", "ORVEX", "Id."), ("media_id", S, 0, "f", "media master", "Media observed."),
 ("observation_type", S, 0, "f", "ORVEX", "upload / publish / removal / share_reference / cascade_member."), ("coordination_status", S, 0, "f", "policy", "not_assessed: no independent coordination evidence."),
 ("platform", S, 1, "b", "URL host", "Platform."), ("platform_post_id", S, 1, "c", "parsed from URL", "Post/video id."),
 ("post_url", S, 1, "a", "source URL", "URL."), ("account_id_pseudonym", S, 1, "c", "SHA-256 prefix of public account name", "Pseudonymised account id (policy)."),
 ("account_id_source_field", S, 1, "f", "n/a", "Source field used (commons uploader) or null."),
 ("publish_time_utc", DT, 1, "b", "Commons upload timestamp", "Publish time."), ("observation_time_utc", DT, 1, "f", "n/a", "Observation time."),
 ("time_precision", S, 1, "f", "n/a", "second / unknown."), ("caption_text", S, 1, "a", "Commons description", "Caption."),
 ("hashtags", S, 1, "f", "n/a", "Not provided."), ("engagement_refs", S, 1, "a", "Commons global usage count", "Permitted engagement/reuse reference."),
 ("metadata_source", S, 0, "f", "source_registry", "Source dataset."), ("collection_method", S, 0, "f", "ORVEX", "official_api / dataset_file."),
 ("order_in_cascade", I, 1, "c", "row order inside FVC cascade", "Temporal order inside cascade as stated by the authors (not a timestamp)."),
 ("cascade_id", S, 1, "a", "FVC cascade_id", "Cascade id."), ("access_status", S, 0, "f", "VOC", "Access."), ("evidence_id", S, 0, "f", "evidence_ledger", "Evidence."),
 ("limitations", S, 1, "f", "ORVEX", "Limitations."),
])

# ---------------------------------------------------------------- 6 evidence ledger
T("evidence_ledger", "data/derived/tables/evidence_ledger.csv", "Evidence records supporting labels, relations and rights decisions.", "both", [
 ("evidence_id", S, 0, "f", "ORVEX", "Id."), ("evidence_type", S, 0, "f", "ORVEX", "source_annotation / source_metadata / controlled_transformation_log / machine_measurement / license_record."),
 ("source_dataset_id", S, 0, "f", "source_registry", "Source."), ("subject_type", S, 0, "f", "ORVEX", "media / relationship_set / variant / license."),
 ("subject_id", S, 0, "f", "ORVEX", "Subject id or set name."), ("source_url", S, 1, "a", "official URL", "URL."),
 ("source_record_ref", S, 1, "f", "file path / record key", "Where inside the source."),
 ("claim_supported", S, 0, "f", "ORVEX", "What this evidence supports."), ("claim_status", S, 0, "f", "policy", "source_asserted / measured / controlled_by_construction."),
 ("observed_fact_vs_inference", S, 0, "f", "policy", "observed_fact / source_annotation / machine_measurement / analyst_inference."),
 ("verification_method", S, 0, "f", "ORVEX", "How checked."), ("evidence_time_utc", DT, 0, "f", "ORVEX", "When evidence was recorded."),
 ("temporal_precision", S, 1, "f", "n/a", "Precision."), ("file_sha256", S, 1, "d", "hashlib", "Hash of the evidence file."),
 ("reviewer_status", S, 0, "f", "policy", "unreviewed / source_curated."), ("permission_status", S, 0, "c", "licence", "Permission."),
 ("confidence_basis", S, 0, "f", "policy", "No calibrated numeric confidence; basis stated."), ("limitations", S, 1, "f", "ORVEX", "Limitations."),
])

# ---------------------------------------------------------------- 7 feature manifest
T("feature_manifest", "data/derived/tables/feature_manifest.csv", "What features actually exist (and which are not computed).", "both", [
 ("feature_record_id", S, 0, "f", "ORVEX", "Id."), ("media_id", S, 0, "f", "media master / variants", "Media or ALL_LOCAL for aggregate rows."),
 ("feature_type", S, 0, "f", "ORVEX", "visual_dhash_24 / audio_pcm_md5_8k / audio_envelope_1s / visual_embedding / audio_embedding / ocr_text / asr_transcript / text_embedding / scene_boundaries."),
 ("extraction_status", S, 0, "d", "script result", "computed / not_computed / failed."), ("tool_name", S, 1, "f", "ORVEX", "Tool."), ("tool_version", S, 1, "d", "tool", "Version."),
 ("parameters_json", J, 1, "f", "ORVEX", "Parameters."), ("sample_timestamps", S, 1, "d", "frame indices", "Sample positions."),
 ("feature_format", S, 1, "f", "ORVEX", "Format/dimension."), ("storage_path", S, 1, "f", "ORVEX", "File holding the feature."),
 ("storage_bytes", I, 1, "d", "os.stat", "Size."), ("feature_sha256", S, 1, "d", "hashlib", "Hash."), ("extracted_utc", DT, 1, "f", "ORVEX", "Time."),
 ("error", S, 1, "f", "ORVEX", "Error."), ("permission_status", S, 0, "c", "licence", "Permission."),
])

# ---------------------------------------------------------------- 8 training pairs
T("training_pairs", "data/derived/tables/training_pairs.csv", "Model examples (related/unrelated/uncertain pairs) with local media only, split by source family.", "phase1", [
 ("example_id", S, 0, "f", "ORVEX", "Id."), ("media_a_id", S, 0, "f", "master/variants", "A."), ("media_b_id", S, 0, "f", "master/variants", "B."),
 ("relationship_id", S, 1, "f", "edges", "Edge backing the label (null for negatives)."), ("label_binary_related", I, 0, "c", "relationship_class", "1 related / 0 not related."),
 ("relationship_class", S, 0, "c", "edge types", "direct_derivation / indirect_derivation / sibling_same_parent / same_family_other / edited_version / unrelated_distinct_source."),
 ("native_label", S, 1, "a", "source label", "Native label if from a source."), ("normalized_label", S, 0, "c", "mapping", "Normalized label."),
 ("label_origin", S, 0, "f", "ORVEX", "controlled_lineage / source_annotation / negative_sampling_rule."), ("label_status", S, 0, "f", "VOC", "Status."),
 ("evidence_id", S, 1, "f", "ledger", "Evidence."), ("feature_refs", S, 1, "f", "feature_manifest", "Feature ids."),
 ("source_family_id", S, 0, "c", "root source", "Family used for splitting (A's family)."), ("event_or_cascade_group_id", S, 1, "a", "FVC/ANAKIN group", "Group."),
 ("split", S, 0, "c", "split_manifest", "train/val/test/excluded."), ("split_version", S, 0, "f", "ORVEX", "Version."),
 ("sampling_method", S, 0, "f", "ORVEX", "How the pair was chosen."), ("negative_rationale", S, 1, "f", "ORVEX", "Why a negative is credible."),
 ("hardness", S, 1, "c", "rule", "easy/medium/hard."), ("leakage_flag", B, 0, "c", "leakage test", "True if pair crosses families/splits."),
 ("exclusion_reason", S, 1, "f", "ORVEX", "Reason excluded."), ("includes_heldout_transform", B, 0, "c", "lineage", "Involves a test-only transformation."),
 ("created_utc", DT, 0, "f", "ORVEX", "Time."),
])

# ---------------------------------------------------------------- 9 campaign clusters (header only unless evidence)
T("campaign_candidate_clusters", "data/derived/tables/campaign_candidate_clusters.csv",
  "Candidate clusters for human review. EMPTY: no authorised account+time evidence is available locally (see QA report).", "phase2", [
 ("cluster_id", S, 0, "f", "ORVEX", "Id."), ("observation_ids", S, 0, "f", "observations", "Observations."), ("media_ids", S, 1, "f", "master", "Media."),
 ("account_pseudonyms", S, 1, "c", "observations", "Accounts."), ("time_window_start_utc", DT, 1, "f", "observations", "Start."), ("time_window_end_utc", DT, 1, "f", "observations", "End."),
 ("common_media_signals", S, 1, "f", "edges", "Media signals."), ("posting_pattern_signals", S, 1, "f", "observations", "Posting signals."),
 ("independent_coordination_evidence", S, 1, "f", "evidence", "Independent evidence."), ("candidate_status", S, 0, "f", "policy", "candidate_cluster / not_assessed."),
 ("reviewer", S, 1, "e", "human", "Reviewer."), ("limitations", S, 1, "f", "ORVEX", "Limitations."),
])

# ---------------------------------------------------------------- 10 transformation runs
T("transformation_run_log", "data/derived/tables/transformation_run_log.csv", "One row per transformation execution.", "phase1", [
 ("run_id", S, 0, "f", "ORVEX", "Run id."), ("variant_media_id", S, 0, "f", "variant registry", "Output."), ("input_media_ids", S, 0, "f", "ORVEX", "Inputs (video|audio donor)."),
 ("tool_name", S, 0, "f", "ORVEX", "Tool."), ("tool_version", S, 0, "d", "ffmpeg", "Version."), ("command_config", S, 0, "f", "ORVEX", "Full argument list (root path abstracted)."),
 ("parameters_json", J, 0, "f", "ORVEX", "Parameters."), ("started_utc", DT, 0, "f", "ORVEX", "Time."), ("return_code", I, 0, "d", "process", "Exit code."),
 ("output_validation_status", S, 0, "d", "ffprobe", "passed/failed."), ("output_bytes", I, 1, "d", "os.stat", "Bytes."),
 ("storage_delta_bytes", I, 1, "d", "os.stat", "Payload change."), ("error", S, 1, "f", "process", "stderr tail."),
 ("deterministic_notes", S, 1, "f", "ORVEX", "Determinism notes."), ("seed", S, 1, "f", "ORVEX", "Selection key."),
])

# ---------------------------------------------------------------- 11 access log
T("download_access_attempt_log", "data/manifests/download_access_attempt_log.csv", "Every download/access attempt.", "both", [
 ("attempt_id", S, 0, "f", "ORVEX", "Id."), ("source_dataset_id", S, 0, "f", "registry", "Source."), ("media_or_file_id", S, 1, "f", "ORVEX", "Item."),
 ("url", S, 1, "f", "ORVEX", "URL (blank for policy-skipped rows)."), ("attempt_time_utc", DT, 0, "f", "ORVEX", "Time."), ("method", S, 0, "f", "ORVEX", "http_get / api."),
 ("http_status", I, 1, "d", "response", "HTTP status."), ("result_category", S, 0, "f", "ORVEX", "ok / failed / skipped_terms / skipped_budget."),
 ("terms_decision", S, 0, "f", "policy", "Decision."), ("retry_count", I, 0, "f", "ORVEX", "Retries."), ("bytes", I, 1, "d", "response", "Bytes."),
 ("sha256", S, 1, "d", "hashlib", "Hash."), ("final_status", S, 0, "f", "VOC.access_status", "Final status."), ("note", S, 1, "f", "ORVEX", "Note."),
])

# ---------------------------------------------------------------- 12 split manifest
T("split_manifest", "data/derived/splits/split_manifest.csv", "Source-family level split assignment.", "phase1", [
 ("split_version", S, 0, "f", "ORVEX", "Version."), ("source_family_id", S, 0, "f", "master", "Root source."), ("source_dataset_id", S, 0, "f", "registry", "Dataset."),
 ("split", S, 0, "c", "hash rule", "Assigned split."), ("assignment_method", S, 0, "f", "ORVEX", "Rule."), ("seed", S, 0, "f", "ORVEX", "Seed."),
 ("domain_stratum", S, 1, "f", "search theme / manipulation type", "Stratum."), ("n_family_items", I, 0, "d", "count", "Items in family."),
 ("n_native_edges", I, 0, "d", "count", "Native edges."), ("heldout_transformations_in_family", S, 1, "c", "lineage", "Held-out transformations present."),
])

# ---------------------------------------------------------------- 13 experiment registry
T("experiment_registry", "data/derived/tables/experiment_registry.csv", "Evaluation registry. Holds only the non-learned dHash sanity baseline (BASE-DHASH-v1); no ORVEX model has been trained.", "phase1", [
 ("experiment_id", S, 0, "f", "ORVEX", "Id."), ("dataset_versions", S, 0, "f", "ORVEX", "Dataset versions."), ("split_version", S, 0, "f", "ORVEX", "Split."),
 ("label_map_version", S, 1, "f", "ORVEX", "Label map."), ("model_version", S, 1, "f", "ORVEX", "Model."), ("feature_version", S, 1, "f", "ORVEX", "Feature set."),
 ("metric_name", S, 1, "f", "ORVEX", "Metric."), ("metric_value", F, 1, "f", "ORVEX", "Value."), ("protocol", S, 1, "f", "ORVEX", "Protocol."),
 ("heldout_policy", S, 1, "f", "ORVEX", "Held-out policy."), ("report_path", S, 1, "f", "ORVEX", "Report."), ("leakage_test_result", S, 1, "f", "ORVEX", "Leakage result."),
])

# ---------------------------------------------------------------- 14 duplicate map
T("duplicate_map", "data/derived/tables/duplicate_map.csv", "Exact/near duplicates and cross-version repeats; canonical record kept.", "both", [
 ("duplicate_id", S, 0, "f", "ORVEX", "Id."), ("canonical_media_id", S, 0, "f", "master", "Kept record."), ("duplicate_media_id", S, 0, "f", "master", "Duplicate record."),
 ("duplicate_type", S, 0, "c", "rule", "exact_hash / near_duplicate_perceptual / same_url_across_versions / same_platform_id_across_sources."),
 ("evidence", S, 0, "d", "hash/dHash/URL", "Evidence."), ("resolution", S, 0, "f", "ORVEX", "What was done."),
])

# ---------------------------------------------------------------- 15 group examples
T("group_examples", "data/derived/tables/group_examples.csv", "Groups of 6 videos (4 related family members + 2 distractors) with ground-truth edges (Module 3: compare 5-6 videos).", "phase1", [
 ("group_id", S, 0, "f", "ORVEX", "Group id."), ("source_family_id", S, 0, "c", "root source", "Family of the related members."),
 ("member_media_ids", S, 0, "f", "master/variants", "Pipe-separated members (related + distractors)."), ("n_members", I, 0, "d", "count", "Number of members."),
 ("family_member_ids", S, 0, "f", "variants", "Related members."), ("distractor_ids", S, 1, "f", "other families in same split", "Unrelated members."),
 ("truth_edges", S, 1, "c", "controlled lineage", "Nearest-selected-ancestor edges parent>child among family members."), ("n_truth_edges", I, 0, "d", "count", "Number of edges."),
 ("split", S, 0, "c", "split_manifest", "Split."), ("split_version", S, 0, "f", "ORVEX", "Version."), ("label_origin", S, 0, "f", "ORVEX", "controlled_lineage."),
 ("evidence_id", S, 1, "f", "ledger", "Evidence."), ("created_utc", DT, 0, "f", "ORVEX", "Time."),
])

def cols(t): return [c[0] for c in TABLES[t]["cols"]]
