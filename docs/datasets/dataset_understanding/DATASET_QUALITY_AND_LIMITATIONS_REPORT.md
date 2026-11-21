# Dataset Quality and Limitations Report

Measured values come from `docs/datasets/repository_audit/` (verified live above). Per-dataset limitations:
| id | dataset | limitations |
|---|---|---|
| DS-001 | Wikimedia Commons CC/PD video originals | Small sample (96 files; 55 usable); themes chosen by ORVEX search queries; licence re-check needed before release; 17 originals lack audio |
| DS-002 | Commons source metadata (candidate records) | uploader names are personal data (masked in outputs); some fields (categories) not normalised into DS-016 |
| DS-003 | ANAKIN subset: trimmed + edited videos | Commissioned edits, Vimeo source rights unverified; evaluation-only; not used to create variants |
| DS-004 | ANAKIN subset: edit masks | Present on disk but untracked by the registry; no code reads them |
| DS-005 | ANAKIN metadata and official listing | 1,042 files in the official listing vs 1,023 metadata rows (see findings) |
| DS-006 | InVID Fake Video Corpus 2018 (v3): URLs and labels | No media bytes; no timestamps; labels mean debunked/verified, not AI-generated; URLs not checked for liveness |
| DS-007 | InVID Fake Video Corpus v2.0: URLs, labels, manipulation types | overlaps DS-006 by URL (see overlap matrix); extra native fields (Discussed, Appeared, Timestamp, Channel...) kept only in raw files |
| DS-008 | InVID Fake Video Corpus v1.0: URLs and annotations | Superseded by DS-006/DS-007; authors state it is not meant for quantitative evaluation |
| DS-009 | FIVR-200K: YouTube ids, events, relation annotations | IDs only: no media, titles or timestamps; DS/CS/IS are scene/incident relations, not derivation proof |
| DS-010 | VCSL: video URLs, copied-segment labels, pair/split files | Dataset licence not stated (code MIT); media not downloaded; segment units assumed seconds (not verified); direction of copying not annotated |
| DS-011 | COVID-related misinformation videos and their spread (RW-31) | No sharer accounts; publish/removal timestamps for a minority of videos; timezone unstated; derived tweet times partly outside stated window |
| DS-012 | Official record snapshots (Zenodo API, GitHub READMEs/licence) | Snapshots date from 2026-10-26; not re-fetched in this audit |
| DS-013 | Controlled variant media | Constructed experimental artefacts (not natural posts); audio/caption from other real records; 2 variants failed validation and were not retained |
| DS-014 | Controlled variant registry | Ground truth only for controlled edits |
| DS-015 | Transformation run log | Command lines abstract the root path |
| DS-016 | Real-world media master | metadata-only rows have no media; labels are source-published |
| DS-017 | Media relationship edges | only 1480 edges have media locally; native edges are not derivation proof |
| DS-018 | Platform observations | No sharer accounts; derived tweet times; FVC order only |
| DS-019 | Evidence ledger | dataset-level evidence for native relations (not per-edge) |
| DS-020 | Feature manifest | only dHash/audio features exist; embeddings/OCR/ASR rows say not_computed |
| DS-021 | Visual 24-frame dHash features | weak for crop/mirror (see baseline) |
| DS-022 | Audio fingerprint features | coarse; not an embedding |
| DS-023 | Training pairs | negatives are sampled (uncertain); 3731 excluded |
| DS-024 | Group examples (5-6 videos) | no code reads this table except audit/tests |
| DS-025 | Split manifest (split-v2) | family-level only |
| DS-026 | Duplicate map | perceptual matches are review candidates |
| DS-027 | Source registry | licence/access fields come from snapshots; 15 entries unverified leads |
| DS-028 | Download/access attempt log | pre-existing interactive downloads logged as such |
| DS-029 | Campaign candidate clusters | no authorised account+time evidence |
| DS-030 | Experiment registry | only a non-learned baseline; no ORVEX model |
| DS-031 | Manifests (checksums, crosswalk, attribution, selection plan, storage budget, protocol) | run logs excluded from checksums by design |
| DS-032 | Build intermediates and run logs | not covered by checksum manifest; regenerable except checkpoints |
| DS-033 | Acceptance and QA report artefacts | snapshots of a past run |
| DS-034 | Dataset documentation corpus (docs/datasets, incl. necessity_audit) | numbers in hand-written reports can become stale (see findings) |
| DS-035 | ORVEX_Literature corpus (35 PDFs, text, review workbook) | outside the dataset budget; 3 PDFs not analysed in the workbook |
| DS-036 | ORVEX_Complete_Project_Specification.pdf | single requirements source (no spec.md/phase.md exists) |
| DS-037 | LOOP-MIND novelty verification workbook | not an ORVEX dataset |
| DS-038 | Tools: portable FFmpeg 9.0.2 | outside dataset payload |
| DS-039 | Pipeline code and tests | one-off patch scripts remain in scripts/datasets |
| DS-040 | Root-level miscellaneous files | 'nul' is a stray artefact |

