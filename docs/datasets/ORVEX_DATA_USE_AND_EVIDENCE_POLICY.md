# ORVEX Data-Use and Evidence Policy (Roadmap 10.4)

Version 1.0 — 2026-10-26. Authoritative for dataset work. It is a working policy, not legal advice; licence texts and platform terms change and must be re-verified before any public release or new source.
Every rule below is enforced either by a script/test (marked **[test]**) or by a documented manual step (marked **[manual]**).

## 1. Principles
1. **Real-world media only.** Every video that enters ORVEX comes from a documented real-world source (Layer A, `data/real_world/`). No AI-generated, synthetic, animated or game-engine footage; no synthetic people, voices or posts. **[test: all variant roots are real sources]**
2. **Created data derives only from Layer A.** Controlled variants, tables, features, pairs and splits (Layer B) carry lineage to their source records. **[test: lineage]**
3. **No generative AI in dataset creation.** Variants are produced by FFmpeg operations only (trim, crop, overlay, recompress, mirror, speed, audio swap/mix). Audio replacement uses audio from a *different real recording*; caption text is the title of a *different real record*; both origins are stored. Such items are *constructed experimental pairings*, never natural posts. **[test]**
4. **Physical separation.** Natural media: `data/real_world/media/`. Controlled variants: `data/controlled_variants/media/`. Tables: `data/derived/`. A variant is always tagged `media_origin=controlled_variant`. **[test]**
5. **Native data is never modified.** Source files stay as downloaded in `data/real_world/raw_metadata/`; normalised values sit beside native values in the master table. **[test: hashes]**
6. **Missing is missing.** Unknown values are null plus a `missingness_note`; nothing is invented to fill a column.

## 2. Source eligibility, rights and access
| Rule | Detail |
|---|---|
| Verified source | A dataset is used only after its official page/record or API was read. Otherwise it is `research_lead_unverified` and not downloaded. |
| Strict real-world scope | Research-created manipulation sets (DFDC, FaceForensics++, Celeb-DF, FakeAVCeleb, AV-Deepfake1M) are excluded from the natural collection (`excluded_not_real_world_for_scope`). |
| Licence gate for media | Only files with CC0, Public domain, CC BY or CC BY-SA licences (machine-readable per file) are stored and transformed. NC, ND, unknown or conflicting licences are rejected. |
| URL-only datasets | FVC (all versions), FIVR-200K and VCSL provide URLs/annotations because the authors do not hold the video rights. Records are `metadata_only`. No third-party downloader, login bypass, scraping or CAPTCHA/TLS bypass is used. |
| Conservative derivative use | A dataset whose card allows reuse but whose underlying footage rights are not verified (ANAKIN/Vimeo) is used for evaluation and native edit relations only — **not** as a source for controlled variants. |
| ShareAlike | A variant of a CC BY-SA original is a derivative and carries CC BY-SA if shared. A composite (audio/caption from another record) must satisfy the stricter licence. |
| Access log | Every attempt is in `download_access_attempt_log` with status, HTTP code and decision. Failures are recorded, not hidden; no hammering of hosts (3-4 workers, retries with back-off). |
| Secrets | No tokens, cookies or credentials are stored in data, logs or Git. |

## 3. Storage levels and permitted uses
| Item | Local storage | Processing | Sharing |
|---|---|---|---|
| Original real media (Commons) | yes, read-only, SHA-256 | yes | with attribution/licence per file |
| Original real media (ANAKIN subset) | yes | evaluation only | CC BY 4.0 per card, rights caveat |
| Metadata-only records (FVC/FIVR/VCSL) | yes (annotations) | yes | annotations only; URLs are public identifiers |
| Controlled variants | yes, separate folder | yes | **not** as free-standing realistic media of identifiable people; share manifests and scripts; each file embeds a metadata comment "ORVEX controlled variant … not authentic media" |
| Features and tables | yes | yes | yes (carry source licence/attribution columns) |
| Platform account data | only fields needed; accounts pseudonymised (`account_id_pseudonym`) | yes | no raw re-publication |
| Restricted datasets (agreement-based) | only after the agreement is accepted | within agreement | no redistribution |
- Retention: platform-derived personal data is kept for the project period, then deleted or irreversibly anonymised (change deliberately).
- Takedown/deletion: if a source file is removed or its licence changes, the original and every derived variant are removed and the changelog updated. **[manual]**
- Privacy: no inference of identity or sensitive attributes; account names are never used to characterise a person.
- Sensitive content (war, violence, disasters) is auto-flagged in QC keywords; a human reviews before any public use. Variants are internal research artefacts and are never posted to platforms.

## 4. Leakage and integrity rules **[test]**
1. Splits are by **source family** (one real original or one ANAKIN video id). All descendants, duplicates and pairs of a family share a split. From `split-v2`, Commons families are additionally grouped by search theme (a whole theme goes to one split) so that every split contains same-theme hard negatives and no theme straddles splits; this was introduced because `split-v1` left the test split with no hard negatives.
2. Exact and near duplicates are detected (SHA-256; 24-frame dHash, ≥45% frame match) and mapped in `duplicate_map`; the canonical record is kept, others are excluded from variants.
3. Unusable media are excluded with reasons in `qc_flags` (<8 s, >120 s, <240p, decode errors, mostly black, static, duplicate).
4. Transformations T11–T14 are **test-only unseen types**; variants whose lineage contains them are never `usable_for_training`, and their pairs are excluded unless the family is in `test`.
5. Negative pairs are drawn inside the same split from distinct records; hard negatives (same search theme) are labelled `uncertain` because shared theme is not proof of independence.
6. A frozen `split_version` is recorded; changing assignments creates a new version.

