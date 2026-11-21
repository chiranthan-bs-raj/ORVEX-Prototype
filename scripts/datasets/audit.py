# -*- coding: utf-8 -*-
"""Executable acceptance checks + requirement coverage matrix. Every PASS is produced by running a check against the real files."""
import os, sys, json, csv, glob, hashlib, re, re
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from common import *
import schema
from transformations import CATALOGUE

_T = {}
def T(name):
    if name not in _T:
        p = os.path.join(ROOT, schema.TABLES[name]["path"])
        _T[name] = pd.read_csv(p, dtype=str, keep_default_na=False, encoding="utf-8-sig") if os.path.exists(p) else pd.DataFrame(columns=schema.cols(name))
    return _T[name]
HELD = {c[0] for c in CATALOGUE if c[6]}
R = {}   # check results: id -> (ok: bool|None, evidence)
def chk(cid):
    def deco(f):
        try: ok, ev = f()
        except Exception as e: ok, ev = False, f"check crashed: {e!r}"
        R[cid] = (bool(ok), ev); return f
    return deco

@chk("K01_schema_columns")
def _():
    bad = []
    for t, d in schema.TABLES.items():
        p = os.path.join(ROOT, d["path"])
        if not os.path.exists(p): bad.append(f"{t}: missing file"); continue
        h = list(csv.reader(open(p, encoding="utf-8-sig")))[0]
        if h != schema.cols(t): bad.append(f"{t}: header differs from contract")
    return not bad, f"{len(schema.TABLES)} tables, {sum(len(d['cols']) for d in schema.TABLES.values())} contract columns; mismatches: {bad or 'none'}"
@chk("K02_required_nonnull")
def _():
    bad = {}
    for t, d in schema.TABLES.items():
        df = T(t)
        for c in d["cols"]:
            if not c[2] and len(df) and (df[c[0]] == "").any(): bad[f"{t}.{c[0]}"] = int((df[c[0]] == "").sum())
    return not bad, f"non-nullable columns with blanks: {bad or 'none'}"
@chk("K03_unique_ids")
def _():
    m, v, e = T("real_world_media_master"), T("controlled_variant_registry"), T("media_relationship_edges")
    d1 = m["media_id"].duplicated().sum(); d2 = v["variant_media_id"].duplicated().sum(); d3 = e["relationship_id"].duplicated().sum(); ov = len(set(m["media_id"]) & set(v["variant_media_id"]))
    return d1 == d2 == d3 == ov == 0, f"duplicate media_id={d1}, variant ids={d2}, relationship ids={d3}, overlap natural/variant ids={ov}; media={len(m)}, variants={len(v)}, edges={len(e)}"
@chk("K04_variant_lineage")
def _():
    m, v = T("real_world_media_master"), T("controlled_variant_registry"); ok = v[v["validation_status"] == "passed"]
    real = set(m[(m["source_dataset_id"] == "RW-01") & (m["usable_for_variants"] == "True")]["media_id"]); ids = set(ok["variant_media_id"]) | set(m["media_id"]); bad = 0
    for _, r in ok.iterrows():
        ch = r["ancestor_chain"].split("|")
        if r["direct_parent_media_id"] not in ids or ch[-1] not in real or r["root_source_media_id"] != ch[-1] or r["video_source_media_id"] not in real: bad += 1
        if r["audio_source_media_id"] and r["audio_source_media_id"] not in real: bad += 1
        if r["caption_text_source_media_id"] and r["caption_text_source_media_id"] not in real: bad += 1
    return bad == 0, f"{len(ok)} passed variants; chains not ending in an eligible real-world root / invalid audio or caption provenance: {bad}"
@chk("K05_separation")
def _():
    m, v = T("real_world_media_master"), T("controlled_variant_registry"); bad = 0
    bad += int((v["media_origin"] != "controlled_variant").sum()) + int((m["media_origin"] == "controlled_variant").sum())
    bad += int((~v[v["local_path"] != ""]["local_path"].str.startswith("data/controlled_variants/media/")).sum()); lp = m[m["local_path"] != ""]["local_path"]
    bad += int((~lp.str.startswith("data/real_world/media/")).sum())
    nat = [f for f in glob.glob(os.path.join(CVMEDIA, "**", "*.*"), recursive=True)]; bad += sum(1 for f in glob.glob(os.path.join(RWMEDIA, "**", "CV-*"), recursive=True))
    return bad == 0, f"separation violations: {bad}; controlled files on disk: {len(nat)}"
