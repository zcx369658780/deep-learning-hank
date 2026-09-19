"""DLH-WL-P2D — focused pre-run protocol tests (Issue #79).

Zero optimizer steps, zero fits, zero training. The tests cover:

* frozen identity (config revision, blobs, plan, ceilings, terminals);
* the **mandatory zero-fit preprocessing-path gate** (Issue #79 section 3): the runner's
  actual setup helper installs the TRAIN-only z-scored design, the accepted module's real
  final prediction path reads that design, the predictions match an independent z-scored
  reference computed from the same frozen parameters, and deliberately clearing
  ``_design_matrix`` reproduces a materially different raw-fallback tensor — so this test
  proves it would have caught the Issue #78 defect;
* the runner's fail-closed refusal to fit through the raw fallback;
* durable ``FIT_COMPLETED`` records carrying full 4x5x5 tensors plus the neural
  preprocessing-contract evidence;
* the mandatory fake 12-fit ledger driving the exact production render path end-to-end
  with zero fits while every fitter is patched to explode;
* the renderer's preprocessing-contract gate, including that it fails loudly on a tampered
  or missing contract;
* renderer AST guards, split interpretation, forbidden imports and artifact schemas.

Authority: Issue #79 ``DLH-WL-P2D``; activation comment ``5740829235``; marker
``DLH_WL_P2D_PREPROCESSING_CORRECTED_DURABLE_REPLICATION_AUTHORIZED``.
"""

from __future__ import annotations

import ast
import json
import sys
import tomllib
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
for path in (str(SRC), str(ROOT / "scripts")):
    if path not in sys.path:
        sys.path.insert(0, path)

import run_dlh_wl_p2d_replication_science as science  # noqa: E402
import render_dlh_wl_p2d_replication as renderer  # noqa: E402
from deep_learning_hank.regional import labor_destination_p2 as sci  # noqa: E402

CONFIG_PATH = ROOT / science.CONFIG_RELPATH
MODULE_PATH = ROOT / science.SCIENTIFIC_MODULE_RELPATH
SCIENCE_RUNNER = ROOT / renderer.SCIENCE_RUNNER_RELPATH
RENDERER = ROOT / renderer.RENDERER_RELPATH
TEST_FREEZE_SHA = "TEST_FREEZE_SHA_NOT_A_REAL_COMMIT"
FROZEN_S0_R00_T1 = [0.477725159, 0.221843778, 0.164194930, 0.136236133]
FROZEN_S1_R04_T4 = [0.151139135, 0.195055970, 0.653804895]
FALLBACK_DIFFERENCE_FLOOR = 1e-3


@pytest.fixture(scope="module")
def config() -> sci.P2Config:
    return sci.load_frozen_config(ROOT, config_relpath=science.CONFIG_RELPATH)


@pytest.fixture(scope="module")
def universe(config: sci.P2Config) -> sci.SyntheticUniverse:
    return sci.build_universe(config, ROOT)


@pytest.fixture
def fresh_universe(config: sci.P2Config) -> sci.SyntheticUniverse:
    """A per-test universe, because the preprocessing tests mutate `_design_matrix`."""
    return sci.build_universe(config, ROOT)


# ------------------------------------------------------- 1. authority and identity
def test_issue_authority_constants():
    assert science.PLANNED_FIT_ATTEMPTS == 12
    assert science.SCIENCE_WALL_CLOCK_CEILING_SECONDS == 1800.0
    assert science.EXPERIMENT_ID == "EXP-20260919-DLH-WL-P2D-001"
    assert science.TASK_ID == "DLH_WL_P2D_PREPROCESSING_CORRECTED_REPLICATION"
    assert science.AUTHORITY_MARKER == (
        "DLH_WL_P2D_PREPROCESSING_CORRECTED_DURABLE_REPLICATION_AUTHORIZED")
    assert science.TERMINAL_PASS == (
        "DLH_WL_P2D_PREPROCESSING_CORRECTED_REPLICATION__PASS__P2_METHOD_GATE_COMPLETE")
    assert science.TERMINAL_GATE_FAIL == (
        "DLH_WL_P2D_PREPROCESSING_CORRECTED_REPLICATION__GATE_FAIL__"
        "NO_SCIENCE_RERUN_AUTHORIZED")
    assert science.TERMINAL_BLOCKED == "BLOCKED_DLH_WL_P2D_PRE_RUN_OR_ENVIRONMENT"
    assert renderer.TERMINAL_PASS == science.TERMINAL_PASS
    assert renderer.TERMINAL_GATE_FAIL == science.TERMINAL_GATE_FAIL
    assert renderer.TERMINAL_BLOCKED == science.TERMINAL_BLOCKED
    assert science.ROUTE == "DLH-WL-V1-20260918"
    assert science.REQUIRED_ASSIGNMENT == "universe._design_matrix = design"
    assert renderer.REQUIRED_ASSIGNMENT == science.REQUIRED_ASSIGNMENT
    assert science.TRAINING_DESIGN_LABEL == "TRAIN_ONLY_ZSCORED"
    assert science.PREDICTION_DESIGN_LABEL == "TRAIN_ONLY_ZSCORED"


def test_frozen_config_identity(config: sci.P2Config):
    raw = tomllib.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    assert raw["authority"]["config_revision"] == 4
    assert config.config_revision == 4
    assert science.blob_sha1_lf(CONFIG_PATH) == science.EXPECTED_CONFIG_BLOB
    assert renderer.blob_sha1_lf(CONFIG_PATH) == renderer.EXPECTED_CONFIG_BLOB
    assert config.neural_seeds == (0, 1, 2)
    assert config.hidden_widths == (16, 8)
    assert config.max_steps == 1500 and config.eval_every == 50
    assert config.early_stop_patience == 200 and config.early_stop_min_delta == 1e-4
    assert config.learning_rate == 0.01
    assert config.absolute_attempt_ceiling == 13
    assert config.planned_fit_executions == 12
    assert config.wall_clock_seconds_max == 1800.0
    assert config.row_normalization_tolerance == 1e-10
    assert config.determinism_tolerance == 1e-12
    assert config.excluded_block_count_expected == 6


def test_scientific_module_blob_is_the_accepted_76_module():
    blob = science.blob_sha1_lf(MODULE_PATH)
    assert blob == science.EXPECTED_SCIENTIFIC_MODULE_BLOB == (
        "b1f2cd043605c511e4965254657d12306170609b")
    assert renderer.blob_sha1_lf(MODULE_PATH) == renderer.EXPECTED_SCIENTIFIC_MODULE_BLOB
    assert science.verify_module_blob() == (science.EXPECTED_SCIENTIFIC_MODULE_BLOB, "MATCH")


def test_frozen_inputs_are_read_only_declarations():
    for relpath in (science.CONFIG_RELPATH, science.CONTRACT_RELPATH, science.SCHEMA_RELPATH,
                    science.P1A_MODULE_RELPATH, science.SCIENTIFIC_MODULE_RELPATH):
        assert (ROOT / relpath).is_file(), relpath
    text = SCIENCE_RUNNER.read_text(encoding="utf-8")
    assert "never modified here" in text
    assert "no real data, no HJB/KFE/GE/MATLAB/household code, no tuning, no extra seed" in text


