# ORVEX Dataset QA Report

Generated 2026-10-26T18:48:15Z by running real checks on the real files (`data/reports/acceptance_checks.json`).

## Acceptance checks run
| check | result | measured evidence |
|---|---|---|
| K01_schema_columns | PASS | 15 tables, 306 contract columns; mismatches: none |
| K02_required_nonnull | PASS | non-nullable columns with blanks: none |
| K03_unique_ids | PASS | duplicate media_id=0, variant ids=0, relationship ids=0, overlap natural/variant ids=0; media=252270, variants=1133, edges=299875 |
| K04_variant_lineage | PASS | 1131 passed variants; chains not ending in an eligible real-world root / invalid audio or caption provenance: 0 |
| K05_separation | PASS | separation violations: 0; controlled files on disk: 1132 |
| K06_hashes | PASS | 1727 local media files re-hashed; missing or hash mismatch: 0 |
| K07_metadata_only_clean | PASS | 251674 metadata_only records; with a local path/hash (would be a false 'downloaded' claim): 0 |
| K08_licence_gate | PASS | 96 downloaded Commons files; licences: {'CC BY-SA 4.0': 35, 'Public domain': 25, 'CC BY 4.0': 12, 'CC BY-SA 3.0': 8, 'CC BY 3.0': 7, 'CC0': 6, 'CC BY 2.0': 1, 'CC BY-SA 2.0': 1, 'CC BY-SA 3.0 nl': 1}; outside allowed set: 0 |
| K09_real_world_only | PASS | variant tools={'ffmpeg'}; sources used for variants={'RW-01'}; catalogue contains only FFmpeg filters (no generative models, no TTS) |
| K10_transform_coverage | PASS | passed by transformation={'recompress_low': 220, 'watermark_overlay': 165, 'crop_center': 110, 'caption_burn_in': 110, 'reencode_hq': 55, 'trim_middle': 55, 'trim_head': 55, 'trim_tail': 55, 'audio_replace': 55, 'mirror_color_shift': 55, 'speed_change': 55, 'reupload_sim': 55, 'audio_noise_mix': 44, 'audio_mute': 42}; multi-step (depth>=2) variants=385; failed=2 |
| K11_controlled_edges | PASS | controlled lineage edges=1131 for 1131 passed variants; variants without an edge: 0 |
| K12_native_edges_preserved | PASS | native edges by dataset={'RW-07': 278885, 'RW-06': 12564, 'RW-03': 5199, 'RW-02': 1997}; distinct native labels kept=16 |
| K13_split_leakage | PASS | 9928 model pairs checked across 305 families; pairs/variants whose members are not wholly inside one split: 0; splits={'train': 215, 'val': 47, 'test': 43} |
| K14_heldout_policy | PASS | held-out transformation types ['T11', 'T12', 'T13', 'T14']; training/validation uses of held-out lineage: 0; test pairs with held-out lineage: 525 |
| K15_pair_labels | PASS | 13659 pairs; class counts={'same_family_other': 5827, 'sibling_same_parent': 4759, 'unrelated_distinct_source': 1142, 'direct_derivation': 1131, 'indirect_derivation': 495, 'edited_version': 250, 'audio_source_only_not_visual_derivation': 55}; label inconsistencies=0 |
| K16_budget | PASS | dataset payload (everything under data/) = 17241740608 bytes = 17.24 GB (decimal) = 16.06 GiB; cap 30 GB, target <=27 GB |
| K17_features | PASS | visual dHash computed for 1726 of 1727 local media (failures ['RW-CMN-P89310222']; all are QC-flagged unusable files excluded from variants: True); NOT computed, no placeholder files: ['visual_embedding', 'audio_embedding', 'ocr_text', 'asr_transcript', 'text_embedding', 'scene_boundaries'] |
| K18_native_files_intact | PASS | 4 official archives re-verified against Zenodo md5; failures: none |
| K19_duplicates | PASS | 378 duplicate records mapped {'same_url_across_versions': 237, 'same_platform_id_across_sources': 119, 'same_url_within_source': 18, 'near_duplicate_perceptual': 4}; dangling ids: 0 |
| K20_campaign_honesty | PASS | campaign clusters=0 (blocked: no multi-account time-stamped distribution evidence); observations with accounts=1031, with publish time=258303, total=352702 |
| K21_policy_present | PASS | policy file present, 1711 words; missing sections: none |
| K22_access_log | PASS | 729 logged attempts: ok=724, failed=2, policy-skipped=3; downloaded media files=596 |
| K23_media_playable | PASS | 596 downloaded real media probed; flagged unplayable: 2 (kept in master, excluded from variants) |
| K24_registry | PASS | 31 candidates; statuses={'research_lead_unverified': 9, 'excluded_not_real_world_for_scope': 6, 'included_metadata_only': 5, 'excluded_duplicate_version': 3, 'excluded_license': 3, 'included_selected_subset': 2, 'excluded_inaccessible': 2, 'legal_review_required': 1}; flagged unverified research leads=15; invalid statuses=0 |
| K25_groups | PASS | 110 groups of 5-6 videos; truth edges total=85 |
| K26_failed_not_trained | PASS | failed variants=2; failed variants marked trainable or retained as files: 0 |
| K27_label_dimensions_separate | PASS | authenticity/misleading labels live only in the media master (edges carry relation labels only); FVC records with an invented authenticity status: 0; issues: none |
| K28_no_zero_byte_or_truncated | PASS | zero-byte files: 0; downloaded media with duration 0/unknown: ['RW-CMN-P89310222'] (all QC-excluded from variants: True) |
| K29_attribution_complete | PASS | 96 attribution rows for 96 downloaded Commons files; rows missing licence/licence URL/file page: 0; author not stated on Commons (uploader link only): 2 |
| K30_manifests_present | PASS | manifests present (8); checksum lines=1883 vs files on disk 1883; crosswalk rows=252270 vs media master 252270 |
| K31_label_dimensions | PASS | coordination_status=not_assessed on 252270 media and 352702 observations; evidence_status values on edges: {'source_annotation': 298645, 'controlled_transformation_log': 1230} |
| K32_covid_dataset | PASS | RW-31 records=8122 (all metadata_only, bad=0); tweet share-references with derived time=257326; 2236 fall outside the dataset's stated Nov 2019-Jun 2020 window and are flagged second_derived_unverified (unflagged: 0); facebook share refs=83222 |
| K33_layer_a_read_only | PASS | 729 Layer A files (media + raw metadata); still writable: 0 |
| K34_gitignore | PASS | .gitignore excludes data/, tools/, secrets (no git repository exists yet) |

