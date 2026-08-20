"""Canonical one-asset continuous-time HANK validation kernel (DLH-3B-R2).

This package is a clean, self-contained reimplementation of the accepted
one-asset HANK household/distribution/equilibrium semantics (Issue #15):

- one liquid risk-free real bond asset ``a``, two-state idiosyncratic CTMC ``z``;
- CRRA + endogenous static labor;
- continuous-time HJB (upwind, state-constraint boundaries, pseudo-time value
  iteration) sharing one infinitesimal generator with the KFE;
- stationary KFE ``G^T g = 0`` with mass conservation;
- deterministic equilibrium fixed point (labor root + asset root);
- transparent residual reporting (HJB, KFE/mass, asset, labor, fiscal,
  profits, goods, wealth flow).

Evidence labels: ``VALIDATION_FIXTURE_NOT_CALIBRATION``,
``D2_MACHINE_DIAGNOSTIC``-style kernel validation evidence.
The kernel is not a Matlab translation and makes no Matlab-parity claim.
"""

from deep_learning_hank.ha_kernel.household import (
    HouseholdKernelResult,
    solve_kernel_household,
)
from deep_learning_hank.ha_kernel.distribution import (
    KernelDistributionResult,
    solve_kernel_distribution,
)
from deep_learning_hank.ha_kernel.equilibrium import (
    KernelEquilibriumResult,
    solve_kernel_equilibrium,
)
from deep_learning_hank.ha_kernel.diagnostics import (
    KernelDiagnostics,
    run_kernel_diagnostics,
)

__all__ = [
    "HouseholdKernelResult",
    "KernelDiagnostics",
    "KernelDistributionResult",
    "KernelEquilibriumResult",
    "run_kernel_diagnostics",
    "solve_kernel_distribution",
    "solve_kernel_equilibrium",
    "solve_kernel_household",
]
