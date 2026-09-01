"""DLH-5E (Issue #28) — focused validation tests.

Covers the exact synthetic tests required by Issue #28:
- conservative boundary assembly;
- row-sum zero;
- nonnegative off-diagonal;
- requested vs admitted boundary rate;
- BOUNDARY_POLICY_VIOLATION classification;
- irreducible 3-state multi-pin equivalence;
- unique stationary distribution with transient zero-support pin;
- default pin fail-closed;
- original residual distinct from contaminated residual;
- nonfinite-aware deterministic comparison.

Plus a frozen-fixture module-scope test running the canonical D0 pipeline
(boundary-policy gate + conservative-generator mechanics + deterministic blocker
reproduction). No production source is modified.
"""

from __future__ import annotations

import pathlib

import numpy as np
import pytest
from scipy import sparse

from deep_learning_hank.two_asset import assemble_source_axis
from deep_learning_hank.two_asset.conservative_stationary_kfe import (
    DLH5EConfig,
    PIN_UNRESOLVED,
    PIN_VALID,
    PIN_ZERO_SUPPORT,
    TERMINAL_BOUNDARY_VIOLATION,
    TERMINAL_DEFAULT_PIN_NOT_VALID,
    TERMINAL_VALIDATED,
    assemble_conservative_operator,
    assemble_conservative_source_axis,
    boundary_outward_diagnostics,
    build_fixture,
    classify_pin,
    compare_records,
    generator_diagnostics,
    load_config,
    null_vector_candidate,
    overall_terminal,
    pin_validation,
    reproduce,
    requested_rates,
    run_all,
)

CONFIG_PATH = "configs/dlh_5e_conservative_stationary_kfe_validation.toml"


def _cfg(tmp_path) -> DLH5EConfig:
    return DLH5EConfig(
        dlh5b_config_path="configs/dlh_5b_two_region_symmetric_anchor.toml",
        region_index=0,
        d0=(1.0, 0.03),
        d1=(0.0, 0.0),
        d2=(0.0, 0.0),
        d3=(0.0, 0.0),
        pin_spec=("first", "quarter", "accepted", "half", "three_quarter", "last"),
        pin_rhs=0.007,
        boundary_threshold=1e-10,
        generator_row_sum_tol=1e-12,
        generator_neg_offdiag_tol=1e-12,
        original_residual_tol=1e-10,
        mass_tol=1e-12,
        min_density_tol=-1e-12,
        multi_pin_diff_tol=1e-10,
        reproducibility_tol=1e-12,
        numeric_compare_tol=1e-12,
        nullspace_tol=1e-8,
        zero_support_rel_tol=1e-6,
        svd_maxiter=5000,
        output_root=str(tmp_path / "dlh_5e_out"),
    )


# ---------------------------------------------------------------------------
# Conservative assembly
# ---------------------------------------------------------------------------


def test_conservative_axis_outward_edge_omits_diagonal_rate(tmp_path):
    """Outward edges are omitted AND their rate is omitted from the diagonal:
    the top state of a pure forward chain has diagonal 0 (not -rate)."""
    cfg = _cfg(tmp_path)
    shape = (3, 1, 1)
    backward = np.zeros(shape)
    forward = np.ones(shape)  # forward drift on all states
    Q = assemble_conservative_source_axis(backward, forward, 0)
    dense = Q.toarray()
    assert dense[2, 2] == pytest.approx(0.0, abs=1e-12)  # outward rate NOT kept in diagonal
    assert dense[2, 2] == 0.0
    row_sums = np.asarray(Q.sum(axis=1)).ravel()
    assert np.max(np.abs(row_sums)) <= 1e-12


def test_conservative_axis_row_sum_zero(tmp_path):
    """Generator diagonal = -sum of ACTUALLY ADMITTED off-diagonal rates -> row sum 0."""
    cfg = _cfg(tmp_path)
    rng = np.random.default_rng(0)
    backward = rng.random((4, 5, 2))
    forward = rng.random((4, 5, 2))
    for axis in (0, 1):
        Q = assemble_conservative_source_axis(backward, forward, axis)
        g = generator_diagnostics(Q)
        assert g["row_sum_max_abs"] <= 1e-12
        row_sums = np.asarray(Q.sum(axis=1)).ravel()
        assert np.max(np.abs(row_sums)) <= 1e-12


def test_conservative_axis_offdiag_nonnegative(tmp_path):
    """No negative off-diagonal beyond tolerance."""
    cfg = _cfg(tmp_path)
    rng = np.random.default_rng(1)
    backward = rng.random((4, 5, 2))
    forward = rng.random((4, 5, 2))
    Q = assemble_conservative_operator(
        requested_rates(np.zeros((4, 5, 2)), np.zeros((4, 5, 2)), 1.0, 1.0),
        np.array([[-0.5, 0.5], [0.5, -0.5]]),
    )
    # Use random drift arrays via assemble_conservative_source_axis directly.
    for axis in (0, 1):
        Qa = assemble_conservative_source_axis(backward, forward, axis)
        g = generator_diagnostics(Qa)
        assert g["negative_offdiag_max_mag"] <= 1e-12
        assert g["negative_offdiag_count"] == 0


