# -*- coding: utf-8 -*-
"""READ-ONLY. Referential integrity, lineage, split/leakage, quality, overlap, storage and documentation-vs-reality checks. Writes facts.json + CSVs into the audit folder."""
import sys, os, json, re, itertools, collections
sys.path.insert(0, os.path.dirname(__file__))
from ra_common import *
import numpy as np
sys.path.insert(0, str(ROOT / "scripts" / "datasets"))
import schema as PS
FM = pd.read_csv(WORK / "file_to_dataset_map.csv"); MP = pd.read_csv(OUT / "media_probe_results.csv"); SCH = json.load(open(WORK / ("schema_inspection_fixed.json" if (WORK / "schema_inspection_fixed.json").exists() else "schema_inspection.json"))); INV = pd.read_json(WORK / "inventory.json")
T = lambda n: read_table(ROOT / PS.TABLES[n]["path"])
master, var, edges, pairs, obs = T("real_world_media_master"), T("controlled_variant_registry"), T("media_relationship_edges"), T("training_pairs"), T("platform_observations")
ev, fman, dupm, spl, grp, runlog = T("evidence_ledger"), T("feature_manifest"), T("duplicate_map"), T("split_manifest"), T("group_examples"), T("transformation_run_log")
F = {}   # facts
# ---------------------------------------------------------------- referential integrity
M_ids = set(master["media_id"]); V_ids = set(var["variant_media_id"]); ALL = M_ids | V_ids; EV_ids = set(ev["evidence_id"]); EDGE_ids = set(edges["relationship_id"])
def dangling(series, universe): return int((~series.isin(universe) & (series != "")).sum())
integ = [("training_pairs.media_a_id -> master|variants", dangling(pairs["media_a_id"], ALL)), ("training_pairs.media_b_id -> master|variants", dangling(pairs["media_b_id"], ALL)), ("training_pairs.relationship_id -> edges", dangling(pairs["relationship_id"], EDGE_ids)),
         ("training_pairs.evidence_id -> evidence_ledger", dangling(pairs["evidence_id"], EV_ids)), ("edges.media_a_id -> master|variants", dangling(edges["media_a_id"], ALL)), ("edges.media_b_id -> master|variants", dangling(edges["media_b_id"], ALL)), ("edges.evidence_id -> evidence_ledger", dangling(edges["evidence_id"], EV_ids)),
         ("observations.media_id -> master", dangling(obs["media_id"], M_ids)), ("observations.evidence_id -> evidence_ledger", dangling(obs["evidence_id"], EV_ids)), ("master.evidence_id -> evidence_ledger", dangling(master["evidence_id"], EV_ids)),
         ("duplicate_map ids -> master", dangling(dupm["canonical_media_id"], M_ids) + dangling(dupm["duplicate_media_id"], M_ids)), ("feature_manifest.media_id -> master|variants (excl. ALL_LOCAL)", dangling(fman[fman["media_id"] != "ALL_LOCAL"]["media_id"], ALL)),
         ("variant.root_source_media_id -> master", dangling(var["root_source_media_id"], M_ids)), ("variant.direct_parent_media_id -> master|variants", dangling(var["direct_parent_media_id"], ALL)), ("run_log.variant_media_id -> variants", dangling(runlog["variant_media_id"], V_ids)),
         ("split_manifest.source_family_id -> master|ANAKIN families", int((~spl["source_family_id"].isin(M_ids | {m[:len("RW-ANK-") + m[len("RW-ANK-"):].rfind("-")] if False else "-".join(m.split("-")[:3]) for m in M_ids if m.startswith("RW-ANK-")})).sum())),
         ("group_examples member ids -> master|variants", sum(1 for s in grp["member_media_ids"] for m in s.split("|") if m not in ALL))]
