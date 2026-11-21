# -*- coding: utf-8 -*-
"""Shared helpers for the READ-ONLY repository audit. Nothing here writes outside docs/datasets/repository_audit/."""
import os, sys, json, ast, re, glob, hashlib, subprocess
from pathlib import Path
import pandas as pd

ROOT = Path(r"<repo>")
OUT = ROOT / "docs" / "datasets" / "repository_audit"
WORK = OUT / "_work"
for p in (OUT, WORK): p.mkdir(parents=True, exist_ok=True)
FFPROBE = next(iter(glob.glob(str(ROOT / "tools" / "ffmpeg-*" / "bin" / "ffprobe.exe"))), "ffprobe")
AUDIT_DATE = "2026-10-27"

def safe_out(name):
    """Never overwrite an existing file: pick a differentiated name instead."""
    p = OUT / name; i = 2
    while p.exists():
        p = OUT / f"{Path(name).stem}_audit{i}{Path(name).suffix}"; i += 1
    return p
def rel(p): return str(Path(p).resolve().relative_to(ROOT)).replace("\\", "/")
def dir_stats(path):
    n = b = 0
    p = Path(path)
    if p.is_file(): return 1, p.stat().st_size
    for r, _, fs in os.walk(p):
        for f in fs:
            try: b += os.path.getsize(os.path.join(r, f)); n += 1
            except OSError: pass
    return n, b
def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""): h.update(c)
    return h.hexdigest()
def read_table(path, nrows=None):
    path = str(path); low = path.lower()
    sep = "\t" if low.endswith(".tsv") else ","
    return pd.read_csv(path, sep=sep, dtype=str, keep_default_na=False, encoding="utf-8-sig", low_memory=False, nrows=nrows, compression="infer")

# ---- AST index of project code: (file -> [(start, end, qualified name)])
def code_index():
    idx = {}
    for f in list((ROOT / "scripts").rglob("*.py")) + list((ROOT / "tests").rglob("*.py")) + list((OUT / "audit_scripts").rglob("*.py")):
        try: tree = ast.parse(f.read_text(encoding="utf-8"))
        except Exception: continue
        items = []
        for n in ast.walk(tree):
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)): items.append((n.lineno, getattr(n, "end_lineno", n.lineno), n.name))
        idx[rel(f)] = sorted(items)
    return idx
def enclosing(idx, file, line):
    best = None
    for s, e, n in idx.get(file, []):
        if s <= line <= e and (best is None or s >= best[0]): best = (s, e, n)
    return best[2] if best else "<module>"
def func_lines(idx, file, name):
    for s, e, n in idx.get(file, []):
        if n == name: return f"{file}:{n} (lines {s}-{e})"
    return None
def grep_code(pattern, flags=0):
    """[(file, line, function, text)] for project code lines matching a regex."""
    idx = code_index(); out = []; rx = re.compile(pattern, flags)
    for f in idx:
        if f.startswith("docs/datasets/repository_audit"): continue      # the audit must not count itself as project usage
        for i, line in enumerate((ROOT / f).read_text(encoding="utf-8").splitlines(), 1):
            if rx.search(line): out.append((f, i, enclosing(idx, f, i), line.strip()[:160]))
    return out
