# -*- coding: utf-8 -*-
"""Feature-readiness baseline (NOT the ORVEX model): non-learned 24-frame dHash frame-matching on the existing labelled pairs.
Threshold 0.45 is fixed a priori (same value used for duplicate detection); nothing is tuned on val/test. Ground truth and predictions stay separate."""
import os, sys, json, time
import numpy as np, pandas as pd
from sklearn.metrics import roc_auc_score
sys.path.insert(0, os.path.dirname(__file__))
from common import *
OUT = os.path.join(DOCS, "necessity_audit"); os.makedirs(OUT, exist_ok=True)
THR = 0.45
H = {}; A = {}
for l in open(os.path.join(FEAT, "visual_dhash24.jsonl"), encoding="utf-8"):
    j = json.loads(l); H[j["media_id"]] = np.array([int(x, 16) for x in j["dhash24"]], dtype=np.uint64)
for l in open(os.path.join(FEAT, "audio_fingerprint.jsonl"), encoding="utf-8"):
    j = json.loads(l); A[j["media_id"]] = (j["audio_md5_8k"], j["audio_env_1s"])
def frac(a, b):
    if len(a) == 0 or len(b) == 0: return np.nan
    d = np.bitwise_count(a[:, None] ^ b[None, :]); return float((d.min(1) <= 8).mean())
def score(a, b): return max(frac(H[a], H[b]), frac(H[b], H[a]))
tp = pd.read_csv(os.path.join(TAB, "training_pairs.csv"), dtype=str, keep_default_na=False, encoding="utf-8-sig"); tp = tp[tp["split"] != "excluded"].copy()
v = pd.read_csv(os.path.join(TAB, "controlled_variant_registry.csv"), dtype=str, keep_default_na=False, encoding="utf-8-sig"); vp = v[v["validation_status"] == "passed"]; tname = dict(zip(vp["variant_media_id"], vp["transformation_name"]))
t0 = time.perf_counter(); tp["score"] = [score(a, b) if a in H and b in H else np.nan for a, b in zip(tp["media_a_id"], tp["media_b_id"])]; lat = (time.perf_counter() - t0) / len(tp) * 1000
tp["audio_identical"] = [int(A.get(a, ("", ""))[0] != "" and A.get(a, ("", ""))[0] == A.get(b, ("", ""))[0]) for a, b in zip(tp["media_a_id"], tp["media_b_id"])]
tp = tp.dropna(subset=["score"]); tp["y"] = tp["label_binary_related"].astype(int); R = {"threshold_fixed_a_priori": THR, "pairs_scored": int(len(tp)), "latency_ms_per_pair": round(lat, 4)}; rows = []
def auc(df): return round(float(roc_auc_score(df["y"], df["score"])), 4) if df["y"].nunique() == 2 and int((df["y"] == 0).sum()) >= 20 and int((df["y"] == 1).sum()) >= 20 else None   # n/a if <20 negatives or positives
for sp in ("train", "val", "test"):
    d = tp[tp["split"] == sp]; R[f"auc_{sp}"] = auc(d)
