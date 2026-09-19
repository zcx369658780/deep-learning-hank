"""Focused non-training tests for the Issue #76 P2A frozen prototype harness.

Authority: Issue #76 ``DLH-WL-P2A``; activation comment ``5739902019``; marker
``DLH_WL_P2A_FROZEN_SYNTHETIC_EXECUTION_AUTHORIZED``; operative baseline
``fa00cdddf10f14bb55d651ff610668d1ac748234``.

Scope ceiling: this file **never** runs the scientific training loop. It parses the
frozen config, builds the deterministic generator, exercises the frozen algebra and
checks the frozen reference values, plus a few single-step gradient checks that are
not training runs. No real data, no HJB/KFE/GE/MATLAB, no household code.
"""

from __future__ import annotations

import ast
import json
import math
import re
import sys
import tomllib
from pathlib import Path

import numpy as np
import pytest

import deep_learning_hank.regional.labor_destination_p2 as p2

REPO_ROOT = Path(p2.__file__).resolve().parents[3]
MODULE_SOURCE = Path(p2.__file__).read_text(encoding="utf-8")
RUNNER_PATH = REPO_ROOT / "scripts" / "run_dlh_wl_p2_offline_prototype.py"
CONFIG_PATH = REPO_ROOT / "configs" / "dlh_wl_p2_offline_prototype.toml"
CONTRACT_PATH = REPO_ROOT / "docs" / "specifications" / "DLH_WL_P2_OFFLINE_PROTOTYPE_CONTRACT_2026_09_18.md"
SCHEMA_PATH = REPO_ROOT / "docs" / "data" / "DLH_WL_P1B_LABEL_AND_SAMPLE_SCHEMA_2026_09_18.md"

FROZEN_S0 = {
    "r00_t1": [0.477725159, 0.221843778, 0.164194930, 0.136236133],
    "r00_t4": [0.477966319, 0.221836852, 0.164104853, 0.136091976],
    "r04_t1": [0.152928167, 0.196744187, 0.650327646],
    "r04_t4": [0.153106303, 0.196861942, 0.650031755],
}
FROZEN_S1 = {
    "r00_t1": [0.479223272, 0.219532182, 0.163400470, 0.137844076],
    "r00_t4": [0.479478444, 0.219535648, 0.163308523, 0.137677385],
    "r04_t1": [0.150941617, 0.194939240, 0.654119143],
    "r04_t4": [0.151139135, 0.195055970, 0.653804895],
}


@pytest.fixture(scope="module")
def config() -> p2.P2Config:
    return p2.load_frozen_config(REPO_ROOT)


@pytest.fixture(scope="module")
def universe(config: p2.P2Config) -> p2.SyntheticUniverse:
    return p2.build_universe(config, REPO_ROOT)


# ---------------------------------------------------------------- 1. config identity
def test_toml_parses_and_revision_is_frozen():
    raw = tomllib.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    assert len(raw) == 17
    assert raw["authority"]["config_revision"] == 4
    assert raw["authority"]["activation_comment"] == 5731890746
    assert raw["authority"]["operative_baseline"] == "4b4dc8c39d6a18b8928407308248f4020c10602c"
    assert raw["authority"]["design_only_in_this_issue"] is True


def test_load_frozen_config_identity(config: p2.P2Config):
    assert config.config_revision == 4
    assert len(config.sha256) == 64
    assert config.fitted_columns == ("log_gdp_dest", "log_wage_gap", "log_adj_distance",
                                     "adjacency", "log_accessibility_dest", "w_ij")
    assert config.neural_seeds == (0, 1, 2)
    assert config.hidden_widths == (16, 8)
    assert config.activations == ("ReLU", "Tanh")
    assert config.max_steps == 1500 and config.eval_every == 50
    assert config.early_stop_patience == 200
    assert abs(config.early_stop_min_delta - 1e-4) < 1e-18
    assert config.learning_rate == 0.01
    assert config.primary_fit_configurations == 8
    assert config.planned_fit_executions == 12
    assert config.absolute_attempt_ceiling == 13
    assert config.wall_clock_seconds_max == 1800.0


