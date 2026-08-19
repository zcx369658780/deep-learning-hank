"""Grids and the idiosyncratic CTMC generator / intensity matrix.

The idiosyncratic-state object is a **continuous-time infinitesimal generator
/ intensity matrix**:
  * off-diagonal rates >= 0;
  * diagonal = negative total outflow;
  * row sums = 0.
It is NOT a row-stochastic transition matrix.
"""

from __future__ import annotations

import numpy as np
import numpy.typing as npt

__all__ = ["build_asset_grid", "build_idiosyncratic_generator", "stationary_state_probabilities"]

FloatArray = npt.NDArray[np.float64]


def build_asset_grid(a_min: float, a_max: float, count: int) -> FloatArray:
    if count < 3 or not a_min < a_max:
        raise ValueError("asset grid requires at least three increasing points")
    return np.linspace(a_min, a_max, count, dtype=np.float64)


def build_idiosyncratic_generator(low_to_high: float, high_to_low: float) -> FloatArray:
    """Two-state CTMC generator: rows sum to 0, off-diagonals >= 0."""
    if low_to_high <= 0.0 or high_to_low <= 0.0:
        raise ValueError("transition intensities must be strictly positive")
    return np.array(
        [[-low_to_high, low_to_high], [high_to_low, -high_to_low]],
        dtype=np.float64,
    )


def stationary_state_probabilities(generator: FloatArray) -> FloatArray:
    """Stationary distribution of a two-state CTMC generator (rows sum 0)."""
    if generator.shape != (2, 2) or not np.allclose(generator.sum(axis=1), 0.0, atol=1e-14):
        raise ValueError("expected a two-state continuous-time generator")
    matrix = generator.T.copy()
    matrix[-1, :] = 1.0
    rhs = np.array([0.0, 1.0], dtype=np.float64)
    probabilities = np.linalg.solve(matrix, rhs)
    if np.any(probabilities < 0.0):
        raise ValueError("stationary probabilities must be nonnegative")
    return np.asarray(probabilities, dtype=np.float64)
