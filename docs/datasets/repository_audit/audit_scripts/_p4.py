p = "ra3c_reports.py"; s = open(p, encoding="utf-8").read()
a = 'FM = pd.read_csv(OUT / "repository_file_manifest.csv")'
assert a in s; s = s.replace(a, 'FM = pd.read_csv(WORK / "file_to_dataset_map.csv")'); open(p, "w", encoding="utf-8").write(s); print("ok")
