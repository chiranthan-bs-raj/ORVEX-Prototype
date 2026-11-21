s = open("ra_common.py", encoding="utf-8").read()
a = '    for f in idx:\n        for i, line in enumerate((ROOT / f).read_text(encoding="utf-8").splitlines(), 1):'
assert a in s
s = s.replace(a, '    for f in idx:\n        if f.startswith("docs/datasets/repository_audit"): continue      # the audit must not count itself as project usage\n        for i, line in enumerate((ROOT / f).read_text(encoding="utf-8").splitlines(), 1):')
open("ra_common.py", "w", encoding="utf-8").write(s)
t = open("ra3a_integrity_quality.py", encoding="utf-8").read()
a = 'SCH = json.load(open(WORK / "schema_inspection.json"))'
assert a in t
t = t.replace(a, 'SCH = json.load(open(WORK / ("schema_inspection_fixed.json" if (WORK / "schema_inspection_fixed.json").exists() else "schema_inspection.json")))')
a = 'ftq = SCH["data/real_world/raw_metadata/invid_fvc_2018/extracted/FVC_text_queries.csv"]'
assert a in t
extra = '''F["fvc2018"]["label_values"] = fall["label"].value_counts().to_dict(); F["fvc2018"]["rows_normalised_to_not_assessed"] = int(((master["source_dataset_id"] == "RW-03") & (master["normalized_misleading_status"] == "not_assessed")).sum())
fiv = edges[edges["source_dataset_id"] == "RW-06"]; F["fivr_norm"] = dict(unnormalised_IS_edges=int(((fiv["native_label"] == "IS") & (fiv["normalized_relation_type"] == "IS")).sum()), dangling_edges=int((~fiv["media_b_id"].isin(M_ids)).sum()), by_label=fiv["native_label"].value_counts().to_dict())
_sel = read_table(ROOT / "data/real_world/raw_metadata/hf_api/anakin_selected_subset.csv"); F["anakin_sources"] = dict(selected=len(_sel), distinct_urls=int(_sel["url"].nunique()), metadata_rows=int(len(read_table(ROOT / "data/real_world/raw_metadata/hf_api/anakin_metadata.csv"))), metadata_distinct_urls=int(read_table(ROOT / "data/real_world/raw_metadata/hf_api/anakin_metadata.csv")["url"].nunique()))
'''
t = t.replace(a, extra + a)
open("ra3a_integrity_quality.py", "w", encoding="utf-8").write(t); print("patched")
