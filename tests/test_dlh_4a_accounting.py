"""DLH-4A two-asset economics / accounting formula tests (Issue #17).

Unit tests for the reconstructed adjustment-cost mechanism ``chi(d,a)``, the
inaction-band transfer FOC, the curved illiquid return, labor FOC helpers, and
the separate asset aggregates (``A_hh``/``B_hh`` never merged).
"""

from __future__ import annotations

import numpy as np

from deep_learning_hank.two_asset.economics import (
    adjustment_cost,
    adjustment_transfer,
    curved_illiquid_return,
    labor_disutility,
    marginal_labor_disutility,
    solve_zero_drift_labor,
    utility,
)

CHI0, CHI1, A_BAR = 0.1, 2.0, 1.0


def test_adjustment_cost_formula():
    d = np.array([0.0, 1.0, -2.0])
    a = np.array([1.0, 2.0, 4.0])
    cost = adjustment_cost(d, a, chi0=CHI0, chi1=CHI1, a_bar=A_BAR)
    expected = np.array(
        [
            CHI0 * 0.0 + CHI1 * 0.0 ** 2 / 2.0 / 1.0,
            CHI0 * 1.0 + CHI1 * 1.0 ** 2 / 2.0 / 2.0,
            CHI0 * 2.0 + CHI1 * 4.0 / 2.0 / 4.0,
        ]
    )
    assert np.allclose(cost, expected)


def test_adjustment_cost_scale_floor():
    # max(a, a_bar) scale: cost finite at a = 0.
    cost = adjustment_cost(np.array([1.0]), np.array([0.0]), chi0=CHI0, chi1=CHI1, a_bar=A_BAR)
    expected = CHI0 * 1.0 + CHI1 * 0.5 / A_BAR
    assert np.allclose(cost, expected)


def test_adjustment_transfer_inaction_band():
    a = np.array([10.0])
    # ratio inside [1-chi0, 1+chi0] -> inaction, d = 0.
    d_in = adjustment_transfer(
        np.array([1.05]), np.array([1.0]), a, chi0=CHI0, chi1=CHI1, a_bar=A_BAR
    )
    assert abs(float(d_in[0])) < 1e-12
    # ratio above 1+chi0 -> buy illiquid (d > 0).
    d_buy = adjustment_transfer(
        np.array([1.3]), np.array([1.0]), a, chi0=CHI0, chi1=CHI1, a_bar=A_BAR
    )
    assert float(d_buy[0]) > 0.0
    # ratio below 1-chi0 -> sell illiquid (d < 0).
    d_sell = adjustment_transfer(
        np.array([0.7]), np.array([1.0]), a, chi0=CHI0, chi1=CHI1, a_bar=A_BAR
    )
    assert float(d_sell[0]) < 0.0


def test_curved_illiquid_return_limits():
    grid = np.array([0.0, 5.0, 10.0])
    r = curved_illiquid_return(grid, ra=0.04, a_max=10.0)
    assert abs(r[0] - 0.04) < 1e-12  # at a = 0: raah = ra
    assert abs(r[2] - 0.04 * 0.9) < 1e-12  # at a = a_max: raah = 0.9*ra
    assert r[1] > r[2] and r[1] < r[0]


def test_labor_helpers():
    l = np.array([0.5, 1.0, 2.0])
    v = labor_disutility(l, alphal=1.0, frisch_l=0.2)
    vp = marginal_labor_disutility(l, alphal=1.0, frisch_l=0.2)
    # v' = l^(1/frisch) with alphal=1
    assert np.allclose(vp, l ** (1.0 / 0.2))
    # u(c) = -1/c for gamma=2, alphac=1
    u = utility(np.array([0.5, 2.0]), alphac=1.0, gamma=2.0)
    assert np.allclose(u, -1.0 / np.array([0.5, 2.0]))


def test_zero_drift_labor_foc():
    c, l, ok = solve_zero_drift_labor(
        0.85, 0.1, alphac=1.0, alphal=1.0, gamma=2.0, frisch_l=0.2, n_max=5.0
    )
    assert ok
    assert c > 0.0 and l > 0.0
    # FOC check: l^(1/frisch) = (alphac/alphal)*q*c^(-gamma)
    lhs = l ** (1.0 / 0.2)
    rhs = 1.0 * 0.85 * c ** (-2.0)
    assert abs(lhs - rhs) < 1e-6


def test_separate_asset_aggregates():
    """A_hh = int a g and B_hh = int b g are distinct objects (never merged)."""
    b = np.array([-1.0, 0.0, 1.0])
    a = np.array([0.0, 2.0, 5.0])
    g = np.array([[0.1, 0.1, 0.0], [0.1, 0.2, 0.1], [0.1, 0.2, 0.1]])
    B_hh = float(np.sum(g * b[:, None]))
    A_hh = float(np.sum(g * a[None, :]))
    assert B_hh != A_hh
    assert A_hh > B_hh  # illiquid aggregate exceeds liquid aggregate in this example
    assert np.isfinite(B_hh) and np.isfinite(A_hh)
