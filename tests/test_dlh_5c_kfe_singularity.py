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

import pathlib

import numpy as np
import pytest
from scipy import sparse

from deep_learning_hank.two_asset import matlab_contaminated_row_index
from deep_learning_hank.diagnostics.dlh_5c_kfe_singularity import (
    DLH5CConfig,
    _pin_indices,
    _root_cause_classification,
    build_contaminated,
    build_fixture,
    case_sequence,
    diagnostic_solve,
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
    # corrected row->col orientation: closed (sink) = no outgoing transition
    g = cases["d2"]["graph"]
    assert g["edge_orientation"].startswith("row -> col")
    assert g["scc_count"] == 46
    assert g["closed_component_count"] == 2
    assert sorted(g["closed_component_sizes"]) == [40, 546]
    # sources (no incoming) = the three R1-mislabeled 'closed' classes
    assert g["source_component_count"] == 3
    assert sorted(g["source_component_sizes"]) == [2, 2, 40]
    # accepted row 295 is in the 546-state closed sink (NOT transient under the
    # corrected orientation; the R1 'transient' label was an orientation artifact)
    assert g["accepted_row_in_closed_component"] is True
    assert g["accepted_row_scc_size"] == 546
    assert g["accepted_row_coords"] == [15, 14, 0]


def test_graph_structure_identical_d1_d2(cases):
    g1 = cases["d1"]["graph"]
    g2 = cases["d2"]["graph"]
    assert g1["scc_count"] == g2["scc_count"] == 46
    assert sorted(g1["closed_component_sizes"]) == sorted(g2["closed_component_sizes"]) == [40, 546]
    assert sorted(g1["source_component_sizes"]) == sorted(g2["source_component_sizes"]) == [2, 2, 40]
    assert g1["accepted_row_in_closed_component"] is True
    assert g2["accepted_row_in_closed_component"] is True


# ---------------------------------------------------------------------------
# R2-F: graph-direction synthetic regression test
# ---------------------------------------------------------------------------


def test_graph_direction_row_to_col_synthetic():
    """R2-A/F: for a positive off-diagonal entry A[row,col]>0 the directed
    transition is row -> col. For Q = [[-1,1,0],[0,-1,1],[0,0,0]] the chain is
    0 -> 1 -> 2, so the true closed sink is {2} (not {0}) and the source is {0}."""
    from deep_learning_hank.diagnostics.dlh_5c_kfe_singularity import graph_diagnostics
    Q = sparse.csr_matrix(np.array([
        [-1.0, 1.0, 0.0],
        [0.0, -1.0, 1.0],
        [0.0, 0.0, 0.0],
    ]))
    g = graph_diagnostics(Q, accepted_row=0, n=3)
    assert g["edge_orientation"].startswith("row -> col")
    assert g["scc_count"] == 3
    assert g["closed_component_count"] == 1
    assert g["closed_component_sizes"] == [1]
    # true closed sink = {2}, NOT {0}
    sink_members = g["closed_classes"][0]["member_indices"]
    assert sink_members == [2]
    # source = {0}
    assert g["source_component_count"] == 1
    assert g["source_classes"][0]["member_indices"] == [0]


def test_graph_reversal_preserves_scc_but_swaps_source_sink():
    """R2-A: full edge reversal preserves SCC membership/count but exchanges the
    source and sink interpretation."""
    from deep_learning_hank.diagnostics.dlh_5c_kfe_singularity import graph_diagnostics
    Q = sparse.csr_matrix(np.array([
        [-1.0, 1.0, 0.0],
        [0.0, -1.0, 1.0],
        [0.0, 0.0, 0.0],
    ]))
    g_forward = graph_diagnostics(Q, accepted_row=0, n=3)
    g_reversed = graph_diagnostics(Q.T.tocsr(), accepted_row=0, n=3)
    # SCC count and membership preserved under reversal
    assert g_reversed["scc_count"] == g_forward["scc_count"] == 3
    assert g_reversed["scc_sizes_sorted"] == g_forward["scc_sizes_sorted"] == [1, 1, 1]
    # source/sink interpretations exchange
    assert g_forward["closed_classes"][0]["member_indices"] == [2]
    assert g_reversed["closed_classes"][0]["member_indices"] == [0]
    assert g_forward["source_classes"][0]["member_indices"] == [0]
    assert g_reversed["source_classes"][0]["member_indices"] == [2]


# ---------------------------------------------------------------------------
# Alternative row-pin diagnostics
# ---------------------------------------------------------------------------


def test_d0_d1_d3_all_pins_finite_but_pin_dependent(cases):
    for cid in ("d0", "d1", "d3"):
        pins = cases[cid]["pins"]
        assert all(p["solve_finite"] for p in pins["rows"])
        # R1: finite pins give different normalized densities, but this is the
        # signature of mixing true stationary solutions (in-class pins 0/400)
        # with manufactured NON-solutions (transient pins), NOT evidence of
        # multiple stationary distributions (see R1 original-residual tests)
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
    assert cls == "FIXED_ROW_SELECTION_ARTIFACT_CANDIDATE"


def test_fixture_reuses_accepted_dlh5b(cfg):
    # the diagnostic fixture is built from the accepted DLH-5B config (read-only reference)
    assert cfg.dlh5b_config_path == "configs/dlh_5b_two_region_symmetric_anchor.toml"
    dlh5b, fixture = build_fixture(cfg)
    grid, params, numerics = fixture
    assert (grid.b.size, grid.a.size, grid.z.size) == (20, 20, 2)
    assert params.rho == 0.02
    assert numerics.convergence_tolerance == 1e-7


# ---------------------------------------------------------------------------
# R1-A: original stationary-equation residual
# ---------------------------------------------------------------------------


def _synthetic_cfg(tmp_path):
    return DLH5CConfig(
        dlh5b_config_path="x",
        region_index=0,
        d0=(1.0, 1.0),
        d1=(1.0, 1.0),
        d2=(1.0, 1.0),
        d3=(1.0, 1.0),
        scan_start="d1",
        scan_end="d2",
        scan_n_points=2,
        pin_spec=("first",),
        pin_rhs=0.007,
        accepted_pin_fraction=0.37,
        reproducibility_tol=1e-12,
        numeric_compare_tol=1e-12,
        singular_value_cases=(),
        svd_maxiter=100,
        svd_tol=1e-10,
        output_root=str(tmp_path),
    )


def test_original_equation_residual_math(tmp_path):
    """R1-A: the recorded original residual is exactly ||operator.T @ density||_inf
    computed independently (contaminated and original residuals kept separate)."""
    n = 6
    T = sparse.csr_matrix(np.array([
        [1.0, -0.2, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.9, -0.1, 0.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, -0.3, 0.0, 0.0],
        [0.0, 0.0, 0.0, 1.0, -0.2, 0.0],
        [0.0, 0.0, 0.0, 0.0, 1.0, -0.1],
        [0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
    ]))
    from deep_learning_hank.diagnostics.dlh_5c_kfe_singularity import pin_diagnostics
    cfg = _synthetic_cfg(tmp_path)
    res = pin_diagnostics(T, n, 1.0, 1.0, cfg)
    p = res["rows"][0]
    assert p["solve_finite"] is True
    # independent recomputation of density and residuals
    index_of, _ = _pin_indices(n, cfg)
    cont, rhs = build_contaminated(T, index_of["first"], cfg.pin_rhs, n)
    raw, _exc, _warn = diagnostic_solve(cont, rhs)
    assert raw is not None and np.isfinite(raw).all()
    density = raw / float(np.sum(raw))
    r_orig = T @ density
    assert p["contaminated_residual_inf"] == pytest.approx(
        float(np.linalg.norm(cont @ raw - rhs, ord=np.inf)), abs=1e-15
    )
    assert p["original_residual_inf"] == pytest.approx(
        float(np.linalg.norm(r_orig, ord=np.inf)), abs=1e-15
    )
    assert p["original_residual_argmax_index"] == int(np.argmax(np.abs(r_orig)))
    assert p["max_residual_at_pinned_row"] == (p["original_residual_argmax_index"] == p["pin_index"])


def test_finite_pin_original_residual_recorded(cases):
    """R1-A: every finite pin records both the contaminated and the original
    stationary-equation residual, with argmax index/coords."""
    for cid in ("d0", "d1", "d3"):
        for p in cases[cid]["pins"]["rows"]:
            assert p["solve_finite"] is True
            assert p["contaminated_residual_inf"] is not None
            assert p["original_residual_inf"] is not None
            assert p["original_residual_argmax_index"] is not None
            assert p["original_residual_argmax_coords"] is not None
            assert len(p["original_residual_argmax_coords"]) == 3
            assert p["original_residual_at_pinned_row"] is not None


def test_in_class_pins_are_near_solutions_of_original_equation(cases):
    """R1-A: pins inside the a=0 closed class (0, 400) recover the unique
    stationary measure -> original residual at machine precision at D0-D3."""
    for cid in ("d0", "d1", "d2", "d3"):
        pins = cases[cid]["pins"]["rows"]
        for label in ("first", "half"):
            p = next(x for x in pins if x["pin_label"] == label)
            assert p["solve_finite"] is True
            assert p["original_residual_inf"] < 1e-9
            assert p["contaminated_residual_inf"] < 1e-9


def test_transient_pins_are_non_solutions_with_max_at_pinned_row(cases):
    """R1-A (re-confirmed R2): pins in the leaky 546-state closed sink (200, 295,
    600, 799) manufacture NON-solutions of the original equation; the largest
    original residual sits exactly on the pinned (replaced) row."""
    for cid in ("d0", "d1", "d3"):
        pins = cases[cid]["pins"]["rows"]
        for label in ("quarter", "accepted", "three_quarter", "last"):
            p = next(x for x in pins if x["pin_label"] == label)
            assert p["solve_finite"] is True
            assert p["original_residual_inf"] > 1e-6
            assert p["max_residual_at_pinned_row"] is True


# ---------------------------------------------------------------------------
# R1-B: sink-component leakage classification
# ---------------------------------------------------------------------------


def test_sink_component_leakage_conservative(cases):
    """R2-B: the corrected closed (sink) classes are [40, 546]; the a=0 class is
    conservative (non-leaky recurrent-class candidate) while the 546-state sink
    containing the accepted row is LEAKY (sub-generator-like), so a graph sink is
    NOT automatically a stationary recurrent class."""
    for cid in ("d0", "d1", "d2", "d3"):
        g = cases[cid]["graph"]
        sizes = [cc["size"] for cc in g["closed_classes"]]
        assert set(sizes) == {40, 546}
        assert len(g["closed_class_member_indices"]) == len(g["closed_classes"]) == 2
        for cc in g["closed_classes"]:
            assert len(cc["member_indices"]) == cc["size"]
            if cc["size"] == 40:
                # the a=0 class is conservative (non-leaky recurrent-class candidate)
                assert cc["leaky_rows_count"] == 0
                assert cc["all_rows_conservative_within_tol"] is True
                assert cc["classification"] == "non_leaky_recurrent_class_candidate"
                assert cc["row_sum_min"] > -1e-12
            else:
                # the 546-state closed sink containing row 295 is LEAKY
                assert cc["size"] == 546
                assert cc["leaky_rows_count"] > 0
                assert cc["all_rows_conservative_within_tol"] is False
                assert cc["classification"] == "leaky_graph_sink"
        # because the 546 sink is leaky, not all closed classes are conservative
        assert g["any_closed_class_leaky"] is True
        assert g["all_closed_classes_conservative"] is False


def test_graph_sink_not_auto_equated_to_stationary_class(cases):
    """R2-B/C: the leaky 546-state closed sink is NOT a stationary recurrent
    class; the singular vector shows the unique null vector is the a=0 class
    measure (the 546 sink carries ~0 mass)."""
    for cid in ("d1", "d2"):
        g = cases[cid]["graph"]
        sv = cases[cid]["singular_vector"]
        sizes = [cc["size"] for cc in g["closed_classes"]]
        fracs = sv["closed_class_mass_fractions"]
        assert len(fracs) == 2
        a0_frac = fracs[sizes.index(40)]
        sink546_frac = fracs[sizes.index(546)]
        assert a0_frac > 0.99
        assert sink546_frac < 1e-3


# ---------------------------------------------------------------------------
# R1-C: smallest-singular-vector diagnostic
# ---------------------------------------------------------------------------


def test_singular_vector_original_residual_and_fields(cases):
    """R1-C: the smallest-singular-vector candidate is a near-null vector of the
    ORIGINAL equation with bounded-sparse fields reported."""
    for cid in ("d1", "d2"):
        sv = cases[cid]["singular_vector"]
        assert sv["converged"] is True
        assert sv["vector_finite"] is True
        assert sv["singular_value"] < 1e-9
        assert sv["original_residual_inf"] < 1e-6
        assert sv["closed_class_mass_fractions"] is not None
        assert sv["transient_mass_proportion"] is not None
        assert sv["positive_count"] + sv["negative_count"] + sv["zero_count"] == N


def test_category_2_refuted_by_unique_stationary_measure(cases):
    """R1-D: the stationary measure is unique -> category 2 (multiple/non-unique
    stationary class) is refuted by the new evidence."""
    k4 = cases["d2"]["singular_values"]["transpose_k4_smallest"]
    assert k4["converged"] is True
    assert sum(1 for v in k4["values_sorted"] if abs(v) < 1e-8) == 1  # nullspace dim 1
    for cid in ("d0", "d1", "d2", "d3"):
        pins = cases[cid]["pins"]
        # in-class pins recover the SAME normalized density
        assert pins["pairwise_density_maxdiff"]["first_vs_half"] < 1e-9


# ---------------------------------------------------------------------------
# R1-E: conservative scan wording
# ---------------------------------------------------------------------------


def test_scan_wording_conservative_within_frozen_resolution():
    """R1-E: the diagnostic never claims a mathematical discontinuity; it reports
    an endpoint-only failure at the frozen 9-point resolution and explicitly
    leaves an unsampled narrower failure interval open."""
    src = pathlib.Path("src/deep_learning_hank/diagnostics/dlh_5c_kfe_singularity.py").read_text(encoding="utf-8")
    assert "endpoint-only failure at the frozen 9-point resolution" in src
    assert "unsampled narrower failure interval between t=7/8 and t=1" in src
    assert "single-point" not in src
    assert "knife-edge" not in src
    assert "mathematical discontinuity" not in src
    assert "discontinuity finding" not in src


# ---------------------------------------------------------------------------
# R1-D: classification driven by the new evidence
# ---------------------------------------------------------------------------


def test_root_cause_classification_driven_by_r1_evidence(cfg, repro):
    """R1-D/R2-E: the root-cause classification is driven by A-C evidence (not
    forced to category 2); with a unique stationary measure and 546-sink-pin
    inconsistencies it must be the fixed-row-selection artifact candidate (the
    corrected graph does not conflict with Category 1)."""
    cls = _root_cause_classification(cfg, repro["run1"])
    assert cls == "FIXED_ROW_SELECTION_ARTIFACT_CANDIDATE"
