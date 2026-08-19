"""Immutable configuration for the DLH-3B HANK steady-state validation fixture.

Mirrors the accepted Tier-0 configuration conventions (``deep_learning_hank/
config.py``): schema/bounds validation only, every fixture field a documented
numerical-regression value under the explicit labels

- ``VALIDATION_FIXTURE_NOT_CALIBRATION``;
- ``HANK_STEADY_STATE_STRUCTURAL_ONLY``;
- ``STARTING_DLH3B_DEVELOPMENT_DOMAIN_NOT_HANK_DOMAIN_ADEQUACY``.

No field here is an empirical calibration.  The asset domain ``[0,100]`` is a
starting development domain for DLH-3B only; it is NOT proven HANK domain
adequacy (that is DLH-3E business).
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path
import tomllib
from typing import Any

__all__ = [
    "HankNumericalControls",
    "HankSteadyStateConfig",
]


@dataclass(frozen=True)
class HankNumericalControls:
    hjb_tolerance: float
    hjb_max_iterations: int
    hjb_pseudo_time_step: float
    consumption_floor: float
    kfe_stationarity_tolerance: float
    kfe_mass_tolerance: float
    negative_mass_threshold: float
    generator_row_sum_tolerance: float
    generator_min_off_diagonal_tolerance: float
    kkt_tolerance: float
    consumption_foc_tolerance: float
    state_marginal_tolerance: float
    clearing_tolerance: float
    goods_tolerance: float
    fiscal_tolerance: float
    profits_tolerance: float
    wealth_tolerance: float
    nominal_tolerance: float
    truncation_upper_mass_tolerance: float
    root_xtol: float
    root_max_iterations: int
    reproducibility_tolerance: float


@dataclass(frozen=True)
class HankSteadyStateConfig:
    """DLH-3B minimal HANK steady-state structural kernel validation fixture.

    All values are ``VALIDATION_FIXTURE_NOT_CALIBRATION``; the asset domain is
    ``STARTING_DLH3B_DEVELOPMENT_DOMAIN_NOT_HANK_DOMAIN_ADEQUACY``.  Frozen by
    Issue #11 §4/§11; do not alter after the first numerical execution.
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
    frisch: float
    chi: float
    n_max: float
    productivity: float
    epsilon: float
    phi_p: float
    phi_pi: float
    pi_bar: float
    epsilon_i: float
    bond_supply: float
    public_outlay: float
    labor_bracket: tuple[float, float]
    labor_scan_bounds: tuple[float, float]
    labor_scan_points: int
    asset_bracket: tuple[float, float]
    asset_scan_bounds: tuple[float, float]
    asset_scan_points: int
    numerical: HankNumericalControls

    @classmethod
    def from_toml(cls, path: Path) -> "HankSteadyStateConfig":
        resolved = path.resolve()
        with resolved.open("rb") as handle:
            data: dict[str, Any] = tomllib.load(handle)
        fixture = data["fixture"]
        production = data["production"]
        monetary = data["monetary"]
        fiscal = data["fiscal"]
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
            frisch=float(fixture["frisch"]),
            chi=float(fixture["chi"]),
            n_max=float(fixture["n_max"]),
            productivity=float(production["Z"]),
            epsilon=float(production["epsilon"]),
            phi_p=float(production["phi_p"]),
            phi_pi=float(monetary["phi_pi"]),
            pi_bar=float(monetary["pi_bar"]),
            epsilon_i=float(monetary["epsilon_i"]),
            bond_supply=float(fiscal["B"]),
            public_outlay=float(fiscal["G"]),
            labor_bracket=tuple(float(x) for x in root["labor_bracket"]),
            labor_scan_bounds=tuple(float(x) for x in root["labor_scan_bounds"]),
            labor_scan_points=int(root["labor_scan_points"]),
            asset_bracket=tuple(float(x) for x in root["asset_bracket"]),
            asset_scan_bounds=tuple(float(x) for x in root["asset_scan_bounds"]),
            asset_scan_points=int(root["asset_scan_points"]),
            numerical=HankNumericalControls(
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
                kkt_tolerance=float(numerical["kkt_tolerance"]),
                consumption_foc_tolerance=float(numerical["consumption_foc_tolerance"]),
                state_marginal_tolerance=float(numerical["state_marginal_tolerance"]),
                clearing_tolerance=float(numerical["clearing_tolerance"]),
                goods_tolerance=float(numerical["goods_tolerance"]),
                fiscal_tolerance=float(numerical["fiscal_tolerance"]),
                profits_tolerance=float(numerical["profits_tolerance"]),
                wealth_tolerance=float(numerical["wealth_tolerance"]),
                nominal_tolerance=float(numerical["nominal_tolerance"]),
                truncation_upper_mass_tolerance=float(
                    numerical["truncation_upper_mass_tolerance"]
                ),
                root_xtol=float(numerical["root_xtol"]),
                root_max_iterations=int(numerical["root_max_iterations"]),
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
        if self.tau_l < 0.0 or self.tau_l >= 1.0:
            raise ValueError("labor tax rate must lie in [0, 1)")
        if self.frisch <= 0.0 or self.chi <= 0.0 or self.n_max <= 0.0:
            raise ValueError("labor disutility / Frisch / n_max must be strictly positive")
        if self.productivity <= 0.0 or self.epsilon <= 1.0 or self.phi_p <= 0.0:
            raise ValueError("production/price-setting fixture must be strictly positive")
        if self.phi_pi <= 1.0:
            raise ValueError("Taylor principle requires phi_pi > 1 (frozen convention)")
        if self.bond_supply <= 0.0 or self.public_outlay < 0.0:
            raise ValueError("bond supply must be positive; public outlay nonnegative")
        ll, lh = self.labor_bracket
        if not 0.0 < ll < lh:
            raise ValueError("labor bracket must be strictly positive and increasing")
        lsl, lsh = self.labor_scan_bounds
        if not 0.0 < lsl < lsh:
            raise ValueError("labor scan bounds must be strictly positive and increasing")
        al, ah = self.asset_bracket
        if not al < ah:
            raise ValueError("asset bracket must be increasing")
        asl, ash = self.asset_scan_bounds
        if not asl < ash:
            raise ValueError("asset scan bounds must be increasing")
        if self.labor_scan_points < 3 or self.asset_scan_points < 3:
            raise ValueError("scan requires at least three points")
        n = self.numerical
        if n.hjb_tolerance <= 0.0 or n.kfe_stationarity_tolerance <= 0.0:
            raise ValueError("tolerances must be positive")
        if n.hjb_max_iterations <= 0 or n.hjb_pseudo_time_step <= 0.0:
            raise ValueError("HJB iteration controls must be positive")
        if n.consumption_floor < 0.0 or n.negative_mass_threshold > 0.0:
            raise ValueError("consumption floor / negative-mass threshold invalid")
        if n.root_xtol <= 0.0 or n.root_max_iterations <= 0:
            raise ValueError("root controls must be positive")
        if n.truncation_upper_mass_tolerance <= 0.0:
            raise ValueError("truncation sanity tolerance must be positive")

    def sha256(self) -> str:
        return hashlib.sha256(self.path.read_bytes()).hexdigest().upper()
