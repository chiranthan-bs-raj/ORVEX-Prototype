# ORVEX - Everything About Every Dataset (complete reference)

Generated from the verified repository audit (live-checked: 2,133 files, 17,927,214,201 bytes). For each of the 40 audit IDs: what it is, where it came from, how it entered the project, where it is stored, counts and size, **every column/field**, how and where it is used in the problem statement and code, licence, limitations and necessity. `UNKNOWN SEMANTICS` = repository gives no documentation for that field.

Reading key for columns: *orig/added* = original source field vs added by ORVEX; *role* = ground truth / metadata / feature / etc.; *usage* = whether any project code reads it downstream.

---
# DS-001 - Wikimedia Commons CC/PD video originals

- **Family / component / category:** Wikimedia Commons pool (ORVEX selection) / media files / Real-world media (naturally occurring, user-uploaded)
- **Original publisher:** Wikimedia Commons contributors
- **Original source:** https://commons.wikimedia.org (file pages listed in DS-002)
- **How it entered the project:** scripts/datasets/s2_collect_media.py:commons (Commons API search, licence gate, download)
- **What was retained:** 96 original files byte-for-byte; per-file licence/author in DS-002
- **Provenance category:** 1 Verified from repository evidence (external source not re-checked online)
- **Location:** `data/real_world/media/commons` (webm/ogv/ogg/mp4); availability: Local files; state: raw
- **Files / records / size:** 96 / 96 / 1687143702 bytes (1.687 GB)
- **Usable / excluded:** 55 usable as variant sources (QC); 95 of 96 readable / 41 excluded (too long/short, duplicate, no decodable frames, non-real CGI screen, etc.)
- **Licence:** per-file CC/PD: {'CC BY-SA 4.0': 35, 'Public domain': 25, 'CC BY 4.0': 12, 'CC BY-SA 3.0': 8, 'CC BY 3.0': 7, 'CC0': 6, 'CC BY 2.0': 1, 'CC BY-SA 2.0': 1, 'CC BY-SA 3.0 nl': 1}
- **Referenced by code:** scripts/datasets/audit.py:_@63; scripts/datasets/audit.py:_@189; scripts/datasets/audit.py:_@228; scripts/datasets/common.py:<module>@8; scripts/datasets/patch_round3.py:<module>@23; scripts/datasets/patch_round3.py:<module>@56 (+13 more)
- **Actually used (verified class):** Preprocessing use verified; Evaluation use verified (features -> baseline)
- **Necessity:** Essential - only source of rights-cleared real media for controlled variants and real-media evaluation; nothing else in the repository can replace it
- **Retention:** Retain in working package
- **Limitations:** Small sample (96 files; 55 usable); themes chosen by ORVEX search queries; licence re-check needed before release; 17 originals lack audio

## How it is used in the problem statement and project
- **R-M1** (p5 Module 1 Dataset Creation): Import source videos; identify duplicates; unique IDs; generate variants; record transformation + parent; save relationships
  - evidence it provides: 96 licensed real videos; QC flags; duplicates; fields/media used: local_path, sha256, license, qc_flags, usable_for_variants
  - consuming module: dataset pipeline script (no ORVEX application module exists in the repository); stage: ingest + QC + dedupe; algorithm: ffprobe/decode check, 24-frame dHash near-duplicate screen, CGI keyword screen
  - input: `data/real_world/media/commons/*`; code: yes: scripts/datasets/s3_normalize.py:qc_commons (lines 55-114)
  - output: DS-016 rows (RW-01), DS-026; evaluation: tests K08/K19/K28
  - status: **Implemented (as data pipeline)**; evidence: Demonstrated; limits: sample of 96; 55 usable
- **R-WF1** (p7 Phase 1 workflow steps 1-8): Collect, dedupe, variants, record relationships, features, train, test, graph
  - evidence it provides: source pool for controlled variants; fields/media used: local_path, has_audio, license
  - consuming module: dataset pipeline script (no ORVEX application module exists in the repository); stage: variant generation input; algorithm: FFmpeg transformations
  - input: `data/real_world/media/commons/*`; code: yes: scripts/datasets/s4_variants.py:process (lines 68-118)
  - output: DS-013, DS-014; evaluation: tests K04/K10
  - status: **Implemented**; evidence: Demonstrated; limits: variants are controlled composites, not natural posts
- **R-M2** (p5 Module 2 Media Processing): Extract frames/audio/text; OCR; visual/audio/text representations; store fingerprints
  - evidence it provides: local media for fingerprints; fields/media used: local_path
  - consuming module: dataset pipeline script (no ORVEX application module exists in the repository); stage: feature extraction; algorithm: OpenCV dHash + FFmpeg audio fingerprint
  - input: `data/real_world/media/commons/*`; code: yes: scripts/datasets/s5_features_pairs_splits.py:feat (lines 71-82)
  - output: DS-021, DS-022; evaluation: K17
  - status: **Partially implemented (hash/fingerprint only)**; evidence: Demonstrated; limits: no embeddings/OCR/ASR

**Code touching this dataset (file : symbol : operation):** `scripts/datasets/audit.py:_` (reference, lines 63-228); `scripts/datasets/common.py:<module>` (reference, lines 8-8); `scripts/datasets/patch_round3.py:<module>` (reference, lines 23-56); `scripts/datasets/s2_collect_media.py:<module>` (reference, lines 11-11); `scripts/datasets/s2_collect_media.py:commons` (write/produce, lines 46-84); `scripts/datasets/s2_collect_media.py:dl` (reference, lines 76-76); `scripts/datasets/s3_normalize.py:<module>` (reference, lines 13-13); `scripts/datasets/s3_normalize.py:build_registry` (reference, lines 273-273); `scripts/datasets/s3_normalize.py:qc_commons` (reference, lines 103-108); `scripts/datasets/s3_normalize.py:work` (reference, lines 58-58) ... (+3 more in DATASET_TO_IMPLEMENTATION_MAP.csv)

## Columns / fields
This component has no structured columns (media files, archives or documents).

---
# DS-002 - Commons source metadata (candidate records)

- **Family / component / category:** Wikimedia Commons pool (ORVEX selection) / metadata / Source metadata (API-derived + ORVEX search fields)
- **Original publisher:** Wikimedia Commons API (assembled by ORVEX)
- **Original source:** https://commons.wikimedia.org/w/api.php
- **How it entered the project:** s2_collect_media.py:commons
- **What was retained:** API fields for 96 files (+ORVEX domain/query/media_id)
- **Provenance category:** 1 Verified from repository evidence (external source not re-checked online)
- **Location:** `data/real_world/raw_metadata/commons/commons_candidates.json` (JSON); availability: Local files; state: raw
- **Files / records / size:** 1 / 96 / 139714 bytes (0.000 GB)
- **Usable / excluded:** 96 / 0
- **Licence:** per-file (same as DS-001)
- **Referenced by code:** scripts/datasets/s2_collect_media.py:commons@47; scripts/datasets/s3_normalize.py:qc_commons@56; scripts/datasets/s4_variants.py:<module>@121; scripts/datasets/s5_features_pairs_splits.py:<module>@15; scripts/datasets/s6_docs.py:<module>@64; scripts/datasets/s7_manifests.py:<module>@16
- **Actually used (verified class):** Preprocessing use verified
- **Necessity:** Essential - licence/attribution/provenance of every original
- **Retention:** Retain
- **Limitations:** uploader names are personal data (masked in outputs); some fields (categories) not normalised into DS-016

## How it is used in the problem statement and project
- No requirement mapping (non-dataset asset or no verified role): intended module = R-M1, R-RM-10.2

**Code touching this dataset (file : symbol : operation):** `scripts/datasets/s2_collect_media.py:commons` (reference, lines 47-47); `scripts/datasets/s3_normalize.py:qc_commons` (read/consume, lines 56-56); `scripts/datasets/s4_variants.py:<module>` (read/consume, lines 121-121); `scripts/datasets/s5_features_pairs_splits.py:<module>` (read/consume, lines 15-15); `scripts/datasets/s6_docs.py:<module>` (reference, lines 64-64); `scripts/datasets/s7_manifests.py:<module>` (read/consume, lines 16-16)

## Columns / fields (25 across 1 file(s))