F["integrity"] = integ
# features vs media
vis = [json.loads(l)["media_id"] for l in open(ROOT / "data/derived/features/visual_dhash24.jsonl", encoding="utf-8")]; aud = [json.loads(l)["media_id"] for l in open(ROOT / "data/derived/features/audio_fingerprint.jsonl", encoding="utf-8")]
local_ids = set(master[master["access_status"] == "downloaded_authorized"]["media_id"]) | set(var[var["validation_status"] == "passed"]["variant_media_id"])
F["features"] = dict(visual_records=len(vis), audio_records=len(aud), visual_orphans=len(set(vis) - ALL), local_media_ids=len(local_ids), local_without_visual=len(local_ids - set(vis)), visual_duplicates=len(vis) - len(set(vis)))
# ---------------------------------------------------------------- variants: lineage on disk
vp = var[var["validation_status"] == "passed"]; ondisk = {p.as_posix() for p in (ROOT / "data/controlled_variants/media").rglob("*.mp4")}; ondisk = {str(Path(p).relative_to(ROOT).as_posix()) for p in (ROOT / "data/controlled_variants/media").rglob("*.mp4")}
inreg = set(vp["local_path"]); extra = sorted(ondisk - inreg); miss = sorted(inreg - ondisk)
ids = set(vp["variant_media_id"]) | M_ids; chain_ok = sum(1 for _, r in vp.iterrows() if all(a in ids for a in r["ancestor_chain"].split("|")) and r["direct_parent_media_id"] in ids)
F["variants"] = dict(registry_rows=len(var), passed=len(vp), failed=len(var) - len(vp), files_on_disk=len(ondisk), extra_files_on_disk=extra, registered_missing_on_disk=miss, chain_complete=chain_ok, failed_with_file_on_disk=[Path(p).stem for p in extra if Path(p).stem in set(var[var["validation_status"] == "failed"]["variant_media_id"])])
F["variants"]["by_transformation"] = vp["transformation_name"].value_counts().to_dict(); F["variants"]["by_depth"] = vp["generation_depth"].value_counts().to_dict()
# ---------------------------------------------------------------- lineage CSV (dataset-level + variant-level)
L = []
def ds_lin(parent, child, tf, script, repro, note): L.append(dict(granularity="dataset-level", parent_dataset=parent, parent_record="*", derived_dataset=child, derived_record="*", transformation=tf, parameters="see script", script_or_function=script, tool_version="python/pandas; ffmpeg where media", run_id="n/a (no run-id registry for table builds)", reproducible=repro, chain_complete="yes (recorded)", inferred_not_recorded="no", verification=note))
ds_lin("DS-001", "DS-016", "normalise + QC + dedupe", "scripts/datasets/s3_normalize.py:qc_commons", "yes (deterministic; needs originals)", "master RW-01 rows present"); ds_lin("DS-003", "DS-016", "normalise ANAKIN rows", "scripts/datasets/s3_normalize.py:anakin_rows", "yes", "master RW-02 rows present")
for d, fn in (("DS-006", "fvc_rows"), ("DS-007", "fvc_rows"), ("DS-008", "fvc_rows"), ("DS-009", "fivr_rows"), ("DS-010", "vcsl_rows"), ("DS-011", "covid_rows")): ds_lin(d, "DS-016", "normalise native records into ORVEX schema", f"scripts/datasets/s3_normalize.py:{fn}", "yes", "records counted in master by source")
ds_lin("DS-005", "DS-017", "native edit edges", "scripts/datasets/s3_normalize.py:anakin_rows/edge", "yes", "edges RW-02 present"); ds_lin("DS-006", "DS-017", "cascade membership edges", "s3_normalize.py:fvc_rows/edge", "yes", "edges RW-03 present"); ds_lin("DS-009", "DS-017", "ND/DS/CS native edges", "s3_normalize.py:fivr_rows/edge", "yes", "edges RW-06 present"); ds_lin("DS-010", "DS-017", "copied-segment edges", "s3_normalize.py:vcsl_rows/edge", "yes", "edges RW-07 present")
ds_lin("DS-001", "DS-013", "14 FFmpeg transformation types + 5 chains", "scripts/datasets/s4_variants.py:process/make/build", "yes (deterministic; seeds by sha256 pick)", f"{len(vp)} passed variants, chain complete {chain_ok}"); ds_lin("DS-013", "DS-021", "24-frame dHash", "scripts/datasets/s5_features_pairs_splits.py:feat", "yes", "records cover local media"); ds_lin("DS-013", "DS-022", "audio md5/envelope", "s5_features_pairs_splits.py:feat", "yes", "records cover local media")
ds_lin("DS-014", "DS-017", "controlled lineage edges", "s5_features_pairs_splits.py (module level)", "yes", "1 controlled edge per passed variant (+ audio-donor edges)"); ds_lin("DS-014", "DS-023", "pairs from lineage + negative sampling", "s5_features_pairs_splits.py:addpair", "yes (seeded)", "pairs reference existing ids (integrity checked)"); ds_lin("DS-023", "DS-030", "non-learned dHash baseline", "scripts/datasets/s9_feature_baseline.py", "yes (deterministic)", "8 metric rows")
for _, r in var.iterrows():
    ok = r["validation_status"] == "passed"; chain = r["ancestor_chain"].split("|") if r["ancestor_chain"] else []
    L.append(dict(granularity="record-level", parent_dataset="DS-001" if r["direct_parent_media_id"] in M_ids else "DS-013", parent_record=r["direct_parent_media_id"], derived_dataset="DS-013", derived_record=r["variant_media_id"], transformation=r["transformation_name"], parameters=r["parameters_json"][:160], script_or_function="scripts/datasets/s4_variants.py:make",
                  tool_version=r["tool_version"], run_id=r["run_id"], reproducible="yes (parameters + FFmpeg command logged)", chain_complete=("yes" if ok and all(a in ids for a in chain) else ("n/a (failed, no output retained)" if not ok else "NO")), inferred_not_recorded="no (recorded in registry)",
                  verification=("file present + independently probed" if r["local_path"] in ondisk and ok else ("FAILED variant; registry says no file" + ("; BUT FILE EXISTS ON DISK" if f"data/controlled_variants/media/{r['variant_media_id'].split('-')[1]}/{r['variant_media_id']}.mp4" in ondisk else "") if not ok else "file missing"))))
