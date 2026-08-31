"""DLH-5C (Issue #26) focused tests: stationary KFE contaminated-row singularity diagnostic.

Validates the frozen D0-D3 states, the exact 9-point D1->D2 region-0 scan, the
accepted KFE success/failure reproduction through the accepted API, operator /
structural-rank / row-sum / LU-pivot diagnostics, positive-transition SCC /
closed-class graph diagnostics, the deterministic alternative row-pin set,
bounded sparse smallest-singular-value attempts, deterministic repeat
reproducibility and the bounded root-cause classification.

The module under test is diagnostic-only: it never modifies the accepted
household oracle, the accepted regional implementation/config, or the accepted
KFE solver. The full diagnostic run is cached at module scope.
"""

from __future__ import annotations

import pytest

from deep_learning_hank.two_asset import matlab_contaminated_row_index
from deep_learning_hank.diagnostics.dlh_5c_kfe_singularity import (
    _pin_indices,
    _root_cause_classification,
    build_fixture,
    case_sequence,
    load_config,
    reproduce,
)

CONFIG_PATH = "configs/dlh_5c_kfe_singularity_diagnostic.toml"
N = 800  # 20*20*2


@pytest.fixture(scope="module")
def cfg():
    return load_config(CONFIG_PATH)


@pytest.fixture(scope="module")
def repro(cfg):
    # deterministic full repeat: D0-D3 + 9-point scan, twice from fresh construction
    return reproduce(cfg)


@pytest.fixture(scope="module")
def cases(cfg, repro):
    return {c["case_id"]: c for c in repro["run1"]["cases"]}


@pytest.fixture(scope="module")
def seq(cfg):
    return case_sequence(cfg)


# ---------------------------------------------------------------------------
# Config / indices / scan construction
# ---------------------------------------------------------------------------


def test_config_frozen_d0_d3_values(cfg):
    assert cfg.d0 == (1.0, 0.03)
    assert cfg.d1 == (0.9977278388290097, 0.0299127630152404)
    assert cfg.d2 == (0.998807521160338, 0.029964194758276677)
    assert cfg.d3 == (1.0011941548981047, 0.03003565330704072)


def test_pin_spec_matches_required_set(cfg):
    assert set(cfg.pin_spec) == {"first", "quarter", "accepted", "half", "three_quarter", "last"}
    assert cfg.accepted_pin_fraction == 0.37
    assert cfg.pin_rhs == 0.007


def test_pin_spec_validation_rejects_bad_set(cfg, tmp_path):
    text = open(CONFIG_PATH, "rb").read().decode("utf-8")
    bad = text.replace(
        'pin_spec = ["first", "quarter", "accepted", "half", "three_quarter", "last"]',
        'pin_spec = ["first", "quarter", "accepted"]',
    )
    assert "pin_spec = [\"first\", \"quarter\", \"accepted\"]" in bad
    bad_path = tmp_path / "bad.toml"
    bad_path.write_text(bad, encoding="utf-8")
    with pytest.raises(ValueError):
        load_config(str(bad_path))


def test_pin_indices_match_required_set(cfg):
    index_of, accepted = _pin_indices(N, cfg)
    assert accepted == matlab_contaminated_row_index(N) == 295
    assert set(index_of.values()) == {0, 200, 295, 400, 600, 799}
    assert index_of == {
        "first": 0,
        "quarter": 200,
        "accepted": 295,
        "half": 400,
        "three_quarter": 600,
        "last": 799,
    }


def test_accepted_row_fortran_coordinates(cfg, repro):
    op = repro["run1"]["cases"][2]["operator"]  # d2
    assert op["accepted_row_index"] == 295
    assert (op["accepted_b_index"], op["accepted_a_index"], op["accepted_z_index"]) == (15, 14, 0)


def test_case_sequence_shape_and_scan_endpoints(seq, cfg):
    ids = [c for c, _, _ in seq]
    assert ids[:4] == ["d0", "d1", "d2", "d3"]
    assert ids[4:] == [f"scan_{k}" for k in range(cfg.scan_n_points)]
    scan0 = seq[4][2]
    scan_end = seq[-1][2]
    assert scan0 == cfg.d1
    assert scan_end == cfg.d2
    # linear interpolation check at midpoints
    for k in (1, 4, 7):
        t = k / (cfg.scan_n_points - 1)
        wbar = (1 - t) * cfg.d1[0] + t * cfg.d2[0]
        ra = (1 - t) * cfg.d1[1] + t * cfg.d2[1]
        assert seq[4 + k][2] == pytest.approx((wbar, ra), abs=1e-15)


