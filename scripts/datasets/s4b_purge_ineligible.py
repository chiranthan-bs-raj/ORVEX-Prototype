# -*- coding: utf-8 -*-
"""Remove ORVEX-generated variants (and checkpoints) whose root, audio-donor or caption source is no longer an eligible real-world source.
Only files under data/controlled_variants/media/<root>/ and the matching checkpoint are touched; real-world originals are never modified."""
import os, sys, json, glob, shutil
sys.path.insert(0, os.path.dirname(__file__))
from common import *
import pandas as pd
m = pd.read_csv(os.path.join(TAB, "real_world_media_master.csv"), dtype=str, keep_default_na=False, encoding="utf-8-sig", usecols=["media_id", "source_dataset_id", "usable_for_variants"])
ok = set(m[(m["source_dataset_id"] == "RW-01") & (m["usable_for_variants"] == "True")]["media_id"]); VB = os.path.join(BUILD, "variants"); purged = []
for f in sorted(glob.glob(os.path.join(VB, "*.json"))):
    j = json.load(open(f, encoding="utf-8")); root = os.path.basename(f)[:-5]; need = {root}
    for r in j["recs"]:
        if r["audio_source_media_id"]: need.add(r["audio_source_media_id"])
        if r["caption_text_source_media_id"]: need.add(r["caption_text_source_media_id"])
    if not need <= ok:
        d = os.path.join(CVMEDIA, root.replace("RW-CMN-", "")); assert os.path.abspath(d).startswith(os.path.abspath(CVMEDIA)) and os.path.basename(d).startswith("P")
        if os.path.isdir(d): shutil.rmtree(d)
        os.remove(f); purged.append((root, sorted(need - ok)))
print("purged sources:", len(purged))
for p in purged: print(" ", p)
print("remaining checkpoints:", len(glob.glob(os.path.join(VB, "*.json"))), "eligible pool:", len(ok))
