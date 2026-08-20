"""Immutable configuration for the DLH-3D full minimal single-region NK GE
closure validation fixture.

Every field is a documented numerical-regression value under the explicit
labels

- ``VALIDATION_FIXTURE_NOT_CALIBRATION``;
- ``D2_MACHINE_DIAGNOSTIC__MINIMAL_SINGLE_REGION_HANK_DYNAMIC_VALIDATION_FIXTURE``.

The accepted DLH-3B and DLH-3C baseline config identities (SHA-256) are
verified at load; any mismatch raises ``BaselineIdentityMismatchError``
(Issue #13 §4).
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path
import tomllib
from typing import Any

__all__ = [
    "BaselineIdentityMismatchError",
    "HankGeGateControls",
    "HankGeNumericalControls",
    "HankGeConfig",
]


class BaselineIdentityMismatchError(RuntimeError):
    """Raised when an accepted predecessor baseline config hash is not as frozen."""


@dataclass(frozen=True)
class HankGeNumericalControls:
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
class HankGeGateControls:
    clearing_asset_tolerance: float
    clearing_labor_tolerance: float
    nkpc_tolerance: float
    fisher_tolerance: float
    taylor_tolerance: float
    goods_tolerance: float
    wealth_flow_tolerance: float
    fiscal_tolerance: float
    profits_tolerance: float
    zero_w_tolerance: float
    zero_N_tolerance: float
    zero_pi_tolerance: float
    zero_r_tolerance: float
    zero_A_hh_tolerance: float
    zero_N_hh_tolerance: float
    zero_C_tolerance: float
    nontrivial_response_threshold: float
    quarter_amplitude_ratio_cap: float
    half_linearity_metric_cap: float
    horizon_window_T: float
    horizon_tolerance: float
    reproducibility_tolerance: float


@dataclass(frozen=True)
class HankGeConfig:
    """DLH-3D full NK GE closure validation fixture (NOT calibration)."""

    path: Path
    baseline_3b_path: Path
    baseline_3b_sha256: str
    baseline_3c_path: Path
    baseline_3c_sha256: str
    T: float
    dt: float
    T_long: float
    L_i: float
    eta_i: float
    amplitude_multipliers: tuple[float, ...]
    root_method: str
    root_tolerance_inf_norm: float
    root_max_nonlinear_iterations: int
    numerical: HankGeNumericalControls
    gates: HankGeGateControls

    @classmethod
    def from_toml(cls, path: Path) -> "HankGeConfig":
        resolved = path.resolve()
        with resolved.open("rb") as handle:
            data: dict[str, Any] = tomllib.load(handle)
        baseline = data["baseline"]
        time_ = data["time"]
        innovation = data["innovation"]
        root = data["root"]
        numerical = data["numerical"]
        gates = data["gates"]
        config = cls(
            path=resolved,
            baseline_3b_path=Path(baseline["dlh_3b_config"]).resolve(),
            baseline_3b_sha256=str(baseline["dlh_3b_config_sha256"]).upper(),
            baseline_3c_path=Path(baseline["dlh_3c_config"]).resolve(),
            baseline_3c_sha256=str(baseline["dlh_3c_config_sha256"]).upper(),
            T=float(time_["T"]),
            dt=float(time_["dt"]),
            T_long=float(time_["T_long"]),
            L_i=float(innovation["L_i"]),
            eta_i=float(innovation["eta_i"]),
            amplitude_multipliers=tuple(float(x) for x in innovation["amplitude_multipliers"]),
            root_method=str(root["method"]),
            root_tolerance_inf_norm=float(root["root_tolerance_inf_norm"]),
            root_max_nonlinear_iterations=int(root["max_nonlinear_iterations"]),
            numerical=HankGeNumericalControls(
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
            gates=HankGeGateControls(
                clearing_asset_tolerance=float(gates["clearing_asset_tolerance"]),
                clearing_labor_tolerance=float(gates["clearing_labor_tolerance"]),
                nkpc_tolerance=float(gates["nkpc_tolerance"]),
                fisher_tolerance=float(gates["fisher_tolerance"]),
                taylor_tolerance=float(gates["taylor_tolerance"]),
                goods_tolerance=float(gates["goods_tolerance"]),
                wealth_flow_tolerance=float(gates["wealth_flow_tolerance"]),
                fiscal_tolerance=float(gates["fiscal_tolerance"]),
                profits_tolerance=float(gates["profits_tolerance"]),
                zero_w_tolerance=float(gates["zero_w_tolerance"]),
                zero_N_tolerance=float(gates["zero_N_tolerance"]),
                zero_pi_tolerance=float(gates["zero_pi_tolerance"]),
                zero_r_tolerance=float(gates["zero_r_tolerance"]),
                zero_A_hh_tolerance=float(gates["zero_A_hh_tolerance"]),
                zero_N_hh_tolerance=float(gates["zero_N_hh_tolerance"]),
                zero_C_tolerance=float(gates["zero_C_tolerance"]),
                nontrivial_response_threshold=float(gates["nontrivial_response_threshold"]),
                quarter_amplitude_ratio_cap=float(gates["quarter_amplitude_ratio_cap"]),
                half_linearity_metric_cap=float(gates["half_linearity_metric_cap"]),
                horizon_window_T=float(gates["horizon_window_T"]),
                horizon_tolerance=float(gates["horizon_tolerance"]),
                reproducibility_tolerance=float(gates["reproducibility_tolerance"]),
            ),
        )
        config.validate()
        return config

    def validate(self) -> None:
        if not self.baseline_3b_path.is_file() or not self.baseline_3c_path.is_file():
            raise ValueError("accepted predecessor baseline configs must exist")
        if not (0.0 < self.dt <= self.T < self.T_long):
            raise ValueError("time grid must satisfy 0 < dt <= T < T_long")
        if self.L_i <= 0.0 or self.L_i > self.T:
            raise ValueError("innovation length must lie in (0, T]")
        if self.eta_i <= 0.0:
            raise ValueError("innovation amplitude must be strictly positive")
        if not all(m >= 0.0 for m in self.amplitude_multipliers):
            raise ValueError("amplitude multipliers must be nonnegative")
        if 1.0 not in self.amplitude_multipliers:
            raise ValueError("full amplitude 1.0 must be in the amplitude sequence")
        if self.root_method != "krylov":
            raise ValueError("frozen root method must be 'krylov' (Issue #13 §7)")
        if self.root_tolerance_inf_norm <= 0.0 or self.root_max_nonlinear_iterations <= 0:
            raise ValueError("root tolerance/iterations must be positive")
        n = self.numerical
        if n.policy_iteration_value_tolerance <= 0.0 or n.policy_iteration_max_iterations <= 0:
            raise ValueError("policy-iteration controls must be positive")
        if n.hjb_residual_tolerance <= 0.0 or n.kkt_tolerance <= 0.0:
            raise ValueError("HJB/KKT tolerances must be positive")
        if n.consumption_floor < 0.0 or n.minimum_mass_threshold > 0.0:
            raise ValueError("consumption floor / minimum-mass threshold invalid")
        g = self.gates
        if g.reproducibility_tolerance <= 0.0 or g.horizon_tolerance <= 0.0:
            raise ValueError("gate tolerances must be positive")

    def verify_baseline_identities(self) -> tuple[str, str]:
        """Verify the accepted DLH-3B and DLH-3C baseline config SHA-256s."""
        observed_3b = hashlib.sha256(self.baseline_3b_path.read_bytes()).hexdigest().upper()
        observed_3c = hashlib.sha256(self.baseline_3c_path.read_bytes()).hexdigest().upper()
        if observed_3b != self.baseline_3b_sha256 or observed_3c != self.baseline_3c_sha256:
            raise BaselineIdentityMismatchError(
                "BLOCKED_DLH_3D_BASELINE_IDENTITY_MISMATCH: "
                f"DLH-3B {observed_3b} (frozen {self.baseline_3b_sha256}); "
                f"DLH-3C {observed_3c} (frozen {self.baseline_3c_sha256})"
            )
        return observed_3b, observed_3c

    def sha256(self) -> str:
        return hashlib.sha256(self.path.read_bytes()).hexdigest().upper()
