# -*- coding: utf-8 -*-
"""Gate 1/6 manifests: crosswalk, attribution, selection plan, storage budget, evaluation protocol, checksums, .gitignore, read-only protection of Layer A."""
import os, sys, json, csv, re, stat, glob
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from common import *
import candidates
D = lambda t: pd.read_csv(os.path.join(ROOT, __import__("schema").TABLES[t]["path"]), dtype=str, keep_default_na=False, encoding="utf-8-sig")
m = D("real_world_media_master"); v = D("controlled_variant_registry"); NOW = now()

# 1) native id -> internal id crosswalk
cw = m[["source_dataset_id", "release_version", "native_record_id", "native_media_id", "platform", "platform_media_id", "source_url", "canonical_url", "media_id"]]
cw.to_csv(os.path.join(MAN, "native_id_crosswalk.csv"), index=False, encoding="utf-8-sig"); print("crosswalk rows", len(cw))

# 2) attribution (licence compliance for CC BY / BY-SA) + dataset citations
cj = {f"RW-CMN-P{c['pageid']}": c for c in json.load(open(os.path.join(RWMETA, "commons", "commons_candidates.json"), encoding="utf-8"))}
att = []
for _, r in m[(m["source_dataset_id"] == "RW-01") & (m["access_status"] == "downloaded_authorized")].iterrows():
    c = cj[r["media_id"]]; att.append(dict(media_id=r["media_id"], title=c["title"], author_or_credit=(c["author"] or c["credit"] or "").strip() or "not stated on Commons (uploader: see file page)", license=c["license"], license_url=c["license_url"] or ("n/a (public domain: Commons provides no licence text)" if "public domain" in c["license"].lower() else "not provided by the Commons API"),
                                          file_page_url=c["page_url"], attribution_required=c["attribution_required"], used_as_variant_source=r["usable_for_variants"], retrieved=r["collected_time_utc"]))
pd.DataFrame(att).to_csv(os.path.join(MAN, "attribution.csv"), index=False, encoding="utf-8-sig")
md = ["# ORVEX Attribution and Citations", "", f"Generated {NOW}. Licence terms must be re-verified on each file page before any public release. CC BY-SA derivatives (variants) must carry CC BY-SA if shared.", "", "## Dataset citations",
      "- InVID Fake Video Corpus 2018 (v3): Papadopoulou, Zampoglou, Papadopoulos, Kompatsiaris. Zenodo 2535479, CC BY 4.0. https://zenodo.org/records/2535479",
      "- InVID Fake Video Corpus v2.0: Papadopoulou et al. Zenodo 1147958, CC BY 4.0. https://zenodo.org/records/1147958", "- InVID Fake Video Corpus v1.0: Papadopoulos et al. Zenodo 242481, CC BY 4.0. https://zenodo.org/records/242481",
      "- InVID FIVR-200K: Kordopatis-Zilos, Papadopoulos, Patras, Kompatsiaris. Zenodo 2564864, CC BY 4.0. https://zenodo.org/records/2564864", "- VCSL: He et al., CVPR 2022. https://github.com/alipay/VCSL (code MIT; dataset licence not stated).",
      "- ANAKIN: Black et al. (VADER, ICCV 2023). cc-by-4.0 per card. https://huggingface.co/datasets/AlexBlck/ANAKIN",
      "- A dataset of Covid-related misinformation videos and their spread on social media: Knuutila. Zenodo 4557828, CC BY 4.0. https://zenodo.org/records/4557828", "", "## Wikimedia Commons media (RW-01)", "",
      "| media id | title | author / credit | licence | file page |", "|---|---|---|---|---|"]
for a in att: md.append("| " + " | ".join(str(a[k]).replace("|", "/").replace("\n", " ")[:90] for k in ("media_id", "title", "author_or_credit", "license", "file_page_url")) + " |")
open(os.path.join(DOCS, "ORVEX_ATTRIBUTION.md"), "w", encoding="utf-8").write("\n".join(md)); print("attribution rows", len(att))

