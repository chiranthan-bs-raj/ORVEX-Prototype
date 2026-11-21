# Findings, Inconsistencies and Remediation Plan

Audit date 2026-10-27. 24 findings ({'Medium': 11, 'Low': 7, 'Info': 5, 'High': 1}). Evidence is from files inspected in this audit. Nothing was changed.

## Priority order of work (no data was modified by this audit)
1. Qualify every PASS as 'data support only' (F-001). 2. Resolve data defects that change labels/relations: FIVR IS normalisation and dangling edges, FVC label mapping (F-003..F-005). 3. Review cross-split near-duplicates and failed-variant file (F-002, F-008). 4. Register or drop ANAKIN masks and FVC text queries (F-006, F-007). 5. Legal/licence review (F-010). 6. Reproducibility and Git (F-011, F-012).

### F-001 [High] Requirement matrices list PASS for capabilities (graph, manipulation analysis, reporting)
- **Dataset:** all
- **Evidence:** No application/model code, notebooks, checkpoints or databases exist (no package.json/pyproject/backend/frontend; 0 model artifacts); only data pipeline scripts s1-s9 and one non-learned baseline
- **Likely explanation:** PASS statuses were defined as 'data supports the capability'
- **Effect on ORVEX:** Readers may assume ORVEX modules exist; runtime and training use of every dataset is zero
- **Recommended correction:** Keep every PASS qualified as 'data support only' in all summaries
- **Fixable without changing data:** Yes (wording)
- **Separate authorization needed:** No

### F-002 [Medium] Completion report/QA: failed variants have 'no file kept'; registry local_path blank
- **Dataset:** DS-013/DS-014
- **Evidence:** File data/controlled_variants/media/P87190658/CV-P87190658-V10.mp4 (3091227 bytes) exists on disk for failed variant ['CV-P87190658-V10']; 1,132 files on disk vs 1,131 passed; the file is also listed in checksums.sha256
- **Likely explanation:** output kept when validation failed (duration check) and the cleanup/K26 check only inspected the registry field
- **Effect on ORVEX:** A failed audio_mute variant could be mistaken for a valid variant; payload counts differ by one
- **Recommended correction:** Delete the file or register it as failed with its path
- **Fixable without changing data:** No (file system change)
- **Separate authorization needed:** Yes

### F-003 [Medium] source_registry/candidates/policy: FIVR annotation has ND/DS/CS (IS implicit)
- **Dataset:** DS-009/DS-017
- **Evidence:** annotation.json holds IS labels: {'ND': 1327, 'DS': 5839, 'CS': 1855, 'IS': 3543}; 3543 edges have normalized_relation_type 'IS' (not normalised)
- **Likely explanation:** s3_normalize.py:fivr_rows only mapped three labels
- **Effect on ORVEX:** 3,543 same-incident relations are not interpretable as 'same incident, not copy'
- **Recommended correction:** Map IS to a same-incident relation and correct the registry/policy text
- **Fixable without changing data:** Docs yes; table needs regeneration
- **Separate authorization needed:** Yes for table changes

### F-004 [Medium] edges reference existing media
- **Dataset:** DS-009/DS-017
- **Evidence:** 61 RW-06 edges point to candidate ids absent from youtube_ids.txt (59 such ids in the source); no master rows exist for them
- **Likely explanation:** inconsistency inside the upstream release
- **Effect on ORVEX:** Edges with no resolvable endpoint
- **Recommended correction:** Add placeholder metadata-only master rows or flag edges
- **Fixable without changing data:** No
- **Separate authorization needed:** Yes

### F-005 [Medium] policy/dictionary: FVC labels are fake or real
- **Dataset:** DS-006/DS-016
- **Evidence:** FVC files contain label values {'fake': 2920, 'real': 2164, 'uncertain': 340, 'debunked': 89, 'parody': 66}; 495 master rows normalised to not_assessed
- **Likely explanation:** normaliser maps only fake/real
- **Effect on ORVEX:** 89 'debunked' and 66 'parody' and 340 'uncertain' rows lose their misleading-status meaning
- **Recommended correction:** Extend the mapping (debunked->debunked_misleading; keep parody/uncertain explicit) and document
- **Fixable without changing data:** Docs yes; table regeneration
- **Separate authorization needed:** Yes for table changes

### F-006 [Medium] Dataset documented as FVC.csv + FVC_dup.csv only
- **Dataset:** DS-006
- **Evidence:** Archive also contains FVC_text_queries.csv: event titles in English, French, Spanish, Russian, Arabic; header has 8 fields but rows have up to 21 (ragged); no ORVEX code reads it
- **Likely explanation:** never inspected during collection
- **Effect on ORVEX:** Native multilingual text (useful for caption/text modules) is unused
- **Recommended correction:** Register it in the master/dictionary or document why excluded; handle ragged rows
- **Fixable without changing data:** Yes (documentation); ingestion needs authorization
- **Separate authorization needed:** No for documentation

