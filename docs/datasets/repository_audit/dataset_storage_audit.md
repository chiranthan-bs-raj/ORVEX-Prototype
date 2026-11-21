# Storage and Capacity Report

Audit date 2026-10-27. Method: every file under <repo> walked (symlinks: 0); this audit's own output folder and __pycache__ excluded. decimal bytes of all files under <repo>\data; excludes tools/, ORVEX_Literature/, docs/, scripts/, tests/ and model weights (none exist); no symlinks followed (none found).

- **Dataset payload (data/): 17241741313 bytes = 17.242 GB = 16.058 GiB. Limit 30 GB: remaining 12.758 GB.**
- Whole repository (incl. tools, literature, docs, code): 17927214201 bytes = 17.927 GB.
- Raw media: Commons 1.687 GB; ANAKIN 2.521 GB; controlled variants 12.501 GB.
- Zip archives 6023814 bytes + extracted copies 12602227 bytes (duplicate storage); donor WAV cache 78 bytes; model weights/indexes: none exist; external storage: none (URL-only datasets occupy no media storage).

## By top-level directory
| directory | size |
|---|---|
| data | 17.242 GB |
| tools | 0.444 GB |
| ORVEX_Literature | 0.240 GB |
| docs | 0.000 GB |
| scripts | 0.000 GB |
| ORVEX_Complete_Project_Specification.pdf | 0.000 GB |
| LOOP-MIND_Novelty_Independent_Verification_2_4_5.xlsx | 0.000 GB |
| tests | 0.000 GB |
| .gitignore | 0.000 GB |
| nul | 0.000 GB |

## By dataset audit ID
| id | dataset | size |
|---|---|---|
| DS-001 | Wikimedia Commons CC/PD video originals | 1687143702 bytes (1.687 GB) |
| DS-002 | Commons source metadata (candidate records) | 139714 bytes (0.000 GB) |
| DS-003 | ANAKIN subset: trimmed + edited videos | 2392113142 bytes (2.392 GB) |
| DS-004 | ANAKIN subset: edit masks | 128979239 bytes (0.129 GB) |
| DS-005 | ANAKIN metadata and official listing | 1033853 bytes (0.001 GB) |
| DS-006 | InVID Fake Video Corpus 2018 (v3): URLs and labels | 650024 bytes (0.001 GB) |
| DS-007 | InVID Fake Video Corpus v2.0: URLs, labels, manipulation types | 74758 bytes (0.000 GB) |
| DS-008 | InVID Fake Video Corpus v1.0: URLs and annotations | 27904 bytes (0.000 GB) |
| DS-009 | FIVR-200K: YouTube ids, events, relation annotations | 17873355 bytes (0.018 GB) |
| DS-010 | VCSL: video URLs, copied-segment labels, pair/split files | 42201384 bytes (0.042 GB) |
| DS-011 | COVID-related misinformation videos and their spread (RW-31) | 4198098 bytes (0.004 GB) |
| DS-012 | Official record snapshots (Zenodo API, GitHub READMEs/licence) | 61057 bytes (0.000 GB) |
| DS-013 | Controlled variant media | 12500690021 bytes (12.501 GB) |
| DS-014 | Controlled variant registry | 1094515 bytes (0.001 GB) |
| DS-015 | Transformation run log | 954337 bytes (0.001 GB) |
| DS-016 | Real-world media master | 148756771 bytes (0.149 GB) |
| DS-017 | Media relationship edges | 149867390 bytes (0.150 GB) |
| DS-018 | Platform observations | 110755040 bytes (0.111 GB) |
| DS-019 | Evidence ledger | 670524 bytes (0.001 GB) |
| DS-020 | Feature manifest | 2252894 bytes (0.002 GB) |
| DS-021 | Visual 24-frame dHash features | 1133311 bytes (0.001 GB) |
| DS-022 | Audio fingerprint features | 216956 bytes (0.000 GB) |
| DS-023 | Training pairs | 4719493 bytes (0.005 GB) |
| DS-024 | Group examples (5-6 videos) | 37349 bytes (0.000 GB) |
| DS-025 | Split manifest (split-v2) | 72085 bytes (0.000 GB) |
| DS-026 | Duplicate map | 78429 bytes (0.000 GB) |
| DS-027 | Source registry | 23226 bytes (0.000 GB) |
| DS-028 | Download/access attempt log | 215252 bytes (0.000 GB) |
| DS-029 | Campaign candidate clusters | 219 bytes (0.000 GB) |
| DS-030 | Experiment registry | 3979 bytes (0.000 GB) |
| DS-031 | Manifests (checksums, crosswalk, attribution, selection plan, storage budget, protocol) | 41965067 bytes (0.042 GB) |
| DS-032 | Build intermediates and run logs | 3706024 bytes (0.004 GB) |
| DS-033 | Acceptance and QA report artefacts | 32201 bytes (0.000 GB) |
| DS-034 | Dataset documentation corpus (docs/datasets, incl. necessity_audit) | 412378 bytes (0.000 GB) |
| DS-035 | ORVEX_Literature corpus (35 PDFs, text, review workbook) | 240494329 bytes (0.240 GB) |
| DS-036 | ORVEX_Complete_Project_Specification.pdf | 251692 bytes (0.000 GB) |
| DS-037 | LOOP-MIND novelty verification workbook | 20779 bytes (0.000 GB) |
| DS-038 | Tools: portable FFmpeg 9.0.2 | 443989875 bytes (0.444 GB) |
| DS-039 | Pipeline code and tests | 303686 bytes (0.000 GB) |
| DS-040 | Root-level miscellaneous files | 149 bytes (0.000 GB) |

Unaccounted storage: files not mapped to a dataset: 2 (.gitignore and the stray 'nul' file). Potential savings from demonstrably redundant artefacts: extracted copies of archives (12602227 bytes) and the donor cache (negligible); the one failed variant file (3091227 bytes). No deletion was performed.
- Compliance: WITHIN the 30 GB budget.