def test_requested_vs_admitted_boundary_rate(tmp_path):
    """At the upper-b boundary the requested outward rate is positive while the
    admitted generator Q_c admits no outward edge (requested > admitted = 0)."""
    cfg = _cfg(tmp_path)
    db = 1.0
    mu_b = np.zeros((4, 1, 1))
    mu_b[-1, 0, 0] = 2.0  # strong outward saving at top-b
    req = requested_rates(mu_b, np.zeros((4, 1, 1)), db, 1.0)
    bd = boundary_outward_diagnostics(req, (4, 1, 1), cfg.boundary_threshold)
    upper = next(b for b in bd["boundaries"] if b["boundary"] == "upper_b")
    assert upper["requested_outward_max"] == pytest.approx(2.0 / db)
    # admitted: the top-b row of Q_c has no positive off-diagonal to a phantom state
    Q = assemble_conservative_source_axis(req["b_backward_requested"], req["b_forward_requested"], 0)
    top_row = Q.getrow(3)
    assert top_row.data.size == 0 or np.max(top_row.data) == 0.0 or top_row.data.max() <= 0.0


def test_boundary_policy_violation_classification(tmp_path):
    """Material outward requested boundary drift -> max requested rate > 1e-10 and
    boundary direction reported; benign (all inward) drift stays below threshold."""
    cfg = _cfg(tmp_path)
    db = da = 1.0
    mu_b = np.zeros((4, 1, 1))
    mu_b[-1, 0, 0] = 0.5
    req = requested_rates(mu_b, np.zeros((4, 1, 1)), db, da)
    bd = boundary_outward_diagnostics(req, (4, 1, 1), cfg.boundary_threshold)
    assert bd["max_requested_outward"] > 1e-10
    assert bd["max_boundary"] == "upper_b"

    mu_b_benign = np.zeros((4, 1, 1))
    mu_b_benign[0, 0, 0] = 0.5     # inward at lower-b (forward into grid)
    mu_b_benign[-1, 0, 0] = -0.5   # inward at upper-b (backward into grid)
    req2 = requested_rates(mu_b_benign, np.zeros((4, 1, 1)), db, da)
    bd2 = boundary_outward_diagnostics(req2, (4, 1, 1), cfg.boundary_threshold)
    assert bd2["max_requested_outward"] <= 1e-10


# ---------------------------------------------------------------------------
# Stationary / pin classification
# ---------------------------------------------------------------------------


def _chain_Q():
    """0 -> 1 -> 2; closed (sink) = {2}; states 0,1 are transients with zero support."""
    return sparse.csr_matrix(np.array([[-1.0, 1.0, 0.0], [0.0, -1.0, 1.0], [0.0, 0.0, 0.0]]))


def _irreducible_Q():
    """Fully connected 3-state generator: unique uniform stationary measure."""
    return sparse.csr_matrix(np.array([[-2.0, 1.0, 1.0], [1.0, -2.0, 1.0], [1.0, 1.0, -2.0]]))


def test_unique_stationary_zero_support_pin_inadmissible(tmp_path):
    """Chain 0->1->2 has unique stationary measure = point mass on {2}; a positive
    component pin on the zero-support transient 0 is inadmissible (null-vector
    evidence), and a pin on 2 is a valid stationary normalization."""
    cfg = _cfg(tmp_path)
    Q = _chain_Q()
    nv = null_vector_candidate(Q, cfg.svd_maxiter)
    assert nv["converged"] is True
    v = nv["vector"]
    assert abs(v[0]) <= 1e-6 and abs(v[1]) <= 1e-6 and abs(v[2]) > 0.5  # support only on {2}
    r0 = classify_pin(Q, 0, cfg.pin_rhs, 3, 1.0, 1.0, v, cfg)
    r1 = classify_pin(Q, 1, cfg.pin_rhs, 3, 1.0, 1.0, v, cfg)
    r2 = classify_pin(Q, 2, cfg.pin_rhs, 3, 1.0, 1.0, v, cfg)
    assert r0["classification"] == PIN_ZERO_SUPPORT
    assert r1["classification"] == PIN_ZERO_SUPPORT
    assert r2["classification"] == PIN_VALID
    assert r0["null_vector_support_rel"] <= 1e-6
    assert r2["original_residual_inf"] <= 1e-10


def test_irreducible_3state_multi_pin_equivalence(tmp_path):
    """For an irreducible conservative generator all pins are valid and recover the
    same normalized density (>= 2 valid pins; max diff <= 1e-10)."""
    cfg = _cfg(tmp_path)
    Q = _irreducible_Q()
    nv = null_vector_candidate(Q, cfg.svd_maxiter)
    for p in (0, 1, 2):
        r = classify_pin(Q, p, cfg.pin_rhs, 3, 1.0, 1.0, nv["vector"], cfg)
        assert r["classification"] == PIN_VALID
    pv = pin_validation(Q, 3, 1.0, 1.0, cfg)
    assert pv["valid_pin_count"] >= 2
    assert pv["valid_pin_max_density_diff"] <= 1e-10
    assert pv["default_pin_class"] == PIN_VALID


