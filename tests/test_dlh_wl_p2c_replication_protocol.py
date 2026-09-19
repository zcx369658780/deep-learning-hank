"""DLH-WL-P2C — focused pre-run protocol tests (Issue #78).

Zero optimizer steps, zero fits, zero training. The tests exercise:

* frozen identity (config revision, blobs, plan, ceilings, terminals);
* durable ledger append/fsync semantics and the fail-closed guards;
* the JSON-safe completed-record persistence format carrying actual-shape 4x5x5
  prediction tensors plus a canonical scientific-payload SHA-256;
* the **mandatory zero-fit recovery gate**: a synthetic fake 12-fit ledger
  (12 STARTED + 12 COMPLETED with real-shape tensors and dummy coefficients) is driven
  end-to-end through the exact production aggregation/render path, producing metrics,
  determinism diagnostics, constraint diagnostics and all four rendered artifacts in a
  temporary directory while the fitters are patched to explode;
* the aggregation input-shape contract that Issue #77 violated silently;
* static/AST guards proving the renderer can never reach a fitter or optimizer.

Authority: Issue #78 ``DLH-WL-P2C``; activation comment ``5740416535``; marker
``DLH_WL_P2C_DURABLE_PER_FIT_OUTPUT_REPLICATION_AUTHORIZED``.
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

import run_dlh_wl_p2c_replication_science as science  # noqa: E402
import render_dlh_wl_p2c_replication as renderer  # noqa: E402
from deep_learning_hank.regional import labor_destination_p2 as sci  # noqa: E402

CONFIG_PATH = ROOT / science.CONFIG_RELPATH
MODULE_PATH = ROOT / science.SCIENTIFIC_MODULE_RELPATH
SCIENCE_RUNNER = ROOT / renderer.SCIENCE_RUNNER_RELPATH
RENDERER = ROOT / renderer.RENDERER_RELPATH
TEST_FREEZE_SHA = "TEST_FREEZE_SHA_NOT_A_REAL_COMMIT"
FROZEN_S0_R00_T1 = [0.477725159, 0.221843778, 0.164194930, 0.136236133]
FROZEN_S1_R04_T4 = [0.151139135, 0.195055970, 0.653804895]


@pytest.fixture(scope="module")
def config() -> sci.P2Config:
    return sci.load_frozen_config(ROOT, config_relpath=science.CONFIG_RELPATH)


@pytest.fixture(scope="module")
def universe(config: sci.P2Config) -> sci.SyntheticUniverse:
    return sci.build_universe(config, ROOT)


# ------------------------------------------------------- 1. authority and identity
def test_issue_authority_constants():
    assert science.PLANNED_FIT_ATTEMPTS == 12
    assert science.SCIENCE_WALL_CLOCK_CEILING_SECONDS == 1800.0
    assert science.EXPERIMENT_ID == "EXP-20260919-DLH-WL-P2C-001"
    assert science.TERMINAL_PASS == (
        "DLH_WL_P2C_DURABLE_OUTPUT_REPLICATION__PASS__P2_METHOD_GATE_COMPLETE")
    assert science.TERMINAL_GATE_FAIL == (
        "DLH_WL_P2C_DURABLE_OUTPUT_REPLICATION__GATE_FAIL__NO_SCIENCE_RERUN_AUTHORIZED")
    assert science.TERMINAL_BLOCKED == "BLOCKED_DLH_WL_P2C_PRE_RUN_OR_ENVIRONMENT"
    assert renderer.TERMINAL_PASS == science.TERMINAL_PASS
    assert renderer.TERMINAL_GATE_FAIL == science.TERMINAL_GATE_FAIL
    assert renderer.TERMINAL_BLOCKED == science.TERMINAL_BLOCKED
    assert science.ROUTE == "DLH-WL-V1-20260918"
    assert science.AUTHORITY_MARKER == (
        "DLH_WL_P2C_DURABLE_PER_FIT_OUTPUT_REPLICATION_AUTHORIZED")


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


# ------------------------------------------------------- 4. durable ledger semantics
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
    # append never truncates: a rerun would add to the same durable file
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
    """The guard must fire before any fit; the fit function is patched to explode."""
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


# --------------------------------------------------- 5. durable payload persistence
def test_prediction_payload_round_trips_exactly(universe: sci.SyntheticUniverse):
    fixed = sci.fixed_baseline_predictions(universe, "S0")
    encoded = science.encode_predictions(fixed, universe)
    assert encoded["prediction_shape"] == [4, 5, 5]
    assert len(encoded["predictions"]) == 4
    assert len(encoded["predictions"][0]) == 5
    assert len(encoded["predictions"][0][0]) == 5
    decoded = science.decode_predictions({
        "fit_key": "ROUNDTRIP", "predictions": encoded["predictions"],
        "prediction_shape": encoded["prediction_shape"]})
    assert np.array_equal(np.asarray(fixed, dtype=float), decoded)
    # the JSON round trip must be byte-stable, so the payload hash is reproducible
    again = json.loads(json.dumps(encoded))
    assert science.decode_predictions({"fit_key": "ROUNDTRIP", **again}).tolist() == \
        np.asarray(fixed, dtype=float).tolist()


def test_encode_predictions_rejects_a_bad_tensor(universe: sci.SyntheticUniverse):
    good = sci.fixed_baseline_predictions(universe, "S0")
    with pytest.raises(ValueError):
        science.encode_predictions(np.zeros((3, 5, 5)), universe)
    bad_support = np.array(good, dtype=float)
    bad_support[0, 0, 0] = 0.25          # own-region diagonal is structurally unavailable
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
    json.dumps(safe)  # genuinely JSON-safe


def test_completed_record_carries_the_complete_scientific_payload(
        universe: sci.SyntheticUniverse, config: sci.P2Config):
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
    assert record["kind"] == "primary" and record["regime"] == "S0"
    assert record["family"] == "parametric" and record["seed"] is None
    assert record["repeat_of"] is None
    assert record["pre_run_freeze_sha"] == TEST_FREEZE_SHA
    assert record["prediction_shape"] == [4, 5, 5]
    assert record["coefficients"] == [1.5, 0.6, -1.2, 0.3, -0.4, 0.0]
    assert record["objective"] == 0.5 and record["backend"] == "TEST_BACKEND"
    assert record["convergence"]["iterations"] == 3
    assert record["diagnostics"] == {"train_blocks": 9}
    assert "best_step" in record and "best_validation_loss" in record
    assert isinstance(record["runtime_seconds"], float)
    assert record["non_finite_originals"] == {}
    assert record["payload_sha256"] == science.canonical_payload_sha256(record)
    assert renderer.canonical_payload_sha256(record) == record["payload_sha256"]
    json.dumps(record, sort_keys=True)
    # the digest is over the scientific payload only: timing/provenance must not move it
    assert record["payload_sha256"] == science.canonical_payload_sha256(
        {**record, "recorded_utc": "1999-01-01T00:00:00+00:00", "runtime_seconds": 99.0,
         "pre_run_freeze_sha": "OTHER"})


def test_payload_hash_is_sensitive_to_scientific_content(
        universe: sci.SyntheticUniverse, config: sci.P2Config):
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


# ------------------------------------------- 6. fake 12-fit ledger (the #77 gate)
def _blended_predictions(universe: sci.SyntheticUniverse, regime: str,
                         target_weight: float) -> np.ndarray:
    """A deterministic, fit-free share tensor: blend of the frozen target and uniform."""
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
    """A duck-typed FitOutcome with real-shape tensors and dummy metadata (no fitting)."""
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
                      omit_seal_seconds: bool = False,
                      tamper_payload_hash: bool = False) -> Path:
    """Build a complete synthetic 12-fit durable ledger through the production writers."""
    plan = science.build_fit_plan(universe.config)
    clock = datetime(2026, 9, 19, 0, 0, 0, tzinfo=timezone.utc)
    step = timedelta(seconds=1)
    for entry in plan:
        science.append_ledger_record(path, {
            "event": "FIT_ATTEMPT_STARTED", "recorded_utc": clock.isoformat(),
            "attempt_index": entry["attempt_index"], "planned_attempts": 12,
            "kind": entry["kind"], "family": entry["family"], "regime": entry["regime"],
            "seed": entry["seed"], "fit_key": entry["fit_key"],
            "repeat_of": entry["repeat_of"], "pre_run_freeze_sha": freeze_sha,
            "started_monotonic_seconds": float(entry["attempt_index"]),
        })
        clock += step
        outcome = _fake_outcome(universe, entry)
        record = science.build_completed_record(entry, outcome, universe,
                                                outcome.runtime_seconds, freeze_sha)
        record["recorded_utc"] = clock.isoformat()
        if tamper_payload_hash:
            record["payload_sha256"] = "0" * 64
        science.append_ledger_record(path, record)
        clock += step
    if with_seal:
        expected = {r["fit_key"]: r for r in science.read_ledger(path)
                    if r.get("event") == "FIT_COMPLETED"}
        assert len(expected) == 12
        science.write_json_durable(path.parent / science.SEAL_RELPATH.split("/")[-1], {
            "phase": "SCIENCE_STAGE_SEAL", "pre_run_freeze_sha": freeze_sha,
            "science_invocations": 1, "science_retries": 0,
            "started_count": 12, "completed_count": 12, "failed_count": 0,
            "science_wall_clock_seconds": (None if omit_seal_seconds else 42.5),
            "science_wall_clock_ceiling_seconds": 1800.0,
            "ledger_relpath": science.LEDGER_RELPATH,
            "scientific_module_blob_sha1": science.EXPECTED_SCIENTIFIC_MODULE_BLOB,
            "terminal": science.TERMINAL_PASS,
        })
    return path


@pytest.fixture
def fake_ledger(universe: sci.SyntheticUniverse, tmp_path: Path) -> Path:
    return write_fake_ledger(universe, tmp_path / renderer.LEDGER_NAME)


@pytest.fixture
def no_fitters(monkeypatch):
    """Every fitting/optimizer entry point becomes an exploding tripwire."""
    calls: list[str] = []

    def tripwire(name: str):
        def explode(*args, **kwargs):  # pragma: no cover - must never be called
            calls.append(name)
            raise AssertionError(f"{name} must never be called by the render stage")
        return explode

    for name in ("fit_parametric", "fit_neural", "run_scientific_program"):
        monkeypatch.setattr(sci, name, tripwire(name))
    for name in ("_adam_step", "_backward", "_forward", "_init_mlp",
                 "_softmax_cross_entropy", "_masked_softmax", "_train_only_zscore"):
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
    assert invariants["exactly_twelve_started"] and invariants["exactly_twelve_completed"]


def test_fake_ledger_payloads_persist_real_shape_tensors(fake_ledger: Path):
    completed = renderer.completed_records(science.read_ledger(fake_ledger))
    assert len(completed) == 12
    checks = renderer.payload_hash_verification(completed)
    assert checks["all_payload_hashes_match"] is True
    assert checks["all_prediction_shapes_frozen"] is True
    assert checks["all_predictions_persisted"] is True
    assert checks["all_metadata_present"] is True
    for record in completed:
        tensor = renderer.decode_predictions(record)
        assert tensor.shape == (4, 5, 5)
        assert tensor.min() >= 0.0
    parametric = [r for r in completed if r["family"] == "parametric"]
    neural = [r for r in completed if r["family"] == "neural"]
    assert len(parametric) == 4 and len(neural) == 8
    assert all(isinstance(r["coefficients"], list) and len(r["coefficients"]) == 6
               for r in parametric)
    assert all(r["coefficients"] is None for r in neural)


def test_aggregate_metrics_output_shape_is_the_constraint_input_contract(
        universe: sci.SyntheticUniverse, fake_ledger: Path):
    """The exact shape the production aggregation produces and the consumer requires."""
    completed = renderer.completed_records(science.read_ledger(fake_ledger))
    aggregated = renderer.aggregate_metrics(universe, completed)
    assert set(aggregated) == set(renderer.PRIMARY_FIT_KEYS) | {
        repeat for _, repeat in renderer.REPEAT_PAIRS}
    for key, entry in aggregated.items():
        assert isinstance(entry, dict)
        assert "metrics" in entry, key
        assert set(entry["metrics"]) == set(renderer.SPLIT_STATES)
        assert entry["prediction_source"] == "PERSISTED_FIT_COMPLETED_PREDICTIONS"
        for split in renderer.SPLIT_STATES:
            block = entry["metrics"][split]
            assert {"weighted_cross_entropy", "mean_absolute_share_error",
                    "row_normalization_violation_max", "negativity_violation_count",
                    "support_violation_count", "top1_destination_accuracy",
                    "share_kl_per_block_mean", "evaluated_cells"} <= set(block)
    fixed = renderer.fixed_baseline_metrics(universe)
    assert set(fixed) == {"S0", "S1"}
    for regime, entry in fixed.items():
        assert set(entry["metrics"]) == set(renderer.SPLIT_STATES)
    constraints = renderer.constraint_diagnostics(universe, aggregated, fixed)
    assert constraints["evaluated_prediction_sets"] == 14
    assert constraints["row_normalization_ok"] is True
    assert constraints["negativity_ok"] is True
    assert constraints["support_ok"] is True
    assert constraints["split_counts_ok"] is True
    assert constraints["excluded_block_count"] == 6


def test_constraint_diagnostics_rejects_the_issue_77_input_shape(
        universe: sci.SyntheticUniverse, fake_ledger: Path):
    """The #77 defect must now fail loudly and early instead of as a bare KeyError."""
    completed = renderer.completed_records(science.read_ledger(fake_ledger))
    good = renderer.aggregate_metrics(universe, completed)
    fixed = renderer.fixed_baseline_metrics(universe)
    legacy_shape = {key: good[key]["metrics"] for key in renderer.PRIMARY_FIT_KEYS}
    with pytest.raises(TypeError) as excinfo:
        renderer.constraint_diagnostics(universe, legacy_shape, fixed)
    assert "Issue #77" in str(excinfo.value)
    assert "metrics" in str(excinfo.value)
    with pytest.raises(TypeError):
        renderer.constraint_diagnostics(universe, {"S0:parametric": []}, fixed)
    with pytest.raises(KeyError):
        renderer.constraint_diagnostics(universe, {}, fixed)
    truncated = {k: v for k, v in good.items() if k != "S1:neural:seed2"}
    with pytest.raises(KeyError):
        renderer.constraint_diagnostics(universe, truncated, fixed)
    incomplete = {k: {"metrics": {s: m for s, m in v["metrics"].items() if s != "TEST"}}
                  for k, v in good.items()}
    with pytest.raises(KeyError):
        renderer.constraint_diagnostics(universe, incomplete, fixed)
    # and the correct shape is accepted
    assert renderer.constraint_diagnostics(universe, good, fixed)["row_normalization_ok"] is True