def test_scan_point_count_and_region_only(cfg):
    assert cfg.scan_n_points == 9
    assert cfg.region_index == 0


# ---------------------------------------------------------------------------
# Accepted KFE reproduction: D0-D3 and the scan
# ---------------------------------------------------------------------------


def test_d0_d1_d3_kfe_success(cases):
    for cid in ("d0", "d1", "d3"):
        rec = cases[cid]
        assert rec["hjb_converged"] is True
        assert rec["kfe_status"] == "SUCCESS"
        assert rec["kfe_normalization_factor"] > 0
        assert rec["kfe_residual_inf"] < 1e-12
        assert rec["kfe_density_min"] >= -1e-12  # allow ~1e-20 numerical noise
        assert rec["kfe_density_mass"] == pytest.approx(1.0, abs=1e-9)


def test_d2_kfe_failure_reproduces_accepted_message(cases):
    rec = cases["d2"]
    assert rec["hjb_converged"] is True
    assert rec["kfe_status"] == "FAILED"
    assert rec["kfe_failure_message"] == "faithful contaminated-row solve is non-finite"
    op = rec["operator"]
    assert op["raw_finite_fraction"] == 0.0  # raw is all non-finite


def test_scan_pattern_failure_only_at_d2_endpoint(cases):
    for k in range(8):
        assert cases[f"scan_{k}"]["kfe_status"] == "SUCCESS"
    assert cases["scan_8"]["kfe_status"] == "FAILED"
    # scan_0 == D1 and scan_8 == D2 behaviorally
    assert cases["scan_0"]["kfe_status"] == cases["d1"]["kfe_status"]
    assert cases["scan_8"]["kfe_status"] == cases["d2"]["kfe_status"]


# ---------------------------------------------------------------------------
# Operator diagnostics
# ---------------------------------------------------------------------------


def test_operator_diagnostics_structure(cases):
    for cid in ("d0", "d1", "d2", "d3"):
        op = cases[cid]["operator"]
        assert op["state_count"] == N
        assert op["shape_x"] == op["shape_y"] == N
        assert op["operator_data_finite"] is True
        assert op["operator_nnz"] > 0
        assert op["contaminated_nnz"] > 0
        assert op["neg_offdiag_count"] == 0  # upwind discretization has no negative off-diagonals
        assert op["leaky_state_count"] > 0  # non-conservative boundary leak present


def test_structural_rank_full_but_numerical_rank_deficient(cases):
    for cid in ("d0", "d1", "d2", "d3"):
        op = cases[cid]["operator"]
        assert op["structural_rank_operator"] == N
        assert op["structural_rank_transpose"] == N
        assert op["structural_rank_contaminated"] == N
        # pattern-level rank is full; SuperLU exposes a near-zero pivot -> numerical rank deficient
        assert op["lu_near_zero_pivots_transpose"] >= 1


def test_d1_vs_d2_operator_near_identical(cases):
    op1 = cases["d1"]["operator"]
    op2 = cases["d2"]["operator"]
    # the operators are near-identical; a single boundary coefficient crosses
    # exactly zero between D1 and D2 (nnz differs by 1) and one more state
    # crosses the leak threshold (leaky_state_count differs by 1) - themselves
    # diagnostic micro-structural observations
    for key in ("operator_nnz", "transpose_nnz", "contaminated_nnz", "leaky_state_count"):
        assert abs(op1[key] - op2[key]) <= 1
    for key in ("neg_offdiag_count", "structural_rank_operator", "structural_rank_transpose"):
        assert op1[key] == op2[key]


# ---------------------------------------------------------------------------
# Graph diagnostics
# ---------------------------------------------------------------------------


