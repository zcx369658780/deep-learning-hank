"""Pure-function economics helpers for the DLH-4A two-asset household kernel.

Mirrors the legacy Matlab reference semantics (``HANK_2ASSETS_HJB.m``,
``HANK3_FOC.m``, ``HANK3_cost.m``, ``lab_solve2.m``):

- CRRA consumption utility ``u(c) = alphac*c^(1-ga)/(1-ga)``;
- labor disutility ``v(l) = alphal*l^(1+1/frisch_l)/(1+1/frisch_l)``;
- static labor FOC ``v'(l) = (1-tau)*w*z*V_b`` (liquidity marginal value);
- adjustment transfer FOC (inaction band):
  ``d = (min(x/y - 1 + chi0, 0) + max(x/y - 1 - chi0, 0)) * a / chi1``;
- adjustment cost ``chi(d,a) = chi0*|d| + chi1*d^2/2 * max(a, a_bar)^(-1)``;
- curved illiquid return ``raah(a) = ra*(1 - 0.1*(amax/a)^(-9))``
  (at ``a = 0``: ``raah = ra``; consistent with the legacy formula limit).

Documented legacy observation: the reference computes the zero-drift labor
initialization with a ``raah^2`` term (``tempMat = Rah.*raah + Rb.*bbb + Tt``);
this reconstruction uses the self-consistent zero-drift consumption base
``c0 = (1-tau)*w*z*l0 + Tt + Rb*b`` (identical to the reference ``C_0``), and
the illiquid return enters only through the illiquid drift ``da = d + raah*a``
and the HJB envelope. See ``DLH_4A_PRECODING_MAPPING.md`` §2.3.
"""

from __future__ import annotations

import numpy as np
import numpy.typing as npt

__all__ = [
    "adjustment_cost",
    "adjustment_transfer",
    "curved_illiquid_return",
    "labor_disutility",
    "labor_policy_from_marginal",
    "marginal_labor_disutility",
    "marginal_utility",
    "solve_zero_drift_labor",
    "utility",
]

FloatArray = npt.NDArray[np.float64]


def utility(consumption: FloatArray, *, alphac: float, gamma: float) -> FloatArray:
    """``u(c) = alphac * c^(1-ga) / (1-ga)``."""
    return alphac * np.asarray(consumption, dtype=np.float64) ** (1.0 - gamma) / (1.0 - gamma)


def marginal_utility(consumption: FloatArray, *, alphac: float, gamma: float) -> FloatArray:
    """``u'(c) = alphac * c^(-ga)``."""
    return alphac * np.asarray(consumption, dtype=np.float64) ** (-gamma)


def labor_disutility(labor: FloatArray, *, alphal: float, frisch_l: float) -> FloatArray:
    """``v(l) = alphal * l^(1+1/frisch_l) / (1+1/frisch_l)``."""
    exponent = 1.0 + 1.0 / frisch_l
    return alphal * np.asarray(labor, dtype=np.float64) ** exponent / exponent


def marginal_labor_disutility(labor: FloatArray, *, alphal: float, frisch_l: float) -> FloatArray:
    """``v'(l) = alphal * l^(1/frisch_l)``."""
    return alphal * np.asarray(labor, dtype=np.float64) ** (1.0 / frisch_l)


def labor_policy_from_marginal(
    effective_wage: FloatArray,
    liquid_marginal_value: FloatArray,
    *,
    alphal: float,
    frisch_l: float,
    n_max: float,
) -> FloatArray:
    """Static labor FOC ``v'(l) = (1-tau)*w*z*V_b`` with KKT clip to ``[0, n_max]``."""
    raw = (
        np.asarray(effective_wage, dtype=np.float64)
        * np.asarray(liquid_marginal_value, dtype=np.float64)
        / alphal
    ) ** frisch_l
    return np.clip(raw, 0.0, n_max)


def curved_illiquid_return(illiquid_grid: FloatArray, *, ra: float, a_max: float) -> FloatArray:
    """``raah(a) = ra*(1 - 0.1*(a_max/a)^(-9))``; at ``a=0``: ``raah = ra``."""
    with np.errstate(divide="ignore", invalid="ignore"):
        ratio = np.asarray(illiquid_grid, dtype=np.float64)
        curvature = (a_max / ratio) ** (-9.0)
        # At a=0: (a_max/0)^(-9) = inf^(-9) = 0.0 -> raah = ra.
        curvature = np.where(ratio > 0.0, curvature, 0.0)
    return ra * (1.0 - 0.1 * curvature)