## Records
| table | rows |
|---|---|
| source_registry | 31 |
| real_world_media_master | 252,270 |
| controlled_variant_registry | 1,133 |
| media_relationship_edges | 299,875 |
| platform_observations | 352,702 |
| evidence_ledger | 1,237 |
| feature_manifest | 5,187 |
| training_pairs | 13,659 |
| campaign_candidate_clusters | 0 |
| transformation_run_log | 1,133 |
| download_access_attempt_log | 729 |
| split_manifest | 305 |
| experiment_registry | 8 |
| duplicate_map | 378 |
| group_examples | 110 |

## Real-world media master by source
| source | records |
|---|---|
| RW-06 | 225,960 |
| RW-07 | 9,207 |
| RW-31 | 8,122 |
| RW-03 | 5,579 |
| RW-02 | 3,020 |
| RW-04 | 227 |
| RW-01 | 96 |
| RW-05 | 59 |

| access status | records |
|---|---|
| metadata_only | 251,674 |
| downloaded_authorized | 596 |

## QC flags on downloaded Commons media
| flag | files |
|---|---|
| too_long(>120s) | 25 |
| no_audio | 17 |
| too_short(<8s) | 8 |
| duplicate | 4 |
| non_real_world_synthetic_or_cgi | 4 |
| mostly_black | 1 |
| decode_errors | 1 |

Usable as variant sources: 55 of 96 downloaded Commons files.

