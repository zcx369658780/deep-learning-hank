"""Stationary distribution / Kolmogorov-forward (KFE) solver (Tier-0).

Contract: solve ``G.T @ g = 0`` with explicit mass normalization; report
stationarity residual, mass error, minimum mass / negative-mass count, state
marginals, mean assets and consumption, boundary mass, NaN/Inf count.
Tiny-negative numerical cleanup is allowed only if pre-cleanup minimum mass
and the cleanup rule are reported.

REIMPLEMENTATION (clean economics/solver separation) based on the audited
source pattern ``distribution_kfe.py``; no wholesale copy.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt
from scipy import sparse

__all__ = ["DistributionSolution", "solve_stationary_distribution"]

FloatArray = npt.NDArray[np.float64]


@dataclass(frozen=True)
class DistributionSolution:
    mass: FloatArray
    stationarity_residual: float
    mass_error: float
    minimum_mass: float
    pre_cleanup_minimum_mass: float
    cleanup_rule: str
    negative_mass_count: int
    nan_inf_count: int
    state_marginals: FloatArray
    mean_assets: float
    mean_consumption: float
    lower_boundary_mass: float
    upper_boundary_mass: float


def solve_stationary_distribution(
    *,
    generator: sparse.csr_matrix,
    asset_grid: FloatArray,
    consumption: FloatArray,
    stationarity_tolerance: float,
    mass_tolerance: float,
    negative_mass_threshold: float,
) -> DistributionSolution:
    state_count, asset_count = consumption.shape
    if generator.shape != (state_count * asset_count, state_count * asset_count):
        raise ValueError("generator and household arrays have incompatible dimensions")
    if not np.allclose(np.asarray(generator.sum(axis=1)).ravel(), 0.0, atol=1e-10):
        raise ValueError("generator must be a CTMC generator / intensity matrix (rows sum 0)")

    matrix = generator.T.toarray()
    matrix[-1, :] = 1.0
    rhs = np.zeros(state_count * asset_count, dtype=np.float64)
    rhs[-1] = 1.0
    raw_mass = np.linalg.solve(matrix, rhs)
    pre_cleanup_minimum_mass = float(np.min(raw_mass))
    if not np.all(np.isfinite(raw_mass)) or abs(float(np.sum(raw_mass))) < mass_tolerance:
        raise ValueError("KFE linear system returned invalid mass")

    mass = raw_mass / float(np.sum(raw_mass))
    tiny_negative = (mass < 0.0) & (mass >= negative_mass_threshold)
    if np.any(tiny_negative):
        mass = mass.copy()
        mass[tiny_negative] = 0.0
        mass /= float(np.sum(mass))
    shaped_mass = np.asarray(mass.reshape((state_count, asset_count)), dtype=np.float64)
    stationarity_residual = float(np.max(np.abs(generator.T @ mass)))
    mass_error = abs(float(np.sum(mass)) - 1.0)
    minimum_mass = float(np.min(mass))
    negative_mass_count = int(np.count_nonzero(mass < negative_mass_threshold))
    nan_inf_count = int(np.count_nonzero(~np.isfinite(mass)))
    state_marginals = np.asarray(shaped_mass.sum(axis=1), dtype=np.float64)
    mean_assets = float(np.sum(shaped_mass * asset_grid[None, :]))
    mean_consumption = float(np.sum(shaped_mass * consumption))
    lower_boundary_mass = float(np.sum(shaped_mass[:, 0]))
    upper_boundary_mass = float(np.sum(shaped_mass[:, -1]))
    return DistributionSolution(
        mass=shaped_mass,
        stationarity_residual=stationarity_residual,
        mass_error=mass_error,
        minimum_mass=minimum_mass,
        pre_cleanup_minimum_mass=pre_cleanup_minimum_mass,
        cleanup_rule=(
            "clip_to_zero_and_renormalize"
            if bool(np.any((raw_mass < 0.0) & (raw_mass >= negative_mass_threshold)))
            else "none"
        ),
        negative_mass_count=negative_mass_count,
        nan_inf_count=nan_inf_count,
        state_marginals=state_marginals,
        mean_assets=mean_assets,
        mean_consumption=mean_consumption,
        lower_boundary_mass=lower_boundary_mass,
        upper_boundary_mass=upper_boundary_mass,
    )