def test_determinism_uses_fake_repeated_predictions(
        universe: sci.SyntheticUniverse, fake_ledger: Path):
    completed = renderer.completed_records(science.read_ledger(fake_ledger))
    by_key = {r["fit_key"]: r for r in completed}
    determinism = renderer.determinism_comparisons(universe, by_key)
    assert set(renderer.DETERMINISM_NAMES) <= set(determinism)
    for name in renderer.DETERMINISM_NAMES:
        assert determinism[name]["deviation"] == 0.0, name
    assert determinism["parametric_S0"]["coefficient_deviation"] == 0.0
    assert determinism["all_within_tolerance"] is True
    assert determinism["max_deviation"] == 0.0
    assert determinism["determinism_tolerance"] == 1e-12

    # a perturbed repeat must be detected (the tolerance is a real check, not vacuous)
    tampered = dict(by_key)
    tampered["S0:parametric:repeat"] = dict(by_key["S0:parametric:repeat"])
    tensor = renderer.decode_predictions(tampered["S0:parametric:repeat"])
    tensor[0, 0, 1] += 1e-6
    tampered["S0:parametric:repeat"]["predictions"] = tensor.tolist()
    detected = renderer.determinism_comparisons(universe, tampered)
    assert detected["parametric_S0"]["deviation"] > 1e-12
    assert detected["all_within_tolerance"] is False
    assert detected["any_deviation_over_tolerance"] is True


