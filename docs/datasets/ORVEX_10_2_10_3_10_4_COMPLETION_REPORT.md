# ORVEX Roadmap 10.2 / 10.3 / 10.4 — Completion Report

Date: 2026-10-26. All numbers below were measured from the files in `<repo>\data\` by `scripts/datasets/audit.py` and `tests/test_dataset_package.py` (**38 passed**: 34 acceptance checks + 4 structural tests). PDF: `ORVEX_Complete_Project_Specification.pdf`, 13 pages, SHA-256 `55cbb2d8…`, re-extracted at the final audit (`data/reports/pdf_text_final_audit.txt`; Modules 1–9, Phase 1/2 and 10.2–10.4 all located).

## 1. Status
| Item | Status | Why |
|---|---|---|
| **10.2 Find and collect source videos** | **PARTIALLY COMPLETE** | Census of 31 candidates with official-source verification for 16; licensed real media collected (96 Commons files, 250 ANAKIN pairs). Not complete because 15 candidates remain unverified research leads, and the naturally-circulating datasets (FVC, FIVR-200K, VCSL) provide URLs only, so their media bytes could not lawfully be obtained. |
| **10.3 Clean and label the dataset** | **COMPLETE for the roadmap deliverable** ("small labelled dataset with known relationships", split by source). PARTIAL for the wider master-prompt items (OCR/ASR/embeddings, campaign clusters, live platform data) | Duplicates removed, unusable flagged, 1,131 validated variants, 13,659 pairs, 110 groups, source-family splits with test-only transformations, zero leakage. |
| **10.4 Set data and evidence rules** | **COMPLETE** | `ORVEX_DATA_USE_AND_EVIDENCE_POLICY.md`; enforceable parts are tested, manual parts are marked **[manual]**. |
Requirement matrix (40 requirements): **27 PASS, 11 PARTIAL, 2 BLOCKED (R11 campaign detection, R36 time-to-detection), 0 FAIL** (`ORVEX_REQUIREMENT_COVERAGE_MATRIX.csv`).

## 2. Real-world datasets selected (Layer A)
| ID | Dataset (official source) | Eligibility | Licence / access | Present locally | Role |
|---|---|---|---|---|---|
| RW-01 | Wikimedia Commons CC/PD video pool (Commons API) | real user recordings | per-file CC0/PD/CC BY/CC BY-SA, verified via API | **96 videos, 1.69 GB**; **55 usable** as variant sources | source of all variants; real upload records |
| RW-02 | ANAKIN incl. VideoSham ([HF card](https://huggingface.co/datasets/AlexBlck/ANAKIN)) | real clips edited by human editors | cc-by-4.0 per card; underlying Vimeo rights unverified | **250 trimmed+edited pairs (500 videos) + masks, 2.52 GB**; metadata for all 1,023 | native edit pairs (evaluation only) |
| RW-03 | InVID Fake Video Corpus 2018 ([Zenodo 2535479](https://zenodo.org/records/2535479)) | naturally circulating | CC BY 4.0 (annotations); URLs only | 5,579 records (metadata_only) | repost cascades, fake/real labels |
| RW-04 | FVC v2.0 ([1147958](https://zenodo.org/records/1147958)) | same | CC BY 4.0; URLs only | 227 records | extra native fields |
| RW-06 | FIVR-200K ([2564864](https://zenodo.org/records/2564864)) | YouTube news videos | CC BY 4.0; URLs only | 225,960 ids; 12,564 labelled relations | same-incident vs copy labels |
| RW-07 | VCSL ([GitHub](https://github.com/alipay/VCSL)) | YouTube/Bilibili videos | code MIT; **dataset licence not stated**; URLs only | 9,207 videos; 278,885 segment relations | partial-copy annotations |
| RW-31 | Covid-related misinformation videos and their spread ([Zenodo 4557828](https://zenodo.org/records/4557828)), added in the cross-check round | real YouTube videos removed for false COVID information | CC BY 4.0 (metadata); URLs/ids only | 8,122 videos, 420 removal times, 257,326 tweet ids (time derived from the id; 2,236 outside the stated window flagged unverified), 83,222 Facebook post ids | real post timeline; no sharer accounts |
All Zenodo archives re-verified against Zenodo md5 (K18) and by the reproducible fetch script (`s1_fetch_metadata.py`, run and passing).

## 3. Considered but excluded (reasons)
- **Research-created, not naturally circulating** (`excluded_not_real_world_for_scope`): DFDC, FaceForensics++, Celeb-DF/++, FakeAVCeleb, AV-Deepfake1M, NewsCLIPpings (also images).
- **Duplicate/superseded versions:** FVC v1.0 (59 entries, superseded), FVC journal-paper record (PDF only), VideoSham (inside ANAKIN).
- **Licence unclear/footage rights:** HMDB51 (movie footage), UCF101, Kinetics (conflicting licence statements).
- **Inaccessible:** Twitter/X IO archive (application), TikTok Research API (approval). `legal_review_required`: YFCC100M.
- **Unverified research leads (not downloaded):** VCDB (official page TLS certificate invalid — not bypassed; GitHub lead 404), WildDeepfake, Deepfake-Eval-2024, VSC 2022/23, CC_WEB_VIDEO, SVD, NIST Nimble/MFC, Pushshift Telegram, Pacheco/Nizzoli datasets.
Full table with evidence URLs: `data/manifests/source_registry.csv`, `ORVEX_DATASET_SELECTION_AND_BUDGET.md`. Search date 2026-10-26; coverage is systematic but not exhaustive.

## 4. ORVEX-created datasets (Layer B) — all derived from Layer A only
| Dataset | Derived from | Records | Phase | Notes |
|---|---|---|---|---|
| real_world_media_master | RW-01…07, RW-31 | 252,270 | both | normalised master; natural media only |
| controlled_variant_registry (+ 12.5 GB media) | RW-01 media | 1,133 (1,131 passed) | 1 | `media_origin=controlled_variant` |
| media_relationship_edges | RW-02/03/06/07 native + RW-01 lineage | 299,875 (1,230 controlled) | both | native labels kept verbatim |
| platform_observations | RW-01 uploads, RW-03 cascades, RW-31 spread | 352,702 | 2 | 338,485 share references, 8,122 publish, 5,579 cascade members, 420 removals, 96 uploads; accounts only for Commons/COVID channels; FVC has order only |
| evidence_ledger | all | 1,237 | both | |
| feature_manifest (+ 2 jsonl) | RW-01/02 media + variants | 5,187 | both | dHash + audio fingerprints computed |
| training_pairs | variants, ANAKIN | 13,659 (train 6,878 / val 1,329 / test 1,721 / excluded 3,731) | 1 | `split-v2` |
| group_examples (5–6 videos) | variants | 110 | 1 | |
| split_manifest | RW-01, RW-02 | 305 families (215/47/43), `split-v2` theme-grouped | 1 | |
| transformation_run_log, duplicate_map, download_access_attempt_log, source_registry | — | 1,133 / 378 / 729 / 31 | both | |
| campaign_candidate_clusters | — | **0 — BLOCKED** | 2 | no authorised account+time evidence; nothing simulated |
| experiment_registry | — | **8** | 1 | only the non-learned dHash baseline BASE-DHASH-v1; no ORVEX model trained |
Extra (ORVEX-added) columns are listed per table in `ORVEX_COLUMN_LINEAGE.md` and `column_lineage.csv` (300 columns, origin codes a–f).

## 5. Controlled variants
Source: 55 eligible real Commons recordings. Passed by type: recompress_low 220, watermark_overlay 165, crop_center 110, caption_burn_in 110, reencode_hq 55, trim_middle 55, trim_head 55, trim_tail 55, audio_replace 55, mirror_color_shift 55, speed_change 55, reupload_sim 55, audio_noise_mix 44, audio_mute 42. Depth 1: 746, depth 2: 275, depth 3: 110. Audio comes from **another real recording**; caption text is **another real record's title** (origin ids stored). Test-only unseen types: T11–T14. Trainable variants: 673 (after the `split-v2` re-split).
**Failures: 2** (`audio_mute` on two sources: output duration shorter than the parent's container duration because the audio track was longer than the picture) — excluded from training and no file kept. Earlier in the run, 25 failed/killed outputs and 15 sources' variants were removed (see §10).

## 6. Column completeness
`docs/datasets/schema_contract.json` (machine-readable), `ORVEX_DATA_DICTIONARY.md` (every column: type, nullability, origin, lineage, definition, allowed values, example, validation), `ORVEX_COLUMN_LINEAGE.md` (source-field mapping incl. **native fields kept only in raw files**, e.g. FVC Discussed/Appeared/Timestamp, FIVR event headlines, Commons categories). K01/K02 verify every CSV header against the contract and non-nullable columns.

## 7. Problem-statement coverage
Supported by data: Module 1 (dataset creation) PASS; Module 3 pairs/groups with direct/indirect derivation; Module 4 labels (trim, crop, caption, audio replace/mix/mute, recompress, ANAKIN edit types); Module 5 graph edges; Module 9 split/held-out protocol.
**Partial/unsupported:** Module 2 (OCR, ASR, embeddings not computed), Module 6 (no live connector; real times only for Commons), Module 7 (**blocked**), Module 9 (no experiments yet), Phase 2 discovery (candidate pools are metadata-only). Full table: requirement matrix.

## 8. Evidence / data-use rules
`ORVEX_DATA_USE_AND_EVIDENCE_POLICY.md`. Key rules: real-world only; created data only from real media; no generative AI/TTS; E1 similarity / E2 derivation / E3 coordination never merged; relation statuses (controlled/source ground truth, uncertain, unknown); direction only with a cue; FVC "fake" = debunked not AI-generated; FIVR DS/CS/IS are not copy proof; no person/account called malicious; accounts pseudonymised; variants internal, manifests shared.

## 9. Storage
**17.24 GB** measured (decimal) = 16.06 GiB, all of `data/` incl. temp; largest recorded measurement 17.24 GB (`data/manifests/storage_budget.csv` lists every stage). Cap 30 GB, target ≤ 27 GB: respected (K16). By category: variants 12.50 GB, ANAKIN 2.52 GB, Commons 1.69 GB, tables 0.42 GB, raw metadata 0.07 GB, manifests/logs/build 0.05 GB. FFmpeg (0.4 GB) is outside `data/`.

## 10. Validation evidence and problems found
- `python -m pytest tests/test_dataset_package.py` → **31 passed** (27 acceptance checks + 4 structural tests). Checks include re-hashing 1,727 local media files (0 mismatches), split-leakage (0), held-out lineage never in train/val (0), metadata-only never claimed as downloaded (0 violations), licence gate (0 outside allowed set), failed variants not trainable.
- **Real defects found by the checks and fixed:** (1) 28 pairs linked a variant to an audio donor in a different split → now excluded; (2) groups with <5 members → fixed; (3) a feature-failure check was too narrow.
- **Non-real content found and removed:** the first run included a *computer simulation* (Biham-Middleton-Levine traffic model), an ESO artist's-impression animation, a NASA/JPL CGI cutaway movie and a NASA SVS visualisation, plus the NASA "Mars Report" (mixed animation). An automated keyword screen (`non_real_world_synthetic_or_cgi`) plus a documented manual list now excludes them; variants of those 4 roots were deleted, and the 11 other sources that used one of them as audio/caption donor were regenerated with eligible donors (15 sources purged in total). **Screening is by title/category/description, not frame-by-frame review; a human spot-check is recommended.**
- Two hung FFmpeg processes (audio loop encodes) were stopped by me; those variants were recorded as failed and later purged with their sources.
- One real file (RW-CMN-P89310222) has duration 0/no decodable frames: flagged and excluded.

### Cross-check round (second pass against the master prompt)
Found and fixed: (1) no checksum, storage-budget, selection-plan, evaluation-protocol, ID-crosswalk or attribution manifests — now created (`data/manifests/`, `docs/datasets/ORVEX_ATTRIBUTION.md`, `ORVEX_EVALUATION_PROTOCOL.md`); (2) missing `coordination_status`, `evidence_status`, `observation_type`, `evidence_id`, `perceptual_hash_ref` columns — added; (3) data dictionary lacked unit/timezone and lineage lacked source datasets — added; (4) feature records lacked size/hash — filled for all 4,660 computed records; (5) no real spread/timeline data — added RW-31; (6) QA lacked native label distributions, cross-version label conflicts, not-generated transformations, per-type sizes — added; (7) requirement matrix lacked RAG records, time-to-detection and manifests — rows added; (8) originals were writable — now read-only (729 files, K33); `.gitignore` created. Seven new checks (K28–K34) were added; K29, K30 and K32 initially failed because Public-domain files have no licence URL, my checksum threshold was arbitrary, and 2,236 tweet ids decode to dates outside the dataset's stated window — each was corrected honestly (explicit "n/a" licence text, exact file-count comparison, `second_derived_unverified` flag), not by loosening the intent.

### Necessity audit (2026-10-27)
A follow-up audit (`docs/datasets/necessity_audit/ORVEX_NECESSITY_AUDIT_REPORT.md`) concluded that no additional dataset is necessary to proceed; it found that `split-v1` had no hard negatives in the test split, fixed it with a theme-grouped `split-v2`, ran a non-learned dHash baseline, and re-validated all 1,131 variants independently. Figures in this report reflect `split-v2`.

## 11. Limitations and next actions
1. Obtain access/terms for unverified leads (VCDB page certificate, VSC, Deepfake-Eval-2024, Twitter IO, TikTok API) before Phase 2 evaluation on naturally circulating media.
2. Compute OCR, ASR and visual/audio/text embeddings (model phase); then fill `experiment_registry`.
3. Campaign module needs real account+time data; none is simulated here.
4. Negative pairs and hard negatives are `uncertain` (same-theme ≠ proven independent).
5. Re-verify Commons licences and sensitive-flagged items before any public release; human spot-check for non-real footage.
6. Source sample is small (55 sources, 28 themes); scale up with more Commons pulls if statistics demand.
7. No source-URL liveness check was run (240k platform URLs would breach the no-hammering rule); 2,236 derived tweet times are unverified; sharer accounts are absent from every open real dataset found, so campaign clustering stays blocked.
8. The PDF was read in full at Gate 0 and re-extracted and cross-checked (Modules 1-9, Phase 1/2, 10.2-10.4) at the final audit and again in the cross-check round; intermediate gates were not individually logged.
9. 25 Commons files are Public domain and Commons gives no licence text for them; 2 files have no author stated (uploader link only).

## 12. Files
Created: `scripts/datasets/*.py` (schema, common, s1–s6, s4b, candidates, catalogue modules, audit, transformations), `tests/test_dataset_package.py`, `docs/datasets/*` (policy, dictionary, lineage, catalogue, selection/budget, QA report, matrix, schema_contract.json, column_lineage.csv, this report), `data/**` (real_world, controlled_variants, derived, manifests, reports), `tools/ffmpeg-9.0.2-essentials_build` (SHA-256 verified against the publisher). Added in the cross-check round: `scripts/datasets/{s5b_feature_hashes,s7_manifests,patch_round2,patch_round3,patch_round4,update_report}.py`, `docs/datasets/{ORVEX_ATTRIBUTION,ORVEX_EVALUATION_PROTOCOL}.md`, `data/manifests/{checksums.sha256,storage_budget.csv,selection_plan.json,native_id_crosswalk.csv,attribution.csv,evaluation_protocol.md}`, `.gitignore`, `data/real_world/raw_metadata/covid_misinfo_4557828/`. **No existing files were modified** (`ORVEX_Complete_Project_Specification.pdf`, the LOOP-MIND workbook and `ORVEX_Literature/` untouched). There is no git repository, so no `.gitignore` was created; `data/` and `tools/` must be excluded if a repository is initialised.
