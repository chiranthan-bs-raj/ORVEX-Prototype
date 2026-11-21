# Dataset Necessity and Redundancy Report

Decisions (from the verified audit): {'Useful and justified': 16, 'Essential': 12, 'Conditionally useful': 4, 'Underutilized': 2, 'Redundant': 2, 'Unused': 2, 'Required but unavailable': 1, 'Unsuitable for intended use': 1}. Nothing is deleted or modified by this report.

| id | dataset | class | unique value | retention | would change if |
|---|---|---|---|---|---|
| DS-001 | Wikimedia Commons CC/PD video originals | Essential | only source of rights-cleared real media for controlled variants and real-media evaluation; nothing else in the repository can replace it | Retain in working package | none |
| DS-002 | Commons source metadata (candidate records) | Essential | licence/attribution/provenance of every original | Retain | none |
| DS-003 | ANAKIN subset: trimmed + edited videos | Useful and justified | only real human-edit pairs; consumed by the baseline; not a variant source | Retain | if a learned model shows over-reliance, or Vimeo rights are disputed |
| DS-004 | ANAKIN subset: edit masks | Underutilized | masks could support manipulation localisation but no code reads them and they are untracked | Retain (archival/future); register in the master first | a localisation requirement is approved |
| DS-005 | ANAKIN metadata and official listing | Essential | labels for the ANAKIN pairs | Retain | none |
| DS-006 | InVID Fake Video Corpus 2018 (v3): URLs and labels | Conditionally useful | repost cascades with labels; media inaccessible; native text queries unused | Retain | lawful media access obtained |
| DS-007 | InVID Fake Video Corpus v2.0: URLs, labels, manipulation types | Conditionally useful | adds manipulation type/debunk URLs; 188 of 227 YouTube ids overlap DS-006 | Retain (extra native fields) | none |
| DS-008 | InVID Fake Video Corpus v1.0: URLs and annotations | Redundant | superseded by later versions; 49 of 59 ids overlap DS-006 | Retain only for provenance/duplicate mapping | none |
| DS-009 | FIVR-200K: YouTube ids, events, relation annotations | Conditionally useful | same-incident vs copy labels (hard negatives) once media accessible; IS labels unnormalised | Retain | media access |
| DS-010 | VCSL: video URLs, copied-segment labels, pair/split files | Conditionally useful | largest real partial-copy annotation set; media inaccessible; licence not stated | Retain (metadata) | media access + licence clarity |
| DS-011 | COVID-related misinformation videos and their spread (RW-31) | Useful and justified | only real spread timeline; insufficient for coordination | Retain | authorised account data obtained |
| DS-012 | Official record snapshots (Zenodo API, GitHub READMEs/licence) | Essential | provenance evidence for licences/checksums | Retain | none |
| DS-013 | Controlled variant media | Essential | ground-truth derivations; 12.5 GB; regenerable from DS-001 + scripts but costly | Retain | none |
| DS-014 | Controlled variant registry | Essential | lineage ground truth | Retain | none |
| DS-015 | Transformation run log | Useful and justified | reproducibility log | Retain | none |
| DS-016 | Real-world media master | Essential | identity/provenance master | Retain | none |
| DS-017 | Media relationship edges | Essential | relationship ground truth/graph edges | Retain; fix noted defects first | none |
| DS-018 | Platform observations | Useful and justified | timeline evidence | Retain | none |
| DS-019 | Evidence ledger | Useful and justified | evidence traceability | Retain | none |
| DS-020 | Feature manifest | Useful and justified | feature index | Retain | none |
| DS-021 | Visual 24-frame dHash features | Essential | baseline and candidate-retrieval fingerprint | Retain | none |
| DS-022 | Audio fingerprint features | Useful and justified | audio replacement evidence | Retain | none |
| DS-023 | Training pairs | Essential | evaluation/training pairs | Retain | none |
| DS-024 | Group examples (5-6 videos) | Underutilized | group data exists but no code consumes it | Retain | group-level experiment planned |
| DS-025 | Split manifest (split-v2) | Essential | leakage control | Retain | none |
| DS-026 | Duplicate map | Useful and justified | duplicate handling | Retain | none |
| DS-027 | Source registry | Useful and justified | census and decisions | Retain | none |
| DS-028 | Download/access attempt log | Useful and justified | access audit trail | Retain | none |
| DS-029 | Campaign candidate clusters | Required but unavailable | Module 7 evidence cannot be obtained from current data | Keep empty | authorised data obtained |
| DS-030 | Experiment registry | Useful and justified | experiment results registry | Retain | none |
| DS-031 | Manifests (checksums, crosswalk, attribution, selection plan, storage budget, protocol) | Useful and justified | checksums/attribution/protocol | Retain | none |
| DS-032 | Build intermediates and run logs | Redundant | resume checkpoints and caches; regenerable; not in checksum manifest | Retain checkpoints; caches may be pruned with approval | none |
| DS-033 | Acceptance and QA report artefacts | Useful and justified | validation evidence snapshots | Retain | none |
| DS-034 | Dataset documentation corpus (docs/datasets, incl. necessity_audit) | Useful and justified | documentation (some hand-edited numbers can go stale) | Retain | none |
| DS-035 | ORVEX_Literature corpus (35 PDFs, text, review workbook) | Unused | literature corpus; not consumed by data pipeline | Retain for research context (outside budget) | none |
| DS-036 | ORVEX_Complete_Project_Specification.pdf | Essential | authoritative requirements | Retain | none |
| DS-037 | LOOP-MIND novelty verification workbook | Unsuitable for intended use | different project's workbook | Retain only if the user wants it; unrelated to ORVEX | none |
| DS-038 | Tools: portable FFmpeg 9.0.2 | Useful and justified | software required to reproduce media steps | Retain (outside dataset budget) | none |
| DS-039 | Pipeline code and tests | Useful and justified | reproducibility code; patch scripts are one-off | Retain | none |
| DS-040 | Root-level miscellaneous files | Unused | root misc: .gitignore (used) and stray 'nul' (accidental) | Remove 'nul' only with approval | none |

Overlap: DS-008 (FVC v1.0) overlaps DS-006 on 49 of 59 ids and DS-007 on 56 of 59 (redundant, kept for provenance); DS-007 shares 188 of 227 ids with DS-006. More data is not recommended: the existing collection suffices to build and evaluate relationship learning (see gaps report).