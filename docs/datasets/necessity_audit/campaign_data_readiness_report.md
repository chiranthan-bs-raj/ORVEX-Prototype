# Campaign-Data Readiness Report

Generated 2026-10-26T18:48:52Z.

## Evidence layers (kept separate)
| layer | state | note |
|---|---|---|
| E1 media similarity | available (hash features, native FIVR/VCSL/FVC relations) | never proves sharing or coordination |
| sharing / reposting evidence | partial: FVC cascades (order only); RW-31 share-reference post ids | no sharer identity |
| account + timestamp observations | very partial (see below) | needed per post: who, when, where |
| coordination evidence | NONE | requires independent multi-account timing/behaviour data over a stated baseline |

## What RW-31 (COVID misinformation videos, Zenodo 4557828) actually provides
| field | count | caveat |
|---|---|---|
| video records | 8122 | all metadata_only; media not provided |
| publish timestamps | 881 | timezone unstated; precision `second_timezone_unstated` |
| channel ids | 935 | YouTube channel of the video (publisher), not sharers |
| platform removal timestamps | 420 | when YouTube removed the video, per authors |
| Twitter share-reference post ids | 257467 | ids only; **0** have a sharer account |
| ...with time derived from tweet-id snowflake | 257326 | 2236 fall outside the dataset's stated Nov 2019-Jun 2020 window -> flagged unverified |
| Facebook share-reference post ids | 83222 | id only: no URL, account or time |
| posts with sharer account | 0 | none |

## Verdict
**Campaign detection (Module 7) stays BLOCKED.** The data shows that many posts shared the same removed videos and *when* those posts existed (derived), but not *who* shared them, so no account-level coordination evidence exists. Nothing was simulated.

## What is needed to unblock (external access, not downloadable now)
- Twitter/X Information Operations archive (application + agreement), TikTok Research API (institutional approval), or another platform source that gives per-post account id + time + media identity.
- Until then: keep `campaign_candidate_clusters` empty; Module 7 can be developed against the interface only.