## Defects and inconsistencies (24 findings)
| id | severity | claim | evidence |
|---|---|---|---|
| F-001 | High | Requirement matrices list PASS for capabilities (graph, manipulation analysis, reporting) | No application/model code, notebooks, checkpoints or databases exist (no package.json/pyproject/backend/frontend; 0 model artifacts); only data pipeline scripts s1-s9 and one non-learned baseline |
| F-002 | Medium | Completion report/QA: failed variants have 'no file kept'; registry local_path blank | File data/controlled_variants/media/P87190658/CV-P87190658-V10.mp4 (3091227 bytes) exists on disk for failed variant ['CV-P87190658-V10']; 1,132 files on disk vs 1,131 passed; the file is also listed  |
| F-003 | Medium | source_registry/candidates/policy: FIVR annotation has ND/DS/CS (IS implicit) | annotation.json holds IS labels: {'ND': 1327, 'DS': 5839, 'CS': 1855, 'IS': 3543}; 3543 edges have normalized_relation_type 'IS' (not normalised) |
| F-004 | Medium | edges reference existing media | 61 RW-06 edges point to candidate ids absent from youtube_ids.txt (59 such ids in the source); no master rows exist for them |
| F-005 | Medium | policy/dictionary: FVC labels are fake or real | FVC files contain label values {'fake': 2920, 'real': 2164, 'uncertain': 340, 'debunked': 89, 'parody': 66}; 495 master rows normalised to not_assessed |
| F-006 | Medium | Dataset documented as FVC.csv + FVC_dup.csv only | Archive also contains FVC_text_queries.csv: event titles in English, French, Spanish, Russian, Arabic; header has 8 fields but rows have up to 21 (ragged); no ORVEX code reads it |
| F-007 | Medium | inventory/registry list ANAKIN media as trimmed+edited | 89 mask zips (128979239 bytes) are on disk, absent from the media master, registry, features and evidence, not opened by any code, integrity unchecked |
| F-008 | Medium | Splits: all descendants/near-duplicates of a source in one split | 9 near-duplicate original pairs (>=45% frame match) lie in different splits, e.g. [['RW-CMN-P145557116', 'RW-ANK-71d1y7-T', 0.54, 'val', 'train'], ['RW-ANK-95w389-T', 'RW-ANK-72y089-T', 0.71, 'train', |
| F-009 | Medium | Negative pairs are 'unrelated' | 952 negatives; same-family: 0; touching duplicate records: 0; hard (same-theme) negatives by split: {'test': 36, 'train': 157, 'val': 29}; labelled uncertain |
| F-010 | Medium | Licence register | VCSL dataset licence not stated (code MIT only); ANAKIN Vimeo source rights unverified; 25 Public-domain Commons files lack a licence URL; 2 files have no author stated |
| F-011 | Medium | Reproducibility | 7 one-off scripts (patch_round2.py, patch_round3.py, patch_round4.py...) rewrote code and documents in place; no single runner documents the order; Gate-1 downloads were interactive (s1 only re-verifi |
| F-012 | Medium | Git provenance | No .git directory; .gitignore exists; no spec.md, phase.md or README.md; only the PDF states requirements |
| F-013 | Low | Clean working tree | Stray file 'nul' (0 bytes) in repository root |
| F-014 | Low | Published counts | Zenodo description claims {'fake': 3957, 'real': 2458}; files hold 2920 fake + 2164 real + others = 5579 rows; journal claim 5195 near-duplicates vs 5199 rows (5192 distinct URLs) |
| F-015 | Low | ANAKIN size claims | Official listing has 1042 edited files; metadata has 1023 rows; 19 files without metadata |
| F-016 | Low | VCSL pair/URL lists | pair files reference 4568 uuids absent from videos_url_uuid.csv (labels file: 0 missing) |
| F-017 | Low | Duplicate storage | 6023814 bytes of zip archives plus 12602227 bytes of extracted copies kept |
| F-018 | Low | Tables listed as integrated | DS-024 is read by no experiment; DS-018/026/027/028/029 are read downstream only by audit/tests; 0 of 259 ORVEX-added columns are referenced only by their producer or nowhere |
| F-019 | Low | Evidence per relationship | Native relations (298,645 edges) share dataset-level evidence ids (EV-FIVR, EV-VCSL ...) rather than one record each |
| F-020 | Info | Commons usable sources | 96 files; 55 usable; flags {'too_long(>120s)': 25, 'no_audio': 17, 'too_short(<8s)': 8, 'duplicate': 4, 'non_real_world_synthetic_or_cgi': 4, 'mostly_black': 1, 'decode_errors': 1}; 1 unreadable origi |
| F-021 | Info | COVID timeline | 2236 derived tweet times fall outside the stated Nov 2019-Jun 2020 window and are flagged; publish timestamps range ['2015-02-03 0:00:00', '2020-06-30 0:00:00'] |
| F-022 | Info | Referential integrity | All checked links resolve except [['edges.media_b_id -> master/variants', 61]] |
| F-023 | Info | Documentation numbers vs data | 8 of 9 automated claim checks matched; unmatched/unchecked: ['group examples'] |
| F-024 | Info | Duplicate artifact name | docs/datasets/necessity_audit/dataset_inventory.csv (earlier, 40 rows of different scope) and docs/datasets/repository_audit/dataset_inventory.csv coexist |

## Evidence distinctions
| claim | supported by |
|---|---|
| visual/audio similarity | dHash/audio fingerprints only (weak for crop/mirror) |
| same-event | FIVR DS/CS/IS metadata only |
| candidate derivation | none stored (no model) |
| confirmed derivation | controlled variants + ANAKIN |
| transformation identification | controlled (14 types) + ANAKIN (5 types) |
| misinformation | FVC fake/real/uncertain/debunked/parody labels (media absent) |
| AI-generated | none |
| coordination/campaign | NOT supported (0 sharer accounts) |

Baseline (non-learned dHash): test ROC-AUC 0.8307; detection by transformation: audio_mute 0.976, audio_noise_mix 1.0, audio_replace 0.964, caption_burn_in 0.982, crop_center 0.036, mirror_color_shift 0.143, recompress_low 0.986, reencode_hq 0.964, reupload_sim 0.857, speed_change 1.0, trim_head 0.745, trim_middle 0.673, trim_tail 0.8, watermark_overlay 0.988. No learned-model results exist.