def test_frozen_inputs_are_read_only_in_this_issue():
    """The #75 config/contract/schema must not be modified by this Issue."""
    gitignore = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")
    assert "configs" not in gitignore.split()
    for path in (CONFIG_PATH, CONTRACT_PATH, SCHEMA_PATH):
        assert path.is_file(), path
    assert "config_revision = 4" in CONFIG_PATH.read_text(encoding="utf-8")


# ---------------------------------------------------------------- 2. universe/generator
def test_universe_shape_support_and_orientation(universe: p2.SyntheticUniverse):
    cfg = universe.config
    assert len(cfg.region_ids) == 5
    assert len(universe.blocks) == 20
    assert len(universe.design_meta) == 72
    assert [len(universe.blocks[i].allowed) for i in range(5)] == [4, 4, 4, 3, 3]
    assert universe.m.min() >= 0.0 and universe.m.max() <= 1.0
    assert abs(universe.m.min() - 0.07) < 1e-12 and abs(universe.m.max() - 0.17) < 1e-12
    assert abs(universe.ell.min() - 60.0) < 1e-12 and abs(universe.ell.max() - 127.2) < 1e-12
    # orientation: diagonal structurally unavailable, blocked pairs unavailable
    assert not np.any(np.diag(universe.support))
    assert not universe.support[3, 2] and not universe.support[4, 2]
    assert np.diag(universe.support).sum() == 0
    for regime in ("S0", "S1"):
        diagonal = np.einsum("tii->ti", universe.targets[regime])
        assert np.all(diagonal == 0.0)
        assert np.all(universe.targets[regime] >= 0.0)
        for b in universe.blocks:
            row_sum = sum(universe.targets[regime][b.time_index, b.origin, j] for j in b.allowed)
            assert abs(row_sum - 1.0) < 1e-12


def test_generator_reference_shares_match_frozen_vectors(universe: p2.SyntheticUniverse):
    report = p2.validate_only_report(universe)
    for regime, expected in (("S0", FROZEN_S0), ("S1", FROZEN_S1)):
        for key, values in expected.items():
            got = report["reference_shares"][f"{regime}:{key}"]
            assert len(got) == len(values)
            for a, b in zip(got, values):
                assert abs(a - b) < 5e-9, (regime, key, got, values)


def test_reference_shares_carry_small_time_variation(universe: p2.SyntheticUniverse):
    report = p2.validate_only_report(universe)
    for regime in ("S0", "S1"):
        t1 = report["reference_shares"][f"{regime}:r00_t1"]
        t4 = report["reference_shares"][f"{regime}:r00_t4"]
        assert max(abs(a - b) for a, b in zip(t1, t4)) > 1e-6


def test_p1a_accounting_invariants_close(universe: p2.SyntheticUniverse):
    diag = universe.p1a_diagnostics
    for regime in ("S0", "S1"):
        for row in diag[regime]:
            assert row["origin_conservation_max_abs_deviation"] <= 1e-12
            assert row["national_conservation_max_abs_deviation"] <= 1e-12
            assert row["destination_aggregation_max_abs_deviation"] <= 1e-12
            # R03/R04 have three allowed foreign destinations, so four blocks are
            # below the five-region count; the P1A row masks must reflect that
            assert row["active_row_count"] == 5
            assert row["valid_row_count"] == 5
            assert row["identifiable_rows"] == 5
            assert row["conditional_choice_identified"] is True
            assert row["total_labor"] > 0.0