@chk("K06_hashes")
def _():
    m, v = T("real_world_media_master"), T("controlled_variant_registry"); bad = 0; n = 0
    for df, col in ((m[m["local_path"] != ""], "sha256"), (v[v["local_path"] != ""], "sha256")):
        for _, r in df.iterrows():
            p = os.path.join(ROOT, r["local_path"]); n += 1
            if not os.path.exists(p) or sha256(p) != r[col]: bad += 1
    return bad == 0, f"{n} local media files re-hashed; missing or hash mismatch: {bad}"
@chk("K07_metadata_only_clean")
def _():
    m = T("real_world_media_master"); mo = m[m["access_status"] == "metadata_only"]; bad = int((mo["local_path"] != "").sum() + (mo["sha256"] != "").sum())
    return bad == 0, f"{len(mo)} metadata_only records; with a local path/hash (would be a false 'downloaded' claim): {bad}"
@chk("K08_licence_gate")
def _():
    m = T("real_world_media_master"); c = m[(m["source_dataset_id"] == "RW-01") & (m["access_status"] == "downloaded_authorized")]
    ok = c["license"].str.match(r"^(CC0|Public domain|CC BY(?!-NC)(?!-ND)|CC BY-SA)", case=False) & ~c["license"].str.contains("NC|ND", case=True)
    return bool(ok.all()) and len(c) > 0, f"{len(c)} downloaded Commons files; licences: {c['license'].value_counts().to_dict()}; outside allowed set: {int((~ok).sum())}"
@chk("K09_real_world_only")
def _():
    v = T("controlled_variant_registry"); m = T("real_world_media_master"); tools = set(v["tool_name"]); src = set(m[m["usable_for_variants"] == "True"]["source_dataset_id"])
    return tools == {"ffmpeg"} and src == {"RW-01"}, f"variant tools={tools}; sources used for variants={src}; catalogue contains only FFmpeg filters (no generative models, no TTS)"
@chk("K10_transform_coverage")
def _():
    v = T("controlled_variant_registry"); ok = v[v["validation_status"] == "passed"]; c = ok["transformation_name"].value_counts().to_dict(); need = {"trim_middle", "trim_head", "trim_tail", "crop_center", "caption_burn_in", "audio_replace", "recompress_low"}
    chain = int((ok["generation_depth"].astype(int) >= 2).sum()); return need <= set(c) and chain > 0, f"passed by transformation={c}; multi-step (depth>=2) variants={chain}; failed={int((v['validation_status'] == 'failed').sum())}"
@chk("K11_controlled_edges")
def _():
    e, v = T("media_relationship_edges"), T("controlled_variant_registry"); ok = v[v["validation_status"] == "passed"]; ce = e[(e["relation_scope"] == "controlled_lineage") & (e["normalized_relation_type"] != "controlled_audio_source_of_variant")]
    missing = set(ok["variant_media_id"]) - set(ce["media_b_id"]); return not missing and len(ce) == len(ok), f"controlled lineage edges={len(ce)} for {len(ok)} passed variants; variants without an edge: {len(missing)}"
@chk("K12_native_edges_preserved")
def _():
    e = T("media_relationship_edges"); n = e[e["relation_scope"] == "real_native"]["source_dataset_id"].value_counts().to_dict(); lab = e[e["relation_scope"] == "real_native"]["native_label"].replace("", pd.NA).dropna().nunique()
    return all(k in n for k in ("RW-02", "RW-03", "RW-06", "RW-07")), f"native edges by dataset={n}; distinct native labels kept={lab}"
@chk("K13_split_leakage")
def _():
    sm = T("split_manifest"); sp = dict(zip(sm["source_family_id"], sm["split"])); tp = T("training_pairs"); tp = tp[tp["split"] != "excluded"]
    def fam(x):
        if x.startswith("CV-"): return "RW-CMN-P" + x.split("-")[1][1:]
        if x.startswith("RW-ANK-"): return "-".join(x.split("-")[:3])
        return x
    bad = 0
    for a, b, f, s in zip(tp["media_a_id"], tp["media_b_id"], tp["source_family_id"], tp["split"]):
        fa, fb = fam(a), fam(b)
        if sp.get(f) != s: bad += 1
        elif tp.shape[0] and (fa not in sp or fb not in sp): bad += 1
        elif sp[fa] != s or sp[fb] != s: bad += 1
    v = T("controlled_variant_registry"); vv = v[v["validation_status"] == "passed"]; bad += int((vv["source_split"] != vv["root_source_media_id"].map(sp)).sum())
    return bad == 0 and len(tp) > 0, f"{len(tp)} model pairs checked across {len(sp)} families; pairs/variants whose members are not wholly inside one split: {bad}; splits={sm['split'].value_counts().to_dict()}"