# ------------------------------------------------------------- 2. generator checks
def test_generator_reference_shares(universe: sci.SyntheticUniverse):
    report = sci.validate_only_report(universe)
    got_s0 = report["reference_shares"]["S0:r00_t1"]
    got_s1 = report["reference_shares"]["S1:r04_t4"]
    assert all(abs(a - b) < 5e-9 for a, b in zip(got_s0, FROZEN_S0_R00_T1))
    assert all(abs(a - b) < 5e-9 for a, b in zip(got_s1, FROZEN_S1_R04_T4))
    assert report["contrast_rank"] == 6
    assert report["s0_contrast_residual"] <= report["residual_precision_floor"]
    assert report["s1_contrast_residual"] > report["residual_precision_floor"]
    assert report["optimizer_steps_performed"] == 0


def test_split_counts_and_interpretation_ceiling(universe: sci.SyntheticUniverse):
    counts = {state: len(universe.blocks_for(state)) for state in renderer.SPLIT_STATES}
    assert counts == {"TRAIN": 9, "VALIDATION": 3, "TEST": 2, "EXCLUDED_REFERENCE_ONLY": 6}
    assert sum(counts.values()) == 20
    view = renderer.frozen_split_interpretation(universe)
    assert view["test_regions_are_unseen_regions"] is False
    assert view["test_touches_train_origin"] is False
    assert view["test_touches_train_time"] is False
    assert view["test_regions_appear_as_train_destinations"] is True
    assert "UNSEEN_REGION" in view["generalization_claims_forbidden"]


def test_no_unseen_region_claim_in_code():
    for path in (SCIENCE_RUNNER, RENDERER, Path(__file__)):
        text = path.read_text(encoding="utf-8")
        if "UNSEEN_REGION" in text:
            assert ("forbidden" in text.lower()) or ("is_unseen_regions" in text), path


# ------------------------------------------------------------------ 3. fit plan data
def test_fit_plan_is_exactly_twelve_frozen_attempts(config: sci.P2Config):
    plan = science.build_fit_plan(config)
    assert len(plan) == 12
    assert [entry["attempt_index"] for entry in plan] == list(range(1, 13))
    assert [entry["fit_key"] for entry in plan] == [
        "S0:parametric", "S1:parametric", "S0:parametric:repeat", "S1:parametric:repeat",
        "S0:neural:seed0", "S0:neural:seed1", "S0:neural:seed2",
        "S1:neural:seed0", "S1:neural:seed1", "S1:neural:seed2",
        "S0:neural:seed0:repeat", "S1:neural:seed0:repeat"]
    families = [entry["family"] for entry in plan]
    assert families.count("parametric") == 4
    assert families.count("neural") == 8
    kinds = [entry["kind"] for entry in plan]
    assert kinds.count("primary") == 8
    assert kinds.count("verification_repeat") == 4
    assert science.primary_fit_keys(plan) == list(renderer.PRIMARY_FIT_KEYS)
    assert science.repeat_pairs(plan) == list(renderer.REPEAT_PAIRS)


def test_fit_plan_rejects_a_non_frozen_seed_list(config: sci.P2Config):
    with pytest.raises(ValueError):
        science.build_fit_plan(replace(config, neural_seeds=(0, 1, 2, 3)))
    with pytest.raises(ValueError):
        science.build_fit_plan(replace(config, neural_seeds=(0, 1)))


def test_science_runner_has_no_retry_or_extra_seed_switches():
    text = SCIENCE_RUNNER.read_text(encoding="utf-8")
    for forbidden in ("--retry", "--extra-seed", "--tune", "--search", "--force",
                      "--max-steps", "--steps"):
        assert forbidden not in text, forbidden
    assert "--execute-science" in text and "--validate-only" in text


# --------------------------------- 4. THE mandatory zero-fit preprocessing-path gate
def test_setup_helper_installs_the_train_only_zscored_design(
        fresh_universe: sci.SyntheticUniverse):
    """Issue #79 section 3 steps 1-4: the runner's actual setup helper installs the state."""
    universe = fresh_universe
    assert universe._design_matrix is None, "a fresh universe must not have a design set"
    design, meta = science.setup_preprocessing_state(universe)
    assert universe._design_matrix is design
    assert np.array_equal(universe.design_matrix, design)
    assert meta["assignment_performed"] == "universe._design_matrix = design"
    assert meta["training_design"] == "TRAIN_ONLY_ZSCORED"
    assert meta["prediction_design"] == "TRAIN_ONLY_ZSCORED"
    assert meta["design_installed_on_universe"] is True


def test_installed_design_is_zscored_and_not_the_raw_fallback(
        fresh_universe: sci.SyntheticUniverse):
    universe = fresh_universe
    design, meta = science.setup_preprocessing_state(universe)
    assert universe.design_matrix is not universe.raw_design
    assert not np.array_equal(universe.design_matrix, universe.raw_design)
    assert meta["zscored_differs_from_raw"] is True
    assert universe.design_matrix.shape == universe.raw_design.shape
    cfg = universe.config
    z_cols = [cfg.pair_features.index(name) for name in cfg.zscored_features]
    train_index = universe.design_indices(universe.blocks_for("TRAIN"))
    train_rows = universe.design_matrix[train_index]
    assert np.allclose(train_rows[:, z_cols].mean(axis=0), 0.0, atol=1e-12)
    assert np.allclose(train_rows[:, z_cols].std(axis=0), 1.0, atol=1e-9)
    raw_cols = [i for i in range(universe.raw_design.shape[1]) if i not in z_cols]
    assert np.array_equal(universe.design_matrix[:, raw_cols],
                          universe.raw_design[:, raw_cols])


def test_fake_params_are_deterministic_and_require_no_optimizer(
        fresh_universe: sci.SyntheticUniverse):
    universe = fresh_universe
    widths = universe.config.hidden_widths
    params = sci._init_mlp(0, universe.raw_design.shape[1], widths)
    again = sci._init_mlp(0, universe.raw_design.shape[1], widths)
    assert all(np.array_equal(params[k], again[k]) for k in params)
    assert params["W0"].shape == (universe.raw_design.shape[1], widths[0])


def test_accepted_final_prediction_path_uses_the_zscored_design(
        fresh_universe: sci.SyntheticUniverse):
    """Issue #79 section 3 steps 5-8: real ``_neural_predict`` vs an independent reference."""
    universe = fresh_universe
    design, _meta = science.setup_preprocessing_state(universe)
    widths = universe.config.hidden_widths
    params = sci._init_mlp(0, design.shape[1], widths)

    via_module = sci._neural_predict(universe, "S0", params, widths)

    reference = np.zeros_like(via_module)
    for block in universe.blocks:
        idx = [universe.row(block.time_index, block.origin, j) for j in block.allowed]
        scores, _, _ = sci._forward(params, np.asarray(design)[idx], widths)
        shares = sci._masked_softmax(scores.reshape(-1), np.ones(len(idx), dtype=bool))
        for pos, j in enumerate(block.allowed):
            reference[block.time_index, block.origin, j] = shares[pos]

    assert via_module.shape == (4, 5, 5)
    assert np.array_equal(via_module, reference), "the module must read the installed design"
    assert np.all(np.isfinite(via_module))


