# Transformation Coverage Report

Generated 2026-10-26T18:48:52Z. All counts measured from `controlled_variant_registry` and re-validated independently with ffprobe in this audit.

## Independent re-validation of all passed variants
| check | result |
|---|---|
| passed_variants | 1131 |
| readable_by_independent_ffprobe | 1131 |
| duration_matches_registry | 1131 |
| carries_controlled_variant_metadata_tag | 1131 |
| parent_chain_complete | 1131 |
| roots_eligible | 1131 |
| audio_variants | 99 |
| audio_donor_documented_real_eligible | 99 |
| caption_variants | 110 |
| caption_variants_with_real_source_text | 110 |
| run_log_return0_and_passed | 1131 |
| tool_params_run_recorded | 1131 |
| failed_variants | 2 |
| failed_excluded_and_no_file | 2 |
| leakage_check | True |
| heldout_check | True |

## Coverage by transformation and split (passed variants)
| transformation | train | val | test | purpose / evaluation value |
|---|---|---|---|---|
| audio_mute | 33 | 4 | 5 | audio removal |
| audio_noise_mix | 33 | 6 | 5 | TEST-ONLY unseen audio mix |
| audio_replace | 40 | 8 | 7 | audio replaced by another real recording (PDF: audio replacement) |
| caption_burn_in | 80 | 16 | 14 | text overlay, mismatched real title (PDF: misleading captions) - controlled pairing |
| crop_center | 80 | 16 | 14 | spatial edit (PDF: cropping) |
| mirror_color_shift | 40 | 8 | 7 | TEST-ONLY unseen spatial+colour edit |
| recompress_low | 160 | 32 | 28 | platform recompression: most common real-world degradation |
| reencode_hq | 40 | 8 | 7 | identity-preserving format change: relationship model must not over-react to codec |
| reupload_sim | 40 | 8 | 7 | TEST-ONLY screen-record-like re-upload |
| speed_change | 40 | 8 | 7 | TEST-ONLY unseen temporal edit |
| trim_head | 40 | 8 | 7 | partial temporal copy, start cut |
| trim_middle | 40 | 8 | 7 | partial temporal copy / segment alignment (PDF: trimming) |
| trim_tail | 40 | 8 | 7 | partial temporal copy, end cut |
| watermark_overlay | 120 | 24 | 21 | overlay that changes pixels but not meaning |

## PDF-required transformation families
| PDF family | transformations | status |
|---|---|---|
| trimming | T03/T04/T05 | covered |
| cropping | T06 | covered |
| caption addition | T07 (+T08 watermark) | covered; caption text is another real record's title, labelled as controlled pairing |
| audio replacement/change | T09, T10, T14 | covered; audio from other real recordings only |
| recompression | T01, T02, T13 | covered |
| multi-step / indirect derivation | chains C1-C5 | covered: 385 variants at depth >= 2 |

## Genuine gaps and decision
- **Coverage gap found:** hard (same-theme) negatives per split = {'train': 157, 'val': 29, 'test': 36}; `split-v1` had none in the test split (found by this audit, fixed by theme-grouped `split-v2` without new data).
- Transformations not generated: audio_mute / audio_noise_mix skipped for 11 eligible sources without an audio track (nothing to remove/mix). No new transformation is justified.
- Per-split counts of the four held-out types are small (see table); this is a statistical-power limit of the 55-source corpus, not a missing transformation.
- **Not proposed (and why):** AI voice, face swap, synthetic video, text-to-video (forbidden by policy); more first-generation variants of the same sources (adds near-identical data, no new evaluation value); extra transformation types before the existing ones have been evaluated with a model.