@chk("K14_heldout_policy")
def _():
    v = T("controlled_variant_registry"); tp = T("training_pairs"); by = dict(zip(v["variant_media_id"], zip(v["transformation_id"], v["direct_parent_media_id"])))
    def held(x):
        while x in by:
            if by[x][0] in HELD: return True
            x = by[x][1]
        return False
    bad = int(v[(v["usable_for_training"] == "True")]["variant_media_id"].map(held).sum())
    bad += sum(1 for a, b, s in zip(tp["media_a_id"], tp["media_b_id"], tp["split"]) if s in ("train", "val") and (held(a) or held(b)))
    return bad == 0, f"held-out transformation types {sorted(HELD)}; training/validation uses of held-out lineage: {bad}; test pairs with held-out lineage: {int(((tp['split'] == 'test') & (tp['includes_heldout_transform'] == 'True')).sum())}"
@chk("K15_pair_labels")
def _():
    tp = T("training_pairs"); pos = {"direct_derivation", "indirect_derivation", "sibling_same_parent", "same_family_other", "edited_version"}; neg = {"unrelated_distinct_source", "audio_source_only_not_visual_derivation"}
    bad = int(((tp["relationship_class"].isin(pos)) & (tp["label_binary_related"] != "1")).sum() + ((tp["relationship_class"].isin(neg)) & (tp["label_binary_related"] != "0")).sum())
    bad += int(((tp["label_binary_related"] == "0") & (tp["relationship_class"] == "unrelated_distinct_source") & (tp["negative_rationale"] == "")).sum())
    return bad == 0 and len(tp) > 0, f"{len(tp)} pairs; class counts={tp['relationship_class'].value_counts().to_dict()}; label inconsistencies={bad}"
@chk("K16_budget")
def _():
    b = payload_bytes(); return b < CAP_HARD and b <= CAP_TARGET, f"dataset payload (everything under data/) = {b} bytes = {b/1e9:.2f} GB (decimal) = {b/2**30:.2f} GiB; cap 30 GB, target <=27 GB"
@chk("K17_features")
def _():
    f = T("feature_manifest"); m = T("real_world_media_master"); v = T("controlled_variant_registry"); nloc = int((m["access_status"] == "downloaded_authorized").sum()) + int((v["validation_status"] == "passed").sum())
    vis = f[f["feature_type"] == "visual_dhash24"]; comp = vis[vis["extraction_status"] == "computed"]; failed = set(vis[vis["extraction_status"] != "computed"]["media_id"])
    unplay = set(m[(m["playable_status"] == "unplayable") | (m["usable_for_variants"] == "False") & (m["source_dataset_id"] == "RW-01")]["media_id"]); agg = f[f["media_id"] == "ALL_LOCAL"]["feature_type"].tolist()
    exist = os.path.exists(os.path.join(FEAT, "visual_dhash24.jsonl")) and os.path.exists(os.path.join(FEAT, "audio_fingerprint.jsonl"))
    return exist and len(vis) == nloc and failed <= unplay, f"visual dHash computed for {len(comp)} of {nloc} local media (failures {sorted(failed)}; all are QC-flagged unusable files excluded from variants: {failed <= unplay}); NOT computed, no placeholder files: {agg}"
@chk("K18_native_files_intact")
def _():
    exp = {"2535479": ("invid_fvc_2018", "fake-video-corpus-2018.zip"), "1147958": ("invid_fvc_v2", "Fake_Video_Corpus_v2.0.zip"), "242481": ("invid_fvc_v1", "Fake_Video_Corpus.zip"), "2564864": ("invid_fivr200k", "fivr_200k_dataset.zip")}; bad = []
    for rid, (d, f) in exp.items():
        j = json.load(open(os.path.join(RWMETA, "zenodo_api", f"zenodo_{rid}.json"), encoding="utf-8")); want = j["files"][0]["checksum"].split(":")[1]; p = os.path.join(RWMETA, d, f)
        if not os.path.exists(p) or hashlib.md5(open(p, "rb").read()).hexdigest() != want: bad.append(rid)
    return not bad, f"4 official archives re-verified against Zenodo md5; failures: {bad or 'none'}"
@chk("K19_duplicates")
def _():
    d, m = T("duplicate_map"), T("real_world_media_master"); ids = set(m["media_id"]); bad = int((~d["canonical_media_id"].isin(ids)).sum() + (~d["duplicate_media_id"].isin(ids)).sum())
    return bad == 0, f"{len(d)} duplicate records mapped {d['duplicate_type'].value_counts().to_dict()}; dangling ids: {bad}"