## Controlled variants
| transformation (passed) | count |
|---|---|
| recompress_low | 220 |
| watermark_overlay | 165 |
| crop_center | 110 |
| caption_burn_in | 110 |
| reencode_hq | 55 |
| trim_middle | 55 |
| trim_head | 55 |
| trim_tail | 55 |
| audio_replace | 55 |
| mirror_color_shift | 55 |
| speed_change | 55 |
| reupload_sim | 55 |
| audio_noise_mix | 44 |
| audio_mute | 42 |

Failed variants: 2. Transformations not generated because the parent had no audio (T10/T14): see run log counts below.

## Splits and pairs
| split (families) | count |
|---|---|
| train | 215 |
| val | 47 |
| test | 43 |

| pair class | count |
|---|---|
| same_family_other | 5827 |
| sibling_same_parent | 4759 |
| unrelated_distinct_source | 1142 |
| direct_derivation | 1131 |
| indirect_derivation | 495 |
| edited_version | 250 |
| audio_source_only_not_visual_derivation | 55 |

| pair split | count |
|---|---|
| train | 6878 |
| excluded | 3731 |
| test | 1721 |
| val | 1329 |

## Native relationship edges
| source / normalised type | edges |
|---|---|
| RW-02 / edited_version_of_trimmed_clip | 1023 |
| RW-02 / trimmed_segment_of_full_video | 974 |
| RW-03 / same_cascade_repost_or_near_duplicate | 5199 |
| RW-06 / IS | 3543 |
| RW-06 / complementary_scene_different_camera_same_incident | 1855 |
| RW-06 / duplicate_scene_same_camera_footage | 5839 |
| RW-06 / near_duplicate | 1327 |
| RW-07 / partial_temporal_copy | 278885 |

## Duplicates
| type | records |
|---|---|
| same_url_across_versions | 237 |
| same_platform_id_across_sources | 119 |
| same_url_within_source | 18 |
| near_duplicate_perceptual | 4 |

## Missingness (columns with >50% blanks in the media master)
| column | blank |
|---|---|
| title | 95% |
| description_caption | 97% |
| publisher_account_id | 99% |
| published_time_utc | 100% |
| observed_time_utc | 100% |
| duration_s | 100% |
| width | 100% |
| height | 100% |
| fps | 100% |
| video_codec | 100% |
| audio_codec | 100% |
| has_audio | 100% |
| container | 100% |
| file_bytes | 100% |
| local_path | 100% |
| sha256 | 100% |
| native_authenticity_label | 98% |
| native_misleading_label | 94% |
| native_manipulation_type | 100% |
| perceptual_hash_ref | 100% |
| qc_flags | 100% |
| duplicate_of_media_id | 100% |

## Known limitations
- Only Commons media (RW-01) are source material for controlled variants; ANAKIN is evaluation-only.
- FVC/FIVR/VCSL media bytes are not available to ORVEX (metadata only).
- OCR/ASR/embeddings are not computed.
- Campaign clusters cannot be created honestly from available data.
- Hard negatives share a search theme, not a verified event; labelled `uncertain`.
- VCDB, WildDeepfake, Deepfake-Eval-2024, VSC, CC_WEB_VIDEO, SVD, NIST, Pushshift are unverified leads.

## Cross-check additions
### Native label distributions (kept verbatim)
| source | native label / manipulation type | records |
|---|---|---|
| RW-03 | debunked | 89 |
| RW-03 | fake | 2920 |
| RW-03 | parody | 66 |
| RW-03 | real | 2164 |
| RW-03 | uncertain | 340 |
| RW-04 | fake | 117 |
| RW-04 | real | 110 |
| RW-05 | fake | 59 |
| RW-02 | audio | 161 |
| RW-02 | frame-level | 172 |
| RW-02 | inpainting | 190 |
| RW-02 | splicing | 228 |
| RW-02 | swap | 272 |
| RW-04 | Tampering | 32 |
| RW-04 | Tampering (audio) | 2 |
| RW-04 | Tampering -heavily re-processed | 1 |

