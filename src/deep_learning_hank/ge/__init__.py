"""DLH-4D minimal single-region two-asset GE steady-state layer (Issue #20).

This package hosts the GE-layer code that sits AROUND the immutable accepted
two-asset household oracle (`deep_learning_hank.two_asset.
matlab_faithful_two_asset_ha`, read-only):

- deterministic cold household initialization adapter
  (`two_asset_initialization`), implemented outside the immutable package;
- the frozen Option A single-region GE steady-state solver
  (`two_asset_single_region`): nested deterministic Brent solves with the
  frozen domains and bracketing protocol; faithful resource/accounting
  diagnostics with the taper wedge `W_taper`.

Labels (per Issue #19 Owner clarification): the illiquid-return taper and the
contaminated-row KFE inside the oracle are `NUMERICAL_REGULARIZATION /
MATLAB_FAITHFUL_IMPLEMENTATION`; the GE closure is
`NEW_SINGLE_REGION_GE_CLOSURE_DESIGN`.  No household mutation is performed.
"""

from deep_learning_hank.ge.two_asset_initialization import (
    build_cold_initialization,
)
from deep_learning_hank.ge.two_asset_single_region import (
    GeConfig,
    GeDiagnostics,
    GeEvaluation,
    GeRootResult,
    GeSolveError,
    RootBracketError,
    evaluate_ge,
    solve_ge,
)

__all__ = [
    "GeConfig",
    "GeDiagnostics",
    "GeEvaluation",
    "GeRootResult",
    "GeSolveError",
    "RootBracketError",
    "build_cold_initialization",
    "evaluate_ge",
    "solve_ge",
]