# 3) selection / sampling plan
json.dump(dict(generated=NOW, search_date="2026-10-26", search_terms=candidates.SEARCH_TERMS, candidates_considered=len(candidates.C),
  commons=dict(queries=[q for q in __import__("s2_collect_media").QUERIES], per_query_max_new_files=4, file_size_bytes=[300000, 45000000], licence_gate="CC0 | Public domain | CC BY | CC BY-SA (NC/ND/unknown rejected)", stem_dedupe="first 18 letters of normalised title",
                qc="duration 8-120 s, height >=240, no decode errors, not mostly black/static, no exact/near duplicate (dHash >=45% frame match), not non-real-world CGI/simulation (keyword screen + manual list)"),
  anakin=dict(rule="sort by sha256('orvex-anakin-v1'+video-id); first 50 per manipulation type while cumulative planned bytes <= 3 GB; full-length videos excluded", selected_pairs=250),
  variants=dict(transformations="T01-T14", chains="C1-C5", donor_and_caption_pick="sha256 of root media id over eligible pool (other-theme donors preferred)", test_only_types=["T11", "T12", "T13", "T14"]),
  splits=dict(unit="source family; Commons families grouped by search theme", pattern="14 train / 3 val / 3 test per 20 themes (Commons) or families (ANAKIN), stride 7 over sorted order", seed="orvex-split-20261026", version="split-v2"),
  negatives=dict(easy="different search theme", hard="same search theme (label uncertain)", within="same split only")), open(os.path.join(MAN, "selection_plan.json"), "w", encoding="utf-8"), indent=1)

# 4) evaluation protocol
proto = """# ORVEX Evaluation Protocol (data side)

1. **Unseen source videos**: all `split=test` families are never used for training/validation; every variant, pair and group of a family stays in its split (checked by K13).
2. **Held-out transformation types**: T11 mirror_color_shift, T12 speed_change, T13 reupload_sim, T14 audio_noise_mix. Variants with these in their lineage are `usable_for_training=False`; their pairs are in the test split only (K14). Report results with and without them.
3. **Real edits**: ANAKIN pairs (`edited_version`) in the test split are an external check on human-made edits (not generated by ORVEX).
4. **Hard negatives**: `unrelated_distinct_source` pairs with `hardness=hard` share a search theme; they are labelled `uncertain` and must be reported separately from easy negatives.
5. **Same-incident vs copy**: FIVR DS/CS/ND relations and VCSL segments exist as native edges with `media_available_locally=False`; they can be used once media access is lawfully obtained, never to claim derivation direction.
6. **Metrics to record in `experiment_registry`**: precision, recall, false-positive rate at fixed threshold, direction accuracy, transformation-type accuracy, graph/edge precision-recall, time-to-detection, per held-out transformation degradation. No experiment has been run yet.
7. **Leakage test**: `tests/test_dataset_package.py::test_acceptance_check[K13_split_leakage]` and `K14_heldout_policy` must pass before any result is reported.
"""
open(os.path.join(DOCS, "ORVEX_EVALUATION_PROTOCOL.md"), "w", encoding="utf-8").write(proto); open(os.path.join(MAN, "evaluation_protocol.md"), "w", encoding="utf-8").write(proto)

# 5) .gitignore (no git repository exists yet; protects against committing media/secrets if one is initialised)
gi = os.path.join(ROOT, ".gitignore")
if not os.path.exists(gi): open(gi, "w", encoding="utf-8").write("# ORVEX: never commit media, datasets, tools or secrets\ndata/\ntools/\n*.mp4\n*.webm\n*.ogv\n*.zip\n.env\n*.key\n*.pem\ncredentials*\n__pycache__/\n")

# 6) Layer A read-only protection
n = 0
for base in (RWMEDIA, RWMETA):
    for r, _, fs in os.walk(base):
        for f in fs:
            p = os.path.join(r, f)
            try: os.chmod(p, stat.S_IREAD); n += 1
            except OSError: pass
print("Layer A files set read-only:", n)

# 7) storage budget log (allocations vs measured + stage measurements recorded in run logs)
rows = []; cat = {"real-world raw metadata": RWMETA, "real-world media: Commons": os.path.join(RWMEDIA, "commons"), "real-world media: ANAKIN subset": os.path.join(RWMEDIA, "anakin"), "controlled variants (media)": CVMEDIA,
       "derived tables": TAB, "derived features": FEAT, "derived splits": SPL, "manifests/logs/build": MAN, "reports": REP}