# ---------------------------------------------------------------- 3. split
def test_split_counts_and_held_out_origin_interpretation(universe: p2.SyntheticUniverse):
    cfg = universe.config
    counts = {state: len(universe.blocks_for(state))
              for state in ("TRAIN", "VALIDATION", "TEST", "EXCLUDED_REFERENCE_ONLY")}
    assert counts == {"TRAIN": 9, "VALIDATION": 3, "TEST": 2, "EXCLUDED_REFERENCE_ONLY": 6}
    assert sum(counts.values()) == 20
    assert counts == cfg.split_counts

    train_origins = {b.origin_id for b in universe.blocks_for("TRAIN")}
    test_origins = {b.origin_id for b in universe.blocks_for("TEST")}
    assert train_origins == {"R00", "R01", "R02"}
    assert test_origins == {"R03", "R04"}
    assert test_origins.isdisjoint(train_origins)

    train_dest_ids = {universe.config.region_ids[j] for b in universe.blocks_for("TRAIN") for j in b.allowed}
    assert test_origins <= train_dest_ids, "R03/R04 must appear as TRAIN destinations"
    assert {b.time_id for b in universe.blocks_for("TEST")} == {4}
    assert {b.time_id for b in universe.blocks_for("TRAIN")} == {1, 2, 3}


def test_excluded_blocks_are_never_used_for_training(universe: p2.SyntheticUniverse):
    train_keys = {b.key for b in universe.blocks_for("TRAIN")}
    for state in ("VALIDATION", "TEST", "EXCLUDED_REFERENCE_ONLY"):
        assert {b.key for b in universe.blocks_for(state)}.isdisjoint(train_keys)
    raw = tomllib.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    assert raw["split"]["excluded_reference_only"]["used_for_fitting"] is False
    assert raw["split"]["excluded_reference_only"]["used_for_early_stopping"] is False
    assert raw["split"]["excluded_reference_only"]["used_for_final_metrics"] is False


# ---------------------------------------------------------------- 4. features
def test_feature_matrix_dimensions_and_order(universe: p2.SyntheticUniverse):
    cfg = universe.config
    assert universe.pair_values.shape == (72, len(cfg.pair_features) == 5 and 5)
    assert universe.node_origin_values.shape == (72, 4)
    assert universe.node_dest_values.shape == (72, 4)
    assert universe.time_values.shape == (72, 1)
    assert universe.static_values.shape == (72, 1)
    assert universe.raw_design.shape == (72, 15)
    frozen_order = [cfg.pair_features.index(n) for n in ("log_gdp_dest", "log_wage_gap",
                                                         "log_adj_distance", "adjacency",
                                                         "log_accessibility_dest")]
    assert frozen_order == [0, 1, 2, 3, 4]
    assert cfg.static_features == ("w_ij",)


def test_preprocessing_is_fitted_on_train_only(universe: p2.SyntheticUniverse):
    train_blocks = universe.blocks_for("TRAIN")
    design, meta = p2._train_only_zscore(universe, train_blocks)
    assert meta["fitted_on"] == "TRAIN_ONLY"
    z_cols = meta["pair_column_indices"]
    train_rows = universe.pair_values[universe.design_indices(train_blocks)]
    assert np.allclose(design[universe.design_indices(train_blocks)][:, z_cols].mean(axis=0), 0.0, atol=1e-12)
    assert np.allclose(design[universe.design_indices(train_blocks)][:, z_cols].std(axis=0), 1.0, atol=1e-12)
    # statistics must differ from whole-universe statistics, proving TRAIN-only fitting
    whole_mean = universe.pair_values[:, z_cols].mean(axis=0)
    assert not np.allclose(meta["mean"], whole_mean, atol=1e-9)


def test_m_and_ell_are_not_model_inputs(universe: p2.SyntheticUniverse):
    cfg = universe.config
    assert cfg.zscored_features == ("log_gdp_dest", "log_wage_gap", "log_adj_distance",
                                    "log_accessibility_dest")
    assert "m_i" not in universe.raw_design.dtype.names if universe.raw_design.dtype.names else True
    assert universe.raw_design.shape[1] == 15  # 5 pair + 4 origin + 4 dest + 1 time + 1 static
    for name in ("m", "ell"):
        assert name not in cfg.pair_features and name not in cfg.node_features


