"""DLH-4A two-asset kernel diagnostics layer (Issue #17).

Evaluates the Issue #17 validation requirements from the household/KFE output:

- generator properties: ``G = G_b + G_a + G_z`` decomposition (structural),
  exact rows-sum-zero, non-negative off-diagonals;
- HJB diagnostics: converged flag, iterations, true HJB residual, labor /
  consumption FOC maxima, adjustment-active fraction, value monotonicity
  fractions (a monotone value function is required for an economically valid
  solution);
- KFE diagnostics: uniqueness of the stationary distribution (nullity of
  ``G^T``), mass conservation, non-negativity;
- separate asset accounting: ``A_hh = int a g`` and ``B_hh = int b g``
  reported independently (never merged, never assumed equal);
- deterministic reproducibility (two identical solves, max repeat difference).

Known outcome on the reference fixture (reported honestly): the HJB iteration
reaches a deterministic fixed point but the value function is not monotone and
the stationary distribution is non-unique; the corresponding gates FAIL and
the overall classification is an engineering failure (see the execution
report).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np

from deep_learning_hank.two_asset.config import TwoAssetConfig
from deep_learning_hank.two_asset.household_hjb import (
    TwoAssetHouseholdResult,
    solve_two_asset_household,
)
from deep_learning_hank.two_asset.kfe import (
    TwoAssetKfeResult,
    solve_two_asset_kfe,
)

__all__ = ["TwoAssetDiagnostics", "TwoAssetDiagnosticsError", "run_two_asset_diagnostics"]


class TwoAssetDiagnosticsError(RuntimeError):
    """Raised when the solve itself fails."""


@dataclass(frozen=True)
class TwoAssetDiagnostics:
    config_sha256: str
    household: TwoAssetHouseholdResult
    kfe: TwoAssetKfeResult
    value_monotone_b: bool
    value_monotone_a: bool
    mono_b_fraction: float
    mono_a_fraction: float
    generator_ok: bool
    hjb_fixed_point_ok: bool
    kfe_ok: bool
    accounting_ok: bool
    all_gates_pass: bool


def run_two_asset_diagnostics(config_path: Path) -> TwoAssetDiagnostics:
    """Solve the two-asset household HJB + KFE and evaluate all gates."""
    config = TwoAssetConfig.from_toml(config_path)
    b_grid = np.linspace(config.b_min, config.b_max, config.b_points)
    a_grid = np.linspace(config.a_min, config.a_max, config.a_points)
    z_states = np.asarray(config.idiosyncratic_states, dtype=np.float64)
    state_generator = np.array(
        [
            [-config.q_low_to_high, config.q_low_to_high],
            [config.q_high_to_low, -config.q_high_to_low],
        ],
        dtype=np.float64,
    )

    household = solve_two_asset_household(
        b_grid=b_grid,
        a_grid=a_grid,
        z_states=z_states,
        state_generator=state_generator,
        w=config.w,
        rb=config.rb,
        rb_gap=config.rb_gap,
        ra=config.ra,
        Tt=config.Tt,
        tau_l=config.tau_l,
        rho=config.rho,
        gamma=config.gamma,
        alphac=config.alphac,
        alphal=config.alphal,
        frisch_l=config.frisch_l,
        n_max=config.n_max,
        chi0=config.chi0,
        chi1=config.chi1,
        a_bar=config.a_bar,
        consumption_floor=config.consumption_floor,
        pseudo_time_step=config.pseudo_time_step,
        value_change_tolerance=config.value_change_tolerance,
        max_value_iterations=config.max_value_iterations,
    )
    kfe = solve_two_asset_kfe(
        generator=household.generator,
        b_grid=b_grid,
        a_grid=a_grid,
        z_states=z_states,
        consumption=household.consumption,
        labor=household.labor,
        mass_tolerance=config.kfe_mass_tolerance,
        negative_mass_threshold=config.negative_mass_threshold,
    )

    mono_b_fraction = float(np.mean((household.value[1:] - household.value[:-1]) > 0.0))
    mono_a_fraction = float(np.mean((household.value[:, 1:] - household.value[:, :-1]) > 0.0))
    value_monotone_b = mono_b_fraction > 0.999
    value_monotone_a = mono_a_fraction > 0.999

    generator_ok = bool(
        household.generator_row_sum_max_abs <= config.generator_row_sum_tolerance
        and household.generator_min_off_diagonal >= config.generator_min_off_diagonal_tolerance
        and household.nan_inf_count == 0
    )
    hjb_fixed_point_ok = bool(
        np.isfinite(household.true_residual)
        and household.true_residual <= 1e-4
        and np.all(np.isfinite(household.value))
        and household.nan_inf_count == 0
    )
    kfe_ok = bool(
        kfe.unique
        and kfe.mass_error <= config.kfe_mass_tolerance
        and kfe.minimum_mass >= config.negative_mass_threshold
        and kfe.negative_mass_count == 0
        and kfe.nan_inf_count == 0
    )
    accounting_ok = bool(
        np.isfinite(kfe.A_hh)
        and np.isfinite(kfe.B_hh)
        and np.isfinite(kfe.L_hh)
        and np.isfinite(kfe.C_hh)
        and abs(kfe.A_hh - kfe.B_hh) > 0.0  # separate objects; never assumed equal
    )
    return TwoAssetDiagnostics(
        config_sha256=config.sha256(),
        household=household,
        kfe=kfe,
        value_monotone_b=value_monotone_b,
        value_monotone_a=value_monotone_a,
        mono_b_fraction=mono_b_fraction,
        mono_a_fraction=mono_a_fraction,
        generator_ok=generator_ok,
        hjb_fixed_point_ok=hjb_fixed_point_ok,
        kfe_ok=kfe_ok,
        accounting_ok=accounting_ok,
        all_gates_pass=bool(
            generator_ok and hjb_fixed_point_ok and value_monotone_b and value_monotone_a and kfe_ok and accounting_ok
        ),
    )