def test_deliberate_raw_fallback_is_materially_different_negative_control(
        fresh_universe: sci.SyntheticUniverse):
    """Issue #79 section 3 step 9: prove the test would have caught the Issue #78 bug."""
    universe = fresh_universe
    design, _meta = science.setup_preprocessing_state(universe)
    widths = universe.config.hidden_widths
    params = sci._init_mlp(0, design.shape[1], widths)

    corrected = sci._neural_predict(universe, "S0", params, widths)

    original = universe._design_matrix
    universe._design_matrix = None            # reproduce the Issue #78 omission
    try:
        assert universe.design_matrix is universe.raw_design
        raw_fallback = sci._neural_predict(universe, "S0", params, widths)
    finally:
        universe._design_matrix = original

    difference = float(np.abs(corrected - raw_fallback).max())
    assert difference > FALLBACK_DIFFERENCE_FLOOR, difference
    assert not np.array_equal(corrected, raw_fallback)
    assert np.array_equal(sci._neural_predict(universe, "S0", params, widths), corrected)
    assert not np.array_equal(design, universe.raw_design)
    assert float(np.abs(np.asarray(design) - universe.raw_design).max()) > 0.1


def test_evidence_block_refuses_the_issue_78_raw_fallback_state(
        fresh_universe: sci.SyntheticUniverse):
    """The runner fails closed instead of silently persisting raw-design predictions."""
    universe = fresh_universe
    design, meta = science.setup_preprocessing_state(universe)
    evidence = science.preprocessing_evidence_block(universe, design, meta)
    assert evidence["design_equality_flag"] is True
    assert evidence["zscored_differs_from_raw"] is True
    assert evidence["universe_design_matrix_sha256_before_fit"] == \
        evidence["zscored_design_sha256"]

    original = universe._design_matrix
    universe._design_matrix = None
    try:
        with pytest.raises(RuntimeError) as excinfo:
            science.preprocessing_evidence_block(universe, design, meta)
        message = str(excinfo.value)
        assert "refusing to fit" in message
        assert "#78" in message
        assert "universe._design_matrix = design" in message
    finally:
        universe._design_matrix = original


def test_array_hash_is_stable_and_design_sensitive(fresh_universe: sci.SyntheticUniverse):
    universe = fresh_universe
    design, _meta = science.setup_preprocessing_state(universe)
    assert science.array_sha256(design) == renderer.array_sha256(design)
    assert science.array_sha256(design) != science.array_sha256(universe.raw_design)
    assert len(science.array_sha256(design)) == 64
    perturbed = np.array(design, dtype=float)
    perturbed[0, 0] += 1e-12
    assert science.array_sha256(perturbed) != science.array_sha256(design)


def test_renderer_recomputes_the_design_independently(fresh_universe: sci.SyntheticUniverse):
    """The renderer must not simply call the accepted module's helper."""
    universe = fresh_universe
    design, meta = science.setup_preprocessing_state(universe)
    expected, expected_meta = renderer.expected_preprocessing_design(universe)
    assert np.array_equal(expected, design)
    assert expected_meta["zscored_design_sha256"] == science.array_sha256(design)
    assert expected_meta["zscored_design_sha256"] == meta["design_sha256"]
    assert expected_meta["raw_design_sha256"] == science.array_sha256(universe.raw_design)
    assert expected_meta["recomputation"] == "INDEPENDENT_OF_THE_ACCEPTED_MODULE_HELPER"
    assert "sci._train_only_zscore(" not in RENDERER.read_text(encoding="utf-8")


# ------------------------------------------------------- 5. durable ledger semantics
def test_ledger_append_is_durable_and_parseable(tmp_path: Path):
    ledger = tmp_path / "ledger.jsonl"
    science.append_ledger_record(ledger, {"event": "FIT_ATTEMPT_STARTED", "attempt_index": 1,
                                          "fit_key": "S0:parametric"})
    science.append_ledger_record(ledger, {"event": "FIT_COMPLETED", "attempt_index": 1,
                                          "fit_key": "S0:parametric", "runtime_seconds": 0.0})
    assert len(ledger.read_text(encoding="utf-8").splitlines()) == 2
    records = science.read_ledger(ledger)
    assert [r["event"] for r in records] == ["FIT_ATTEMPT_STARTED", "FIT_COMPLETED"]
    summary = science.ledger_summary(records)
    assert summary["started_count"] == 1 and summary["completed_count"] == 1
    assert summary["failed_count"] == 0 and summary["science_retries"] == 0
    assert summary["science_invocations"] == 1
    science.append_ledger_record(ledger, {"event": "FIT_FAILED", "attempt_index": 2})
    assert len(science.read_ledger(ledger)) == 3


def test_ledger_summary_counts_failures_and_indices(tmp_path: Path):
    ledger = tmp_path / "ledger.jsonl"
    for index in (1, 2):
        science.append_ledger_record(ledger, {"event": "FIT_ATTEMPT_STARTED",
                                              "attempt_index": index,
                                              "fit_key": f"fit{index}"})
    science.append_ledger_record(ledger, {"event": "FIT_COMPLETED", "attempt_index": 1,
                                          "fit_key": "fit1"})
    science.append_ledger_record(ledger, {"event": "FIT_FAILED", "attempt_index": 2,
                                          "fit_key": "fit2", "error_type": "RuntimeError"})
    summary = science.ledger_summary(science.read_ledger(ledger))
    assert summary["started_count"] == 2
    assert summary["completed_count"] == 1
    assert summary["failed_count"] == 1
    invariants = renderer.ledger_invariants(science.read_ledger(ledger))
    assert invariants["no_unmatched_started"] is False
    assert invariants["zero_failed"] is False


def test_refuse_science_start_when_outputs_exist(tmp_path: Path):
    ledger = tmp_path / "ledger.jsonl"
    seal = tmp_path / "seal.json"
    assert science.refuse_if_outputs_exist(ledger, seal) is None
    ledger.write_text("", encoding="utf-8")
    assert "ledger already exists" in science.refuse_if_outputs_exist(ledger, seal)
    ledger.unlink()
    seal.write_text("{}", encoding="utf-8")
    assert "science seal already exists" in science.refuse_if_outputs_exist(ledger, seal)


def test_execute_science_refuses_without_running_fits(monkeypatch, tmp_path: Path):
    calls: list[str] = []

    def explode(*args, **kwargs):  # pragma: no cover - must never be called
        calls.append("fit")
        raise AssertionError("no fit may run when the guard fires")

    monkeypatch.setattr(science, "run_one_fit", explode)
    monkeypatch.setattr(science, "ROOT", tmp_path)
    (tmp_path / science.LEDGER_RELPATH).parent.mkdir(parents=True, exist_ok=True)
    (tmp_path / science.LEDGER_RELPATH).write_text("", encoding="utf-8")
    assert science.execute_science("TESTFREEZE") == 3
    assert calls == []


# --------------------------------------------------- 6. durable payload persistence
def test_prediction_payload_round_trips_exactly(universe: sci.SyntheticUniverse):
    fixed = sci.fixed_baseline_predictions(universe, "S0")
    encoded = science.encode_predictions(fixed, universe)
    assert encoded["prediction_shape"] == [4, 5, 5]
    decoded = science.decode_predictions({
        "fit_key": "ROUNDTRIP", "predictions": encoded["predictions"],
        "prediction_shape": encoded["prediction_shape"]})
    assert np.array_equal(np.asarray(fixed, dtype=float), decoded)
    again = json.loads(json.dumps(encoded))
    assert science.decode_predictions({"fit_key": "ROUNDTRIP", **again}).tolist() == \
        np.asarray(fixed, dtype=float).tolist()


def test_encode_predictions_rejects_a_bad_tensor(universe: sci.SyntheticUniverse):
    good = sci.fixed_baseline_predictions(universe, "S0")
    with pytest.raises(ValueError):
        science.encode_predictions(np.zeros((3, 5, 5)), universe)
    bad_support = np.array(good, dtype=float)
    bad_support[0, 0, 0] = 0.25
    with pytest.raises(ValueError):
        science.encode_predictions(bad_support, universe)
    non_finite = np.array(good, dtype=float)
    non_finite[0, 0, 1] = float("nan")
    with pytest.raises(ValueError):
        science.encode_predictions(non_finite, universe)


