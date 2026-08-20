"""DLH-4A two-asset stationary KFE solver (Issue #17).

Solves ``G^T g = 0`` for the density ``g(b, a, z)`` with the reference
normalization convention (density integrates to one against the grid measure
``db*da``).  The solve uses the null space of ``G^T`` (SVD), which is exact for
the singular stationary problem and avoids the conditioning pitfalls of a
fixed pinned row on near-degenerate generators.

If the generator is reducible (nullity > 1), the stationary distribution is
non-unique; this is reported (``unique = False``) and aggregates are NaN —
an explicit diagnostic rather than a silently chosen invariant measure.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt
from scipy import sparse

__all__ = ["TwoAssetKfeResult", "solve_two_asset_kfe"]

FloatArray = npt.NDArray[np.float64]


@dataclass(frozen=True)
class TwoAssetKfeResult:
    mass: FloatArray
    unique: bool
    nullity: int
    stationarity_residual: float
    mass_error: float
    minimum_mass: float
    negative_mass_count: int
    nan_inf_count: int
    state_marginals: FloatArray
    A_hh: float
    B_hh: float
    B_hh_pos: float
    B_hh_neg: float
    L_hh: float
    C_hh: float


def solve_two_asset_kfe(
    *,
    generator: sparse.csr_matrix,
    b_grid: FloatArray,
    a_grid: FloatArray,
    z_states: FloatArray,
    consumption: FloatArray,
    labor: FloatArray,
    mass_tolerance: float,
    negative_mass_threshold: float,
    nullity_threshold: float = 1e-7,
) -> TwoAssetKfeResult:
    """Stationary density from the null space of the transposed generator."""
    i_count = b_grid.size
    j_count = a_grid.size
    nz_count = z_states.size
    size = i_count * j_count * nz_count
    if generator.shape != (size, size):
        raise ValueError("generator dimensions do not match the household grid")

    db = float(b_grid[1] - b_grid[0])
    da = float(a_grid[1] - a_grid[0])
    measure = db * da

    _, singular_values, vh = np.linalg.svd(generator.T.toarray())
    nullity = int(np.sum(singular_values <= nullity_threshold))
    stationarity_residual = float(singular_values[0]) if size > 0 else float("nan")

    if nullity != 1:
        return TwoAssetKfeResult(
            mass=np.zeros_like(consumption),
            unique=False,
            nullity=nullity,
            stationarity_residual=stationarity_residual,
            mass_error=float("nan"),
            minimum_mass=float("nan"),
            negative_mass_count=-1,
            nan_inf_count=-1,
            state_marginals=np.full(nz_count, float("nan"), dtype=np.float64),
            A_hh=float("nan"),
            B_hh=float("nan"),
            B_hh_pos=float("nan"),
            B_hh_neg=float("nan"),
            L_hh=float("nan"),
            C_hh=float("nan"),
        )

    raw = vh[-1]
    if float(np.sum(raw)) < 0.0:
        raw = -raw
    if not np.all(np.isfinite(raw)) or abs(float(np.sum(raw))) < mass_tolerance:
        raise ValueError("KFE null space returned invalid mass")
    mass_flat = raw / float(np.sum(raw) * measure)
    mass = mass_flat.reshape((i_count, j_count, nz_count))
    mass_error = abs(float(np.sum(mass_flat) * measure) - 1.0)
    minimum_mass = float(np.min(mass_flat))
    negative_mass_count = int(np.count_nonzero(mass_flat < negative_mass_threshold))
    nan_inf_count = int(np.count_nonzero(~np.isfinite(mass_flat)))
    state_marginals = np.asarray(
        [float(np.sum(mass[:, :, nz]) * measure) for nz in range(nz_count)], dtype=np.float64
    )

    b_3d = np.broadcast_to(b_grid[:, None, None], mass.shape)
    a_3d = np.broadcast_to(a_grid[None, :, None], mass.shape)
    z_3d = np.broadcast_to(z_states[None, None, :], mass.shape)
    A_hh = float(np.sum(mass * a_3d) * measure)
    B_hh = float(np.sum(mass * b_3d) * measure)
    B_hh_pos = float(np.sum(mass * b_3d * (b_3d >= 0.0)) * measure)
    B_hh_neg = float(-np.sum(mass * b_3d * (b_3d < 0.0)) * measure)
    L_hh = float(np.sum(mass * z_3d * labor) * measure)
    C_hh = float(np.sum(mass * consumption) * measure)
    return TwoAssetKfeResult(
        mass=mass,
        unique=True,
        nullity=nullity,
        stationarity_residual=stationarity_residual,
        mass_error=mass_error,
        minimum_mass=minimum_mass,
        negative_mass_count=negative_mass_count,
        nan_inf_count=nan_inf_count,
        state_marginals=state_marginals,
        A_hh=A_hh,
        B_hh=B_hh,
        B_hh_pos=B_hh_pos,
        B_hh_neg=B_hh_neg,
        L_hh=L_hh,
        C_hh=C_hh,
    )
