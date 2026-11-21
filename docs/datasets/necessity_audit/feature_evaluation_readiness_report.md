# Feature and Evaluation Readiness Report

Generated 2026-10-26T18:48:52Z. Features exist only where listed as computed; the baseline below is **not** the ORVEX model.

## Computed (real files, hashes in feature_manifest)
| feature | records |
|---|---|
| visual_dhash24 | 1726 |
| audio_pcm_md5_8k | 1467 |
| audio_envelope_1s | 1467 |

## Non-learned dHash baseline (BASE-DHASH-v1, threshold 0.45 fixed a priori, nothing tuned)
| metric | value |
|---|---|
| pairs scored | 9928 |
| ROC-AUC train / val / test | 0.8734 / 0.8992 / 0.8307 |
| ROC-AUC test excluding held-out lineage | 0.8486 |
| ROC-AUC test, held-out-lineage positives | 0.7922 |
| test negatives by hardness | {'easy': 114, 'hard': 36} |
| ROC-AUC test hard negatives only | 0.8307 |
| pair scoring latency | 0.0194 ms/pair (not time-to-detection) |
| temporal start estimation (trims) | MAE 0.0758 of duration; 70% within 0.05 |

### Detection by transformation (direct derivation pairs, score >= 0.45)
| transformation | pairs | detected | audio identical |
|---|---|---|---|
| audio_mute | 42 | 0.976 | 0.0 |
| audio_noise_mix | 5 | 1.0 | 0.0 |
| audio_replace | 55 | 0.964 | 0.0 |
| caption_burn_in | 110 | 0.982 | 0.009 |
| crop_center | 110 | 0.036 | 0.009 |
| mirror_color_shift | 7 | 0.143 | 0.0 |
| recompress_low | 220 | 0.986 | 0.014 |
| reencode_hq | 55 | 0.964 | 0.0 |
| reupload_sim | 7 | 0.857 | 0.0 |
| speed_change | 7 | 1.0 | 0.0 |
| trim_head | 55 | 0.745 | 0.0 |
| trim_middle | 55 | 0.673 | 0.0 |
| trim_tail | 55 | 0.8 | 0.0 |
| watermark_overlay | 165 | 0.988 | 0.012 |

**Reading:** hashes are robust to recompression, captions, watermarks and audio edits but weak for crop_center, mirror_color_shift, trim_middle, trim_head. This proves the fingerprints are usable for candidate retrieval and ground-truth sanity checks and shows exactly where learned visual embeddings are needed — a **computation/software** gap, not a data gap.

## Missing computations (not data)
| computation | what is missing | storage |
|---|---|---|
| visual embeddings | software: PyTorch >= 2.4 or an embedding model (installed torch 2.3.1 disables transformers); weights not counted as dataset payload | < 0.1 GB |
| audio embeddings | software: audio model | < 0.05 GB |
| speech transcription (ASR) | software: whisper-class model not installed | < 0.05 GB transcripts |
| OCR | software: no OCR engine installed; caption ground truth exists to validate it | < 0.05 GB |
| dense frame sampling / temporal alignment | recompute features at 1 fps (24 frames give ~4% granularity) | < 0.1 GB |
| relationship scoring + confidence calibration | model training on existing pairs | < 0.2 GB |
| evaluation harness + time-to-detection | software | negligible |

## Evaluation limits
- Commons test families: 7; ANAKIN test pairs: 36 (families, not pairs). Per-family confidence intervals will be wide.
- Hard negatives per split: {'train': 157, 'val': 29, 'test': 36}.
- No ORVEX model exists: no calibrated confidences, false-positive rates at deployment thresholds, or time-to-detection.