def test_share_distribution_check_reads_the_recovery_object(
        universe: sci.SyntheticUniverse, fake_ledger: Path):
    completed = renderer.completed_records(science.read_ledger(fake_ledger))
    shares = renderer.share_distribution_check(universe, completed)
    assert len(shares["per_fit"]) == 12
    assert shares["all_valid"] is True
    for info in shares["per_fit"].values():
        assert info["max_row_sum_deviation"] <= 1e-12
        assert info["min_allowed_share"] >= 0.0
        assert info["unavailable_cell_violations"] == 0


def test_fake_ledger_renders_end_to_end_with_zero_fits(
        universe: sci.SyntheticUniverse, fake_ledger: Path, tmp_path: Path,
        no_fitters, capsys):
    """THE mandatory P2C gate: the exact production path, end to end, zero fits."""
    exit_code = renderer.render(repo_root=ROOT, ledger_path=fake_ledger,
                                seal_path=tmp_path / renderer.SEAL_NAME, outdir=tmp_path)
    assert no_fitters == [], f"the render stage called a fitter: {no_fitters}"
    assert exit_code == 0
    stdout = json.loads(capsys.readouterr().out)
    assert stdout["fits"] == 0 and stdout["optimizer_steps"] == 0
    assert stdout["metrics_computed_from"] == "PERSISTED_LEDGER_PREDICTIONS_ONLY"
    assert stdout["gate_ok"] is True
    assert stdout["terminal"] == renderer.TERMINAL_PASS
    assert stdout["all_checks_pass"] is True

    for name in (renderer.RAW_NAME, renderer.RESULTS_NAME, renderer.MANIFEST_NAME):
        assert (tmp_path / name).is_file(), name
    assert (tmp_path / renderer.REPORT_NAME).is_file()

    raw = json.loads((tmp_path / renderer.RAW_NAME).read_text(encoding="utf-8"))
    results = json.loads((tmp_path / renderer.RESULTS_NAME).read_text(encoding="utf-8"))
    manifest = json.loads((tmp_path / renderer.MANIFEST_NAME).read_text(encoding="utf-8"))

    # metrics
    assert set(results["metrics_by_split"]) == set(renderer.PRIMARY_FIT_KEYS) | {
        repeat for _, repeat in renderer.REPEAT_PAIRS}
    for key, by_split in results["metrics_by_split"].items():
        assert set(by_split) == set(renderer.SPLIT_STATES)
        assert by_split["TEST"]["evaluated_cells"] == 6
        assert by_split["TRAIN"]["evaluated_cells"] == 36
        assert by_split["VALIDATION"]["evaluated_cells"] == 12
        assert by_split["EXCLUDED_REFERENCE_ONLY"]["evaluated_cells"] == 18
        assert by_split["TEST"]["split_blocks"] == 2
    assert set(results["fixed_baseline_metrics"]) == {"S0", "S1"}
    # determinism
    assert results["determinism"]["all_within_tolerance"] is True
    assert results["determinism"]["max_deviation"] == 0.0
    # constraints
    constraints = results["constraint_diagnostics"]
    assert constraints["row_normalization_ok"] is True
    assert constraints["negativity_ok"] is True
    assert constraints["support_ok"] is True
    assert constraints["split_counts"] == {"TRAIN": 9, "VALIDATION": 3, "TEST": 2,
                                          "EXCLUDED_REFERENCE_ONLY": 6}
    assert constraints["excluded_block_count"] == 6
    assert results["p1a_accounting_checks"]["closes"] is True
    assert results["share_distribution_check"]["all_valid"] is True
    assert results["payload_hash_verification"]["all_payload_hashes_match"] is True
    assert results["attempt_ledger_summary"]["started_count"] == 12
    assert results["attempt_ledger_summary"]["completed_count"] == 12
    assert results["render_only_invocations"] == 1
    assert results["zero_fit_statement"] == renderer.ZERO_FIT_STATEMENT

    # every gate is green in the fake-ledger path
    assert all(results["acceptance_gate_checks"].values()), [
        k for k, v in results["acceptance_gate_checks"].items() if not v]

    # identity chain is acyclic and recomputes
    import hashlib

    core = {k: v for k, v in results.items()
            if k not in (renderer.RESULTS_DIGEST_FIELD, renderer.MANIFEST_DIGEST_FIELD)}
    assert results[renderer.RESULTS_DIGEST_FIELD] == \
        hashlib.sha256(renderer.dumps(core)).hexdigest().upper()
    assert results[renderer.MANIFEST_DIGEST_FIELD] == \
        hashlib.sha256(renderer.dumps(manifest)).hexdigest().upper()
    assert manifest["artifact_hashes"]["ledger_sha256_lf"] == renderer.sha256_lf(fake_ledger)
    assert manifest["artifact_hashes"]["results_canonical_sha256"] == \
        results[renderer.RESULTS_DIGEST_FIELD]
    assert manifest["terminal"] == results["terminal"] == renderer.TERMINAL_PASS
    assert manifest["declarations"]["renderer_calls_any_fitter"] is False
    assert manifest["science_protocol"]["fits_performed_by_renderer"] == 0
    assert manifest["science_protocol"]["optimizer_steps_performed_by_renderer"] == 0
    assert manifest["science_protocol"]["zero_fit_publication"] is True
    assert raw["zero_fit_recovery"]["fits_performed_here"] == 0
    assert raw["pre_run_freeze_sha"] == TEST_FREEZE_SHA
    assert raw["aggregation_contract"]["shape_validated_loudly"] is True
    assert "PASS" in (tmp_path / renderer.REPORT_NAME).read_text(encoding="utf-8")


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
    assert after["determinism"]["deviations"] == before["determinism"]["deviations"]
    assert after["constraint_diagnostics"] == before["constraint_diagnostics"]