def test_json_safe_normalizes_non_finite_values():
    safe, originals = science.json_safe({"a": float("inf"), "b": [1.0, float("nan")],
                                         "c": "text", "d": None, "e": 3})
    assert safe == {"a": None, "b": [1.0, None], "c": "text", "d": None, "e": 3}
    assert originals == {"a": "inf", "b[1]": "nan"}
    json.dumps(safe)


def test_completed_record_carries_the_complete_scientific_payload(
        fresh_universe: sci.SyntheticUniverse, config: sci.P2Config):
    universe = fresh_universe
    design, _meta = science.setup_preprocessing_state(universe)
    entry = science.build_fit_plan(config)[0]
    predictions = sci.fixed_baseline_predictions(universe, entry["regime"])
    outcome = sci.FitOutcome(
        family="parametric", regime=entry["regime"], seed=None, predictions=predictions,
        coefficients=[1.5, 0.6, -1.2, 0.3, -0.4, 0.0], objective=0.5,
        convergence={"success": True, "status": 0, "message": "dummy", "iterations": 3,
                     "function_evaluations": 4, "gradient_norm_inf": 1e-9},
        best_step=None, best_validation_loss=None, runtime_seconds=0.001, attempts=1,
        backend="TEST_BACKEND", diagnostics={"train_blocks": 9})
    record = science.build_completed_record(entry, outcome, universe, 0.001, TEST_FREEZE_SHA)
    assert record["event"] == "FIT_COMPLETED"
    assert record["attempt_index"] == 1 and record["fit_key"] == "S0:parametric"
    assert record["prediction_shape"] == [4, 5, 5]
    assert record["coefficients"] == [1.5, 0.6, -1.2, 0.3, -0.4, 0.0]
    assert record["objective"] == 0.5 and record["backend"] == "TEST_BACKEND"
    assert "best_step" in record and "best_validation_loss" in record
    assert record["preprocessing_contract"]["applies"] is False
    assert record["preprocessing_contract"]["reason"] == (
        "PARAMETRIC_PATH_USES_THE_FROZEN_CONTRAST_FITTED_MATRIX")
    assert record["payload_sha256"] == science.canonical_payload_sha256(record)
    assert renderer.canonical_payload_sha256(record) == record["payload_sha256"]
    json.dumps(record, sort_keys=True)
    assert record["payload_sha256"] == science.canonical_payload_sha256(
        {**record, "recorded_utc": "1999-01-01T00:00:00+00:00", "runtime_seconds": 99.0,
         "pre_run_freeze_sha": "OTHER"})
    assert design is universe._design_matrix


def test_neural_completed_record_carries_the_preprocessing_contract(
        fresh_universe: sci.SyntheticUniverse, config: sci.P2Config):
    universe = fresh_universe
    design, meta = science.setup_preprocessing_state(universe)
    entry = [e for e in science.build_fit_plan(config)
             if e["family"] == "neural" and e["kind"] == "primary"][0]
    evidence = science.preprocessing_evidence_block(universe, design, meta)
    outcome = sci.FitOutcome(
        family="neural", regime=entry["regime"], seed=entry["seed"],
        predictions=sci.fixed_baseline_predictions(universe, entry["regime"]),
        coefficients=None, objective=1.25,
        convergence={"early_stopped": True, "final_step": 400}, best_step=350,
        best_validation_loss=1.2, runtime_seconds=0.01, attempts=1,
        backend="numpy-adam-full-batch", diagnostics={"hidden_widths": [16, 8]})
    record = science.build_completed_record(entry, outcome, universe, 0.01, TEST_FREEZE_SHA,
                                            evidence)
    contract = record["preprocessing_contract"]
    assert contract["applies"] is True
    assert contract["training_design"] == "TRAIN_ONLY_ZSCORED"
    assert contract["prediction_design"] == "TRAIN_ONLY_ZSCORED"
    assert contract["required_assignment"] == "universe._design_matrix = design"
    assert contract["design_equality_flag"] is True
    assert contract["zscored_design_sha256"] == contract[
        "universe_design_matrix_sha256_before_fit"]
    assert contract["raw_design_sha256"] == science.array_sha256(universe.raw_design)
    assert contract["zscored_differs_from_raw"] is True
    assert contract["design_shape"] == [72, 15]
    assert contract["raw_design_shape"] == [72, 15]
    assert contract["train_row_count"] == 36
    assert contract["design_max_abs_difference_from_raw"] > 0.1
    assert record["payload_sha256"] == science.canonical_payload_sha256(record)
    assert renderer.canonical_payload_sha256(record) == record["payload_sha256"]


def test_payload_hash_is_sensitive_to_scientific_content(
        fresh_universe: sci.SyntheticUniverse, config: sci.P2Config):
    universe = fresh_universe
    design, meta = science.setup_preprocessing_state(universe)
    entry = science.build_fit_plan(config)[0]
    base = sci.FitOutcome(
        family="parametric", regime="S0", seed=None,
        predictions=sci.fixed_baseline_predictions(universe, "S0"),
        coefficients=[0.0] * 6, objective=1.0, convergence={"success": True},
        best_step=None, best_validation_loss=None, runtime_seconds=0.0, attempts=1,
        backend="B", diagnostics={})
    first = science.build_completed_record(entry, base, universe, 0.0, TEST_FREEZE_SHA)
    perturbed = np.array(base.predictions, dtype=float)
    perturbed[0, 0, 1] += 1e-9
    second = science.build_completed_record(
        entry, replace(base, predictions=perturbed), universe, 0.0, TEST_FREEZE_SHA)
    assert first["payload_sha256"] != second["payload_sha256"]
    assert design is universe._design_matrix and meta["design_sha256"]


# ------------------------------------------- 7. fake 12-fit ledger (production render)
def _blended_predictions(universe: sci.SyntheticUniverse, regime: str,
                         target_weight: float) -> np.ndarray:
    out = np.zeros_like(universe.targets[regime])
    for block in universe.blocks:
        n = len(block.allowed)
        raw = [target_weight * universe.targets[regime][block.time_index, block.origin, j]
               + (1.0 - target_weight) / n for j in block.allowed]
        total = sum(raw)
        for pos, j in enumerate(block.allowed):
            out[block.time_index, block.origin, j] = raw[pos] / total
    return out


def _fake_outcome(universe: sci.SyntheticUniverse, entry: dict[str, Any]) -> sci.FitOutcome:
    family, regime, seed = entry["family"], entry["regime"], entry["seed"]
    if family == "parametric":
        weight = 0.70 if regime == "S0" else 0.65
        coefficients = ([1.5, 0.6, -1.2, 0.3, -0.4, 0.0] if regime == "S0"
                        else [1.4, 0.5, -1.1, 0.25, -0.35, 0.0])
        return sci.FitOutcome(
            family="parametric", regime=regime, seed=None,
            predictions=_blended_predictions(universe, regime, weight),
            coefficients=coefficients, objective=0.5123 if regime == "S0" else 0.4987,
            convergence={"success": True, "status": 0, "message": "FAKE_CONVERGED",
                         "iterations": 12, "function_evaluations": 20,
                         "gradient_norm_inf": 1e-11},
            best_step=None, best_validation_loss=None, runtime_seconds=0.004, attempts=1,
            backend="scipy.optimize.minimize:L-BFGS-B",
            diagnostics={"fitted_columns": list(universe.config.fitted_columns),
                         "train_blocks": 9, "fake": True})
    weight = (0.60 if regime == "S0" else 0.55) + 0.02 * int(seed)
    return sci.FitOutcome(
        family="neural", regime=regime, seed=int(seed),
        predictions=_blended_predictions(universe, regime, weight), coefficients=None,
        objective=0.7 + 0.01 * int(seed),
        convergence={"early_stopped": True, "final_step": 400},
        best_step=350, best_validation_loss=0.72,
        runtime_seconds=0.02, attempts=1, backend="numpy-adam-full-batch",
        diagnostics={"hidden_widths": [16, 8], "activations": ["ReLU", "Tanh"],
                     "steps_executed": 400, "learning_rate": 0.01,
                     "history": [{"step": 50, "train_loss": 0.9, "validation_loss": 0.8}],
                     "train_weighted_cross_entropy": 0.7 + 0.01 * int(seed), "fake": True})


