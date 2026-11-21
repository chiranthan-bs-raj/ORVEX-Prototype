p = "ra3a_integrity_quality.py"; s = open(p, encoding="utf-8").read()
a = 'claim(CR, r"13,659 \(train", len(pairs), "training pairs (total)")'
assert a in s
s = s.replace(a, 'claim(CR, r"\| training_pairs \|[^|]*\| (\d[\d,]*) \(train", len(pairs), "training pairs (total)")')
open(p, "w", encoding="utf-8").write(s); print("ok")