def test_render_refuses_without_a_ledger(tmp_path: Path, no_fitters, capsys):
    exit_code = renderer.render(repo_root=ROOT, ledger_path=tmp_path / "absenta.jsonl",
                                outdir=tmp_path)
    assert exit_code == 3
    assert no_fitters == []
    payload = json.loads(capsys.readouterr().out)
    assert payload["terminal"] == renderer.TERMINAL_BLOCKED
    assert payload["fits"] == 0 and payload["optimizer_steps"] == 0
    assert not (tmp_path / renderer.RESULTS_NAME).exists()


def test_render_fails_the_gate_on_a_tampered_payload_hash(
        universe: sci.SyntheticUniverse, tmp_path: Path, no_fitters, capsys):
    ledger = write_fake_ledger(universe, tmp_path / renderer.LEDGER_NAME,
                               tamper_payload_hash=True)
    exit_code = renderer.render(repo_root=ROOT, ledger_path=ledger,
                                seal_path=tmp_path / renderer.SEAL_NAME, outdir=tmp_path)
    assert no_fitters == []
    assert exit_code == 2
    stdout = json.loads(capsys.readouterr().out)
    assert stdout["gate_ok"] is False
    assert stdout["terminal"] == renderer.TERMINAL_GATE_FAIL
    assert stdout["gate_checks"]["every_payload_sha256_verifies"] is False