for p in extra:
    if Path(p).stem not in set(var["variant_media_id"]) or Path(p).stem in set(var[var["validation_status"] == "failed"]["variant_media_id"]): pass
pd.DataFrame(L).to_csv(safe_out("dataset_lineage.csv"), index=False, encoding="utf-8-sig"); F["lineage_rows"] = len(L)
# ---------------------------------------------------------------- splits and leakage (independent)
sp = dict(zip(spl["source_family_id"], spl["split"]))
def fam(x):
    if x.startswith("CV-"): return "RW-CMN-P" + x.split("-")[1][1:]
    if x.startswith("RW-ANK-"): return "-".join(x.split("-")[:3])
    return x
pa = pairs[pairs["split"] != "excluded"]; cross = int(sum(1 for a, b, s in zip(pa["media_a_id"], pa["media_b_id"], pa["split"]) if sp.get(fam(a)) != s or sp.get(fam(b)) != s))
varsplit = int((vp["source_split"] != vp["root_source_media_id"].map(sp)).sum()); HELD = {"T11", "T12", "T13", "T14"}; byv = dict(zip(var["variant_media_id"], zip(var["transformation_id"], var["direct_parent_media_id"])))
def held(x):
    while x in byv:
        if byv[x][0] in HELD: return True
        x = byv[x][1]
    return False
heldtrain = int(sum(1 for a, b, s in zip(pa["media_a_id"], pa["media_b_id"], pa["split"]) if s in ("train", "val") and (held(a) or held(b))))
neg = pairs[(pairs["relationship_class"] == "unrelated_distinct_source") & (pairs["split"] != "excluded")]; dupids = set(dupm["canonical_media_id"]) | set(dupm["duplicate_media_id"])
same_family_neg = int(sum(1 for a, b in zip(neg["media_a_id"], neg["media_b_id"]) if fam(a) == fam(b))); neg_dup = int(sum(1 for a, b in zip(neg["media_a_id"], neg["media_b_id"]) if fam(a) in dupids or fam(b) in dupids))
# near-duplicate leakage among originals (dHash, threshold 0.45) across splits
H = {}
for l in open(ROOT / "data/derived/features/visual_dhash24.jsonl", encoding="utf-8"):
    j = json.loads(l); H[j["media_id"]] = np.array([int(x, 16) for x in j["dhash24"]], dtype=np.uint64)