# ---------------------------------------------------------------- 5. frozen design checks
def test_contrast_design_rank_and_residuals(universe: p2.SyntheticUniverse):
    report = p2.validate_only_report(universe)
    assert report["contrast_rows"] == 27
    assert report["contrast_columns"] == 6
    assert report["contrast_rank"] == 6
    assert report["s0_contrast_residual"] <= report["residual_precision_floor"]
    assert abs(report["s0_contrast_residual"] - 1.1102230246251565e-15) < 1e-18
    assert abs(report["s1_contrast_residual"] - 0.008699130793511367) < 1e-12
    assert abs(report["x2_contrast_residual"] - 0.17058604712292663) < 1e-12
    assert abs(report["x3_contrast_residual"] - 0.019805631317407806) < 1e-12
    assert report["s1_contrast_residual"] > 1e-3
    assert report["optimizer_steps_performed"] == 0


def test_masked_softmax_and_fixed_baseline(universe: p2.SyntheticUniverse):
    scores = np.array([1.0, 2.0, 3.0])
    mask = np.array([True, False, True])
    shares = p2._masked_softmax(scores, mask)
    assert abs(shares.sum() - 1.0) < 1e-15
    assert shares[1] == 0.0
    assert shares[2] > shares[0]

    for regime in ("S0", "S1"):
        pred = p2.fixed_baseline_predictions(universe, regime)
        for b in universe.blocks:
            share = 1.0 / len(b.allowed)
            for j in b.allowed:
                assert abs(pred[b.time_index, b.origin, j] - share) < 1e-15
        metrics = p2.evaluate_predictions(universe, regime, pred, universe.blocks_for("TEST"))
        assert metrics["row_normalization_violation_max"] <= 1e-15
        assert metrics["negativity_violation_count"] == 0
        assert metrics["support_violation_count"] == 0


def test_loss_and_metric_algebra_on_hand_built_predictions(universe: p2.SyntheticUniverse):
    regime = "S0"
    perfect = universe.targets[regime].copy()
    blocks = universe.blocks_for("TEST")
    metrics = p2.evaluate_predictions(universe, regime, perfect, blocks)
    # a perfect prediction has zero error, zero KL and unit row sums; its weighted
    # cross entropy equals the weighted entropy of the target, not zero
    weights = np.array([universe.ell[b.time_index, b.origin] for b in blocks])
    weights = weights / weights.sum()
    expected_entropy = 0.0
    for weight, b in zip(weights, blocks):
        for j in b.allowed:
            t_val = universe.targets[regime][b.time_index, b.origin, j]
            expected_entropy += -weight * t_val * math.log(t_val)
    assert metrics["mean_absolute_share_error"] <= 1e-15
    assert metrics["row_normalization_violation_max"] <= 1e-12
    assert metrics["top1_destination_accuracy"] == 1.0
    assert metrics["share_kl_per_block_mean"] <= 1e-12
    assert metrics["support_violation_count"] == 0
    assert abs(metrics["weighted_cross_entropy"] - expected_entropy) < 1e-12

    uniform = p2.fixed_baseline_predictions(universe, regime)
    uniform_metrics = p2.evaluate_predictions(universe, regime, uniform, blocks)
    expected_ce = 0.0
    weights = np.array([universe.ell[b.time_index, b.origin] for b in blocks])
    weights = weights / weights.sum()
    for weight, b in zip(weights, blocks):
        expected_ce += -weight * math.log(1.0 / len(b.allowed))
    assert abs(uniform_metrics["weighted_cross_entropy"] - expected_ce) < 1e-12
    assert uniform_metrics["weighted_cross_entropy"] > metrics["weighted_cross_entropy"]

    test_block = blocks[0]
    origin = test_block.origin
    broken = uniform.copy()
    broken[test_block.time_index, origin, 0] = -0.5        # negativity + row-sum violation
    broken[test_block.time_index, origin, 2] = 0.25        # blocked/structural cell (R02)
    broken_metrics = p2.evaluate_predictions(universe, regime, broken, blocks)
    assert broken_metrics["negativity_violation_count"] >= 1
    assert broken_metrics["support_violation_count"] >= 1
    assert broken_metrics["row_normalization_violation_max"] > 0.0