### F-007 [Medium] inventory/registry list ANAKIN media as trimmed+edited
- **Dataset:** DS-004
- **Evidence:** 89 mask zips (128979239 bytes) are on disk, absent from the media master, registry, features and evidence, not opened by any code, integrity unchecked
- **Likely explanation:** downloaded by s2_collect_media.py for has-masks pairs but never integrated
- **Effect on ORVEX:** Untracked storage; localisation evidence unused
- **Recommended correction:** Register or remove; verify zip integrity read-only
- **Fixable without changing data:** Docs yes
- **Separate authorization needed:** Yes for deletion/registration

### F-008 [Medium] Splits: all descendants/near-duplicates of a source in one split
- **Dataset:** DS-023/DS-025
- **Evidence:** 9 near-duplicate original pairs (>=45% frame match) lie in different splits, e.g. [['RW-CMN-P145557116', 'RW-ANK-71d1y7-T', 0.54, 'val', 'train'], ['RW-ANK-95w389-T', 'RW-ANK-72y089-T', 0.71, 'train', 'test']]; ANAKIN selected clips have distinct URLs (250/250), so these are look-alike review candidates
- **Likely explanation:** dHash look-alikes between different ANAKIN videos (possible common footage); not proven duplicates
- **Effect on ORVEX:** Possible optimistic test metrics for ANAKIN pairs
- **Recommended correction:** Review the 9 pairs; merge families if confirmed
- **Fixable without changing data:** Review yes; re-split no
- **Separate authorization needed:** Yes (changes split_version)

### F-009 [Medium] Negative pairs are 'unrelated'
- **Dataset:** DS-023
- **Evidence:** 952 negatives; same-family: 0; touching duplicate records: 0; hard (same-theme) negatives by split: {'test': 36, 'train': 157, 'val': 29}; labelled uncertain
- **Likely explanation:** negatives are sampled by rule; same theme is not proof of independence
- **Effect on ORVEX:** Hard negatives may include same-event pairs
- **Recommended correction:** Keep uncertain label; human-review a sample
- **Fixable without changing data:** Yes
- **Separate authorization needed:** No

### F-010 [Medium] Licence register
- **Dataset:** DS-010/DS-003/DS-001
- **Evidence:** VCSL dataset licence not stated (code MIT only); ANAKIN Vimeo source rights unverified; 25 Public-domain Commons files lack a licence URL; 2 files have no author stated
- **Likely explanation:** upstream metadata gaps
- **Effect on ORVEX:** Legal status of redistribution/derivatives unresolved for some sources
- **Recommended correction:** Legal/policy review before release
- **Fixable without changing data:** Yes
- **Separate authorization needed:** Yes

### F-011 [Medium] Reproducibility
- **Dataset:** repository
- **Evidence:** 7 one-off scripts (patch_round2.py, patch_round3.py, patch_round4.py...) rewrote code and documents in place; no single runner documents the order; Gate-1 downloads were interactive (s1 only re-verifies)
- **Likely explanation:** iterative development
- **Effect on ORVEX:** Re-running from scratch may require manual reconstruction
- **Recommended correction:** Add a documented runner and archive patch history
- **Fixable without changing data:** Yes (new docs)
- **Separate authorization needed:** Yes (code changes)

### F-012 [Medium] Git provenance
- **Dataset:** repository
- **Evidence:** No .git directory; .gitignore exists; no spec.md, phase.md or README.md; only the PDF states requirements
- **Likely explanation:** project not under version control
- **Effect on ORVEX:** No commit history to verify provenance or modification
- **Recommended correction:** Initialise Git or document the lack
- **Fixable without changing data:** Yes
- **Separate authorization needed:** Yes

### F-013 [Low] Clean working tree
- **Dataset:** repository
- **Evidence:** Stray file 'nul' (0 bytes) in repository root
- **Likely explanation:** accidental redirect (a shell command wrote to a file named nul)
- **Effect on ORVEX:** Clutter only
- **Recommended correction:** Remove with approval
- **Fixable without changing data:** No
- **Separate authorization needed:** Yes

### F-014 [Low] Published counts
- **Dataset:** DS-006
- **Evidence:** Zenodo description claims {'fake': 3957, 'real': 2458}; files hold 2920 fake + 2164 real + others = 5579 rows; journal claim 5195 near-duplicates vs 5199 rows (5192 distinct URLs)
- **Likely explanation:** different release/paper versions
- **Effect on ORVEX:** Counts quoted from papers cannot be used as file counts
- **Recommended correction:** Quote measured counts
- **Fixable without changing data:** Yes
- **Separate authorization needed:** No

