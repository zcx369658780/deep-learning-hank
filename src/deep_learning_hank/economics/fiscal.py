"""Minimal lump-sum / balanced fiscal helper (Tier-0).

Balanced budget: ``labor_tax_revenue = tau_l * wage * labor``;
``transfer = labor_tax_revenue - public_outlay``; fiscal residual = 0 by
construction.  No SOE rent, no debt, no distortionary taxation.
"""

from __future__ import annotations

from dataclasses import dataclass

__all__ = ["FiscalResult", "balanced_fiscal"]


@dataclass(frozen=True)
class FiscalResult:
    labor_tax_revenue: float
    public_outlay: float
    transfer: float
    residual: float


def balanced_fiscal(*, wage: float, labor: float, tau_l: float, public_outlay: float = 0.0) -> FiscalResult:
    labor_tax_revenue = tau_l * wage * labor
    transfer = labor_tax_revenue - public_outlay
    residual = labor_tax_revenue - public_outlay - transfer
    return FiscalResult(
        labor_tax_revenue=float(labor_tax_revenue),
        public_outlay=float(public_outlay),
        transfer=float(transfer),
        residual=float(residual),
    )
