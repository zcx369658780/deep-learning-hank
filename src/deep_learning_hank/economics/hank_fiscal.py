"""DLH-3B fiscal / bond block (isolated HANK module).

Frozen DLH-3A R1 steady-state fiscal conventions (Issue #11 §4.4):

- constant real government bond supply ``B`` (``B_t ≡ B``, ``dot B = 0``);
- public purchases ``G = 0``;
- tax revenue ``T = tau_l * w * N``;
- government budget ``r*B + tr = T`` (no seigniorage, no issuance);
- lump-sum transfer ``tr = T - r*B``;
- firm profits are distributed lump-sum per capita (household block input).

``VALIDATION_FIXTURE_NOT_CALIBRATION``.
"""

from __future__ import annotations

from dataclasses import dataclass

__all__ = ["HankFiscalResult", "hank_fiscal"]


@dataclass(frozen=True)
class HankFiscalResult:
    tax_revenue: float
    bond_service: float
    transfer: float
    public_outlay: float
    residual: float


def hank_fiscal(
    *, wage: float, labor: float, real_return: float, bond_supply: float, tau_l: float, public_outlay: float
) -> HankFiscalResult:
    """Constant-bond fiscal closure: ``T = tau_l*w*N``, ``tr = T - r*B``.

    The residual ``T - r*B - tr`` is computed, never set to zero by labeling.
    """
    if wage < 0.0 or labor < 0.0:
        raise ValueError("wage and labor must be nonnegative")
    if bond_supply < 0.0 or public_outlay < 0.0:
        raise ValueError("bond supply and public outlay must be nonnegative")
    if tau_l < 0.0 or tau_l >= 1.0:
        raise ValueError("labor tax rate must lie in [0, 1)")
    tax_revenue = tau_l * wage * labor
    bond_service = real_return * bond_supply
    transfer = tax_revenue - bond_service - public_outlay
    residual = tax_revenue - bond_service - public_outlay - transfer
    return HankFiscalResult(
        tax_revenue=float(tax_revenue),
        bond_service=float(bond_service),
        transfer=float(transfer),
        public_outlay=float(public_outlay),
        residual=float(residual),
    )
