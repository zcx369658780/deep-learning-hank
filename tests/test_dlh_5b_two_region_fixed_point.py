"""DLH-5B (Issue #25) focused tests: deterministic two-region fixed-point prototype.

Validates the frozen fixture, one-shot anchor derivation, S0 anchor smoke, S1
perturbed outer iteration, S2 region-order invariance, conservation/accounting
gates, HJB/KFE/boundary diagnostics, firm validity and deterministic
reproducibility. Household solves call the accepted oracle; the module under
test does not reimplement HJB/KFE logic.

R1 (GPT review 2026-08-31): adds S1 per-turn validity-bundle enforcement,
required trace fields (`P^L`, `lambda`, `Gamma_next`), NaN-aware numeric
comparison, fail-closed terminal classification on S2/reproducibility, and
no-regression of the predecessor S0/S1 observed scientific outcome.
"""

from __future__ import annotations

import dataclasses
from types import SimpleNamespace

import numpy as np
import pytest

from deep_learning_hank.regional.two_region_fixed_point import (
    S0_TRACE_FIELDS,
    FrozenFirmParams,
    _is_blocked_stop,
    _terminal_classification,
    _trace_row,
    build_fixture,
    canonical_numbers,
    derive_anchor,
    firm_block,
    load_config,
    max_numeric_diff,
    one_turn,
    run_s0,
    run_s1,
    run_s2,
    validity_bundle,
)

CONFIG_PATH = "configs/dlh_5b_two_region_symmetric_anchor.toml"


@pytest.fixture(scope="module")
def cfg():
    return load_config(CONFIG_PATH)


@pytest.fixture(scope="module")
def base(cfg):
    return build_fixture(cfg)  # grid, params, numerics


@pytest.fixture(scope="module")
def anchor(cfg, base):
    grid, params, numerics = base
    return derive_anchor(cfg, grid, params, numerics)


@pytest.fixture(scope="module")
def firm(cfg, anchor):
    return FrozenFirmParams(
        Z=(anchor.Z_star, anchor.Z_star),
        delta=(anchor.delta_star, anchor.delta_star),
        alpha=(cfg.alpha[0], cfg.alpha[1]),
    )


@pytest.fixture(scope="module")
def s0(cfg, base, firm):
    grid, params, numerics = base
    return run_s0(cfg, grid, params, numerics, firm)


@pytest.fixture(scope="module")
def s1(cfg, base, firm):
    grid, params, numerics = base
    return run_s1(cfg, grid, params, numerics, firm)


@pytest.fixture(scope="module")
def s2(cfg, base, firm):
    grid, params, numerics = base
    return run_s2(cfg, grid, params, numerics, firm)


# ---------------------------------------------------------------------------
# 1. frozen config integrity (guard against PASS-seeking edits)
# ---------------------------------------------------------------------------


def test_frozen_config_values(cfg):
    assert cfg.lambda_ == 0.5
    assert cfg.tol_w == 1e-6
    assert cfg.tol_ra == 1e-6
    assert cfg.max_iter == 25
    assert cfg.s0_tol_w == 1e-10
    assert cfg.s0_tol_ra == 1e-10
    assert list(cfg.P_L[0]) == [0.9, 0.1]
    assert list(cfg.P_L[1]) == [0.1, 0.9]
    assert list(cfg.M) == [1.0, 1.0]
    assert cfg.r_b == 0.015
    assert list(cfg.tau) == [0.15, 0.15]
    assert list(cfg.r_a_star) == [0.03, 0.03]
    assert list(cfg.alpha) == [pytest.approx(1.0 / 3.0)] * 2
    # P^L rows sum to one
    for row in cfg.P_L:
        assert abs(sum(row) - 1.0) <= 1e-12


def test_network_validity(cfg):
    for row in cfg.P_L:
        assert min(row) >= -1e-12
        assert abs(sum(row) - 1.0) <= 1e-12
    for m in cfg.m_L:
        assert 0.0 <= m <= 1.0


# ---------------------------------------------------------------------------
# 2. anchor fixture + one-shot derivation
# ---------------------------------------------------------------------------