def write_fake_ledger(universe: sci.SyntheticUniverse, path: Path,
                      *, with_seal: bool = True,
                      freeze_sha: str = TEST_FREEZE_SHA,
                      tamper: str | None = None) -> Path:
    """Build a complete synthetic 12-fit durable ledger through the production writers.

    ``tamper`` optionally breaks the FIRST neural completed record's preprocessing
    contract: ``"drop_contract"`` removes it, ``"flag_false"`` flips the equality flag,
    ``"wrong_hash"`` corrupts the recorded z-scored digest. The payload digest is
    recomputed afterwards so only the preprocessing gate can fail.
    """
    design, meta = science.setup_preprocessing_state(universe)
    plan = science.build_fit_plan(universe.config)
    clock = datetime(2026, 9, 19, 0, 0, 0, tzinfo=timezone.utc)
    step = timedelta(seconds=1)
    tampered_once = False
    for entry in plan:
        if entry["family"] == "neural":
            contract: dict[str, Any] = science.preprocessing_evidence_block(
                universe, design, meta)
        else:
            contract = science.parametric_preprocessing_block()
        science.append_ledger_record(path, {
            "event": "FIT_ATTEMPT_STARTED", "recorded_utc": clock.isoformat(),
            "attempt_index": entry["attempt_index"], "planned_attempts": 12,
            "kind": entry["kind"], "family": entry["family"], "regime": entry["regime"],
            "seed": entry["seed"], "fit_key": entry["fit_key"],
            "repeat_of": entry["repeat_of"], "pre_run_freeze_sha": freeze_sha,
            "started_monotonic_seconds": float(entry["attempt_index"]),
            "training_design": contract["training_design"],
            "prediction_design": contract["prediction_design"],
            "design_equality_flag": contract.get("design_equality_flag"),
        })
        clock += step
        outcome = _fake_outcome(universe, entry)
        record = science.build_completed_record(entry, outcome, universe,
                                                outcome.runtime_seconds, freeze_sha,
                                                contract)
        record["recorded_utc"] = clock.isoformat()
        if entry["family"] == "neural" and tamper and not tampered_once:
            tampered_once = True
            if tamper == "drop_contract":
                record.pop("preprocessing_contract", None)
            elif tamper == "flag_false":
                record["preprocessing_contract"]["design_equality_flag"] = False
            elif tamper == "wrong_hash":
                record["preprocessing_contract"]["zscored_design_sha256"] = "0" * 64
            record["payload_sha256"] = science.canonical_payload_sha256(record)
        science.append_ledger_record(path, record)
        clock += step
    if with_seal:
        science.write_json_durable(path.parent / science.SEAL_RELPATH.split("/")[-1], {
            "phase": "SCIENCE_STAGE_SEAL", "pre_run_freeze_sha": freeze_sha,
            "science_invocations": 1, "science_retries": 0,
            "started_count": 12, "completed_count": 12, "failed_count": 0,
            "science_wall_clock_seconds": 42.5,
            "science_wall_clock_ceiling_seconds": 1800.0,
            "ledger_relpath": science.LEDGER_RELPATH,
            "scientific_module_blob_sha1": science.EXPECTED_SCIENTIFIC_MODULE_BLOB,
            "terminal": science.TERMINAL_PASS,
        })
    return path


@pytest.fixture
def fake_ledger(fresh_universe: sci.SyntheticUniverse, tmp_path: Path) -> Path:
    return write_fake_ledger(fresh_universe, tmp_path / renderer.LEDGER_NAME)


@pytest.fixture
def no_fitters(monkeypatch):
    """Every fitting/optimizer entry point becomes an exploding tripwire.

    ``sci._train_only_zscore`` is deliberately **not** in this set: it is a pure
    preprocessing helper with no optimizer, the ledger fixture legitimately needs it, and
    the renderer's freedom from it is enforced separately by
    ``test_renderer_recomputes_the_design_independently`` (source-level assertion plus the
    AST guard below).
    """
    calls: list[str] = []

    def tripwire(name: str):
        def explode(*args, **kwargs):  # pragma: no cover - must never be called
            calls.append(name)
            raise AssertionError(f"{name} must never be called by the render stage")
        return explode

    for name in ("fit_parametric", "fit_neural", "run_scientific_program"):
        monkeypatch.setattr(sci, name, tripwire(name))
    for name in ("_adam_step", "_backward", "_forward", "_init_mlp",
                 "_softmax_cross_entropy", "_masked_softmax"):
        monkeypatch.setattr(sci, name, tripwire(name), raising=False)
    return calls


def test_fake_ledger_has_twelve_started_and_twelve_completed(fake_ledger: Path):
    records = science.read_ledger(fake_ledger)
    invariants = renderer.ledger_invariants(records)
    assert invariants["records"] == 24
    assert invariants["started_count"] == 12 and invariants["completed_count"] == 12
    assert invariants["failed_count"] == 0
    assert invariants["started_indices_are_exactly_1_to_12"] is True
    assert invariants["completed_indices_are_exactly_1_to_12"] is True
    assert invariants["started_before_completed_ordering_ok"] is True


def test_fake_ledger_neural_records_carry_full_preprocessing_evidence(fake_ledger: Path):
    completed = renderer.completed_records(science.read_ledger(fake_ledger))
    neural = [r for r in completed if r["family"] == "neural"]
    parametric = [r for r in completed if r["family"] == "parametric"]
    assert len(neural) == 8 and len(parametric) == 4
    for record in neural:
        contract = record["preprocessing_contract"]
        assert contract["applies"] is True
        assert contract["training_design"] == "TRAIN_ONLY_ZSCORED"
        assert contract["prediction_design"] == "TRAIN_ONLY_ZSCORED"
        assert contract["design_equality_flag"] is True
        assert contract["zscored_design_sha256"] == contract[
            "universe_design_matrix_sha256_before_fit"]
        assert contract["zscored_differs_from_raw"] is True
        assert renderer.decode_predictions(record).shape == (4, 5, 5)
    checks = renderer.payload_hash_verification(completed)
    assert checks["all_payload_hashes_match"] is True
    assert checks["all_prediction_shapes_frozen"] is True
    assert checks["all_metadata_present"] is True