### F-015 [Low] ANAKIN size claims
- **Dataset:** DS-005
- **Evidence:** Official listing has 1042 edited files; metadata has 1023 rows; 19 files without metadata
- **Likely explanation:** upstream mismatch
- **Effect on ORVEX:** None locally (subset selected from metadata rows)
- **Recommended correction:** Note in registry
- **Fixable without changing data:** Yes
- **Separate authorization needed:** No

### F-016 [Low] VCSL pair/URL lists
- **Dataset:** DS-010
- **Evidence:** pair files reference 4568 uuids absent from videos_url_uuid.csv (labels file: 0 missing)
- **Likely explanation:** upstream release inconsistency
- **Effect on ORVEX:** Some benchmark pairs cannot be resolved to URLs
- **Recommended correction:** Note in registry
- **Fixable without changing data:** Yes
- **Separate authorization needed:** No

### F-017 [Low] Duplicate storage
- **Dataset:** DS-012
- **Evidence:** 6023814 bytes of zip archives plus 12602227 bytes of extracted copies kept
- **Likely explanation:** archives kept for checksum provenance
- **Effect on ORVEX:** Minor
- **Recommended correction:** Keep or drop one copy with approval
- **Fixable without changing data:** No
- **Separate authorization needed:** Yes

### F-018 [Low] Tables listed as integrated
- **Dataset:** DS-024/DS-018/DS-026/DS-027/DS-028/DS-029
- **Evidence:** DS-024 is read by no experiment; DS-018/026/027/028/029 are read downstream only by audit/tests; 0 of 259 ORVEX-added columns are referenced only by their producer or nowhere
- **Likely explanation:** built ahead of the model phase
- **Effect on ORVEX:** Underutilised data
- **Recommended correction:** Keep; consume in future experiments
- **Fixable without changing data:** Yes
- **Separate authorization needed:** No

### F-019 [Low] Evidence per relationship
- **Dataset:** DS-019
- **Evidence:** Native relations (298,645 edges) share dataset-level evidence ids (EV-FIVR, EV-VCSL ...) rather than one record each
- **Likely explanation:** scale
- **Effect on ORVEX:** Evidence granularity is coarse
- **Recommended correction:** Document or add per-edge references
- **Fixable without changing data:** Yes
- **Separate authorization needed:** No

### F-020 [Info] Commons usable sources
- **Dataset:** DS-001
- **Evidence:** 96 files; 55 usable; flags {'too_long(>120s)': 25, 'no_audio': 17, 'too_short(<8s)': 8, 'duplicate': 4, 'non_real_world_synthetic_or_cgi': 4, 'mostly_black': 1, 'decode_errors': 1}; 1 unreadable original (duration 0) retained and excluded
- **Likely explanation:** QC by design
- **Effect on ORVEX:** none
- **Recommended correction:** none
- **Fixable without changing data:** Yes
- **Separate authorization needed:** No

### F-021 [Info] COVID timeline
- **Dataset:** DS-011
- **Evidence:** 2236 derived tweet times fall outside the stated Nov 2019-Jun 2020 window and are flagged; publish timestamps range ['2015-02-03 0:00:00', '2020-06-30 0:00:00']
- **Likely explanation:** videos can pre-date sharing; some ids may not be tweets
- **Effect on ORVEX:** Flagged, not hidden
- **Recommended correction:** none
- **Fixable without changing data:** Yes
- **Separate authorization needed:** No

### F-022 [Info] Referential integrity
- **Dataset:** all tables
- **Evidence:** All checked links resolve except [['edges.media_b_id -> master|variants', 61]]
- **Likely explanation:** see F-004
- **Effect on ORVEX:** see F-004
- **Recommended correction:** see F-004
- **Fixable without changing data:** Yes
- **Separate authorization needed:** No

### F-023 [Info] Documentation numbers vs data
- **Dataset:** docs
- **Evidence:** 8 of 9 automated claim checks matched; unmatched/unchecked: ['group examples']
- **Likely explanation:** n/a
- **Effect on ORVEX:** none
- **Recommended correction:** none
- **Fixable without changing data:** Yes
- **Separate authorization needed:** No

### F-024 [Info] Duplicate artifact name
- **Dataset:** docs
- **Evidence:** docs/datasets/necessity_audit/dataset_inventory.csv (earlier, 40 rows of different scope) and docs/datasets/repository_audit/dataset_inventory.csv coexist
- **Likely explanation:** two audits
- **Effect on ORVEX:** possible confusion
- **Recommended correction:** Treat this audit as authoritative
- **Fixable without changing data:** Yes
- **Separate authorization needed:** No