def test_anchor_household_solves(cfg, base, anchor):
    grid, params, numerics = base
    assert not anchor.region.blocked
    assert anchor.region.hjb_converged
    assert anchor.region.hjb_statistic <= cfg.conv_tol
    assert anchor.A_star > 0.0
    assert anchor.L_star > 0.0
    assert anchor.C_star > 0.0
    assert np.isfinite(anchor.B_star)
    assert anchor.region.kfe_mass_error <= cfg.kfe_mass_tol


def test_anchor_derivation_sanity(cfg, anchor):
    assert all(anchor.sanity.values())
    assert anchor.Z_star > 0.0
    assert 0.0 < anchor.delta_star < 1.0
    assert anchor.K_star == pytest.approx(anchor.A_star, rel=1e-12)  # M=1
    assert anchor.Ldest_star == pytest.approx(anchor.L_star, rel=1e-12)


def test_anchor_firm_reproduces_anchor_prices(cfg, anchor):
    # At K*=A*, Ldest*=L* the derived Z*,delta* must reproduce w*=1, r_a*=0.03.
    Y, w_hat, r_hat_a = firm_block(
        anchor.Z_star, anchor.alpha, anchor.delta_star, anchor.K_star, anchor.Ldest_star
    )
    assert w_hat == pytest.approx(1.0, rel=1e-9)
    assert r_hat_a == pytest.approx(0.03, rel=1e-9)
    assert Y > 0.0


# ---------------------------------------------------------------------------
# 3. S0 anchor smoke
# ---------------------------------------------------------------------------


def test_s0_residual_gate(cfg, s0):
    assert s0.pass_bool, s0.reason
    assert s0.record.R_w <= cfg.s0_tol_w
    assert s0.record.R_ra <= cfg.s0_tol_ra


def test_s0_conservation_accounting(cfg, s0):
    assert all(s0.accounting.values()), s0.accounting


def test_s0_kfe_gate(s0):
    assert all(s0.kfe_checks.values()), s0.kfe_checks


def test_s0_firm_gate(s0):
    assert all(s0.firm_checks.values()), s0.firm_checks


def test_s0_boundary_masses_reported_and_finite(cfg, s0):
    for i in (0, 1):
        bm = s0.record.region[i].boundary_masses
        assert bm is not None
        for key in ("b_min", "b_max", "a_min", "a_max"):
            assert np.isfinite(bm[key])
            assert bm[key] >= -1e-12


# ---------------------------------------------------------------------------
# 4. S1 perturbed outer iteration
# ---------------------------------------------------------------------------


def test_s1_stop_reason_and_iteration_bounds(cfg, s1):
    assert s1.stop_reason in (
        "ACCEPTED",
        "MAX_ITER_REACHED",
    ) or s1.stop_reason.startswith(("HOUSEHOLD_BLOCK_FAILED", "INVALID_FIRM_STATE"))
    assert 1 <= s1.iterations <= cfg.max_iter
    assert len(s1.trace) == s1.iterations


def test_s1_convergence_implies_residuals_within_tol(cfg, s1):
    if s1.stop_reason == "ACCEPTED":
        assert s1.converged
        assert s1.final_residuals is not None
        assert s1.final_residuals[0] <= cfg.tol_w
        assert s1.final_residuals[1] <= cfg.tol_ra


def test_s1_trace_finite_and_valid_records(cfg, s1):
    for rec in s1.trace:
        if rec.valid:
            assert np.isfinite(rec.R_w)
            assert np.isfinite(rec.R_ra)
            for i in (0, 1):
                assert rec.K[i] > 0.0
                assert rec.Ldest[i] > 0.0
                assert rec.Y[i] > 0.0
                assert rec.w_hat[i] > 0.0
                assert np.isfinite(rec.r_hat_a[i])


# ---------------------------------------------------------------------------
# 5. S2 region-order invariance
# ---------------------------------------------------------------------------


def test_s2_region_order_invariance(cfg, s2):
    assert s2.pass_bool
    assert s2.max_diff <= cfg.order_invariance_tol
    assert s2.record_order12.valid
    assert s2.record_order21.valid


# ---------------------------------------------------------------------------
# 6. deterministic reproducibility (fresh construction)
# ---------------------------------------------------------------------------


def test_reproducibility_s0(cfg, base, firm):
    grid, params, numerics = base
    r1 = run_s0(cfg, grid, params, numerics, firm)
    g2, p2, n2 = build_fixture(cfg)
    r2 = run_s0(cfg, g2, p2, n2, firm)
    assert r1.pass_bool == r2.pass_bool
    assert r1.reason == r2.reason
    assert max_numeric_diff(canonical_numbers(r1.record), canonical_numbers(r2.record)) <= cfg.reproducibility_tol


