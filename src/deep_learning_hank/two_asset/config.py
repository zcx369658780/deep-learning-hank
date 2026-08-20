"""Immutable configuration for the DLH-4A two-asset household kernel fixture.

All values are ``VALIDATION_FIXTURE_NOT_CALIBRATION`` (Issue #17). Grid
dimensions and preference/adjustment parameters mirror the legacy Matlab
reference (read-only); household-block inputs ``(w, rb, ra, Tt, tau)`` are
validation-fixture choices within the reference parameter ranges.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path
import tomllib
from typing import Any

__all__ = ["TwoAssetConfig"]


@dataclass(frozen=True)
class TwoAssetConfig:
    path: Path
    b_min: float
    b_max: float
    b_points: int
    a_min: float
    a_max: float
    a_points: int
    idiosyncratic_states: tuple[float, float]
    q_low_to_high: float
    q_high_to_low: float
    rho: float
    gamma: float
    alphac: float
    alphal: float
    frisch_l: float
    n_max: float
    tau_l: float
    w: float
    rb: float
    rb_gap: float
    ra: float
    Tt: float
    consumption_floor: float
    chi0: float
    chi1: float
    a_bar: float
    fixcost: float
    fixcost2: float
    pseudo_time_step: float
    value_change_tolerance: float
    max_value_iterations: int
    generator_row_sum_tolerance: float
    generator_min_off_diagonal_tolerance: float
    kfe_stationarity_tolerance: float
    kfe_mass_tolerance: float
    negative_mass_threshold: float
    reproducibility_tolerance: float

    @classmethod
    def from_toml(cls, path: Path) -> "TwoAssetConfig":
        resolved = path.resolve()
        with resolved.open("rb") as handle:
            data: dict[str, Any] = tomllib.load(handle)
        fixture = data["fixture"]
        household = data["household"]
        adjustment = data["adjustment"]
        numerical = data["numerical"]
        config = cls(
            path=resolved,
            b_min=float(fixture["b_min"]),
            b_max=float(fixture["b_max"]),
            b_points=int(fixture["b_points"]),
            a_min=float(fixture["a_min"]),
            a_max=float(fixture["a_max"]),
            a_points=int(fixture["a_points"]),
            idiosyncratic_states=tuple(float(x) for x in fixture["idiosyncratic_states"]),
            q_low_to_high=float(fixture["q_low_to_high"]),
            q_high_to_low=float(fixture["q_high_to_low"]),
            rho=float(household["rho"]),
            gamma=float(household["gamma"]),
            alphac=float(household["alphac"]),
            alphal=float(household["alphal"]),
            frisch_l=float(household["frisch_l"]),
            n_max=float(household["n_max"]),
            tau_l=float(household["tau_l"]),
            w=float(household["w"]),
            rb=float(household["rb"]),
            rb_gap=float(household["rb_gap"]),
            ra=float(household["ra"]),
            Tt=float(household["Tt"]),
            consumption_floor=float(household["consumption_floor"]),
            chi0=float(adjustment["chi0"]),
            chi1=float(adjustment["chi1"]),
            a_bar=float(adjustment["a_bar"]),
            fixcost=float(adjustment["fixcost"]),
            fixcost2=float(adjustment["fixcost2"]),
            pseudo_time_step=float(numerical["pseudo_time_step"]),
            value_change_tolerance=float(numerical["value_change_tolerance"]),
            max_value_iterations=int(numerical["max_value_iterations"]),
            generator_row_sum_tolerance=float(numerical["generator_row_sum_tolerance"]),
            generator_min_off_diagonal_tolerance=float(
                numerical["generator_min_off_diagonal_tolerance"]
            ),
            kfe_stationarity_tolerance=float(numerical["kfe_stationarity_tolerance"]),
            kfe_mass_tolerance=float(numerical["kfe_mass_tolerance"]),
            negative_mass_threshold=float(numerical["negative_mass_threshold"]),
            reproducibility_tolerance=float(numerical["reproducibility_tolerance"]),
        )
        config.validate()
        return config

    def validate(self) -> None:
        if not (self.b_min < self.b_max and self.a_min < self.a_max):
            raise ValueError("asset grids must be increasing")
        if self.b_points < 3 or self.a_points < 3:
            raise ValueError("grids require at least three points")
        if len(self.idiosyncratic_states) != 2:
            raise ValueError("two-state CTMC required")
        if self.q_low_to_high <= 0.0 or self.q_high_to_low <= 0.0:
            raise ValueError("CTMC intensities must be positive")
        if self.rho <= 0.0 or self.gamma <= 0.0 or self.alphal <= 0.0:
            raise ValueError("preference parameters must be positive")
        if self.chi1 <= 0.0 or self.chi0 < 0.0:
            raise ValueError("adjustment-cost parameters invalid")
        if self.pseudo_time_step <= 0.0 or self.value_change_tolerance <= 0.0:
            raise ValueError("numerical controls must be positive")
        if self.max_value_iterations <= 0:
            raise ValueError("max_value_iterations must be positive")

    def sha256(self) -> str:
        return hashlib.sha256(self.path.read_bytes()).hexdigest().upper()