def test_render_derives_the_wall_clock_from_the_ledger_when_the_seal_is_absent(
        universe: sci.SyntheticUniverse, tmp_path: Path, no_fitters, capsys):
    ledger = write_fake_ledger(universe, tmp_path / renderer.LEDGER_NAME, with_seal=False)
    exit_code = renderer.render(repo_root=ROOT, ledger_path=ledger,
                                seal_path=tmp_path / renderer.SEAL_NAME, outdir=tmp_path)
    assert exit_code == 0
    capsys.readouterr()
    results = json.loads((tmp_path / renderer.RESULTS_NAME).read_text(encoding="utf-8"))
    clock = results["science_wall_clock"]
    assert clock["wall_clock_source"] == "DERIVED_FROM_LEDGER_RECORDED_UTC"
    assert clock["within_ceiling"] is True
    assert clock["seal_present"] is False
    assert clock["ledger_span_seconds"] > 0.0
    assert clock["sum_completed_fit_runtime_seconds"] > 0.0


def test_resolve_science_wall_clock_prefers_the_seal(universe: sci.SyntheticUniverse,
                                                     fake_ledger: Path):
    records = science.read_ledger(fake_ledger)
    seal = json.loads((fake_ledger.parent / renderer.SEAL_NAME).read_text(encoding="utf-8"))
    clock = renderer.resolve_science_wall_clock(records, seal)
    assert clock["wall_clock_source"] == "SCIENCE_SEAL"
    assert clock["science_wall_clock_seconds"] == 42.5
    assert clock["seal_seconds"] == 42.5
    assert clock["seal_present"] is True
    assert clock["within_ceiling"] is True