def test_reproducibility_s1(cfg, base, firm):
    grid, params, numerics = base
    r1 = run_s1(cfg, grid, params, numerics, firm)
    g2, p2, n2 = build_fixture(cfg)
    r2 = run_s1(cfg, g2, p2, n2, firm)
    assert r1.stop_reason == r2.stop_reason
    assert r1.iterations == r2.iterations
    max_diff = 0.0
    for a, b in zip(r1.trace, r2.trace):
        max_diff = max(max_diff, max_numeric_diff(canonical_numbers(a), canonical_numbers(b)))
    assert max_diff <= cfg.reproducibility_tol


# ---------------------------------------------------------------------------
# R1-A: S1 per-turn validity-bundle enforcement
# ---------------------------------------------------------------------------


def test_s1_validity_gate_enforcement(cfg, base, firm):
    """A failing validity gate on a valid turn must stop with VALIDITY_GATE_FAILED."""
    grid, params, numerics = base
    # Negative accounting tolerance makes the accounting gate deterministically fail.
    bad_cfg = dataclasses.replace(cfg, accounting_tol=-1.0)
    r = run_s1(bad_cfg, grid, params, numerics, firm)
    assert r.stop_reason.startswith("VALIDITY_GATE_FAILED:")
    assert r.iterations == 1
    assert len(r.trace) == 1
    assert r.trace[-1].valid  # turn preserved in trace


def test_s1_valid_turns_pass_validity_bundle(cfg, s1):
    """All valid S1 turns satisfy the full frozen validity bundle (no regression)."""
    for rec in s1.trace:
        if rec.valid:
            ok, detail, _ = validity_bundle(cfg, rec)
            assert ok, (rec.gamma, detail)


# ---------------------------------------------------------------------------
# R1-B: required trace fields
# ---------------------------------------------------------------------------


def _field_index():
    return {f: i for i, f in enumerate(S0_TRACE_FIELDS)}


def test_trace_required_fields_valid_turn(cfg, s0):
    idx = _field_index()
    for f in ("P11", "P12", "P21", "P22", "lambda",
              "gamma_next_w1", "gamma_next_w2", "gamma_next_ra1", "gamma_next_ra2"):
        assert f in idx, f
    row = _trace_row(s0.record, "PASS", cfg)
    assert row[idx["P11"]] == 0.9
    assert row[idx["P12"]] == 0.1
    assert row[idx["P21"]] == 0.1
    assert row[idx["P22"]] == 0.9
    assert row[idx["lambda"]] == 0.5
    gnext = [row[idx[f]] for f in ("gamma_next_w1", "gamma_next_w2", "gamma_next_ra1", "gamma_next_ra2")]
    assert all(np.isfinite(x) for x in gnext)


def test_trace_required_fields_blocked_terminal_turn(cfg, s1):
    idx = _field_index()
    blocked = s1.trace[-1]
    assert _is_blocked_stop(s1.stop_reason)
    row = _trace_row(blocked, s1.stop_reason, cfg)
    gnext = [row[idx[f]] for f in ("gamma_next_w1", "gamma_next_w2", "gamma_next_ra1", "gamma_next_ra2")]
    assert all(np.isnan(x) for x in gnext)
    assert row[idx["stop_reason"]] == s1.stop_reason


# ---------------------------------------------------------------------------
# R1-C: NaN-aware numeric comparison
# ---------------------------------------------------------------------------


def test_max_numeric_diff_nan_aware():
    assert max_numeric_diff([1.0, float("nan")], [1.0, float("nan")]) == 0.0
    assert max_numeric_diff([1.0, float("nan")], [1.0, 2.0]) == float("inf")
    assert max_numeric_diff([1.0, 2.0], [1.0, float("nan")]) == float("inf")
    assert max_numeric_diff([1.0, float("inf")], [1.0, float("inf")]) == 0.0
    assert max_numeric_diff([1.0, float("inf")], [1.0, float("-inf")]) == float("inf")
    assert max_numeric_diff([1.0, 2.0], [1.0, 3.0]) == 1.0
    assert max_numeric_diff([1.0, 2.0, 3.0], [1.0, 2.0]) == float("inf")
    assert max_numeric_diff([], []) == 0.0