orig = [m for m in master[(master["source_dataset_id"].isin(["RW-01"])) & (master["usable_for_variants"] == "True")]["media_id"]] + [m for m in master[(master["source_dataset_id"] == "RW-02") & (master["media_id"].str.endswith("-T")) & (master["access_status"] == "downloaded_authorized")]["media_id"]]
def fr(a, b): return float((np.bitwise_count(a[:, None] ^ b[None, :]).min(1) <= 8).mean()) if len(a) and len(b) else 0.0
nd = [];
for a, b in itertools.combinations([o for o in orig if o in H], 2):
    s = max(fr(H[a], H[b]), fr(H[b], H[a]))
    if s >= 0.45: nd.append((a, b, round(s, 2), sp.get(fam(a)), sp.get(fam(b))))
F["splits"] = dict(families_by_dataset_split=spl.groupby(["source_dataset_id", "split"]).size().unstack(fill_value=0).to_dict(), pairs_by_split=pairs["split"].value_counts().to_dict(), cross_split_pairs=cross, variant_split_mismatch=varsplit, heldout_in_train_val_pairs=heldtrain,
                   negatives_total=len(neg), negatives_same_family=same_family_neg, negatives_touching_duplicate_records=neg_dup, hardness_by_split=pairs[(pairs["relationship_class"] == "unrelated_distinct_source") & (pairs["split"] != "excluded")].groupby(["split", "hardness"]).size().unstack(fill_value=0).to_dict(),
                   near_duplicate_original_pairs=len(nd), near_duplicate_cross_split=[x for x in nd if x[3] != x[4]][:10], near_duplicate_cross_split_count=sum(1 for x in nd if x[3] != x[4]), originals_compared=len([o for o in orig if o in H]),
                   class_by_split=pairs.groupby(["split", "relationship_class"]).size().unstack(fill_value=0).to_dict(), variants_by_split=vp["source_split"].value_counts().to_dict(), trainable=int((var["usable_for_training"] == "True").sum()))
# ---------------------------------------------------------------- media quality
q = {}
for c, g in MP.groupby("component"):
    q[c] = dict(files=len(g), readable=int(g["readable"].sum()), hours=round(float(g["duration_s"].sum()) / 3600, 2), dur_min=round(float(g["duration_s"].min()), 1), dur_median=round(float(g["duration_s"].median()), 1), dur_max=round(float(g["duration_s"].max()), 1), audio_share=round(float(g["has_audio"].astype(bool).mean()), 3),
                heights=g["height"].dropna().astype(int).value_counts().head(6).to_dict(), fps=g["fps"].dropna().round(0).astype(int).value_counts().head(5).to_dict(), unreadable=g[~g["readable"]]["path"].tolist()[:5])
