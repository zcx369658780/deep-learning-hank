"""DLH-4B transfer tests: import identity and canonical-content integrity.

Issue #18 Phase D tests 1-2 plus the dependency/public-API boundary (mirroring
the accepted source-repository standalone-export contract):

1. source/import identity and provenance marker test;
2. source SHA / canonical-content integrity test;
3. dependency boundary and public API surface.
"""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import numpy as np
from scipy import sparse

from deep_learning_hank.two_asset import matlab_faithful_two_asset_ha as oracle

CANONICAL_PATH = Path("src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py")
# Issue #23 (DLH-4D-R3) is the sole Owner-authorized exception to oracle
# immutability: the narrow transfer-FOC liquid-derivative repair changed the
# canonical file.  The post-repair identity below replaces the pre-repair
# 276D2244B389D6EDE140DAF8B1F9B0BE1F4AA859368941CED1A12BA8A5831AB8; the frozen
# Issue #20 config retains the pre-repair value and its identity gate now
# fail-closes against the authorized change (see
# test_dlh_4d_ge_equations.py::test_immutable_oracle_identity_detects_issue23_repair).
REQUIRED_SHA256 = "1795718C469FC3B427CAB8E3D5957C133BEAD6EACC9EF0A25A3EDB7211D1A024"
EXPORT_AUTHORITY = "6469e5a87a00366c1b2af38f27efaa3014206936"
MATLAB_SHA256 = "049136B769560040BC678F828F5D3EC5338DDCAA2090D6BED4E40732F56C3EAE"


def test_canonical_file_sha256_integrity():
    """The committed canonical copy carries the Issue #23 post-repair identity."""
    observed = hashlib.sha256(CANONICAL_PATH.read_bytes()).hexdigest().upper()
    assert observed == REQUIRED_SHA256


def test_provenance_markers_present():
    docstring = oracle.__doc__ or ""
    assert EXPORT_AUTHORITY in docstring
    assert MATLAB_SHA256 in docstring
    assert "HANK_2ASSETS_HJB.m" in docstring
    assert "MATLAB_FAITHFUL_STATIONARY_KFE_CONTAMINATED_ROW_SOLVE_IS_REQUIRED" in docstring
    assert "MATLAB_FAITHFUL_TRANSFER_FOC_USES_BARE_A" in docstring
    assert "MATLAB_FAITHFUL_ILLIQUID_RETURN_TAPER_IS_REQUIRED_NUMERICAL_STABILIZATION" in docstring


def test_dependency_and_public_api_boundary():
    """Only dataclasses/numpy/scipy; no source-repo package import; clean API."""
    tree = ast.parse(CANONICAL_PATH.read_text(encoding="utf-8"))
    imports = {node.names[0].name.split(".")[0] for node in tree.body if isinstance(node, ast.Import)}
    from_imports = {
        node.module.split(".")[0]
        for node in tree.body
        if isinstance(node, ast.ImportFrom) and node.module != "__future__"
    }
    assert imports | from_imports <= {"dataclasses", "numpy", "scipy"}
    assert "ch5_two_asset_hank" not in CANONICAL_PATH.read_text(encoding="utf-8")
    required = {
        "solve_matlab_faithful_hjb",
        "solve_matlab_faithful_stationary_kfe",
        "aggregate_stationary_household",
        "solve_household_steady_state",
    }
    assert required <= set(oracle.__all__)
    assert not any("ge" in name.lower() or "dynamic" in name.lower() for name in oracle.__all__)


def test_faithful_economics_markers():
    """The faithful pairings required by the Owner clarification are present."""
    p = oracle.EconomicParams(0.05, 2.0, 1.0, 0.1, 2.0, 1e-6, 0.0, 0.0)
    # bare-a transfer FOC: at a = 0 the candidate is zero regardless of the ratio.
    assert oracle.transfer_candidate(1.5, 1.0, 0.0, p) == 0.0
    # taper: raah(0) = ra, raah(a_max) = 0.9*ra, interior between.
    result = oracle.matlab_faithful_illiquid_return(np.array([0.0, 1.0, 2.0]), 2.0, 0.04)
    assert result[0] == 0.04 and result[2] == 0.04 * (1.0 - 0.1)
    assert 0.036 < result[1] < 0.04
    # contamination anchor constant from the reference.
    assert oracle.matlab_contaminated_row_index(50) == 17
