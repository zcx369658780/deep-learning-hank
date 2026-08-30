"""Deterministic cold household initialization adapter (DLH-4D, Issue #20).

Implements the Issue #20 "Deterministic household initialization adapter"
OUTSIDE the immutable household package.  For each candidate GE point it
constructs, deterministically and from the candidate point alone (no
sequential previous-GE-point warm start):

1. effective liquid rate `r_b_eff = r_b + rb_gap` if `b < 0`, else `r_b`;
2. net wage `net_wage = (1 - tau) * w * z`;
3. baseline zero-adjustment-transfer liquid resources
   `c0(l) = net_wage * l + T + r_b_eff * b` (`T` = fiscal transfer income);
4. solve the static labor FOC for positive `c0` deterministically
   (`l^phi = net_wage * c0^(-gamma_c)`, scalar brentq);
5. initial consumption = `net_wage * l0 + T + r_b_eff * b + r_a_eff(a) * a`
   (adding the accepted effective illiquid-return income);
6. initial value = flow utility / `rho`.

Deterministic bracketing only; if no positive-consumption labor root exists at
any state, fail closed (fail-closed initialization; no tuning of economics or
the fixture).
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import brentq

from deep_learning_hank.two_asset.matlab_faithful_two_asset_ha import (
    EconomicParams,
    HouseholdInputs,
    MatlabFaithfulHJBGrid,
    flow_utility,
    matlab_faithful_illiquid_return,
)

__all__ = ["InitializationError", "build_cold_initialization"]

LABOR_BRACKET_LOW = 1e-8
LABOR_BRACKET_HIGH = 5.0


class InitializationError(RuntimeError):
    """Raised when a deterministic positive-consumption labor root cannot be
    constructed at some state (fail-closed initialization)."""


def _zero_drift_labor(
    net_wage: float,
    liquid_base: float,
    params: EconomicParams,
) -> tuple[float, float]:
    """Solve `l^phi = net_wage * c0^(-gamma_c)` with `c0 = net_wage*l + base`."""
    if net_wage <= 0.0:
        raise InitializationError("non-positive net wage in initialization")
    c_max = liquid_base + net_wage * LABOR_BRACKET_HIGH
    if c_max <= 0.0:
        raise InitializationError("no positive-consumption labor root (base too low)")

    def f(l: float) -> float:
        c = liquid_base + net_wage * l
        if c <= 1e-12:
            return -np.inf
        return l ** params.phi - net_wage * c ** (-params.gamma_c)

    f_max = f(LABOR_BRACKET_HIGH)
    if f_max <= 0.0:
        return float(c_max), float(LABOR_BRACKET_HIGH)
    l_min = max(0.0, (1e-12 - liquid_base) / net_wage)
    f_min = f(l_min)
    if f_min >= 0.0:
        raise InitializationError("no feasible interior labor root")
    root = brentq(f, l_min, LABOR_BRACKET_HIGH, xtol=1e-14)
    return float(liquid_base + net_wage * root), float(root)


def build_cold_initialization(
    grid: MatlabFaithfulHJBGrid,
    params: EconomicParams,
    *,
    r_a: float,
    r_b: float,
    w: float,
    transfer_income: float,
    rb_gap: float,
    tau: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Deterministic cold initialization at one candidate GE point.

    Returns ``(initial_value, baseline_labor)`` with shape ``(I, J, Nz)``.
    """
    b = grid.b
    a = grid.a
    z = grid.z
    shape = (b.size, a.size, z.size)
    labor0 = np.empty(shape)
    initial = np.empty(shape)
    inputs = HouseholdInputs(
        r_a=r_a,
        r_b=r_b,
        tau=tau,
        wages=np.array([w]),
        migration_costs=np.array([0.0]),
        labor_weights=np.array([1.0]),
    )
    for nz in range(z.size):
        for j in range(a.size):
            for i in range(b.size):
                rb_eff = r_b + (rb_gap if b[i] < 0.0 else 0.0)
                base = transfer_income + rb_eff * b[i]
                net = (1.0 - tau) * w * z[nz]
                c0, l0 = _zero_drift_labor(net, base, params)
                r_a_eff = float(matlab_faithful_illiquid_return(a[j], a[-1], r_a))
                c_full = c0 + r_a_eff * a[j]
                labor0[i, j, nz] = l0
                initial[i, j, nz] = flow_utility(
                    c_full, np.array([l0]), inputs, params
                ) / params.rho
    return initial, labor0