# ---------------------------------------------------------------------------
# R1-D: fail-closed terminal classification
# ---------------------------------------------------------------------------


def _ok_s0():
    return SimpleNamespace(pass_bool=True)


def _ok_repro():
    return {"pass_bool": True, "within_tol": True}


def _ok_s2():
    return SimpleNamespace(pass_bool=True)


def test_terminal_classification_s2_failure_blocks_architecture_class():
    s1 = SimpleNamespace(stop_reason="ACCEPTED")
    cls = _terminal_classification(
        None, _ok_s0(), s1, SimpleNamespace(pass_bool=False), _ok_repro(), _ok_repro()
    )
    assert cls == "BLOCKED_DLH_5B_S2_ORDER_INVARIANCE_FAILED"
    assert "ARCHITECTURE_VALIDATED" not in cls


def test_terminal_classification_s0_repro_failure_blocks_architecture_class():
    s1 = SimpleNamespace(stop_reason="ACCEPTED")
    cls = _terminal_classification(
        None, _ok_s0(), s1, _ok_s2(), {"pass_bool": True, "within_tol": False}, _ok_repro()
    )
    assert cls == "BLOCKED_DLH_5B_S0_REPRODUCIBILITY_FAILED"
    assert "ARCHITECTURE_VALIDATED" not in cls


def test_terminal_classification_s1_repro_failure_blocks_architecture_class():
    s1 = SimpleNamespace(stop_reason="ACCEPTED")
    cls = _terminal_classification(
        None, _ok_s0(), s1, _ok_s2(), _ok_repro(), {"pass_bool": False, "within_tol": True}
    )
    assert cls == "BLOCKED_DLH_5B_S1_REPRODUCIBILITY_FAILED"
    assert "ARCHITECTURE_VALIDATED" not in cls


def test_terminal_classification_accept_and_validity_fail_positive_classes():
    conv = _terminal_classification(
        None, _ok_s0(), SimpleNamespace(stop_reason="ACCEPTED"),
        _ok_s2(), _ok_repro(), _ok_repro(),
    )
    assert conv == "DLH_5B_TWO_REGION_ANCHOR_AND_PERTURBED_FIXED_POINT_CONVERGED__READY_FOR_GPT_REVIEW"
    vgf = _terminal_classification(
        None, _ok_s0(), SimpleNamespace(stop_reason="VALIDITY_GATE_FAILED:accounting:origin0_conservation=False"),
        _ok_s2(), _ok_repro(), _ok_repro(),
    )
    assert vgf == "DLH_5B_TWO_REGION_ARCHITECTURE_VALIDATED__PERTURBED_PATH_VALIDITY_GATE_FAILED_READY_FOR_GPT_REVIEW"
    hb = _terminal_classification(
        None, _ok_s0(), SimpleNamespace(stop_reason="HOUSEHOLD_BLOCK_FAILED:region0:..."),
        _ok_s2(), _ok_repro(), _ok_repro(),
    )
    assert hb == "DLH_5B_TWO_REGION_ARCHITECTURE_VALIDATED__PERTURBED_PATH_HOUSEHOLD_BLOCKED_READY_FOR_GPT_REVIEW"


# ---------------------------------------------------------------------------
# R1-E: no regression of predecessor S0/S1 observed scientific outcome
# ---------------------------------------------------------------------------


def test_s0_s1_predecessor_outcome_no_regression(cfg, s0, s1):
    # S0 anchor smoke still passes (same as predecessor evidence).
    assert s0.pass_bool
    assert s0.record.R_w <= cfg.s0_tol_w
    assert s0.record.R_ra <= cfg.s0_tol_ra
    # S1 observed predecessor outcome preserved: region-0 household KFE
    # fail-closed at iteration 4 after three valid turns (GPT-cited evidence).
    assert s1.stop_reason.startswith("HOUSEHOLD_BLOCK_FAILED:region0:")
    assert s1.iterations == 4
    # Residuals across the valid turns are non-increasing (deterministic trend).
    valid = [rec for rec in s1.trace if rec.valid]
    assert len(valid) == 3
    rws = [rec.R_w for rec in valid]
    assert all(b <= a for a, b in zip(rws, rws[1:]))
