p = "ra3c_reports.py"; s = open(p, encoding="utf-8").read()
a = "see findings F-002/F-004"; assert a in s; s = s.replace(a, "see findings F-003 (FIVR IS) and F-005 (FVC labels)"); open(p, "w", encoding="utf-8").write(s); print("ok")