F["media_quality"] = q
cm = master[master["source_dataset_id"] == "RW-01"]; flags = pd.Series([f for s in cm["qc_flags"] for f in s.split("|") if f]).value_counts().to_dict()
F["commons"] = dict(files=len(cm), usable=int((cm["usable_for_variants"] == "True").sum()), qc_flags=flags, licences=cm["license"].value_counts().to_dict(), no_audio_usable=int(((cm["usable_for_variants"] == "True") & (cm["has_audio"] != "True")).sum()), by_theme={k: int(v) for k, v in pd.Series({r["media_id"]: json.load(open(ROOT / "data/real_world/raw_metadata/commons/commons_candidates.json", encoding="utf-8")) for r in []}).items()} if False else {})
cj = json.load(open(ROOT / "data/real_world/raw_metadata/commons/commons_candidates.json", encoding="utf-8")); th = {f"RW-CMN-P{c['pageid']}": c["domain"] for c in cj}
F["commons"]["usable_by_theme"] = pd.Series([th[m] for m in cm[cm["usable_for_variants"] == "True"]["media_id"]]).value_counts().to_dict()
F["commons"]["missing_author"] = int(sum(1 for c in cj if not (c["author"] or c["credit"]))); F["commons"]["missing_license_url"] = int(sum(1 for c in cj if not c["license_url"]))
# ---------------------------------------------------------------- native-source consistency checks
Rm = ROOT / "data/real_world/raw_metadata"
fv = read_table(Rm / "invid_fvc_2018/extracted/FVC.csv"); fd = read_table(Rm / "invid_fvc_2018/extracted/FVC_dup.csv"); fall = pd.concat([fv, fd])
zdesc = json.load(open(Rm / "zenodo_api/zenodo_2535479.json", encoding="utf-8"))["metadata"]["description"]; m_claim = re.search(r"(\d+) videos annotated as fake and (\d+) annotated as real", zdesc)
F["fvc2018"] = dict(heads=len(fv), dup_rows=len(fd), total_rows=len(fall), file_fake=int((fall["label"] == "fake").sum()), file_real=int((fall["label"] == "real").sum()), record_claims=dict(fake=int(m_claim.group(1)), real=int(m_claim.group(2))) if m_claim else None, dup_rows_distinct_urls=int(fd["video_url"].nunique()), journal_claim_near_duplicates=5195)
F["fvc2018"]["label_values"] = fall["label"].value_counts().to_dict(); F["fvc2018"]["rows_normalised_to_not_assessed"] = int(((master["source_dataset_id"] == "RW-03") & (master["normalized_misleading_status"] == "not_assessed")).sum())
fiv = edges[edges["source_dataset_id"] == "RW-06"]; F["fivr_norm"] = dict(unnormalised_IS_edges=int(((fiv["native_label"] == "IS") & (fiv["normalized_relation_type"] == "IS")).sum()), dangling_edges=int((~fiv["media_b_id"].isin(M_ids)).sum()), by_label=fiv["native_label"].value_counts().to_dict())
_sel = read_table(ROOT / "data/real_world/raw_metadata/hf_api/anakin_selected_subset.csv"); F["anakin_sources"] = dict(selected=len(_sel), distinct_urls=int(_sel["url"].nunique()), metadata_rows=int(len(read_table(ROOT / "data/real_world/raw_metadata/hf_api/anakin_metadata.csv"))), metadata_distinct_urls=int(read_table(ROOT / "data/real_world/raw_metadata/hf_api/anakin_metadata.csv")["url"].nunique()))
ftq = SCH["data/real_world/raw_metadata/invid_fvc_2018/extracted/FVC_text_queries.csv"]; F["fvc2018"]["text_queries_file"] = dict(rows=ftq.get("rows"), header_fields=ftq.get("header_fields"), max_fields=ftq.get("max_fields"), ragged_rows=ftq.get("ragged_rows"), read_by_orvex_code=bool(grep_code(r"FVC_text_queries|text_queries")))
blobs = json.load(open(Rm / "hf_api/anakin_blobs.json", encoding="utf-8"))["siblings"]; ed = {x["rfilename"].split("/")[1][:-4] for x in blobs if x["rfilename"].startswith("edited/")}; meta = read_table(Rm / "hf_api/anakin_metadata.csv"); mid = set(meta["video-id"])
F["anakin"] = dict(official_edited_files=len(ed), metadata_rows=len(meta), files_without_metadata=len(ed - mid), metadata_without_files=len(mid - ed), selected_pairs=sch_rows if False else len(read_table(Rm / "hf_api/anakin_selected_subset.csv")), types=meta["manipulation-type"].value_counts().to_dict(), mask_files_local=len(list((ROOT / "data/real_world/media/anakin/masks").glob("*.zip"))),
                   mask_bytes=sum(p.stat().st_size for p in (ROOT / "data/real_world/media/anakin/masks").glob("*.zip")), masks_referenced_by_code=[f"{f}:{ln}" for f, ln, fn, t in grep_code(r"masks")][:6])