te = tp[tp["split"] == "test"]; R["test_negatives_by_hardness"] = te[te["y"] == 0]["hardness"].value_counts().to_dict(); R["auc_test_hard_negatives_only"] = auc(te[(te["y"] == 1) | ((te["hardness"] == "hard") & (te["relationship_class"] == "unrelated_distinct_source"))]); R["auc_test_easy_negatives_only"] = auc(te[(te["y"] == 1) | ((te["hardness"] == "easy") & (te["relationship_class"] == "unrelated_distinct_source"))])
R["auc_test_without_heldout_lineage"] = auc(te[te["includes_heldout_transform"] != "True"]); R["auc_test_heldout_lineage_pos_vs_all_neg"] = auc(te[(te["y"] == 0) | (te["includes_heldout_transform"] == "True")])
R["detection_rate_threshold"] = {c: round(float((g["score"] >= THR).mean()), 3) for c, g in tp.groupby("relationship_class")}
dd = tp[tp["relationship_class"] == "direct_derivation"].copy(); dd["t"] = [tname.get(b, tname.get(a, "")) for a, b in zip(dd["media_a_id"], dd["media_b_id"])]
R["direct_derivation_detection_by_transformation"] = {k: dict(n=int(len(g)), detected=round(float((g["score"] >= THR).mean()), 3), audio_identical=round(float(g["audio_identical"].mean()), 3)) for k, g in dd.groupby("t")}
# temporal alignment check on trims: start fraction of the variant inside its original, estimated from matched sampled frames
errs = []; GT = {"trim_middle": 0.15, "trim_head": 0.20, "trim_tail": 0.0}
for _, r in vp[vp["transformation_name"].isin(GT) & (vp["generation_depth"] == "1")].iterrows():
    a, b = r["root_source_media_id"], r["variant_media_id"]
    if a not in H or b not in H or len(H[a]) < 2 or len(H[b]) < 2: continue
    d = np.bitwise_count(H[b][:, None] ^ H[a][None, :]); j0 = int(d[0].argmin()); errs.append((r["transformation_name"], abs(j0 / (len(H[a]) - 1) - GT[r["transformation_name"]]), int(d[0].min() <= 8)))
e = pd.DataFrame(errs, columns=["t", "err", "matched"]); R["temporal_start_estimation"] = dict(n=int(len(e)), mean_abs_error_fraction=round(float(e["err"].mean()), 4), within_0_05=round(float((e["err"] <= 0.05).mean()), 3), first_frame_matched=round(float(e["matched"].mean()), 3),
        per_type={k: round(float(g["err"].mean()), 4) for k, g in e.groupby("t")}, note="24 sampled frames give ~4% granularity; finer segment bounds need denser frame sampling (computation, not data)")
json.dump(R, open(os.path.join(OUT, "dhash_baseline_results.json"), "w", encoding="utf-8"), indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
ver = "dhash24-frame-match v1 (non-learned)"; ref = "docs/datasets/necessity_audit/dhash_baseline_results.json"
def row(metric, val, proto): rows.append(dict(experiment_id="BASE-DHASH-v1", dataset_versions="tables snapshot of 2026-10-26 (see checksums.sha256)", split_version="split-v1", label_map_version="labelmap-v1", model_version="none: non-learned baseline, threshold fixed a priori 0.45; NOT the ORVEX relationship model",
                  feature_version=ver, metric_name=metric, metric_value=val, protocol=proto, heldout_policy="T11-T14 lineage test-only; reported separately", report_path=ref, leakage_test_result="K13/K14 pass in the same audit run"))
for sp in ("train", "val", "test"): row(f"roc_auc_related_vs_unrelated_{sp}", R[f"auc_{sp}"], f"all labelled pairs in {sp} split, score = max directional matched-frame fraction")
row("roc_auc_test_hard_negatives_only", R["auc_test_hard_negatives_only"] if R["auc_test_hard_negatives_only"] is not None else "", "test split, same-theme hard negatives only (blank = fewer than 20 negatives)"); row("roc_auc_test_without_heldout_lineage", R["auc_test_without_heldout_lineage"], "test split excluding held-out transformation lineage")
row("roc_auc_test_heldout_lineage_positives", R["auc_test_heldout_lineage_pos_vs_all_neg"], "test split: held-out-lineage positives vs all negatives")
row("temporal_start_mae_fraction", R["temporal_start_estimation"]["mean_abs_error_fraction"], "trim variants vs their roots, first-frame match position"); row("pair_scoring_latency_ms", R["latency_ms_per_pair"], "mean CPU time per pair, 24x24 Hamming matrix (not end-to-end time-to-detection)")
emit("experiment_registry", [dict(r, experiment_id=f"BASE-DHASH-v1-{i + 1:02d}") for i, r in enumerate(rows)])
print(json.dumps(R, indent=1)[:3500])
