# ORVEX Data Dictionary

Generated 2026-10-26T18:48:14Z from `scripts/datasets/schema.py` (the machine-readable contract: `docs/datasets/schema_contract.json`). All 15 tables and 306 columns are described. Examples and distinct values are read from the real files.

Origin codes: **a** = copied from a named source field; **b** = normalized/renamed from a named source field; **c** = derived by an explicit deterministic rule from named fields; **d** = computed from the actual media/files by a named tool; **e** = annotated/decided by a human analyst with stated evidence; **f** = new ORVEX bookkeeping/administrative column

Controlled vocabularies:

- `record_origin`: real_world_source_record, orvex_normalized_record, orvex_controlled_variant_record, orvex_computed_record
- `media_origin`: naturally_collected_real_world, real_world_human_edited_dataset, controlled_variant, not_applicable_metadata_only
- `transformation_status`: none_source_unmodified, controlled_transformation_applied, controlled_transformation_failed, not_applicable
- `access_status`: downloaded_authorized, metadata_only, not_found, private_or_deleted, blocked_by_terms, access_not_available, retry_pending
- `direction_status`: directed_supported_by_source, directed_controlled_transformation, unknown_direction, non_directional
- `label_status`: source_ground_truth, controlled_ground_truth, uncertain, unknown, not_assessed
- `inclusion_status`: included_media_and_metadata, included_metadata_only, included_selected_subset, excluded_license, excluded_not_real_world_for_scope, excluded_duplicate_version, excluded_inaccessible, excluded_over_budget, research_lead_unverified, legal_review_required
- `split`: train, val, test, excluded
- `validation_status`: passed, failed, not_run

## source_registry
- File: `data/manifests/source_registry.csv` — rows: **31** — phase: both
- Purpose: Every dataset/source considered, with official source, terms, access, size and decision.