def test_preprocessing_contract_check_passes_on_the_fake_ledger(
        fresh_universe: sci.SyntheticUniverse, fake_ledger: Path):
    universe = fresh_universe
    completed = renderer.completed_records(science.read_ledger(fake_ledger))
    check = renderer.preprocessing_contract_check(universe, completed)
    summary = check["summary"]
    assert summary["neural_fits_examined"] == 8
    assert summary["all_neural_fits_covered"] is True
    assert summary["every_neural_fit_carries_preprocessing_contract"] is True
    assert summary["every_neural_contract_satisfied"] is True
    assert summary[
        "training_and_prediction_design_hashes_identical_for_all_neural_fits"] is True
    assert summary[
        "zscored_design_matches_frozen_recomputation_for_all_neural_fits"] is True
    assert summary["zscored_design_differs_from_raw_for_all_neural_fits"] is True
    for key, row in check["per_fit"].items():
        assert row["contract_satisfied"] is True, key
        assert row["zscored_design_sha256"] == row["expected_zscored_design_sha256"]
        assert row["raw_design_sha256"] == row["expected_raw_design_sha256"]


def test_aggregate_metrics_output_shape_is_the_constraint_input_contract(
        fresh_universe: sci.SyntheticUniverse, fake_ledger: Path):
    universe = fresh_universe
    completed = renderer.completed_records(science.read_ledger(fake_ledger))
    aggregated = renderer.aggregate_metrics(universe, completed)
    assert set(aggregated) == set(renderer.PRIMARY_FIT_KEYS) | {
        repeat for _, repeat in renderer.REPEAT_PAIRS}
    for key, entry in aggregated.items():
        assert set(entry["metrics"]) == set(renderer.SPLIT_STATES), key
        assert entry["prediction_source"] == "PERSISTED_FIT_COMPLETED_PREDICTIONS"
    fixed = renderer.fixed_baseline_metrics(universe)
    constraints = renderer.constraint_diagnostics(universe, aggregated, fixed)
    assert constraints["evaluated_prediction_sets"] == 14
    assert constraints["row_normalization_ok"] is True
    assert constraints["support_ok"] is True
    assert constraints["excluded_block_count"] == 6


def test_constraint_diagnostics_rejects_the_issue_77_input_shape(
        fresh_universe: sci.SyntheticUniverse, fake_ledger: Path):
    universe = fresh_universe
    completed = renderer.completed_records(science.read_ledger(fake_ledger))
    good = renderer.aggregate_metrics(universe, completed)
    fixed = renderer.fixed_baseline_metrics(universe)
    legacy_shape = {key: good[key]["metrics"] for key in renderer.PRIMARY_FIT_KEYS}
    with pytest.raises(TypeError) as excinfo:
        renderer.constraint_diagnostics(universe, legacy_shape, fixed)
    assert "Issue #77" in str(excinfo.value)
    with pytest.raises(KeyError):
        renderer.constraint_diagnostics(universe, {}, fixed)
    assert renderer.constraint_diagnostics(universe, good, fixed)[
        "row_normalization_ok"] is True


def test_determinism_uses_fake_repeated_predictions(
        fresh_universe: sci.SyntheticUniverse, fake_ledger: Path):
    universe = fresh_universe
    completed = renderer.completed_records(science.read_ledger(fake_ledger))
    by_key = {r["fit_key"]: r for r in completed}
    determinism = renderer.determinism_comparisons(universe, by_key)
    for name in renderer.DETERMINISM_NAMES:
        assert determinism[name]["deviation"] == 0.0, name
    assert determinism["all_within_tolerance"] is True
    assert determinism["max_deviation"] == 0.0
    tampered = dict(by_key)
    tampered["S0:neural:seed0:repeat"] = dict(by_key["S0:neural:seed0:repeat"])
    tensor = renderer.decode_predictions(tampered["S0:neural:seed0:repeat"])
    tensor[0, 0, 1] += 1e-6
    tampered["S0:neural:seed0:repeat"]["predictions"] = tensor.tolist()
    detected = renderer.determinism_comparisons(universe, tampered)
    assert detected["neural_S0_seed0"]["deviation"] > 1e-12
    assert detected["all_within_tolerance"] is False


def test_share_distribution_check_reads_the_recovery_object(
        fresh_universe: sci.SyntheticUniverse, fake_ledger: Path):
    universe = fresh_universe
    completed = renderer.completed_records(science.read_ledger(fake_ledger))
    shares = renderer.share_distribution_check(universe, completed)
    assert len(shares["per_fit"]) == 12
    assert shares["all_valid"] is True


def test_fake_ledger_renders_end_to_end_with_zero_fits(
        fake_ledger: Path, tmp_path: Path, no_fitters, capsys):
    """THE mandatory gate: the exact production path, end to end, zero fits."""
    exit_code = renderer.render(repo_root=ROOT, ledger_path=fake_ledger,
                                seal_path=tmp_path / renderer.SEAL_NAME, outdir=tmp_path)
    assert no_fitters == [], f"the render stage called a fitter: {no_fitters}"
    assert exit_code == 0
    stdout = json.loads(capsys.readouterr().out)
    assert stdout["fits"] == 0 and stdout["optimizer_steps"] == 0
    assert stdout["metrics_computed_from"] == "PERSISTED_LEDGER_PREDICTIONS_ONLY"
    assert stdout["preprocessing_contract_satisfied"] is True
    assert stdout["gate_ok"] is True
    assert stdout["terminal"] == renderer.TERMINAL_PASS
    assert stdout["all_checks_pass"] is True

    for name in (renderer.RAW_NAME, renderer.RESULTS_NAME, renderer.MANIFEST_NAME,
                 renderer.REPORT_NAME):
        assert (tmp_path / name).is_file(), name
    raw = json.loads((tmp_path / renderer.RAW_NAME).read_text(encoding="utf-8"))
    results = json.loads((tmp_path / renderer.RESULTS_NAME).read_text(encoding="utf-8"))
    manifest = json.loads((tmp_path / renderer.MANIFEST_NAME).read_text(encoding="utf-8"))
    report = (tmp_path / renderer.REPORT_NAME).read_text(encoding="utf-8")

    assert set(results["metrics_by_split"]) == set(renderer.PRIMARY_FIT_KEYS) | {
        repeat for _, repeat in renderer.REPEAT_PAIRS}
    for key, by_split in results["metrics_by_split"].items():
        assert set(by_split) == set(renderer.SPLIT_STATES), key
        assert by_split["TEST"]["evaluated_cells"] == 6
        assert by_split["TRAIN"]["evaluated_cells"] == 36
        assert by_split["VALIDATION"]["evaluated_cells"] == 12
        assert by_split["EXCLUDED_REFERENCE_ONLY"]["evaluated_cells"] == 18
    assert results["determinism"]["all_within_tolerance"] is True
    constraints = results["constraint_diagnostics"]
    assert constraints["row_normalization_ok"] is True
    assert constraints["negativity_ok"] is True
    assert constraints["support_ok"] is True
    assert constraints["split_counts"] == {"TRAIN": 9, "VALIDATION": 3, "TEST": 2,
                                          "EXCLUDED_REFERENCE_ONLY": 6}
    assert results["p1a_accounting_checks"]["closes"] is True
    assert results["share_distribution_check"]["all_valid"] is True
    assert results["payload_hash_verification"]["all_payload_hashes_match"] is True
    assert results["attempt_ledger_summary"]["started_count"] == 12
    assert results["attempt_ledger_summary"]["completed_count"] == 12
    assert results["render_only_invocations"] == 1
    assert results["confirmatory_p2_pass_allowed"] is True
    assert all(results["acceptance_gate_checks"].values()), [
        k for k, v in results["acceptance_gate_checks"].items() if not v]

    verification = results["preprocessing_contract_verification"]
    assert verification["summary"]["every_neural_contract_satisfied"] is True
    assert verification["summary"][
        "training_and_prediction_design_hashes_identical_for_all_neural_fits"] is True
    assert verification["summary"][
        "zscored_design_differs_from_raw_for_all_neural_fits"] is True
    assert verification["expected_design"]["zscored_design_sha256"] != \
        verification["expected_design"]["raw_design_sha256"]
    assert "TRAIN_ONLY_ZSCORED" in report
    assert verification["expected_design"]["zscored_design_sha256"] in report
    assert verification["expected_design"]["raw_design_sha256"] in report
    assert raw["preprocessing_contract_checks"]["every_neural_contract_satisfied"] is True
    assert manifest["preprocessing_contract_verification"]["summary"][
        "every_neural_contract_satisfied"] is True
    assert manifest["declarations"]["renderer_calls_any_fitter"] is False
    assert manifest["declarations"]["universe_design_matrix_installed_by_renderer"] is False
    assert manifest["science_protocol"]["fits_performed_by_renderer"] == 0
    assert manifest["science_protocol"]["optimizer_steps_performed_by_renderer"] == 0

    import hashlib

    core = {k: v for k, v in results.items()
            if k not in (renderer.RESULTS_DIGEST_FIELD, renderer.MANIFEST_DIGEST_FIELD)}
    assert results[renderer.RESULTS_DIGEST_FIELD] == \
        hashlib.sha256(renderer.dumps(core)).hexdigest().upper()
    assert results[renderer.MANIFEST_DIGEST_FIELD] == \
        hashlib.sha256(renderer.dumps(manifest)).hexdigest().upper()
    assert manifest["terminal"] == results["terminal"] == renderer.TERMINAL_PASS


