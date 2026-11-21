# -*- coding: utf-8 -*-
"""Gate 1/2: reproducible fetch of OFFICIAL metadata/annotation files (no media). Verifies Zenodo md5; skips files already present (re-verifying them)."""
import os, sys, json, hashlib, zipfile
sys.path.insert(0, os.path.dirname(__file__))
from common import *
Z = {"2535479": ("RW-03", "invid_fvc_2018"), "1147958": ("RW-04", "invid_fvc_v2"), "242481": ("RW-05", "invid_fvc_v1"), "2564864": ("RW-06", "invid_fivr200k")}
GH = ["videos_url_uuid.csv", "label_file_uuid_total.json", "pair_file_train.csv", "pair_file_val.csv", "pair_file_test.csv", "video_categories.json", "split_meta_pairs.json"]
import requests
for rid, (ds, d) in Z.items():
    api = os.path.join(RWMETA, "zenodo_api", f"zenodo_{rid}.json")
    if not os.path.exists(api): http_get(f"https://zenodo.org/api/records/{rid}", api, ds, f"zenodo_api_{rid}")
    j = json.load(open(api, encoding="utf-8"))
    for f in j["files"]:
        out = os.path.join(RWMETA, d, f["key"].replace(" ", "_"))
        if not os.path.exists(out): http_get(f["links"]["self"], out, ds, f["key"])
        md5 = hashlib.md5(open(out, "rb").read()).hexdigest(); print(rid, f["key"], "md5 OK" if "md5:" + md5 == f["checksum"] else "MD5 MISMATCH")
        if not os.path.isdir(os.path.join(RWMETA, d, "extracted")): zipfile.ZipFile(out).extractall(os.path.join(RWMETA, d, "extracted"))
for f in GH:
    out = os.path.join(RWMETA, "vcsl", f)
    if not os.path.exists(out): http_get(f"https://raw.githubusercontent.com/alipay/VCSL/main/data/{f}", out, "RW-07", f)
os.makedirs(os.path.join(RWMETA, "hf_api"), exist_ok=True)
for nm, url in (("anakin_metadata.csv", "https://huggingface.co/datasets/AlexBlck/ANAKIN/raw/main/metadata.csv"), ("anakin_blobs.json", "https://huggingface.co/api/datasets/AlexBlck/ANAKIN?blobs=true"), ("anakin.json", "https://huggingface.co/api/datasets/AlexBlck/ANAKIN")):
    out = os.path.join(RWMETA, "hf_api", nm)
    if not os.path.exists(out): http_get(url, out, "RW-02", nm)
print("metadata present; payload", payload_bytes())
