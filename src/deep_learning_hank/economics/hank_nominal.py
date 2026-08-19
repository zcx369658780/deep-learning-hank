"""DLH-3B nominal block residuals (isolated HANK module).

Frozen DLH-3A R1 conventions (Issue #11 §4.3): zero-inflation / zero-shock
steady state with

- Fisher: ``i = r + pi``;
- Taylor: ``i = r_bar + pi_bar + phi_pi*(pi - pi_bar) + epsilon_i``,
  ``pi_bar = 0``, ``phi_pi > 1``, ``epsilon_i = 0``;
- at steady state ``r_bar = r`` so ``i* = r*``;
- frozen linearized NKPC ``pi_dot = rho_hh*pi - (epsilon/phi_p)*(mc - 1/mu)``.

All residuals are computed, never set to zero by labeling.
``VALIDATION_FIXTURE_NOT_CALIBRATION``.
"""

from __future__ import annotations

from dataclasses import dataclass

__all__ = ["HankNominalResult", "hank_nominal"]


@dataclass(frozen=True)
class HankNominalResult:
    interest_rate: float
    real_rate_bar: float
    inflation: float
    fisher_residual: float
    taylor_residual: float
    nkpc_residual: float


def hank_nominal(
    *,
    real_return: float,
    inflation: float,
    inflation_dot: float,
    marginal_cost: float,
    epsilon: float,
    phi_p: float,
    rho_hh: float,
    phi_pi: float,
    pi_bar: float,
    epsilon_i: float,
) -> HankNominalResult:
    """Nominal consistency residuals at the DLH-3B steady state."""
    if phi_p <= 0.0 or rho_hh <= 0.0:
        raise ValueError("phi_p and rho_hh must be strictly positive")
    if phi_pi <= 1.0:
        raise ValueError("Taylor principle requires phi_pi > 1 (frozen convention)")
    markup = epsilon / (epsilon - 1.0)
    interest_rate = real_return + inflation
    real_rate_bar = real_return
    fisher_residual = interest_rate - real_return - inflation
    taylor_residual = interest_rate - (
        real_rate_bar + pi_bar + phi_pi * (inflation - pi_bar) + epsilon_i
    )
    nkpc_residual = inflation_dot - rho_hh * inflation + (epsilon / phi_p) * (
        marginal_cost - 1.0 / markup
    )
    return HankNominalResult(
        interest_rate=float(interest_rate),
        real_rate_bar=float(real_rate_bar),
        inflation=float(inflation),
        fisher_residual=float(fisher_residual),
        taylor_residual=float(taylor_residual),
        nkpc_residual=float(nkpc_residual),
    )