alloc = {"real-world raw metadata": 0.4e9, "real-world media: Commons": 3.0e9, "real-world media: ANAKIN subset": 3.0e9, "controlled variants (media)": 14.0e9, "derived tables": 1.0e9}
for k, p in cat.items():
    b = dir_bytes(p); rows.append(dict(kind="final_category", name=k, bytes=b, GB_decimal=round(b / 1e9, 3), GiB=round(b / 2 ** 30, 3), allocation_bytes=int(alloc.get(k, 0)), within_allocation=("yes" if b <= alloc.get(k, 1e12) else "NO"), source="measured by du-equivalent walk"))
tot = payload_bytes(); rows.append(dict(kind="final_total", name="dataset payload (all of data/)", bytes=tot, GB_decimal=round(tot / 1e9, 3), GiB=round(tot / 2 ** 30, 3), allocation_bytes=int(CAP_HARD), within_allocation="yes" if tot < CAP_TARGET else "NO", source="cap 30 GB, target 27 GB, stop 29 GB"))
def logmax(path, pat):
    out = []
    if os.path.exists(path):
        for l in open(path, encoding="utf-8", errors="ignore"):
            mm = re.search(pat, l)
            if mm: out.append((l.strip()[:60], int(mm.group(1))))
    return out
for logf in ("s2_run.log", "s4_run.log", "s456_run.log"):
    for line, b in logmax(os.path.join(MAN, logf), r"payload(?: before| after)?:? (\d{6,})"):
        rows.append(dict(kind="stage_measurement", name=f"{logf}: {line}", bytes=b, GB_decimal=round(b / 1e9, 3), GiB=round(b / 2 ** 30, 3), allocation_bytes="", within_allocation="yes" if b < CAP_STOP else "NO", source=f"printed by the script in {logf}"))
for logf in ("s356_run.log",):
    for line, b in logmax(os.path.join(MAN, logf), r"payload (\d{6,})"):
        rows.append(dict(kind="stage_measurement", name=f"{logf}: after features/pairs stage", bytes=b, GB_decimal=round(b / 1e9, 3), GiB=round(b / 2 ** 30, 3), allocation_bytes="", within_allocation="yes" if b < CAP_STOP else "NO", source=f"printed by the script in {logf}"))
peak = max([r["bytes"] for r in rows if r["kind"] != "final_category"] + [0]); rows.append(dict(kind="peak_recorded", name="largest recorded payload measurement", bytes=peak, GB_decimal=round(peak / 1e9, 3), GiB=round(peak / 2 ** 30, 3), allocation_bytes=int(CAP_HARD), within_allocation="yes" if peak < CAP_STOP else "NO", source="max of stage measurements (definition: decimal bytes under data/)"))
pd.DataFrame(rows).to_csv(os.path.join(MAN, "storage_budget.csv"), index=False, encoding="utf-8-sig")

# 8) checksums (media reuse the hashes already stored in the tables; other files hashed here)
known = {}
for _, r in m[m["sha256"] != ""].iterrows(): known[os.path.normpath(os.path.join(ROOT, r["local_path"]))] = r["sha256"]
for _, r in v[v["sha256"] != ""].iterrows(): known[os.path.normpath(os.path.join(ROOT, r["local_path"]))] = r["sha256"]
lines = []; out = os.path.join(MAN, "checksums.sha256")
for base in (RW, CV, os.path.join(DATA, "derived"), MAN):
    for r, _, fs in os.walk(base):
        if os.sep + "_build" in r: continue
        for f in sorted(fs):
            p = os.path.normpath(os.path.join(r, f))
            if p == os.path.normpath(out) or re.search(r"_run\d*\.log$", f): continue      # volatile run logs are excluded
            lines.append(f"{known.get(p) or sha256(p)}  {rel(p)}")
open(out, "w", encoding="utf-8").write("\n".join(lines) + "\n"); print("checksums lines", len(lines), "payload", payload_bytes())