| column | type | unit / timezone | nullable | origin | lineage (source field / rule) | definition | allowed values | example | validation |
|---|---|---|---|---|---|---|---|---|---|
| source_dataset_id | str | - | no | f | ORVEX id (RW-xx) | Stable ORVEX id of the real-world source dataset. |  | RW-01 | contract header + non-null check (K01,K02) |
| title | str | - | no | a | official dataset page/paper title | Full title. |  | Wikimedia Commons CC/PD video pool (ORVEX selection) | contract header + non-null check (K01,K02) |
| creator | str | - | yes | a | official record creators | Creators/authors. |  | Wikimedia Commons contributors (per-file author) | contract header + non-null check (K01,K02) |
| release_version | str | - | yes | a | official release/version | Release or version label. |  | API snapshot 2026-10-26 | contract header + non-null check (K01,K02) |
| official_url | str | - | yes | a | official landing page | Official landing URL. |  | https://commons.wikimedia.org/wiki/Commons:Reusing_content_o | contract header + non-null check (K01,K02) |
| download_url | str | - | yes | a | official download/repository URL | Where files come from. |  | https://commons.wikimedia.org/w/api.php | contract header + non-null check (K01,K02) |
| paper_doi_or_url | str | - | yes | a | paper/DOI | Associated paper. |  | https://arxiv.org/abs/2303.13193 | contract header + non-null check (K01,K02) |
| accessed_date | str | - | no | f | date of verification | Date the page/API was accessed. | observed: 2026-10-26 | 2026-10-26 | contract header + non-null check (K01,K02) |
| license_terms | str | - | yes | a | licence field on official page | Licence/terms exactly as stated (or 'not stated'). |  | Per file (machine-readable): CC0 / Public domain / CC BY / C | contract header + non-null check (K01,K02) |
| license_evidence_url | str | - | yes | a | URL where the licence was read | Evidence link. |  | Commons API extmetadata LicenseShortName per file | contract header + non-null check (K01,K02) |
| bytes_or_urls_provided | str | - | no | a | official description | media_bytes / metadata_urls_only / mixed / unverified. | observed: API only, media_bytes, media_bytes (edited, trimmed, masks, full) + metadata.csv with Vimeo URLs, media_bytes after approval, metadata_urls_only, paper PDF only, unverified | media_bytes | contract header + non-null check (K01,K02) |
| derivative_use_status | str | - | no | c | licence text | permitted / not_stated / not_permitted / unverified. |  | permitted_per_file_licence | contract header + non-null check (K01,K02) |
| training_use_status | str | - | no | c | licence text | permitted / not_stated / unverified. |  | permitted_per_file_licence | contract header + non-null check (K01,K02) |
| redistribution_status | str | - | no | c | licence text | Whether files may be redistributed (with conditions). |  | permitted_with_attribution_and_sharealike_where_applicable | contract header + non-null check (K01,K02) |
| real_world_eligibility | str | - | no | e | analyst decision with evidence | Eligible / not eligible for the strict real-world collection and why. |  | Eligible: real user-uploaded recordings; selection is ORVEX' | contract header + non-null check (K01,K02) |
| native_task | str | - | yes | a | official description | Task the source was built for. |  | General media repository (no task) | contract header + non-null check (K01,K02) |
| native_labels | str | - | yes | a | official description | Native labels/annotations. |  | categories, description, licence | contract header + non-null check (K01,K02) |
| media_origin_characterization | str | - | no | e | analyst decision | How the media came to exist (user-uploaded, circulated, professionally edited...). |  | User-uploaded real-world video (speeches, street, wildlife,  | contract header + non-null check (K01,K02) |
| release_size_bytes | int | bytes | yes | a | official file sizes | Total official release size when known. |  | 55000000000 | contract header + non-null check (K01,K02) |
| planned_download_bytes | int | bytes | no | f | selection plan | Budgeted bytes. |  | 3000000000 | contract header + non-null check (K01,K02) |
| actual_local_bytes | int | bytes | no | d | du of local folder | Measured local bytes. |  | 1687283416 | contract header + non-null check (K01,K02) |
| record_count_local | int | - | no | d | row count of local files | Records held locally. |  | 96 | contract header + non-null check (K01,K02) |
| auth_required | str | - | no | a | official access docs | none / account / agreement / API. | observed: API approval, agreement, application, none, none for metadata, none for metadata; media must be fetched from platforms under their terms, registration, unknown | none | contract header + non-null check (K01,K02) |
| overlap_with | str | - | yes | e | analyst comparison | Other sources it overlaps. |  | VideoSham (subset) | contract header + non-null check (K01,K02) |
| inclusion_status | str | - | no | f | controlled vocabulary | Decision. | included_media_and_metadata, included_metadata_only, included_selected_subset, excluded_license, excluded_not_real_world_for_scope, excluded_duplicate_version, excluded_inaccessible, excluded_over_budget, research_lead_unverified, legal_review_required | included_selected_subset | contract header + non-null check (K01,K02); vocabulary |
| inclusion_reason | str | - | no | e | analyst decision | Why. |  | Only surveyed source with real media bytes whose per-file li | contract header + non-null check (K01,K02) |
| tasks_supported | str | - | yes | f | mapping to ORVEX modules | ORVEX modules/tasks supported. |  | Phase1: controlled variants, relationship ground truth, feat | contract header + non-null check (K01,K02) |
| evidence_links | str | - | yes | f | URLs consulted | Pipe-separated URLs. |  | https://commons.wikimedia.org/wiki/Commons:Reusing_content_o | contract header + non-null check (K01,K02) |
| limitations | str | - | yes | e | analyst notes | Known limitations. |  | Not a benchmark; no native relationship labels; themes chose | contract header + non-null check (K01,K02) |
| verification_level | str | - | no | f | see policy | verified_official_page / verified_api / research_lead_unverified. | observed: research_lead_unverified, verified_api, verified_official_page | verified_api | contract header + non-null check (K01,K02) |

## real_world_media_master
- File: `data/derived/tables/real_world_media_master.csv` — rows: **252,270** — phase: both
- Purpose: Normalized master of every real-world media record (downloaded or metadata-only). Controlled variants are NOT here.

| column | type | unit / timezone | nullable | origin | lineage (source field / rule) | definition | allowed values | example | validation |
|---|---|---|---|---|---|---|---|---|---|
| media_id | str | - | no | f | ORVEX id | Stable internal id (RW-<src>-...). |  | RW-CMN-P14634957 | contract header + non-null check (K01,K02) |
| source_dataset_id | str | - | no | f | source_registry | Source dataset. | observed: RW-01, RW-02, RW-03, RW-04, RW-05, RW-06, RW-07, RW-31 | RW-01 | contract header + non-null check (K01,K02) |
| release_version | str | - | yes | a | source release | Release/version of source. | observed: 2018, 2019, 2021-02-23, main@2026-10-26, v1.0, v2.0 | 2018 | contract header + non-null check (K01,K02) |
| native_record_id | str | - | yes | a | FVC cascade_id / FIVR query+id / VCSL uuid / ANAKIN video-id / Commons pageid | Native id of the record. |  | 14634957 | contract header + non-null check (K01,K02) |
| native_media_id | str | - | yes | a | platform video id or file title | Native media id. |  | File:Ante Pavelić Speech 21051941.ogv | contract header + non-null check (K01,K02) |
| platform | str | - | yes | b | host of source URL / 'wikimedia_commons' / 'vimeo' | Platform normalized to lowercase name. | observed: bilibili, facebook, huggingface_dataset, twitter, vimeo, wikimedia_commons, youtube | wikimedia_commons | contract header + non-null check (K01,K02) |
| platform_media_id | str | - | yes | c | parsed from URL | Platform video id. |  | 14634957 | contract header + non-null check (K01,K02) |
| source_url | str | - | yes | a | FVC video_url / VCSL url / ANAKIN url / Commons descriptionurl | Source URL as published. |  | https://commons.wikimedia.org/wiki/File:Ante_Paveli%C4%87_Sp | contract header + non-null check (K01,K02) |
| canonical_url | str | - | yes | c | normalized source_url | Canonical URL (scheme/host lowercased, tracking removed). |  | https://commons.wikimedia.org/wiki/File:Ante_Paveli%C4%87_Sp | contract header + non-null check (K01,K02) |
| title | str | - | yes | a | Commons title / ANAKIN task text | Title if the source has one. |  | File:Ante Pavelić Speech 21051941.ogv | contract header + non-null check (K01,K02) |
| description_caption | str | - | yes | a | Commons ImageDescription / ANAKIN task | Caption/description. |  | Ante Pavelić Speech | contract header + non-null check (K01,K02) |
| publisher_account_id | str | - | yes | b | Commons uploader username (public)  | Publisher account as published; pseudonymise in reports. |  | Quahadi | contract header + non-null check (K01,K02) |
| event_or_cascade_id | str | - | yes | a | FVC cascade_id / FIVR event id / ANAKIN video-id | Group the record belongs to. |  | 4zyvv7 | contract header + non-null check (K01,K02) |
| published_time_utc | datetime | UTC ISO-8601 (precision in time_precision) | yes | b | Commons upload timestamp | Publish time (only when the source provides one). |  | 2011-03-18T10:36:10Z | contract header + non-null check (K01,K02) |
| observed_time_utc | datetime | UTC ISO-8601 (precision in time_precision) | yes | f | n/a | Observation time if provided by source (rare). |  | (none — see missingness) | contract header + non-null check (K01,K02) |
| collected_time_utc | datetime | UTC ISO-8601 (precision in time_precision) | no | f | ORVEX run | When ORVEX collected/registered the record. |  | 2026-10-26T15:02:46Z | contract header + non-null check (K01,K02) |
| time_precision | str | - | yes | f | n/a | second / unknown. | observed: second, second_timezone_unstated, unknown | second | contract header + non-null check (K01,K02) |
| duration_s | float | seconds | yes | d | ffprobe | Duration (downloaded media only). |  | 522.893 | contract header + non-null check (K01,K02) |
| width | int | pixels | yes | d | ffprobe | Width. |  | 320 | contract header + non-null check (K01,K02) |
| height | int | pixels | yes | d | ffprobe | Height. |  | 240 | contract header + non-null check (K01,K02) |
| fps | float | frames/second | yes | d | ffprobe | Frame rate. |  | 0.0 | contract header + non-null check (K01,K02) |
| video_codec | str | - | yes | d | ffprobe | Video codec. | observed: av1, h264, theora, vp8, vp9 | theora | contract header + non-null check (K01,K02) |
| audio_codec | str | - | yes | d | ffprobe | Audio codec. | observed: aac, mp3, opus, vorbis | vorbis | contract header + non-null check (K01,K02) |
| has_audio | bool | - | yes | d | ffprobe | Audio stream present. |  | True | contract header + non-null check (K01,K02) |
| container | str | - | yes | d | ffprobe | Container. | observed: matroska,webm, mov,mp4,m4a,3gp,3g2,mj2, ogg | ogg | contract header + non-null check (K01,K02) |
| file_bytes | int | bytes | yes | d | os.stat | File size. |  | 23898980 | contract header + non-null check (K01,K02) |
| local_path | str | - | yes | f | ORVEX | Relative path of local file. |  | data/real_world/media/commons/RW-CMN-P14634957.ogv | contract header + non-null check (K01,K02) |
| sha256 | str | - | yes | d | hashlib SHA-256 | File hash (locally computed). |  | abc7b993b3d64239823134f765b99432619d3217c0d400dce80eddc88ca0 | contract header + non-null check (K01,K02) |
| access_status | str | - | no | f | VOC.access_status | Access status. | downloaded_authorized, metadata_only, not_found, private_or_deleted, blocked_by_terms, access_not_available, retry_pending | downloaded_authorized | contract header + non-null check (K01,K02); vocabulary |
| playable_status | str | - | yes | d | ffmpeg decode check | playable / unplayable / not_checked. | observed: not_checked, playable, unplayable | playable | contract header + non-null check (K01,K02) |
| rights_status | str | - | no | c | licence | Rights decision for storage/processing. | observed: cc-by-4.0_per_dataset_card_underlying_rights_unverified, dataset_licence_not_stated_media_not_downloaded, licence_permits_storage_transformation_redistribution_with_attribution, media_not_provided_by_source, not_cleared_vimeo_uploader_rights | licence_permits_storage_transformation_redistribution_with_a | contract header + non-null check (K01,K02) |
| license | str | - | yes | a | Commons LicenseShortName / dataset licence | Licence. |  | Public domain | contract header + non-null check (K01,K02) |
| license_url | str | - | yes | a | Commons LicenseUrl | Licence URL. |  | https://creativecommons.org/licenses/by/4.0 | contract header + non-null check (K01,K02) |
| attribution | str | - | yes | a | Commons Artist/Credit / dataset citation | Attribution string. |  | Ante_Pavelić | contract header + non-null check (K01,K02) |
| record_origin | str | - | no | f | VOC.record_origin | Origin of the record. | real_world_source_record, orvex_normalized_record, orvex_controlled_variant_record, orvex_computed_record | real_world_source_record | contract header + non-null check (K01,K02); vocabulary |
| media_origin | str | - | no | f | VOC.media_origin | Origin of the media. | naturally_collected_real_world, real_world_human_edited_dataset, controlled_variant, not_applicable_metadata_only | naturally_collected_real_world | contract header + non-null check (K01,K02); vocabulary |
| native_authenticity_label | str | - | yes | a | FVC label (fake/real) | Native label exactly as published. | observed: debunked, fake, parody, real, uncertain | fake | contract header + non-null check (K01,K02) |
| native_misleading_label | str | - | yes | a | FVC label | Native label (same field) kept separately. | observed: debunked, fake, parody, real, removed_by_youtube_for_false_information (dataset definition), uncertain | fake | contract header + non-null check (K01,K02) |
| native_manipulation_type | str | - | yes | a | ANAKIN manipulation-type | Native manipulation type. | observed: Tampering, Tampering (audio), Tampering -heavily re-processed, audio, frame-level, inpainting, splicing, swap | frame-level | contract header + non-null check (K01,K02) |
| normalized_authenticity_status | str | - | no | c | mapping rule in policy | unknown unless the native label states it; 'fake' in FVC = debunked, NOT AI-generated. | observed: manipulated_human_edit_documented, unknown, unmodified_clip_of_source_per_dataset | unknown | contract header + non-null check (K01,K02) |
| normalized_misleading_status | str | - | no | c | mapping rule | debunked_misleading / verified_not_misleading / not_assessed. | observed: debunked_misleading, not_assessed, removed_by_platform_for_false_information_per_source, verified_not_misleading | not_assessed | contract header + non-null check (K01,K02) |
| coordination_status | str | - | no | f | ORVEX policy | not_assessed for every record: no independent account/time coordination evidence exists locally. | observed: not_assessed | not_assessed | contract header + non-null check (K01,K02) |
| evidence_id | str | - | yes | f | evidence_ledger | Evidence record backing the source annotation / licence of this record. |  | EV-CMN-14634957 | contract header + non-null check (K01,K02) |
| perceptual_hash_ref | str | - | yes | d | feature_manifest visual_dhash24 | Reference to the computed 24-frame dHash features (local media only). | observed: data/derived/features/visual_dhash24.jsonl | data/derived/features/visual_dhash24.jsonl | contract header + non-null check (K01,K02) |
| annotation_status | str | - | no | f | ORVEX | source_annotation / none. | observed: none, source_annotation | none | contract header + non-null check (K01,K02) |
| qc_flags | str | - | yes | c | ORVEX QC rules | Flags (too_short, no_audio, decode_errors...). |  | too_long(>120s) | contract header + non-null check (K01,K02) |
| duplicate_of_media_id | str | - | yes | c | duplicate_map | Canonical media id if this is a duplicate. |  | RW-CMN-P128562512 | contract header + non-null check (K01,K02) |
| usable_for_variants | bool | - | no | c | rights + QC rules | Eligible as source for controlled variants. |  | False | contract header + non-null check (K01,K02) |
| missingness_note | str | - | yes | f | ORVEX | Why fields are null. |  | no native relationship/authenticity labels in source | contract header + non-null check (K01,K02) |

## controlled_variant_registry
- File: `data/derived/tables/controlled_variant_registry.csv` — rows: **1,133** — phase: phase1
- Purpose: Every controlled variant rendered by ORVEX from eligible real-world media. Never mixed with naturally collected media.

| column | type | unit / timezone | nullable | origin | lineage (source field / rule) | definition | allowed values | example | validation |
|---|---|---|---|---|---|---|---|---|---|
| variant_media_id | str | - | no | f | ORVEX id | Id of the created video (CV-...). |  | CV-P10491224-V01 | contract header + non-null check (K01,K02) |
| direct_parent_media_id | str | - | no | f | ORVEX transformation plan | Immediate parent (real source or earlier variant). |  | RW-CMN-P10491224 | contract header + non-null check (K01,K02) |
| root_source_media_id | str | - | no | f | media master | Real-world root source. |  | RW-CMN-P10491224 | contract header + non-null check (K01,K02) |
| ancestor_chain | str | - | no | c | parent links | Pipe-separated ancestors up to the root. |  | RW-CMN-P10491224 | contract header + non-null check (K01,K02) |
| video_source_media_id | str | - | no | f | media master | Real-world source of the picture track. |  | RW-CMN-P10491224 | contract header + non-null check (K01,K02) |
| audio_source_media_id | str | - | yes | f | media master | Real-world source of replaced/mixed audio. |  | RW-CMN-P115080780 | contract header + non-null check (K01,K02) |
| caption_text_source_media_id | str | - | yes | f | media master | Real-world record the caption text came from. |  | RW-CMN-P176367262 | contract header + non-null check (K01,K02) |
| caption_text | str | - | yes | b | title of the caption-source record (ASCII-normalised) | Caption burned in. |  | Ballistische Kurve | contract header + non-null check (K01,K02) |
| caption_text_origin_field | str | - | yes | f | n/a | Field of the source record used (commons_title). | observed: title | title | contract header + non-null check (K01,K02) |
| transformation_id | str | - | no | f | catalogue | T01-T14. |  | T01 | contract header + non-null check (K01,K02) |
| transformation_name | str | - | no | f | catalogue | Name. |  | reencode_hq | contract header + non-null check (K01,K02) |
| transformation_family | str | - | no | f | catalogue | Family. | observed: audio, compression, overlay, spatial, temporal, text | compression | contract header + non-null check (K01,K02) |
| parameters_json | json | - | no | f | ORVEX | Exact parameters. |  | {"crf": 18} | contract header + non-null check (K01,K02) |
| tool_name | str | - | no | f | ORVEX | ffmpeg. | observed: ffmpeg | ffmpeg | contract header + non-null check (K01,K02) |
| tool_version | str | - | no | d | ffmpeg -version | Tool version. | observed: ffmpeg version 9.0.2-essentials_build-www.gyan.dev Copyright (c) 2000-2026 the FFmpeg developers | ffmpeg version 9.0.2-essentials_build-www.gyan.dev Copyright | contract header + non-null check (K01,K02) |
| run_id | str | - | no | f | ORVEX | Run id. |  | RUN-CV-P10491224-V01 | contract header + non-null check (K01,K02) |
| seed | str | - | yes | f | ORVEX | Deterministic selection key. |  | sha256-pick:RW-CMN-P10491224 | contract header + non-null check (K01,K02) |
| created_utc | datetime | UTC ISO-8601 (precision in time_precision) | no | f | ORVEX | Creation time. |  | 2026-10-26T06:41:04Z | contract header + non-null check (K01,K02) |
| local_path | str | - | yes | f | ORVEX | Path of the created file (blank for failed variants: no file retained). |  | data/controlled_variants/media/P10491224/CV-P10491224-V01.mp | contract header + non-null check (K01,K02) |
| sha256 | str | - | yes | d | hashlib | Output hash (blank for failed variants). |  | f7bd4dfed1436d66ee06426a562c740f5a5f921b43257cfec52be7d197d7 | contract header + non-null check (K01,K02) |
| bytes | int | bytes | no | d | os.stat | Output size. |  | 5755540 | contract header + non-null check (K01,K02) |
| duration_s | float | seconds | yes | d | ffprobe | Output duration. |  | 27.133 | contract header + non-null check (K01,K02) |
| width | int | pixels | yes | d | ffprobe | Width. |  | 720 | contract header + non-null check (K01,K02) |
| height | int | pixels | yes | d | ffprobe | Height. |  | 576 | contract header + non-null check (K01,K02) |
| fps | float | frames/second | yes | d | ffprobe | fps. |  | 30.0 | contract header + non-null check (K01,K02) |
| has_audio | bool | - | yes | d | ffprobe | Audio present. |  | True | contract header + non-null check (K01,K02) |
| generation_depth | int | - | no | c | chain length | Edits from the real root. |  | 1 | contract header + non-null check (K01,K02) |
| chain_id | str | - | yes | f | catalogue | Chain id. | observed: C1, C2, C3, C4, C5 | C1 | contract header + non-null check (K01,K02) |
| permission_basis | str | - | no | c | root licence | Why the transformation is permitted. |  | CC BY-SA 3.0 permits adaptation (root); audio/caption source | contract header + non-null check (K01,K02) |
| root_license | str | - | no | a | media master license | Licence of root. | observed: CC BY 3.0, CC BY 4.0, CC BY-SA 2.0, CC BY-SA 3.0, CC BY-SA 4.0, CC0, Public domain | CC BY-SA 3.0 | contract header + non-null check (K01,K02) |
| validation_status | str | - | no | d | ffprobe checks | passed/failed/not_run. | passed, failed, not_run | passed | contract header + non-null check (K01,K02); vocabulary |
| validation_checks_json | json | - | no | d | ffprobe | Checks and results. |  | {"probe_ok": true, "duration_expected_s": 27.13, "duration_a | contract header + non-null check (K01,K02) |
| failure_reason | str | - | yes | f | ORVEX | Reason if failed. | observed: validation checks failed | validation checks failed | contract header + non-null check (K01,K02) |
| media_origin | str | - | no | f | VOC | Always controlled_variant. | naturally_collected_real_world, real_world_human_edited_dataset, controlled_variant, not_applicable_metadata_only | controlled_variant | contract header + non-null check (K01,K02); vocabulary |
| record_origin | str | - | no | f | VOC | Always orvex_controlled_variant_record. | real_world_source_record, orvex_normalized_record, orvex_controlled_variant_record, orvex_computed_record | orvex_controlled_variant_record | contract header + non-null check (K01,K02); vocabulary |
| transformation_status | str | - | no | f | VOC | controlled_transformation_applied / failed. | none_source_unmodified, controlled_transformation_applied, controlled_transformation_failed, not_applicable | controlled_transformation_applied | contract header + non-null check (K01,K02); vocabulary |
| usable_for_training | bool | - | no | c | validation + split + held-out rule | True only if passed, train split and no held-out transform in lineage. |  | True | contract header + non-null check (K01,K02) |
| source_split | str | - | no | c | split_manifest | Split of the root source family. | observed: test, train, val | train | contract header + non-null check (K01,K02) |

## media_relationship_edges
- File: `data/derived/tables/media_relationship_edges.csv` — rows: **299,875** — phase: both
- Purpose: Relationship edges: source-provided native relations (kept with original label) and controlled-transformation lineage.

| column | type | unit / timezone | nullable | origin | lineage (source field / rule) | definition | allowed values | example | validation |
|---|---|---|---|---|---|---|---|---|---|
| relationship_id | str | - | no | f | ORVEX | Edge id. |  | REL-0000001 | contract header + non-null check (K01,K02) |
| source_dataset_id | str | - | no | f | source_registry | Where the relation comes from (or ORVEX-CTRL). | observed: ORVEX-CTRL, RW-02, RW-03, RW-06, RW-07 | RW-02 | contract header + non-null check (K01,K02) |
| relation_scope | str | - | no | f | ORVEX | real_native / controlled_lineage. | observed: controlled_lineage, real_native | real_native | contract header + non-null check (K01,K02) |
| evidence_id | str | - | no | f | evidence_ledger | Evidence record. |  | EV-ANK-meta | contract header + non-null check (K01,K02) |
| media_a_id | str | - | no | f | media master/variant registry | First item. |  | RW-ANK-4zyvv7-T | contract header + non-null check (K01,K02) |
| media_b_id | str | - | no | f | media master/variant registry | Second item. |  | RW-ANK-4zyvv7-E | contract header + non-null check (K01,K02) |
| native_media_a_id | str | - | yes | a | native ids | Native id of A. |  | 4zyvv7 | contract header + non-null check (K01,K02) |
| native_media_b_id | str | - | yes | a | native ids | Native id of B. |  | 4zyvv7 | contract header + non-null check (K01,K02) |
| native_label | str | - | yes | a | FIVR ND/DS/CS/IS; VCSL label_file; FVC label; ANAKIN manipulation-type | Label exactly as published. |  | frame-level | contract header + non-null check (K01,K02) |
| normalized_relation_type | str | - | no | c | mapping table | e.g. near_duplicate, partial_temporal_copy, same_scene_not_copy, same_incident_not_copy, edited_version, controlled_*. |  | edited_version_of_trimmed_clip | contract header + non-null check (K01,K02) |
| direction_status | str | - | no | c | VOC | Direction support. | directed_supported_by_source, directed_controlled_transformation, unknown_direction, non_directional | directed_supported_by_source | contract header + non-null check (K01,K02); vocabulary |
| parent_media_id | str | - | yes | c | only when direction supported | Parent. |  | RW-ANK-4zyvv7-T | contract header + non-null check (K01,K02) |
| child_media_id | str | - | yes | c | only when direction supported | Child. |  | RW-ANK-4zyvv7-E | contract header + non-null check (K01,K02) |
| a_segment_start_s | float | seconds | yes | a | VCSL label_file | Copied segment start in A. |  | 0 | contract header + non-null check (K01,K02) |
| a_segment_end_s | float | seconds | yes | a | VCSL label_file | End in A. |  | 8 | contract header + non-null check (K01,K02) |
| b_segment_start_s | float | seconds | yes | a | VCSL label_file | Start in B. |  | 164 | contract header + non-null check (K01,K02) |
| b_segment_end_s | float | seconds | yes | a | VCSL label_file | End in B. |  | 497 | contract header + non-null check (K01,K02) |
| overlap_ratio | float | - | yes | c | segment durations / duration | Copied-duration ratio when measurable. |  | (none — see missingness) | contract header + non-null check (K01,K02) |
| transformation_type | str | - | yes | f | catalogue / ANAKIN manipulation-type | Transformation type. |  | frame-level | contract header + non-null check (K01,K02) |
| label_source | str | - | no | f | ORVEX | source_annotation / controlled_transformation_log. | observed: controlled_transformation_log, source_annotation | source_annotation | contract header + non-null check (K01,K02) |
| label_status | str | - | no | f | VOC | Label status. | source_ground_truth, controlled_ground_truth, uncertain, unknown, not_assessed | source_ground_truth | contract header + non-null check (K01,K02); vocabulary |
| evidence_status | str | - | no | f | policy | kind of evidence behind the label: source_annotation / controlled_transformation_log (separate from label status). | observed: controlled_transformation_log, source_annotation | source_annotation | contract header + non-null check (K01,K02) |
| confidence_status | str | - | no | f | policy | No numeric confidence: source_ground_truth / controlled_ground_truth. | observed: controlled_ground_truth_not_calibrated, source_ground_truth_not_calibrated | source_ground_truth_not_calibrated | contract header + non-null check (K01,K02) |
| reviewer | str | - | yes | e | human reviewer | Reviewer id (none yet). |  | (none — see missingness) | contract header + non-null check (K01,K02) |
| method_version | str | - | no | f | ORVEX | Script version. | observed: s3_normalize.py@1, s4_variants.py@1 | s3_normalize.py@1 | contract header + non-null check (K01,K02) |
| created_utc | datetime | UTC ISO-8601 (precision in time_precision) | no | f | ORVEX | Creation time. |  | 2026-10-26T15:02:46Z | contract header + non-null check (K01,K02) |
| media_available_locally | bool | - | no | d | file exists | Both media bytes present locally. |  | True | contract header + non-null check (K01,K02) |
| conflict_flag | bool | - | no | c | cross-source check | Conflicting labels between sources. |  | False | contract header + non-null check (K01,K02) |
| notes | str | - | yes | f | ORVEX | Notes. |  | editor task: Speeding up/Slowing down : 33% | contract header + non-null check (K01,K02) |

## platform_observations
- File: `data/derived/tables/platform_observations.csv` — rows: **352,702** — phase: phase2
- Purpose: Real posts/observations of media on platforms as provided by the sources (no invented posts).

| column | type | unit / timezone | nullable | origin | lineage (source field / rule) | definition | allowed values | example | validation |
|---|---|---|---|---|---|---|---|---|---|
| observation_id | str | - | no | f | ORVEX | Id. |  | OBS-CMN-14634957 | contract header + non-null check (K01,K02) |
| media_id | str | - | no | f | media master | Media observed. |  | RW-CMN-P14634957 | contract header + non-null check (K01,K02) |
| observation_type | str | - | no | f | ORVEX | upload / publish / removal / share_reference / cascade_member. | observed: cascade_member, publish, removal, share_reference, upload | upload | contract header + non-null check (K01,K02) |
| coordination_status | str | - | no | f | policy | not_assessed: no independent coordination evidence. | observed: not_assessed | not_assessed | contract header + non-null check (K01,K02) |
| platform | str | - | yes | b | URL host | Platform. | observed: facebook, twitter, wikimedia_commons, youtube | wikimedia_commons | contract header + non-null check (K01,K02) |
| platform_post_id | str | - | yes | c | parsed from URL | Post/video id. |  | 14634957 | contract header + non-null check (K01,K02) |
| post_url | str | - | yes | a | source URL | URL. |  | https://commons.wikimedia.org/wiki/File:Ante_Paveli%C4%87_Sp | contract header + non-null check (K01,K02) |
| account_id_pseudonym | str | - | yes | c | SHA-256 prefix of public account name | Pseudonymised account id (policy). |  | c30f326068b9 | contract header + non-null check (K01,K02) |
| account_id_source_field | str | - | yes | f | n/a | Source field used (commons uploader) or null. | observed: channel_id, commons_uploader_username | commons_uploader_username | contract header + non-null check (K01,K02) |
| publish_time_utc | datetime | UTC ISO-8601 (precision in time_precision) | yes | b | Commons upload timestamp | Publish time. |  | 2011-03-18T10:36:10Z | contract header + non-null check (K01,K02) |
| observation_time_utc | datetime | UTC ISO-8601 (precision in time_precision) | yes | f | n/a | Observation time. |  | 2020-05-16T23:31:30 | contract header + non-null check (K01,K02) |
| time_precision | str | - | yes | f | n/a | second / unknown. | observed: second, second_derived_unverified, second_timezone_unstated, unknown | second | contract header + non-null check (K01,K02) |
| caption_text | str | - | yes | a | Commons description | Caption. |  | Ante Pavelić Speech | contract header + non-null check (K01,K02) |
| hashtags | str | - | yes | f | n/a | Not provided. |  | (none — see missingness) | contract header + non-null check (K01,K02) |
| engagement_refs | str | - | yes | a | Commons global usage count | Permitted engagement/reuse reference. |  | commons_global_usage_count=2 | contract header + non-null check (K01,K02) |
| metadata_source | str | - | no | f | source_registry | Source dataset. | observed: RW-01, RW-03, RW-31 | RW-01 | contract header + non-null check (K01,K02) |
| collection_method | str | - | no | f | ORVEX | official_api / dataset_file. | observed: dataset_file, official_api | official_api | contract header + non-null check (K01,K02) |
| order_in_cascade | int | - | yes | c | row order inside FVC cascade | Temporal order inside cascade as stated by the authors (not a timestamp). |  | 0 | contract header + non-null check (K01,K02) |
| cascade_id | str | - | yes | a | FVC cascade_id | Cascade id. |  | f0 | contract header + non-null check (K01,K02) |
| access_status | str | - | no | f | VOC | Access. | downloaded_authorized, metadata_only, not_found, private_or_deleted, blocked_by_terms, access_not_available, retry_pending | downloaded_authorized | contract header + non-null check (K01,K02); vocabulary |
| evidence_id | str | - | no | f | evidence_ledger | Evidence. |  | EV-CMN-14634957 | contract header + non-null check (K01,K02) |
| limitations | str | - | yes | f | ORVEX | Limitations. | observed: derived time is OUTSIDE the dataset's stated sharing window (Nov 2019-Jun 2020): treat as unverified; time derived from the tweet-id snowflake; sharing account not provided in the source, no timestamp or account in source; order is the authors' cascade order, only a post id is provided: no URL, account or time, publish time/channel present only for part of the videos, removal time as stated by the dataset authors (when YouTube removed the video), time derived from the tweet-id snowflake; sharing account not provided in the source, upload event only; not a social-media distribution trace | upload event only; not a social-media distribution trace | contract header + non-null check (K01,K02) |

## evidence_ledger
- File: `data/derived/tables/evidence_ledger.csv` — rows: **1,237** — phase: both
- Purpose: Evidence records supporting labels, relations and rights decisions.

| column | type | unit / timezone | nullable | origin | lineage (source field / rule) | definition | allowed values | example | validation |
|---|---|---|---|---|---|---|---|---|---|
| evidence_id | str | - | no | f | ORVEX | Id. |  | EV-CMN-14634957 | contract header + non-null check (K01,K02) |
| evidence_type | str | - | no | f | ORVEX | source_annotation / source_metadata / controlled_transformation_log / machine_measurement / license_record. | observed: controlled_transformation_log, license_record, machine_measurement, source_annotation, source_metadata | license_record | contract header + non-null check (K01,K02) |
| source_dataset_id | str | - | no | f | source_registry | Source. |  | RW-01 | contract header + non-null check (K01,K02) |
| subject_type | str | - | no | f | ORVEX | media / relationship_set / variant / license. | observed: media, relationship_set, variant | media | contract header + non-null check (K01,K02) |
| subject_id | str | - | no | f | ORVEX | Subject id or set name. |  | RW-CMN-P14634957 | contract header + non-null check (K01,K02) |
| source_url | str | - | yes | a | official URL | URL. |  | https://commons.wikimedia.org/wiki/File:Ante_Paveli%C4%87_Sp | contract header + non-null check (K01,K02) |
| source_record_ref | str | - | yes | f | file path / record key | Where inside the source. |  | Commons API extmetadata pageid=14634957 | contract header + non-null check (K01,K02) |
| claim_supported | str | - | no | f | ORVEX | What this evidence supports. |  | licence Public domain permits storage/transformation with at | contract header + non-null check (K01,K02) |
| claim_status | str | - | no | f | policy | source_asserted / measured / controlled_by_construction. | observed: controlled_by_construction, measured, source_asserted | source_asserted | contract header + non-null check (K01,K02) |
| observed_fact_vs_inference | str | - | no | f | policy | observed_fact / source_annotation / machine_measurement / analyst_inference. | observed: analyst_inference, machine_measurement, source_annotation | source_annotation | contract header + non-null check (K01,K02) |
| verification_method | str | - | no | f | ORVEX | How checked. | observed: Commons API machine-readable licence, FFmpeg run log + ffprobe/decode/frame validation, GitHub raw files read; dataset licence not stated, Zenodo record + file read (md5 verified), Zenodo record + files read (md5 verified), Zenodo record read (md5 verified); label definitions read in the FIVR paper, dataset card + metadata file read, distinct page ids + dHash near-duplicate screen (duplicate_map) | Commons API machine-readable licence | contract header + non-null check (K01,K02) |
| evidence_time_utc | datetime | UTC ISO-8601 (precision in time_precision) | no | f | ORVEX | When evidence was recorded. |  | 2026-10-26T15:02:46Z | contract header + non-null check (K01,K02) |
| temporal_precision | str | - | yes | f | n/a | Precision. | observed: date, second | date | contract header + non-null check (K01,K02) |
| file_sha256 | str | - | yes | d | hashlib | Hash of the evidence file. |  | abc7b993b3d64239823134f765b99432619d3217c0d400dce80eddc88ca0 | contract header + non-null check (K01,K02) |
| reviewer_status | str | - | no | f | policy | unreviewed / source_curated. | observed: source_curated, unreviewed | unreviewed | contract header + non-null check (K01,K02) |
| permission_status | str | - | no | c | licence | Permission. | observed: cc-by-4.0_annotations, cc-by-4.0_metadata, cc-by-4.0_per_card, dataset_licence_not_stated_annotations_used_as_metadata_only, licence_permits, licence_permits_adaptation, n/a | licence_permits | contract header + non-null check (K01,K02) |
| confidence_basis | str | - | no | f | policy | No calibrated numeric confidence; basis stated. | observed: controlled ground truth (known transformation), not a calibrated probability, sampling rule, not proof of independence, source_curated_annotation_no_calibrated_confidence | source_curated_annotation_no_calibrated_confidence | contract header + non-null check (K01,K02) |
| limitations | str | - | yes | f | ORVEX | Limitations. | observed: constructed experimental artefact, not a natural post, same-theme negatives may still share an event; flagged hard | constructed experimental artefact, not a natural post | contract header + non-null check (K01,K02) |

## feature_manifest
- File: `data/derived/tables/feature_manifest.csv` — rows: **5,187** — phase: both
- Purpose: What features actually exist (and which are not computed).

| column | type | unit / timezone | nullable | origin | lineage (source field / rule) | definition | allowed values | example | validation |
|---|---|---|---|---|---|---|---|---|---|
| feature_record_id | str | - | no | f | ORVEX | Id. |  | FEAT-000001 | contract header + non-null check (K01,K02) |
| media_id | str | - | no | f | media master / variants | Media or ALL_LOCAL for aggregate rows. |  | RW-CMN-P14634957 | contract header + non-null check (K01,K02) |
| feature_type | str | - | no | f | ORVEX | visual_dhash_24 / audio_pcm_md5_8k / audio_envelope_1s / visual_embedding / audio_embedding / ocr_text / asr_transcript / text_embedding / scene_boundaries. |  | visual_dhash24 | contract header + non-null check (K01,K02) |
| extraction_status | str | - | no | d | script result | computed / not_computed / failed. | observed: computed, not_computed | computed | contract header + non-null check (K01,K02) |
| tool_name | str | - | yes | f | ORVEX | Tool. | observed: opencv-python+ffmpeg+numpy | opencv-python+ffmpeg+numpy | contract header + non-null check (K01,K02) |
| tool_version | str | - | yes | d | tool | Version. | observed: opencv 4.12.0; ffmpeg version 9.0.2 | opencv 4.12.0; ffmpeg version 9.0.2 | contract header + non-null check (K01,K02) |
| parameters_json | json | - | yes | f | ORVEX | Parameters. |  | {"frames": 24, "dhash": "9x8 grayscale", "audio": "8 kHz mon | contract header + non-null check (K01,K02) |
| sample_timestamps | str | - | yes | d | frame indices | Sample positions. |  | 0,568,1136,1704,2273,2841,3409,3977,4546,5114,5682,6250,6819 | contract header + non-null check (K01,K02) |
| feature_format | str | - | yes | f | ORVEX | Format/dimension. | observed: 64-bit hex x24, hex digit/second, md5 hex | 64-bit hex x24 | contract header + non-null check (K01,K02) |
| storage_path | str | - | yes | f | ORVEX | File holding the feature. | observed: data/derived/features/audio_fingerprint.jsonl, data/derived/features/visual_dhash24.jsonl | data/derived/features/visual_dhash24.jsonl | contract header + non-null check (K01,K02) |
| storage_bytes | int | bytes | yes | d | os.stat | Size. |  | 407 | contract header + non-null check (K01,K02) |
| feature_sha256 | str | - | yes | d | hashlib | Hash. |  | f29f705bf9ff2a6f437c1fce643f23d0e598d027dd8051fe73f9a59cdcc3 | contract header + non-null check (K01,K02) |
| extracted_utc | datetime | UTC ISO-8601 (precision in time_precision) | yes | f | ORVEX | Time. |  | 2026-10-26T18:06:44Z | contract header + non-null check (K01,K02) |
| error | str | - | yes | f | ORVEX | Error. | observed: no audio stream, no decodable frames, not computed in roadmap 10.2-10.4 (model phase); no placeholder files exist | no audio stream | contract header + non-null check (K01,K02) |
| permission_status | str | - | no | c | licence | Permission. | observed: licence_permits | licence_permits | contract header + non-null check (K01,K02) |

## training_pairs
- File: `data/derived/tables/training_pairs.csv` — rows: **13,659** — phase: phase1
- Purpose: Model examples (related/unrelated/uncertain pairs) with local media only, split by source family.

| column | type | unit / timezone | nullable | origin | lineage (source field / rule) | definition | allowed values | example | validation |
|---|---|---|---|---|---|---|---|---|---|
| example_id | str | - | no | f | ORVEX | Id. |  | EX-0000001 | contract header + non-null check (K01,K02) |
| media_a_id | str | - | no | f | master/variants | A. |  | RW-CMN-P10491224 | contract header + non-null check (K01,K02) |
| media_b_id | str | - | no | f | master/variants | B. |  | CV-P10491224-V01 | contract header + non-null check (K01,K02) |
| relationship_id | str | - | yes | f | edges | Edge backing the label (null for negatives). |  | REL-C-000001 | contract header + non-null check (K01,K02) |
| label_binary_related | int | - | no | c | relationship_class | 1 related / 0 not related. |  | 1 | contract header + non-null check (K01,K02) |
| relationship_class | str | - | no | c | edge types | direct_derivation / indirect_derivation / sibling_same_parent / same_family_other / edited_version / unrelated_distinct_source. | observed: audio_source_only_not_visual_derivation, direct_derivation, edited_version, indirect_derivation, same_family_other, sibling_same_parent, unrelated_distinct_source | direct_derivation | contract header + non-null check (K01,K02) |
| native_label | str | - | yes | a | source label | Native label if from a source. | observed: audio, frame-level, inpainting, splicing, swap | splicing | contract header + non-null check (K01,K02) |
| normalized_label | str | - | no | c | mapping | Normalized label. | observed: audio_source_only_not_visual_derivation, direct_derivation, edited_version, indirect_derivation, same_family_other, sibling_same_parent, unrelated_distinct_source | direct_derivation | contract header + non-null check (K01,K02) |
| label_origin | str | - | no | f | ORVEX | controlled_lineage / source_annotation / negative_sampling_rule. | observed: controlled_lineage, negative_sampling_rule, source_annotation | controlled_lineage | contract header + non-null check (K01,K02) |
| label_status | str | - | no | f | VOC | Status. | source_ground_truth, controlled_ground_truth, uncertain, unknown, not_assessed | controlled_ground_truth | contract header + non-null check (K01,K02); vocabulary |
| evidence_id | str | - | yes | f | ledger | Evidence. |  | EV-CV-CV-P10491224-V01 | contract header + non-null check (K01,K02) |
| feature_refs | str | - | yes | f | feature_manifest | Feature ids. | observed: visual_dhash24\|audio_fingerprint;visual_dhash24\|audio_fingerprint | visual_dhash24\|audio_fingerprint;visual_dhash24\|audio_finger | contract header + non-null check (K01,K02) |
| source_family_id | str | - | no | c | root source | Family used for splitting (A's family). |  | RW-CMN-P10491224 | contract header + non-null check (K01,K02) |
| event_or_cascade_group_id | str | - | yes | a | FVC/ANAKIN group | Group. |  | 7e2p57 | contract header + non-null check (K01,K02) |
| split | str | - | no | c | split_manifest | train/val/test/excluded. | train, val, test, excluded | train | contract header + non-null check (K01,K02); vocabulary |
| split_version | str | - | no | f | ORVEX | Version. | observed: split-v2 | split-v2 | contract header + non-null check (K01,K02) |
| sampling_method | str | - | no | f | ORVEX | How the pair was chosen. | observed: all within-family pairs, seeded random negative sampling inside split | all within-family pairs | contract header + non-null check (K01,K02) |
| negative_rationale | str | - | yes | f | ORVEX | Why a negative is credible. | observed: audio shared by construction; picture tracks are unrelated, different ANAKIN video-ids (distinct source videos/URLs per the dataset metadata), distinct Commons uploads (different page ids) with no exact/near-duplicate match in the dHash check; different search themes, distinct Commons uploads (different page ids) with no exact/near-duplicate match in the dHash check; same search theme, not necessarily same event (not proof of independence) | distinct Commons uploads (different page ids) with no exact/ | contract header + non-null check (K01,K02) |
| hardness | str | - | yes | c | rule | easy/medium/hard. | observed: easy, hard, medium | easy | contract header + non-null check (K01,K02) |
| leakage_flag | bool | - | no | c | leakage test | True if pair crosses families/splits. |  | False | contract header + non-null check (K01,K02) |
| exclusion_reason | str | - | yes | f | ORVEX | Reason excluded. | observed: audio_donor_family_in_different_split, held_out_transform_test_only_family_not_test | held_out_transform_test_only_family_not_test | contract header + non-null check (K01,K02) |
| includes_heldout_transform | bool | - | no | c | lineage | Involves a test-only transformation. |  | False | contract header + non-null check (K01,K02) |
| created_utc | datetime | UTC ISO-8601 (precision in time_precision) | no | f | ORVEX | Time. |  | 2026-10-26T18:06:44Z | contract header + non-null check (K01,K02) |

## campaign_candidate_clusters
- File: `data/derived/tables/campaign_candidate_clusters.csv` — rows: **0** — phase: phase2
- Purpose: Candidate clusters for human review. EMPTY: no authorised account+time evidence is available locally (see QA report).

| column | type | unit / timezone | nullable | origin | lineage (source field / rule) | definition | allowed values | example | validation |
|---|---|---|---|---|---|---|---|---|---|
| cluster_id | str | - | no | f | ORVEX | Id. |  | (none — see missingness) | contract header + non-null check (K01,K02) |
| observation_ids | str | - | no | f | observations | Observations. |  | (none — see missingness) | contract header + non-null check (K01,K02) |
| media_ids | str | - | yes | f | master | Media. |  | (none — see missingness) | contract header + non-null check (K01,K02) |
| account_pseudonyms | str | - | yes | c | observations | Accounts. |  | (none — see missingness) | contract header + non-null check (K01,K02) |
| time_window_start_utc | datetime | UTC ISO-8601 (precision in time_precision) | yes | f | observations | Start. |  | (none — see missingness) | contract header + non-null check (K01,K02) |
| time_window_end_utc | datetime | UTC ISO-8601 (precision in time_precision) | yes | f | observations | End. |  | (none — see missingness) | contract header + non-null check (K01,K02) |
| common_media_signals | str | - | yes | f | edges | Media signals. |  | (none — see missingness) | contract header + non-null check (K01,K02) |
| posting_pattern_signals | str | - | yes | f | observations | Posting signals. |  | (none — see missingness) | contract header + non-null check (K01,K02) |
| independent_coordination_evidence | str | - | yes | f | evidence | Independent evidence. |  | (none — see missingness) | contract header + non-null check (K01,K02) |
| candidate_status | str | - | no | f | policy | candidate_cluster / not_assessed. |  | (none — see missingness) | contract header + non-null check (K01,K02) |
| reviewer | str | - | yes | e | human | Reviewer. |  | (none — see missingness) | contract header + non-null check (K01,K02) |
| limitations | str | - | yes | f | ORVEX | Limitations. |  | (none — see missingness) | contract header + non-null check (K01,K02) |

## transformation_run_log
- File: `data/derived/tables/transformation_run_log.csv` — rows: **1,133** — phase: phase1
- Purpose: One row per transformation execution.

| column | type | unit / timezone | nullable | origin | lineage (source field / rule) | definition | allowed values | example | validation |
|---|---|---|---|---|---|---|---|---|---|
| run_id | str | - | no | f | ORVEX | Run id. |  | RUN-CV-P10491224-V01 | contract header + non-null check (K01,K02) |
| variant_media_id | str | - | no | f | variant registry | Output. |  | CV-P10491224-V01 | contract header + non-null check (K01,K02) |
| input_media_ids | str | - | no | f | ORVEX | Inputs (video\|audio donor). |  | RW-CMN-P10491224 | contract header + non-null check (K01,K02) |
| tool_name | str | - | no | f | ORVEX | Tool. | observed: ffmpeg | ffmpeg | contract header + non-null check (K01,K02) |
| tool_version | str | - | no | d | ffmpeg | Version. | observed: ffmpeg version 9.0.2-essentials_build-www.gyan.dev Copyright (c) 2000-2026 the FFmpeg developers | ffmpeg version 9.0.2-essentials_build-www.gyan.dev Copyright | contract header + non-null check (K01,K02) |
| command_config | str | - | no | f | ORVEX | Full argument list (root path abstracted). |  | -y -v error -i <ROOT>\data/real_world/media/commons/RW-CMN-P | contract header + non-null check (K01,K02) |
| parameters_json | json | - | no | f | ORVEX | Parameters. |  | {"crf": 18} | contract header + non-null check (K01,K02) |
| started_utc | datetime | UTC ISO-8601 (precision in time_precision) | no | f | ORVEX | Time. |  | 2026-10-26T06:41:04Z | contract header + non-null check (K01,K02) |
| return_code | int | - | no | d | process | Exit code. |  | 0 | contract header + non-null check (K01,K02) |
| output_validation_status | str | - | no | d | ffprobe | passed/failed. | observed: failed, passed | passed | contract header + non-null check (K01,K02) |
| output_bytes | int | bytes | yes | d | os.stat | Bytes. |  | 5755540 | contract header + non-null check (K01,K02) |
| storage_delta_bytes | int | bytes | yes | d | os.stat | Payload change. |  | 5755540 | contract header + non-null check (K01,K02) |
| error | str | - | yes | f | process | stderr tail. |  | (none — see missingness) | contract header + non-null check (K01,K02) |
| deterministic_notes | str | - | yes | f | ORVEX | Determinism notes. | observed: parameters fixed; donor/caption picked by sha256 of root id | parameters fixed; donor/caption picked by sha256 of root id | contract header + non-null check (K01,K02) |
| seed | str | - | yes | f | ORVEX | Selection key. |  | sha256-pick:RW-CMN-P10491224 | contract header + non-null check (K01,K02) |

## download_access_attempt_log
- File: `data/manifests/download_access_attempt_log.csv` — rows: **729** — phase: both
- Purpose: Every download/access attempt.

| column | type | unit / timezone | nullable | origin | lineage (source field / rule) | definition | allowed values | example | validation |
|---|---|---|---|---|---|---|---|---|---|
| attempt_id | str | - | no | f | ORVEX | Id. |  | ACC-000001 | contract header + non-null check (K01,K02) |
| source_dataset_id | str | - | no | f | registry | Source. | observed: RW-01, RW-02, RW-03, RW-04, RW-05, RW-06, RW-07, RW-08 | RW-01 | contract header + non-null check (K01,K02) |
| media_or_file_id | str | - | yes | f | ORVEX | Item. |  | search:speech:0 | contract header + non-null check (K01,K02) |
| url | str | - | yes | f | ORVEX | URL (blank for policy-skipped rows). |  | https://commons.wikimedia.org/w/api.php?action=query&format= | contract header + non-null check (K01,K02) |
| attempt_time_utc | datetime | UTC ISO-8601 (precision in time_precision) | no | f | ORVEX | Time. |  | 2026-10-26T06:13:43Z | contract header + non-null check (K01,K02) |
| method | str | - | no | f | ORVEX | http_get / api. | observed: api, http_get, policy | api | contract header + non-null check (K01,K02) |
| http_status | int | - | yes | d | response | HTTP status. |  | 200 | contract header + non-null check (K01,K02) |
| result_category | str | - | no | f | ORVEX | ok / failed / skipped_terms / skipped_budget. | observed: failed, ok, skipped_terms | ok | contract header + non-null check (K01,K02) |
| terms_decision | str | - | no | f | policy | Decision. | observed: annotation_file_dataset_licence_not_stated, cc-by-4.0_per_card, media rights not held by dataset authors; no third-party downloader / platform scraping used, n/a, not_bypassed, open_access_cc_by_4.0, permitted_by_licence_or_open_access | permitted_by_licence_or_open_access | contract header + non-null check (K01,K02) |
| retry_count | int | - | no | f | ORVEX | Retries. |  | 0 | contract header + non-null check (K01,K02) |
| bytes | int | bytes | yes | d | response | Bytes. |  | 120502 | contract header + non-null check (K01,K02) |
| sha256 | str | - | yes | d | hashlib | Hash. |  | fee8a7d2305afb50e143175aa5baab8f6733ae21a7ef7050519c38400620 | contract header + non-null check (K01,K02) |
| final_status | str | - | no | f | VOC.access_status | Final status. | observed: access_not_available, downloaded_authorized, metadata_only, not_found | downloaded_authorized | contract header + non-null check (K01,K02) |
| note | str | - | yes | f | ORVEX | Note. | observed: Gate 1 interactive download, downloaded during Gate 1 (interactive request); md5 verified against Zenodo record, media not requested, self signed certificate in certificate chain; TLS verification not bypassed, suggested lead returned 404 | downloaded during Gate 1 (interactive request); md5 verified | contract header + non-null check (K01,K02) |

## split_manifest
- File: `data/derived/splits/split_manifest.csv` — rows: **305** — phase: phase1
- Purpose: Source-family level split assignment.

| column | type | unit / timezone | nullable | origin | lineage (source field / rule) | definition | allowed values | example | validation |
|---|---|---|---|---|---|---|---|---|---|
| split_version | str | - | no | f | ORVEX | Version. | observed: split-v2 | split-v2 | contract header + non-null check (K01,K02) |
| source_family_id | str | - | no | f | master | Root source. |  | RW-CMN-P10491224 | contract header + non-null check (K01,K02) |
| source_dataset_id | str | - | no | f | registry | Dataset. | observed: RW-01, RW-02 | RW-01 | contract header + non-null check (K01,K02) |
| split | str | - | no | c | hash rule | Assigned split. | train, val, test, excluded | train | contract header + non-null check (K01,K02); vocabulary |
| assignment_method | str | - | no | f | ORVEX | Rule. | observed: Commons: whole search themes assigned (sorted, stride-7 over 14/3/3 pattern per 20); ANAKIN: per family, same pattern over (manipulation type, id) | Commons: whole search themes assigned (sorted, stride-7 over | contract header + non-null check (K01,K02) |
| seed | str | - | no | f | ORVEX | Seed. | observed: orvex-split-20261026 | orvex-split-20261026 | contract header + non-null check (K01,K02) |
| domain_stratum | str | - | yes | f | search theme / manipulation type | Stratum. |  | education | contract header + non-null check (K01,K02) |
| n_family_items | int | - | no | d | count | Items in family. |  | 22 | contract header + non-null check (K01,K02) |
| n_native_edges | int | - | no | d | count | Native edges. |  | 0 | contract header + non-null check (K01,K02) |
| heldout_transformations_in_family | str | - | yes | c | lineage | Held-out transformations present. | observed: audio_noise_mix\|mirror_color_shift\|reupload_sim\|speed_change, mirror_color_shift\|reupload_sim\|speed_change | audio_noise_mix\|mirror_color_shift\|reupload_sim\|speed_change | contract header + non-null check (K01,K02) |

## experiment_registry
- File: `data/derived/tables/experiment_registry.csv` — rows: **8** — phase: phase1
- Purpose: Evaluation registry. Holds only the non-learned dHash sanity baseline (BASE-DHASH-v1); no ORVEX model has been trained.

| column | type | unit / timezone | nullable | origin | lineage (source field / rule) | definition | allowed values | example | validation |
|---|---|---|---|---|---|---|---|---|---|
| experiment_id | str | - | no | f | ORVEX | Id. | observed: BASE-DHASH-v1-01, BASE-DHASH-v1-02, BASE-DHASH-v1-03, BASE-DHASH-v1-04, BASE-DHASH-v1-05, BASE-DHASH-v1-06, BASE-DHASH-v1-07, BASE-DHASH-v1-08 | BASE-DHASH-v1-01 | contract header + non-null check (K01,K02) |
| dataset_versions | str | - | no | f | ORVEX | Dataset versions. | observed: tables snapshot of 2026-10-26 (see checksums.sha256) | tables snapshot of 2026-10-26 (see checksums.sha256) | contract header + non-null check (K01,K02) |
| split_version | str | - | no | f | ORVEX | Split. | observed: split-v1 | split-v1 | contract header + non-null check (K01,K02) |
| label_map_version | str | - | yes | f | ORVEX | Label map. | observed: labelmap-v1 | labelmap-v1 | contract header + non-null check (K01,K02) |
| model_version | str | - | yes | f | ORVEX | Model. | observed: none: non-learned baseline, threshold fixed a priori 0.45; NOT the ORVEX relationship model | none: non-learned baseline, threshold fixed a priori 0.45; N | contract header + non-null check (K01,K02) |
| feature_version | str | - | yes | f | ORVEX | Feature set. | observed: dhash24-frame-match v1 (non-learned) | dhash24-frame-match v1 (non-learned) | contract header + non-null check (K01,K02) |
| metric_name | str | - | yes | f | ORVEX | Metric. | observed: pair_scoring_latency_ms, roc_auc_related_vs_unrelated_test, roc_auc_related_vs_unrelated_train, roc_auc_related_vs_unrelated_val, roc_auc_test_hard_negatives_only, roc_auc_test_heldout_lineage_positives, roc_auc_test_without_heldout_lineage, temporal_start_mae_fraction | roc_auc_related_vs_unrelated_train | contract header + non-null check (K01,K02) |
| metric_value | float | - | yes | f | ORVEX | Value. |  | 0.8734 | contract header + non-null check (K01,K02) |
| protocol | str | - | yes | f | ORVEX | Protocol. | observed: all labelled pairs in test split, score = max directional matched-frame fraction, all labelled pairs in train split, score = max directional matched-frame fraction, all labelled pairs in val split, score = max directional matched-frame fraction, mean CPU time per pair, 24x24 Hamming matrix (not end-to-end time-to-detection), test split excluding held-out transformation lineage, test split, same-theme hard negatives only (blank = fewer than 20 negatives), test split: held-out-lineage positives vs all negatives, trim variants vs their roots, first-frame match position | all labelled pairs in train split, score = max directional m | contract header + non-null check (K01,K02) |
| heldout_policy | str | - | yes | f | ORVEX | Held-out policy. | observed: T11-T14 lineage test-only; reported separately | T11-T14 lineage test-only; reported separately | contract header + non-null check (K01,K02) |
| report_path | str | - | yes | f | ORVEX | Report. | observed: docs/datasets/necessity_audit/dhash_baseline_results.json | docs/datasets/necessity_audit/dhash_baseline_results.json | contract header + non-null check (K01,K02) |
| leakage_test_result | str | - | yes | f | ORVEX | Leakage result. | observed: K13/K14 pass in the same audit run | K13/K14 pass in the same audit run | contract header + non-null check (K01,K02) |

## duplicate_map
- File: `data/derived/tables/duplicate_map.csv` — rows: **378** — phase: both
- Purpose: Exact/near duplicates and cross-version repeats; canonical record kept.

| column | type | unit / timezone | nullable | origin | lineage (source field / rule) | definition | allowed values | example | validation |
|---|---|---|---|---|---|---|---|---|---|
| duplicate_id | str | - | no | f | ORVEX | Id. |  | DUP-00001 | contract header + non-null check (K01,K02) |
| canonical_media_id | str | - | no | f | master | Kept record. |  | RW-CMN-P128562512 | contract header + non-null check (K01,K02) |
| duplicate_media_id | str | - | no | f | master | Duplicate record. |  | RW-CMN-P191996630 | contract header + non-null check (K01,K02) |
| duplicate_type | str | - | no | c | rule | exact_hash / near_duplicate_perceptual / same_url_across_versions / same_platform_id_across_sources. | observed: near_duplicate_perceptual, same_platform_id_across_sources, same_url_across_versions, same_url_within_source | near_duplicate_perceptual | contract header + non-null check (K01,K02) |
| evidence | str | - | no | d | hash/dHash/URL | Evidence. |  | dHash24 frame match 0.58 (threshold 0.45) | contract header + non-null check (K01,K02) |
| resolution | str | - | no | f | ORVEX | What was done. | observed: both records kept (distinct native annotations); linked, not double counted in statistics, canonical = first occurrence; repeat kept for its own metadata, canonical=FVC2018 record; older version kept for its extra native fields, excluded_from_variants_original_file_kept | excluded_from_variants_original_file_kept | contract header + non-null check (K01,K02) |

## group_examples
- File: `data/derived/tables/group_examples.csv` — rows: **110** — phase: phase1
- Purpose: Groups of 6 videos (4 related family members + 2 distractors) with ground-truth edges (Module 3: compare 5-6 videos).

| column | type | unit / timezone | nullable | origin | lineage (source field / rule) | definition | allowed values | example | validation |
|---|---|---|---|---|---|---|---|---|---|
| group_id | str | - | no | f | ORVEX | Group id. |  | GRP-00001 | contract header + non-null check (K01,K02) |
| source_family_id | str | - | no | c | root source | Family of the related members. |  | RW-CMN-P10491224 | contract header + non-null check (K01,K02) |
| member_media_ids | str | - | no | f | master/variants | Pipe-separated members (related + distractors). |  | CV-P10491224-V15\|CV-P10491224-V06\|CV-P10491224-V05\|CV-P10491 | contract header + non-null check (K01,K02) |
| n_members | int | - | no | d | count | Number of members. |  | 6 | contract header + non-null check (K01,K02) |
| family_member_ids | str | - | no | f | variants | Related members. |  | CV-P10491224-V15\|CV-P10491224-V06\|CV-P10491224-V05\|CV-P10491 | contract header + non-null check (K01,K02) |
| distractor_ids | str | - | yes | f | other families in same split | Unrelated members. |  | CV-P150038214-V06\|RW-CMN-P167507705 | contract header + non-null check (K01,K02) |
| truth_edges | str | - | yes | c | controlled lineage | Nearest-selected-ancestor edges parent>child among family members. |  | RW-CMN-P105004791>CV-P105004791-V09;RW-CMN-P105004791>CV-P10 | contract header + non-null check (K01,K02) |
| n_truth_edges | int | - | no | d | count | Number of edges. |  | 0 | contract header + non-null check (K01,K02) |
| split | str | - | no | c | split_manifest | Split. | train, val, test, excluded | train | contract header + non-null check (K01,K02); vocabulary |
| split_version | str | - | no | f | ORVEX | Version. | observed: split-v2 | split-v2 | contract header + non-null check (K01,K02) |
| label_origin | str | - | no | f | ORVEX | controlled_lineage. | observed: controlled_lineage | controlled_lineage | contract header + non-null check (K01,K02) |
| evidence_id | str | - | yes | f | ledger | Evidence. | observed: EV-NEG-RULE | EV-NEG-RULE | contract header + non-null check (K01,K02) |
| created_utc | datetime | UTC ISO-8601 (precision in time_precision) | no | f | ORVEX | Time. |  | 2026-10-26T18:06:44Z | contract header + non-null check (K01,K02) |