def adjustment_transfer(
    illiquid_marginal: FloatArray,
    liquid_marginal: FloatArray,
    illiquid_holdings: FloatArray,
    *,
    chi0: float,
    chi1: float,
    a_bar: float,
) -> FloatArray:
    """Adjustment transfer FOC (inaction band) consistent with the cost function.

    ``d = (min(x/y - 1 + chi0, 0) + max(x/y - 1 - chi0, 0)) * max(a, a_bar) / chi1``,
    with ``x = V_a`` (illiquid marginal), ``y = V_b`` (liquid marginal),
    ``a`` = illiquid holdings.  Inaction when ``x/y in [1-chi0, 1+chi0]``.

    Documented legacy correction: the reference ``HANK3_FOC.m`` scales by ``a``
    (so ``d = 0`` at ``a = 0``, making zero illiquid holdings absorbing), while
    its cost ``HANK3_cost.m`` scales by ``max(a, a_bar)``.  Using the cost's
    scale keeps the FOC consistent with the stated cost function and removes
    the absorbing ``a = 0`` degeneracy (see ``DLH_4A_PRECODING_MAPPING.md``).
    """
    x = np.asarray(illiquid_marginal, dtype=np.float64)
    y = np.asarray(liquid_marginal, dtype=np.float64)
    a = np.asarray(illiquid_holdings, dtype=np.float64)
    safe_y = np.maximum(y, 1e-6)
    # Ratio cap: guards the transient against V_b -> 0 amplification; the
    # converged solution has moderate ratios so the cap is not binding there.
    ratio = np.clip(x / safe_y, -12.0, 12.0)
    scale = np.maximum(a, a_bar)
    d = (np.minimum(ratio - 1.0 + chi0, 0.0) + np.maximum(ratio - 1.0 - chi0, 0.0)) * scale / chi1
    return d


def adjustment_cost(
    transfer: FloatArray, illiquid_holdings: FloatArray, *, chi0: float, chi1: float, a_bar: float
) -> FloatArray:
    """``chi(d,a) = chi0*|d| + chi1*d^2/2 * max(a, a_bar)^(-1)``."""
    d = np.asarray(transfer, dtype=np.float64)
    a = np.asarray(illiquid_holdings, dtype=np.float64)
    scale = 1.0 / np.maximum(a, a_bar)
    return chi0 * np.abs(d) + chi1 * d * d / 2.0 * scale


def solve_zero_drift_labor(
    effective_wage: float,
    liquid_base: float,
    *,
    alphac: float,
    alphal: float,
    gamma: float,
    frisch_l: float,
    n_max: float,
) -> tuple[float, float, bool]:
    """Zero-drift liquid policy: ``c0 = q*l0 + b0`` with the static labor FOC.

    FOC ``l0^(1/frisch_l) = (alphac/alphal)*q*c0^(-gamma)`` (monotone in ``l0``;
    scalar bracket root).  ``q`` = after-tax effective wage, ``b0`` = non-labor
    liquid income ``Tt + Rb*b``.  Returns ``(c0, l0, feasible)``.
    """
    if effective_wage <= 0.0:
        return (float("nan"), float("nan"), False)
    c_max = liquid_base + effective_wage * n_max
    if c_max <= 0.0:
        return (float("nan"), float("nan"), False)

    def f(l: float) -> float:
        c = liquid_base + effective_wage * l
        if c <= 1e-12:
            return -np.inf
        return l ** (1.0 / frisch_l) - (alphac / alphal) * effective_wage * c ** (-gamma)

    f_max = f(n_max)
    if f_max <= 0.0:
        return (float(c_max), float(n_max), True)
    l_min = max(0.0, (1e-12 - liquid_base) / effective_wage)
    f_min = f(l_min)
    if f_min >= 0.0:
        return (float("nan"), float("nan"), False)
    from scipy.optimize import brentq

    root = brentq(f, l_min, n_max, xtol=1e-14)
    return (float(liquid_base + effective_wage * root), float(root), True)
