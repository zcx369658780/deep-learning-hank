"""DLH-3C forward KFE transition solver (isolated module).

Implements Issue #12 §7: the frozen implicit forward step

    [I - dt * G_k^T] g_{k+1} = g_k

from the accepted DLH-3B stationary distribution ``g(0) = g_ss``, using the
time-dependent policy generator path from the backward HJB solve.

Distribution mass is **not** renormalized after each step; mass conservation
must emerge from the generator/discretization (generator rows sum to zero, so
``1^T G^T = 0`` and the step is exactly mass-conserving in exact arithmetic).

No dynamic asset/labor/goods market clearing is imposed in DLH-3C because the
aggregate paths are prescribed and full aggregate GE is intentionally open.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt
from scipy import sparse
from scipy.sparse.linalg import spsolve

__all__ = ["DynamicDistributionResult", "forward_kfe_transition"]


@dataclass(frozen=True)
class DynamicDistributionResult:
    time_grid: FloatArray
    mass_path: npt.NDArray[np.float64]
    mass_error_path: FloatArray
    minimum_mass_path: FloatArray
    negative_mass_count_path: npt.NDArray[np.int64]
    nan_inf_count_path: npt.NDArray[np.int64]
    state_marginals_path: npt.NDArray[np.float64]
    A_hh_path: FloatArray
    N_hh_path: FloatArray
    C_path: FloatArray
    mass_error_max: float
    minimum_mass_min: float
    negative_mass_count_max: int
    nan_inf_count_max: int


def forward_kfe_transition(
    *,
    initial_mass: FloatArray,
    generator_path: tuple[sparse.csr_matrix, ...],
    asset_grid: FloatArray,
    efficiency_states: FloatArray,
    labor_path: FloatArray,
    consumption_path: FloatArray,
    dt: float,
) -> DynamicDistributionResult:
    """Forward implicit KFE along the policy generator path.

    ``generator_path`` has ``N+1`` generators for ``k = 0..N``; step ``k ->
    k+1`` uses ``G_k`` for ``k = 0..N-1``.  ``labor_path`` / ``consumption_path``
    are the ``(N+1, states, assets)`` policy paths used to form aggregates.
    """
    n_points = len(generator_path)
    if n_points < 2:
        raise ValueError("generator path must cover at least two time points")
    if labor_path.shape[0] != n_points or consumption_path.shape[0] != n_points:
        raise ValueError("policy paths must match the generator path length")
    time_grid = dt * np.arange(n_points, dtype=np.float64)
    mass = np.asarray(initial_mass, dtype=np.float64).reshape(labor_path.shape[1:])
    mass_error_list: list[float] = []
    minimum_mass_list: list[float] = []
    negative_mass_count_list: list[int] = []
    nan_inf_count_list: list[int] = []
    state_marginals_list: list[npt.NDArray[np.float64]] = []
    A_hh_list: list[float] = []
    N_hh_list: list[float] = []
    C_list: list[float] = []
    mass_path_list: list[npt.NDArray[np.float64]] = [mass.copy()]

    def _record(m: FloatArray, k: int) -> None:
        mass_error_list.append(abs(float(np.sum(m)) - 1.0))
        minimum_mass_list.append(float(np.min(m)))
        negative_mass_count_list.append(int(np.count_nonzero(m < -1e-12)))
        nan_inf_count_list.append(int(np.count_nonzero(~np.isfinite(m))))
        state_marginals_list.append(np.asarray(m.sum(axis=1), dtype=np.float64))
        A_hh_list.append(float(np.sum(m * asset_grid[None, :])))
        N_hh_list.append(float(np.sum(m * efficiency_states[:, None] * labor_path[k])))
        C_list.append(float(np.sum(m * consumption_path[k])))

    _record(mass, 0)
    identity = sparse.eye(mass.size, format="csr", dtype=np.float64)
    for k in range(n_points - 1):
        generator_t = generator_path[k].T.tocsr()
        matrix = identity - dt * generator_t
        mass_next = np.asarray(spsolve(matrix, mass.ravel()), dtype=np.float64).reshape(mass.shape)
        mass = mass_next
        mass_path_list.append(mass.copy())
        _record(mass, k + 1)
    return DynamicDistributionResult(
        time_grid=time_grid,
        mass_path=np.stack(mass_path_list),
        mass_error_path=np.asarray(mass_error_list, dtype=np.float64),
        minimum_mass_path=np.asarray(minimum_mass_list, dtype=np.float64),
        negative_mass_count_path=np.asarray(negative_mass_count_list, dtype=np.int64),
        nan_inf_count_path=np.asarray(nan_inf_count_list, dtype=np.int64),
        state_marginals_path=np.stack(state_marginals_list),
        A_hh_path=np.asarray(A_hh_list, dtype=np.float64),
        N_hh_path=np.asarray(N_hh_list, dtype=np.float64),
        C_path=np.asarray(C_list, dtype=np.float64),
        mass_error_max=float(max(mass_error_list)),
        minimum_mass_min=float(min(minimum_mass_list)),
        negative_mass_count_max=int(max(negative_mass_count_list)),
        nan_inf_count_max=int(max(nan_inf_count_list)),
    )
