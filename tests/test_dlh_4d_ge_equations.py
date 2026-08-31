"""DLH-4D GE equation tests (Issue #20).

Unit tests for the frozen Option A equations: the inverse-MPK capital mapping,
the competitive firm block (w, r_a, Y), the balanced transfer rule, the
ordered residual definitions, the config fixture, and the immutable oracle
identity.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np
import pytest

from deep_learning_hank.ge import GeConfig, GeSolveError, evaluate_ge

CONFIG_PATH = Path("configs/dlh_4d_two_asset_single_region_ge_validation.toml")


def _config():
    return GeConfig.from_toml(CONFIG_PATH)


def test_config_fixture_values():
    cfg = _config()
    assert cfg.b_points == 20 and cfg.a_points == 20
    assert cfg.z_states == (0.8, 1.3)
    assert cfg.rho == 0.02 and cfg.gamma_c == 2.0 and cfg.phi == 5.0
    assert cfg.chi_0 == 0.1 and cfg.chi_1 == 2.0 and cfg.a_bar == 1e-6
    assert cfg.Z == 1.0 and cfg.alpha == 0.36 and cfg.delta_capital == 0.025
    assert cfg.B_gov == 1.0 and cfg.tau == 0.15 and cfg.rb_gap == 0.01
    assert cfg.r_a_low == 0.0 and cfg.r_a_high == 0.12
    assert cfg.r_b_low == -0.05 and cfg.r_b_high == 0.10
    assert cfg.L_low == 0.2 and cfg.L_high == 3.0


def test_immutable_oracle_identity_detects_issue23_repair():
    """Issue #23 (DLH-4D-R3) is the sole Owner-authorized exception to oracle
    immutability: the narrow transfer-FOC liquid-derivative repair changed the
    canonical file.  The frozen Issue #20 config still asserts the pre-repair
    SHA, so the identity gate now fail-closes with exactly the authorized
    mismatch, and the on-disk oracle carries the documented post-repair
    identity."""
    cfg = _config()
    with pytest.raises(
        GeSolveError, match="BLOCKED_DLH_4D_IMMUTABLE_HOUSEHOLD_IDENTITY_MISMATCH"
    ):
        cfg.verify_oracle_identity()
    observed = hashlib.sha256(cfg.oracle_path().read_bytes()).hexdigest().upper()
    assert observed == "1795718C469FC3B427CAB8E3D5957C133BEAD6EACC9EF0A25A3EDB7211D1A024"


def test_frozen_firm_mapping():
    cfg = _config()
    alpha, Z, delta = cfg.alpha, cfg.Z, cfg.delta_capital
    r_a, L = 0.03, 1.0
    K = L * (alpha * Z / (r_a + delta)) ** (1.0 / (1.0 - alpha))
    w = (1.0 - alpha) * Z * (K / L) ** alpha
    Y = Z * (K ** alpha) * (L ** (1.0 - alpha))
    # MPK identity: r_a = alpha*Y/K - delta
    assert abs((alpha * Y / K - delta) - r_a) < 1e-12
    # MPL identity: w = (1-alpha)*Y/L
    assert abs(((1.0 - alpha) * Y / L) - w) < 1e-12
    assert r_a + delta > 0.0


def test_balanced_transfer_rule():
    cfg = _config()
    r_a, r_b, L = 0.03, 0.015, 1.0
    K = L * (cfg.alpha * cfg.Z / (r_a + cfg.delta_capital)) ** (1.0 / (1.0 - cfg.alpha))
    w = (1.0 - cfg.alpha) * cfg.Z * (K / L) ** cfg.alpha
    T = cfg.tau * w * L - r_b * cfg.B_gov
    assert abs((cfg.tau * w * L - r_b * cfg.B_gov) - T) < 1e-14


def test_residual_definitions_match_contract():
    cfg = _config()
    e = evaluate_ge(cfg, 0.02, 0.015, 1.0)
    assert e.finite
    # Residuals follow the frozen map exactly.
    assert abs(e.R1 - (e.A_hh - e.K)) < 1e-12
    assert abs(e.R2 - (e.B_hh - cfg.B_gov)) < 1e-12
    assert abs(e.R3 - (e.L_hh - e.L)) < 1e-12
    # Faithful resource objects are separate and consistent by definition.
    assert abs(e.R_resource_faithful - (e.R_resource_structural - e.W_taper)) < 1e-12


def test_k_mapping_requires_positive_denominator():
    cfg = _config()
    e = evaluate_ge(cfg, -0.03, 0.015, 1.0)
    assert not e.finite  # r_a + delta <= 0 -> fail closed, no root evaluation