vu = read_table(Rm / "vcsl/videos_url_uuid.csv"); uu = set(vu["uuid"]); lab = json.load(open(Rm / "vcsl/label_file_uuid_total.json")); lab_ids = {x for k in lab for x in k.split("-")}
pf = {n: read_table(Rm / f"vcsl/pair_file_{n}.csv") for n in ("train", "val", "test")}
F["vcsl"] = dict(videos=len(vu), label_pairs=len(lab), segments=sum(len(v) for v in lab.values()), label_ids_not_in_url_list=len(lab_ids - uu), pair_file_rows={k: len(v) for k, v in pf.items()}, pair_ids_not_in_url_list=sum(len(set(v["query_id"]) | set(v["reference_id"]) - uu) for v in pf.values()), hosts=vu["url"].str.extract(r"https?://([^/]+)/")[0].value_counts().head(4).to_dict())
ann = json.load(open(Rm / "invid_fivr200k/extracted/annotation.json")); yid = {l.strip() for l in open(Rm / "invid_fivr200k/extracted/youtube_ids.txt") if l.strip()}; evn = json.load(open(Rm / "invid_fivr200k/extracted/events.json", encoding="utf-8"))
cand = {v for q_ in ann.values() for L_ in q_.values() for v in L_}
F["fivr"] = dict(ids=len(yid), queries=len(ann), labels={k: sum(len(q_.get(k, [])) for q_ in ann.values()) for k in ("ND", "DS", "CS", "IS")}, query_ids_not_in_ids=len(set(ann) - yid), candidate_ids_not_in_ids=len(cand - yid), events=len(evn), event_keys=sorted({k for e in evn for k in e}))
cv = read_table(Rm / "covid_misinfo_4557828/covid-misinfo-videos.csv.gz"); F["covid"] = dict(rows=len(cv), publish_ts=int((cv["published_timestamp"] != "").sum()), channel=int((cv["channel_id"] != "").sum()), removal_ts=int((cv["removal_timestamp"] != "").sum()), dup_urls=int(cv["youtube_link"].duplicated().sum()), twitter_ids=int(sum(len(re.findall(r"\d{10,}", x)) for x in cv["twitter_post_ids"])), facebook_ids=int(sum(len(re.findall(r"\d{6,}", x)) for x in cv["facebook_post_ids"])),
                  tweets_unverified_time=int((obs["time_precision"] == "second_derived_unverified").sum()), sharer_accounts=int(((obs["observation_type"] == "share_reference") & (obs["account_id_pseudonym"] != "")).sum()), pub_ts_range=[cv[cv["published_timestamp"] != ""]["published_timestamp"].min(), cv[cv["published_timestamp"] != ""]["published_timestamp"].max()])
# ---------------------------------------------------------------- overlap (YouTube ids by dataset)
yt = master[(master["platform"] == "youtube") & (master["platform_media_id"] != "")]; sets = {s: set(g["platform_media_id"]) for s, g in yt.groupby("source_dataset_id")}
ov = [dict(dataset_a=a, dataset_b=b, ids_a=len(sets[a]), ids_b=len(sets[b]), shared_youtube_ids=len(sets[a] & sets[b])) for a, b in itertools.combinations(sorted(sets), 2)]
pd.DataFrame(ov).to_csv(safe_out("dataset_overlap_matrix.csv"), index=False, encoding="utf-8-sig"); F["overlap"] = ov
hashes = {l.split("  ")[1].strip(): l.split("  ")[0] for l in open(ROOT / "data/manifests/checksums.sha256", encoding="utf-8")}; mh = {p: h for p, h in hashes.items() if p.endswith((".mp4", ".webm", ".ogv", ".ogg"))}; cnt = collections.Counter(mh.values())
F["media_hash_duplicates"] = dict(media_files_hashed=len(mh), duplicate_hash_groups=sum(1 for v in cnt.values() if v > 1), files_in_duplicate_groups=sum(v for v in cnt.values() if v > 1))
# ---------------------------------------------------------------- storage
data_b = int(FM[FM["path"].str.startswith("data/")]["bytes"].sum()); repo_b = int(FM["bytes"].sum())
zip_b = sum(p.stat().st_size for p in Rm.rglob("*.zip")); ext_b = sum(dir_stats(d)[1] for d in Rm.glob("*/extracted"))
ds_b = FM.groupby("ds")["bytes"].sum().to_dict(); build = ROOT / "data/manifests/_build"; wav_b = sum(p.stat().st_size for p in build.rglob("*.wav")) if build.exists() else 0
F["storage"] = dict(data_bytes=data_b, repo_bytes=repo_b, cap_bytes=30 * 10 ** 9, remaining_to_cap=30 * 10 ** 9 - data_b, by_dataset={k: int(v) for k, v in ds_b.items()}, archives_zip_bytes=int(zip_b), extracted_copies_bytes=int(ext_b), donor_wav_cache_bytes=int(wav_b), symlinks=int(FM["symlink"].sum()),
                    media_bytes=dict(commons=int(ds_b.get("DS-001", 0)), anakin=int(ds_b.get("DS-003", 0) + ds_b.get("DS-004", 0)), variants=int(ds_b.get("DS-013", 0))), definition="decimal bytes of all files under <repo>\\data; excludes tools/, ORVEX_Literature/, docs/, scripts/, tests/ and model weights (none exist); no symlinks followed (none found)")