# ------------------------------------------------- 7. render-only cannot fit
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
    """A static guard on attribute access as well as on call targets."""
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


def test_science_runner_validate_only_is_zero_fit(capsys):
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
    assert payload["science_start_allowed"] is True


def test_science_runner_cli_requires_a_mode():
    with pytest.raises(SystemExit):
        science.main([])


# ------------------------------------------------- 8. static import / content guards
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
    """The renderer must emit the documented publication keys."""
    text = RENDERER.read_text(encoding="utf-8")
    for emitted in ("metrics_by_split", "fixed_baseline_metrics", "fit_summaries",
                    "determinism", "constraint_diagnostics", "p1a_accounting_checks",
                    "acceptance_gate_checks", "audit_context_vs_issue_76",
                    "interpretation_ceiling", "negative_result_flags",
                    "payload_hash_verification", "share_distribution_check",
                    "aggregation_contract", "zero_fit_recovery", "artifact_hashes",
                    "provenance_chain", "declarations", "render_only_invocations"):
        assert emitted in text, emitted
    science_text = SCIENCE_RUNNER.read_text(encoding="utf-8")
    for emitted in ("FIT_ATTEMPT_STARTED", "FIT_COMPLETED", "FIT_FAILED", "payload_sha256",
                    "prediction_shape", "non_finite_originals", "PAYLOAD_SCIENTIFIC_KEYS",
                    "payload_canonicalization"):
        assert emitted in science_text, emitted


