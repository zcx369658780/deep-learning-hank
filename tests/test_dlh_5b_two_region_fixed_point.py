"""DLH-5B (Issue #25) focused tests: deterministic two-region fixed-point prototype.

Validates the frozen fixture, one-shot anchor derivation, S0 anchor smoke, S1
perturbed outer iteration, S2 region-order invariance, conservation/accounting
gates, HJB/KFE/boundary diagnostics, firm validity and deterministic
reproducibility. Household solves call the accepted oracle; the module under
test does not reimplement HJB/KFE logic.
"""

from __future__ import annotations

import numpy as np
import pytest

from deep_learning_hank.regional.two_region_fixed_point import (
    FrozenFirmParams,
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
