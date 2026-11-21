# Data Quality and Split Audit

Audit date 2026-10-27. Counts are distinct on purpose: files discovered != readable != usable != consumed != used in an experiment.

## Media (independent ffprobe in this audit)
| component | files | readable | hours | min/median/max s | audio share | heights | unreadable |
|---|---|---|---|---|---|---|---|
| anakin_edited | 250 | 250 | 0.47 | 2.0/5.0/29.4 | 0.972 | {'720': 69, '360': 54, '540': 49, '1080': 25, '480': 18, '640': 9} | [] |
| anakin_trimmed | 250 | 250 | 0.47 | 2.0/5.0/59.2 | 0.976 | {'720': 72, '360': 60, '540': 52, '480': 18, '1080': 12, '640': 9} | [] |
| commons_originals | 96 | 95 | 13.46 | 0.0/41.2/36061.7 | 0.823 | {'1080': 31, '720': 15, '480': 11, '2160': 7, '360': 6, '1920': 5} | ['data/real_world/media/commons/RW-CMN-P89310222.webm'] |
| controlled_variants | 1132 | 1132 | 11.32 | 4.8/27.1/116.6 | 0.797 | {'1080': 252, '360': 246, '720': 100, '2160': 83, '576': 63, '864': 60} | [] |

Hash verification: 796 files re-hashed (all Commons + ANAKIN + 200 random variants); matches 796, mismatches 0; manifest lines 1883; on disk not in manifest 0; in manifest not on disk 0. Duplicate media files by hash: 0.

## Count ladder for the media datasets
| dataset | files discovered | readable | usable | consumed by a pipeline | in an experiment |
|---|---|---|---|---|---|
| DS-001 Commons | 96 | 95 | 55 | consumed by s3/s4/s5 (all 96 inspected; 55 used for variants) | baseline uses features of all local media |
| DS-003 ANAKIN trimmed+edited | 500 | 500 | 250 | consumed by s3 and s5 features | 250 edited_version pairs in baseline |
| DS-013 variants | 1132 | 1132 | 1131 passed / 673 trainable | consumed by s5 | baseline scored pairs from them |

Commons QC flags: {'too_long(>120s)': 25, 'no_audio': 17, 'too_short(<8s)': 8, 'duplicate': 4, 'non_real_world_synthetic_or_cgi': 4, 'mostly_black': 1, 'decode_errors': 1}; usable by theme: {'sports': 4, 'nature': 4, 'protest': 3, 'street': 3, 'traffic': 3, 'market': 3, 'animals': 3, 'music': 3, 'festival': 3, 'science': 3, 'transport': 3, 'workshop': 3, 'education': 3, 'ceremony': 3, 'news': 2, 'wildlife': 2, 'cooking': 2, 'city': 2, 'speech': 1, 'interview': 1, 'space': 1}; usable without audio: 11.

## Annotation completeness and native-source consistency
| source | measured | inconsistency |
|---|---|---|
| FVC 2018 | 5579 rows; labels {'fake': 2920, 'real': 2164, 'uncertain': 340, 'debunked': 89, 'parody': 66} | text-queries file ragged ({'rows': 380, 'header_fields': 8, 'max_fields': 21, 'ragged_rows': 62, 'read_by_orvex_code': False}) |
| FIVR-200K | ids 225960; labels {'ND': 1327, 'DS': 5839, 'CS': 1855, 'IS': 3543} | 59 candidate ids not in id list |
| VCSL | 9207 videos; 166146 labelled pairs; 278885 segments | pair files reference 4568 unknown uuids |
| ANAKIN | 1023 metadata rows; types {'swap': 272, 'splicing': 228, 'inpainting': 190, 'frame-level': 172, 'audio': 161} | listing 1042 files vs 1023 rows |
| COVID | 8122 videos; publish 881, channel 935, removal 420 | 18 duplicate URLs; sharer accounts 0 |

## Splits (split-v2)
- Families by dataset/split: {'test': {'RW-01': 7, 'RW-02': 36}, 'train': {'RW-01': 40, 'RW-02': 175}, 'val': {'RW-01': 8, 'RW-02': 39}}
- Pairs by split: {'train': 6878, 'excluded': 3731, 'test': 1721, 'val': 1329}; classes: {'audio_source_only_not_visual_derivation': {'excluded': 21, 'test': 0, 'train': 32, 'val': 2}, 'direct_derivation': {'excluded': 183, 'test': 143, 'train': 673, 'val': 132}, 'edited_version': {'excluded': 0, 'test': 36, 'train': 175, 'val': 39}, 'indirect_derivation': {'excluded': 0, 'test': 63, 'train': 360, 'val': 72}, 'same_family_other': {'excluded': 1281, 'test': 735, 'train': 3191, 'val': 620}, 'sibling_same_parent': {'excluded': 2056, 'test': 594, 'train': 1777, 'val': 332}, 'unrelated_distinct_source': {'excluded': 190, 'test': 150, 'train': 670, 'val': 132}}
- Variants by split: {'train': 826, 'val': 162, 'test': 143}; trainable variants: 673
- Hard/easy negatives by split: {'easy': {'test': 114, 'train': 513, 'val': 103}, 'hard': {'test': 36, 'train': 157, 'val': 29}}
- Independent leakage checks: cross-split pairs 0; variant/split mismatches 0; held-out lineage in train/val pairs 0; same-family negatives 0; negatives touching duplicate records 0.
- **Near-duplicate leakage candidates:** 15 original pairs of 305 compared have >=45% frame match; 9 of them cross splits (see finding F-008). They are review candidates, not proven duplicates.
- Split reproducible: yes (deterministic stride rule, seed in split_manifest); reflects deployment: partially (controlled variants and commissioned edits, not circulating media).

## Distinctions the data can and cannot make
| relationship | supported by |
|---|---|
| same source | controlled families (recorded) and ANAKIN pairs (source-annotated) |
| derived media | controlled variants (ground truth); ANAKIN edits (source-annotated) |
| same event | FIVR DS/CS/IS (metadata only) |
| same caption/transcript | caption variants only (ground-truth text); no transcripts |
| same campaign / coordinated activity | NOT supported by any dataset |

## Overlap between datasets (shared YouTube ids)
| a | b | ids a | ids b | shared |
|---|---|---|---|---|
| RW-03 | RW-04 | 3369 | 227 | 188 |
| RW-03 | RW-05 | 3369 | 59 | 49 |
| RW-03 | RW-06 | 3369 | 225960 | 112 |
| RW-04 | RW-05 | 227 | 59 | 56 |
| RW-04 | RW-06 | 227 | 225960 | 13 |