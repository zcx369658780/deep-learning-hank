"""Immutable configuration for the DLH-2A fixed-price validation fixture.

This module intentionally provides *bounds/schema* validation only.  It does
NOT freeze a hard-coded calibration: every fixture field is a documented
numerical-regression value (``VALIDATION_FIXTURE_NOT_CALIBRATION``), and
deviations within declared domains are admissible.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path
import tomllib
from typing import Any

__all__ = [
    "FixedPriceConfig",
    "NumericalControls",
    "SteadyStateConfig",
    "SteadyStateNumericalControls",
]


@dataclass(frozen=True)
class NumericalControls:
    hjb_tolerance: float
    hjb_max_iterations: int
    hjb_pseudo_time_step: float
    consumption_floor: float
    kfe_stationarity_tolerance: float
    kfe_mass_tolerance: float
    negative_mass_threshold: float
    generator_row_sum_tolerance: float
    generator_min_off_diagonal_tolerance: float
    reproducibility_tolerance: float


@dataclass(frozen=True)
class FixedPriceConfig:
    """DLH-2A fixed-price household + KFE validation fixture (NOT calibration)."""

    path: Path
    frequency: str
    asset_grid_count: int
    a_min: float
    a_max: float
    idiosyncratic_states: tuple[float, float]
    q_low_to_high: float
    q_high_to_low: float
    rho_hh: float
    gamma: float
    wage: float
    portfolio_return: float
    transfer: float
    tau_l: float
    numerical: NumericalControls

    @classmethod
    def from_toml(cls, path: Path) -> "FixedPriceConfig":
        resolved = path.resolve()
        with resolved.open("rb") as handle:
            data: dict[str, Any] = tomllib.load(handle)
        fixture = data["fixture"]
        numerical = data["numerical"]
        config = cls(
            path=resolved,
            frequency=str(fixture["frequency"]),
            asset_grid_count=int(fixture["asset_grid_count"]),
            a_min=float(fixture["a_min"]),
            a_max=float(fixture["a_max"]),
            idiosyncratic_states=tuple(float(x) for x in fixture["idiosyncratic_states"]),
            q_low_to_high=float(fixture["q_low_to_high"]),
            q_high_to_low=float(fixture["q_high_to_low"]),
            rho_hh=float(fixture["rho_hh"]),
            gamma=float(fixture["gamma"]),
            wage=float(fixture["wage"]),
            portfolio_return=float(fixture["portfolio_return"]),
            transfer=float(fixture["transfer"]),
            tau_l=float(fixture["tau_l"]),
            numerical=NumericalControls(
                hjb_tolerance=float(numerical["hjb_tolerance"]),
                hjb_max_iterations=int(numerical["hjb_max_iterations"]),
                hjb_pseudo_time_step=float(numerical["hjb_pseudo_time_step"]),
                consumption_floor=float(numerical["consumption_floor"]),
                kfe_stationarity_tolerance=float(numerical["kfe_stationarity_tolerance"]),
                kfe_mass_tolerance=float(numerical["kfe_mass_tolerance"]),
                negative_mass_threshold=float(numerical["negative_mass_threshold"]),
                generator_row_sum_tolerance=float(numerical["generator_row_sum_tolerance"]),
                generator_min_off_diagonal_tolerance=float(
                    numerical["generator_min_off_diagonal_tolerance"]
                ),
                reproducibility_tolerance=float(numerical["reproducibility_tolerance"]),
            ),
        )
        config.validate()
        return config

    def validate(self) -> None:
        if self.asset_grid_count < 3 or not self.a_min < self.a_max:
            raise ValueError("asset grid must be increasing with at least three points")
        if len(self.idiosyncratic_states) != 2:
            raise ValueError("fixture uses two idiosyncratic productivity states")
        if self.q_low_to_high <= 0.0 or self.q_high_to_low <= 0.0:
            raise ValueError("transition intensities must be strictly positive")
        if self.rho_hh <= 0.0:
            raise ValueError("household discount rate must be positive")
        if self.gamma <= 0.0:
            raise ValueError("CRRA curvature must be positive")
        if self.tau_l < 0.0 or self.tau_l >= 1.0:
            raise ValueError("labor tax rate must lie in [0, 1)")
        n = self.numerical
        if n.hjb_tolerance <= 0.0 or n.kfe_stationarity_tolerance <= 0.0:
            raise ValueError("tolerances must be positive")
        if n.hjb_max_iterations <= 0 or n.hjb_pseudo_time_step <= 0.0:
            raise ValueError("HJB iteration controls must be positive")
        if n.consumption_floor < 0.0:
            raise ValueError("consumption floor must be nonnegative")
        if n.negative_mass_threshold > 0.0:
            raise ValueError("negative-mass threshold must be nonpositive")

    def sha256(self) -> str:
        return hashlib.sha256(self.path.read_bytes()).hexdigest().upper()


@dataclass(frozen=True)
class SteadyStateNumericalControls:
    hjb_tolerance: float
    hjb_max_iterations: int
    hjb_pseudo_time_step: float
    consumption_floor: float
    kfe_stationarity_tolerance: float
    kfe_mass_tolerance: float
    negative_mass_threshold: float
    generator_row_sum_tolerance: float
    generator_min_off_diagonal_tolerance: float
    outer_capital_tolerance: float
    outer_max_iterations: int
    reproducibility_tolerance: float


@dataclass(frozen=True)
class SteadyStateConfig:
    """Single-region Tier-0 HA/Aiyagari steady-state validation fixture.

    ``VALIDATION_FIXTURE_NOT_CALIBRATION``: numerical regression values only;
    never empirical calibration.  Household/distribution fields inherit the
    accepted DLH-2A fixture; firm/root fields are Tier-0 additions.
    """

    path: Path
    frequency: str
    asset_grid_count: int
    a_min: float
    a_max: float
    idiosyncratic_states: tuple[float, float]
    q_low_to_high: float
    q_high_to_low: float
    rho_hh: float
    gamma: float
    tau_l: float
    productivity: float
    alpha_k: float
    delta: float
    public_outlay: float
    capital_bracket: tuple[float, float]
    scan_bounds: tuple[float, float]
    scan_points: int
    numerical: SteadyStateNumericalControls

    @classmethod
    def from_toml(cls, path: Path) -> "SteadyStateConfig":
        resolved = path.resolve()
        with resolved.open("rb") as handle:
            data: dict[str, Any] = tomllib.load(handle)
        fixture = data["fixture"]
        root = data["root"]
        numerical = data["numerical"]
        config = cls(
            path=resolved,
            frequency=str(fixture["frequency"]),
            asset_grid_count=int(fixture["asset_grid_count"]),
            a_min=float(fixture["a_min"]),
            a_max=float(fixture["a_max"]),
            idiosyncratic_states=tuple(float(x) for x in fixture["idiosyncratic_states"]),
            q_low_to_high=float(fixture["q_low_to_high"]),
            q_high_to_low=float(fixture["q_high_to_low"]),
            rho_hh=float(fixture["rho_hh"]),
            gamma=float(fixture["gamma"]),
            tau_l=float(fixture["tau_l"]),
            productivity=float(root["A"]),
            alpha_k=float(root["alpha_k"]),
            delta=float(root["delta"]),
            public_outlay=float(root["G"]),
            capital_bracket=tuple(float(x) for x in root["capital_bracket"]),
            scan_bounds=tuple(float(x) for x in root["scan_bounds"]),
            scan_points=int(root["scan_points"]),
            numerical=SteadyStateNumericalControls(
                hjb_tolerance=float(numerical["hjb_tolerance"]),
                hjb_max_iterations=int(numerical["hjb_max_iterations"]),
                hjb_pseudo_time_step=float(numerical["hjb_pseudo_time_step"]),
                consumption_floor=float(numerical["consumption_floor"]),
                kfe_stationarity_tolerance=float(numerical["kfe_stationarity_tolerance"]),
                kfe_mass_tolerance=float(numerical["kfe_mass_tolerance"]),
                negative_mass_threshold=float(numerical["negative_mass_threshold"]),
                generator_row_sum_tolerance=float(numerical["generator_row_sum_tolerance"]),
                generator_min_off_diagonal_tolerance=float(
                    numerical["generator_min_off_diagonal_tolerance"]
                ),
                outer_capital_tolerance=float(numerical["outer_capital_tolerance"]),
                outer_max_iterations=int(numerical["outer_max_iterations"]),
                reproducibility_tolerance=float(numerical["reproducibility_tolerance"]),
            ),
        )
        config.validate()
        return config

    def validate(self) -> None:
        if self.asset_grid_count < 3 or not self.a_min < self.a_max:
            raise ValueError("asset grid must be increasing with at least three points")
        if len(self.idiosyncratic_states) != 2:
            raise ValueError("fixture uses two idiosyncratic productivity states")
        if self.q_low_to_high <= 0.0 or self.q_high_to_low <= 0.0:
            raise ValueError("transition intensities must be strictly positive")
        if self.rho_hh <= 0.0 or self.gamma <= 0.0:
            raise ValueError("discount rate and CRRA curvature must be positive")
        if not 0.0 < self.alpha_k < 1.0:
            raise ValueError("capital share must lie in (0, 1)")
        if self.delta < 0.0 or self.productivity <= 0.0 or self.public_outlay < 0.0:
            raise ValueError("invalid firm/fiscal fixture")
        if self.tau_l < 0.0 or self.tau_l >= 1.0:
            raise ValueError("labor tax rate must lie in [0, 1)")
        lo, hi = self.capital_bracket
        if not 0.0 < lo < hi:
            raise ValueError("capital bracket must be strictly positive and increasing")
        slo, shi = self.scan_bounds
        if not 0.0 < slo < shi:
            raise ValueError("scan bounds must be strictly positive and increasing")
        if self.scan_points < 3:
            raise ValueError("scan requires at least three points")
        n = self.numerical
        if n.hjb_tolerance <= 0.0 or n.kfe_stationarity_tolerance <= 0.0:
            raise ValueError("tolerances must be positive")
        if n.hjb_max_iterations <= 0 or n.hjb_pseudo_time_step <= 0.0:
            raise ValueError("HJB iteration controls must be positive")
        if n.outer_capital_tolerance <= 0.0 or n.outer_max_iterations <= 0:
            raise ValueError("outer root controls must be positive")
        if n.consumption_floor < 0.0 or n.negative_mass_threshold > 0.0:
            raise ValueError("consumption floor / negative-mass threshold invalid")

    def sha256(self) -> str:
        return hashlib.sha256(self.path.read_bytes()).hexdigest().upper()