### `data/real_world/raw_metadata/commons/commons_candidates.json`  - 25 fields, 1 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| $ | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $[] | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $[].pageid | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 14634957 | metadata | Unreferenced in project code |
| $[].title | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | File:Ante Pavelić Speech 21051941.ogv | metadata | Unreferenced in project code |
| $[].url | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | https://upload.wikimedia.org/wikipedia/commons/9/9 | metadata | Unreferenced in project code |
| $[].page_url | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | https://commons.wikimedia.org/wiki/File:Ante_Pavel | metadata | Unreferenced in project code |
| $[].mime | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | application/ogg | metadata | Unreferenced in project code |
| $[].size | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 23898980 | metadata | Unreferenced in project code |
| $[].uploaded | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 2011-03-18T10:36:10Z | metadata | Unreferenced in project code |
| $[].uploader | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | [masked] | metadata | Unreferenced in project code |
| $[].upload_comment | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | == {{int:filedesc}} == {{Information /Descriptio | metadata | Unreferenced in project code |
| $[].commons_sha1 | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | f8e270087d31b396ac7c7eeeb2799f4f150df47e | metadata | Unreferenced in project code |
| $[].license | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | Public domain | metadata | Unreferenced in project code |
| $[].license_url | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $[].author | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | [masked] | metadata | Unreferenced in project code |
| $[].credit | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | [masked] | metadata | Unreferenced in project code |
| $[].attribution_required | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | false | metadata | Unreferenced in project code |
| $[].description | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | Ante Pavelić Speech | metadata | Unreferenced in project code |
| $[].categories | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $[].categories[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | Ante Pavelić | metadata | Unreferenced in project code |
| $[].domain | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | speech | metadata | Unreferenced in project code |
| $[].query | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | speech | metadata | Unreferenced in project code |
| $[].global_usage_count | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 2 | metadata | Unreferenced in project code |
| $[].media_id | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | RW-CMN-P14634957 | metadata | Unreferenced in project code |
| $[].local_file | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | RW-CMN-P14634957.ogv | metadata | Unreferenced in project code |

---
# DS-003 - ANAKIN subset: trimmed + edited videos

- **Family / component / category:** ANAKIN (incl. VideoSham) / media files (trimmed source clip + edited version) / Real-world human-edited media (commissioned edits of real Vimeo clips)
- **Original publisher:** Black et al. (ANAKIN/VADER), Hugging Face AlexBlck/ANAKIN
- **Original source:** https://huggingface.co/datasets/AlexBlck/ANAKIN
- **How it entered the project:** s2_collect_media.py:anakin (HF resolve URLs, deterministic subset)
- **What was retained:** 250 trimmed + 250 edited clips, unmodified
- **Provenance category:** 1 Verified from repository evidence (external source not re-checked online)
- **Location:** `data/real_world/media/anakin` (mp4); availability: Local files; state: derived/processed
- **Files / records / size:** 500 / 250 / 2392113142 bytes (2.392 GB)
- **Usable / excluded:** 250 pairs with both files readable / 0
- **Licence:** cc-by-4.0 (HF dataset card snapshot); underlying Vimeo rights not verified
- **Referenced by code:** scripts/datasets/common.py:<module>@21; scripts/datasets/patch_round2.py:<module>@55; scripts/datasets/patch_round2.py:<module>@57; scripts/datasets/patch_round3.py:<module>@80; scripts/datasets/s1_fetch_metadata.py:<module>@22; scripts/datasets/s2_collect_media.py:<module>@11 (+28 more)
- **Actually used (verified class):** Preprocessing use verified; Evaluation use verified (baseline pairs)
- **Necessity:** Useful and justified - only real human-edit pairs; consumed by the baseline; not a variant source
- **Retention:** Retain
- **Limitations:** Commissioned edits, Vimeo source rights unverified; evaluation-only; not used to create variants

## How it is used in the problem statement and project
- **R-M4** (p6 Module 4 Manipulation Analysis): Trimming/cropping, captions, audio replacement, inconsistencies
  - evidence it provides: 250 real human-edited pairs with manipulation type; fields/media used: native_manipulation_type, parent/child edge
  - consuming module: dataset pipeline script (no ORVEX application module exists in the repository); stage: baseline evaluation; algorithm: non-learned dHash frame matching
  - input: `data/real_world/media/anakin/{trimmed,edited}`; code: yes: scripts/datasets/s9_feature_baseline.py (module level)
  - output: DS-030 metrics; necessity_audit/dhash_baseline_results.json; evaluation: baseline detection rate on edited_version pairs
  - status: **Partially implemented (baseline only)**; evidence: Demonstrated: detection 0.92 at fixed threshold; limits: commissioned edits; no learned model
- **R-M9b** (p8 Phase 1 step 7; p11 §9.6): Unseen sources and transformations
  - evidence it provides: real edits as unseen-manipulation proxy; fields/media used: edited_version pairs, split
  - consuming module: dataset pipeline script (no ORVEX application module exists in the repository); stage: evaluation protocol; algorithm: split-by-family
  - input: `DS-025 + DS-023`; code: yes: scripts/datasets/s5_features_pairs_splits.py:assign (lines 25-28)
  - output: DS-025; evaluation: K13
  - status: **Implemented (split only)**; evidence: Demonstrated; limits: no model evaluated on them

**Code touching this dataset (file : symbol : operation):** `scripts/datasets/common.py:<module>` (reference, lines 21-21); `scripts/datasets/patch_round2.py:<module>` (reference, lines 55-57); `scripts/datasets/patch_round3.py:<module>` (reference, lines 80-80); `scripts/datasets/s1_fetch_metadata.py:<module>` (reference, lines 22-22); `scripts/datasets/s2_collect_media.py:<module>` (reference, lines 11-115); `scripts/datasets/s2_collect_media.py:anakin` (read+write, lines 86-111); `scripts/datasets/s3_normalize.py:<module>` (reference, lines 13-283); `scripts/datasets/s3_normalize.py:anakin_rows` (read/consume, lines 117-141); `scripts/datasets/s3_normalize.py:build_registry` (reference, lines 273-278); `scripts/datasets/s5_features_pairs_splits.py:<module>` (read/consume, lines 30-209) ... (+2 more in DATASET_TO_IMPLEMENTATION_MAP.csv)

## Columns / fields
This component has no structured columns (media files, archives or documents).

---
# DS-004 - ANAKIN subset: edit masks

- **Family / component / category:** ANAKIN (incl. VideoSham) / annotations (per-frame binary masks, zip) / Real-world annotations
- **Original publisher:** ANAKIN authors
- **Original source:** https://huggingface.co/datasets/AlexBlck/ANAKIN
- **How it entered the project:** s2_collect_media.py:anakin (same loop)
- **What was retained:** 89 mask zips for has-masks pairs, unmodified, never opened
- **Provenance category:** 2 Documented, not independently verified
- **Location:** `data/real_world/media/anakin/masks` (zip); availability: Local files; state: derived/processed
- **Files / records / size:** 89 / 89 / 128979239 bytes (0.129 GB)
- **Usable / excluded:** Unknown (not opened) / Unknown
- **Licence:** cc-by-4.0 (card)
- **Referenced by code:** scripts/datasets/candidates.py:<module>@19; scripts/datasets/candidates.py:<module>@22; scripts/datasets/candidates.py:<module>@24; scripts/datasets/s2_collect_media.py:<module>@4; scripts/datasets/s2_collect_media.py:anakin@87; scripts/datasets/s2_collect_media.py:anakin@95 (+3 more)
- **Actually used (verified class):** Reference only (downloaded by s2, never read)
- **Necessity:** Underutilized - masks could support manipulation localisation but no code reads them and they are untracked
- **Retention:** Retain (archival/future); register in the master first
- **Limitations:** Present on disk but untracked by the registry; no code reads them

## How it is used in the problem statement and project
- **R-M4** (p6 Module 4 Manipulation Analysis): Trimming/cropping, captions, audio replacement, inconsistencies
  - evidence it provides: per-frame edit masks (89 zips); fields/media used: mask zip
  - consuming module: none; stage: none; algorithm: none
  - input: `data/real_world/media/anakin/masks/*.zip`; code: NO: no reference
  - output: none; evaluation: none
  - status: **Not implemented**; evidence: Absent (never read); limits: untracked in registry; integrity not checked

**Code touching this dataset (file : symbol : operation):** `scripts/datasets/candidates.py:<module>` (reference, lines 19-24); `scripts/datasets/s2_collect_media.py:<module>` (reference, lines 4-4); `scripts/datasets/s2_collect_media.py:anakin` (write/produce, lines 87-104); `scripts/datasets/s6_docs.py:<module>` (reference, lines 63-100)

## Columns / fields
This component has no structured columns (media files, archives or documents).

---
# DS-005 - ANAKIN metadata and official listing

- **Family / component / category:** ANAKIN (incl. VideoSham) / metadata/annotations / Source metadata and annotations
- **Original publisher:** ANAKIN authors / Hugging Face API
- **Original source:** https://huggingface.co/datasets/AlexBlck/ANAKIN
- **How it entered the project:** interactive Gate-1 download; s1_fetch_metadata.py re-fetches metadata.csv/blobs/card
- **What was retained:** metadata.csv (1,023 rows), HF file listing, card, loader script, selected-subset list (ORVEX-derived)
- **Provenance category:** 1 Verified from repository evidence (external source not re-checked online)
- **Location:** `data/real_world/raw_metadata/hf_api` (CSV/JSON); availability: Local files; state: raw
- **Files / records / size:** 5 / 1023 / 1033853 bytes (0.001 GB)
- **Usable / excluded:** 250 selected rows / 0
- **Licence:** cc-by-4.0 (card)
- **Referenced by code:** scripts/datasets/s1_fetch_metadata.py:<module>@22; scripts/datasets/s2_collect_media.py:anakin@88; scripts/datasets/s2_collect_media.py:anakin@98; scripts/datasets/s3_normalize.py:anakin_rows@118; scripts/datasets/s3_normalize.py:anakin_rows@121; scripts/datasets/s5_features_pairs_splits.py:<module>
- **Actually used (verified class):** Preprocessing use verified
- **Necessity:** Essential - labels for the ANAKIN pairs
- **Retention:** Retain
- **Limitations:** 1,042 files in the official listing vs 1,023 metadata rows (see findings)

## How it is used in the problem statement and project
- **R-M4** (p6 Module 4 Manipulation Analysis): Trimming/cropping, captions, audio replacement, inconsistencies
  - evidence it provides: manipulation-type labels for 1,023 pairs; fields/media used: manipulation-type, task, start-time, end-time
  - consuming module: dataset pipeline script (no ORVEX application module exists in the repository); stage: normalise native edit edges; algorithm: none (label copy/normalise)
  - input: `data/real_world/raw_metadata/hf_api/anakin_metadata.csv`; code: yes: scripts/datasets/s3_normalize.py:anakin_rows (lines 117-147)
  - output: DS-017 (RW-02 edges), DS-016; evaluation: K12
  - status: **Implemented**; evidence: Demonstrated; limits: only 250 pairs have media

**Code touching this dataset (file : symbol : operation):** `scripts/datasets/s1_fetch_metadata.py:<module>` (reference, lines 22-22); `scripts/datasets/s2_collect_media.py:anakin` (read+write, lines 88-98); `scripts/datasets/s3_normalize.py:anakin_rows` (read/consume, lines 118-121); `scripts/datasets/s5_features_pairs_splits.py:<module>` (read/consume, lines 30-209)

## Columns / fields (82 across 4 file(s))

### `data/real_world/raw_metadata/hf_api/anakin.json`  - 29 fields, 1 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| $ | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $._id | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 64de138cd1885643ca1ad3ac | metadata | Unreferenced in project code |
| $.id | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | AlexBlck/ANAKIN | metadata | Unreferenced in project code |
| $.author | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | [masked] | metadata | Unreferenced in project code |
| $.sha | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 978fe26e78ecaaf6562aa249be43c2c690484d0a | metadata | Unreferenced in project code |
| $.lastModified | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 2023-09-21T10:37:04.000Z | metadata | Unreferenced in project code |
| $.private | bool | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | False | metadata | Unreferenced in project code |
| $.gated | bool | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | False | metadata | Unreferenced in project code |
| $.disabled | bool | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | False | metadata | Unreferenced in project code |
| $.tags | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.tags[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | task_categories:video-classification | metadata | Unreferenced in project code |
| $.citation | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | @misc{black2023vader,       title={VADER: Video Al | metadata | Unreferenced in project code |
| $.description | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | ANAKIN is a dataset of mANipulated videos and mAsK | metadata | Unreferenced in project code |
| $.downloads | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 1445 | metadata | Unreferenced in project code |
| $.likes | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 2 | metadata | Unreferenced in project code |
| $.cardData | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.cardData.license | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | cc-by-4.0 | metadata | Unreferenced in project code |
| $.cardData.task_categories | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.cardData.task_categories[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | video-classification | metadata | Unreferenced in project code |
| $.cardData.language | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.cardData.language[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | en | metadata | Unreferenced in project code |
| $.cardData.pretty_name | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | ANAKIN: manipulated videos and mask annotations | metadata | Unreferenced in project code |
| $.cardData.size_categories | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.cardData.size_categories[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 1K<n<10K | metadata | Unreferenced in project code |
| $.siblings | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.siblings[] | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.siblings[].rfilename | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | .gitattributes | metadata | Unreferenced in project code |
| $.createdAt | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 2023-08-17T12:33:16.000Z | metadata | Unreferenced in project code |
| $.usedStorage | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 81378675780 | metadata | Unreferenced in project code |

### `data/real_world/raw_metadata/hf_api/anakin_blobs.json`  - 35 fields, 1 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| $ | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $._id | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 64de138cd1885643ca1ad3ac | metadata | Unreferenced in project code |
| $.id | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | AlexBlck/ANAKIN | metadata | Unreferenced in project code |
| $.author | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | [masked] | metadata | Unreferenced in project code |
| $.sha | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 978fe26e78ecaaf6562aa249be43c2c690484d0a | metadata | Unreferenced in project code |
| $.lastModified | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 2023-09-21T10:37:04.000Z | metadata | Unreferenced in project code |
| $.private | bool | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | False | metadata | Unreferenced in project code |
| $.gated | bool | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | False | metadata | Unreferenced in project code |
| $.disabled | bool | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | False | metadata | Unreferenced in project code |
| $.tags | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.tags[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | task_categories:video-classification | metadata | Unreferenced in project code |
| $.citation | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | @misc{black2023vader,       title={VADER: Video Al | metadata | Unreferenced in project code |
| $.description | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | ANAKIN is a dataset of mANipulated videos and mAsK | metadata | Unreferenced in project code |
| $.downloads | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 1445 | metadata | Unreferenced in project code |
| $.likes | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 2 | metadata | Unreferenced in project code |
| $.cardData | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.cardData.license | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | cc-by-4.0 | metadata | Unreferenced in project code |
| $.cardData.task_categories | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.cardData.task_categories[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | video-classification | metadata | Unreferenced in project code |
| $.cardData.language | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.cardData.language[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | en | metadata | Unreferenced in project code |
| $.cardData.pretty_name | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | ANAKIN: manipulated videos and mask annotations | metadata | Unreferenced in project code |
| $.cardData.size_categories | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.cardData.size_categories[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 1K<n<10K | metadata | Unreferenced in project code |
| $.siblings | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.siblings[] | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.siblings[].rfilename | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | .gitattributes | metadata | Unreferenced in project code |
| $.siblings[].blobId | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | edfa28d379efaa9a036be7c8e70d7d2fe1b6bd8a | metadata | Unreferenced in project code |
| $.siblings[].size | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 7479 | metadata | Unreferenced in project code |
| $.siblings[].lfs | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.siblings[].lfs.sha256 | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 10d1181299ff5dc43a46325ec02332047278df08c4fa1fa342 | metadata | Unreferenced in project code |
| $.siblings[].lfs.size | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 21602416 | metadata | Unreferenced in project code |
| $.siblings[].lfs.pointerSize | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 133 | metadata | Unreferenced in project code |
| $.createdAt | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 2023-08-17T12:33:16.000Z | metadata | Unreferenced in project code |
| $.usedStorage | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 81378675780 | metadata | Unreferenced in project code |

### `data/real_world/raw_metadata/hf_api/anakin_metadata.csv`  - 9 fields, 1023 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| video-id | str | ANAKIN video id | original source field | copied (native) | 0.0 | 1023 | 4zyvv7 | metadata | Used by downstream code |
| start-time | int | trim start inside the full video (s) | original source field | copied (native) | 0.0 | 104 | 0 | source annotation | Used by downstream code |
| end-time | int | trim end inside the full video (s) | original source field | copied (native) | 0.0 | 109 | 8 | source annotation | Used by downstream code |
| url | str | Vimeo URL of the full source video | original source field | copied (native) | 0.0 | 1013 | https://vimeo.com/640582697 | metadata | Used by downstream code |
| has-masks | bool | whether per-frame edit masks exist | original source field | copied (native) | 0.0 | 2 | FALSE | metadata | Used by downstream code |
| task | str | editing task given to the editor | original source field | copied (native) | 0.0 | 911 | Speeding up/Slowing down : 33% | source annotation | Used by downstream code |
| manipulation-type | str | splicing / inpainting / swap / audio / frame-level | original source field | copied (native) | 0.0 | 5 | frame-level | source annotation (ground truth) | Used by downstream code |
| editor-id | str | anonymous editor id | original source field | copied (native) | 0.0 | 10 | [masked] | metadata | Used by downstream code |
| full-available | bool | whether the full video is hosted | original source field | copied (native) | 0.0 | 2 | TRUE | metadata | Used by downstream code |

### `data/real_world/raw_metadata/hf_api/anakin_selected_subset.csv`  - 9 fields, 250 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| video-id | str | ANAKIN video id (subset row copied by ORVEX) | original source field | copied (native) | 0.0 | 250 | 7e2p57 | metadata | Used by downstream code |
| start-time | int | trim start inside the full video (s) (subset row copied by ORVEX) | original source field | copied (native) | 0.0 | 60 | 10 | source annotation | Used by downstream code |
| end-time | int | trim end inside the full video (s) (subset row copied by ORVEX) | original source field | copied (native) | 0.0 | 64 | 15 | source annotation | Used by downstream code |
| url | str | Vimeo URL of the full source video (subset row copied by ORVEX) | original source field | copied (native) | 0.0 | 250 | https://vimeo.com/532330511 | metadata | Used by downstream code |
| has-masks | bool | whether per-frame edit masks exist (subset row copied by ORVEX) | original source field | copied (native) | 0.0 | 2 | True | metadata | Used by downstream code |
| task | str | editing task given to the editor (subset row copied by ORVEX) | original source field | copied (native) | 0.0 | 230 | Add dollar sign to t-shirt | source annotation | Used by downstream code |
| manipulation-type | str | splicing / inpainting / swap / audio / frame-level (subset row copied by ORVEX) | original source field | copied (native) | 0.0 | 5 | splicing | source annotation (ground truth) | Used by downstream code |
| editor-id | str | anonymous editor id (subset row copied by ORVEX) | original source field | copied (native) | 0.0 | 10 | [masked] | metadata | Used by downstream code |
| full-available | bool | whether the full video is hosted (subset row copied by ORVEX) | original source field | copied (native) | 0.0 | 2 | True | metadata | Used by downstream code |

---
# DS-006 - InVID Fake Video Corpus 2018 (v3): URLs and labels

- **Family / component / category:** InVID FVC / metadata/annotations (URL-only) / Real-world source metadata (naturally circulating videos; media NOT local)
- **Original publisher:** Papadopoulou, Zampoglou, Papadopoulos, Kompatsiaris (CERTH-ITI/AFP)
- **Original source:** https://zenodo.org/records/2535479
- **How it entered the project:** interactive Gate-1 download from Zenodo (md5 verified); s1_fetch_metadata.py re-fetches
- **What was retained:** official zip + extracted copy (FVC.csv, FVC_dup.csv, FVC_text_queries.csv, README)
- **Provenance category:** 1 Verified from repository evidence (external source not re-checked online)
- **Location:** `data/real_world/raw_metadata/invid_fvc_2018` (CSV (+zip)); availability: Metadata only (no media); state: metadata-only
- **Files / records / size:** 5 / 5579 / 650024 bytes (0.001 GB)
- **Usable / excluded:** 5579 URL records (metadata-only) / 0 (liveness not tested)
- **Licence:** cc-by-4.0 (Zenodo snapshot; annotations)
- **Referenced by code:** scripts/datasets/audit.py:_@142; scripts/datasets/patch_round2.py:<module>@55; scripts/datasets/patch_round2.py:<module>@57; scripts/datasets/s1_fetch_metadata.py:<module>@6; scripts/datasets/s3_normalize.py:fvc_rows@150; scripts/datasets/s3_normalize.py:fvc_rows@151 (+4 more)
- **Actually used (verified class):** Preprocessing use verified
- **Necessity:** Conditionally useful - repost cascades with labels; media inaccessible; native text queries unused
- **Retention:** Retain
- **Limitations:** No media bytes; no timestamps; labels mean debunked/verified, not AI-generated; URLs not checked for liveness

## How it is used in the problem statement and project
- **R-M3** (p5-6 Module 3 Relationship Detection): Compare two videos; share a source; direct/indirect derivation; likely vs uncertain; confidence + evidence
  - evidence it provides: 5,579 URL records in cascades with labels; fields/media used: cascade_id, video_url, label
  - consuming module: dataset pipeline script (no ORVEX application module exists in the repository); stage: normalise cascade edges; algorithm: none
  - input: `data/real_world/raw_metadata/invid_fvc_2018/extracted/FVC*.csv`; code: yes: scripts/datasets/s3_normalize.py:fvc_rows (lines 150-192)
  - output: DS-016, DS-017, DS-018; evaluation: K12
  - status: **Partially implemented (metadata only)**; evidence: Indirect (no media); limits: no media; labels include uncertain/debunked/parody (495 rows not normalised)
- **R-M6** (p6 Module 6 Platform Integration): Permitted APIs; post IDs/URLs/timestamps/metadata; normalise; handle limits
  - evidence it provides: cascade order of reposts; fields/media used: cascade_id, order
  - consuming module: dataset pipeline script (no ORVEX application module exists in the repository); stage: observation table; algorithm: none
  - input: `FVC_dup.csv`; code: yes: scripts/datasets/s3_normalize.py:fvc_rows (lines 150-192)
  - output: DS-018 (cascade_member); evaluation: K22
  - status: **Partially implemented**; evidence: Demonstrated (order only); limits: no timestamps or accounts

**Code touching this dataset (file : symbol : operation):** `scripts/datasets/audit.py:_` (reference, lines 142-142); `scripts/datasets/patch_round2.py:<module>` (reference, lines 55-57); `scripts/datasets/s1_fetch_metadata.py:<module>` (reference, lines 6-6); `scripts/datasets/s3_normalize.py:<module>` (reference, lines 283-283); `scripts/datasets/s3_normalize.py:build_registry` (reference, lines 273-273); `scripts/datasets/s3_normalize.py:fvc_rows` (reference, lines 150-153); `scripts/datasets/s5_features_pairs_splits.py:<module>` (reference, lines 201-201)

## Columns / fields (27 across 3 file(s))

### `data/real_world/raw_metadata/invid_fvc_2018/extracted/FVC.csv`  - 3 fields, 380 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| cascade_id | str | Verification cascade id ('f'+n debunked / 'r'+n verified) of the head video | added by ORVEX | derived | 0.0 | 380 | f0 | FVC (Zenodo) | Used by downstream code |
| video_url | str | URL of the video on YouTube/Facebook/Twitter | original source field | copied (native) | 0.0 | 380 | https://www.youtube.com/watch?v=Y7MJlmbnLQA | metadata | Used by downstream code |
| label | str | fake (debunked) or real (verified) as published; NOT a deepfake/AI label | added by ORVEX | derived | 0.0 | 2 | fake | FVC (Zenodo) | Used by downstream code |

### `data/real_world/raw_metadata/invid_fvc_2018/extracted/FVC_dup.csv`  - 3 fields, 5199 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| cascade_id | str | Cascade id the near-duplicate repost belongs to | added by ORVEX | derived | 0.0 | 322 | f0 | FVC (Zenodo) | Used by downstream code |
| video_url | str | URL of a near-duplicate/repost found by the authors | original source field | copied (native) | 0.0 | 5192 | https://www.facebook.com/palasqueseaoficial/videos | metadata | Used by downstream code |
| label | str | label of the cascade (fake/real) as published | added by ORVEX | derived | 0.0 | 5 | fake | FVC (Zenodo) | Used by downstream code |

### `data/real_world/raw_metadata/invid_fvc_2018/extracted/FVC_text_queries.csv`  - 21 fields, 380 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| cascade_id | str | Cascade id (same as FVC.csv) | added by ORVEX | derived | 0.0 | 380 | f0 | FVC (Zenodo) | Used by downstream code |
| video_url | str | URL of the head video | original source field | copied (native) | 0.0 | 380 | https://www.youtube.com/watch?v=Y7MJlmbnLQA | metadata | Used by downstream code |
| label | str | fake/real label as published | added by ORVEX | derived | 0.0 | 2 | fake | FVC (Zenodo) | Used by downstream code |
| event_title | str | English text query/title describing the event, used by the authors to search for related videos | original source field | copied (native) | 0.0 | 371 | Woman falls in volcano lava | source annotation (text query) | Unreferenced in project code |
| french | str | French rendering of event_title (translation method not documented) | original source field | copied (native) | 0.0 | 372 | femme tombe dans la lave du volcan | source annotation (translation) | Unreferenced in project code |
| spanish | str | Spanish rendering of event_title (method not documented) | original source field | copied (native) | 0.0 | 372 | Mujer cae en la lava del volcán | source annotation (translation) | Unreferenced in project code |
| russian | str | Russian rendering of event_title (method not documented) | original source field | copied (native) | 0.0 | 372 | женщина падает в вулкан лавы | source annotation (translation) | Unreferenced in project code |
| arabic | str | Arabic rendering of event_title (method not documented) | original source field | copied (native) | 0.26 | 370 | امرأة تقع في الحمم بركان | source annotation (translation) | Unreferenced in project code |
| (unnamed trailing field 9) | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 83.68 | 60 | طفل مع البطاطس والقلب يحصل بالشاحنات | metadata (unverified meaning) | Unreferenced in project code |
| (unnamed trailing field 10) | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 92.63 | 28 | кот 5 ураган Ирма разрушает ул. Тёркс | metadata (unverified meaning) | Unreferenced in project code |
| (unnamed trailing field 11) | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 92.89 | 27 | القط 5 إعصار إيرما يدمر الحادي والعشرين. جونز، أنت | metadata (unverified meaning) | Unreferenced in project code |
| (unnamed trailing field 12) | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 93.95 | 23 | اعصار في كيب تاون، جنوب أفريقيا | metadata (unverified meaning) | Unreferenced in project code |
| (unnamed trailing field 13) | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 98.42 | 6 | точно удар умной бомбы КАБ-500 против одного здани | metadata (unverified meaning) | Unreferenced in project code |
| (unnamed trailing field 14) | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 98.42 | 6 | подземный этаж которого прошла встреча командовани | metadata (unverified meaning) | Unreferenced in project code |
| (unnamed trailing field 15) | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 98.42 | 6 | работающий в Идлиб провинции | metadata (unverified meaning) | Unreferenced in project code |
| (unnamed trailing field 16) | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 98.68 | 5 | استضافت تحديد إضراب مع القنبلة الذكية KAB-500 ضد م | metadata (unverified meaning) | Unreferenced in project code |
| (unnamed trailing field 17) | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 99.47 | 2 | расположенных вблизи dokmak. Прямое попадание возд | metadata (unverified meaning) | Unreferenced in project code |
| (unnamed trailing field 18) | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 99.74 | 1 | оборудования и материальных средств боевиков | metadata (unverified meaning) | Unreferenced in project code |
| (unnamed trailing field 19) | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 99.74 | 1 | которые были на позициях | metadata (unverified meaning) | Unreferenced in project code |
| (unnamed trailing field 20) | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 99.74 | 1 | были уничтожены. | metadata (unverified meaning) | Unreferenced in project code |
| (unnamed trailing field 21) | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 99.74 | 1 | قضت قوات الفضاء الروسية نقطة قوية للإرهابيين "الدو | metadata (unverified meaning) | Unreferenced in project code |

---
# DS-007 - InVID Fake Video Corpus v2.0: URLs, labels, manipulation types

- **Family / component / category:** InVID FVC / metadata/annotations (URL-only) / Real-world source metadata (media NOT local)
- **Original publisher:** Papadopoulou et al. (CERTH-ITI/AFP)
- **Original source:** https://zenodo.org/records/1147958
- **How it entered the project:** same (Zenodo 1147958)
- **What was retained:** zip + extracted TSVs
- **Provenance category:** 1 Verified from repository evidence (external source not re-checked online)
- **Location:** `data/real_world/raw_metadata/invid_fvc_v2` (TSV (+zip)); availability: Metadata only (no media); state: metadata-only
- **Files / records / size:** 4 / 227 / 74758 bytes (0.000 GB)
- **Usable / excluded:** see inventory notes / 0
- **Licence:** cc-by-4.0 (Zenodo snapshot)
- **Referenced by code:** scripts/datasets/audit.py:_@142; scripts/datasets/s1_fetch_metadata.py:<module>@6; scripts/datasets/s3_normalize.py:fvc_rows@178; scripts/datasets/s3_normalize.py:fvc_rows@181; scripts/datasets/s3_normalize.py:build_registry@274; scripts/datasets/s5_features_pairs_splits.py:<module>@201
- **Actually used (verified class):** Preprocessing use verified
- **Necessity:** Conditionally useful - adds manipulation type/debunk URLs; 188 of 227 YouTube ids overlap DS-006
- **Retention:** Retain (extra native fields)
- **Limitations:** overlaps DS-006 by URL (see overlap matrix); extra native fields (Discussed, Appeared, Timestamp, Channel...) kept only in raw files

## How it is used in the problem statement and project
- **R-M4** (p6 Module 4 Manipulation Analysis): Trimming/cropping, captions, audio replacement, inconsistencies
  - evidence it provides: manipulation types for 117 fake videos; fields/media used: Type of Manipulation, Timestamp
  - consuming module: dataset pipeline script (no ORVEX application module exists in the repository); stage: normalise; algorithm: none
  - input: `invid_fvc_v2 TSVs`; code: yes: scripts/datasets/s3_normalize.py:fvc_rows (lines 150-192)
  - output: DS-016.native_manipulation_type; evaluation: none
  - status: **Partially implemented**; evidence: Indirect; limits: Timestamp/Discussed/Appeared only in raw files

**Code touching this dataset (file : symbol : operation):** `scripts/datasets/audit.py:_` (reference, lines 142-142); `scripts/datasets/s1_fetch_metadata.py:<module>` (reference, lines 6-6); `scripts/datasets/s3_normalize.py:build_registry` (reference, lines 274-274); `scripts/datasets/s3_normalize.py:fvc_rows` (reference, lines 178-181); `scripts/datasets/s5_features_pairs_splits.py:<module>` (reference, lines 201-201)

## Columns / fields (16 across 2 file(s))

### `data/real_world/raw_metadata/invid_fvc_v2/extracted/Fake Video Corpus v2.0/fake-video-corpus - fake-videos.tsv`  - 8 fields, 117 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| InVID_id | str | Row id in the corpus (fvc-n / fvc_r-n) | original source field | copied (native) | 0.0 | 117 | fvc-1 | metadata | Used by downstream code |
| Link | str | Video URL | original source field | copied (native) | 0.0 | 117 | https://www.youtube.com/watch?v=65vcSu93MUE | metadata | Used by downstream code |
| Title | str | Title given by the authors | original source field | copied (native) | 0.0 | 117 | Syrian boy rescues girl after being shot | metadata | Used by downstream code |
| Type of Manipulation | str | Type of tampering for fake videos | original source field | copied (native) | 70.09 | 3 | Tampering | source annotation | Used by downstream code |
| Comments | str | Authors' comments | original source field | copied (native) | 0.85 | 88 | The video was staged: it was filmed in Malta by No | metadata | Used by downstream code |
| Discussed | str | URL where the video is debunked | original source field | copied (native) | 11.97 | 86 | http://www.independent.co.uk/news/world/middle-eas | source annotation | Unreferenced in project code |
| Appeared | str | URL of the first news article where the video appeared (if known) | original source field | copied (native) | 87.18 | 14 | http://www.telegraph.co.uk/news/worldnews/middleea | source annotation | Unreferenced in project code |
| Timestamp | str | Time inside the video where tampering appears | original source field | copied (native) | 73.5 | 25 | 18-22; 37-39; 48-1:04 | source annotation | Unreferenced in project code |

### `data/real_world/raw_metadata/invid_fvc_v2/extracted/Fake Video Corpus v2.0/fake-video-corpus - real-videos.tsv`  - 8 fields, 110 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| InVID_id | str | Row id in the corpus (fvc-n / fvc_r-n) | original source field | copied (native) | 0.0 | 110 | fvc_r-1 | metadata | Used by downstream code |
| Link | str | Video URL | original source field | copied (native) | 0.0 | 110 | https://www.youtube.com/watch?v=0pFWyDn0o1o | metadata | Used by downstream code |
| Title | str | Title given by the authors | original source field | copied (native) | 0.0 | 109 | young girl bombed while singing - Syria | metadata | Used by downstream code |
| Comments | str | Authors' comments | original source field | copied (native) | 95.45 | 5 | http://www.scmp.com/news/china/society/article/202 | metadata | Used by downstream code |
| Channel | str | YouTube channel of a real video | original source field | copied (native) | 0.0 | 87 | [masked] | metadata | Used by downstream code |
| Official channel | str | whether the channel is official | original source field | copied (native) | 57.27 | 1 | yes | metadata | Unreferenced in project code |
| Subscriptions | str | channel subscriber count | original source field | copied (native) | 0.0 | 87 | 104 | metadata | Unreferenced in project code |
| Description | str | video description | original source field | copied (native) | 44.55 | 32 | no | metadata | Used by downstream code |

---
# DS-008 - InVID Fake Video Corpus v1.0: URLs and annotations

- **Family / component / category:** InVID FVC / metadata/annotations (URL-only) / Real-world source metadata (media NOT local)
- **Original publisher:** Papadopoulos, Zampoglou, Kompatsiaris, Teyssou
- **Original source:** https://zenodo.org/records/242481
- **How it entered the project:** same (Zenodo 242481)
- **What was retained:** zip + extracted TSV
- **Provenance category:** 1 Verified from repository evidence (external source not re-checked online)
- **Location:** `data/real_world/raw_metadata/invid_fvc_v1` (TSV (+zip)); availability: Metadata only (no media); state: metadata-only
- **Files / records / size:** 3 / 59 / 27904 bytes (0.000 GB)
- **Usable / excluded:** records mapped to later versions / 0
- **Licence:** cc-by-4.0 (Zenodo snapshot)
- **Referenced by code:** scripts/datasets/audit.py:_@142; scripts/datasets/s1_fetch_metadata.py:<module>@6; scripts/datasets/s3_normalize.py:fvc_rows@179; scripts/datasets/s3_normalize.py:fvc_rows@181; scripts/datasets/s3_normalize.py:build_registry@274; scripts/datasets/s5_features_pairs_splits.py:<module>@202
- **Actually used (verified class):** Preprocessing use verified
- **Necessity:** Redundant - superseded by later versions; 49 of 59 ids overlap DS-006
- **Retention:** Retain only for provenance/duplicate mapping
- **Limitations:** Superseded by DS-006/DS-007; authors state it is not meant for quantitative evaluation

## How it is used in the problem statement and project
- No requirement mapping (non-dataset asset or no verified role): intended module = none (superseded)

**Code touching this dataset (file : symbol : operation):** `scripts/datasets/audit.py:_` (reference, lines 142-142); `scripts/datasets/s1_fetch_metadata.py:<module>` (reference, lines 6-6); `scripts/datasets/s3_normalize.py:build_registry` (reference, lines 274-274); `scripts/datasets/s3_normalize.py:fvc_rows` (reference, lines 179-181); `scripts/datasets/s5_features_pairs_splits.py:<module>` (reference, lines 202-202)

## Columns / fields (6 across 1 file(s))

### `data/real_world/raw_metadata/invid_fvc_v1/extracted/Fake Video Corpus/fake_video_corpus.tsv`  - 6 fields, 59 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| InVID_id | str | Row id in the corpus (fvc-n / fvc_r-n) | original source field | copied (native) | 0.0 | 59 | fvc-1 | metadata | Used by downstream code |
| Link | str | Video URL | original source field | copied (native) | 0.0 | 59 | https://www.youtube.com/watch?v=65vcSu93MUE | metadata | Used by downstream code |
| Title | str | Title given by the authors | original source field | copied (native) | 0.0 | 59 | Syrian boy rescues girl after being shot | metadata | Used by downstream code |
| Comments | str | Authors' comments | original source field | copied (native) | 0.0 | 47 | The video was staged: it was filmed in Malta by No | metadata | Used by downstream code |
| Discussed | str | URL where the video is debunked | original source field | copied (native) | 0.0 | 55 | http://www.independent.co.uk/news/world/middle-eas | source annotation | Unreferenced in project code |
| Appeared | str | URL of the first news article where the video appeared (if known) | original source field | copied (native) | 71.19 | 14 | http://www.telegraph.co.uk/news/worldnews/middleea | source annotation | Unreferenced in project code |

---
# DS-009 - FIVR-200K: YouTube ids, events, relation annotations

- **Family / component / category:** InVID FIVR-200K / metadata/annotations (id-only) / Real-world source metadata (media NOT local)
- **Original publisher:** Kordopatis-Zilos et al. (CERTH-ITI)
- **Original source:** https://zenodo.org/records/2564864
- **How it entered the project:** same (Zenodo 2564864)
- **What was retained:** zip + extracted annotation.json, events.json, youtube_ids.txt
- **Provenance category:** 1 Verified from repository evidence (external source not re-checked online)
- **Location:** `data/real_world/raw_metadata/invid_fivr200k` (TXT/JSON (+zip)); availability: Metadata only (no media); state: metadata-only
- **Files / records / size:** 5 / 225960 / 17873355 bytes (0.018 GB)
- **Usable / excluded:** 225,960 ids; 12,564 labelled relations / 0
- **Licence:** cc-by-4.0 (Zenodo snapshot)
- **Referenced by code:** scripts/datasets/audit.py:_@142; scripts/datasets/patch_round2.py:<module>@55; scripts/datasets/patch_round2.py:<module>@57; scripts/datasets/s1_fetch_metadata.py:<module>@6; scripts/datasets/s3_normalize.py:fivr_rows@195; scripts/datasets/s3_normalize.py:fivr_rows@196 (+4 more)
- **Actually used (verified class):** Preprocessing use verified
- **Necessity:** Conditionally useful - same-incident vs copy labels (hard negatives) once media accessible; IS labels unnormalised
- **Retention:** Retain
- **Limitations:** IDs only: no media, titles or timestamps; DS/CS/IS are scene/incident relations, not derivation proof

## How it is used in the problem statement and project
- **R-GAP** (p3-4 §4.3-4.7): Variants look different; relationship labels missing; platform limits; coordination separate; new manipulation methods
  - evidence it provides: ND/DS/CS/IS relation labels for 100 queries (12,564+3,543 relations incl. IS); fields/media used: annotation.json
  - consuming module: dataset pipeline script (no ORVEX application module exists in the repository); stage: normalise native edges; algorithm: none
  - input: `invid_fivr200k/extracted/annotation.json`; code: yes: scripts/datasets/s3_normalize.py:fivr_rows (lines 195-210)
  - output: DS-017 (RW-06 edges); evaluation: K12
  - status: **Partially implemented**; evidence: Demonstrated for ND/DS/CS; IS edges stored UNNORMALISED; limits: no media; 59 candidate ids absent from id list -> 61 dangling edges

**Code touching this dataset (file : symbol : operation):** `scripts/datasets/audit.py:_` (reference, lines 142-142); `scripts/datasets/patch_round2.py:<module>` (reference, lines 55-57); `scripts/datasets/s1_fetch_metadata.py:<module>` (reference, lines 6-6); `scripts/datasets/s3_normalize.py:<module>` (reference, lines 283-283); `scripts/datasets/s3_normalize.py:build_registry` (reference, lines 274-274); `scripts/datasets/s3_normalize.py:fivr_rows` (read/consume, lines 195-201); `scripts/datasets/s5_features_pairs_splits.py:<module>` (reference, lines 202-202)

## Columns / fields (22 across 3 file(s))

### `data/real_world/raw_metadata/invid_fivr200k/extracted/annotation.json`  - 10 fields, 1 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| $ | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.<key> | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.<key>.CS | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.<key>.CS[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | j1EzVHDnzrw | metadata | Unreferenced in project code |
| $.<key>.ND | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.<key>.ND[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | -s7iv3BsBXM | metadata | Unreferenced in project code |
| $.<key>.DS | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.<key>.DS[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | -ZyNUxtYarE | metadata | Unreferenced in project code |
| $.<key>.IS | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.<key>.IS[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | hbZCuelNak4 | metadata | Unreferenced in project code |

### `data/real_world/raw_metadata/invid_fivr200k/extracted/events.json`  - 11 fields, 1 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| $ | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $[] | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $[].headline | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | iraqi insurgency | metadata | Unreferenced in project code |
| $[].text | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $[].text[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | car bombings in baghdad kill at least 17 people an | metadata | Unreferenced in project code |
| $[].youtube | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $[].youtube[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | ZpjqUq-EnbQ | metadata | Unreferenced in project code |
| $[].topic | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | armed conflict and attack | metadata | Unreferenced in project code |
| $[].href | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $[].href[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | http://www.bbc.co.uk/news/world-middle-east-211412 | metadata | Unreferenced in project code |
| $[].date | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 2013-01-22 | metadata | Unreferenced in project code |

### `data/real_world/raw_metadata/invid_fivr200k/extracted/youtube_ids.txt`  - 1 fields, 225960 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| youtube_ids.txt | str | one value per line | see file | see file | 0 | 225960 | ---m4jjFPu0 | metadata | Used by downstream code |

---
# DS-010 - VCSL: video URLs, copied-segment labels, pair/split files

- **Family / component / category:** VCSL / metadata/annotations (URL-only) / Real-world source metadata (media NOT local)
- **Original publisher:** He et al., Ant Group (alipay/VCSL)
- **Original source:** https://github.com/alipay/VCSL
- **How it entered the project:** raw GitHub files (interactive; s1 re-fetches 7 files)
- **What was retained:** URL list, label file, pair files, categories, split_meta; no publisher checksum
- **Provenance category:** 2 Documented, not independently verified
- **Location:** `data/real_world/raw_metadata/vcsl` (CSV/JSON); availability: Metadata only (no media); state: metadata-only
- **Files / records / size:** 9 / 9207 / 42201384 bytes (0.042 GB)
- **Usable / excluded:** 166146 labelled pairs / 0
- **Licence:** code: MIT License; dataset licence NOT STATED in the repository snapshot
- **Referenced by code:** scripts/datasets/candidates.py:<module>@58; scripts/datasets/patch_round2.py:<module>@55; scripts/datasets/patch_round2.py:<module>@57; scripts/datasets/s1_fetch_metadata.py:<module>@7; scripts/datasets/s3_normalize.py:vcsl_rows@213; scripts/datasets/s3_normalize.py:vcsl_rows@215 (+5 more)
- **Actually used (verified class):** Preprocessing use verified
- **Necessity:** Conditionally useful - largest real partial-copy annotation set; media inaccessible; licence not stated
- **Retention:** Retain (metadata)
- **Limitations:** Dataset licence not stated (code MIT); media not downloaded; segment units assumed seconds (not verified); direction of copying not annotated

## How it is used in the problem statement and project
- **R-M3** (p5-6 Module 3 Relationship Detection): Compare two videos; share a source; direct/indirect derivation; likely vs uncertain; confidence + evidence
  - evidence it provides: 166,146 labelled pairs / 278,885 copied segments; fields/media used: label_file_uuid_total.json
  - consuming module: dataset pipeline script (no ORVEX application module exists in the repository); stage: normalise native edges; algorithm: none
  - input: `data/real_world/raw_metadata/vcsl/label_file_uuid_total.json`; code: yes: scripts/datasets/s3_normalize.py:vcsl_rows (lines 213-227)
  - output: DS-017 (RW-07 edges); evaluation: K12
  - status: **Partially implemented**; evidence: Demonstrated (metadata); limits: no media; direction unknown; dataset licence not stated

**Code touching this dataset (file : symbol : operation):** `scripts/datasets/candidates.py:<module>` (reference, lines 58-58); `scripts/datasets/patch_round2.py:<module>` (reference, lines 55-57); `scripts/datasets/s1_fetch_metadata.py:<module>` (reference, lines 7-7); `scripts/datasets/s3_normalize.py:<module>` (reference, lines 283-283); `scripts/datasets/s3_normalize.py:vcsl_rows` (read/consume, lines 213-217); `scripts/datasets/s5_features_pairs_splits.py:<module>` (reference, lines 206-206); `scripts/datasets/s6_docs.py:<module>` (reference, lines 62-62)

## Columns / fields (103 across 7 file(s))

### `data/real_world/raw_metadata/vcsl/label_file_uuid_total.json`  - 4 fields, 1 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| $ | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.<key> | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.<key>[] | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.<key>[][] | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 11 | metadata | Unreferenced in project code |

### `data/real_world/raw_metadata/vcsl/pair_file_test.csv`  - 2 fields, 54630 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| query_id | str | uuid of the query video in an evaluated pair | original source field | copied (native) | 0.0 | 925 | f9861a9dece845379078e666b9ed8bdd | benchmark pair (source split) | Unreferenced in project code |
| reference_id | str | uuid of the reference video in the pair | original source field | copied (native) | 0.0 | 1066 | 06b30f0db715454f83f633efd7a35deb | benchmark pair (source split) | Unreferenced in project code |

### `data/real_world/raw_metadata/vcsl/pair_file_train.csv`  - 2 fields, 97033 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| query_id | str | uuid of the query video in an evaluated pair | original source field | copied (native) | 0.0 | 2422 | eed33fe83df14e0b8d63135834654613 | benchmark pair (source split) | Unreferenced in project code |
| reference_id | str | uuid of the reference video in the pair | original source field | copied (native) | 0.0 | 2687 | 99b7e3b22da3458fa4efe01a7c5cd3f1 | benchmark pair (source split) | Unreferenced in project code |

### `data/real_world/raw_metadata/vcsl/pair_file_val.csv`  - 2 fields, 41798 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| query_id | str | uuid of the query video in an evaluated pair | original source field | copied (native) | 0.0 | 1221 | 53cb15bbf74e45379c68686648b3140a | benchmark pair (source split) | Unreferenced in project code |
| reference_id | str | uuid of the reference video in the pair | original source field | copied (native) | 0.0 | 1332 | 7c62f68892f149048df819c6fe1cfec1 | benchmark pair (source split) | Unreferenced in project code |

### `data/real_world/raw_metadata/vcsl/split_meta_pairs.json`  - 68 fields, 1 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| $ | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.train | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.train.<key> | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.train.<key>[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | eed33fe83df14e0b8d63135834654613-99b7e3b22da3458fa | metadata | Unreferenced in project code |
| $.val | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.val.<key> | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.val.<key>[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 53cb15bbf74e45379c68686648b3140a-7c62f68892f149048 | metadata | Unreferenced in project code |
| $.test | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.test.4f35a9a73d354cac8653eda43ccf8d8e | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.test.4f35a9a73d354cac8653eda43ccf8d8e[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 4f35a9a73d354cac8653eda43ccf8d8e-a3edf812b02d47a9a | metadata | Unreferenced in project code |
| $.test.88a654aa1cc84ad2b9703d0a5521e43f | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.test.88a654aa1cc84ad2b9703d0a5521e43f[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 944eeb60c5974982ae4e8255df012770-27af9e1470544930a | metadata | Unreferenced in project code |
| $.test.a372bb16d435449d8c089fcdaaf90ae4 | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.test.a372bb16d435449d8c089fcdaaf90ae4[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 4c7567f8b747461a9d0a5ab7d3514be1-97fda907a89d4f20b | metadata | Unreferenced in project code |
| $.test.f2998a313d9c4eadb1723fef854f9614 | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.test.f2998a313d9c4eadb1723fef854f9614[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 94cd102b44f74734abe5df19773b1894-d45f83f6546946c59 | metadata | Unreferenced in project code |
| $.test.d71408e317c64ce9bd3fd1139e3d5c0c | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.test.d71408e317c64ce9bd3fd1139e3d5c0c[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | f8539c582b69477fb0141efaa395abf2-a7bc977837604300b | metadata | Unreferenced in project code |
| $.test.4bfb654708444cc48ddda9c4de532aab | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.test.4bfb654708444cc48ddda9c4de532aab[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 4bfb654708444cc48ddda9c4de532aab-dd9fb00b686f4aa49 | metadata | Unreferenced in project code |
| $.test.166195baa824427a8d82a285c56adc00 | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.test.166195baa824427a8d82a285c56adc00[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 166195baa824427a8d82a285c56adc00-a6ff763c37f54ae68 | metadata | Unreferenced in project code |
| $.test.ac92d0ea6e11418788887bf8b2df38b3 | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.test.ac92d0ea6e11418788887bf8b2df38b3[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | ac92d0ea6e11418788887bf8b2df38b3-bc1e948cc9e64bffa | metadata | Unreferenced in project code |
| $.test.ff79943ea3cd44588f4da316a29a8e63 | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.test.ff79943ea3cd44588f4da316a29a8e63[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | ff79943ea3cd44588f4da316a29a8e63-9546ea50802547728 | metadata | Unreferenced in project code |
| $.test.05cb0d3087284ae9970a999baf6cb48a | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.test.05cb0d3087284ae9970a999baf6cb48a[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 5eeaa8dd5e8642c9a4291ef2fd6a24ad-c0ae154da7984cfeb | metadata | Unreferenced in project code |
| $.test.71b46673cae14e238ccebb966ba7fd86 | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.test.71b46673cae14e238ccebb966ba7fd86[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 71b46673cae14e238ccebb966ba7fd86-71b46673cae14e238 | metadata | Unreferenced in project code |
| $.test.b6c84b3f8b1e4c3280d4634c745e516c | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.test.b6c84b3f8b1e4c3280d4634c745e516c[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 7f229ec6118d4229bec80cb61e4b67f6-fbffe631e6a942da9 | metadata | Unreferenced in project code |
| $.test.78cb6c2d559c4de9a605042afa4d2bcb | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.test.78cb6c2d559c4de9a605042afa4d2bcb[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 78cb6c2d559c4de9a605042afa4d2bcb-78cb6c2d559c4de9a | metadata | Unreferenced in project code |
| $.test.7133109c1db64ad5b3c726df4462b470 | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.test.7133109c1db64ad5b3c726df4462b470[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 7133109c1db64ad5b3c726df4462b470-fbb9d4bdc37e47128 | metadata | Unreferenced in project code |
| $.test.88200e0f267d414aaadaf2bcd6e6ecfd | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.test.88200e0f267d414aaadaf2bcd6e6ecfd[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | d765992510d24c60ba064199dbf78c72-218eae5da56348768 | metadata | Unreferenced in project code |
| $.test.dd44c4be9fdc4c95bdf075e7e756294e | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.test.dd44c4be9fdc4c95bdf075e7e756294e[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | dd44c4be9fdc4c95bdf075e7e756294e-d4dfa28e9c024799b | metadata | Unreferenced in project code |
| $.test.06d224d87ea14fa5aec57903e8be37a0 | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.test.06d224d87ea14fa5aec57903e8be37a0[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 06d224d87ea14fa5aec57903e8be37a0-ae9cc6f7424a4628b | metadata | Unreferenced in project code |
| $.test.d54a1f1d31a94f5c92496b22bc6dc4b4 | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.test.d54a1f1d31a94f5c92496b22bc6dc4b4[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | d54a1f1d31a94f5c92496b22bc6dc4b4-58cb411c31c84cb48 | metadata | Unreferenced in project code |
| $.test.e45b9eec5ea54e00a2d6e6689cd5fe92 | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.test.e45b9eec5ea54e00a2d6e6689cd5fe92[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | e45b9eec5ea54e00a2d6e6689cd5fe92-e45b9eec5ea54e00a | metadata | Unreferenced in project code |
| $.test.aa2783f15e994ccc853f85460ad0ad20 | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.test.aa2783f15e994ccc853f85460ad0ad20[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | faf3a40cab6e4369bd7d72b167bd1fbe-7f19e8daae5240eaa | metadata | Unreferenced in project code |
| $.test.2d500266205d4adc8638d2fea37a00b7 | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.test.2d500266205d4adc8638d2fea37a00b7[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 2d500266205d4adc8638d2fea37a00b7-7f13ea8f074740778 | metadata | Unreferenced in project code |
| $.test.0ed7c63b71e446baaa27e351133f5726 | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.test.0ed7c63b71e446baaa27e351133f5726[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 00dcf4889ed64b83988e88af1fd7406f-8297a8a654804b0b8 | metadata | Unreferenced in project code |
| $.test.574f2f0aac6749999fdfb41e630c1d51 | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.test.574f2f0aac6749999fdfb41e630c1d51[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | ce78fd038bbd4c15b426699abdb2dc20-c49c0631eba84dcb9 | metadata | Unreferenced in project code |
| $.test.146c67ab895744e6b6b54dabeea4b64f | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.test.146c67ab895744e6b6b54dabeea4b64f[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 6c3e941483c24ecab8a41e256c6170f1-136d82349e5d403ab | metadata | Unreferenced in project code |
| $.test.ecfe5a8b0cd54cb8b0e51da72dca9f1e | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.test.ecfe5a8b0cd54cb8b0e51da72dca9f1e[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | dc9da8bb187e46ef9cfa823f091a62d0-9cebb811243d4b98b | metadata | Unreferenced in project code |
| $.test.029d0980e5e04c75b6defd03070f251f | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.test.029d0980e5e04c75b6defd03070f251f[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | ed26654f037648ab9950deedcc07435e-7fe3411d4f434132a | metadata | Unreferenced in project code |
| $.test.9e55757ab2f046a281dd1a25c6b247b5 | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.test.9e55757ab2f046a281dd1a25c6b247b5[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | bbe5b9e059ac43adb7e3078382648b80-466595dbcd9148148 | metadata | Unreferenced in project code |
| $.test.5b74e41445984be9bff4dbc9f7356306 | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.test.5b74e41445984be9bff4dbc9f7356306[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | c973905e790c4857a3c1b1ab7a8826bb-5a00fdef866e4e1a9 | metadata | Unreferenced in project code |
| $.test.ff20c83f1e554f479e7c6d270e00d3ce | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.test.ff20c83f1e554f479e7c6d270e00d3ce[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | ad54c12209b7412ab66fe11c88bbe820-30c60c1f2fdf492a8 | metadata | Unreferenced in project code |
| $.test.6c7d9a037f794846a0b79f8efeeee977 | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.test.6c7d9a037f794846a0b79f8efeeee977[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 479fff6293254d1ea5f03e40ab971e88-f5cf06b7022346bb9 | metadata | Unreferenced in project code |

### `data/real_world/raw_metadata/vcsl/video_categories.json`  - 23 fields, 1 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| $ | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.variety show | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.variety show[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 0000ab50f69044d898ffd71a3d215a81 | metadata | Unreferenced in project code |
| $.games | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.games[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 350524e8101844e19b2d0616e95a163f | metadata | Unreferenced in project code |
| $.music videos | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.music videos[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | cfa69f998f374401ae320eaef2f2bc6e | metadata | Unreferenced in project code |
| $.news | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.news[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 61ca6289ec904d38b04449d8572c0a76 | metadata | Unreferenced in project code |
| $.sports | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.sports[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | e0d9fe5810c4435ab27757c311c24f80 | metadata | Unreferenced in project code |
| $.daily life | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.daily life[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 845e547c5f034e5db65f20f9b14d7f47 | metadata | Unreferenced in project code |
| $.TV series | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.TV series[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 8d4a600203df4e48ba99a7b9bb76d9cc | metadata | Unreferenced in project code |
| $.kichiku | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.kichiku[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | e4a3df1a28304176b4a1e90920c34abb | metadata | Unreferenced in project code |
| $.advertisement | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.advertisement[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | fb41e7a8e1f74bed83a6366dd32c7c82 | metadata | Unreferenced in project code |
| $.animation | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.animation[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | e63f2a33267d41c8a9807c62e07d516c | metadata | Unreferenced in project code |
| $.movies | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.movies[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 61c30173a9f04b0cb6b5661b3c9e8d05 | metadata | Unreferenced in project code |

### `data/real_world/raw_metadata/vcsl/videos_url_uuid.csv`  - 2 fields, 9207 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| url | str | Source URL of a VCSL video (YouTube/Bilibili) | original source field | copied (native) | 0.0 | 9207 | https://www.youtube.com/watch?v=6rJndnVNMEY | metadata | Used by downstream code |
| uuid | str | VCSL internal video identifier used in all pair/label files | original source field | copied (native) | 0.0 | 9207 | 5a4188d704be4c48b21754e5ee7f2b34 | metadata | Unreferenced in project code |

---
# DS-011 - COVID-related misinformation videos and their spread (RW-31)

- **Family / component / category:** Knuutila COVID misinformation spread dataset / metadata/annotations (URL/id-only) / Real-world source metadata (media NOT local)
- **Original publisher:** Knuutila, A. (Zenodo)
- **Original source:** https://zenodo.org/records/4557828
- **How it entered the project:** interactive download from Zenodo 4557828 (md5 verified); NOT in s1_fetch_metadata.py
- **What was retained:** covid-misinfo-videos.csv.gz unmodified
- **Provenance category:** 1 Verified from repository evidence (external source not re-checked online)
- **Location:** `data/real_world/raw_metadata/covid_misinfo_4557828/covid-misinfo-videos.csv.gz` (CSV.GZ); availability: Metadata only (no media); state: metadata-only
- **Files / records / size:** 1 / 8122 / 4198098 bytes (0.004 GB)
- **Usable / excluded:** 8,122 video records / 0
- **Licence:** cc-by-4.0 (Zenodo snapshot; metadata)
- **Referenced by code:** scripts/datasets/patch_round2.py:<module>@47; scripts/datasets/patch_round2.py:<module>@54; scripts/datasets/patch_round2.py:<module>@57; scripts/datasets/s3_normalize.py:covid_rows@231; scripts/datasets/s3_normalize.py:covid_rows@232; scripts/datasets/s3_normalize.py:build_registry@274 (+2 more)
- **Actually used (verified class):** Preprocessing use verified
- **Necessity:** Useful and justified - only real spread timeline; insufficient for coordination
- **Retention:** Retain
- **Limitations:** No sharer accounts; publish/removal timestamps for a minority of videos; timezone unstated; derived tweet times partly outside stated window

## How it is used in the problem statement and project
- **R-M6** (p6 Module 6 Platform Integration): Permitted APIs; post IDs/URLs/timestamps/metadata; normalise; handle limits
  - evidence it provides: post timeline: 881 publish times, 420 removals, 257,326 tweet ids; fields/media used: published_timestamp, removal_timestamp, twitter_post_ids
  - consuming module: dataset pipeline script (no ORVEX application module exists in the repository); stage: observations; algorithm: snowflake decoding of tweet ids
  - input: `covid-misinfo-videos.csv.gz`; code: yes: scripts/datasets/s3_normalize.py:covid_rows (lines 231-268)
  - output: DS-018; evaluation: K32
  - status: **Partially implemented**; evidence: Demonstrated (derived times); limits: no sharer accounts; 2,236 derived times outside stated window
- **R-M7** (p6 Module 7 Campaign Detection): Cluster posts; posting times/accounts; coordination signals separate from similarity
  - evidence it provides: evidence layer for spread (not coordination); fields/media used: share_reference observations
  - consuming module: dataset pipeline script (no ORVEX application module exists in the repository); stage: none (campaign table empty); algorithm: none
  - input: `DS-018`; code: yes: scripts/datasets/s5_features_pairs_splits.py (module level)
  - output: DS-029 (empty); evaluation: K20
  - status: **Blocked**; evidence: Absent (no account+time evidence); limits: cannot support coordination claims

**Code touching this dataset (file : symbol : operation):** `scripts/datasets/patch_round2.py:<module>` (reference, lines 47-57); `scripts/datasets/s3_normalize.py:<module>` (reference, lines 283-283); `scripts/datasets/s3_normalize.py:build_registry` (reference, lines 274-274); `scripts/datasets/s3_normalize.py:covid_rows` (read/consume, lines 231-232); `scripts/datasets/update_report.py:<module>` (reference, lines 24-24)

## Columns / fields (14 across 1 file(s))

### `data/real_world/raw_metadata/covid_misinfo_4557828/covid-misinfo-videos.csv.gz`  - 14 fields, 8122 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| youtube_link | str | YouTube URL of the removed video | original source field | copied (native) | 0.0 | 8104 | https://youtube.com/watch?v=-0ERhEl3n4U | metadata | Used by downstream code |
| video_title | str | title where recoverable | original source field | copied (native) | 10.93 | 7120 | DA NON PERDERE! DR RASHID BUTTAR VS GATES E FAUCI | metadata | Used by downstream code |
| video_description | str | description where recoverable | original source field | copied (native) | 16.36 | 6544 | N. B. Per il RISPETTO di tutti, non saranno approv | metadata | Used by downstream code |
| view_count | int | views where recoverable | original source field | copied (native) | 88.49 | 914 | 1896 | metadata | Used by downstream code |
| channel_id | str | YouTube channel id of the video (publisher) | original source field | copied (native) | 88.49 | 712 | [masked] | metadata | Used by downstream code |
| subscriber_count | int | channel subscribers | original source field | copied (native) | 89.28 | 614 | 8 | metadata | Unreferenced in project code |
| removal_timestamp | datetime | when YouTube removed the video (timezone unstated) | original source field | copied (native) | 94.83 | 420 | 2020-05-16 23:31:30 | source annotation | Used by downstream code |
| published_timestamp | datetime | when the video was published (timezone unstated) | original source field | copied (native) | 89.15 | 144 | 2020-05-11 0:00:00 | metadata | Used by downstream code |
| archive_url | str | web-archive URL of the video | original source field | copied (native) | 88.49 | 934 | http://web.archive.org/web/20200511183250/https:// | metadata | Unreferenced in project code |
| facebook_graph_reactions | int | Facebook reactions count | original source field | copied (native) | 0.0 | 2480 | 700 | metadata (engagement) | Used by downstream code |
| facebook_graph_comments | int | Facebook comments count | original source field | copied (native) | 0.0 | 1822 | 183 | metadata (engagement) | Used by downstream code |
| facebook_graph_shares | int | Facebook shares count | original source field | copied (native) | 0.0 | 2248 | 1300 | metadata (engagement) | Used by downstream code |
| twitter_post_ids | json-in-string | list (as text) of Twitter post ids that shared the video | original source field | copied (native) | 35.79 | 5201 | [1254689102546558976, 1253642806704386048, 1253449 | metadata (share reference) | Used by downstream code |
| facebook_post_ids | json-in-string | list (as text) of Facebook post ids that shared the video | original source field | copied (native) | 5.26 | 7678 | [3396214160413490, 368262960761073, 52987530123626 | metadata (share reference) | Used by downstream code |

---
# DS-012 - Official record snapshots (Zenodo API, GitHub READMEs/licence)

- **Family / component / category:** provenance snapshots / metadata (provenance evidence) / Source metadata
- **Original publisher:** ORVEX project (generated)
- **Original source:** N/A (generated in this repository)
- **How it entered the project:** Zenodo API / GitHub raw (interactive + s1)
- **What was retained:** JSON API snapshots, READMEs, VCSL LICENSE
- **Provenance category:** 1 Verified from repository evidence (external source not re-checked online)
- **Location:** `data/real_world/raw_metadata` (JSON/MD); availability: Local files; state: raw
- **Files / records / size:** 11 / 11 / 61057 bytes (0.000 GB)
- **Usable / excluded:** all readable / 0
- **Licence:** mixed (API record snapshots)
- **Referenced by code:** scripts/datasets/audit.py:_@144; scripts/datasets/s1_fetch_metadata.py:<module>@10; scripts/datasets/s1_fetch_metadata.py:<module>@11
- **Actually used (verified class):** Preprocessing use verified (provenance/licence evidence read by audit and s1)
- **Necessity:** Essential - provenance evidence for licences/checksums
- **Retention:** Retain
- **Limitations:** Snapshots date from 2026-10-26; not re-fetched in this audit

## How it is used in the problem statement and project
- No requirement mapping (non-dataset asset or no verified role): intended module = R-RM-10.2

**Code touching this dataset (file : symbol : operation):** `scripts/datasets/audit.py:_` (read/consume, lines 144-144); `scripts/datasets/s1_fetch_metadata.py:<module>` (write/produce, lines 10-11)

## Columns / fields (128 across 1 file(s))

### `data/real_world/raw_metadata/zenodo_api/*.json`  - 128 fields, 7 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| $ | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.created | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 2018-01-15T13:59:55.553074+00:00 | metadata | Unreferenced in project code |
| $.modified | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 2020-01-24T19:26:03.275169+00:00 | metadata | Unreferenced in project code |
| $.id | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 1147958 | metadata | Unreferenced in project code |
| $.conceptrecid | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 1147957 | metadata | Unreferenced in project code |
| $.doi | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 10.5281/zenodo.1147958 | metadata | Unreferenced in project code |
| $.conceptdoi | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 10.5281/zenodo.1147957 | metadata | Unreferenced in project code |
| $.doi_url | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | https://doi.org/10.5281/zenodo.1147958 | metadata | Unreferenced in project code |
| $.metadata | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.metadata.title | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | InVID Fake Video Corpus v2.0 | metadata | Unreferenced in project code |
| $.metadata.doi | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 10.5281/zenodo.1147958 | metadata | Unreferenced in project code |
| $.metadata.publication_date | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 2018-01-15 | metadata | Unreferenced in project code |
| $.metadata.description | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | <p>The InVID TV Fake Video Corpus was developed in | metadata | Unreferenced in project code |
| $.metadata.access_right | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | open | metadata | Unreferenced in project code |
| $.metadata.creators | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.metadata.creators[] | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.metadata.creators[].name | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | Olga Papadopoulou | metadata | Unreferenced in project code |
| $.metadata.creators[].affiliation | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | CERTH-ITI, Thessaloniki, Greece | metadata | Unreferenced in project code |
| $.metadata.keywords | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.metadata.keywords[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | Fake video corpus | metadata | Unreferenced in project code |
| $.metadata.version | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 2.0 | metadata | Unreferenced in project code |
| $.metadata.references | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.metadata.references[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | Version v1.0 DOI: 10.5281/zenodo.242481 | metadata | Unreferenced in project code |
| $.metadata.language | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | eng | metadata | Unreferenced in project code |
| $.metadata.resource_type | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.metadata.resource_type.title | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | Dataset | metadata | Unreferenced in project code |
| $.metadata.resource_type.type | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | dataset | metadata | Unreferenced in project code |
| $.metadata.license | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.metadata.license.id | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | cc-by-4.0 | metadata | Unreferenced in project code |
| $.metadata.grants | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.metadata.grants[] | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.metadata.grants[].code | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 687786 | metadata | Unreferenced in project code |
| $.metadata.grants[].internal_id | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 10.13039/501100000780::687786 | metadata | Unreferenced in project code |
| $.metadata.grants[].funder | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.metadata.grants[].funder.name | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | European Commission | metadata | Unreferenced in project code |
| $.metadata.grants[].funder.doi | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 10.13039/501100000780 | metadata | Unreferenced in project code |
| $.metadata.grants[].funder.acronym | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | EC | metadata | Unreferenced in project code |
| $.metadata.grants[].title | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | In Video Veritas – Verification of Social Media Vi | metadata | Unreferenced in project code |
| $.metadata.grants[].acronym | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | InVID | metadata | Unreferenced in project code |
| $.metadata.grants[].program | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | H2020-EU.2.1.1. | metadata | Unreferenced in project code |
| $.metadata.grants[].url | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | https://cordis.europa.eu/projects/687786 | metadata | Unreferenced in project code |
| $.metadata.communities | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.metadata.communities[] | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.metadata.communities[].id | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | invid-h2020 | metadata | Unreferenced in project code |
| $.metadata.relations | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.metadata.relations.version | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.metadata.relations.version[] | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.metadata.relations.version[].index | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 0 | metadata | Unreferenced in project code |
| $.metadata.relations.version[].is_last | bool | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | True | metadata | Unreferenced in project code |
| $.metadata.relations.version[].parent | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.metadata.relations.version[].parent.pid_type | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | recid | metadata | Unreferenced in project code |
| $.metadata.relations.version[].parent.pid_value | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 1147957 | metadata | Unreferenced in project code |
| $.title | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | InVID Fake Video Corpus v2.0 | metadata | Unreferenced in project code |
| $.links | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.links.self | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | https://zenodo.org/api/records/1147958 | metadata | Unreferenced in project code |
| $.links.self_html | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | https://zenodo.org/records/1147958 | metadata | Unreferenced in project code |
| $.links.preview_html | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | https://zenodo.org/records/1147958?preview=1 | metadata | Unreferenced in project code |
| $.links.doi | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | https://doi.org/10.5281/zenodo.1147958 | metadata | Unreferenced in project code |
| $.links.self_doi | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | https://doi.org/10.5281/zenodo.1147958 | metadata | Unreferenced in project code |
| $.links.self_doi_html | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | https://zenodo.org/doi/10.5281/zenodo.1147958 | metadata | Unreferenced in project code |
| $.links.reserve_doi | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | https://zenodo.org/api/records/1147958/draft/pids/ | metadata | Unreferenced in project code |
| $.links.parent | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | https://zenodo.org/api/records/1147957 | metadata | Unreferenced in project code |
| $.links.parent_html | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | https://zenodo.org/records/1147957 | metadata | Unreferenced in project code |
| $.links.parent_doi | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | https://doi.org/10.5281/zenodo.1147957 | metadata | Unreferenced in project code |
| $.links.parent_doi_html | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | https://zenodo.org/doi/10.5281/zenodo.1147957 | metadata | Unreferenced in project code |
| $.links.self_iiif_manifest | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | https://zenodo.org/api/iiif/record:1147958/manifes | metadata | Unreferenced in project code |
| $.links.self_iiif_sequence | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | https://zenodo.org/api/iiif/record:1147958/sequenc | metadata | Unreferenced in project code |
| $.links.files | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | https://zenodo.org/api/records/1147958/files | metadata | Unreferenced in project code |
| $.links.media_files | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | https://zenodo.org/api/records/1147958/media-files | metadata | Unreferenced in project code |
| $.links.latest | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | https://zenodo.org/api/records/1147958/versions/la | metadata | Unreferenced in project code |
| $.links.latest_html | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | https://zenodo.org/records/1147958/latest | metadata | Unreferenced in project code |
| $.links.versions | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | https://zenodo.org/api/records/1147958/versions | metadata | Unreferenced in project code |
| $.links.draft | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | https://zenodo.org/api/records/1147958/draft | metadata | Unreferenced in project code |
| $.links.access_links | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | https://zenodo.org/api/records/1147958/access/link | metadata | Unreferenced in project code |
| $.links.access_grants | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | https://zenodo.org/api/records/1147958/access/gran | metadata | Unreferenced in project code |
| $.links.access_users | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | https://zenodo.org/api/records/1147958/access/user | metadata | Unreferenced in project code |
| $.links.access_request | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | https://zenodo.org/api/records/1147958/access/requ | metadata | Unreferenced in project code |
| $.links.access | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | https://zenodo.org/api/records/1147958/access | metadata | Unreferenced in project code |
| $.links.communities | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | https://zenodo.org/api/records/1147958/communities | metadata | Unreferenced in project code |
| $.links.communities-suggestions | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | https://zenodo.org/api/records/1147958/communities | metadata | Unreferenced in project code |
| $.links.request_deletion | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | https://zenodo.org/api/records/1147958/request-del | metadata | Unreferenced in project code |
| $.links.file_modification | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | https://zenodo.org/api/records/1147958/file-modifi | metadata | Unreferenced in project code |
| $.links.quota_increase | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | https://zenodo.org/api/records/1147958/quota-incre | metadata | Unreferenced in project code |
| $.links.requests | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | https://zenodo.org/api/records/1147958/requests | metadata | Unreferenced in project code |
| $.updated | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 2020-01-24T19:26:03.275169+00:00 | metadata | Unreferenced in project code |
| $.recid | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 1147958 | metadata | Unreferenced in project code |
| $.revision | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 6 | metadata | Unreferenced in project code |
| $.files | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.files[] | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.files[].id | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | e474e254-d3e0-4937-b025-1901dc01ecb0 | metadata | Unreferenced in project code |
| $.files[].key | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | Fake Video Corpus v2.0.zip | metadata | Unreferenced in project code |
| $.files[].size | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 21360 | metadata | Unreferenced in project code |
| $.files[].checksum | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | md5:c08d53adf9b85bc4ee595cd833e3304d | metadata | Unreferenced in project code |
| $.files[].links | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.files[].links.self | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | https://zenodo.org/api/records/1147958/files/Fake% | metadata | Unreferenced in project code |
| $.swh | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.owners | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.owners[] | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.owners[].id | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 27159 | metadata | Unreferenced in project code |
| $.status | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | published | metadata | Unreferenced in project code |
| $.stats | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.stats.downloads | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 408 | metadata | Unreferenced in project code |
| $.stats.unique_downloads | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 394 | metadata | Unreferenced in project code |
| $.stats.views | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 2518 | metadata | Unreferenced in project code |
| $.stats.unique_views | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 2267 | metadata | Unreferenced in project code |
| $.stats.version_downloads | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 406 | metadata | Unreferenced in project code |
| $.stats.version_unique_downloads | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 392 | metadata | Unreferenced in project code |
| $.stats.version_unique_views | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 2257 | metadata | Unreferenced in project code |
| $.stats.version_views | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 2505 | metadata | Unreferenced in project code |
| $.state | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | done | metadata | Unreferenced in project code |
| $.submitted | bool | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | True | metadata | Unreferenced in project code |
| $.metadata.creators[].orcid | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | 0000-0002-0498-7506 | metadata | Unreferenced in project code |
| $.metadata.resource_type.subtype | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | article | metadata | Unreferenced in project code |
| $.links.thumbnails | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.links.thumbnails.10 | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | https://zenodo.org/api/iiif/record:2535495:Papadop | metadata | Unreferenced in project code |
| $.links.thumbnails.50 | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | https://zenodo.org/api/iiif/record:2535495:Papadop | metadata | Unreferenced in project code |
| $.links.thumbnails.100 | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | https://zenodo.org/api/iiif/record:2535495:Papadop | metadata | Unreferenced in project code |
| $.links.thumbnails.250 | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | https://zenodo.org/api/iiif/record:2535495:Papadop | metadata | Unreferenced in project code |
| $.links.thumbnails.750 | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | https://zenodo.org/api/iiif/record:2535495:Papadop | metadata | Unreferenced in project code |
| $.links.thumbnails.1200 | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | https://zenodo.org/api/iiif/record:2535495:Papadop | metadata | Unreferenced in project code |
| $.metadata.related_identifiers | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.metadata.related_identifiers[] | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.metadata.related_identifiers[].identifier | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | https://arxiv.org/abs/1809.04094 | metadata | Unreferenced in project code |
| $.metadata.related_identifiers[].relation | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | isSupplementTo | metadata | Unreferenced in project code |
| $.metadata.related_identifiers[].scheme | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | url | metadata | Unreferenced in project code |
| $.metadata.alternate_identifiers | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.metadata.alternate_identifiers[] | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.metadata.alternate_identifiers[].identifier | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Original source field | see file | n/a | n/a | arXiv:1809.04094 | metadata | Unreferenced in project code |

---
# DS-013 - Controlled variant media

- **Family / component / category:** ORVEX controlled variants / media files / Controlled variants (derived from real-world media)
- **Original publisher:** ORVEX project (generated)
- **Original source:** N/A (generated in this repository)
- **How it entered the project:** ORVEX scripts (see Processing History)
- **What was retained:** generated artefact
- **Provenance category:** 1 Verified from repository evidence (external source not re-checked online)
- **Location:** `data/controlled_variants/media` (mp4); availability: Local files; state: derived/processed
- **Files / records / size:** 1132 / 1132 / 12500690021 bytes (12.501 GB)
- **Usable / excluded:** 1132 readable; 1131 passed validation; 673 trainable / 2 failed (no file kept)
- **Licence:** N/A (ORVEX-generated; inherits source licence)
- **Referenced by code:** scripts/datasets/audit.py:_@61; scripts/datasets/audit.py:_@63; scripts/datasets/audit.py:_@189; scripts/datasets/common.py:<module>@9; scripts/datasets/common.py:<module>@21; scripts/datasets/patch_round3.py:<module>@23 (+9 more)
- **Actually used (verified class):** Preprocessing use verified; Evaluation use verified (baseline)
- **Necessity:** Essential - ground-truth derivations; 12.5 GB; regenerable from DS-001 + scripts but costly
- **Retention:** Retain
- **Limitations:** Constructed experimental artefacts (not natural posts); audio/caption from other real records; 2 variants failed validation and were not retained

## How it is used in the problem statement and project
- **R-M3** (p5-6 Module 3 Relationship Detection): Compare two videos; share a source; direct/indirect derivation; likely vs uncertain; confidence + evidence
  - evidence it provides: 1,131 validated variants with parents; fields/media used: variant_media_id, direct_parent_media_id, transformation_name
  - consuming module: dataset pipeline script (no ORVEX application module exists in the repository); stage: ground-truth derivations; algorithm: FFmpeg transformations
  - input: `data/controlled_variants/media/*`; code: yes: scripts/datasets/s4_variants.py:make (lines 75-105)
  - output: DS-014, DS-017, DS-023; evaluation: K04/K11/K15 + independent ffprobe in this audit
  - status: **Implemented (data)**; evidence: Demonstrated; limits: controlled; not natural
- **R-M9b** (p8 Phase 1 step 7; p11 §9.6): Unseen sources and transformations
  - evidence it provides: 4 held-out transformation types (T11-T14); fields/media used: transformation_id, usable_for_training
  - consuming module: dataset pipeline script (no ORVEX application module exists in the repository); stage: evaluation protocol; algorithm: held-out lineage rule
  - input: `DS-014`; code: yes: scripts/datasets/s5_features_pairs_splits.py:lineage_heldout (lines 39-44)
  - output: DS-023.includes_heldout_transform; evaluation: K14
  - status: **Implemented (data)**; evidence: Demonstrated: dHash detection mirror 0.143; limits: unseen types are FFmpeg edits
- **R-M4** (p6 Module 4 Manipulation Analysis): Trimming/cropping, captions, audio replacement, inconsistencies
  - evidence it provides: trim/crop/caption/audio edits with ground truth; fields/media used: transformation_name, params
  - consuming module: dataset pipeline script (no ORVEX application module exists in the repository); stage: labels; algorithm: FFmpeg
  - input: `DS-014`; code: yes: scripts/datasets/s4_variants.py:build (lines 20-46)
  - output: DS-014; evaluation: coverage report
  - status: **Implemented (data)**; evidence: Demonstrated; limits: no detector built

**Code touching this dataset (file : symbol : operation):** `scripts/datasets/audit.py:_` (reference, lines 61-189); `scripts/datasets/common.py:<module>` (reference, lines 9-21); `scripts/datasets/patch_round3.py:<module>` (reference, lines 23-23); `scripts/datasets/s4_variants.py:make` (reference, lines 80-80); `scripts/datasets/s4_variants.py:process` (write/produce, lines 71-71); `scripts/datasets/s4b_purge_ineligible.py:<module>` (reference, lines 3-16); `scripts/datasets/s6_docs.py:<module>` (reference, lines 72-78); `scripts/datasets/s7_manifests.py:<module>` (reference, lines 69-69); `scripts/datasets/s8_necessity_audit.py:<module>` (read/consume, lines 67-97)

## Columns / fields
This component has no structured columns (media files, archives or documents).

---
# DS-014 - Controlled variant registry

- **Family / component / category:** ORVEX controlled variants / table / Created table (lineage ground truth)
- **Original publisher:** ORVEX project (generated)
- **Original source:** N/A (generated in this repository)
- **How it entered the project:** ORVEX scripts (see Processing History)
- **What was retained:** generated artefact
- **Provenance category:** 1 Verified from repository evidence (external source not re-checked online)
- **Location:** `data/derived/tables/controlled_variant_registry.csv` (CSV); availability: Local files; state: derived/processed
- **Files / records / size:** 1 / 1133 / 1094515 bytes (0.001 GB)
- **Usable / excluded:** 1131 passed / 2 failed
- **Licence:** N/A (ORVEX-generated; inherits source licence)
- **Referenced by code:** scripts/datasets/audit.py:_@44; scripts/datasets/audit.py:_@49; scripts/datasets/audit.py:_@59; scripts/datasets/audit.py:_@67; scripts/datasets/audit.py:_@84; scripts/datasets/audit.py:_@88 (+19 more)
- **Actually used (verified class):** Preprocessing + Evaluation use verified
- **Necessity:** Essential - lineage ground truth
- **Retention:** Retain
- **Limitations:** Ground truth only for controlled edits

## How it is used in the problem statement and project
- **R-M1** (p5 Module 1 Dataset Creation): Import source videos; identify duplicates; unique IDs; generate variants; record transformation + parent; save relationships
  - evidence it provides: parent/transformation per variant; fields/media used: direct_parent_media_id, root_source_media_id, ancestor_chain
  - consuming module: dataset pipeline script (no ORVEX application module exists in the repository); stage: registry; algorithm: none
  - input: `data/derived/tables/controlled_variant_registry.csv`; code: yes: scripts/datasets/s4_variants.py:process (lines 68-118)
  - output: DS-017; evaluation: K04
  - status: **Implemented**; evidence: Demonstrated; limits: one failed variant still has a file on disk

**Code touching this dataset (file : symbol : operation):** `scripts/datasets/audit.py:_` (read/consume, lines 44-177); `scripts/datasets/s5_features_pairs_splits.py:<module>` (write/produce, lines 48-48); `scripts/datasets/s6_docs.py:<module>` (read/consume, lines 76-132); `scripts/datasets/s7_manifests.py:<module>` (reference, lines 9-9); `scripts/datasets/s8_necessity_audit.py:<module>` (read/consume, lines 17-47); `scripts/datasets/s9_feature_baseline.py:<module>` (read/consume, lines 21-21); `scripts/datasets/schema.py:<module>` (read/consume, lines 103-103); `tests/test_dataset_package.py:test_controlled_variant_ids_are_not_natural_ids` (read/consume, lines 26-26)

## Columns / fields (38 across 1 file(s))

### `data/derived/tables/controlled_variant_registry.csv`  - 38 fields, 1133 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| variant_media_id | str | Id of the created video (CV-...). | added by ORVEX | bookkeeping/administrative | 0.0 | 1133 | CV-P10491224-V01 | metadata | Used by downstream code |
| direct_parent_media_id | str | Immediate parent (real source or earlier variant). | added by ORVEX | bookkeeping/administrative | 0.0 | 385 | RW-CMN-P10491224 | ground truth (controlled lineage) | Used by downstream code |
| root_source_media_id | str | Real-world root source. | added by ORVEX | bookkeeping/administrative | 0.0 | 55 | RW-CMN-P10491224 | ground truth (controlled lineage) | Used by downstream code |
| ancestor_chain | str | Pipe-separated ancestors up to the root. | added by ORVEX | derived by deterministic rule/inferred | 0.0 | 385 | RW-CMN-P10491224 | ground truth (controlled lineage) | Referenced by audit/docs/tests only |
| video_source_media_id | str | Real-world source of the picture track. | added by ORVEX | bookkeeping/administrative | 0.0 | 55 | RW-CMN-P10491224 | metadata | Referenced by audit/docs/tests only |
| audio_source_media_id | str | Real-world source of replaced/mixed audio. | added by ORVEX | bookkeeping/administrative | 91.26 | 33 | RW-CMN-P115080780 | metadata | Used by downstream code |
| caption_text_source_media_id | str | Real-world record the caption text came from. | added by ORVEX | bookkeeping/administrative | 90.29 | 30 | RW-CMN-P176367262 | metadata | Used by downstream code |
| caption_text | str | Caption burned in. | original source field | normalized/renamed | 90.29 | 30 | Ballistische Kurve | metadata | Used by downstream code |
| caption_text_origin_field | str | Field of the source record used (commons_title). | added by ORVEX | bookkeeping/administrative | 90.29 | 1 | title | metadata | Referenced by audit/docs/tests only |
| transformation_id | str | T01-T14. | added by ORVEX | bookkeeping/administrative | 0.0 | 14 | T01 | ground truth (controlled lineage) | Used by downstream code |
| transformation_name | str | Name. | added by ORVEX | bookkeeping/administrative | 0.0 | 14 | reencode_hq | ground truth (controlled lineage) | Used by downstream code |
| transformation_family | str | Family. | added by ORVEX | bookkeeping/administrative | 0.0 | 6 | compression | metadata | Referenced by audit/docs/tests only |
| parameters_json | json-in-string | Exact parameters. | added by ORVEX | bookkeeping/administrative | 0.0 | 260 | {"crf": 18} | ground truth (controlled lineage) | Used by downstream code |
| tool_name | str | ffmpeg. | added by ORVEX | bookkeeping/administrative | 0.0 | 1 | ffmpeg | metadata | Used by downstream code |
| tool_version | str | Tool version. | added by ORVEX | computed from media/files by a tool | 0.0 | 1 | ffmpeg version 9.0.2-essentials_build-www.gyan.dev | derived metadata/feature | Used by downstream code |
| run_id | str | Run id. | added by ORVEX | bookkeeping/administrative | 0.0 | 1133 | RUN-CV-P10491224-V01 | metadata | Used by downstream code |
| seed | str | Deterministic selection key. | added by ORVEX | bookkeeping/administrative | 0.0 | 55 | sha256-pick:RW-CMN-P10491224 | metadata | Used by downstream code |
| created_utc | datetime | Creation time. | added by ORVEX | bookkeeping/administrative | 0.0 | 1008 | 2026-10-26T06:41:04Z | metadata | Used by downstream code |
| local_path | str | Path of the created file (blank for failed variants: no file retained). | added by ORVEX | bookkeeping/administrative | 0.18 | 1131 | data/controlled_variants/media/P10491224/CV-P10491 | metadata | Used by downstream code |
| sha256 | str | Output hash (blank for failed variants). | added by ORVEX | computed from media/files by a tool | 0.18 | 1131 | f7bd4dfed1436d66ee06426a562c740f5a5f921b43257cfec5 | derived metadata/feature | Used by downstream code |
| bytes | int | Output size. | added by ORVEX | computed from media/files by a tool | 0.0 | 1132 | 5755540 | derived metadata/feature | Used by downstream code |
| duration_s | float | Output duration. | added by ORVEX | computed from media/files by a tool | 0.0 | 380 | 27.133 | derived metadata/feature | Used by downstream code |
| width | int | Width. | added by ORVEX | computed from media/files by a tool | 0.0 | 25 | 720 | derived metadata/feature | Used by downstream code |
| height | int | Height. | added by ORVEX | computed from media/files by a tool | 0.0 | 23 | 576 | derived metadata/feature | Used by downstream code |
| fps | float | fps. | added by ORVEX | computed from media/files by a tool | 0.0 | 49 | 30.0 | derived metadata/feature | Used by downstream code |
| has_audio | bool | Audio present. | added by ORVEX | computed from media/files by a tool | 0.0 | 2 | True | derived metadata/feature | Used by downstream code |
| generation_depth | int | Edits from the real root. | added by ORVEX | derived by deterministic rule/inferred | 0.0 | 3 | 1 | derived metadata/feature | Used by downstream code |
| chain_id | str | Chain id. | added by ORVEX | bookkeeping/administrative | 66.02 | 5 | C1 | metadata | Used by downstream code |
| permission_basis | str | Why the transformation is permitted. | added by ORVEX | derived by deterministic rule/inferred | 0.0 | 41 | CC BY-SA 3.0 permits adaptation (root); audio/capt | derived metadata/feature | Referenced by audit/docs/tests only |
| root_license | str | Licence of root. | original source field | copied | 0.0 | 7 | CC BY-SA 3.0 | metadata | Referenced by audit/docs/tests only |
| validation_status | str | passed/failed/not_run. | added by ORVEX | computed from media/files by a tool | 0.0 | 2 | passed | derived metadata/feature | Used by downstream code |
| validation_checks_json | json-in-string | Checks and results. | added by ORVEX | computed from media/files by a tool | 0.0 | 1051 | {"probe_ok": true, "duration_expected_s": 27.13, " | derived metadata/feature | Referenced by audit/docs/tests only |
| failure_reason | str | Reason if failed. | added by ORVEX | bookkeeping/administrative | 99.82 | 1 | validation checks failed | metadata | Referenced by audit/docs/tests only |
| media_origin | str | Always controlled_variant. | added by ORVEX | bookkeeping/administrative | 0.0 | 1 | controlled_variant | metadata | Used by downstream code |
| record_origin | str | Always orvex_controlled_variant_record. | added by ORVEX | bookkeeping/administrative | 0.0 | 1 | orvex_controlled_variant_record | metadata | Used by downstream code |
| transformation_status | str | controlled_transformation_applied / failed. | added by ORVEX | bookkeeping/administrative | 0.0 | 2 | controlled_transformation_applied | metadata | Referenced by audit/docs/tests only |
| usable_for_training | bool | True only if passed, train split and no held-out transform in lineage. | added by ORVEX | derived by deterministic rule/inferred | 0.0 | 2 | True | derived metadata/feature | Used by downstream code |
| source_split | str | Split of the root source family. | added by ORVEX | derived by deterministic rule/inferred | 0.0 | 3 | train | derived metadata/feature | Used by downstream code |

---
# DS-015 - Transformation run log

- **Family / component / category:** ORVEX controlled variants / table / Created table (processing log)
- **Original publisher:** ORVEX project (generated)
- **Original source:** N/A (generated in this repository)
- **How it entered the project:** ORVEX scripts (see Processing History)
- **What was retained:** generated artefact
- **Provenance category:** 1 Verified from repository evidence (external source not re-checked online)
- **Location:** `data/derived/tables/transformation_run_log.csv` (CSV); availability: Local files; state: derived/processed
- **Files / records / size:** 1 / 1133 / 954337 bytes (0.001 GB)
- **Usable / excluded:** 1133 runs / 0
- **Licence:** N/A (ORVEX-generated; inherits source licence)
- **Referenced by code:** scripts/datasets/patch_round3.py:<module>@89; scripts/datasets/s5_features_pairs_splits.py:<module>@48; scripts/datasets/s6_docs.py:<module>@84; scripts/datasets/s6_docs.py:<module>@96; scripts/datasets/s6_docs.py:<module>@150; scripts/datasets/s8_necessity_audit.py:<module>@18 (+1 more)
- **Actually used (verified class):** Test-only use (audit/tests) plus s4 writer
- **Necessity:** Useful and justified - reproducibility log
- **Retention:** Retain
- **Limitations:** Command lines abstract the root path

## How it is used in the problem statement and project
- No requirement mapping (non-dataset asset or no verified role): intended module = R-WF1-3

**Code touching this dataset (file : symbol : operation):** `scripts/datasets/patch_round3.py:<module>` (reference, lines 89-89); `scripts/datasets/s5_features_pairs_splits.py:<module>` (write/produce, lines 48-48); `scripts/datasets/s6_docs.py:<module>` (reference, lines 84-150); `scripts/datasets/s8_necessity_audit.py:<module>` (read/consume, lines 18-18); `scripts/datasets/schema.py:<module>` (read/consume, lines 224-224)

## Columns / fields (15 across 1 file(s))

### `data/derived/tables/transformation_run_log.csv`  - 15 fields, 1133 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| run_id | str | Run id. | added by ORVEX | bookkeeping/administrative | 0.0 | 1133 | RUN-CV-P10491224-V01 | metadata | Used by downstream code |
| variant_media_id | str | Output. | added by ORVEX | bookkeeping/administrative | 0.0 | 1133 | CV-P10491224-V01 | metadata | Used by downstream code |
| input_media_ids | str | Inputs (video/audio donor). | added by ORVEX | bookkeeping/administrative | 0.0 | 440 | RW-CMN-P10491224 | metadata | Referenced by audit/docs/tests only |
| tool_name | str | Tool. | added by ORVEX | bookkeeping/administrative | 0.0 | 1 | ffmpeg | metadata | Used by downstream code |
| tool_version | str | Version. | added by ORVEX | computed from media/files by a tool | 0.0 | 1 | ffmpeg version 9.0.2-essentials_build-www.gyan.dev | derived metadata/feature | Used by downstream code |
| command_config | str | Full argument list (root path abstracted). | added by ORVEX | bookkeeping/administrative | 0.0 | 1133 | -y -v error -i <ROOT>\data/real_world/media/common | metadata | Referenced by audit/docs/tests only |
| parameters_json | json-in-string | Parameters. | added by ORVEX | bookkeeping/administrative | 0.0 | 260 | {"crf": 18} | metadata | Used by downstream code |
| started_utc | datetime | Time. | added by ORVEX | bookkeeping/administrative | 0.0 | 1008 | 2026-10-26T06:41:04Z | metadata | Referenced by audit/docs/tests only |
| return_code | int | Exit code. | added by ORVEX | computed from media/files by a tool | 0.0 | 1 | 0 | derived metadata/feature | Referenced by audit/docs/tests only |
| output_validation_status | str | passed/failed. | added by ORVEX | computed from media/files by a tool | 0.0 | 2 | passed | derived metadata/feature | Referenced by audit/docs/tests only |
| output_bytes | int | Bytes. | added by ORVEX | computed from media/files by a tool | 0.0 | 1133 | 5755540 | derived metadata/feature | Referenced by audit/docs/tests only |
| storage_delta_bytes | int | Payload change. | added by ORVEX | computed from media/files by a tool | 0.0 | 1133 | 5755540 | derived metadata/feature | Referenced by audit/docs/tests only |
| error | empty | stderr tail. | added by ORVEX | bookkeeping/administrative | 100.0 | 0 |  | metadata | Used by downstream code |
| deterministic_notes | str | Determinism notes. | added by ORVEX | bookkeeping/administrative | 0.0 | 1 | parameters fixed; donor/caption picked by sha256 o | metadata | Referenced by audit/docs/tests only |
| seed | str | Selection key. | added by ORVEX | bookkeeping/administrative | 0.0 | 55 | sha256-pick:RW-CMN-P10491224 | metadata | Used by downstream code |

---
# DS-016 - Real-world media master

- **Family / component / category:** ORVEX normalised master / table / Created table (normalised real-world records; no variants)
- **Original publisher:** ORVEX project (generated)
- **Original source:** N/A (generated in this repository)
- **How it entered the project:** ORVEX scripts (see Processing History)
- **What was retained:** generated artefact
- **Provenance category:** 1 Verified from repository evidence (external source not re-checked online)
- **Location:** `data/derived/tables/real_world_media_master.csv` (CSV); availability: Local files; state: derived/processed
- **Files / records / size:** 1 / 252270 / 148756771 bytes (0.149 GB)
- **Usable / excluded:** 596 rows with local media; 251674 metadata-only / duplicates mapped in DS-026
- **Licence:** N/A (ORVEX-generated; inherits source licence)
- **Referenced by code:** scripts/datasets/audit.py:_@44; scripts/datasets/audit.py:_@49; scripts/datasets/audit.py:_@59; scripts/datasets/audit.py:_@67; scripts/datasets/audit.py:_@75; scripts/datasets/audit.py:_@79 (+34 more)
- **Actually used (verified class):** Preprocessing use verified
- **Necessity:** Essential - identity/provenance master
- **Retention:** Retain
- **Limitations:** metadata-only rows have no media; labels are source-published

## How it is used in the problem statement and project
- **R-M1** (p5 Module 1 Dataset Creation): Import source videos; identify duplicates; unique IDs; generate variants; record transformation + parent; save relationships
  - evidence it provides: 252,270 normalised records; fields/media used: media_id, source_dataset_id, access_status
  - consuming module: dataset pipeline script (no ORVEX application module exists in the repository); stage: master table; algorithm: none
  - input: `data/derived/tables/real_world_media_master.csv`; code: yes: scripts/datasets/s3_normalize.py:qc_commons (lines 55-114); scripts/datasets/s3_normalize.py:anakin_rows (lines 117-147); scripts/datasets/s3_normalize.py:fvc_rows (lines 150-192); scripts/datasets/s3_normalize.py:f
  - output: DS-016; evaluation: K03/K07
  - status: **Implemented**; evidence: Demonstrated; limits: metadata-only rows have no media

**Code touching this dataset (file : symbol : operation):** `scripts/datasets/audit.py:_` (read/consume, lines 44-221); `scripts/datasets/patch_round3.py:<module>` (read/consume, lines 27-89); `scripts/datasets/s3_normalize.py:<module>` (write/produce, lines 303-303); `scripts/datasets/s4_variants.py:<module>` (read/consume, lines 121-121); `scripts/datasets/s4b_purge_ineligible.py:<module>` (read/consume, lines 8-8); `scripts/datasets/s5_features_pairs_splits.py:<module>` (read/consume, lines 14-14); `scripts/datasets/s6_docs.py:<module>` (read/consume, lines 76-150); `scripts/datasets/s7_manifests.py:<module>` (reference, lines 9-9); `scripts/datasets/s8_necessity_audit.py:<module>` (read/consume, lines 17-17); `scripts/datasets/schema.py:<module>` (read/consume, lines 57-57) ... (+2 more in DATASET_TO_IMPLEMENTATION_MAP.csv)

## Columns / fields (49 across 1 file(s))

### `data/derived/tables/real_world_media_master.csv`  - 49 fields, 252270 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| media_id | str | Stable internal id (RW-<src>-...). | added by ORVEX | bookkeeping/administrative | 0.0 | 252270 | RW-CMN-P14634957 | metadata | Used by downstream code |
| source_dataset_id | str | Source dataset. | added by ORVEX | bookkeeping/administrative | 0.0 | 8 | RW-01 | metadata | Used by downstream code |
| release_version | int | Release/version of source. | original source field | copied | 1.24 | 6 | 2018 | metadata | Used by downstream code |
| native_record_id | str | Native id of the record. | original source field | copied | 0.0 | 244997 | 14634957 | source annotation (ground truth as published by dataset authors) | Used by downstream code |
| native_media_id | str | Native media id. | original source field | copied | 0.0 | 252001 | File:Ante Pavelić Speech 21051941.ogv | source annotation (ground truth as published by dataset authors) | Used by downstream code |
| platform | str | Platform normalized to lowercase name. | original source field | normalized/renamed | 0.0 | 7 | wikimedia_commons | metadata | Used by downstream code |
| platform_media_id | str | Platform video id. | added by ORVEX | derived by deterministic rule/inferred | 0.0 | 250856 | 14634957 | derived metadata/feature | Used by downstream code |
| source_url | str | Source URL as published. | original source field | copied | 0.0 | 251879 | https://commons.wikimedia.org/wiki/File:Ante_Pavel | metadata | Used by downstream code |
| canonical_url | str | Canonical URL (scheme/host lowercased, tracking removed). | added by ORVEX | derived by deterministic rule/inferred | 0.0 | 251879 | https://commons.wikimedia.org/wiki/File:Ante_Pavel | derived metadata/feature | Used by downstream code |
| title | str | Title if the source has one. | original source field | copied | 94.52 | 8367 | File:Ante Pavelić Speech 21051941.ogv | metadata | Used by downstream code |
| description_caption | str | Caption/description. | original source field | copied | 96.77 | 7671 | Ante Pavelić Speech | metadata | Referenced by audit/docs/tests only |
| publisher_account_id | str | Publisher account as published; pseudonymise in reports. | original source field | normalized/renamed | 99.14 | 888 | [masked] | metadata | Referenced by audit/docs/tests only |
| event_or_cascade_id | str | Group the record belongs to. | original source field | copied | 7.02 | 5742 | 4zyvv7 | metadata | Referenced by audit/docs/tests only |
| published_time_utc | datetime | Publish time (only when the source provides one). | original source field | normalized/renamed | 99.61 | 240 | 2011-03-18T10:36:10Z | metadata | Used by downstream code |
| observed_time_utc | empty | Observation time if provided by source (rare). | added by ORVEX | bookkeeping/administrative | 100.0 | 0 |  | metadata | Referenced by audit/docs/tests only |
| collected_time_utc | datetime | When ORVEX collected/registered the record. | added by ORVEX | bookkeeping/administrative | 0.0 | 1 | 2026-10-26T15:02:46Z | metadata | Used by downstream code |
| time_precision | str | second / unknown. | added by ORVEX | bookkeeping/administrative | 0.0 | 3 | second | metadata | Used by downstream code |
| duration_s | float | Duration (downloaded media only). | added by ORVEX | computed from media/files by a tool | 99.76 | 200 | 522.893 | derived metadata/feature | Used by downstream code |
| width | int | Width. | added by ORVEX | computed from media/files by a tool | 99.76 | 28 | 320 | derived metadata/feature | Used by downstream code |
| height | int | Height. | added by ORVEX | computed from media/files by a tool | 99.76 | 29 | 240 | derived metadata/feature | Used by downstream code |
| fps | float | Frame rate. | added by ORVEX | computed from media/files by a tool | 99.76 | 26 | 0.0 | derived metadata/feature | Used by downstream code |
| video_codec | str | Video codec. | added by ORVEX | computed from media/files by a tool | 99.76 | 5 | theora | derived metadata/feature | Used by downstream code |
| audio_codec | str | Audio codec. | added by ORVEX | computed from media/files by a tool | 99.78 | 4 | vorbis | derived metadata/feature | Used by downstream code |
| has_audio | bool | Audio stream present. | added by ORVEX | computed from media/files by a tool | 99.76 | 2 | True | derived metadata/feature | Used by downstream code |
| container | str | Container. | added by ORVEX | computed from media/files by a tool | 99.76 | 3 | ogg | derived metadata/feature | Used by downstream code |
| file_bytes | int | File size. | added by ORVEX | computed from media/files by a tool | 99.76 | 584 | 23898980 | derived metadata/feature | Referenced by audit/docs/tests only |
| local_path | str | Relative path of local file. | added by ORVEX | bookkeeping/administrative | 99.76 | 596 | data/real_world/media/commons/RW-CMN-P14634957.ogv | metadata | Used by downstream code |
| sha256 | str | File hash (locally computed). | added by ORVEX | computed from media/files by a tool | 99.76 | 596 | abc7b993b3d64239823134f765b99432619d3217c0d400dce8 | derived metadata/feature | Used by downstream code |
| access_status | str | Access status. | added by ORVEX | bookkeeping/administrative | 0.0 | 2 | downloaded_authorized | metadata | Used by downstream code |
| playable_status | str | playable / unplayable / not_checked. | added by ORVEX | computed from media/files by a tool | 0.0 | 3 | playable | derived metadata/feature | Used by downstream code |
| rights_status | str | Rights decision for storage/processing. | added by ORVEX | derived by deterministic rule/inferred | 0.0 | 5 | licence_permits_storage_transformation_redistribut | derived metadata/feature | Referenced by audit/docs/tests only |
| license | str | Licence. | original source field | copied | 0.39 | 13 | Public domain | metadata | Used by downstream code |
| license_url | str | Licence URL. | original source field | copied | 4.05 | 9 | https://creativecommons.org/licenses/by/4.0 | metadata | Used by downstream code |
| attribution | str | Attribution string. | original source field | copied | 0.39 | 92 | Ante_Pavelić | metadata | Referenced by audit/docs/tests only |
| record_origin | str | Origin of the record. | added by ORVEX | bookkeeping/administrative | 0.0 | 1 | real_world_source_record | metadata | Used by downstream code |
| media_origin | str | Origin of the media. | added by ORVEX | bookkeeping/administrative | 0.0 | 3 | naturally_collected_real_world | metadata | Used by downstream code |
| native_authenticity_label | str | Native label exactly as published. | original source field | copied | 97.68 | 5 | fake | source annotation (ground truth as published by dataset authors) | Used by downstream code |
| native_misleading_label | str | Native label (same field) kept separately. | original source field | copied | 94.46 | 6 | fake | source annotation (ground truth as published by dataset authors) | Referenced by audit/docs/tests only |
| native_manipulation_type | str | Native manipulation type. | original source field | copied | 99.58 | 8 | frame-level | source annotation (ground truth as published by dataset authors) | Used by downstream code |
| normalized_authenticity_status | str | unknown unless the native label states it; 'fake' in FVC = debunked, NOT AI-generated. | added by ORVEX | derived by deterministic rule/inferred | 0.0 | 3 | unknown | normalised label / policy status (not model prediction) | Referenced by audit/docs/tests only |
| normalized_misleading_status | str | debunked_misleading / verified_not_misleading / not_assessed. | added by ORVEX | derived by deterministic rule/inferred | 0.0 | 4 | not_assessed | normalised label / policy status (not model prediction) | Used by downstream code |
| coordination_status | str | not_assessed for every record: no independent account/time coordination evidence exists locally. | added by ORVEX | bookkeeping/administrative | 0.0 | 1 | not_assessed | normalised label / policy status (not model prediction) | Used by downstream code |
| evidence_id | str | Evidence record backing the source annotation / licence of this record. | added by ORVEX | bookkeeping/administrative | 0.0 | 103 | EV-CMN-14634957 | metadata | Used by downstream code |
| perceptual_hash_ref | str | Reference to the computed 24-frame dHash features (local media only). | added by ORVEX | computed from media/files by a tool | 99.76 | 1 | data/derived/features/visual_dhash24.jsonl | derived metadata/feature | Used by downstream code |
| annotation_status | str | source_annotation / none. | added by ORVEX | bookkeeping/administrative | 0.0 | 2 | none | metadata | Used by downstream code |
| qc_flags | str | Flags (too_short, no_audio, decode_errors...). | added by ORVEX | derived by deterministic rule/inferred | 99.98 | 11 | too_long(>120s) | derived metadata/feature | Used by downstream code |
| duplicate_of_media_id | str | Canonical media id if this is a duplicate. | added by ORVEX | derived by deterministic rule/inferred | 99.9 | 207 | RW-CMN-P128562512 | derived metadata/feature | Used by downstream code |
| usable_for_variants | bool | Eligible as source for controlled variants. | added by ORVEX | derived by deterministic rule/inferred | 0.0 | 2 | False | derived metadata/feature | Used by downstream code |
| missingness_note | str | Why fields are null. | added by ORVEX | bookkeeping/administrative | 0.0 | 9 | no native relationship/authenticity labels in sour | metadata | Used by downstream code |

---
# DS-017 - Media relationship edges

- **Family / component / category:** ORVEX relationships / table / Created table (native relations + controlled lineage)
- **Original publisher:** ORVEX project (generated)
- **Original source:** N/A (generated in this repository)
- **How it entered the project:** ORVEX scripts (see Processing History)
- **What was retained:** generated artefact
- **Provenance category:** 1 Verified from repository evidence (external source not re-checked online)
- **Location:** `data/derived/tables/media_relationship_edges.csv` (CSV); availability: Local files; state: derived/processed
- **Files / records / size:** 1 / 299875 / 149867390 bytes (0.150 GB)
- **Usable / excluded:** 1480 edges with local media / 298395 metadata-only
- **Licence:** N/A (ORVEX-generated; inherits source licence)
- **Referenced by code:** scripts/datasets/audit.py:_@44; scripts/datasets/audit.py:_@92; scripts/datasets/audit.py:_@96; scripts/datasets/audit.py:_@181; scripts/datasets/audit.py:_@216; scripts/datasets/patch_round3.py:<module>@45 (+16 more)
- **Actually used (verified class):** Preprocessing use verified
- **Necessity:** Essential - relationship ground truth/graph edges
- **Retention:** Retain; fix noted defects first
- **Limitations:** only 1480 edges have media locally; native edges are not derivation proof

## How it is used in the problem statement and project
- **R-M5** (p6 Module 5 Relationship Graph): Nodes/edges, parent-child, manipulation type per connection
  - evidence it provides: 299,875 typed edges with direction/evidence status; fields/media used: media_a_id, media_b_id, normalized_relation_type, direction_status, evidence_id
  - consuming module: dataset pipeline script (no ORVEX application module exists in the repository); stage: edge table (no graph store); algorithm: none
  - input: `data/derived/tables/media_relationship_edges.csv`; code: yes: scripts/datasets/s5_features_pairs_splits.py (module level)
  - output: edge table; evaluation: K11/K12
  - status: **Partially implemented (table; no graph build)**; evidence: Demonstrated; limits: 61 dangling endpoints; IS edges unnormalised; no numeric confidence

**Code touching this dataset (file : symbol : operation):** `scripts/datasets/audit.py:_` (read/consume, lines 44-216); `scripts/datasets/patch_round3.py:<module>` (read/consume, lines 45-45); `scripts/datasets/patch_round6.py:<module>` (read/consume, lines 9-10); `scripts/datasets/s3_normalize.py:<module>` (write/produce, lines 303-303); `scripts/datasets/s5_features_pairs_splits.py:<module>` (read+write, lines 52-68); `scripts/datasets/s6_docs.py:<module>` (read/consume, lines 61-132); `scripts/datasets/s8_necessity_audit.py:<module>` (read/consume, lines 17-17); `scripts/datasets/schema.py:<module>` (read/consume, lines 134-134)

## Columns / fields (29 across 1 file(s))

### `data/derived/tables/media_relationship_edges.csv`  - 29 fields, 299875 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| relationship_id | str | Edge id. | added by ORVEX | bookkeeping/administrative | 0.0 | 299875 | REL-0000001 | metadata | Used by downstream code |
| source_dataset_id | str | Where the relation comes from (or ORVEX-CTRL). | added by ORVEX | bookkeeping/administrative | 0.0 | 5 | RW-02 | metadata | Used by downstream code |
| relation_scope | str | real_native / controlled_lineage. | added by ORVEX | bookkeeping/administrative | 0.0 | 2 | real_native | metadata | Used by downstream code |
| evidence_id | str | Evidence record. | added by ORVEX | bookkeeping/administrative | 0.0 | 1135 | EV-ANK-meta | metadata | Used by downstream code |
| media_a_id | str | First item. | added by ORVEX | bookkeeping/administrative | 0.0 | 7320 | RW-ANK-4zyvv7-T | metadata | Used by downstream code |
| media_b_id | str | Second item. | added by ORVEX | bookkeeping/administrative | 0.0 | 25220 | RW-ANK-4zyvv7-E | metadata | Used by downstream code |
| native_media_a_id | str | Native id of A. | original source field | copied | 0.41 | 5961 | 4zyvv7 | source annotation (ground truth as published by dataset authors) | Referenced by audit/docs/tests only |
| native_media_b_id | str | Native id of B. | original source field | copied | 0.41 | 23108 | 4zyvv7 | source annotation (ground truth as published by dataset authors) | Referenced by audit/docs/tests only |
| native_label | str | Label exactly as published. | original source field | copied | 0.41 | 16 | frame-level | source annotation (ground truth as published by dataset authors) | Used by downstream code |
| normalized_relation_type | str | e.g. near_duplicate, partial_temporal_copy, same_scene_not_copy, same_incident_not_copy, edited_version, controlled_*. | added by ORVEX | derived by deterministic rule/inferred | 0.0 | 19 | edited_version_of_trimmed_clip | ground truth label (source or controlled) - normalised | Used by downstream code |
| direction_status | str | Direction support. | added by ORVEX | derived by deterministic rule/inferred | 0.0 | 4 | directed_supported_by_source | ground truth label (source or controlled) - normalised | Used by downstream code |
| parent_media_id | str | Parent. | added by ORVEX | derived by deterministic rule/inferred | 98.92 | 2382 | RW-ANK-4zyvv7-T | ground truth label (source or controlled) - normalised | Used by downstream code |
| child_media_id | str | Child. | added by ORVEX | derived by deterministic rule/inferred | 98.92 | 3128 | RW-ANK-4zyvv7-E | ground truth label (source or controlled) - normalised | Used by downstream code |
| a_segment_start_s | int | Copied segment start in A. | original source field | copied | 6.67 | 1880 | 0 | metadata | Referenced by audit/docs/tests only |
| a_segment_end_s | int | End in A. | original source field | copied | 6.67 | 1597 | 8 | metadata | Referenced by audit/docs/tests only |
| b_segment_start_s | int | Start in B. | original source field | copied | 7.0 | 2170 | 164 | metadata | Referenced by audit/docs/tests only |
| b_segment_end_s | int | End in B. | original source field | copied | 7.0 | 1878 | 497 | metadata | Referenced by audit/docs/tests only |
| overlap_ratio | empty | Copied-duration ratio when measurable. | added by ORVEX | derived by deterministic rule/inferred | 100.0 | 0 |  | derived metadata/feature | Referenced by audit/docs/tests only |
| transformation_type | str | Transformation type. | added by ORVEX | bookkeeping/administrative | 5.92 | 21 | frame-level | metadata | Used by downstream code |
| label_source | str | source_annotation / controlled_transformation_log. | added by ORVEX | bookkeeping/administrative | 0.0 | 2 | source_annotation | metadata | Used by downstream code |
| label_status | str | Label status. | added by ORVEX | bookkeeping/administrative | 0.0 | 2 | source_ground_truth | ground truth label (source or controlled) - normalised | Used by downstream code |
| evidence_status | str | kind of evidence behind the label: source_annotation / controlled_transformation_log (separate from label status). | added by ORVEX | bookkeeping/administrative | 0.0 | 2 | source_annotation | ground truth label (source or controlled) - normalised | Used by downstream code |
| confidence_status | str | No numeric confidence: source_ground_truth / controlled_ground_truth. | added by ORVEX | bookkeeping/administrative | 0.0 | 2 | source_ground_truth_not_calibrated | metadata | Used by downstream code |
| reviewer | empty | Reviewer id (none yet). | added by ORVEX | analyst/human decision | 100.0 | 0 |  | derived metadata/feature | Referenced by audit/docs/tests only |
| method_version | str | Script version. | added by ORVEX | bookkeeping/administrative | 0.0 | 2 | s3_normalize.py@1 | metadata | Used by downstream code |
| created_utc | datetime | Creation time. | added by ORVEX | bookkeeping/administrative | 0.0 | 1008 | 2026-10-26T15:02:46Z | metadata | Used by downstream code |
| media_available_locally | bool | Both media bytes present locally. | added by ORVEX | computed from media/files by a tool | 0.0 | 2 | True | derived metadata/feature | Used by downstream code |
| conflict_flag | bool | Conflicting labels between sources. | added by ORVEX | derived by deterministic rule/inferred | 0.0 | 1 | False | derived metadata/feature | Used by downstream code |
| notes | str | Notes. | added by ORVEX | bookkeeping/administrative | 0.0 | 924 | editor task: Speeding up/Slowing down : 33% | metadata | Used by downstream code |

---
# DS-018 - Platform observations

- **Family / component / category:** ORVEX timeline / table / Created table (real post/upload/removal observations)
- **Original publisher:** ORVEX project (generated)
- **Original source:** N/A (generated in this repository)
- **How it entered the project:** ORVEX scripts (see Processing History)
- **What was retained:** generated artefact
- **Provenance category:** 1 Verified from repository evidence (external source not re-checked online)
- **Location:** `data/derived/tables/platform_observations.csv` (CSV); availability: Local files; state: derived/processed
- **Files / records / size:** 1 / 352702 / 110755040 bytes (0.111 GB)
- **Usable / excluded:** see quality audit / 2,236 tweet times flagged unverified
- **Licence:** N/A (ORVEX-generated; inherits source licence)
- **Referenced by code:** scripts/datasets/audit.py:_@153; scripts/datasets/audit.py:_@216; scripts/datasets/audit.py:_@221; scripts/datasets/patch_round3.py:<module>@45; scripts/datasets/patch_round3.py:<module>@50; scripts/datasets/patch_round3.py:<module>@89 (+11 more)
- **Actually used (verified class):** Test/audit use only downstream of s3
- **Necessity:** Useful and justified - timeline evidence
- **Retention:** Retain
- **Limitations:** No sharer accounts; derived tweet times; FVC order only

## How it is used in the problem statement and project
- **R-M6** (p6 Module 6 Platform Integration): Permitted APIs; post IDs/URLs/timestamps/metadata; normalise; handle limits
  - evidence it provides: 352,702 observations; fields/media used: platform, post_url, publish_time_utc, observation_type
  - consuming module: dataset pipeline script (no ORVEX application module exists in the repository); stage: normalised observations; algorithm: none
  - input: `data/derived/tables/platform_observations.csv`; code: yes: scripts/datasets/s3_normalize.py:covid_rows (lines 231-268)
  - output: DS-018; evaluation: K22/K32
  - status: **Partially implemented**; evidence: Demonstrated; limits: no live connector

**Code touching this dataset (file : symbol : operation):** `scripts/datasets/audit.py:_` (read/consume, lines 153-221); `scripts/datasets/patch_round3.py:<module>` (read/consume, lines 45-94); `scripts/datasets/s3_normalize.py:<module>` (write/produce, lines 303-303); `scripts/datasets/s6_docs.py:<module>` (reference, lines 85-155); `scripts/datasets/s8_necessity_audit.py:<module>` (read/consume, lines 17-17); `scripts/datasets/schema.py:<module>` (read/consume, lines 156-156); `scripts/datasets/update_report.py:<module>` (reference, lines 14-14)

## Columns / fields (22 across 1 file(s))

### `data/derived/tables/platform_observations.csv`  - 22 fields, 352702 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| observation_id | str | Id. | added by ORVEX | bookkeeping/administrative | 0.0 | 352308 | OBS-CMN-14634957 | metadata | Used by downstream code |
| media_id | str | Media observed. | added by ORVEX | bookkeeping/administrative | 0.0 | 13797 | RW-CMN-P14634957 | metadata | Used by downstream code |
| observation_type | str | upload / publish / removal / share_reference / cascade_member. | added by ORVEX | bookkeeping/administrative | 0.0 | 5 | upload | metadata | Used by downstream code |
| coordination_status | str | not_assessed: no independent coordination evidence. | added by ORVEX | bookkeeping/administrative | 0.0 | 1 | not_assessed | normalised label / policy status (not model prediction) | Used by downstream code |
| platform | str | Platform. | original source field | normalized/renamed | 0.0 | 4 | wikimedia_commons | metadata | Used by downstream code |
| platform_post_id | str | Post/video id. | added by ORVEX | derived by deterministic rule/inferred | 0.0 | 350932 | 14634957 | derived metadata/feature | Used by downstream code |
| post_url | str | URL. | original source field | copied | 23.01 | 269923 | https://commons.wikimedia.org/wiki/File:Ante_Pavel | metadata | Used by downstream code |
| account_id_pseudonym | str | Pseudonymised account id (policy). | added by ORVEX | derived by deterministic rule/inferred | 99.71 | 791 | [masked] | derived metadata/feature | Referenced by audit/docs/tests only |
| account_id_source_field | str | Source field used (commons uploader) or null. | added by ORVEX | bookkeeping/administrative | 99.71 | 2 | commons_uploader_username | metadata | Referenced by audit/docs/tests only |
| publish_time_utc | datetime | Publish time. | original source field | normalized/renamed | 26.76 | 249753 | 2011-03-18T10:36:10Z | metadata | Used by downstream code |
| observation_time_utc | datetime | Observation time. | added by ORVEX | bookkeeping/administrative | 99.88 | 420 | 2020-05-16T23:31:30 | metadata | Referenced by audit/docs/tests only |
| time_precision | str | second / unknown. | added by ORVEX | bookkeeping/administrative | 0.0 | 4 | second | metadata | Used by downstream code |
| caption_text | str | Caption. | original source field | copied | 99.97 | 91 | Ante Pavelić Speech | metadata | Used by downstream code |
| hashtags | empty | Not provided. | added by ORVEX | bookkeeping/administrative | 100.0 | 0 |  | metadata | Referenced by audit/docs/tests only |
| engagement_refs | str | Permitted engagement/reuse reference. | original source field | copied | 97.67 | 7763 | commons_global_usage_count=2 | metadata | Referenced by audit/docs/tests only |
| metadata_source | str | Source dataset. | added by ORVEX | bookkeeping/administrative | 0.0 | 3 | RW-01 | metadata | Referenced by audit/docs/tests only |
| collection_method | str | official_api / dataset_file. | added by ORVEX | bookkeeping/administrative | 0.0 | 2 | official_api | metadata | Referenced by audit/docs/tests only |
| order_in_cascade | int | Temporal order inside cascade as stated by the authors (not a timestamp). | added by ORVEX | derived by deterministic rule/inferred | 98.42 | 224 | 0 | derived metadata/feature | Referenced by audit/docs/tests only |
| cascade_id | str | Cascade id. | original source field | copied | 98.42 | 380 | f0 | metadata | Referenced by audit/docs/tests only |
| access_status | str | Access. | added by ORVEX | bookkeeping/administrative | 0.0 | 2 | downloaded_authorized | metadata | Used by downstream code |
| evidence_id | str | Evidence. | added by ORVEX | bookkeeping/administrative | 0.0 | 98 | EV-CMN-14634957 | metadata | Used by downstream code |
| limitations | str | Limitations. | added by ORVEX | bookkeeping/administrative | 0.0 | 7 | upload event only; not a social-media distribution | metadata | Used by downstream code |

---
# DS-019 - Evidence ledger

- **Family / component / category:** ORVEX evidence / table / Created table (evidence records)
- **Original publisher:** ORVEX project (generated)
- **Original source:** N/A (generated in this repository)
- **How it entered the project:** ORVEX scripts (see Processing History)
- **What was retained:** generated artefact
- **Provenance category:** 1 Verified from repository evidence (external source not re-checked online)
- **Location:** `data/derived/tables/evidence_ledger.csv` (CSV); availability: Local files; state: derived/processed
- **Files / records / size:** 1 / 1237 / 670524 bytes (0.001 GB)
- **Usable / excluded:** all / 0
- **Licence:** N/A (ORVEX-generated; inherits source licence)
- **Referenced by code:** scripts/datasets/patch_round2.py:<module>@15; scripts/datasets/patch_round3.py:<module>@89; scripts/datasets/patch_round6.py:<module>@9; scripts/datasets/patch_round6.py:<module>@10; scripts/datasets/patch_round6.py:<module>@11; scripts/datasets/s3_normalize.py:<module>@303 (+14 more)
- **Actually used (verified class):** Preprocessing use verified
- **Necessity:** Useful and justified - evidence traceability
- **Retention:** Retain
- **Limitations:** dataset-level evidence for native relations (not per-edge)

## How it is used in the problem statement and project
- **R-M8** (p6-7 Module 8 Dashboard/report): Upload reference; view relations/evidence; export report
  - evidence it provides: 1,237 evidence records; fields/media used: evidence_id, claim_supported, source_url
  - consuming module: dataset pipeline script (no ORVEX application module exists in the repository); stage: evidence ledger; algorithm: none
  - input: `data/derived/tables/evidence_ledger.csv`; code: yes: scripts/datasets/s3_normalize.py:evid (lines 42-45)
  - output: report input (not built); evaluation: K03/K31
  - status: **Partially implemented (ledger only)**; evidence: Indirect; limits: no report generator; dataset-level evidence for native relations

**Code touching this dataset (file : symbol : operation):** `scripts/datasets/patch_round2.py:<module>` (reference, lines 15-15); `scripts/datasets/patch_round3.py:<module>` (reference, lines 89-89); `scripts/datasets/patch_round6.py:<module>` (read/consume, lines 9-11); `scripts/datasets/s3_normalize.py:<module>` (write/produce, lines 303-303); `scripts/datasets/s5_features_pairs_splits.py:<module>` (read+write, lines 51-175); `scripts/datasets/s6_docs.py:<module>` (reference, lines 85-150); `scripts/datasets/s8_necessity_audit.py:<module>` (reference, lines 122-122); `scripts/datasets/schema.py:<module>` (read/consume, lines 93-173); `scripts/datasets/update_report.py:<module>` (reference, lines 15-15)

## Columns / fields (18 across 1 file(s))

### `data/derived/tables/evidence_ledger.csv`  - 18 fields, 1237 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| evidence_id | str | Id. | added by ORVEX | bookkeeping/administrative | 0.0 | 1237 | EV-CMN-14634957 | metadata | Used by downstream code |
| evidence_type | str | source_annotation / source_metadata / controlled_transformation_log / machine_measurement / license_record. | added by ORVEX | bookkeeping/administrative | 0.0 | 5 | license_record | metadata | Used by downstream code |
| source_dataset_id | str | Source. | added by ORVEX | bookkeeping/administrative | 0.0 | 9 | RW-01 | metadata | Used by downstream code |
| subject_type | str | media / relationship_set / variant / license. | added by ORVEX | bookkeeping/administrative | 0.0 | 3 | media | metadata | Used by downstream code |
| subject_id | str | Subject id or set name. | added by ORVEX | bookkeeping/administrative | 0.0 | 1237 | RW-CMN-P14634957 | metadata | Used by downstream code |
| source_url | str | URL. | original source field | copied | 91.67 | 103 | https://commons.wikimedia.org/wiki/File:Ante_Pavel | metadata | Used by downstream code |
| source_record_ref | str | Where inside the source. | added by ORVEX | bookkeeping/administrative | 0.0 | 1236 | Commons API extmetadata pageid=14634957 | metadata | Used by downstream code |
| claim_supported | str | What this evidence supports. | added by ORVEX | bookkeeping/administrative | 0.0 | 1149 | licence Public domain permits storage/transformati | metadata | Used by downstream code |
| claim_status | str | source_asserted / measured / controlled_by_construction. | added by ORVEX | bookkeeping/administrative | 0.0 | 3 | source_asserted | metadata | Used by downstream code |
| observed_fact_vs_inference | str | observed_fact / source_annotation / machine_measurement / analyst_inference. | added by ORVEX | bookkeeping/administrative | 0.0 | 3 | source_annotation | metadata | Used by downstream code |
| verification_method | str | How checked. | added by ORVEX | bookkeeping/administrative | 0.0 | 8 | Commons API machine-readable licence | metadata | Used by downstream code |
| evidence_time_utc | datetime | When evidence was recorded. | added by ORVEX | bookkeeping/administrative | 0.0 | 1010 | 2026-10-26T15:02:46Z | metadata | Used by downstream code |
| temporal_precision | str | Precision. | added by ORVEX | bookkeeping/administrative | 0.0 | 2 | date | metadata | Used by downstream code |
| file_sha256 | str | Hash of the evidence file. | added by ORVEX | computed from media/files by a tool | 0.24 | 1234 | abc7b993b3d64239823134f765b99432619d3217c0d400dce8 | derived metadata/feature | Used by downstream code |
| reviewer_status | str | unreviewed / source_curated. | added by ORVEX | bookkeeping/administrative | 0.0 | 2 | unreviewed | metadata | Used by downstream code |
| permission_status | str | Permission. | added by ORVEX | derived by deterministic rule/inferred | 0.0 | 7 | licence_permits | derived metadata/feature | Used by downstream code |
| confidence_basis | str | No calibrated numeric confidence; basis stated. | added by ORVEX | bookkeeping/administrative | 0.0 | 3 | source_curated_annotation_no_calibrated_confidence | metadata | Used by downstream code |
| limitations | str | Limitations. | added by ORVEX | bookkeeping/administrative | 8.33 | 2 | constructed experimental artefact, not a natural p | metadata | Used by downstream code |

---
# DS-020 - Feature manifest

- **Family / component / category:** ORVEX features / table / Created table (feature index)
- **Original publisher:** ORVEX project (generated)
- **Original source:** N/A (generated in this repository)
- **How it entered the project:** ORVEX scripts (see Processing History)
- **What was retained:** generated artefact
- **Provenance category:** 1 Verified from repository evidence (external source not re-checked online)
- **Location:** `data/derived/tables/feature_manifest.csv` (CSV); availability: Local files; state: derived/processed
- **Files / records / size:** 1 / 5187 / 2252894 bytes (0.002 GB)
- **Usable / excluded:** computed records only / not_computed placeholders (no files)
- **Licence:** N/A (ORVEX-generated; inherits source licence)
- **Referenced by code:** scripts/datasets/audit.py:_@135; scripts/datasets/patch_round2.py:<module>@16; scripts/datasets/s5b_feature_hashes.py:<module>@11; scripts/datasets/s5b_feature_hashes.py:<module>@17; scripts/datasets/s5_features_pairs_splits.py:<module>@99; scripts/datasets/s6_docs.py:<module>@86 (+10 more)
- **Actually used (verified class):** Preprocessing use verified
- **Necessity:** Useful and justified - feature index
- **Retention:** Retain
- **Limitations:** only dHash/audio features exist; embeddings/OCR/ASR rows say not_computed

## How it is used in the problem statement and project
- **R-M2** (p5 Module 2 Media Processing): Extract frames/audio/text; OCR; visual/audio/text representations; store fingerprints
  - evidence it provides: 5,187 feature index rows (6 types not_computed); fields/media used: media_id + feature values
  - consuming module: dataset pipeline script (no ORVEX application module exists in the repository); stage: feature extraction; algorithm: dHash / PCM md5 / RMS envelope
  - input: `local media`; code: yes: scripts/datasets/s5_features_pairs_splits.py:feat (lines 71-82)
  - output: feature jsonl/manifest; evaluation: K17 + baseline
  - status: **Partially implemented**; evidence: Demonstrated; limits: weak for crop/mirror; no learned embeddings

**Code touching this dataset (file : symbol : operation):** `scripts/datasets/audit.py:_` (read/consume, lines 135-135); `scripts/datasets/patch_round2.py:<module>` (reference, lines 16-16); `scripts/datasets/s5_features_pairs_splits.py:<module>` (write/produce, lines 99-99); `scripts/datasets/s5b_feature_hashes.py:<module>` (read+write, lines 11-17); `scripts/datasets/s6_docs.py:<module>` (reference, lines 86-135); `scripts/datasets/s8_necessity_audit.py:<module>` (read/consume, lines 83-109); `scripts/datasets/schema.py:<module>` (read/consume, lines 94-204)

## Columns / fields (15 across 1 file(s))

### `data/derived/tables/feature_manifest.csv`  - 15 fields, 5187 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| feature_record_id | str | Id. | added by ORVEX | bookkeeping/administrative | 0.0 | 5187 | FEAT-000001 | feature (computed) / feature index | Referenced by audit/docs/tests only |
| media_id | str | Media or ALL_LOCAL for aggregate rows. | added by ORVEX | bookkeeping/administrative | 0.0 | 1728 | RW-CMN-P14634957 | feature (computed) / feature index | Used by downstream code |
| feature_type | str | visual_dhash_24 / audio_pcm_md5_8k / audio_envelope_1s / visual_embedding / audio_embedding / ocr_text / asr_transcript / text_embedding / scene_bound | added by ORVEX | bookkeeping/administrative | 0.0 | 9 | visual_dhash24 | feature (computed) / feature index | Used by downstream code |
| extraction_status | str | computed / not_computed / failed. | added by ORVEX | computed from media/files by a tool | 0.0 | 2 | computed | feature (computed) / feature index | Used by downstream code |
| tool_name | str | Tool. | added by ORVEX | bookkeeping/administrative | 0.12 | 1 | opencv-python+ffmpeg+numpy | feature (computed) / feature index | Used by downstream code |
| tool_version | str | Version. | added by ORVEX | computed from media/files by a tool | 0.12 | 1 | opencv 4.12.0; ffmpeg version 9.0.2 | feature (computed) / feature index | Used by downstream code |
| parameters_json | json-in-string | Parameters. | added by ORVEX | bookkeeping/administrative | 0.12 | 1 | {"frames": 24, "dhash": "9x8 grayscale", "audio":  | feature (computed) / feature index | Used by downstream code |
| sample_timestamps | str | Sample positions. | added by ORVEX | computed from media/files by a tool | 66.72 | 415 | 0,568,1136,1704,2273,2841,3409,3977,4546,5114,5682 | feature (computed) / feature index | Referenced by audit/docs/tests only |
| feature_format | str | Format/dimension. | added by ORVEX | bookkeeping/administrative | 0.12 | 3 | 64-bit hex x24 | feature (computed) / feature index | Referenced by audit/docs/tests only |
| storage_path | str | File holding the feature. | added by ORVEX | bookkeeping/administrative | 0.12 | 2 | data/derived/features/visual_dhash24.jsonl | feature (computed) / feature index | Referenced by audit/docs/tests only |
| storage_bytes | int | Size. | added by ORVEX | computed from media/files by a tool | 10.16 | 83 | 407 | feature (computed) / feature index | Used by downstream code |
| feature_sha256 | str | Hash. | added by ORVEX | computed from media/files by a tool | 10.16 | 3637 | f29f705bf9ff2a6f437c1fce643f23d0e598d027dd8051fe73 | feature (computed) / feature index | Used by downstream code |
| extracted_utc | datetime | Time. | added by ORVEX | bookkeeping/administrative | 0.12 | 1 | 2026-10-26T18:06:44Z | feature (computed) / feature index | Referenced by audit/docs/tests only |
| error | str | Error. | added by ORVEX | bookkeeping/administrative | 89.84 | 3 | no audio stream | feature (computed) / feature index | Used by downstream code |
| permission_status | str | Permission. | added by ORVEX | derived by deterministic rule/inferred | 0.0 | 1 | licence_permits | feature (computed) / feature index | Used by downstream code |

---
# DS-021 - Visual 24-frame dHash features

- **Family / component / category:** ORVEX features / feature file / Derived feature (perceptual hash)
- **Original publisher:** ORVEX project (generated)
- **Original source:** N/A (generated in this repository)
- **How it entered the project:** ORVEX scripts (see Processing History)
- **What was retained:** generated artefact
- **Provenance category:** 1 Verified from repository evidence (external source not re-checked online)
- **Location:** `data/derived/features/visual_dhash24.jsonl` (JSONL); availability: Local files; state: derived/processed
- **Files / records / size:** 1 / 1727 / 1133311 bytes (0.001 GB)
- **Usable / excluded:** all local media / media with no decodable frames
- **Licence:** N/A (ORVEX-generated; inherits source licence)
- **Referenced by code:** scripts/datasets/audit.py:_@136; scripts/datasets/audit.py:_@138; scripts/datasets/patch_round2.py:<module>@16; scripts/datasets/patch_round2.py:<module>@61; scripts/datasets/s3_normalize.py:<module>@287; scripts/datasets/s5b_feature_hashes.py:<module>@7 (+9 more)
- **Actually used (verified class):** Evaluation use verified (baseline)
- **Necessity:** Essential - baseline and candidate-retrieval fingerprint
- **Retention:** Retain
- **Limitations:** weak for crop/mirror (see baseline)

## How it is used in the problem statement and project
- **R-M2** (p5 Module 2 Media Processing): Extract frames/audio/text; OCR; visual/audio/text representations; store fingerprints
  - evidence it provides: 1,727 visual hash records; fields/media used: media_id + feature values
  - consuming module: dataset pipeline script (no ORVEX application module exists in the repository); stage: feature extraction; algorithm: dHash / PCM md5 / RMS envelope
  - input: `local media`; code: yes: scripts/datasets/s5_features_pairs_splits.py:feat (lines 71-82)
  - output: feature jsonl/manifest; evaluation: K17 + baseline
  - status: **Partially implemented**; evidence: Demonstrated; limits: weak for crop/mirror; no learned embeddings
- **R-M3** (p5-6 Module 3 Relationship Detection): Compare two videos; share a source; direct/indirect derivation; likely vs uncertain; confidence + evidence
  - evidence it provides: baseline relatedness scoring; fields/media used: dhash24
  - consuming module: dataset pipeline script (no ORVEX application module exists in the repository); stage: baseline evaluation; algorithm: frame-match fraction >= 0.45
  - input: `visual_dhash24.jsonl`; code: yes: scripts/datasets/s9_feature_baseline.py (module level)
  - output: DS-030; evaluation: ROC-AUC
  - status: **Partially implemented (non-learned)**; evidence: Demonstrated: test AUC 0.8307; limits: 34% of test positives score 0

**Code touching this dataset (file : symbol : operation):** `scripts/datasets/audit.py:_` (reference, lines 136-138); `scripts/datasets/patch_round2.py:<module>` (reference, lines 16-61); `scripts/datasets/s3_normalize.py:<module>` (reference, lines 287-287); `scripts/datasets/s5_features_pairs_splits.py:<module>` (write/produce, lines 85-101); `scripts/datasets/s5b_feature_hashes.py:<module>` (read/consume, lines 7-15); `scripts/datasets/s9_feature_baseline.py:<module>` (read/consume, lines 12-12); `scripts/datasets/schema.py:<module>` (reference, lines 94-94)

## Columns / fields (6 across 1 file(s))

### `data/derived/features/visual_dhash24.jsonl`  - 6 fields, 500 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| $ | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.media_id | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | RW-CMN-P14634957 | metadata | Unreferenced in project code |
| $.dhash24 | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.dhash24[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 4d78f0e8f0e8f4fc | metadata | Unreferenced in project code |
| $.frame_indices | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.frame_indices[] | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 0 | metadata | Unreferenced in project code |

---
# DS-022 - Audio fingerprint features

- **Family / component / category:** ORVEX features / feature file / Derived feature (audio md5 + envelope)
- **Original publisher:** ORVEX project (generated)
- **Original source:** N/A (generated in this repository)
- **How it entered the project:** ORVEX scripts (see Processing History)
- **What was retained:** generated artefact
- **Provenance category:** 1 Verified from repository evidence (external source not re-checked online)
- **Location:** `data/derived/features/audio_fingerprint.jsonl` (JSONL); availability: Local files; state: derived/processed
- **Files / records / size:** 1 / 1727 / 216956 bytes (0.000 GB)
- **Usable / excluded:** media with audio / media without audio
- **Licence:** N/A (ORVEX-generated; inherits source licence)
- **Referenced by code:** scripts/datasets/audit.py:_@138; scripts/datasets/s5b_feature_hashes.py:<module>@9; scripts/datasets/s5_features_pairs_splits.py:<module>@85; scripts/datasets/s5_features_pairs_splits.py:<module>@101; scripts/datasets/s9_feature_baseline.py:<module>@14
- **Actually used (verified class):** Evaluation use verified (baseline)
- **Necessity:** Useful and justified - audio replacement evidence
- **Retention:** Retain
- **Limitations:** coarse; not an embedding

## How it is used in the problem statement and project
- **R-M2** (p5 Module 2 Media Processing): Extract frames/audio/text; OCR; visual/audio/text representations; store fingerprints
  - evidence it provides: 1,727 audio fingerprint records; fields/media used: media_id + feature values
  - consuming module: dataset pipeline script (no ORVEX application module exists in the repository); stage: feature extraction; algorithm: dHash / PCM md5 / RMS envelope
  - input: `local media`; code: yes: scripts/datasets/s5_features_pairs_splits.py:feat (lines 71-82)
  - output: feature jsonl/manifest; evaluation: K17 + baseline
  - status: **Partially implemented**; evidence: Demonstrated; limits: weak for crop/mirror; no learned embeddings

**Code touching this dataset (file : symbol : operation):** `scripts/datasets/audit.py:_` (reference, lines 138-138); `scripts/datasets/s5_features_pairs_splits.py:<module>` (write/produce, lines 85-101); `scripts/datasets/s5b_feature_hashes.py:<module>` (read/consume, lines 9-9); `scripts/datasets/s9_feature_baseline.py:<module>` (read/consume, lines 14-14)

## Columns / fields (4 across 1 file(s))

### `data/derived/features/audio_fingerprint.jsonl`  - 4 fields, 500 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| $ | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.media_id | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | RW-CMN-P14634957 | metadata | Unreferenced in project code |
| $.audio_md5_8k | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 840fdf0e1df3aaacd33452ae0cfeaee0 | metadata | Unreferenced in project code |
| $.audio_env_1s | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 00000ccbceeeeeeeeeeeeeeeeeeeeeeeecedceddeeeedccedc | metadata | Unreferenced in project code |

---
# DS-023 - Training pairs

- **Family / component / category:** ORVEX examples / table / Created table (labelled pairs)
- **Original publisher:** ORVEX project (generated)
- **Original source:** N/A (generated in this repository)
- **How it entered the project:** ORVEX scripts (see Processing History)
- **What was retained:** generated artefact
- **Provenance category:** 1 Verified from repository evidence (external source not re-checked online)
- **Location:** `data/derived/tables/training_pairs.csv` (CSV); availability: Local files; state: derived/processed
- **Files / records / size:** 1 / 13659 / 4719493 bytes (0.005 GB)
- **Usable / excluded:** 9928 in a split / 3731 excluded
- **Licence:** N/A (ORVEX-generated; inherits source licence)
- **Referenced by code:** scripts/datasets/audit.py:_@100; scripts/datasets/audit.py:_@115; scripts/datasets/audit.py:_@126; scripts/datasets/s5_features_pairs_splits.py:<module>@175; scripts/datasets/s6_docs.py:<module>@76; scripts/datasets/s6_docs.py:<module>@86 (+9 more)
- **Actually used (verified class):** Evaluation use verified (baseline)
- **Necessity:** Essential - evaluation/training pairs
- **Retention:** Retain
- **Limitations:** negatives are sampled (uncertain); 3731 excluded

## How it is used in the problem statement and project
- **R-M3** (p5-6 Module 3 Relationship Detection): Compare two videos; share a source; direct/indirect derivation; likely vs uncertain; confidence + evidence
  - evidence it provides: 9,928 usable labelled pairs; fields/media used: label_binary_related, relationship_class, split
  - consuming module: dataset pipeline script (no ORVEX application module exists in the repository); stage: baseline scoring; algorithm: non-learned dHash
  - input: `data/derived/tables/training_pairs.csv`; code: yes: scripts/datasets/s9_feature_baseline.py (module level)
  - output: DS-030; evaluation: ROC-AUC by split
  - status: **Partially implemented**; evidence: Demonstrated; limits: negatives are sampled (uncertain); no learned model
- **R-M9** (p7 Module 9 Evaluation): Precision/recall; false positives; graph/cluster quality; unseen transformations; time-to-detection; model versions
  - evidence it provides: pairs split by source family; fields/media used: split, includes_heldout_transform
  - consuming module: dataset pipeline script (no ORVEX application module exists in the repository); stage: evaluation; algorithm: split-v2
  - input: `DS-023 + DS-025`; code: yes: scripts/datasets/s5_features_pairs_splits.py:addpair (lines 125-129)
  - output: DS-030; evaluation: K13/K14
  - status: **Partially implemented**; evidence: Demonstrated (protocol); no model; limits: no confidence intervals

**Code touching this dataset (file : symbol : operation):** `scripts/datasets/audit.py:_` (read/consume, lines 100-126); `scripts/datasets/s5_features_pairs_splits.py:<module>` (write/produce, lines 175-175); `scripts/datasets/s6_docs.py:<module>` (read/consume, lines 76-137); `scripts/datasets/s8_necessity_audit.py:<module>` (read/consume, lines 17-17); `scripts/datasets/s9_feature_baseline.py:<module>` (read/consume, lines 20-20); `scripts/datasets/schema.py:<module>` (read/consume, lines 198-198); `scripts/datasets/update_report2.py:<module>` (reference, lines 12-12)

## Columns / fields (23 across 1 file(s))

### `data/derived/tables/training_pairs.csv`  - 23 fields, 13659 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| example_id | str | Id. | added by ORVEX | bookkeeping/administrative | 0.0 | 13659 | EX-0000001 | metadata | Referenced by audit/docs/tests only |
| media_a_id | str | A. | added by ORVEX | bookkeeping/administrative | 0.0 | 1645 | RW-CMN-P10491224 | metadata | Used by downstream code |
| media_b_id | str | B. | added by ORVEX | bookkeeping/administrative | 0.0 | 1635 | CV-P10491224-V01 | metadata | Used by downstream code |
| relationship_id | str | Edge backing the label (null for negatives). | added by ORVEX | bookkeeping/administrative | 91.72 | 1131 | REL-C-000001 | metadata | Used by downstream code |
| label_binary_related | int | 1 related / 0 not related. | added by ORVEX | derived by deterministic rule/inferred | 0.0 | 2 | 1 | ground truth (controlled lineage / source annotation) or sampling-rule proxy for negatives | Used by downstream code |
| relationship_class | str | direct_derivation / indirect_derivation / sibling_same_parent / same_family_other / edited_version / unrelated_distinct_source. | added by ORVEX | derived by deterministic rule/inferred | 0.0 | 7 | direct_derivation | ground truth (controlled lineage / source annotation) or sampling-rule proxy for negatives | Used by downstream code |
| native_label | str | Native label if from a source. | original source field | copied | 98.17 | 5 | splicing | source annotation (ground truth as published by dataset authors) | Used by downstream code |
| normalized_label | str | Normalized label. | added by ORVEX | derived by deterministic rule/inferred | 0.0 | 7 | direct_derivation | ground truth (controlled lineage / source annotation) or sampling-rule proxy for negatives | Referenced by audit/docs/tests only |
| label_origin | str | controlled_lineage / source_annotation / negative_sampling_rule. | added by ORVEX | bookkeeping/administrative | 0.0 | 3 | controlled_lineage | metadata | Referenced by audit/docs/tests only |
| label_status | str | Status. | added by ORVEX | bookkeeping/administrative | 0.0 | 3 | controlled_ground_truth | metadata | Used by downstream code |
| evidence_id | str | Evidence. | added by ORVEX | bookkeeping/administrative | 0.0 | 1133 | EV-CV-CV-P10491224-V01 | metadata | Used by downstream code |
| feature_refs | str | Feature ids. | added by ORVEX | bookkeeping/administrative | 0.0 | 1 | visual_dhash24/audio_fingerprint;visual_dhash24/au | metadata | Referenced by audit/docs/tests only |
| source_family_id | str | Family used for splitting (A's family). | added by ORVEX | derived by deterministic rule/inferred | 0.0 | 305 | RW-CMN-P10491224 | derived metadata/feature | Referenced by audit/docs/tests only |
| event_or_cascade_group_id | str | Group. | original source field | copied | 94.51 | 250 | 7e2p57 | metadata | Referenced by audit/docs/tests only |
| split | str | train/val/test/excluded. | added by ORVEX | derived by deterministic rule/inferred | 0.0 | 4 | train | derived metadata/feature | Used by downstream code |
| split_version | str | Version. | added by ORVEX | bookkeeping/administrative | 0.0 | 1 | split-v2 | metadata | Used by downstream code |
| sampling_method | str | How the pair was chosen. | added by ORVEX | bookkeeping/administrative | 0.0 | 2 | all within-family pairs | metadata | Referenced by audit/docs/tests only |
| negative_rationale | str | Why a negative is credible. | added by ORVEX | bookkeeping/administrative | 91.24 | 4 | distinct Commons uploads (different page ids) with | metadata | Referenced by audit/docs/tests only |
| hardness | str | easy/medium/hard. | added by ORVEX | derived by deterministic rule/inferred | 0.0 | 3 | easy | derived metadata/feature | Used by downstream code |
| leakage_flag | bool | True if pair crosses families/splits. | added by ORVEX | derived by deterministic rule/inferred | 0.0 | 1 | False | derived metadata/feature | Referenced by audit/docs/tests only |
| exclusion_reason | str | Reason excluded. | added by ORVEX | bookkeeping/administrative | 72.68 | 2 | held_out_transform_test_only_family_not_test | metadata | Referenced by audit/docs/tests only |
| includes_heldout_transform | bool | Involves a test-only transformation. | added by ORVEX | derived by deterministic rule/inferred | 0.0 | 2 | False | derived metadata/feature | Used by downstream code |
| created_utc | datetime | Time. | added by ORVEX | bookkeeping/administrative | 0.0 | 1 | 2026-10-26T18:06:44Z | metadata | Used by downstream code |

---
# DS-024 - Group examples (5-6 videos)

- **Family / component / category:** ORVEX examples / table / Created table
- **Original publisher:** ORVEX project (generated)
- **Original source:** N/A (generated in this repository)
- **How it entered the project:** ORVEX scripts (see Processing History)
- **What was retained:** generated artefact
- **Provenance category:** 1 Verified from repository evidence (external source not re-checked online)
- **Location:** `data/derived/tables/group_examples.csv` (CSV); availability: Local files; state: derived/processed
- **Files / records / size:** 1 / 110 / 37349 bytes (0.000 GB)
- **Usable / excluded:** all / 0
- **Licence:** N/A (ORVEX-generated; inherits source licence)
- **Referenced by code:** scripts/datasets/audit.py:_@173; scripts/datasets/s5_features_pairs_splits.py:<module>@194; scripts/datasets/s6_docs.py:<module>@86; scripts/datasets/s6_docs.py:<module>@88; scripts/datasets/s6_docs.py:<module>@95; scripts/datasets/s6_docs.py:<module>@122 (+1 more)
- **Actually used (verified class):** Test/audit use only (no experiment)
- **Necessity:** Underutilized - group data exists but no code consumes it
- **Retention:** Retain
- **Limitations:** no code reads this table except audit/tests

## How it is used in the problem statement and project
- **R-M3b** (p5 Module 3): Compare a group of 5-6 videos
  - evidence it provides: 110 groups of 6 with truth edges; fields/media used: member_media_ids, truth_edges
  - consuming module: none (only audit/tests read it); stage: none; algorithm: none
  - input: `data/derived/tables/group_examples.csv`; code: yes: scripts/datasets/s5_features_pairs_splits.py (module level)
  - output: none; evaluation: K25 only
  - status: **Planned (data exists; not consumed)**; evidence: Absent for experiments; limits: 69 groups have no truth edges

**Code touching this dataset (file : symbol : operation):** `scripts/datasets/audit.py:_` (read/consume, lines 173-173); `scripts/datasets/s5_features_pairs_splits.py:<module>` (write/produce, lines 194-194); `scripts/datasets/s6_docs.py:<module>` (reference, lines 86-122); `scripts/datasets/schema.py:<module>` (read/consume, lines 266-266)

## Columns / fields (13 across 1 file(s))

### `data/derived/tables/group_examples.csv`  - 13 fields, 110 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| group_id | str | Group id. | added by ORVEX | bookkeeping/administrative | 0.0 | 110 | GRP-00001 | metadata | Referenced by audit/docs/tests only |
| source_family_id | str | Family of the related members. | added by ORVEX | derived by deterministic rule/inferred | 0.0 | 55 | RW-CMN-P10491224 | derived metadata/feature | Referenced by audit/docs/tests only |
| member_media_ids | str | Pipe-separated members (related + distractors). | added by ORVEX | bookkeeping/administrative | 0.0 | 110 | CV-P10491224-V15/CV-P10491224-V06/CV-P10491224-V05 | metadata | Referenced by audit/docs/tests only |
| n_members | int | Number of members. | added by ORVEX | computed from media/files by a tool | 0.0 | 1 | 6 | derived metadata/feature | Referenced by audit/docs/tests only |
| family_member_ids | str | Related members. | added by ORVEX | bookkeeping/administrative | 0.0 | 110 | CV-P10491224-V15/CV-P10491224-V06/CV-P10491224-V05 | metadata | Referenced by audit/docs/tests only |
| distractor_ids | str | Unrelated members. | added by ORVEX | bookkeeping/administrative | 0.0 | 110 | CV-P150038214-V06/RW-CMN-P167507705 | metadata | Referenced by audit/docs/tests only |
| truth_edges | str | Nearest-selected-ancestor edges parent>child among family members. | added by ORVEX | derived by deterministic rule/inferred | 58.18 | 46 | RW-CMN-P105004791>CV-P105004791-V09;RW-CMN-P105004 | derived metadata/feature | Referenced by audit/docs/tests only |
| n_truth_edges | int | Number of edges. | added by ORVEX | computed from media/files by a tool | 0.0 | 4 | 0 | derived metadata/feature | Referenced by audit/docs/tests only |
| split | str | Split. | added by ORVEX | derived by deterministic rule/inferred | 0.0 | 3 | train | derived metadata/feature | Used by downstream code |
| split_version | str | Version. | added by ORVEX | bookkeeping/administrative | 0.0 | 1 | split-v2 | metadata | Used by downstream code |
| label_origin | str | controlled_lineage. | added by ORVEX | bookkeeping/administrative | 0.0 | 1 | controlled_lineage | metadata | Referenced by audit/docs/tests only |
| evidence_id | str | Evidence. | added by ORVEX | bookkeeping/administrative | 0.0 | 1 | EV-NEG-RULE | metadata | Used by downstream code |
| created_utc | datetime | Time. | added by ORVEX | bookkeeping/administrative | 0.0 | 1 | 2026-10-26T18:06:44Z | metadata | Used by downstream code |

---
# DS-025 - Split manifest (split-v2)

- **Family / component / category:** ORVEX splits / table / Created table
- **Original publisher:** ORVEX project (generated)
- **Original source:** N/A (generated in this repository)
- **How it entered the project:** ORVEX scripts (see Processing History)
- **What was retained:** generated artefact
- **Provenance category:** 1 Verified from repository evidence (external source not re-checked online)
- **Location:** `data/derived/splits/split_manifest.csv` (CSV); availability: Local files; state: derived/processed
- **Files / records / size:** 1 / 305 / 72085 bytes (0.000 GB)
- **Usable / excluded:** all families / 0
- **Licence:** N/A (ORVEX-generated; inherits source licence)
- **Referenced by code:** scripts/datasets/audit.py:_@100; scripts/datasets/s5_features_pairs_splits.py:<module>@112; scripts/datasets/s6_docs.py:<module>@86; scripts/datasets/s6_docs.py:<module>@95; scripts/datasets/s6_docs.py:<module>@127; scripts/datasets/s6_docs.py:<module>@129 (+8 more)
- **Actually used (verified class):** Preprocessing use verified (pairs/variants splits)
- **Necessity:** Essential - leakage control
- **Retention:** Retain
- **Limitations:** family-level only

## How it is used in the problem statement and project
- **R-M9** (p7 Module 9 Evaluation): Precision/recall; false positives; graph/cluster quality; unseen transformations; time-to-detection; model versions
  - evidence it provides: 305 families, split-v2; fields/media used: source_family_id, split
  - consuming module: dataset pipeline script (no ORVEX application module exists in the repository); stage: split assignment; algorithm: theme-grouped stride split
  - input: `data/derived/splits/split_manifest.csv`; code: yes: scripts/datasets/s5_features_pairs_splits.py:assign (lines 25-28)
  - output: DS-014/DS-023 split fields; evaluation: K13
  - status: **Implemented**; evidence: Demonstrated; limits: 7 Commons test families

**Code touching this dataset (file : symbol : operation):** `scripts/datasets/audit.py:_` (read/consume, lines 100-100); `scripts/datasets/s5_features_pairs_splits.py:<module>` (write/produce, lines 112-112); `scripts/datasets/s6_docs.py:<module>` (read/consume, lines 86-176); `scripts/datasets/s8_necessity_audit.py:<module>` (read/consume, lines 17-17); `scripts/datasets/schema.py:<module>` (read/consume, lines 130-271); `scripts/datasets/update_report2.py:<module>` (reference, lines 13-13)

## Columns / fields (10 across 1 file(s))

### `data/derived/splits/split_manifest.csv`  - 10 fields, 305 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| split_version | str | Version. | added by ORVEX | bookkeeping/administrative | 0.0 | 1 | split-v2 | metadata | Used by downstream code |
| source_family_id | str | Root source. | added by ORVEX | bookkeeping/administrative | 0.0 | 305 | RW-CMN-P10491224 | metadata | Referenced by audit/docs/tests only |
| source_dataset_id | str | Dataset. | added by ORVEX | bookkeeping/administrative | 0.0 | 2 | RW-01 | metadata | Used by downstream code |
| split | str | Assigned split. | added by ORVEX | derived by deterministic rule/inferred | 0.0 | 3 | train | derived metadata/feature | Used by downstream code |
| assignment_method | str | Rule. | added by ORVEX | bookkeeping/administrative | 0.0 | 1 | Commons: whole search themes assigned (sorted, str | metadata | Used by downstream code |
| seed | str | Seed. | added by ORVEX | bookkeeping/administrative | 0.0 | 1 | orvex-split-20261026 | metadata | Used by downstream code |
| domain_stratum | str | Stratum. | added by ORVEX | bookkeeping/administrative | 0.0 | 26 | education | metadata | Referenced by audit/docs/tests only |
| n_family_items | int | Items in family. | added by ORVEX | computed from media/files by a tool | 0.0 | 4 | 22 | derived metadata/feature | Referenced by audit/docs/tests only |
| n_native_edges | int | Native edges. | added by ORVEX | computed from media/files by a tool | 0.0 | 2 | 0 | derived metadata/feature | Referenced by audit/docs/tests only |
| heldout_transformations_in_family | str | Held-out transformations present. | added by ORVEX | derived by deterministic rule/inferred | 81.97 | 2 | audio_noise_mix/mirror_color_shift/reupload_sim/sp | derived metadata/feature | Referenced by audit/docs/tests only |

---
# DS-026 - Duplicate map

- **Family / component / category:** ORVEX QC / table / Created table
- **Original publisher:** ORVEX project (generated)
- **Original source:** N/A (generated in this repository)
- **How it entered the project:** ORVEX scripts (see Processing History)
- **What was retained:** generated artefact
- **Provenance category:** 1 Verified from repository evidence (external source not re-checked online)
- **Location:** `data/derived/tables/duplicate_map.csv` (CSV); availability: Local files; state: derived/processed
- **Files / records / size:** 1 / 378 / 78429 bytes (0.000 GB)
- **Usable / excluded:** all / 0
- **Licence:** N/A (ORVEX-generated; inherits source licence)
- **Referenced by code:** scripts/datasets/audit.py:_@149; scripts/datasets/candidates.py:<module>@39; scripts/datasets/patch_round3.py:<module>@99; scripts/datasets/s3_normalize.py:<module>@303; scripts/datasets/s5_features_pairs_splits.py:<module>@173; scripts/datasets/s6_docs.py:<module>@87 (+7 more)
- **Actually used (verified class):** Test/audit use only downstream of s3
- **Necessity:** Useful and justified - duplicate handling
- **Retention:** Retain
- **Limitations:** perceptual matches are review candidates

## How it is used in the problem statement and project
- **R-M1** (p5 Module 1 Dataset Creation): Import source videos; identify duplicates; unique IDs; generate variants; record transformation + parent; save relationships
  - evidence it provides: 378 duplicate mappings; fields/media used: duplicate_type, canonical_media_id
  - consuming module: dataset pipeline script (no ORVEX application module exists in the repository); stage: dedupe; algorithm: SHA-256 + dHash + URL
  - input: `data/derived/tables/duplicate_map.csv`; code: yes: scripts/datasets/s3_normalize.py:qc_commons (lines 55-114)
  - output: usable_for_variants flag; evaluation: K19
  - status: **Implemented**; evidence: Demonstrated; limits: perceptual matches are review candidates

**Code touching this dataset (file : symbol : operation):** `scripts/datasets/audit.py:_` (read/consume, lines 149-149); `scripts/datasets/candidates.py:<module>` (reference, lines 39-39); `scripts/datasets/patch_round3.py:<module>` (read/consume, lines 99-99); `scripts/datasets/s3_normalize.py:<module>` (write/produce, lines 303-303); `scripts/datasets/s5_features_pairs_splits.py:<module>` (reference, lines 173-173); `scripts/datasets/s6_docs.py:<module>` (read/consume, lines 87-184); `scripts/datasets/schema.py:<module>` (read/consume, lines 97-259)

## Columns / fields (6 across 1 file(s))

### `data/derived/tables/duplicate_map.csv`  - 6 fields, 378 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| duplicate_id | str | Id. | added by ORVEX | bookkeeping/administrative | 0.0 | 378 | DUP-00001 | metadata | Referenced by audit/docs/tests only |
| canonical_media_id | str | Kept record. | added by ORVEX | bookkeeping/administrative | 0.0 | 313 | RW-CMN-P128562512 | metadata | Used by downstream code |
| duplicate_media_id | str | Duplicate record. | added by ORVEX | bookkeeping/administrative | 0.0 | 378 | RW-CMN-P191996630 | metadata | Used by downstream code |
| duplicate_type | str | exact_hash / near_duplicate_perceptual / same_url_across_versions / same_platform_id_across_sources. | added by ORVEX | derived by deterministic rule/inferred | 0.0 | 4 | near_duplicate_perceptual | derived metadata/feature | Used by downstream code |
| evidence | str | Evidence. | added by ORVEX | computed from media/files by a tool | 0.0 | 312 | dHash24 frame match 0.58 (threshold 0.45) | derived metadata/feature | Used by downstream code |
| resolution | str | What was done. | added by ORVEX | bookkeeping/administrative | 0.0 | 4 | excluded_from_variants_original_file_kept | metadata | Referenced by audit/docs/tests only |

---
# DS-027 - Source registry

- **Family / component / category:** ORVEX registry / table / Created table (dataset census)
- **Original publisher:** ORVEX project (generated)
- **Original source:** N/A (generated in this repository)
- **How it entered the project:** ORVEX scripts (see Processing History)
- **What was retained:** generated artefact
- **Provenance category:** 1 Verified from repository evidence (external source not re-checked online)
- **Location:** `data/manifests/source_registry.csv` (CSV); availability: Local files; state: n/a
- **Files / records / size:** 1 / 31 / 23226 bytes (0.000 GB)
- **Usable / excluded:** all / 0
- **Licence:** N/A (ORVEX-generated; inherits source licence)
- **Referenced by code:** scripts/datasets/audit.py:_@169; scripts/datasets/audit.py:_@203; scripts/datasets/patch_round3.py:<module>@37; scripts/datasets/patch_round3.py:<module>@87; scripts/datasets/s3_normalize.py:<module>@304; scripts/datasets/s6_docs.py:<module>@53 (+12 more)
- **Actually used (verified class):** Test/audit use only downstream of s3
- **Necessity:** Useful and justified - census and decisions
- **Retention:** Retain
- **Limitations:** licence/access fields come from snapshots; 15 entries unverified leads

## How it is used in the problem statement and project
- **R-RM** (p12 §10.2-10.4): Source collection with licences; cleaning/labelling; data and evidence rules
  - evidence it provides: 31 candidates with licence/access verdicts; fields/media used: inclusion_status, license_terms
  - consuming module: dataset pipeline script (no ORVEX application module exists in the repository); stage: census; algorithm: none
  - input: `data/manifests/source_registry.csv`; code: yes: scripts/datasets/s3_normalize.py:build_registry (lines 270-280)
  - output: DS-027; evaluation: K24
  - status: **Implemented**; evidence: Demonstrated; limits: 15 unverified leads

**Code touching this dataset (file : symbol : operation):** `scripts/datasets/audit.py:_` (read/consume, lines 169-203); `scripts/datasets/patch_round3.py:<module>` (reference, lines 37-87); `scripts/datasets/s3_normalize.py:<module>` (write/produce, lines 304-304); `scripts/datasets/s6_docs.py:<module>` (read/consume, lines 53-136); `scripts/datasets/s8_necessity_audit.py:<module>` (read/consume, lines 18-18); `scripts/datasets/schema.py:<module>` (read/consume, lines 23-175)

## Columns / fields (30 across 1 file(s))

### `data/manifests/source_registry.csv`  - 30 fields, 31 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| source_dataset_id | str | Stable ORVEX id of the real-world source dataset. | added by ORVEX | bookkeeping/administrative | 0.0 | 31 | RW-01 | metadata | Used by downstream code |
| title | str | Full title. | original source field | copied | 0.0 | 31 | Wikimedia Commons CC/PD video pool (ORVEX selectio | metadata | Used by downstream code |
| creator | str | Creators/authors. | original source field | copied | 0.0 | 30 | Wikimedia Commons contributors (per-file author) | metadata | Used by downstream code |
| release_version | str | Release or version label. | original source field | copied | 0.0 | 28 | API snapshot 2026-10-26 | metadata | Used by downstream code |
| official_url | str | Official landing URL. | original source field | copied | 3.23 | 30 | https://commons.wikimedia.org/wiki/Commons:Reusing | metadata | Used by downstream code |
| download_url | str | Where files come from. | original source field | copied | 67.74 | 10 | https://commons.wikimedia.org/w/api.php | metadata | Used by downstream code |
| paper_doi_or_url | str | Associated paper. | original source field | copied | 25.81 | 23 | https://arxiv.org/abs/2303.13193 | metadata | Used by downstream code |
| accessed_date | datetime | Date the page/API was accessed. | added by ORVEX | bookkeeping/administrative | 0.0 | 1 | 2026-10-26 | metadata | Referenced by audit/docs/tests only |
| license_terms | str | Licence/terms exactly as stated (or 'not stated'). | original source field | copied | 0.0 | 19 | Per file (machine-readable): CC0 / Public domain / | metadata | Used by downstream code |
| license_evidence_url | str | Evidence link. | original source field | copied | 48.39 | 16 | Commons API extmetadata LicenseShortName per file | metadata | Used by downstream code |
| bytes_or_urls_provided | str | media_bytes / metadata_urls_only / mixed / unverified. | original source field | copied | 0.0 | 7 | media_bytes | metadata | Used by downstream code |
| derivative_use_status | str | permitted / not_stated / not_permitted / unverified. | added by ORVEX | derived by deterministic rule/inferred | 0.0 | 10 | permitted_per_file_licence | derived metadata/feature | Used by downstream code |
| training_use_status | str | permitted / not_stated / unverified. | added by ORVEX | derived by deterministic rule/inferred | 0.0 | 10 | permitted_per_file_licence | derived metadata/feature | Used by downstream code |
| redistribution_status | str | Whether files may be redistributed (with conditions). | added by ORVEX | derived by deterministic rule/inferred | 0.0 | 11 | permitted_with_attribution_and_sharealike_where_ap | derived metadata/feature | Used by downstream code |
| real_world_eligibility | str | Eligible / not eligible for the strict real-world collection and why. | added by ORVEX | analyst/human decision | 0.0 | 31 | Eligible: real user-uploaded recordings; selection | derived metadata/feature | Used by downstream code |
| native_task | str | Task the source was built for. | original source field | copied | 3.23 | 24 | General media repository (no task) | source annotation (ground truth as published by dataset authors) | Used by downstream code |
| native_labels | str | Native labels/annotations. | original source field | copied | 22.58 | 19 | categories, description, licence | source annotation (ground truth as published by dataset authors) | Used by downstream code |
| media_origin_characterization | str | How the media came to exist (user-uploaded, circulated, professionally edited...). | added by ORVEX | analyst/human decision | 0.0 | 28 | User-uploaded real-world video (speeches, street,  | derived metadata/feature | Used by downstream code |
| release_size_bytes | int | Total official release size when known. | original source field | copied | 70.97 | 9 | 55000000000 | metadata | Used by downstream code |
| planned_download_bytes | int | Budgeted bytes. | added by ORVEX | bookkeeping/administrative | 0.0 | 8 | 3000000000 | metadata | Referenced by audit/docs/tests only |
| actual_local_bytes | int | Measured local bytes. | added by ORVEX | computed from media/files by a tool | 0.0 | 9 | 1687283416 | derived metadata/feature | Referenced by audit/docs/tests only |
| record_count_local | int | Records held locally. | added by ORVEX | computed from media/files by a tool | 0.0 | 9 | 96 | derived metadata/feature | Referenced by audit/docs/tests only |
| auth_required | str | none / account / agreement / API. | original source field | copied | 0.0 | 8 | none | metadata | Used by downstream code |
| overlap_with | str | Other sources it overlaps. | added by ORVEX | analyst/human decision | 64.52 | 11 | VideoSham (subset) | derived metadata/feature | Used by downstream code |
| inclusion_status | str | Decision. | added by ORVEX | bookkeeping/administrative | 0.0 | 8 | included_selected_subset | metadata | Used by downstream code |
| inclusion_reason | str | Why. | added by ORVEX | analyst/human decision | 0.0 | 31 | Only surveyed source with real media bytes whose p | derived metadata/feature | Used by downstream code |
| tasks_supported | str | ORVEX modules/tasks supported. | added by ORVEX | bookkeeping/administrative | 41.94 | 17 | Phase1: controlled variants, relationship ground t | metadata | Used by downstream code |
| evidence_links | str | Pipe-separated URLs. | added by ORVEX | bookkeeping/administrative | 0.0 | 31 | https://commons.wikimedia.org/wiki/Commons:Reusing | metadata | Used by downstream code |
| limitations | str | Known limitations. | added by ORVEX | analyst/human decision | 70.97 | 9 | Not a benchmark; no native relationship labels; th | derived metadata/feature | Used by downstream code |
| verification_level | str | verified_official_page / verified_api / research_lead_unverified. | added by ORVEX | bookkeeping/administrative | 0.0 | 3 | verified_api | metadata | Used by downstream code |

---
# DS-028 - Download/access attempt log

- **Family / component / category:** ORVEX registry / table / Created table (access log)
- **Original publisher:** ORVEX project (generated)
- **Original source:** N/A (generated in this repository)
- **How it entered the project:** ORVEX scripts (see Processing History)
- **What was retained:** generated artefact
- **Provenance category:** 1 Verified from repository evidence (external source not re-checked online)
- **Location:** `data/manifests/download_access_attempt_log.csv` (CSV); availability: Local files; state: n/a
- **Files / records / size:** 1 / 729 / 215252 bytes (0.000 GB)
- **Usable / excluded:** all / 0
- **Licence:** N/A (ORVEX-generated; inherits source licence)
- **Referenced by code:** scripts/datasets/audit.py:_@162; scripts/datasets/audit.py:_@203; scripts/datasets/common.py:AccessLog@76; scripts/datasets/common.py:AccessLog@77; scripts/datasets/common.py:http_get@97; scripts/datasets/common.py:http_get@100 (+10 more)
- **Actually used (verified class):** Preprocessing use verified (writer) / Test-audit use
- **Necessity:** Useful and justified - access audit trail
- **Retention:** Retain
- **Limitations:** pre-existing interactive downloads logged as such

## How it is used in the problem statement and project
- No requirement mapping (non-dataset asset or no verified role): intended module = R-M6

**Code touching this dataset (file : symbol : operation):** `scripts/datasets/audit.py:_` (read/consume, lines 162-203); `scripts/datasets/common.py:AccessLog` (reference, lines 76-77); `scripts/datasets/common.py:http_get` (write/produce, lines 97-104); `scripts/datasets/patch_round3.py:<module>` (reference, lines 37-37); `scripts/datasets/s2_collect_media.py:dl` (write/produce, lines 78-78); `scripts/datasets/s2_collect_media.py:search` (write/produce, lines 28-28); `scripts/datasets/s5_features_pairs_splits.py:<module>` (read+write, lines 198-219); `scripts/datasets/s6_docs.py:<module>` (reference, lines 87-125); `scripts/datasets/schema.py:<module>` (read/consume, lines 234-234)

## Columns / fields (14 across 1 file(s))

### `data/manifests/download_access_attempt_log.csv`  - 14 fields, 729 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| attempt_id | str | Id. | added by ORVEX | bookkeeping/administrative | 0.0 | 729 | ACC-000001 | metadata | Used by downstream code |
| source_dataset_id | str | Source. | added by ORVEX | bookkeeping/administrative | 0.0 | 8 | RW-01 | metadata | Used by downstream code |
| media_or_file_id | str | Item. | added by ORVEX | bookkeeping/administrative | 0.0 | 729 | search:speech:0 | metadata | Used by downstream code |
| url | str | URL (blank for policy-skipped rows). | added by ORVEX | bookkeeping/administrative | 0.41 | 726 | https://commons.wikimedia.org/w/api.php?action=que | metadata | Used by downstream code |
| attempt_time_utc | datetime | Time. | added by ORVEX | bookkeeping/administrative | 0.0 | 587 | 2026-10-26T06:13:43Z | metadata | Used by downstream code |
| method | str | http_get / api. | added by ORVEX | bookkeeping/administrative | 0.0 | 3 | api | metadata | Used by downstream code |
| http_status | int | HTTP status. | added by ORVEX | computed from media/files by a tool | 0.55 | 2 | 200 | derived metadata/feature | Used by downstream code |
| result_category | str | ok / failed / skipped_terms / skipped_budget. | added by ORVEX | bookkeeping/administrative | 0.0 | 3 | ok | metadata | Used by downstream code |
| terms_decision | str | Decision. | added by ORVEX | bookkeeping/administrative | 0.0 | 7 | permitted_by_licence_or_open_access | metadata | Used by downstream code |
| retry_count | int | Retries. | added by ORVEX | bookkeeping/administrative | 0.0 | 1 | 0 | metadata | Used by downstream code |
| bytes | int | Bytes. | added by ORVEX | computed from media/files by a tool | 0.27 | 713 | 120502 | derived metadata/feature | Used by downstream code |
| sha256 | str | Hash. | added by ORVEX | computed from media/files by a tool | 4.39 | 697 | fee8a7d2305afb50e143175aa5baab8f6733ae21a7ef705051 | derived metadata/feature | Used by downstream code |
| final_status | str | Final status. | added by ORVEX | bookkeeping/administrative | 0.0 | 4 | downloaded_authorized | metadata | Used by downstream code |
| note | str | Note. | added by ORVEX | bookkeeping/administrative | 97.67 | 5 | downloaded during Gate 1 (interactive request); md | metadata | Used by downstream code |

---
# DS-029 - Campaign candidate clusters

- **Family / component / category:** ORVEX campaign / table (header only) / Created table (empty by design)
- **Original publisher:** ORVEX project (generated)
- **Original source:** N/A (generated in this repository)
- **How it entered the project:** ORVEX scripts (see Processing History)
- **What was retained:** generated artefact
- **Provenance category:** 1 Verified from repository evidence (external source not re-checked online)
- **Location:** `data/derived/tables/campaign_candidate_clusters.csv` (CSV); availability: Local file, 0 records; state: n/a
- **Files / records / size:** 1 / 0 / 219 bytes (0.000 GB)
- **Usable / excluded:** 0 / N/A
- **Licence:** N/A (ORVEX-generated; inherits source licence)
- **Referenced by code:** scripts/datasets/audit.py:_@153; scripts/datasets/s5_features_pairs_splits.py:<module>@197; scripts/datasets/s6_docs.py:<module>@87; scripts/datasets/s6_docs.py:<module>@96; scripts/datasets/s6_docs.py:<module>@126; scripts/datasets/s8_necessity_audit.py:<module>@79 (+1 more)
- **Actually used (verified class):** Test/audit use only (empty)
- **Necessity:** Required but unavailable - Module 7 evidence cannot be obtained from current data
- **Retention:** Keep empty
- **Limitations:** no authorised account+time evidence

## How it is used in the problem statement and project
- **R-M7** (p6 Module 7 Campaign Detection): Cluster posts; posting times/accounts; coordination signals separate from similarity
  - evidence it provides: empty table; fields/media used: all
  - consuming module: none; stage: none; algorithm: none
  - input: `data/derived/tables/campaign_candidate_clusters.csv`; code: yes: scripts/datasets/s5_features_pairs_splits.py (module level)
  - output: none; evaluation: K20
  - status: **Blocked**; evidence: Absent; limits: no authorised account+time evidence

**Code touching this dataset (file : symbol : operation):** `scripts/datasets/audit.py:_` (read/consume, lines 153-153); `scripts/datasets/s5_features_pairs_splits.py:<module>` (write/produce, lines 197-197); `scripts/datasets/s6_docs.py:<module>` (reference, lines 87-126); `scripts/datasets/s8_necessity_audit.py:<module>` (reference, lines 79-79); `scripts/datasets/schema.py:<module>` (read/consume, lines 214-214)

## Columns / fields (12 across 1 file(s))

### `data/derived/tables/campaign_candidate_clusters.csv`  - 12 fields, 0 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| cluster_id | empty | Id. | added by ORVEX | bookkeeping/administrative | 0.0 | 0 |  | metadata | Referenced by audit/docs/tests only |
| observation_ids | empty | Observations. | added by ORVEX | bookkeeping/administrative | 0.0 | 0 |  | metadata | Referenced by audit/docs/tests only |
| media_ids | empty | Media. | added by ORVEX | bookkeeping/administrative | 0.0 | 0 |  | metadata | Referenced by audit/docs/tests only |
| account_pseudonyms | empty | Accounts. | added by ORVEX | derived by deterministic rule/inferred | 0.0 | 0 |  | derived metadata/feature | Referenced by audit/docs/tests only |
| time_window_start_utc | empty | Start. | added by ORVEX | bookkeeping/administrative | 0.0 | 0 |  | metadata | Referenced by audit/docs/tests only |
| time_window_end_utc | empty | End. | added by ORVEX | bookkeeping/administrative | 0.0 | 0 |  | metadata | Referenced by audit/docs/tests only |
| common_media_signals | empty | Media signals. | added by ORVEX | bookkeeping/administrative | 0.0 | 0 |  | metadata | Referenced by audit/docs/tests only |
| posting_pattern_signals | empty | Posting signals. | added by ORVEX | bookkeeping/administrative | 0.0 | 0 |  | metadata | Referenced by audit/docs/tests only |
| independent_coordination_evidence | empty | Independent evidence. | added by ORVEX | bookkeeping/administrative | 0.0 | 0 |  | metadata | Referenced by audit/docs/tests only |
| candidate_status | empty | candidate_cluster / not_assessed. | added by ORVEX | bookkeeping/administrative | 0.0 | 0 |  | metadata | Referenced by audit/docs/tests only |
| reviewer | empty | Reviewer. | added by ORVEX | analyst/human decision | 0.0 | 0 |  | derived metadata/feature | Referenced by audit/docs/tests only |
| limitations | empty | Limitations. | added by ORVEX | bookkeeping/administrative | 0.0 | 0 |  | metadata | Used by downstream code |

---
# DS-030 - Experiment registry

- **Family / component / category:** ORVEX experiments / table / Created table (experiment results)
- **Original publisher:** ORVEX project (generated)
- **Original source:** N/A (generated in this repository)
- **How it entered the project:** ORVEX scripts (see Processing History)
- **What was retained:** generated artefact
- **Provenance category:** 1 Verified from repository evidence (external source not re-checked online)
- **Location:** `data/derived/tables/experiment_registry.csv` (CSV); availability: Local files; state: derived/processed
- **Files / records / size:** 1 / 8 / 3979 bytes (0.000 GB)
- **Usable / excluded:** 8 metric rows / 0
- **Licence:** N/A (ORVEX-generated; inherits source licence)
- **Referenced by code:** scripts/datasets/patch_round3.py:<module>@90; scripts/datasets/patch_round5.py:<module>@31; scripts/datasets/patch_round5.py:<module>@32; scripts/datasets/patch_round5.py:<module>@33; scripts/datasets/patch_round5.py:<module>@34; scripts/datasets/s5_features_pairs_splits.py:<module>@197 (+9 more)
- **Actually used (verified class):** Evaluation use verified (written by s9)
- **Necessity:** Useful and justified - experiment results registry
- **Retention:** Retain
- **Limitations:** only a non-learned baseline; no ORVEX model

## How it is used in the problem statement and project
- **R-M9** (p7 Module 9 Evaluation): Precision/recall; false positives; graph/cluster quality; unseen transformations; time-to-detection; model versions
  - evidence it provides: 8 baseline metric rows; fields/media used: metric_name, metric_value
  - consuming module: dataset pipeline script (no ORVEX application module exists in the repository); stage: experiment registry; algorithm: non-learned baseline
  - input: `data/derived/tables/experiment_registry.csv`; code: yes: scripts/datasets/s9_feature_baseline.py (module level)
  - output: DS-030; evaluation: ROC-AUC, MAE, latency
  - status: **Partially implemented**; evidence: Demonstrated (baseline only); limits: no ORVEX model; latency != time-to-detection

**Code touching this dataset (file : symbol : operation):** `scripts/datasets/patch_round3.py:<module>` (reference, lines 90-90); `scripts/datasets/patch_round5.py:<module>` (reference, lines 31-34); `scripts/datasets/s5_features_pairs_splits.py:<module>` (write/produce, lines 197-197); `scripts/datasets/s6_docs.py:<module>` (reference, lines 87-151); `scripts/datasets/s7_manifests.py:<module>` (reference, lines 49-49); `scripts/datasets/s8_necessity_audit.py:<module>` (reference, lines 115-115); `scripts/datasets/s9_feature_baseline.py:<module>` (write/produce, lines 49-49); `scripts/datasets/schema.py:<module>` (read/consume, lines 251-251); `scripts/datasets/update_report2.py:<module>` (reference, lines 14-14)

## Columns / fields (12 across 1 file(s))

### `data/derived/tables/experiment_registry.csv`  - 12 fields, 8 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| experiment_id | str | Id. | added by ORVEX | bookkeeping/administrative | 0.0 | 8 | BASE-DHASH-v1-01 | computed metric (non-learned baseline) | Referenced by audit/docs/tests only |
| dataset_versions | str | Dataset versions. | added by ORVEX | bookkeeping/administrative | 0.0 | 1 | tables snapshot of 2026-10-26 (see checksums.sha25 | computed metric (non-learned baseline) | Referenced by audit/docs/tests only |
| split_version | str | Split. | added by ORVEX | bookkeeping/administrative | 0.0 | 1 | split-v1 | computed metric (non-learned baseline) | Used by downstream code |
| label_map_version | str | Label map. | added by ORVEX | bookkeeping/administrative | 0.0 | 1 | labelmap-v1 | computed metric (non-learned baseline) | Referenced by audit/docs/tests only |
| model_version | str | Model. | added by ORVEX | bookkeeping/administrative | 0.0 | 1 | none: non-learned baseline, threshold fixed a prio | computed metric (non-learned baseline) | Referenced by audit/docs/tests only |
| feature_version | str | Feature set. | added by ORVEX | bookkeeping/administrative | 0.0 | 1 | dhash24-frame-match v1 (non-learned) | computed metric (non-learned baseline) | Referenced by audit/docs/tests only |
| metric_name | str | Metric. | added by ORVEX | bookkeeping/administrative | 0.0 | 8 | roc_auc_related_vs_unrelated_train | computed metric (non-learned baseline) | Referenced by audit/docs/tests only |
| metric_value | float | Value. | added by ORVEX | bookkeeping/administrative | 0.0 | 7 | 0.8734 | computed metric (non-learned baseline) | Referenced by audit/docs/tests only |
| protocol | str | Protocol. | added by ORVEX | bookkeeping/administrative | 0.0 | 8 | all labelled pairs in train split, score = max dir | computed metric (non-learned baseline) | Referenced by audit/docs/tests only |
| heldout_policy | str | Held-out policy. | added by ORVEX | bookkeeping/administrative | 0.0 | 1 | T11-T14 lineage test-only; reported separately | computed metric (non-learned baseline) | Referenced by audit/docs/tests only |
| report_path | str | Report. | added by ORVEX | bookkeeping/administrative | 0.0 | 1 | docs/datasets/necessity_audit/dhash_baseline_resul | computed metric (non-learned baseline) | Referenced by audit/docs/tests only |
| leakage_test_result | str | Leakage result. | added by ORVEX | bookkeeping/administrative | 0.0 | 1 | K13/K14 pass in the same audit run | computed metric (non-learned baseline) | Referenced by audit/docs/tests only |

---
# DS-031 - Manifests (checksums, crosswalk, attribution, selection plan, storage budget, protocol)

- **Family / component / category:** ORVEX manifests / manifests / Created manifests
- **Original publisher:** ORVEX project (generated)
- **Original source:** N/A (generated in this repository)
- **How it entered the project:** ORVEX scripts (see Processing History)
- **What was retained:** generated artefact
- **Provenance category:** 1 Verified from repository evidence (external source not re-checked online)
- **Location:** `data/manifests` (CSV/JSON/MD/sha256); availability: Local files; state: derived/processed
- **Files / records / size:** 6 / 6 / 41965067 bytes (0.042 GB)
- **Usable / excluded:** all / 0
- **Licence:** N/A (ORVEX-generated; inherits source licence)
- **Referenced by code:** scripts/datasets/audit.py:_@197; scripts/datasets/audit.py:_@203; scripts/datasets/audit.py:_@206; scripts/datasets/audit.py:_@211; scripts/datasets/patch_round3.py:<module>@31; scripts/datasets/patch_round3.py:<module>@37 (+15 more)
- **Actually used (verified class):** Test/audit use
- **Necessity:** Useful and justified - checksums/attribution/protocol
- **Retention:** Retain
- **Limitations:** run logs excluded from checksums by design

## How it is used in the problem statement and project
- No requirement mapping (non-dataset asset or no verified role): intended module = R-RM

**Code touching this dataset (file : symbol : operation):** `scripts/datasets/audit.py:_` (read/consume, lines 197-211); `scripts/datasets/patch_round3.py:<module>` (read/consume, lines 31-125); `scripts/datasets/patch_round4.py:<module>` (reference, lines 25-25); `scripts/datasets/patch_round6.py:<module>` (reference, lines 18-18); `scripts/datasets/s6_docs.py:<module>` (reference, lines 111-111); `scripts/datasets/s7_manifests.py:<module>` (read+write, lines 13-95); `scripts/datasets/s8_necessity_audit.py:<module>` (read+write, lines 97-102); `scripts/datasets/s9_feature_baseline.py:row` (reference, lines 43-43); `scripts/datasets/update_report.py:<module>` (reference, lines 17-24)

## Columns / fields (61 across 5 file(s))

### `data/manifests/attribution.csv`  - 9 fields, 96 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| media_id | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 96 | RW-CMN-P14634957 | metadata (unverified meaning) | Used by downstream code |
| title | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 96 | File:Ante Pavelić Speech 21051941.ogv | metadata (unverified meaning) | Used by downstream code |
| author_or_credit | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 86 | [masked] | metadata (unverified meaning) | Used by downstream code |
| license | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 9 | Public domain | metadata (unverified meaning) | Used by downstream code |
| license_url | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 9 | n/a (public domain: Commons provides no licence te | metadata (unverified meaning) | Used by downstream code |
| file_page_url | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 96 | https://commons.wikimedia.org/wiki/File:Ante_Pavel | metadata (unverified meaning) | Used by downstream code |
| attribution_required | bool | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 2 | false | metadata (unverified meaning) | Used by downstream code |
| used_as_variant_source | bool | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 2 | False | metadata (unverified meaning) | Used by downstream code |
| retrieved | datetime | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 1 | 2026-10-26T15:02:46Z | metadata (unverified meaning) | Used by downstream code |

### `data/manifests/checksums.sha256`  - 1 fields, 1883 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| checksums.sha256 | str | one value per line | see file | see file | 0 | 1883 | bd225d2603b3aace534c4713854c25c24e8aad859b21eda3fb14947ff76751bf  data | metadata | Used by downstream code |

### `data/manifests/native_id_crosswalk.csv`  - 9 fields, 252270 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| source_dataset_id | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 8 | RW-01 | metadata (unverified meaning) | Used by downstream code |
| release_version | int | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 1.24 | 6 | 2018 | metadata (unverified meaning) | Used by downstream code |
| native_record_id | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 244997 | 14634957 | metadata (unverified meaning) | Used by downstream code |
| native_media_id | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 252001 | File:Ante Pavelić Speech 21051941.ogv | metadata (unverified meaning) | Used by downstream code |
| platform | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 7 | wikimedia_commons | metadata (unverified meaning) | Used by downstream code |
| platform_media_id | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 250856 | 14634957 | metadata (unverified meaning) | Used by downstream code |
| source_url | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 251879 | https://commons.wikimedia.org/wiki/File:Ante_Pavel | metadata (unverified meaning) | Used by downstream code |
| canonical_url | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 251879 | https://commons.wikimedia.org/wiki/File:Ante_Pavel | metadata (unverified meaning) | Used by downstream code |
| media_id | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 252270 | RW-CMN-P14634957 | metadata (unverified meaning) | Used by downstream code |

### `data/manifests/selection_plan.json`  - 34 fields, 1 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| $ | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.generated | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 2026-10-26T18:47:37Z | metadata | Unreferenced in project code |
| $.search_date | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 2026-10-26 | metadata | Unreferenced in project code |
| $.search_terms | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.search_terms[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | VCSL dataset ... download license | metadata | Unreferenced in project code |
| $.candidates_considered | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 31 | metadata | Unreferenced in project code |
| $.commons | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.commons.queries | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.commons.queries[] | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.commons.queries[][] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | speech | metadata | Unreferenced in project code |
| $.commons.per_query_max_new_files | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 4 | metadata | Unreferenced in project code |
| $.commons.file_size_bytes | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.commons.file_size_bytes[] | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 300000 | metadata | Unreferenced in project code |
| $.commons.licence_gate | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | CC0 / Public domain / CC BY / CC BY-SA (NC/ND/unkn | metadata | Unreferenced in project code |
| $.commons.stem_dedupe | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | first 18 letters of normalised title | metadata | Unreferenced in project code |
| $.commons.qc | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | duration 8-120 s, height >=240, no decode errors,  | metadata | Unreferenced in project code |
| $.anakin | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.anakin.rule | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | sort by sha256('orvex-anakin-v1'+video-id); first  | metadata | Unreferenced in project code |
| $.anakin.selected_pairs | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 250 | metadata | Unreferenced in project code |
| $.variants | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.variants.transformations | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | T01-T14 | metadata | Unreferenced in project code |
| $.variants.chains | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | C1-C5 | metadata | Unreferenced in project code |
| $.variants.donor_and_caption_pick | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | sha256 of root media id over eligible pool (other- | metadata | Unreferenced in project code |
| $.variants.test_only_types | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.variants.test_only_types[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | T11 | metadata | Unreferenced in project code |
| $.splits | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.splits.unit | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | source family; Commons families grouped by search  | metadata | Unreferenced in project code |
| $.splits.pattern | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 14 train / 3 val / 3 test per 20 themes (Commons)  | metadata | Unreferenced in project code |
| $.splits.seed | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | orvex-split-20261026 | metadata | Unreferenced in project code |
| $.splits.version | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | split-v2 | metadata | Unreferenced in project code |
| $.negatives | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.negatives.easy | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | different search theme | metadata | Unreferenced in project code |
| $.negatives.hard | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | same search theme (label uncertain) | metadata | Unreferenced in project code |
| $.negatives.within | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | same split only | metadata | Unreferenced in project code |

### `data/manifests/storage_budget.csv`  - 8 fields, 19 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| kind | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 4 | final_category | metadata (unverified meaning) | Used by downstream code |
| name | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 19 | real-world raw metadata | metadata (unverified meaning) | Used by downstream code |
| bytes | int | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 18 | 66260147 | metadata (unverified meaning) | Used by downstream code |
| GB_decimal | float | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 17 | 0.066 | metadata (unverified meaning) | Used by downstream code |
| GiB | float | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 17 | 0.062 | metadata (unverified meaning) | Used by downstream code |
| allocation_bytes | int | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 42.11 | 6 | 400000000 | metadata (unverified meaning) | Used by downstream code |
| within_allocation | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 1 | yes | metadata (unverified meaning) | Used by downstream code |
| source | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 7 | measured by du-equivalent walk | metadata (unverified meaning) | Used by downstream code |

---
# DS-032 - Build intermediates and run logs

- **Family / component / category:** ORVEX pipeline internals / intermediate files / Processing artefacts
- **Original publisher:** ORVEX project (generated)
- **Original source:** N/A (generated in this repository)
- **How it entered the project:** ORVEX scripts (see Processing History)
- **What was retained:** generated artefact
- **Provenance category:** 1 Verified from repository evidence (external source not re-checked online)
- **Location:** `data/manifests` (JSON/WAV/LOG/TXT); availability: Local files; state: derived/processed
- **Files / records / size:** 72 / 72 / 3706024 bytes (0.004 GB)
- **Usable / excluded:** n/a / n/a
- **Licence:** N/A (ORVEX-generated; inherits source licence)
- **Referenced by code:** scripts/datasets/audit.py:_@210; scripts/datasets/common.py:<module>@12; scripts/datasets/common.py:AccessLog@78; scripts/datasets/common.py:add@81; scripts/datasets/patch_round4.py:<module>@24; scripts/datasets/patch_round6.py:<module>@14 (+7 more)
- **Actually used (verified class):** Pipeline resume use verified
- **Necessity:** Redundant - resume checkpoints and caches; regenerable; not in checksum manifest
- **Retention:** Retain checkpoints; caches may be pruned with approval
- **Limitations:** not covered by checksum manifest; regenerable except checkpoints

## How it is used in the problem statement and project
- No requirement mapping (non-dataset asset or no verified role): intended module = R-RM reproducibility

**Code touching this dataset (file : symbol : operation):** `scripts/datasets/audit.py:_` (reference, lines 210-210); `scripts/datasets/common.py:<module>` (reference, lines 12-12); `scripts/datasets/common.py:AccessLog` (reference, lines 78-78); `scripts/datasets/common.py:add` (write/produce, lines 81-81); `scripts/datasets/patch_round4.py:<module>` (reference, lines 24-24); `scripts/datasets/patch_round6.py:<module>` (reference, lines 14-15); `scripts/datasets/s4_variants.py:<module>` (write/produce, lines 10-10); `scripts/datasets/s4_variants.py:make` (write/produce, lines 83-83); `scripts/datasets/s4b_purge_ineligible.py:<module>` (reference, lines 9-9); `scripts/datasets/s5_features_pairs_splits.py:<module>` (reference, lines 12-12) ... (+2 more in DATASET_TO_IMPLEMENTATION_MAP.csv)

## Columns / fields (36 across 3 file(s))

### `data/manifests/_build/access_log.jsonl`  - 14 fields, 500 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| $ | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.attempt_time_utc | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 2026-10-26T06:13:43Z | metadata | Unreferenced in project code |
| $.method | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | api | metadata | Unreferenced in project code |
| $.retry_count | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 0 | metadata | Unreferenced in project code |
| $.terms_decision | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | permitted_by_licence_or_open_access | metadata | Unreferenced in project code |
| $.source_dataset_id | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | RW-01 | metadata | Unreferenced in project code |
| $.media_or_file_id | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | search:speech:0 | metadata | Unreferenced in project code |
| $.url | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | https://commons.wikimedia.org/w/api.php?action=que | metadata | Unreferenced in project code |
| $.http_status | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 200 | metadata | Unreferenced in project code |
| $.result_category | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | ok | metadata | Unreferenced in project code |
| $.bytes | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 120502 | metadata | Unreferenced in project code |
| $.sha256 | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.final_status | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | downloaded_authorized | metadata | Unreferenced in project code |
| $.note | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |

### `data/manifests/_build/eligible_titles.txt`  - 1 fields, 59 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| eligible_titles.txt | str | one value per line | see file | see file | 0 | 59 | 61797230 / Boston Free Speech rally attendees leaving.ogv / speech / B | metadata | Unreferenced in project code |

### `data/manifests/_build/variants/*.json`  - 21 fields, 55 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| $ | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.recs | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.recs[] | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.recs[].<key> | str/int/float/bool | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | CV-P10491224-V01 | metadata | Unreferenced in project code |
| $.logs | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.logs[] | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.logs[].run_id | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | RUN-CV-P10491224-V01 | metadata | Unreferenced in project code |
| $.logs[].variant_media_id | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | CV-P10491224-V01 | metadata | Unreferenced in project code |
| $.logs[].input_media_ids | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | RW-CMN-P10491224 | metadata | Unreferenced in project code |
| $.logs[].tool_name | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | ffmpeg | metadata | Unreferenced in project code |
| $.logs[].tool_version | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | ffmpeg version 9.0.2-essentials_build-www.gyan.dev | metadata | Unreferenced in project code |
| $.logs[].command_config | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | -y -v error -i <ROOT>\data/real_world/media/common | metadata | Unreferenced in project code |
| $.logs[].parameters_json | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | {"crf": 18} | metadata | Unreferenced in project code |
| $.logs[].started_utc | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 2026-10-26T06:41:04Z | metadata | Unreferenced in project code |
| $.logs[].return_code | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 0 | metadata | Unreferenced in project code |
| $.logs[].output_validation_status | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | passed | metadata | Unreferenced in project code |
| $.logs[].output_bytes | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 5755540 | metadata | Unreferenced in project code |
| $.logs[].storage_delta_bytes | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 5755540 | metadata | Unreferenced in project code |
| $.logs[].error | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.logs[].deterministic_notes | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | parameters fixed; donor/caption picked by sha256 o | metadata | Unreferenced in project code |
| $.logs[].seed | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | sha256-pick:RW-CMN-P10491224 | metadata | Unreferenced in project code |

---
# DS-033 - Acceptance and QA report artefacts

- **Family / component / category:** ORVEX QA / reports / Generated reports
- **Original publisher:** ORVEX project (generated)
- **Original source:** N/A (generated in this repository)
- **How it entered the project:** ORVEX scripts (see Processing History)
- **What was retained:** generated artefact
- **Provenance category:** 1 Verified from repository evidence (external source not re-checked online)
- **Location:** `data/reports` (JSON/TXT); availability: Local files; state: derived/processed
- **Files / records / size:** 3 / 3 / 32201 bytes (0.000 GB)
- **Usable / excluded:** n/a / n/a
- **Licence:** N/A
- **Referenced by code:** N/A
- **Actually used (verified class):** N/A
- **Necessity:** Useful and justified - validation evidence snapshots
- **Retention:** Retain
- **Limitations:** snapshots of a past run

## How it is used in the problem statement and project
- No requirement mapping (non-dataset asset or no verified role): intended module = R-RM

## Columns / fields (4 across 1 file(s))

### `data/reports/acceptance_checks.json`  - 4 fields, 1 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| $ | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.<key> | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.<key>.ok | bool | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | True | metadata | Unreferenced in project code |
| $.<key>.evidence | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 15 tables, 306 contract columns; mismatches: none | metadata | Unreferenced in project code |

---
# DS-034 - Dataset documentation corpus (docs/datasets, incl. necessity_audit)

- **Family / component / category:** documentation / documents + small CSV/JSON / Documentation (not a dataset)
- **Original publisher:** ORVEX project (generated)
- **Original source:** N/A (generated in this repository)
- **How it entered the project:** ORVEX scripts (see Processing History)
- **What was retained:** generated artefact
- **Provenance category:** 4 Not applicable / unknown
- **Location:** `docs/datasets` (MD/CSV/JSON); availability: Local files; state: derived/processed
- **Files / records / size:** 21 / 21 / 412378 bytes (0.000 GB)
- **Usable / excluded:** n/a / n/a
- **Licence:** N/A
- **Referenced by code:** N/A
- **Actually used (verified class):** N/A
- **Necessity:** Useful and justified - documentation (some hand-edited numbers can go stale)
- **Retention:** Retain
- **Limitations:** numbers in hand-written reports can become stale (see findings)

## How it is used in the problem statement and project
- No requirement mapping (non-dataset asset or no verified role): intended module = R-RM

## Columns / fields (358 across 7 file(s))

### `docs/datasets/ORVEX_REQUIREMENT_COVERAGE_MATRIX.csv`  - 10 fields, 40 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| requirement_id | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 40 | R01 | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| pdf_reference | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 35 | p2 §2; p4 §5 Phase 1 | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| requirement | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 40 | Create a controlled dataset from real source video | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| modules | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 16 | M1,M3 | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| phase | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 4 | 1 | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| artifacts | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 40 | controlled_variant_registry, media_relationship_ed | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| checks | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 38 | K04/K10/K11 | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| status | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 3 | PASS | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| evidence | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 38 | K04: 1131 passed variants; chains not ending in an | metadata (unverified meaning) | Used by downstream code |
| limitation_or_blocker | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 52.5 | 19 | captions are mismatched real titles (constructed), | metadata (unverified meaning) | Referenced by audit/docs/tests only |

### `docs/datasets/column_lineage.csv`  - 13 fields, 306 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| table | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 15 | source_registry | metadata (unverified meaning) | Used by downstream code |
| column | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 243 | source_dataset_id | metadata (unverified meaning) | Used by downstream code |
| source_datasets | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 11 | ORVEX (no source-dataset field) | metadata (unverified meaning) | Used by downstream code |
| type | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 6 | str | metadata (unverified meaning) | Used by downstream code |
| nullable | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 2 | no | metadata (unverified meaning) | Used by downstream code |
| origin_code | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 6 | f | metadata (unverified meaning) | Used by downstream code |
| origin_meaning | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 6 | new ORVEX bookkeeping/administrative column | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| source_field_or_rule | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 132 | ORVEX id (RW-xx) | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| present_in_source_dataset | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 2 | no (ORVEX-added) | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| description | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 271 | Stable ORVEX id of the real-world source dataset. | metadata (unverified meaning) | Used by downstream code |
| allowed_values | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 62.09 | 103 | observed: 2026-10-26 | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| validation | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 2 | contract header + non-null check (K01,K02) | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| rationale | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 2 | added by ORVEX to support relationship learning/ev | metadata (unverified meaning) | Referenced by audit/docs/tests only |

### `docs/datasets/necessity_audit/dataset_inventory.csv`  - 9 fields, 47 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| kind | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 2 | real-world | metadata (unverified meaning) | Used by downstream code |
| id | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 47 | RW-01 | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| name | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 47 | Wikimedia Commons CC/PD video pool (ORVEX selectio | metadata (unverified meaning) | Used by downstream code |
| classification | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 10 | real-world media downloaded and verified (selected | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| status | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 9 | included_selected_subset | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| verification | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 5 | verified_api | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| records_local | int | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 23 | 96 | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| local_bytes | int | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 25 | 1687283416 | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| reason | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 34.04 | 31 | Only surveyed source with real media bytes whose p | metadata (unverified meaning) | Referenced by audit/docs/tests only |

### `docs/datasets/necessity_audit/dhash_baseline_results.json`  - 89 fields, 1 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| $ | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.threshold_fixed_a_priori | float | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 0.45 | metadata | Unreferenced in project code |
| $.pairs_scored | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 9928 | metadata | Unreferenced in project code |
| $.latency_ms_per_pair | float | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 0.0194 | metadata | Unreferenced in project code |
| $.auc_train | float | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 0.8734 | metadata | Unreferenced in project code |
| $.auc_val | float | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 0.8992 | metadata | Unreferenced in project code |
| $.auc_test | float | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 0.8307 | metadata | Unreferenced in project code |
| $.test_negatives_by_hardness | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.test_negatives_by_hardness.easy | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 114 | metadata | Unreferenced in project code |
| $.test_negatives_by_hardness.hard | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 36 | metadata | Unreferenced in project code |
| $.auc_test_hard_negatives_only | float | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 0.8307 | metadata | Unreferenced in project code |
| $.auc_test_easy_negatives_only | float | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 0.8307 | metadata | Unreferenced in project code |
| $.auc_test_without_heldout_lineage | float | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 0.8486 | metadata | Unreferenced in project code |
| $.auc_test_heldout_lineage_pos_vs_all_neg | float | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 0.7922 | metadata | Unreferenced in project code |
| $.detection_rate_threshold | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.detection_rate_threshold.audio_source_only_not_visual_derivation | float | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 0.0 | metadata | Unreferenced in project code |
| $.detection_rate_threshold.direct_derivation | float | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 0.823 | metadata | Unreferenced in project code |
| $.detection_rate_threshold.edited_version | float | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 0.92 | metadata | Unreferenced in project code |
| $.detection_rate_threshold.indirect_derivation | float | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 0.451 | metadata | Unreferenced in project code |
| $.detection_rate_threshold.same_family_other | float | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 0.382 | metadata | Unreferenced in project code |
| $.detection_rate_threshold.sibling_same_parent | float | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 0.669 | metadata | Unreferenced in project code |
| $.detection_rate_threshold.unrelated_distinct_source | float | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 0.0 | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.audio_mute | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.audio_mute.n | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 42 | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.audio_mute.detected | float | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 0.976 | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.audio_mute.audio_identical | float | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 0.0 | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.audio_noise_mix | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.audio_noise_mix.n | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 5 | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.audio_noise_mix.detected | float | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 1.0 | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.audio_noise_mix.audio_identical | float | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 0.0 | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.audio_replace | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.audio_replace.n | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 55 | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.audio_replace.detected | float | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 0.964 | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.audio_replace.audio_identical | float | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 0.0 | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.caption_burn_in | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.caption_burn_in.n | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 110 | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.caption_burn_in.detected | float | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 0.982 | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.caption_burn_in.audio_identical | float | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 0.009 | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.crop_center | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.crop_center.n | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 110 | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.crop_center.detected | float | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 0.036 | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.crop_center.audio_identical | float | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 0.009 | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.mirror_color_shift | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.mirror_color_shift.n | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 7 | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.mirror_color_shift.detected | float | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 0.143 | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.mirror_color_shift.audio_identical | float | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 0.0 | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.recompress_low | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.recompress_low.n | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 220 | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.recompress_low.detected | float | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 0.986 | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.recompress_low.audio_identical | float | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 0.014 | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.reencode_hq | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.reencode_hq.n | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 55 | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.reencode_hq.detected | float | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 0.964 | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.reencode_hq.audio_identical | float | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 0.0 | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.reupload_sim | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.reupload_sim.n | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 7 | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.reupload_sim.detected | float | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 0.857 | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.reupload_sim.audio_identical | float | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 0.0 | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.speed_change | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.speed_change.n | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 7 | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.speed_change.detected | float | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 1.0 | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.speed_change.audio_identical | float | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 0.0 | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.trim_head | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.trim_head.n | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 55 | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.trim_head.detected | float | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 0.745 | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.trim_head.audio_identical | float | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 0.0 | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.trim_middle | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.trim_middle.n | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 55 | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.trim_middle.detected | float | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 0.673 | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.trim_middle.audio_identical | float | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 0.0 | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.trim_tail | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.trim_tail.n | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 55 | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.trim_tail.detected | float | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 0.8 | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.trim_tail.audio_identical | float | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 0.0 | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.watermark_overlay | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.watermark_overlay.n | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 165 | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.watermark_overlay.detected | float | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 0.988 | metadata | Unreferenced in project code |
| $.direct_derivation_detection_by_transformation.watermark_overlay.audio_identical | float | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 0.012 | metadata | Unreferenced in project code |
| $.temporal_start_estimation | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.temporal_start_estimation.n | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 162 | metadata | Unreferenced in project code |
| $.temporal_start_estimation.mean_abs_error_fraction | float | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 0.0758 | metadata | Unreferenced in project code |
| $.temporal_start_estimation.within_0_05 | float | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 0.704 | metadata | Unreferenced in project code |
| $.temporal_start_estimation.first_frame_matched | float | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 0.704 | metadata | Unreferenced in project code |
| $.temporal_start_estimation.per_type | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.temporal_start_estimation.per_type.trim_head | float | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 0.1316 | metadata | Unreferenced in project code |
| $.temporal_start_estimation.per_type.trim_middle | float | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 0.0935 | metadata | Unreferenced in project code |
| $.temporal_start_estimation.per_type.trim_tail | float | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 0.0024 | metadata | Unreferenced in project code |
| $.temporal_start_estimation.note | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 24 sampled frames give ~4% granularity; finer segm | metadata | Unreferenced in project code |

### `docs/datasets/necessity_audit/requirement_data_decision_table.csv`  - 12 fields, 40 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| requirement_id | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 40 | R01 | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| required_capability | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 40 | Create a controlled dataset from real source video | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| existing_support | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 40 | controlled_variant_registry, media_relationship_ed | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| evidence_it_works | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 37 | K04: 1131 passed variants; chains not ending in an | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| gap | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 20 | none | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| gap_type | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 12 | none | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| additional_data_necessary | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 2 | no | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| recommended_source_or_transformation | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 17 | none | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| permission_constraints | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 8 | licences of Commons sources | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| est_additional_storage_gb | float | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 7 | 0.0 | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| acceptance_test | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 37 | K04,K10,K11 | metadata (unverified meaning) | Referenced by audit/docs/tests only |
| status_now | str | Not documented in the repository; meaning inferred from header and values | Unknown | Unknown | 0.0 | 3 | PASS | metadata (unverified meaning) | Referenced by audit/docs/tests only |

### `docs/datasets/necessity_audit/variant_independent_validation.json`  - 17 fields, 1 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| $ | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.passed_variants | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 1131 | metadata | Unreferenced in project code |
| $.readable_by_independent_ffprobe | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 1131 | metadata | Unreferenced in project code |
| $.duration_matches_registry | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 1131 | metadata | Unreferenced in project code |
| $.carries_controlled_variant_metadata_tag | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 1131 | metadata | Unreferenced in project code |
| $.parent_chain_complete | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 1131 | metadata | Unreferenced in project code |
| $.roots_eligible | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 1131 | metadata | Unreferenced in project code |
| $.audio_variants | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 99 | metadata | Unreferenced in project code |
| $.audio_donor_documented_real_eligible | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 99 | metadata | Unreferenced in project code |
| $.caption_variants | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 110 | metadata | Unreferenced in project code |
| $.caption_variants_with_real_source_text | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 110 | metadata | Unreferenced in project code |
| $.run_log_return0_and_passed | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 1131 | metadata | Unreferenced in project code |
| $.tool_params_run_recorded | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 1131 | metadata | Unreferenced in project code |
| $.failed_variants | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 2 | metadata | Unreferenced in project code |
| $.failed_excluded_and_no_file | int | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | 2 | metadata | Unreferenced in project code |
| $.leakage_check | bool | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | True | metadata | Unreferenced in project code |
| $.heldout_check | bool | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | True | metadata | Unreferenced in project code |

### `docs/datasets/schema_contract.json`  - 208 fields, 1 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| $ | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.origin_codes | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.origin_codes.a | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | copied from a named source field | metadata | Unreferenced in project code |
| $.origin_codes.b | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | normalized/renamed from a named source field | metadata | Unreferenced in project code |
| $.origin_codes.c | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | derived by an explicit deterministic rule from nam | metadata | Unreferenced in project code |
| $.origin_codes.d | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | computed from the actual media/files by a named to | metadata | Unreferenced in project code |
| $.origin_codes.e | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | annotated/decided by a human analyst with stated e | metadata | Unreferenced in project code |
| $.origin_codes.f | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | new ORVEX bookkeeping/administrative column | metadata | Unreferenced in project code |
| $.vocabularies | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.vocabularies.record_origin | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.vocabularies.record_origin[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | real_world_source_record | metadata | Unreferenced in project code |
| $.vocabularies.media_origin | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.vocabularies.media_origin[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | naturally_collected_real_world | metadata | Unreferenced in project code |
| $.vocabularies.transformation_status | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.vocabularies.transformation_status[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | none_source_unmodified | metadata | Unreferenced in project code |
| $.vocabularies.access_status | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.vocabularies.access_status[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | downloaded_authorized | metadata | Unreferenced in project code |
| $.vocabularies.direction_status | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.vocabularies.direction_status[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | directed_supported_by_source | metadata | Unreferenced in project code |
| $.vocabularies.label_status | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.vocabularies.label_status[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | source_ground_truth | metadata | Unreferenced in project code |
| $.vocabularies.inclusion_status | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.vocabularies.inclusion_status[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | included_media_and_metadata | metadata | Unreferenced in project code |
| $.vocabularies.split | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.vocabularies.split[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | train | metadata | Unreferenced in project code |
| $.vocabularies.validation_status | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.vocabularies.validation_status[] | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | passed | metadata | Unreferenced in project code |
| $.tables | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.tables.source_registry | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.tables.source_registry.path | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | data/manifests/source_registry.csv | metadata | Unreferenced in project code |
| $.tables.source_registry.purpose | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | Every dataset/source considered, with official sou | metadata | Unreferenced in project code |
| $.tables.source_registry.phase | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | both | metadata | Unreferenced in project code |
| $.tables.source_registry.columns | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.tables.source_registry.columns[] | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.tables.source_registry.columns[].name | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | source_dataset_id | metadata | Unreferenced in project code |
| $.tables.source_registry.columns[].type | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | str | metadata | Unreferenced in project code |
| $.tables.source_registry.columns[].nullable | bool | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | False | metadata | Unreferenced in project code |
| $.tables.source_registry.columns[].origin | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | f | metadata | Unreferenced in project code |
| $.tables.source_registry.columns[].lineage | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | ORVEX id (RW-xx) | metadata | Unreferenced in project code |
| $.tables.source_registry.columns[].description | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | Stable ORVEX id of the real-world source dataset. | metadata | Unreferenced in project code |
| $.tables.real_world_media_master | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.tables.real_world_media_master.path | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | data/derived/tables/real_world_media_master.csv | metadata | Unreferenced in project code |
| $.tables.real_world_media_master.purpose | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | Normalized master of every real-world media record | metadata | Unreferenced in project code |
| $.tables.real_world_media_master.phase | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | both | metadata | Unreferenced in project code |
| $.tables.real_world_media_master.columns | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.tables.real_world_media_master.columns[] | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.tables.real_world_media_master.columns[].name | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | media_id | metadata | Unreferenced in project code |
| $.tables.real_world_media_master.columns[].type | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | str | metadata | Unreferenced in project code |
| $.tables.real_world_media_master.columns[].nullable | bool | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | False | metadata | Unreferenced in project code |
| $.tables.real_world_media_master.columns[].origin | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | f | metadata | Unreferenced in project code |
| $.tables.real_world_media_master.columns[].lineage | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | ORVEX id | metadata | Unreferenced in project code |
| $.tables.real_world_media_master.columns[].description | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | Stable internal id (RW-<src>-...). | metadata | Unreferenced in project code |
| $.tables.controlled_variant_registry | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.tables.controlled_variant_registry.path | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | data/derived/tables/controlled_variant_registry.cs | metadata | Unreferenced in project code |
| $.tables.controlled_variant_registry.purpose | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | Every controlled variant rendered by ORVEX from el | metadata | Unreferenced in project code |
| $.tables.controlled_variant_registry.phase | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | phase1 | metadata | Unreferenced in project code |
| $.tables.controlled_variant_registry.columns | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.tables.controlled_variant_registry.columns[] | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.tables.controlled_variant_registry.columns[].name | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | variant_media_id | metadata | Unreferenced in project code |
| $.tables.controlled_variant_registry.columns[].type | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | str | metadata | Unreferenced in project code |
| $.tables.controlled_variant_registry.columns[].nullable | bool | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | False | metadata | Unreferenced in project code |
| $.tables.controlled_variant_registry.columns[].origin | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | f | metadata | Unreferenced in project code |
| $.tables.controlled_variant_registry.columns[].lineage | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | ORVEX id | metadata | Unreferenced in project code |
| $.tables.controlled_variant_registry.columns[].description | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | Id of the created video (CV-...). | metadata | Unreferenced in project code |
| $.tables.media_relationship_edges | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.tables.media_relationship_edges.path | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | data/derived/tables/media_relationship_edges.csv | metadata | Unreferenced in project code |
| $.tables.media_relationship_edges.purpose | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | Relationship edges: source-provided native relatio | metadata | Unreferenced in project code |
| $.tables.media_relationship_edges.phase | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | both | metadata | Unreferenced in project code |
| $.tables.media_relationship_edges.columns | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.tables.media_relationship_edges.columns[] | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.tables.media_relationship_edges.columns[].name | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | relationship_id | metadata | Unreferenced in project code |
| $.tables.media_relationship_edges.columns[].type | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | str | metadata | Unreferenced in project code |
| $.tables.media_relationship_edges.columns[].nullable | bool | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | False | metadata | Unreferenced in project code |
| $.tables.media_relationship_edges.columns[].origin | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | f | metadata | Unreferenced in project code |
| $.tables.media_relationship_edges.columns[].lineage | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | ORVEX | metadata | Unreferenced in project code |
| $.tables.media_relationship_edges.columns[].description | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | Edge id. | metadata | Unreferenced in project code |
| $.tables.platform_observations | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.tables.platform_observations.path | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | data/derived/tables/platform_observations.csv | metadata | Unreferenced in project code |
| $.tables.platform_observations.purpose | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | Real posts/observations of media on platforms as p | metadata | Unreferenced in project code |
| $.tables.platform_observations.phase | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | phase2 | metadata | Unreferenced in project code |
| $.tables.platform_observations.columns | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.tables.platform_observations.columns[] | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.tables.platform_observations.columns[].name | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | observation_id | metadata | Unreferenced in project code |
| $.tables.platform_observations.columns[].type | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | str | metadata | Unreferenced in project code |
| $.tables.platform_observations.columns[].nullable | bool | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | False | metadata | Unreferenced in project code |
| $.tables.platform_observations.columns[].origin | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | f | metadata | Unreferenced in project code |
| $.tables.platform_observations.columns[].lineage | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | ORVEX | metadata | Unreferenced in project code |
| $.tables.platform_observations.columns[].description | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | Id. | metadata | Unreferenced in project code |
| $.tables.evidence_ledger | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.tables.evidence_ledger.path | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | data/derived/tables/evidence_ledger.csv | metadata | Unreferenced in project code |
| $.tables.evidence_ledger.purpose | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | Evidence records supporting labels, relations and  | metadata | Unreferenced in project code |
| $.tables.evidence_ledger.phase | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | both | metadata | Unreferenced in project code |
| $.tables.evidence_ledger.columns | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.tables.evidence_ledger.columns[] | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.tables.evidence_ledger.columns[].name | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | evidence_id | metadata | Unreferenced in project code |
| $.tables.evidence_ledger.columns[].type | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | str | metadata | Unreferenced in project code |
| $.tables.evidence_ledger.columns[].nullable | bool | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | False | metadata | Unreferenced in project code |
| $.tables.evidence_ledger.columns[].origin | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | f | metadata | Unreferenced in project code |
| $.tables.evidence_ledger.columns[].lineage | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | ORVEX | metadata | Unreferenced in project code |
| $.tables.evidence_ledger.columns[].description | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | Id. | metadata | Unreferenced in project code |
| $.tables.feature_manifest | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.tables.feature_manifest.path | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | data/derived/tables/feature_manifest.csv | metadata | Unreferenced in project code |
| $.tables.feature_manifest.purpose | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | What features actually exist (and which are not co | metadata | Unreferenced in project code |
| $.tables.feature_manifest.phase | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | both | metadata | Unreferenced in project code |
| $.tables.feature_manifest.columns | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.tables.feature_manifest.columns[] | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.tables.feature_manifest.columns[].name | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | feature_record_id | metadata | Unreferenced in project code |
| $.tables.feature_manifest.columns[].type | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | str | metadata | Unreferenced in project code |
| $.tables.feature_manifest.columns[].nullable | bool | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | False | metadata | Unreferenced in project code |
| $.tables.feature_manifest.columns[].origin | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | f | metadata | Unreferenced in project code |
| $.tables.feature_manifest.columns[].lineage | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | ORVEX | metadata | Unreferenced in project code |
| $.tables.feature_manifest.columns[].description | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | Id. | metadata | Unreferenced in project code |
| $.tables.training_pairs | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.tables.training_pairs.path | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | data/derived/tables/training_pairs.csv | metadata | Unreferenced in project code |
| $.tables.training_pairs.purpose | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | Model examples (related/unrelated/uncertain pairs) | metadata | Unreferenced in project code |
| $.tables.training_pairs.phase | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | phase1 | metadata | Unreferenced in project code |
| $.tables.training_pairs.columns | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.tables.training_pairs.columns[] | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.tables.training_pairs.columns[].name | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | example_id | metadata | Unreferenced in project code |
| $.tables.training_pairs.columns[].type | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | str | metadata | Unreferenced in project code |
| $.tables.training_pairs.columns[].nullable | bool | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | False | metadata | Unreferenced in project code |
| $.tables.training_pairs.columns[].origin | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | f | metadata | Unreferenced in project code |
| $.tables.training_pairs.columns[].lineage | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | ORVEX | metadata | Unreferenced in project code |
| $.tables.training_pairs.columns[].description | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | Id. | metadata | Unreferenced in project code |
| $.tables.campaign_candidate_clusters | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.tables.campaign_candidate_clusters.path | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | data/derived/tables/campaign_candidate_clusters.cs | metadata | Unreferenced in project code |
| $.tables.campaign_candidate_clusters.purpose | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | Candidate clusters for human review. EMPTY: no aut | metadata | Unreferenced in project code |
| $.tables.campaign_candidate_clusters.phase | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | phase2 | metadata | Unreferenced in project code |
| $.tables.campaign_candidate_clusters.columns | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.tables.campaign_candidate_clusters.columns[] | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.tables.campaign_candidate_clusters.columns[].name | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | cluster_id | metadata | Unreferenced in project code |
| $.tables.campaign_candidate_clusters.columns[].type | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | str | metadata | Unreferenced in project code |
| $.tables.campaign_candidate_clusters.columns[].nullable | bool | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | False | metadata | Unreferenced in project code |
| $.tables.campaign_candidate_clusters.columns[].origin | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | f | metadata | Unreferenced in project code |
| $.tables.campaign_candidate_clusters.columns[].lineage | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | ORVEX | metadata | Unreferenced in project code |
| $.tables.campaign_candidate_clusters.columns[].description | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | Id. | metadata | Unreferenced in project code |
| $.tables.transformation_run_log | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.tables.transformation_run_log.path | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | data/derived/tables/transformation_run_log.csv | metadata | Unreferenced in project code |
| $.tables.transformation_run_log.purpose | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | One row per transformation execution. | metadata | Unreferenced in project code |
| $.tables.transformation_run_log.phase | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | phase1 | metadata | Unreferenced in project code |
| $.tables.transformation_run_log.columns | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.tables.transformation_run_log.columns[] | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.tables.transformation_run_log.columns[].name | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | run_id | metadata | Unreferenced in project code |
| $.tables.transformation_run_log.columns[].type | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | str | metadata | Unreferenced in project code |
| $.tables.transformation_run_log.columns[].nullable | bool | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | False | metadata | Unreferenced in project code |
| $.tables.transformation_run_log.columns[].origin | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | f | metadata | Unreferenced in project code |
| $.tables.transformation_run_log.columns[].lineage | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | ORVEX | metadata | Unreferenced in project code |
| $.tables.transformation_run_log.columns[].description | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | Run id. | metadata | Unreferenced in project code |
| $.tables.download_access_attempt_log | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.tables.download_access_attempt_log.path | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | data/manifests/download_access_attempt_log.csv | metadata | Unreferenced in project code |
| $.tables.download_access_attempt_log.purpose | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | Every download/access attempt. | metadata | Unreferenced in project code |
| $.tables.download_access_attempt_log.phase | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | both | metadata | Unreferenced in project code |
| $.tables.download_access_attempt_log.columns | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.tables.download_access_attempt_log.columns[] | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.tables.download_access_attempt_log.columns[].name | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | attempt_id | metadata | Unreferenced in project code |
| $.tables.download_access_attempt_log.columns[].type | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | str | metadata | Unreferenced in project code |
| $.tables.download_access_attempt_log.columns[].nullable | bool | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | False | metadata | Unreferenced in project code |
| $.tables.download_access_attempt_log.columns[].origin | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | f | metadata | Unreferenced in project code |
| $.tables.download_access_attempt_log.columns[].lineage | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | ORVEX | metadata | Unreferenced in project code |
| $.tables.download_access_attempt_log.columns[].description | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | Id. | metadata | Unreferenced in project code |
| $.tables.split_manifest | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.tables.split_manifest.path | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | data/derived/splits/split_manifest.csv | metadata | Unreferenced in project code |
| $.tables.split_manifest.purpose | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | Source-family level split assignment. | metadata | Unreferenced in project code |
| $.tables.split_manifest.phase | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | phase1 | metadata | Unreferenced in project code |
| $.tables.split_manifest.columns | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.tables.split_manifest.columns[] | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.tables.split_manifest.columns[].name | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | split_version | metadata | Unreferenced in project code |
| $.tables.split_manifest.columns[].type | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | str | metadata | Unreferenced in project code |
| $.tables.split_manifest.columns[].nullable | bool | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | False | metadata | Unreferenced in project code |
| $.tables.split_manifest.columns[].origin | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | f | metadata | Unreferenced in project code |
| $.tables.split_manifest.columns[].lineage | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | ORVEX | metadata | Unreferenced in project code |
| $.tables.split_manifest.columns[].description | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | Version. | metadata | Unreferenced in project code |
| $.tables.experiment_registry | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.tables.experiment_registry.path | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | data/derived/tables/experiment_registry.csv | metadata | Unreferenced in project code |
| $.tables.experiment_registry.purpose | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | Evaluation registry. Holds only the non-learned dH | metadata | Unreferenced in project code |
| $.tables.experiment_registry.phase | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | phase1 | metadata | Unreferenced in project code |
| $.tables.experiment_registry.columns | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.tables.experiment_registry.columns[] | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.tables.experiment_registry.columns[].name | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | experiment_id | metadata | Unreferenced in project code |
| $.tables.experiment_registry.columns[].type | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | str | metadata | Unreferenced in project code |
| $.tables.experiment_registry.columns[].nullable | bool | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | False | metadata | Unreferenced in project code |
| $.tables.experiment_registry.columns[].origin | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | f | metadata | Unreferenced in project code |
| $.tables.experiment_registry.columns[].lineage | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | ORVEX | metadata | Unreferenced in project code |
| $.tables.experiment_registry.columns[].description | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | Id. | metadata | Unreferenced in project code |
| $.tables.duplicate_map | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.tables.duplicate_map.path | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | data/derived/tables/duplicate_map.csv | metadata | Unreferenced in project code |
| $.tables.duplicate_map.purpose | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | Exact/near duplicates and cross-version repeats; c | metadata | Unreferenced in project code |
| $.tables.duplicate_map.phase | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | both | metadata | Unreferenced in project code |
| $.tables.duplicate_map.columns | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.tables.duplicate_map.columns[] | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.tables.duplicate_map.columns[].name | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | duplicate_id | metadata | Unreferenced in project code |
| $.tables.duplicate_map.columns[].type | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | str | metadata | Unreferenced in project code |
| $.tables.duplicate_map.columns[].nullable | bool | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | False | metadata | Unreferenced in project code |
| $.tables.duplicate_map.columns[].origin | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | f | metadata | Unreferenced in project code |
| $.tables.duplicate_map.columns[].lineage | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | ORVEX | metadata | Unreferenced in project code |
| $.tables.duplicate_map.columns[].description | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | Id. | metadata | Unreferenced in project code |
| $.tables.group_examples | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.tables.group_examples.path | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | data/derived/tables/group_examples.csv | metadata | Unreferenced in project code |
| $.tables.group_examples.purpose | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | Groups of 6 videos (4 related family members + 2 d | metadata | Unreferenced in project code |
| $.tables.group_examples.phase | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | phase1 | metadata | Unreferenced in project code |
| $.tables.group_examples.columns | list | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.tables.group_examples.columns[] | dict | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a |  | metadata | Unreferenced in project code |
| $.tables.group_examples.columns[].name | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | group_id | metadata | Unreferenced in project code |
| $.tables.group_examples.columns[].type | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | str | metadata | Unreferenced in project code |
| $.tables.group_examples.columns[].nullable | bool | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | False | metadata | Unreferenced in project code |
| $.tables.group_examples.columns[].origin | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | f | metadata | Unreferenced in project code |
| $.tables.group_examples.columns[].lineage | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | ORVEX | metadata | Unreferenced in project code |
| $.tables.group_examples.columns[].description | str | Nested field; not individually documented in the repository (structure inferred from data; occurrences counted) | Added by ORVEX (generated artefact) | see file | n/a | n/a | Group id. | metadata | Unreferenced in project code |

---
# DS-035 - ORVEX_Literature corpus (35 PDFs, text, review workbook)

- **Family / component / category:** literature review (10.1) / papers + spreadsheet / Research literature (not ORVEX data)
- **Original publisher:** N/A
- **Original source:** arXiv/CVF/EURASIP open copies (see ORVEX_Literature)
- **How it entered the project:** ORVEX scripts (see Processing History)
- **What was retained:** generated artefact
- **Provenance category:** 4 Not applicable / unknown
- **Location:** `ORVEX_Literature` (PDF/TXT/XLSX); availability: Local files; state: n/a
- **Files / records / size:** 77 / 77 / 240494329 bytes (0.240 GB)
- **Usable / excluded:** n/a / n/a
- **Licence:** N/A
- **Referenced by code:** N/A
- **Actually used (verified class):** Documented/reference
- **Necessity:** Unused - literature corpus; not consumed by data pipeline
- **Retention:** Retain for research context (outside budget)
- **Limitations:** outside the dataset budget; 3 PDFs not analysed in the workbook

## How it is used in the problem statement and project
- No requirement mapping (non-dataset asset or no verified role): intended module = R-RM-10.1

## Columns / fields (51 across 7 file(s))

### `ORVEX_Literature/ORVEX_Literature_Review_10_1.xlsx#Feasibility`  - 6 fields, 12 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| Area | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 12 | Dataset creation (Phase 1) | documentation | Unreferenced in project code |
| Rating | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 6 | High | documentation | Unreferenced in project code |
| Assessment | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 12 | Generating variants with FFmpeg (trim, crop, capti | documentation | Unreferenced in project code |
| Evidence from literature / machine | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 8.33 | 11 | Same recipe used by Bharati 2020, Costa 2014, VPN  | documentation | Unreferenced in project code |
| Main risk | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 12 | Source-video licensing and consent; FFmpeg must be | documentation | Unreferenced in project code |
| Mitigation / decision | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 12 | Install FFmpeg; start with 20-50 videos to test th | documentation | Unreferenced in project code |

### `ORVEX_Literature/ORVEX_Literature_Review_10_1.xlsx#Literature Review`  - 20 fields, 32 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| Novelty and Theme | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 8 | Novelty 1 — Relationship detection instead of real | documentation | Unreferenced in project code |
| Paper Title | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 32 | Image Phylogeny Forests Reconstruction | documentation | Unreferenced in project code |
| Year | int | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 10 | 2014 | documentation | Unreferenced in project code |
| Authors | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 31 | Filipe de O. Costa; Marina A. Oikawa; Zanoni Dias; | documentation | Unreferenced in project code |
| Research Objective | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 32 | Most image-phylogeny methods assume one set of nea | documentation | Unreferenced in project code |
| Detailed Abstract (Paraphrased) | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 32 | Reviews state-of-the-art image-phylogeny algorithm | documentation | Unreferenced in project code |
| Technical Stack / Methods | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 32 | Image phylogeny; optimum-branching (Edmonds/Kruska | documentation | Unreferenced in project code |
| Dataset and Evaluation | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 32 | Synthetic near-duplicate sets built with resamplin | documentation | Unreferenced in project code |
| Main Findings | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 32 | Combined strategies (e.g. E-AOB) outperform the ea | documentation | Unreferenced in project code |
| Conclusion | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 32 | Reconstructing forests rather than single trees is | documentation | Unreferenced in project code |
| Drawbacks / Limitations | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 32 | Images only (no video, audio or captions); relies  | documentation | Unreferenced in project code |
| Similarity to ORVEX | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 32 | Very high conceptual similarity: ORVEX also wants  | documentation | Unreferenced in project code |
| How ORVEX Improves the Limitation | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 32 | ORVEX moves from hand-modelled image transformatio | documentation | Unreferenced in project code |
| Research Gap / Contribution Angle | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 32 | Phylogeny was formalised for images; extension to  | documentation | Unreferenced in project code |
| Novelty Status | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 4 | Foundation (builds on) | documentation | Unreferenced in project code |
| Last Verification | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 1 | Verified (2026-10-26) | documentation | Unreferenced in project code |
| Verification Evidence | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 23 | Full PDF downloaded from the authors' institutiona | documentation | Unreferenced in project code |
| What to Tell the Jury | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 32 | This IEEE paper proved that related images can be  | documentation | Unreferenced in project code |
| Technical Stack / Methods (of my project ORVEX) | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 8 | PLANNED (Modules 3 + 5): pairwise relationship mod | documentation | Unreferenced in project code |
| Dataset and Evaluation (of my project ORVEX) | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 8 | PLANNED: custom dataset of source videos + control | documentation | Unreferenced in project code |

### `ORVEX_Literature/ORVEX_Literature_Review_10_1.xlsx#Novelty Verdict`  - 7 fields, 7 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| ORVEX claim (spec §) | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 7 | 9.1 Relationship detection instead of only real/fa | documentation | Unreferenced in project code |
| Closest prior work in this review | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 7 | Moreira 2018; Costa 2014; Milani 2017; Gerhardt 20 | documentation | Unreferenced in project code |
| What already exists | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 7 | Provenance/phylogeny graphs for images, for audio, | documentation | Unreferenced in project code |
| What was NOT found in this review | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 7 | A LEARNED, multi-modal (visual + audio + text) rel | documentation | Unreferenced in project code |
| Verdict | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 7 | Partially novel (extension, not invention) | documentation | Unreferenced in project code |
| Safe wording for report / jury | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 7 | ORVEX extends provenance/phylogeny analysis from i | documentation | Unreferenced in project code |
| Evidence needed from experiments | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 7 | Beat pairwise-similarity baselines (ViSiL-style, S | documentation | Unreferenced in project code |

### `ORVEX_Literature/ORVEX_Literature_Review_10_1.xlsx#Open Items`  - 3 fields, 9 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| # | int | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 9 | 1 | documentation | Unreferenced in project code |
| Item | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 9 | IEEE Xplore was not searched directly | documentation | Unreferenced in project code |
| Why / suggested next step | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 9 | No authenticated access from this environment. IEE | documentation | Unreferenced in project code |

### `ORVEX_Literature/ORVEX_Literature_Review_10_1.xlsx#Paper Register`  - 9 fields, 32 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| # | int | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 32 | 1 | documentation | Unreferenced in project code |
| Theme | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 8 | Novelty 1 | documentation | Unreferenced in project code |
| Paper | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 32 | Image Phylogeny Forests Reconstruction | documentation | Unreferenced in project code |
| Year | int | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 10 | 2014 | documentation | Unreferenced in project code |
| Venue / source | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 32 | IEEE Transactions on Information Forensics and Sec | documentation | Unreferenced in project code |
| Link | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 32 | https://www.ic.unicamp.br/~siome/papers/Costa-TIFS | documentation | Used by downstream code |
| Local file | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 32 | Costa_2014_TIFS_image_phylogeny_forests.pdf | documentation | Unreferenced in project code |
| Access | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 2 | Open (author / proceedings copy) | documentation | Unreferenced in project code |
| Verification level | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 1 | Full PDF downloaded; abstract + method/evaluation  | documentation | Unreferenced in project code |

### `ORVEX_Literature/ORVEX_Literature_Review_10_1.xlsx#Research Summary`  - 2 fields, 9 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| Topic | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 9 | Scope of review | documentation | Unreferenced in project code |
| Summary | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 9 | 32 papers analysed in depth (all PDFs downloaded)  | documentation | Unreferenced in project code |

### `ORVEX_Literature/ORVEX_Literature_Review_10_1.xlsx#Search Log`  - 4 fields, 14 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| # | int | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 14 | 1 | documentation | Unreferenced in project code |
| Query / method | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 14 | video phylogeny provenance analysis multimedia nea | documentation | Unreferenced in project code |
| Source | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 3 | Web search | documentation | Unreferenced in project code |
| Outcome | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 14 | Milani 2017, Gerhardt 2024, Politecnico di Milano  | documentation | Unreferenced in project code |

---
# DS-036 - ORVEX_Complete_Project_Specification.pdf

- **Family / component / category:** specification / document / Authoritative specification
- **Original publisher:** N/A
- **Original source:** N/A (generated in this repository)
- **How it entered the project:** ORVEX scripts (see Processing History)
- **What was retained:** generated artefact
- **Provenance category:** 4 Not applicable / unknown
- **Location:** `ORVEX_Complete_Project_Specification.pdf` (PDF); availability: Local files; state: n/a
- **Files / records / size:** 1 / 1 / 251692 bytes (0.000 GB)
- **Usable / excluded:** 13 pages / 0
- **Licence:** N/A
- **Referenced by code:** N/A
- **Actually used (verified class):** Documented/reference
- **Necessity:** Essential - authoritative requirements
- **Retention:** Retain
- **Limitations:** single requirements source (no spec.md/phase.md exists)

## How it is used in the problem statement and project
- No requirement mapping (non-dataset asset or no verified role): intended module = all

## Columns / fields
This component has no structured columns (media files, archives or documents).

---
# DS-037 - LOOP-MIND novelty verification workbook

- **Family / component / category:** unrelated project / document / Unrelated asset
- **Original publisher:** N/A
- **Original source:** N/A (generated in this repository)
- **How it entered the project:** ORVEX scripts (see Processing History)
- **What was retained:** generated artefact
- **Provenance category:** 4 Not applicable / unknown
- **Location:** `LOOP-MIND_Novelty_Independent_Verification_2_4_5.xlsx` (XLSX); availability: Local files; state: n/a
- **Files / records / size:** 1 / 1 / 20779 bytes (0.000 GB)
- **Usable / excluded:** n/a / n/a
- **Licence:** N/A
- **Referenced by code:** N/A
- **Actually used (verified class):** N/A
- **Necessity:** Unsuitable for intended use - different project's workbook
- **Retention:** Retain only if the user wants it; unrelated to ORVEX
- **Limitations:** not an ORVEX dataset

## How it is used in the problem statement and project
- No requirement mapping (non-dataset asset or no verified role): intended module = N/A

## Columns / fields (20 across 1 file(s))

### `LOOP-MIND_Novelty_Independent_Verification_2_4_5.xlsx#Literature Review`  - 20 fields, 9 occurrences/rows
| column | type | meaning | orig/added | derivation | null % | distinct | example | role | usage |
|---|---|---|---|---|---|---|---|---|---|
| Novelty and Theme | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 3 | Novelty 2 — Two-Sided Intelligence — Student Intel | documentation | Unreferenced in project code |
| Paper Title | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 9 | Quasi-Metric Learning for Bilateral Person-Job Fit | documentation | Unreferenced in project code |
| Year | int | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 5 | 2025 | documentation | Unreferenced in project code |
| Authors | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 9 | Yingpeng Du; Hongzhi Liu; Hengshu Zhu; Yang Song;  | documentation | Unreferenced in project code |
| Research Objective | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 9 | Traditional person-job fit models often treat matc | documentation | Unreferenced in project code |
| Detailed Abstract (Paraphrased) | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 9 | The paper proposes a bilateral person-job-fit fram | documentation | Unreferenced in project code |
| Technical Stack / Methods | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 9 | Quasi-metric learning; asymmetric similarity/dista | documentation | Unreferenced in project code |
| Dataset and Evaluation | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 9 | Several real-world recruitment/recommendation data | documentation | Unreferenced in project code |
| Main Findings | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 9 | The proposed bilateral framework improves person-j | documentation | Unreferenced in project code |
| Conclusion | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 9 | The study establishes that bilateral recruitment c | documentation | Unreferenced in project code |
| Drawbacks / Limitations | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 9 | Primarily optimizes bilateral matching/recommendat | documentation | Unreferenced in project code |
| Similarity to LOOP-MIND | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 9 | Very high conceptual similarity to LOOP-MIND's two | documentation | Unreferenced in project code |
| How LOOP-MIND Improves the Limitation | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 9 | Use the two-sided concept as the foundation, then  | documentation | Unreferenced in project code |
| Research Gap / Contribution Angle | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 9 | The research supports the claim that recruitment i | documentation | Unreferenced in project code |
| Novelty Status | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 1 | Partially Used | documentation | Unreferenced in project code |
| Last Verification | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 2 | Not Verified | documentation | Unreferenced in project code |
| Verification Evidence | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 9 | Confirmed via IEEE TPAMI 2025 (Du et al.): the pap | documentation | Unreferenced in project code |
| What to Tell the Jury | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 9 | This paper builds a genuinely bilateral matching a | documentation | Unreferenced in project code |
| Technical Stack / Methods (of my project LOOP-MIND) | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 9 | Two separate portals (student, recruiter) sharing  | documentation | Unreferenced in project code |
| Dataset and Evaluation (of my project LOOP-MIND) | str | Literature/other workbook column (documentation, not a dataset field) | Authored | annotated by author | 0.0 | 9 | No formal dataset/evaluation exists for a bilatera | documentation | Unreferenced in project code |

---
# DS-038 - Tools: portable FFmpeg 9.0.2

- **Family / component / category:** software / binaries + archive / Software (not data)
- **Original publisher:** N/A
- **Original source:** N/A (generated in this repository)
- **How it entered the project:** ORVEX scripts (see Processing History)
- **What was retained:** generated artefact
- **Provenance category:** 4 Not applicable / unknown
- **Location:** `tools` (exe/zip); availability: Local files; state: n/a
- **Files / records / size:** 47 / 47 / 443989875 bytes (0.444 GB)
- **Usable / excluded:** n/a / n/a
- **Licence:** N/A
- **Referenced by code:** N/A
- **Actually used (verified class):** N/A
- **Necessity:** Useful and justified - software required to reproduce media steps
- **Retention:** Retain (outside dataset budget)
- **Limitations:** outside dataset payload

## How it is used in the problem statement and project
- No requirement mapping (non-dataset asset or no verified role): intended module = N/A

## Columns / fields
This component has no structured columns (media files, archives or documents).

---
# DS-039 - Pipeline code and tests

- **Family / component / category:** code / scripts/tests / Code (not data)
- **Original publisher:** N/A
- **Original source:** N/A (generated in this repository)
- **How it entered the project:** ORVEX scripts (see Processing History)
- **What was retained:** generated artefact
- **Provenance category:** 4 Not applicable / unknown
- **Location:** `` (PY); availability: Local files; state: n/a
- **Files / records / size:** 25 / 25 / 303686 bytes (0.000 GB)
- **Usable / excluded:** n/a / n/a
- **Licence:** N/A
- **Referenced by code:** N/A
- **Actually used (verified class):** N/A
- **Necessity:** Useful and justified - reproducibility code; patch scripts are one-off
- **Retention:** Retain
- **Limitations:** one-off patch scripts remain in scripts/datasets

## How it is used in the problem statement and project
- No requirement mapping (non-dataset asset or no verified role): intended module = R-RM

## Columns / fields
This component has no structured columns (media files, archives or documents).

---
# DS-040 - Root-level miscellaneous files

- **Family / component / category:** misc / files / Housekeeping
- **Original publisher:** N/A
- **Original source:** N/A (generated in this repository)
- **How it entered the project:** ORVEX scripts (see Processing History)
- **What was retained:** generated artefact
- **Provenance category:** 4 Not applicable / unknown
- **Location:** `` (misc); availability: Local files; state: n/a
- **Files / records / size:** 2 / 2 / 149 bytes (0.000 GB)
- **Usable / excluded:** n/a / n/a
- **Licence:** N/A
- **Referenced by code:** N/A
- **Actually used (verified class):** N/A
- **Necessity:** Unused - root misc: .gitignore (used) and stray 'nul' (accidental)
- **Retention:** Remove 'nul' only with approval
- **Limitations:** 'nul' is a stray artefact

## How it is used in the problem statement and project
- No requirement mapping (non-dataset asset or no verified role): intended module = N/A

## Columns / fields
This component has no structured columns (media files, archives or documents).