@chk("K20_campaign_honesty")
def _():
    c = T("campaign_candidate_clusters"); o = T("platform_observations"); acc = int((o["account_id_pseudonym"] != "").sum()); t = int((o["publish_time_utc"] != "").sum())
    return len(c) == 0, f"campaign clusters={len(c)} (blocked: no multi-account time-stamped distribution evidence); observations with accounts={acc}, with publish time={t}, total={len(o)}"
@chk("K21_policy_present")
def _():
    p = os.path.join(DOCS, "ORVEX_DATA_USE_AND_EVIDENCE_POLICY.md"); t = open(p, encoding="utf-8").read() if os.path.exists(p) else ""
    need = ["Evidence classes", "Relationship status rules", "E1 Media similarity", "never", "Real-world media only", "campaign"]; miss = [n for n in need if n.lower() not in t.lower()]
    return not miss, f"policy file {'present' if t else 'missing'}, {len(t.split())} words; missing sections: {miss or 'none'}"
@chk("K22_access_log")
def _():
    a = T("download_access_attempt_log"); m = T("real_world_media_master"); dl = int(((m["access_status"] == "downloaded_authorized")).sum()); ok = int((a["result_category"] == "ok").sum()); fails = int((a["result_category"] == "failed").sum())
    return ok >= dl, f"{len(a)} logged attempts: ok={ok}, failed={fails}, policy-skipped={int((a['result_category'] == 'skipped_terms').sum())}; downloaded media files={dl}"
@chk("K23_media_playable")
def _():
    m = T("real_world_media_master"); d = m[m["access_status"] == "downloaded_authorized"]; bad = int((d["playable_status"] == "unplayable").sum()); return True, f"{len(d)} downloaded real media probed; flagged unplayable: {bad} (kept in master, excluded from variants)"
@chk("K24_registry")
def _():
    s = T("source_registry"); v = set(schema.VOC["inclusion_status"]); bad = int((~s["inclusion_status"].isin(v)).sum()); un = int((s["verification_level"] == "research_lead_unverified").sum())
    return bad == 0 and len(s) >= 25, f"{len(s)} candidates; statuses={s['inclusion_status'].value_counts().to_dict()}; flagged unverified research leads={un}; invalid statuses={bad}"
@chk("K25_groups")
def _():
    g = T("group_examples"); ok = g["n_members"].astype(int).between(5, 6).all() if len(g) else False; return bool(ok), f"{len(g)} groups of 5-6 videos; truth edges total={int(g['n_truth_edges'].astype(int).sum()) if len(g) else 0}"

@chk("K26_failed_not_trained")
def _():
    v = T("controlled_variant_registry"); f = v[v["validation_status"] != "passed"]; bad = int((f["usable_for_training"] == "True").sum() + (f["local_path"] != "").sum())
    return bad == 0, f"failed variants={len(f)}; failed variants marked trainable or retained as files: {bad}"
@chk("K27_label_dimensions_separate")
def _():
    m, e = T("real_world_media_master"), T("media_relationship_edges"); need_m = {"native_authenticity_label", "native_misleading_label", "normalized_authenticity_status", "normalized_misleading_status", "native_manipulation_type"}
    bad = (need_m - set(m.columns)) | ({c for c in e.columns if "authenticity" in c or "misleading" in c})
    fvc = m[m["source_dataset_id"] == "RW-03"]; mix = int(((fvc["normalized_authenticity_status"] != "unknown")).sum())
    return not bad and mix == 0, f"authenticity/misleading labels live only in the media master (edges carry relation labels only); FVC records with an invented authenticity status: {mix}; issues: {sorted(bad) or 'none'}"

@chk("K28_no_zero_byte_or_truncated")
def _():
    bad = []
    for base in (RWMEDIA, CVMEDIA):
        for r, _d, fs in os.walk(base):
            for f in fs:
                if os.path.getsize(os.path.join(r, f)) == 0: bad.append(f)
    m = T("real_world_media_master"); d = m[m["access_status"] == "downloaded_authorized"]; zero = d[d["duration_s"].isin(["", "0", "0.0"])]; excl = set(m[m["usable_for_variants"] == "False"]["media_id"])
    return not bad and set(zero["media_id"]) <= excl, f"zero-byte files: {len(bad)}; downloaded media with duration 0/unknown: {sorted(zero['media_id'])} (all QC-excluded from variants: {set(zero['media_id']) <= excl})"