def test_default_parity_pin_fail_closed(tmp_path):
    """For the chain, the default MATLAB parity pin (floor(0.37*3)-1 = 0) has zero
    stationary support -> classified inadmissible -> the default-pin rule stops for
    scientific review (no auto-switch)."""
    cfg = _cfg(tmp_path)
    Q = _chain_Q()
    pv = pin_validation(Q, 3, 1.0, 1.0, cfg)
    assert pv["default_pin_class"] == PIN_ZERO_SUPPORT
    assert pv["terminal"] == TERMINAL_DEFAULT_PIN_NOT_VALID


def test_original_residual_distinct_from_contaminated_residual(tmp_path):
    """The contaminated residual can be machine-epsilon while the ORIGINAL
    Q^T g residual is material: pin at state 0 of the accepted-style leaky
    operator (outward rate kept in the diagonal, destination omitted)."""
    cfg = _cfg(tmp_path)
    db = 1.0
    backward = np.zeros((3, 1, 1))
    forward = np.ones((3, 1, 1))
    Q_leaky = assemble_source_axis(backward, forward, 0)  # accepted (non-conservative) assembler
    g = generator_diagnostics(Q_leaky)
    assert g["row_sum_max_abs"] > 1e-6  # genuinely leaky at the top row
    r = classify_pin(Q_leaky, 0, cfg.pin_rhs, 3, db, 1.0, None, cfg)
    assert r["solve_finite"] is True
    assert r["contaminated_residual_inf"] <= 1e-12
    assert r["original_residual_inf"] > 1e-6
    assert r["classification"] == PIN_UNRESOLVED  # fails original residual, no zero-support evidence


def test_nonfinite_aware_deterministic_comparison(tmp_path):
    """Aligned non-finite fields are explicit and allowed; a mismatch between a
    finite and a non-finite value fails the deterministic comparison."""
    cfg = _cfg(tmp_path)
    base = {"terminal": "T", "hjb_converged": True, "boundary_policy_gate": "VIOLATION",
            "boundary": {"max_requested_outward": float("nan")},
            "generator": {"row_sum_max_abs": float("nan"), "negative_offdiag_max_mag": 0.0,
                          "row_sum_min": float("nan"), "row_sum_max": float("nan")},
            "graph": {}, "nullspace": {}, "pins": {}}
    r1 = dict(base)
    r2 = dict(base)
    cmp = compare_records(r1, r2, cfg)
    assert cmp["pass_bool"] is True
    assert cmp["aligned_nonfinite_fields"] >= 1
    r3 = dict(base)
    r3["boundary"] = {"max_requested_outward": 1.0}  # finite vs non-finite -> mismatch
    cmp_bad = compare_records(r1, r3, cfg)
    assert cmp_bad["pass_bool"] is False
    assert cmp_bad["mismatched_fields"] >= 1


# ---------------------------------------------------------------------------
# Frozen-fixture canonical D0 pipeline (module scope)
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def repro():
    cfg = load_config(CONFIG_PATH)
    fixture = build_fixture(cfg)
    return cfg, fixture, reproduce(cfg, fixture)


def test_d0_hjb_converges_and_generator_conservative(repro):
    cfg, fixture, rep = repro
    d0 = rep["run1"]["cases"][0]
    assert d0["case_id"] == "d0"
    assert d0["hjb_converged"] is True
    g = d0["generator"]
    assert g["row_sum_max_abs"] <= cfg.generator_row_sum_tol
    assert g["negative_offdiag_max_mag"] <= cfg.generator_neg_offdiag_tol


def test_d0_boundary_policy_gate_blocks(repro):
    cfg, fixture, rep = repro
    d0 = rep["run1"]["cases"][0]
    b = d0["boundary"]
    assert b["max_requested_outward"] > cfg.boundary_threshold
    assert d0["boundary_policy_gate"] == "VIOLATION"
    assert d0["terminal"] == TERMINAL_BOUNDARY_VIOLATION
    assert d0["reached_aggregates"] is False
    # no stationary density / aggregates / anchor accepted
    assert d0["pins"] is None and d0["aggregates"] is None and d0["anchor"] is None


def test_d1_d3_not_reached_when_d0_blocked(repro):
    cfg, fixture, rep = repro
    for rec in rep["run1"]["cases"][1:]:
        assert rec["terminal"] == "NOT_REACHED__D0_BLOCKED"


def test_deterministic_blocker_reproduction(repro):
    cfg, fixture, rep = repro
    assert rep["randomness"] == "NOT_APPLICABLE"
    assert rep["pass_bool"] is True
    assert rep["terminal_run1"] == rep["terminal_run2"] == TERMINAL_BOUNDARY_VIOLATION
    assert rep["run1"]["d0_ok"] is False and rep["run2"]["d0_ok"] is False
    for cid, cmp in rep["per_case"].items():
        assert cmp["pass_bool"] is True
        assert cmp["identical_structural_signature"] is True
