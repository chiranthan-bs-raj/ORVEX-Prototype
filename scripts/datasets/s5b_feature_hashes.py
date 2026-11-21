# -*- coding: utf-8 -*-
"""Fill storage_bytes / feature_sha256 per computed feature record (hash of the stored feature value itself)."""
import os, sys, json, hashlib
sys.path.insert(0, os.path.dirname(__file__))
from common import *
vis = {}; aud = {}
for l in open(os.path.join(FEAT, "visual_dhash24.jsonl"), encoding="utf-8"):
    j = json.loads(l); vis[j["media_id"]] = "|".join(j["dhash24"])
for l in open(os.path.join(FEAT, "audio_fingerprint.jsonl"), encoding="utf-8"):
    j = json.loads(l); aud[j["media_id"]] = (j["audio_md5_8k"], j["audio_env_1s"])
rows = load("feature_manifest"); n = 0
for r in rows:
    if r["extraction_status"] != "computed": continue
    ft = r["feature_type"]
    val = vis.get(r["media_id"], "") if ft == "visual_dhash24" else aud.get(r["media_id"], ("", ""))[0 if ft == "audio_pcm_md5_8k" else 1]
    if val: r["storage_bytes"] = len(val.encode()); r["feature_sha256"] = hashlib.sha256(val.encode()).hexdigest(); n += 1
emit("feature_manifest", rows); print("feature hashes filled:", n, "of", sum(1 for r in rows if r["extraction_status"] == "computed"))
