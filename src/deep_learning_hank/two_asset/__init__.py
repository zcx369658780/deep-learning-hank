"""DLH-4A two-asset HANK household HJB/KFE reconstruction kernel (Issue #17).

Faithful Python reconstruction of the legacy two-asset household kernel
(``HANK_2ASSETS_HJB.m`` reference family):

- state ``(b, a, z)``: liquid asset ``b`` (borrowing allowed with premium),
  illiquid asset ``a >= 0`` (curved return), two-state idiosyncratic CTMC ``z``;
- controls: consumption ``c``, endogenous static labor ``l``, illiquid-asset
  transfer ``d`` with explicit adjustment cost ``chi(d,a)`` (inaction band);
- continuous-time upwind HJB (forward/backward derivatives in both asset
  dimensions, candidate policies, Hamiltonian selection, boundary treatment);
- infinitesimal generator ``G = G_b + G_a + G_z`` shared by the HJB and KFE;
- stationary KFE ``G^T g = 0`` for the density ``g(b,a,z)`` with mass
  normalization and non-negativity diagnostics;
- separate asset aggregates ``A_hh = int a g`` and ``B_hh = int b g``
  (never merged, never assumed equal).

Evidence labels: ``VALIDATION_FIXTURE_NOT_CALIBRATION``,
``TWO_ASSET_HANK_HOUSEHOLD_KERNEL_ONLY``.
This is a reconstruction of the household kernel only; no firm/monetary/
fiscal/regional closure and no neural components are included.
"""

from deep_learning_hank.two_asset.config import TwoAssetConfig
from deep_learning_hank.two_asset.household_hjb import (
    TwoAssetHouseholdResult,
    solve_two_asset_household,
)
from deep_learning_hank.two_asset.kfe import (
    TwoAssetKfeResult,
    solve_two_asset_kfe,
)
from deep_learning_hank.two_asset.diagnostics import (
    TwoAssetDiagnostics,
    run_two_asset_diagnostics,
)

__all__ = [
    "TwoAssetConfig",
    "TwoAssetDiagnostics",
    "TwoAssetHouseholdResult",
    "TwoAssetKfeResult",
    "run_two_asset_diagnostics",
    "solve_two_asset_household",
    "solve_two_asset_kfe",
]