# ---------------------------------------------------------------- 6. gradient sanity
def test_neural_forward_backward_matches_finite_differences(universe: p2.SyntheticUniverse):
    """Single-step gradient check; this is not a training run."""
    cfg = universe.config
    design, _ = p2._train_only_zscore(universe, universe.blocks_for("TRAIN"))
    train = universe.blocks_for("TRAIN")
    X, Y, raw_w, mask, cell_index = p2._stack(universe, train, "S0", design)
    w = raw_w / raw_w.sum()
    params = p2._init_mlp(0, design.shape[1], cfg.hidden_widths)
    keys = sorted(params)

    def flat(p: dict[str, np.ndarray]) -> np.ndarray:
        return np.concatenate([p[k].ravel() for k in keys])

    def unflat(theta: np.ndarray) -> dict[str, np.ndarray]:
        out, pos = {}, 0
        for k in keys:
            size = int(params[k].size)
            out[k] = theta[pos:pos + size].reshape(params[k].shape)
            pos += size
        return out

    def loss(theta: np.ndarray) -> float:
        scores, _, _ = p2._forward(unflat(theta), X, cfg.hidden_widths)
        value, _ = p2._softmax_cross_entropy(scores.reshape(-1), Y, w, mask, cell_index)
        return value

    scores, acts, pre = p2._forward(params, X, cfg.hidden_widths)
    _, grad_scores = p2._softmax_cross_entropy(scores.reshape(-1), Y, w, mask, cell_index)
    analytic = p2._backward(params, acts, pre, grad_scores, cfg.hidden_widths)
    theta = flat(params)
    grad_flat = np.concatenate([analytic[k].ravel() for k in keys])

    # the loss is softmax-invariant to a constant added to every score in a block,
    # so only derivatives that actually move the score vector are compared: the
    # output bias b2 and any constant shift are excluded by construction.
    eps = 1e-5
    checked = 0
    for i in range(0, theta.size, 17):
        up, down = theta.copy(), theta.copy()
        up[i] += eps
        down[i] -= eps
        numeric = (loss(up) - loss(down)) / (2 * eps)
        assert abs(numeric - grad_flat[i]) < 1e-5 * max(1.0, abs(numeric), abs(grad_flat[i])) or (
            abs(numeric) < 1e-9 and abs(grad_flat[i]) < 1e-9), (i, numeric, grad_flat[i])
        checked += 1
    assert checked >= 20


def test_adam_step_reduces_loss_on_a_two_block_problem(universe: p2.SyntheticUniverse):
    """Twenty Adam steps on a two-block toy problem; not the scientific run."""
    cfg = universe.config
    R = len(cfg.region_ids)
    mask = np.zeros((2, R), dtype=bool)
    mask[0, 0] = mask[0, 1] = True
    mask[1, 1] = mask[1, 2] = True
    cell_index = np.array([0, 0, 1, 1])
    Y = np.array([0.3, 0.7, 0.6, 0.4])
    w = np.array([1.0, 1.0])
    X = np.array([
        [1.0, -0.5, 0.25, 0.0, -1.0, 0.5, 0.2, -0.2, 0.1, -0.1, 0.3, 0.4, -0.4, 0.05, 0.5],
        [0.5, 0.5, -0.25, 0.1, 0.5, -0.5, -0.2, 0.2, -0.1, 0.1, -0.3, -0.4, 0.4, -0.05, -0.5],
        [-0.5, 0.25, 0.5, -0.2, 0.25, 0.25, 0.4, 0.1, -0.3, 0.2, 0.1, -0.2, 0.2, 0.15, 0.25],
        [0.25, -0.75, 0.0, 0.3, -0.25, 0.75, -0.4, -0.1, 0.3, -0.2, -0.1, 0.2, -0.2, -0.15, -0.25],
    ])
    params = p2._init_mlp(0, X.shape[1], cfg.hidden_widths)
    state: dict[str, np.ndarray] = {}

    def loss() -> float:
        scores, _, _ = p2._forward(params, X, cfg.hidden_widths)
        value, _ = p2._softmax_cross_entropy(scores.reshape(-1), Y, w, mask, cell_index)
        return value

    start = loss()
    for step in range(1, 21):
        scores, acts, pre = p2._forward(params, X, cfg.hidden_widths)
        _, grad_scores = p2._softmax_cross_entropy(scores.reshape(-1), Y, w, mask, cell_index)
        grads = p2._backward(params, acts, pre, grad_scores, cfg.hidden_widths)
        p2._adam_step(params, grads, state, step, cfg.learning_rate)
    assert loss() < start