# Layer A read-only status
ro = w = 0
for base in ("data/real_world/media", "data/real_world/raw_metadata"):
    for r, _, fs in os.walk(ROOT / base):
        for f in fs: ro += int(not os.access(os.path.join(r, f), os.W_OK)); w += int(os.access(os.path.join(r, f), os.W_OK))
F["layer_a_read_only"] = dict(read_only=ro, writable=w)
# ---------------------------------------------------------------- documentation-vs-reality claims
def num(s): return float(s.replace(",", ""))
DOCS = ROOT / "docs/datasets"; claims = []
def claim(doc, rx, actual, label, tol=0):
    p = DOCS / doc
    if not p.exists(): claims.append(dict(doc=doc, claim=label, claimed="doc missing", actual=actual, match=None)); return
    m = re.search(rx, p.read_text(encoding="utf-8"))
    if not m: claims.append(dict(doc=doc, claim=label, claimed="claim text not found", actual=actual, match=None)); return
    c = num(m.group(1)); claims.append(dict(doc=doc, claim=label, claimed=c, actual=actual, match=abs(c - actual) <= tol))
CR = "ORVEX_10_2_10_3_10_4_COMPLETION_REPORT.md"
claim(CR, r"\| training_pairs \|[^|]*\| (\d[\d,]*) \(train", len(pairs), "training pairs (total)"); claim(CR, r"\| group_examples \|[^|]*\| (\d[\d,]*) \|", len(grp), "group examples"); claim(CR, r"\*\*(\d+\.\d+) GB\*\* measured", data_b / 1e9, "dataset payload GB", 0.05); claim(CR, r"Trainable variants: (\d+)", F["splits"]["trainable"], "trainable variants")
claim(CR, r"\| real_world_media_master \|[^|]*\| (\d[\d,]*) \|", len(master), "media master rows"); claim(CR, r"\| platform_observations \|[^|]*\| (\d[\d,]*) \|", len(obs), "platform observation rows"); claim(CR, r"\| evidence_ledger \|[^|]*\| (\d[\d,]*) \|", len(ev), "evidence ledger rows")
claim(CR, r"\*\*Failures: (\d+)\*\*", F["variants"]["failed"], "failed variants"); claim(CR, r"(\d+) local media files re-hashed|re-hashing (\d[\d,]*) local media", len(mh) if False else 0, "locally re-hashed media (claim text check only)") if False else None
claim(CR, r"no file kept|and no file kept", 0, "failed variants retained as files on disk (claim: none)") if False else None
claim("ORVEX_DATASET_QA_REPORT.md", r"Failed variants: (\d+)", F["variants"]["failed"], "QA report failed variants")
ret = (DOCS / CR).read_text(encoding="utf-8"); F["claim_no_file_kept_for_failed"] = ("no file kept" in ret or "no file retained" in ret); F["claims"] = claims
F["stray_files"] = [p for p in FM[FM["ds"] == "DS-040"]["path"].tolist()]; F["nul_size"] = int((ROOT / "nul").stat().st_size) if (ROOT / "nul").exists() else None
F["no_git"] = not (ROOT / ".git").exists(); F["no_app_code"] = not any((ROOT / n).exists() for n in ("package.json", "pyproject.toml", "requirements.txt", "backend", "frontend", "src"))
F["model_artifacts"] = int(FM["path"].str.lower().str.endswith((".pt", ".pth", ".onnx", ".pkl", ".joblib", ".h5", ".safetensors", ".ipynb", ".parquet", ".sqlite", ".db")).sum())
F["patch_scripts"] = sorted(p.name for p in (ROOT / "scripts/datasets").glob("patch_round*.py")) + sorted(p.name for p in (ROOT / "scripts/datasets").glob("update_report*.py"))
json.dump(F, open(WORK / "facts.json", "w"), indent=1, default=str)
print(json.dumps({k: F[k] for k in ("variants", "storage", "layer_a_read_only", "media_hash_duplicates", "features")}, indent=0, default=str)[:2500]); print("integrity:", [x for x in integ if x[1]]); print("claims mismatches:", [c for c in claims if c["match"] is False])
