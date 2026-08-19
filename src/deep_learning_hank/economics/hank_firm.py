"""DLH-3B labor-only production / price-setting block (isolated HANK module).

Frozen DLH-3A R1 steady-state implications used here (Issue #11 §4.2):

- labor-only technology ``Y_t = Z_t N_t`` (no productive capital);
- zero-inflation steady state ``pi = 0``;
- real marginal cost ``mc = 1/mu`` with markup ``mu = epsilon/(epsilon-1)``;
- real wage ``w = Z * mc = Z/mu``;
- firm profits at zero inflation ``Pi = Y - w*N``.

``phi_p`` is a validation-fixture Rotemberg coefficient; it does not create a
price-adjustment resource cost at ``pi = 0``.  ``VALIDATION_FIXTURE_NOT_CALIBRATION``.
"""

from __future__ import annotations

from dataclasses import dataclass

__all__ = ["HankProductionResult", "hank_production"]


@dataclass(frozen=True)
class HankProductionResult:
    output: float
    wage: float
    marginal_cost: float
    markup: float
    labor_demand: float
    profits: float


def hank_production(*, productivity: float, labor: float, epsilon: float) -> HankProductionResult:
    """Zero-inflation steady-state labor-only production block.

    ``labor`` is aggregate effective labor used in production (in equilibrium
    equal to household aggregate labor supply).  Returns output ``Y = Z*N``,
    markup ``mu``, steady-state marginal cost ``mc = 1/mu``, real wage
    ``w = Z*mc``, technological labor demand ``N^d = Y/Z``, and zero-inflation
    profits ``Pi = Y - w*N``.
    """
    if productivity <= 0.0:
        raise ValueError("aggregate productivity must be strictly positive")
    if labor < 0.0:
        raise ValueError("labor must be nonnegative")
    if epsilon <= 1.0:
        raise ValueError("demand elasticity must exceed one")
    markup = epsilon / (epsilon - 1.0)
    marginal_cost = 1.0 / markup
    output = productivity * labor
    wage = productivity * marginal_cost
    labor_demand = output / productivity
    profits = output - wage * labor
    return HankProductionResult(
        output=float(output),
        wage=float(wage),
        marginal_cost=float(marginal_cost),
        markup=float(markup),
        labor_demand=float(labor_demand),
        profits=float(profits),
    )
