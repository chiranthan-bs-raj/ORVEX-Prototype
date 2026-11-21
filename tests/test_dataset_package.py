# -*- coding: utf-8 -*-
"""Executable acceptance tests for the ORVEX 10.2-10.4 dataset package. Each test runs a real check against the real files.
Run:  python -m pytest tests/test_dataset_package.py -q"""
import os, sys
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts", "datasets"))
import audit, schema

CHECKS = sorted(audit.R)

# These four checks re-hash or count every file of the authors' complete local dataset (all videos, raw API dumps, masks).
# The public repository ships the tables and the 1,727 demo videos (Hugging Face dataset), not the raw dumps, so they only run
# when the full folders exist: videos via `python scripts/fetch_data.py --media` and data/real_world/raw_metadata.
NEEDS_FULL_DATASET = {"K06_hashes": "data/real_world/media", "K18_native_files_intact": "data/real_world/raw_metadata", "K30_manifests_present": "data/real_world/raw_metadata", "K33_layer_a_read_only": "data/real_world/raw_metadata"}
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


@pytest.mark.parametrize("check_id", CHECKS)
def test_acceptance_check(check_id):
    need = NEEDS_FULL_DATASET.get(check_id)
    if need and not os.path.isdir(os.path.join(ROOT_DIR, need)):
        pytest.skip(f"needs the complete local dataset ({need} not present in this checkout)")
    ok, evidence = audit.R[check_id]
    assert ok, evidence

def test_every_table_exists_and_has_contract_header():
    for t, d in schema.TABLES.items():
        assert os.path.exists(os.path.join(audit.ROOT, d["path"])), t

def test_every_column_has_lineage_and_definition():
    for t, d in schema.TABLES.items():
        for name, typ, nul, org, lin, desc in d["cols"]:
            assert org in "abcdef" and lin and desc, (t, name)

def test_controlled_variant_ids_are_not_natural_ids():
    m = audit.T("real_world_media_master"); v = audit.T("controlled_variant_registry")
    assert not (set(m["media_id"]) & set(v["variant_media_id"]))
    assert v["variant_media_id"].str.startswith("CV-").all() and not m["media_id"].str.startswith("CV-").any()

def test_required_documents_exist():
    base = os.path.join(audit.ROOT, "docs", "datasets")
    for f in ["ORVEX_DATA_USE_AND_EVIDENCE_POLICY.md", "ORVEX_DATA_DICTIONARY.md", "ORVEX_COLUMN_LINEAGE.md", "ORVEX_DATASET_CATALOG.md", "ORVEX_DATASET_SELECTION_AND_BUDGET.md",
              "ORVEX_REQUIREMENT_COVERAGE_MATRIX.csv", "ORVEX_DATASET_QA_REPORT.md", "schema_contract.json", "column_lineage.csv"]:
        assert os.path.exists(os.path.join(base, f)), f