| source | native relation label | edges |
|---|---|---|
| RW-02 | audio | 161 |
| RW-02 | frame-level | 172 |
| RW-02 | inpainting | 190 |
| RW-02 | splicing | 228 |
| RW-02 | swap | 272 |
| RW-02 | trimmed_from_full | 974 |
| RW-03 | debunked | 89 |
| RW-03 | fake | 2720 |
| RW-03 | parody | 66 |
| RW-03 | real | 1984 |
| RW-03 | uncertain | 340 |
| RW-06 | CS | 1855 |
| RW-06 | DS | 5839 |
| RW-06 | IS | 3543 |
| RW-06 | ND | 1327 |
| RW-07 | copied_segment | 278885 |

### Conflicting source labels across versions (same canonical URL)
4 conflicts found among 237 cross-version URL matches.

| canonical | label | duplicate | label | URL |
|---|---|---|---|---|
| RW-FVC18-f182-18 | parody | RW-FVCv20-fvc-54 | fake | canonical URL equal: https://youtube.com/watch?v=h-AkAF2Tc1k |
| RW-FVC18-f76-8 | debunked | RW-FVCv20-fvc-63 | fake | canonical URL equal: https://youtube.com/watch?v=r1NkMQ8FGec |
| RW-FVC18-f192-12 | real | RW-FVCv20-fvc-113 | fake | canonical URL equal: https://youtube.com/watch?v=k6PxMRUgmbA |
| RW-FVC18-f182-18 | parody | RW-FVCv10-fvc-56 | fake | canonical URL equal: https://youtube.com/watch?v=h-AkAF2Tc1k |

### Transformations not generated (and why)
- audio_mute (T10): 13 of 55 sources skipped (2 more failed validation) — parent has no audio track or failed validation.
- audio_noise_mix (T14): 11 of 55 sources skipped — parent has no audio track.
- Voice cloning, face swap, TTS, text-to-video: **intentionally not generated** (no generative AI rule). Audio replacement uses only real recordings.

### Variant storage by transformation type (measured)
| transformation | files | size |
|---|---|---|
| audio_mute | 42 | 694,924,674 B (0.695 GB / 0.647 GiB) |
| audio_noise_mix | 44 | 732,230,136 B (0.732 GB / 0.682 GiB) |
| audio_replace | 55 | 905,945,665 B (0.906 GB / 0.844 GiB) |
| caption_burn_in | 110 | 1,415,986,841 B (1.416 GB / 1.319 GiB) |
| crop_center | 110 | 1,123,018,858 B (1.123 GB / 1.046 GiB) |
| mirror_color_shift | 55 | 958,683,418 B (0.959 GB / 0.893 GiB) |
| recompress_low | 220 | 175,236,156 B (0.175 GB / 0.163 GiB) |
| reencode_hq | 55 | 1,698,942,064 B (1.699 GB / 1.582 GiB) |
| reupload_sim | 55 | 28,455,838 B (0.028 GB / 0.027 GiB) |
| speed_change | 55 | 786,004,353 B (0.786 GB / 0.732 GiB) |
| trim_head | 55 | 723,213,932 B (0.723 GB / 0.674 GiB) |
| trim_middle | 55 | 555,276,230 B (0.555 GB / 0.517 GiB) |
| trim_tail | 55 | 684,887,753 B (0.685 GB / 0.638 GiB) |
| watermark_overlay | 165 | 2,014,792,876 B (2.015 GB / 1.876 GiB) |

### Per-source-dataset field completeness
| source | records | blank source_url | blank platform id | blank publish time | local files |
|---|---|---|---|---|---|
| RW-01 | 96 | 0% | 0% | 0% | 96 |
| RW-02 | 3020 | 0% | 0% | 100% | 500 |
| RW-03 | 5579 | 0% | 0% | 100% | 0 |
| RW-04 | 227 | 0% | 0% | 100% | 0 |
| RW-05 | 59 | 0% | 0% | 100% | 0 |
| RW-06 | 225960 | 0% | 0% | 100% | 0 |
| RW-07 | 9207 | 0% | 0% | 100% | 0 |
| RW-31 | 8122 | 0% | 0% | 89% | 0 |

### Not assessed
- Liveness of source URLs (broken/deleted videos) was **not** checked: requesting platform URLs for 240k records would breach the no-hammering/no-scraping rule; those records stay `metadata_only`.
- Truncated-file detection is limited to ffprobe/ffmpeg decode errors and zero duration.