"""Two-factor Cobb-Douglas firm block (Tier-0).

``Y = A * K^alpha_k * L^(1 - alpha_k)``.  No state-owned-services (SOE) third
factor, no nominal/price-adjustment block: those are out of Tier-0 scope.
"""

from __future__ import annotations

from dataclasses import dataclass

__all__ = ["ProductionResult", "production_block"]


@dataclass(frozen=True)
class ProductionResult:
    output: float
    mpk: float
    net_capital_return: float
    wage: float


def production_block(
    *,
    capital: float,
    labor: float,
    productivity: float,
    alpha_k: float,
    delta: float,
) -> ProductionResult:
    if min(capital, labor, productivity) <= 0.0:
        raise ValueError("production inputs must be strictly positive")
    if alpha_k <= 0.0 or alpha_k >= 1.0:
        raise ValueError("capital share must lie in (0, 1)")
    if delta < 0.0:
        raise ValueError("depreciation must be nonnegative")
    output = productivity * (capital**alpha_k) * (labor ** (1.0 - alpha_k))
    mpk = alpha_k * output / capital
    return ProductionResult(
        output=float(output),
        mpk=float(mpk),
        net_capital_return=float(mpk - delta),
        wage=float((1.0 - alpha_k) * output / labor),
    )