def test_graph_closed_classes(cases):
    g = cases["d2"]["graph"]
    assert g["scc_count"] == 46
    assert g["closed_component_count"] == 3
    assert sorted(g["closed_component_sizes"]) == [2, 2, 40]
    assert g["accepted_row_in_closed_component"] is False  # row 295 is transient
    assert g["accepted_row_coords"] == [15, 14, 0]


def test_graph_structure_identical_d1_d2(cases):
    g1 = cases["d1"]["graph"]
    g2 = cases["d2"]["graph"]
    assert g1["scc_count"] == g2["scc_count"] == 46
    assert sorted(g1["closed_component_sizes"]) == sorted(g2["closed_component_sizes"]) == [2, 2, 40]
    assert g1["accepted_row_in_closed_component"] == g2["accepted_row_in_closed_component"] is False


# ---------------------------------------------------------------------------
# Alternative row-pin diagnostics
# ---------------------------------------------------------------------------


def test_d0_d1_d3_all_pins_finite_but_pin_dependent(cases):
    for cid in ("d0", "d1", "d3"):
        pins = cases[cid]["pins"]
        assert all(p["solve_finite"] for p in pins["rows"])
        # non-uniqueness evidence: finite pins give different normalized densities
        diffs = list(pins["pairwise_density_maxdiff"].values())
        assert any(d > 1e-9 for d in diffs)
        # pins 0 and 400 lie in the same a=0 closed class -> agree
        assert pins["pairwise_density_maxdiff"]["first_vs_half"] < 1e-9


def test_d2_pin_pattern(cases):
    pins = cases["d2"]["pins"]
    status = {p["pin_label"]: p["solve_finite"] for p in pins["rows"]}
    assert status == {
        "first": True,
        "quarter": False,
        "accepted": False,
        "half": True,
        "three_quarter": False,
        "last": False,
    }
    # in-class pins agree with each other
    assert pins["pairwise_density_maxdiff"]["first_vs_half"] < 1e-9


# ---------------------------------------------------------------------------
# Bounded singular-value attempts (D1/D2)
# ---------------------------------------------------------------------------


def test_singular_values_show_nullspace(cases):
    for cid in ("d1", "d2"):
        sv = cases[cid]["singular_values"]
        k4 = sv["transpose_k4_smallest"]
        assert k4["converged"] is True
        values = k4["values_sorted"]
        assert len(values) == 4
        # numerical nullspace present (>= 1 near-zero value) AND positive spectrum
        # separated (>= 1 value >> 1e-4): in these runs the nullspace is exactly
        # 1-dimensional (rank 799)
        assert sum(1 for v in values if abs(v) < 1e-8) >= 1
        assert sum(1 for v in values if abs(v) > 1e-4) >= 1
        # at least one smallest-singular-value attempt (arpack or propack)
        # converged to a tiny value
        tiny_vals = [
            e["value"] for mat in ("contaminated", "transpose")
            for e in sv[mat] if e["converged"] and e["value"] is not None
        ]
        assert tiny_vals and all(abs(v) < 1e-9 for v in tiny_vals)


# ---------------------------------------------------------------------------
# Reproducibility + classification
# ---------------------------------------------------------------------------


def test_reproducibility(cfg, repro):
    assert repro["randomness"] == "NOT_APPLICABLE"
    assert repro["pass_bool"] is True
    assert repro["identical_classifications"] is True
    assert repro["identical_graph"] is True
    assert repro["max_numeric_diff"] <= cfg.reproducibility_tol
    for c in repro["per_case"]:
        assert c["pass"] is True


def test_root_cause_classification(cfg, repro):
    cls = _root_cause_classification(cfg, repro["run1"])
    assert cls == "MULTIPLE_OR_NONUNIQUE_STATIONARY_CLASS_CANDIDATE"


def test_fixture_reuses_accepted_dlh5b(cfg):
    # the diagnostic fixture is built from the accepted DLH-5B config (read-only reference)
    assert cfg.dlh5b_config_path == "configs/dlh_5b_two_region_symmetric_anchor.toml"
    dlh5b, fixture = build_fixture(cfg)
    grid, params, numerics = fixture
    assert (grid.b.size, grid.a.size, grid.z.size) == (20, 20, 2)
    assert params.rho == 0.02
    assert numerics.convergence_tolerance == 1e-7
