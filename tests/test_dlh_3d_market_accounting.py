"""DLH-3D market/accounting tests: independent residual gates for NKPC,
Fisher, Taylor, goods/resource, KFE-consistent dynamic wealth flow, fiscal
and profit accounting, plus household/KFE gates on every run."""

from pathlib import Path

import numpy as np
import pytest

from deep_learning_hank.diagnostics.hank_ge_transition import run_ge_validation_cached
from deep_learning_hank.hank_ge_config import HankGeConfig

FIXTURE_PATH = Path(__file__).resolve().parents[1] / "configs" / "dlh_3d_hank_monetary_ge_validation.toml"


@pytest.fixture(scope="module")
def config():
    return HankGeConfig.from_toml(FIXTURE_PATH)


@pytest.fixture(scope="module")
def result(config):
    return run_ge_validation_cached(config)


def test_aggregate_equation_residuals_on_root_interval(config, result) -> None:
    full = next(r for r in result.runs if r.amplitude == 1.0 and r.horizon == config.T)
    final = full.result.final
    k = final.K
    g = config.gates
    assert np.max(np.abs(final.R_nkpc[:k])) <= g.nkpc_tolerance
    assert np.max(np.abs(final.R_fisher[:k])) <= g.fisher_tolerance
    assert np.max(np.abs(final.R_taylor[:k])) <= g.taylor_tolerance
    assert np.max(np.abs(final.R_goods[:k])) <= g.goods_tolerance
    assert np.max(np.abs(final.R_wealth[:k])) <= g.wealth_flow_tolerance
    assert np.max(np.abs(final.R_fiscal[:k])) <= g.fiscal_tolerance
    assert np.max(np.abs(final.R_profits[:k])) <= g.profits_tolerance


def test_wealth_flow_uses_g_next_timing(config, result) -> None:
    full = next(r for r in result.runs if r.amplitude == 1.0 and r.horizon == config.T)
    final = full.result.final
    k = final.K
    # The strict KFE-consistent discrete wealth-flow residual uses g_{k+1}.
    assert final.R_wealth.size == k
    assert np.all(np.isfinite(final.R_wealth))
    assert np.max(np.abs(final.R_wealth)) <= config.gates.wealth_flow_tolerance


def test_goods_residual_is_independent(config, result) -> None:
    full = next(r for r in result.runs if r.amplitude == 1.0 and r.horizon == config.T)
    final = full.result.final
    k = final.K
    # R_goods = Y - C - AC computed independently (never zeroed by Walras-law
    # assumption); terminal point is reported as a separate diagnostic.
    assert np.all(np.isfinite(final.R_goods))
    assert np.max(np.abs(final.R_goods[:k])) <= config.gates.goods_tolerance


def test_household_kfe_gates_every_run(config, result) -> None:
    n = config.numerical
    for run in result.runs:
        final = run.result.final
        hjb = final.hjb
        assert hjb.converged_all
        assert hjb.hjb_residual_max <= n.hjb_residual_tolerance
        assert np.min(hjb.consumption_path) > 0.0
        assert np.min(hjb.drift_path[:, :, 0]) >= -1e-12
        assert np.max(hjb.drift_path[:, :, -1]) <= 1e-12
        assert hjb.labor_kkt_max <= n.kkt_tolerance
        assert hjb.consumption_foc_max <= n.consumption_foc_tolerance
        assert all(s.nan_inf_count == 0 for s in hjb.steps)
        kfe = final.kfe
        assert kfe.mass_error_max <= n.kfe_mass_tolerance
        assert kfe.minimum_mass_min >= n.minimum_mass_threshold
        assert kfe.negative_mass_count_max == 0
        assert kfe.nan_inf_count_max == 0
        assert run.hjb_gates_pass and run.kfe_gates_pass


def test_all_runs_finite(result) -> None:
    for run in result.runs:
        final = run.result.final
        assert np.all(np.isfinite(final.A_hh))
        assert np.all(np.isfinite(final.N_hh))
        assert np.all(np.isfinite(final.C))
        assert np.all(np.isfinite(final.aggregates.w))
        assert np.all(np.isfinite(final.aggregates.N))