@pytest.mark.parametrize("tamper,expected_failed_check", [
    ("drop_contract", "every_neural_fit_carries_preprocessing_contract"),
    ("flag_false", "every_neural_contract_satisfied"),
    ("wrong_hash", "zscored_design_matches_frozen_recomputation"),
])
def test_render_gate_fails_on_a_broken_preprocessing_contract(
        fresh_universe: sci.SyntheticUniverse, tmp_path: Path, no_fitters, capsys,
        tamper: str, expected_failed_check: str):
    """The preprocessing gate must bite: it is what makes P2D different from #78."""
    ledger = write_fake_ledger(fresh_universe, tmp_path / renderer.LEDGER_NAME,
                               tamper=tamper)
    exit_code = renderer.render(repo_root=ROOT, ledger_path=ledger,
                                seal_path=tmp_path / renderer.SEAL_NAME, outdir=tmp_path)
    assert no_fitters == []
    assert exit_code == 2
    stdout = json.loads(capsys.readouterr().out)
    assert stdout["gate_ok"] is False
    assert stdout["terminal"] == renderer.TERMINAL_GATE_FAIL
    assert stdout["preprocessing_contract_satisfied"] is False
    assert stdout["gate_checks"][expected_failed_check] is False
    results = json.loads((tmp_path / renderer.RESULTS_NAME).read_text(encoding="utf-8"))
    assert results["confirmatory_p2_pass_allowed"] is False
    assert results["terminal"] == renderer.TERMINAL_GATE_FAIL


def test_renderer_never_installs_the_design_matrix(
        fake_ledger: Path, tmp_path: Path, no_fitters, capsys):
    """Rendering is zero-fit and must not mutate preprocessing state either."""
    observed: list[Any] = []
    original = renderer.expected_preprocessing_design

    def spy(universe):
        design, meta = original(universe)
        observed.append(universe._design_matrix)
        return design, meta

    renderer.expected_preprocessing_design = spy  # type: ignore[assignment]
    try:
        exit_code = renderer.render(repo_root=ROOT, ledger_path=fake_ledger,
                                    seal_path=tmp_path / renderer.SEAL_NAME, outdir=tmp_path)
    finally:
        renderer.expected_preprocessing_design = original  # type: ignore[assignment]
    assert exit_code == 0
    assert no_fitters == []
    assert observed == [None], "the renderer must not install a design matrix"
    capsys.readouterr()


def test_render_is_idempotent_and_increments_the_render_counter(
        fake_ledger: Path, tmp_path: Path, no_fitters, capsys):
    first = renderer.render(repo_root=ROOT, ledger_path=fake_ledger,
                            seal_path=tmp_path / renderer.SEAL_NAME, outdir=tmp_path)
    assert first == 0
    capsys.readouterr()
    before = json.loads((tmp_path / renderer.RESULTS_NAME).read_text(encoding="utf-8"))
    second = renderer.render(repo_root=ROOT, ledger_path=fake_ledger,
                             seal_path=tmp_path / renderer.SEAL_NAME, outdir=tmp_path)
    assert second == 0
    capsys.readouterr()
    after = json.loads((tmp_path / renderer.RESULTS_NAME).read_text(encoding="utf-8"))
    assert no_fitters == []
    assert after["render_only_invocations"] == before["render_only_invocations"] + 1
    assert after["metrics_by_split"] == before["metrics_by_split"]
    assert after["preprocessing_contract_verification"] == \
        before["preprocessing_contract_verification"]


def test_render_refuses_without_a_ledger(tmp_path: Path, no_fitters, capsys):
    exit_code = renderer.render(repo_root=ROOT, ledger_path=tmp_path / "absent.jsonl",
                                outdir=tmp_path)
    assert exit_code == 3
    assert no_fitters == []
    payload = json.loads(capsys.readouterr().out)
    assert payload["terminal"] == renderer.TERMINAL_BLOCKED
    assert payload["fits"] == 0 and payload["optimizer_steps"] == 0
    assert not (tmp_path / renderer.RESULTS_NAME).exists()


def test_render_derives_the_wall_clock_from_the_ledger_when_the_seal_is_absent(
        fresh_universe: sci.SyntheticUniverse, tmp_path: Path, no_fitters, capsys):
    ledger = write_fake_ledger(fresh_universe, tmp_path / renderer.LEDGER_NAME,
                               with_seal=False)
    exit_code = renderer.render(repo_root=ROOT, ledger_path=ledger,
                                seal_path=tmp_path / renderer.SEAL_NAME, outdir=tmp_path)
    assert exit_code == 0
    capsys.readouterr()
    results = json.loads((tmp_path / renderer.RESULTS_NAME).read_text(encoding="utf-8"))
    clock = results["science_wall_clock"]
    assert clock["wall_clock_source"] == "DERIVED_FROM_LEDGER_RECORDED_UTC"
    assert clock["within_ceiling"] is True
    assert clock["seal_present"] is False


# ------------------------------------------------- 8. render-only cannot fit
FORBIDDEN_CALLS = ("fit_parametric", "fit_neural", "run_scientific_program", "_adam_step",
                   "_backward", "_forward", "_init_mlp", "_train_only_zscore",
                   "_softmax_cross_entropy", "minimize")


def test_renderer_never_references_fitting_entry_points():
    tree = ast.parse(RENDERER.read_text(encoding="utf-8"))
    calls: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name):
                calls.add(func.id)
            elif isinstance(func, ast.Attribute):
                calls.add(func.attr)
    for forbidden in FORBIDDEN_CALLS:
        assert forbidden not in calls, forbidden
    assert renderer._calls_any_fitter() is False


def test_renderer_cannot_reach_a_fitter_even_via_attribute_access():
    tree = ast.parse(RENDERER.read_text(encoding="utf-8"))
    attributes: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute):
            attributes.add(node.attr)
    for forbidden in ("fit_parametric", "fit_neural", "run_scientific_program"):
        assert forbidden not in attributes, forbidden


