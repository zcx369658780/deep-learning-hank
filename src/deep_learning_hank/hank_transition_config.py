"""Immutable configuration for the DLH-3C time-dependent household HJB/KFE
transition-validation fixture.

Mirrors the accepted DLH-3B configuration conventions.  Every field is a
documented numerical-regression value under the explicit labels

- ``VALIDATION_FIXTURE_NOT_CALIBRATION``;
- ``EXOGENOUS_NUMERICAL_RESPONSE_PATH_NOT_STRUCTURAL_SHOCK``;
- ``D2_MACHINE_DIAGNOSTIC__HANK_TIME_DEPENDENT_HOUSEHOLD_KFE_ONLY``.

The accepted DLH-3B baseline config identity (SHA-256) is verified at load;
any mismatch raises ``BaselineIdentityMismatchError`` (Issue #12 §4).
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path
import tomllib
from typing import Any

__all__ = [
    "BaselineIdentityMismatchError",
    "HankTransitionNumericalControls",
    "HankTransitionGateControls",
    "HankTransitionConfig",
]


class BaselineIdentityMismatchError(RuntimeError):
    """Raised when the accepted DLH-3B baseline config hash is not as frozen."""


@dataclass(frozen=True)
class HankTransitionNumericalControls:
    policy_iteration_value_tolerance: float
    policy_iteration_max_iterations: int
    consumption_floor: float
    hjb_residual_tolerance: float
    kkt_tolerance: float
    consumption_foc_tolerance: float
    kfe_mass_tolerance: float
    minimum_mass_threshold: float
    negative_mass_threshold: float
    generator_row_sum_tolerance: float
    generator_min_off_diagonal_tolerance: float


@dataclass(frozen=True)
class HankTransitionGateControls:
    zero_path_V_tolerance: float
    zero_path_policy_tolerance: float
    zero_path_mass_tolerance: float
    zero_path_aggregate_tolerance: float
    nontrivial_response_threshold: float
    quarter_amplitude_ratio_cap: float
    half_linearity_metric_cap: float
    horizon_window_T: float
    horizon_aggregate_tolerance: float
    reproducibility_tolerance: float


@dataclass(frozen=True)
class HankTransitionConfig:
    """DLH-3C transition-validation fixture (NOT calibration)."""

    path: Path
    baseline_config_path: Path
    baseline_config_sha256: str
    T: float
    dt: float
    T_long: float
    bump_length_L: float
    eta_w: float
    eta_r: float
    amplitude_multipliers: tuple[float, ...]
    numerical: HankTransitionNumericalControls
    gates: HankTransitionGateControls

    @classmethod
    def from_toml(cls, path: Path) -> "HankTransitionConfig":
        resolved = path.resolve()
        with resolved.open("rb") as handle:
            data: dict[str, Any] = tomllib.load(handle)
        baseline = data["baseline"]
        time_ = data["time"]
        paths = data["paths"]
        numerical = data["numerical"]
        gates = data["gates"]
        config = cls(
            path=resolved,
            baseline_config_path=Path(baseline["dlh_3b_config"]).resolve(),
            baseline_config_sha256=str(baseline["dlh_3b_config_sha256"]).upper(),
            T=float(time_["T"]),
            dt=float(time_["dt"]),
            T_long=float(time_["T_long"]),
            bump_length_L=float(time_["bump_length_L"]),
            eta_w=float(paths["eta_w"]),
            eta_r=float(paths["eta_r"]),
            amplitude_multipliers=tuple(float(x) for x in paths["amplitude_multipliers"]),
            numerical=HankTransitionNumericalControls(
                policy_iteration_value_tolerance=float(
                    numerical["policy_iteration_value_tolerance"]
                ),
                policy_iteration_max_iterations=int(numerical["policy_iteration_max_iterations"]),
                consumption_floor=float(numerical["consumption_floor"]),
                hjb_residual_tolerance=float(numerical["hjb_residual_tolerance"]),
                kkt_tolerance=float(numerical["kkt_tolerance"]),
                consumption_foc_tolerance=float(numerical["consumption_foc_tolerance"]),
                kfe_mass_tolerance=float(numerical["kfe_mass_tolerance"]),
                minimum_mass_threshold=float(numerical["minimum_mass_threshold"]),
                negative_mass_threshold=float(numerical["negative_mass_threshold"]),
                generator_row_sum_tolerance=float(numerical["generator_row_sum_tolerance"]),
                generator_min_off_diagonal_tolerance=float(
                    numerical["generator_min_off_diagonal_tolerance"]
                ),
            ),
            gates=HankTransitionGateControls(
                zero_path_V_tolerance=float(gates["zero_path_V_tolerance"]),
                zero_path_policy_tolerance=float(gates["zero_path_policy_tolerance"]),
                zero_path_mass_tolerance=float(gates["zero_path_mass_tolerance"]),
                zero_path_aggregate_tolerance=float(gates["zero_path_aggregate_tolerance"]),
                nontrivial_response_threshold=float(gates["nontrivial_response_threshold"]),
                quarter_amplitude_ratio_cap=float(gates["quarter_amplitude_ratio_cap"]),
                half_linearity_metric_cap=float(gates["half_linearity_metric_cap"]),
                horizon_window_T=float(gates["horizon_window_T"]),
                horizon_aggregate_tolerance=float(gates["horizon_aggregate_tolerance"]),
                reproducibility_tolerance=float(gates["reproducibility_tolerance"]),
            ),
        )
        config.validate()
        return config

    def validate(self) -> None:
        if not self.baseline_config_path.is_file():
            raise ValueError(f"baseline DLH-3B config not found: {self.baseline_config_path}")
        if not (0.0 < self.dt <= self.T < self.T_long):
            raise ValueError("time grid must satisfy 0 < dt <= T < T_long")
        if self.bump_length_L <= 0.0 or self.bump_length_L > self.T:
            raise ValueError("bump length must lie in (0, T]")
        if self.eta_w <= 0.0 or self.eta_r <= 0.0:
            raise ValueError("path amplitudes must be strictly positive")
        if not all(m >= 0.0 for m in self.amplitude_multipliers):
            raise ValueError("amplitude multipliers must be nonnegative")
        if 1.0 not in self.amplitude_multipliers:
            raise ValueError("full amplitude 1.0 must be in the amplitude sequence")
        n = self.numerical
        if n.policy_iteration_value_tolerance <= 0.0 or n.policy_iteration_max_iterations <= 0:
            raise ValueError("policy-iteration controls must be positive")
        if n.hjb_residual_tolerance <= 0.0 or n.kkt_tolerance <= 0.0:
            raise ValueError("HJB/KKT tolerances must be positive")
        if n.consumption_floor < 0.0 or n.minimum_mass_threshold > 0.0:
            raise ValueError("consumption floor / minimum-mass threshold invalid")
        g = self.gates
        if g.reproducibility_tolerance <= 0.0 or g.horizon_aggregate_tolerance <= 0.0:
            raise ValueError("gate tolerances must be positive")

    def verify_baseline_identity(self) -> str:
        """Verify the accepted DLH-3B baseline config SHA-256 (Issue #12 §4)."""
        observed = hashlib.sha256(self.baseline_config_path.read_bytes()).hexdigest().upper()
        if observed != self.baseline_config_sha256:
            raise BaselineIdentityMismatchError(
                "BLOCKED_DLH_3C_BASELINE_IDENTITY_MISMATCH: "
                f"DLH-3B baseline config SHA-256 {observed} != frozen {self.baseline_config_sha256}"
            )
        return observed

    def sha256(self) -> str:
        return hashlib.sha256(self.path.read_bytes()).hexdigest().upper()
