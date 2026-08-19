"""CRRA preferences (pure functions).

Contract: ``u(c) = c^(1-gamma)/(1-gamma)`` (log at ``gamma == 1``),
marginal ``u'(c) = c^-gamma``, inverse marginal ``u'^{-1}(m) = m^(-1/gamma)``.
"""

from __future__ import annotations

import numpy as np
import numpy.typing as npt

__all__ = ["utility", "marginal_utility", "inverse_marginal_utility"]

FloatArray = npt.NDArray[np.float64]


def utility(consumption: FloatArray, *, gamma: float) -> FloatArray:
    if gamma <= 0.0 or np.any(consumption <= 0.0):
        raise ValueError("CRRA utility requires positive consumption and curvature")
    if gamma == 1.0:
        return np.log(consumption)
    return np.asarray(consumption ** (1.0 - gamma) / (1.0 - gamma), dtype=np.float64)


def marginal_utility(consumption: FloatArray, *, gamma: float) -> FloatArray:
    if gamma <= 0.0 or np.any(consumption <= 0.0):
        raise ValueError("marginal utility requires positive consumption and curvature")
    return np.asarray(consumption ** (-gamma), dtype=np.float64)


def inverse_marginal_utility(marginal: FloatArray, *, gamma: float) -> FloatArray:
    if gamma <= 0.0 or np.any(marginal <= 0.0):
        raise ValueError("inverse marginal utility requires positive arguments")
    return np.asarray(marginal ** (-1.0 / gamma), dtype=np.float64)