def test_renderer_validate_only_reports_zero_fits(capsys):
    assert renderer.main(["--validate-only"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["optimizer_steps_performed"] == 0
    assert payload["fit_attempts_performed"] == 0
    assert payload["renderer_imports_fitters"] is False
    assert payload["metrics_computed_from"] == "DURABLE_LEDGER_PERSISTED_PREDICTIONS_ONLY"


def test_science_runner_validate_only_proves_the_preprocessing_state(capsys):
    assert science.validate_only() == 0
    out = capsys.readouterr().out
    assert "VALIDATE_ONLY_COMPLETE__ZERO_OPTIMIZER_STEPS__ZERO_FITS" in out
    payload = json.loads(out.split("VALIDATE_ONLY_COMPLETE")[0])
    assert payload["optimizer_steps_performed"] == 0
    assert payload["fit_attempts_performed"] == 0
    assert payload["module_blob_status"] == "MATCH"
    assert payload["config_blob_status"] == "MATCH"
    assert payload["planned_fit_attempts"] == 12
    assert payload["prediction_tensor_shape"] == [4, 5, 5]
    assert payload["prediction_roundtrip_exact"] is True
    assert payload["payload_hash_verifies"] is True
    assert payload["primary_fit_keys"] == list(renderer.PRIMARY_FIT_KEYS)
    assert payload["repeat_pairs"] == [list(pair) for pair in renderer.REPEAT_PAIRS]
    assert payload["design_matrix_unset_before_setup"] is True
    assert payload["preprocessing_assignment_performed"] == \
        "universe._design_matrix = design"
    assert payload["design_installed_equals_zscored_design"] is True
    assert payload["design_matrix_is_not_raw_fallback"] is True
    assert payload["training_design"] == "TRAIN_ONLY_ZSCORED"
    assert payload["prediction_design"] == "TRAIN_ONLY_ZSCORED"
    assert payload["design_equality_flag"] is True
    assert payload["zscored_differs_from_raw"] is True
    assert payload["zscored_design_sha256"] == payload["before_fit_design_sha256"]
    assert payload["zscored_design_sha256"] != payload["raw_design_sha256"]


def test_science_runner_cli_requires_a_mode():
    with pytest.raises(SystemExit):
        science.main([])


# ------------------------------------------------- 9. static import / content guards
def test_no_forbidden_scientific_imports():
    for path in (SCIENCE_RUNNER, RENDERER):
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
            assert name != "deep_learning_hank.household", (path, name)
    text = SCIENCE_RUNNER.read_text(encoding="utf-8")
    for symbol in ("solve_household_steady_state", "solve_matlab_faithful_hjb",
                   "BoundaryHJBSolver", "matlab_contaminated_row_index"):
        assert symbol not in text


def test_science_runner_performs_the_authorized_assignment_before_fitting():
    """Static proof that the Issue #79 repair is in the executed science path."""
    text = SCIENCE_RUNNER.read_text(encoding="utf-8")
    assert "universe._design_matrix = design" in text
    tree = ast.parse(text)
    assignment_lines: list[int] = []
    for node in ast.walk(tree):
        targets: list[Any] = []
        if isinstance(node, ast.Assign):
            targets = list(node.targets)
        elif isinstance(node, ast.AnnAssign) and node.value is not None:
            targets = [node.target]
        for target in targets:
            for sub in ast.walk(target):
                if isinstance(sub, ast.Attribute) and sub.attr == "_design_matrix":
                    assignment_lines.append(node.lineno)
    assert assignment_lines, "the runner must assign universe._design_matrix"
    assert "setup_preprocessing_state" in text
    assert "setup_preprocessing_state(universe)" in text
    assert 'sci._train_only_zscore(universe, universe.blocks_for("TRAIN"))' not in text


def test_renderer_declares_the_zero_fit_contract():
    text = RENDERER.read_text(encoding="utf-8")
    assert "zero fits" in text
    assert "zero optimizer steps" in text
    assert "never trains" in text
    assert renderer.MANIFEST_DIGEST_FIELD in text and renderer.RESULTS_DIGEST_FIELD in text
    assert "zero_fit_recovery" in text
    assert renderer.ZERO_FIT_STATEMENT.split(".")[0] in text
    assert "authoritative zero-fit recovery object" in text


def test_rendered_artifact_schema_expectations():
    text = RENDERER.read_text(encoding="utf-8")
    for emitted in ("metrics_by_split", "fixed_baseline_metrics", "fit_summaries",
                    "determinism", "constraint_diagnostics", "p1a_accounting_checks",
                    "acceptance_gate_checks", "audit_context_vs_issue_76",
                    "interpretation_ceiling", "negative_result_flags",
                    "payload_hash_verification", "share_distribution_check",
                    "aggregation_contract", "zero_fit_recovery", "artifact_hashes",
                    "provenance_chain", "declarations", "render_only_invocations",
                    "preprocessing_contract_verification", "metric_provenance"):
        assert emitted in text, emitted
    science_text = SCIENCE_RUNNER.read_text(encoding="utf-8")
    for emitted in ("FIT_ATTEMPT_STARTED", "FIT_COMPLETED", "FIT_FAILED", "payload_sha256",
                    "prediction_shape", "non_finite_originals", "PAYLOAD_SCIENTIFIC_KEYS",
                    "payload_canonicalization", "preprocessing_contract",
                    "zscored_design_sha256", "raw_design_sha256", "design_equality_flag",
                    "zscored_differs_from_raw"):
        assert emitted in science_text, emitted


def test_science_writes_only_the_ledger_and_the_seal():
    text = SCIENCE_RUNNER.read_text(encoding="utf-8")
    assert "RAW_RESULTS" not in text
    assert "RESULTS_RELPATH" not in text
    assert "MANIFEST_RELPATH" not in text
    assert "REPORT_RELPATH" not in text
    assert "no metric" in text.lower()
    assert science.LEDGER_RELPATH == (
        "reports/dlh_wl_p2d_2026_09_19/DLH_WL_P2D_ATTEMPT_LEDGER.jsonl")
    assert science.SEAL_RELPATH == (
        "reports/dlh_wl_p2d_2026_09_19/DLH_WL_P2D_SCIENCE_SEAL.json")
    assert renderer.RAW_RELPATH == (
        "reports/dlh_wl_p2d_2026_09_19/DLH_WL_P2D_RAW_RESULTS.json")
    assert renderer.RESULTS_RELPATH == (
        "reports/dlh_wl_p2d_2026_09_19/DLH_WL_P2D_RESULTS.json")
    assert renderer.MANIFEST_RELPATH == (
        "reports/dlh_wl_p2d_2026_09_19/DLH_WL_P2D_MANIFEST.json")
    assert renderer.REPORT_RELPATH == (
        "reports/dlh_wl_p2d_2026_09_19/DLH_WL_P2D_REPORT.md")


def test_science_stage_has_not_been_run_twice_against_the_repository():
    ledger = ROOT / science.LEDGER_RELPATH
    seal = ROOT / science.SEAL_RELPATH
    if not ledger.exists():
        assert not seal.exists()
        assert science.refuse_if_outputs_exist(ledger, seal) is None
    else:
        invariants = renderer.ledger_invariants(science.read_ledger(ledger))
        assert invariants["records"] == 24
        assert invariants["started_count"] == 12
        assert invariants["completed_count"] == 12
        assert invariants["science_invocations"] == 1
        assert invariants["science_retries"] == 0
