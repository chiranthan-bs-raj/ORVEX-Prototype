p = "ra2_datasets_dictionary.py"; s = open(p, encoding="utf-8").read()
a = '''_rows = list(_csv.reader(open(ROOT / _p, encoding="utf-8-sig"))); _h = _rows[0]; _body = [r + [""] * (len(_h) - len(r)) for r in _rows[1:]]'''
b = '''_rows = list(_csv.reader(open(ROOT / _p, encoding="utf-8-sig"))); _w = max(len(r) for r in _rows); _h = _rows[0] + [f"(unnamed trailing field {i})" for i in range(len(_rows[0]) + 1, _w + 1)]; _body = [r + [""] * (_w - len(r)) for r in _rows[1:]]'''
assert a in s; s = s.replace(a, b)
a2 = '''ragged_rows=int(sum(1 for r in _rows[1:] if len(r) != len(_h)))'''
b2 = '''ragged_rows=int(sum(1 for r in _rows[1:] if len(r) != len(_rows[0]))), max_fields=_w, header_fields=len(_rows[0])'''
assert a2 in s; s = s.replace(a2, b2); open(p, "w", encoding="utf-8").write(s); print("patched")
