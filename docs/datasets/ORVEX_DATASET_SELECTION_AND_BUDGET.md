# ORVEX Dataset Selection and Storage Budget

Generated 2026-10-26T18:48:15Z. Size definition: **decimal bytes under `<repo>\data\`** (media, variants, features, tables, manifests, logs, build/temp). Installed tools (FFmpeg, ~0.4 GB) are outside `data/` and reported separately.

## Budget plan (set before large downloads)
| category | allocation |
|---|---|
| real-world raw metadata | 0.4 GB |
| Commons real media | 3.0 GB |
| ANAKIN subset (trimmed+edited+masks) | 3.0 GB (planned 2.52 GB from API sizes) |
| controlled variants | 14.0 GB |
| features + tables + logs | 1.0 GB |
| total allocation | 21.4 GB; hard cap 30 GB, target <=27 GB, stop 29 GB |

Selection rules: ANAKIN — deterministic sort by sha256('orvex-anakin-v1'+id), first 50 per manipulation type, only while cumulative planned bytes <= 3 GB (full-length videos, 44.6 GB, excluded). Commons — 28 themed queries, <=4 new files per query, files 0.3-45 MB, licence gate, stem de-duplication.

## Measured sizes
| category | measured |
|---|---|
| real-world raw metadata/annotations | 66,260,147 B (0.066 GB / 0.062 GiB) |
| real-world media (Commons) | 1,687,143,702 B (1.687 GB / 1.571 GiB) |
| real-world media (ANAKIN subset) | 2,521,092,381 B (2.521 GB / 2.348 GiB) |
| controlled variants (media) | 12,500,690,021 B (12.501 GB / 11.642 GiB) |
| derived tables | 419,190,940 B (0.419 GB / 0.390 GiB) |
| derived features | 1,350,267 B (0.001 GB / 0.001 GiB) |
| derived splits | 72,085 B (0.000 GB / 0.000 GiB) |
| manifests/logs | 45,908,858 B (0.046 GB / 0.043 GiB) |
| reports | 32,207 B (0.000 GB / 0.000 GiB) |
| temp/build (donor wav etc.) | 3,666,750 B (0.004 GB / 0.003 GiB) |
| **TOTAL dataset payload** | 17,241,740,608 B (17.242 GB / 16.058 GiB) |
| cap / target | 30 GB / 27 GB |
| cap respected | YES |

## Source-by-source decision
| id | dataset | decision | reason | limitations |
|---|---|---|---|---|
| RW-01 | Wikimedia Commons CC/PD video pool (ORVEX selection) | included_selected_subset | Only surveyed source with real media bytes whose per-file licence permits storage, transformation and redistribution with attribution; used as source pool for controlled variants. | Not a benchmark; no native relationship labels; themes chosen by ORVEX queries; per-file licence re-check needed before public release; Commons 'Public domain' can be jurisdiction-specific |
| RW-02 | ANAKIN: manipulated videos and mask annotations (incl. VideoSham edited videos) | included_selected_subset | Only open set with real source->edited video pairs and edit types. Stratified subset of trimmed+edited(+masks) downloaded; 'full' videos (44.6 GB) excluded_over_budget. Used for native edit relations/evaluation, NOT as source for controlled variants (conservative: underlying Vimeo rights). | Editors were commissioned (not wild reposts); Vimeo source rights unverified; subset only |
| RW-03 | InVID Fake Video Corpus 2018 (v3) | included_metadata_only | Real-world repost cascades with fake/real labels; media bytes are not provided (authors do not own rights) so records stay metadata_only; no third-party downloader used. | URLs may be dead; no timestamps in the CSV (order within cascade only); label 'fake' means debunked, not AI-generated |
| RW-04 | InVID Fake Video Corpus v2.0 | included_metadata_only | Adds native fields not in 2018 CSV (type of manipulation, debunk URLs, tamper timestamp); overlapping records are mapped, not double counted. | Overlaps other versions; URLs-only |
| RW-05 | InVID Fake Video Corpus v1.0 | excluded_duplicate_version | Earlier version (59 entries) superseded by later versions; records kept in media master only to map duplicates (not counted twice). | Authors state it is not meant for quantitative evaluation |
| RW-06 | InVID FIVR-200K (Fine-grained Incident Video Retrieval) | included_metadata_only | Native related-scene vs copy labels (needed to separate same-event from derivation); 225,960 YouTube ids + 100 query annotations. Media bytes not provided. | Same-incident labels are NOT derivation labels; videos not downloaded |
| RW-07 | VCSL (Video Copy Segment Localization) | included_metadata_only | Best real segment-level copy annotations; media rights not cleared, dataset licence not stated, so only annotations and URLs are used; no third-party downloader used. | Some links dead; segment units assumed seconds (1 fps sampling per README); media rights unresolved |
| RW-08 | VCDB (Video Copy Detection Benchmark) | research_lead_unverified | Official Fudan page failed TLS certificate validation (not bypassed); the suggested GitHub lead (ccny-zhangx/VCDB) returned 404 on 2026-10-26. | Not accessible this session |
| RW-09 | A corpus of debunked and verified user-generated videos (journal paper record) | excluded_duplicate_version | Describes the same corpus as RW-03; contains only the article PDF (380 videos, 5,195 near-duplicates). |  |
| RW-10 | WildDeepfake | research_lead_unverified | Optional authenticity benchmark only; terms and provenance not verified; must not substitute for a lineage dataset. |  |
| RW-11 | DFDC (DeepFake Detection Challenge) dataset | excluded_not_real_world_for_scope | Research-generated manipulation dataset; excluded from the naturally-circulating collection per project rule. |  |
| RW-12 | FaceForensics++ | excluded_not_real_world_for_scope | Research-created fakes; not naturally circulating. |  |
| RW-13 | Celeb-DF / Celeb-DF++ | excluded_not_real_world_for_scope | Research-created deepfakes. |  |
| RW-14 | FakeAVCeleb | excluded_not_real_world_for_scope | Contains AI-generated audio/video; violates the no-synthetic-audio rule. |  |
| RW-15 | AV-Deepfake1M | excluded_not_real_world_for_scope | Synthetic content. |  |
| RW-16 | Deepfake-Eval-2024 | research_lead_unverified | Authenticity benchmark, optional; access not verified. |  |
| RW-17 | VSC 2022/2023 Video Similarity Challenge dataset | research_lead_unverified | Terms/access not verified; audio removed so unusable for audio evidence. |  |
| RW-18 | YFCC100M (video subset) | legal_review_required | Requires a signed Webscope agreement; current distribution route not verified. |  |
| RW-19 | CC_WEB_VIDEO | research_lead_unverified | Official page not reached. |  |
| RW-20 | SVD (Short Video Dataset) | research_lead_unverified | Terms/access not verified. |  |
| RW-21 | NIST Nimble / Media Forensics Challenge data | research_lead_unverified | Registration route not verified; mostly images. |  |
| RW-22 | Twitter/X Information Operations archive | excluded_inaccessible | Needs institutional application; current availability unverified. Campaign table left empty. |  |
| RW-23 | Pushshift Telegram dataset | research_lead_unverified | Availability and terms not verified. |  |
| RW-24 | TikTok Research API (2024 US election videos, Luceri et al.) | excluded_inaccessible | Requires institutional API approval. |  |
| RW-25 | VideoSham | excluded_duplicate_version | Its 352 edited videos are already part of ANAKIN (RW-02). |  |
| RW-26 | HMDB51 | excluded_license | Underlying movie footage rights not cleared; no relationship labels. |  |
| RW-27 | UCF101 | excluded_license | Licence unresolved; no relationship labels. |  |
| RW-28 | Kinetics | excluded_license | Licence conflict; links only; no relationship labels. |  |
| RW-29 | NewsCLIPpings | excluded_not_real_world_for_scope | Images, with algorithmically constructed mismatches; not video lineage. |  |
| RW-30 | Datasets for coordinated behaviour (Pacheco 2021, Nizzoli 2021, Indiana coordinated-reply datasheet) | research_lead_unverified | Not verified; Twitter-era data; no video lineage. |  |
| RW-31 | A dataset of Covid-related misinformation videos and their spread on social media | included_metadata_only | Real post-level spread evidence (257k Twitter post ids, 81k Facebook post ids, platform removal times) for the source/post timeline; sharer accounts are NOT provided, so it cannot support coordination claims. | no sharer accounts; publish/removal timestamps present only for part of the videos; Twitter time derived from the post-id snowflake; videos not provided |

## Portfolio coverage of the required capability areas
| area | datasets | coverage / caveat |
|---|---|---|
| (a) video-copy / partial-segment matching | RW-07 VCSL (metadata), controlled trims T03-T05 (RW-01) | annotations + controlled ground truth; native media not local |
| (b) near-duplicate discovery vs same-event | RW-06 FIVR-200K (ND/DS/CS), controlled variants | metadata only for FIVR; same-incident labels never used as copy labels |
| (c) naturally occurring manipulated/misleading video + evidence | RW-03/04 FVC, RW-31 COVID removed videos, RW-02 ANAKIN (human edits) | FVC/COVID metadata only; ANAKIN has media (commissioned edits) |
| (d) repost / cascade / timeline evidence | RW-03 FVC cascades (order), RW-31 (publish, removal, 257k tweet share times, 81k Facebook post ids) | no sharer accounts |
| (e) authorised real media for controlled variants | RW-01 Commons (55 usable sources) | per-file CC/PD licences |
| (f) campaign-related metadata | RW-31 (video-level spread), RW-01 uploads | INSUFFICIENT for coordination claims (no multi-account time evidence); Twitter IO / TikTok API inaccessible |

## Cap by dataset and by variant type
Per-dataset allocations are in the budget table above. Variants have one total cap (14 GB, enforced by the generator guard before every encode) and no per-type cap; measured per-type sizes are in `ORVEX_DATASET_QA_REPORT.md` and `data/manifests/storage_budget.csv`.

Machine-readable plan: `data/manifests/selection_plan.json`; storage log: `data/manifests/storage_budget.csv`; checksums: `data/manifests/checksums.sha256`; ID crosswalk: `data/manifests/native_id_crosswalk.csv`; attribution: `ORVEX_ATTRIBUTION.md`; protocol: `ORVEX_EVALUATION_PROTOCOL.md`.