# Storage Budget Report

Generated 2026-10-26T18:48:52Z. Definition: decimal bytes of everything under `<repo>\data\` (media, variants, features, tables, manifests, logs, build/temp). FFmpeg (~0.4 GB) is outside `data/`.

| category | measured | within allocation |
|---|---|---|
| real-world raw metadata | 0.07 GB | yes |
| real-world media: Commons | 1.69 GB | yes |
| real-world media: ANAKIN subset | 2.52 GB | yes |
| controlled variants (media) | 12.50 GB | yes |
| derived tables | 0.42 GB | yes |
| derived features | 0.00 GB | yes |
| derived splits | 0.00 GB | yes |
| manifests/logs/build | 0.05 GB | yes |
| reports | 0.00 GB | yes |
| dataset payload (all of data/) | 17.24 GB | yes |
| largest recorded payload measurement | 17.24 GB | yes |

Headroom to the 30 GB cap: **12.76 GB**; to the 27 GB target: **9.76 GB**.

## Estimated cost of conditional additions (none executed)
| addition | estimated size | projected total |
|---|---|---|
| +25 Commons sources (originals + full variant set) | 6.13 GB | 23.37 GB |
| +40 Commons sources | 9.81 GB | 27.05 GB |
| visual+audio embeddings, ASR, OCR, dense hashes | < 0.5 GB | 17.74 GB |
| ANAKIN full-length videos (rejected) | 44.6 GB | exceeds cap |

The existing package fits comfortably; the only sizeable optional item is more Commons sources, and +25 sources stays well under the 27 GB target.