def test_science_writes_only_the_ledger_and_the_seal():
    """Science-stage artifact allowlist: no metric and no publication file."""
    text = SCIENCE_RUNNER.read_text(encoding="utf-8")
    assert "RAW_RESULTS" not in text
    assert "RESULTS_RELPATH" not in text
    assert "MANIFEST_RELPATH" not in text
    assert "REPORT_RELPATH" not in text
    assert "no metric" in text.lower()
    assert science.LEDGER_RELPATH == (
        "reports/dlh_wl_p2c_2026_09_19/DLH_WL_P2C_ATTEMPT_LEDGER.jsonl")
    assert science.SEAL_RELPATH == (
        "reports/dlh_wl_p2c_2026_09_19/DLH_WL_P2C_SCIENCE_SEAL.json")
    assert renderer.RAW_RELPATH == (
        "reports/dlh_wl_p2c_2026_09_19/DLH_WL_P2C_RAW_RESULTS.json")
    assert renderer.RESULTS_RELPATH == (
        "reports/dlh_wl_p2c_2026_09_19/DLH_WL_P2C_RESULTS.json")
    assert renderer.MANIFEST_RELPATH == (
        "reports/dlh_wl_p2c_2026_09_19/DLH_WL_P2C_MANIFEST.json")
    assert renderer.REPORT_RELPATH == (
        "reports/dlh_wl_p2c_2026_09_19/DLH_WL_P2C_REPORT.md")


def test_science_stage_has_not_been_run_twice_against_the_repository():
    """Pre-run this asserts the science stage has not started.

    Post-run it asserts the durable ledger is exactly one complete 12/12 science
    invocation — never a second one.
    """
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