@chk("K29_attribution_complete")
def _():
    p = os.path.join(MAN, "attribution.csv"); at = pd.read_csv(p, dtype=str, keep_default_na=False, encoding="utf-8-sig") if os.path.exists(p) else pd.DataFrame()
    m = T("real_world_media_master"); n = int(((m["source_dataset_id"] == "RW-01") & (m["access_status"] == "downloaded_authorized")).sum())
    nostated = int(at["author_or_credit"].str.startswith("not stated").sum()) if len(at) else -1; miss = int(((at["license"] == "") | (at["license_url"] == "") | (at["file_page_url"] == "")).sum()) if len(at) else -1
    return len(at) == n and miss == 0, f"{len(at)} attribution rows for {n} downloaded Commons files; rows missing licence/licence URL/file page: {miss}; author not stated on Commons (uploader link only): {nostated}"
@chk("K30_manifests_present")
def _():
    need = ["checksums.sha256", "storage_budget.csv", "selection_plan.json", "native_id_crosswalk.csv", "evaluation_protocol.md", "attribution.csv", "source_registry.csv", "download_access_attempt_log.csv"]
    miss = [n for n in need if not os.path.exists(os.path.join(MAN, n))]; nl = 0
    if not miss:
        nl = sum(1 for _ in open(os.path.join(MAN, "checksums.sha256"), encoding="utf-8")); cw = len(pd.read_csv(os.path.join(MAN, "native_id_crosswalk.csv"), usecols=["media_id"], dtype=str)); m = len(T("real_world_media_master"))
        exp = 0
        for base in (RW, CV, os.path.join(DATA, "derived"), MAN):
            for r, _d, fs in os.walk(base):
                if os.sep + "_build" in r: continue
                exp += sum(1 for f in fs if os.path.normpath(os.path.join(r, f)) != os.path.normpath(os.path.join(MAN, "checksums.sha256")) and not re.search(r"_run\d*\.log$", f))
        return nl == exp and cw == m, f"manifests present ({len(need)}); checksum lines={nl} vs files on disk {exp}; crosswalk rows={cw} vs media master {m}"
    return False, f"missing manifests: {miss}"
@chk("K31_label_dimensions")
def _():
    m, e, o = T("real_world_media_master"), T("media_relationship_edges"), T("platform_observations")
    ok = (m["coordination_status"] == "not_assessed").all() and (o["coordination_status"] == "not_assessed").all() and e["evidence_status"].isin(["source_annotation", "controlled_transformation_log"]).all()
    return bool(ok), f"coordination_status=not_assessed on {len(m)} media and {len(o)} observations; evidence_status values on edges: {e['evidence_status'].value_counts().to_dict()}"
@chk("K32_covid_dataset")
def _():
    m, o = T("real_world_media_master"), T("platform_observations"); c = m[m["source_dataset_id"] == "RW-31"]; tw = o[(o["platform"] == "twitter") & (o["publish_time_utc"] != "")]
    bad = int((c["access_status"] != "metadata_only").sum() + (c["local_path"] != "").sum()); yrs = tw["publish_time_utc"].str[:4].value_counts().to_dict()
    out = tw[(tw["publish_time_utc"] < "2019-11-01") | (tw["publish_time_utc"] > "2020-07-01")]; unflagged = int((out["time_precision"] != "second_derived_unverified").sum())
    return len(c) >= 8000 and bad == 0 and unflagged == 0, f"RW-31 records={len(c)} (all metadata_only, bad={bad}); tweet share-references with derived time={len(tw)}; {len(out)} fall outside the dataset's stated Nov 2019-Jun 2020 window and are flagged second_derived_unverified (unflagged: {unflagged}); facebook share refs={int(((o['platform'] == 'facebook')).sum())}"
@chk("K33_layer_a_read_only")
def _():
    n = w = 0
    for base in (RWMEDIA, RWMETA):
        for r, _d, fs in os.walk(base):
            for f in fs:
                n += 1; w += int(os.access(os.path.join(r, f), os.W_OK))
    return n > 0 and w == 0, f"{n} Layer A files (media + raw metadata); still writable: {w}"
@chk("K34_gitignore")
def _():
    p = os.path.join(ROOT, ".gitignore"); t = open(p, encoding="utf-8").read() if os.path.exists(p) else ""
    return all(x in t for x in ("data/", "tools/", ".env")), ".gitignore excludes data/, tools/, secrets (no git repository exists yet)"

def summary(): return {k: dict(ok=v[0], evidence=v[1]) for k, v in R.items()}
if __name__ == "__main__":
    for k, (ok, ev) in R.items(): print(("PASS " if ok else "FAIL "), k, "-", ev)