## 5. Evidence classes (never merged)
| Class | Meaning | Examples |
|---|---|---|
| E1 Media similarity | content looks/sounds alike | hash match, embedding similarity, FIVR DS/CS/IS relations |
| E2 Derivation/lineage | one item was made from another | controlled transformation log; ANAKIN trimmed→edited; explicit source lineage |
| E3 Coordination signals | accounts behave in a coordinated way | synchronised posting, repeated cross-posting with independent account/time evidence |
- E1 never proves E2. Same incident ≠ copy. A repost is not a parent-child edge unless direction is supported.
- E2 never proves E3. Media relationships are not evidence of coordinated behaviour.
- Only E3 evidence from permitted account/time data can support a `candidate_cluster`; otherwise the state is `not_assessed`. **No account or person is ever called malicious, guilty or coordinated on media similarity alone.**
- `campaign_candidate_clusters` is deliberately empty in this package because no authorised account+time evidence is available locally.

## 6. Evidence types (what each record means)
`observed_fact` · `source_annotation` (as published by the dataset authors) · `machine_measurement` (hash, probe, fingerprint) · `ml_prediction` (never stored as ground truth) · `analyst_inference` · `unverified_claim` · `confirmed_evidence` (human-reviewed only). Every evidence record stores source URL/record, capture time, precision, hash where allowed, verification method, reviewer status, confidence basis and limitations.

## 7. Label dimensions (stored separately, never inferred from each other)
`authenticity_status` · `misleading_status` · `media_relationship_type` · `derivation_direction_status` · `transformation_type` · `coordination_status` · `evidence_status`.
- Native labels are kept verbatim (`native_*`); normalised labels sit in separate columns with the mapping rule in the data dictionary.
- FVC `fake` = debunked/misleading **not** AI-generated; `real` = verified. `normalized_authenticity_status` stays `unknown` unless the source says more.
- FIVR: ND = near-duplicate; DS = same scene from the same camera (copy-level); CS = same incident segment from a different camera (complementary, **not** a copy); IS = same incident. Only ND/DS suggest copying and none carries direction.
- VCSL: copied segments, direction not annotated (`unknown_direction`).
- ANAKIN: trimmed→edited is directed (documented editing task); full→trimmed is directed with segment bounds.
- Controlled variants: direction is `directed_controlled_transformation` because the transformation log defines it.
- Model predictions are always stored apart from ground truth and are never promoted to ground truth without a reviewed annotation.

### 7.1 Spread/timeline records (observations)
- Each observation has an `observation_type` (`upload`, `publish`, `removal`, `share_reference`, `cascade_member`) and `coordination_status=not_assessed`. A removal time is when the platform removed the video, not when it was created or first posted.
- Tweet times in RW-31 are derived deterministically from the tweet-id snowflake (UTC, second precision); they say when a post existed, **not who posted it** (no sharer accounts are provided). Facebook shares carry an id only.
- Publish times without a stated timezone are stored with precision `second_timezone_unstated`.
- A set of posts sharing one video, however large, is **not** coordination evidence; it remains `not_assessed`.

## 8. Relationship status rules
| Status | When used | Required evidence |
|---|---|---|
| `controlled_ground_truth` | edge created by a logged ORVEX transformation | run log + validation |
| `source_ground_truth` | relation published by the dataset authors | source file + hash |
| `uncertain` | sampled negatives, weak/contradictory/single-class evidence | stated rule; always routed to human review before any claim |
| `unknown` / `not_assessed` | nothing supports a decision | none |
Rules for future model output (Phase 2): **likely** = confidence above a threshold calibrated on the validation split to a stated precision AND ≥2 independent evidence types AND no contradiction; **uncertain** = between thresholds, single evidence type or contradiction; **unverified** = candidate without sufficient evidence (never drawn as an edge); **confirmed** = human reviewer with reason only. Numeric confidences carry no meaning until calibrated; none are stored now.

## 9. Directions, transformations, times
- Direction (parent→child) is stated only with a directional cue: source annotation, controlled log, or timestamps **plus** corroboration. Otherwise `unknown_direction`.
- A transformation is "detected" only if a detector for it has measured accuracy; otherwise "possible".
- "First observed" is never "first created". Timestamps carry precision; FVC has order only, not time.

## 10. Reporting rules
- Never use words such as "guilty", "malicious", "fake news source" about a person/account; use "candidate", "signal", "possible".
- Every statement in a report links to evidence IDs; the report/LLM agent may only quote tool outputs and evidence records and must not invent source facts.
- Accounts are pseudonymised in reports unless a licence requires attribution (then only in an attribution annex).
- Human review is mandatory for ambiguous edges, label conflicts, disputed labels and any campaign candidate. **[manual]**

## 11. Governance
Policy owner: project lead. Review: before each new source, before any public release, and when a licence/terms change. Violations (e.g., unverified source used, restricted media redistributed) require removal and a changelog entry.