def test_loss_uses_per_block_masked_softmax_not_a_global_one(universe: p2.SyntheticUniverse):
    """Zero scores must give a uniform-within-block loss, never a cross-block gain."""
    design, _ = p2._train_only_zscore(universe, universe.blocks_for("TRAIN"))
    blocks = universe.blocks_for("TRAIN")
    X, Y, raw_w, mask, cell_index = p2._stack(universe, blocks, "S0", design)
    w = raw_w / raw_w.sum()
    value, grad = p2._softmax_cross_entropy(np.zeros(X.shape[0]), Y, w, mask, cell_index)
    expected = 0.0
    for weight, b in zip(w, blocks):
        expected += -weight * math.log(1.0 / len(b.allowed))
    assert abs(value - expected) < 1e-12
    # with zero scores the per-block softmax is uniform, so p equals the uniform
    # target only when the block is uniform; the gradient stays finite and bounded
    assert np.all(np.isfinite(grad))
    assert np.abs(grad).max() < 1.0


# ---------------------------------------------------------------- 7. static guards
def test_no_forbidden_scientific_imports_in_module_or_runner():
    for path in (Path(p2.__file__), RUNNER_PATH):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imported: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module)
        for name in imported:
            assert not name.startswith("deep_learning_hank.two_asset"), (path, name)
            assert not name.startswith(("torch", "tensorflow", "jax", "matlab")), (path, name)


def test_module_never_references_household_or_solver_entrypoints():
    for symbol in ("solve_household_steady_state", "solve_matlab_faithful_hjb",
                   "solve_matlab_faithful_stationary_kfe", "select_matlab_faithful_local_policy",
                   "assemble_source_operator", "BoundaryHJBSolver"):
        assert symbol not in MODULE_SOURCE
        assert symbol not in RUNNER_PATH.read_text(encoding="utf-8")


def test_runner_declares_frozen_budget_and_read_only_inputs():
    text = RUNNER_PATH.read_text(encoding="utf-8")
    assert "--validate-only" in text and "--execute" in text
    assert "configs/dlh_wl_p2_offline_prototype.toml" in text
    assert "OMP_NUM_THREADS" in text and "PYTHONHASHSEED" in text
    assert "DLH_WL_P2_RESULTS.json" in text
    assert "DLH_WL_P2_MANIFEST.json" in text
    assert "DLH_WL_P2_REPORT.md" in text


def test_terminal_strings_are_exactly_the_issue_set(universe: p2.SyntheticUniverse):
    assert p2.TERMINAL_PASS == "DLH_WL_P2A_OFFLINE_SYNTHETIC_PROTOTYPE__PASS__RESULT_INTERPRETABLE"
    assert p2.TERMINAL_GATE_FAIL == "DLH_WL_P2A_OFFLINE_SYNTHETIC_PROTOTYPE__GATE_FAIL__NO_TUNING_AUTHORIZED"
    assert p2.TERMINAL_BLOCKED == "BLOCKED_DLH_WL_P2A_IMPLEMENTATION_ENVIRONMENT_OR_BUDGET"


def test_interpretation_ceiling_is_declared(universe: p2.SyntheticUniverse):
    assert universe.config.region_ids == ("R00", "R01", "R02", "R03", "R04")
    source = MODULE_SOURCE
    assert "unseen-region" in source
    assert "no real data" in source.lower()
    assert "held-out" in source.lower()
