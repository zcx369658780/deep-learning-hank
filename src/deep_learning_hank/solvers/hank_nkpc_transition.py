"""DLH-3D backward NKPC recursion and Taylor/Fisher nominal block (isolated
module).

Frozen DLH-3D aggregate closure (Issue #13 §6):

- ``Y_t = Z*N_t``, ``mc_t = w_t/Z``;
- accepted local-linear operational NKPC ``pi_dot = rho_hh*pi - kappa*(mc - 1/mu)``
  with ``kappa = epsilon/phi_p``, solved backward-Euler with terminal ``pi(T) = 0``:

  ``(pi_{k+1} - pi_k)/dt = rho_hh*pi_k - kappa*(mc_k - 1/mu)``

  ``pi_k = [pi_{k+1} + dt*kappa*(mc_k - 1/mu)] / [1 + dt*rho_hh]``

- Taylor (``pi_bar = 0``): ``i_t = r_bar + phi_pi*pi_t + epsilon_i(t)``;
- Fisher: ``r_t = i_t - pi_t``.

All residuals are recomputed independently and never labelled zero by
construction without recomputation.
"""

from __future__ import annotations

import numpy as np
import numpy.typing as npt

__all__ = [
    "backward_nkpc",
    "nkpc_residual",
    "taylor_fisher",
]

FloatArray = npt.NDArray[np.float64]


def backward_nkpc(
    marginal_cost_path: FloatArray,
    *,
    dt: float,
    rho_hh: float,
    kappa: float,
    mc_frictionless: float,
    pi_terminal: float = 0.0,
) -> FloatArray:
    """Backward-Euler NKPC recursion with terminal ``pi(T) = pi_terminal``.

    ``pi_dot = rho_hh*pi - kappa*(mc - mc_frictionless)`` with
    ``mc_frictionless = 1/mu``; returns the inflation path for ``k = 0..K``.
    """
    marginal_cost_path = np.asarray(marginal_cost_path, dtype=np.float64)
    n_points = marginal_cost_path.size
    if n_points < 2 or dt <= 0.0 or rho_hh <= 0.0 or kappa <= 0.0:
        raise ValueError("invalid NKPC inputs")
    pi_path = np.empty(n_points, dtype=np.float64)
    pi_path[-1] = float(pi_terminal)
    denominator = 1.0 + dt * rho_hh
    for k in range(n_points - 2, -1, -1):
        pi_path[k] = (
            pi_path[k + 1] + dt * kappa * (marginal_cost_path[k] - mc_frictionless)
        ) / denominator
    return pi_path


def nkpc_residual(
    pi_path: FloatArray,
    marginal_cost_path: FloatArray,
    *,
    dt: float,
    rho_hh: float,
    kappa: float,
    mc_frictionless: float,
) -> FloatArray:
    """Discrete NKPC residual over ``k = 0..K-1`` (recomputed, not labelled zero)."""
    pi_path = np.asarray(pi_path, dtype=np.float64)
    marginal_cost_path = np.asarray(marginal_cost_path, dtype=np.float64)
    if pi_path.size != marginal_cost_path.size:
        raise ValueError("paths must have equal length")
    numerator = np.diff(pi_path) / dt  # (pi_{k+1} - pi_k)/dt for k = 0..K-1
    return numerator - rho_hh * pi_path[:-1] + kappa * (marginal_cost_path[:-1] - mc_frictionless)


def taylor_fisher(
    *,
    real_rate_bar: float,
    phi_pi: float,
    pi_path: FloatArray,
    epsilon_i_path: FloatArray,
) -> tuple[FloatArray, FloatArray, FloatArray, FloatArray]:
    """Taylor rule + Fisher relation (``pi_bar = 0``).

    Returns ``(i_path, r_path, taylor_residual, fisher_residual)``.
    """
    pi_path = np.asarray(pi_path, dtype=np.float64)
    epsilon_i_path = np.asarray(epsilon_i_path, dtype=np.float64)
    if pi_path.size != epsilon_i_path.size:
        raise ValueError("paths must have equal length")
    i_path = real_rate_bar + phi_pi * pi_path + epsilon_i_path
    r_path = i_path - pi_path
    taylor_residual = i_path - (real_rate_bar + phi_pi * pi_path + epsilon_i_path)
    fisher_residual = r_path - (i_path - pi_path)
    return i_path, r_path, taylor_residual, fisher_residual
