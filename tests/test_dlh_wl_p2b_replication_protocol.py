"""DLH-WL-P2B — focused pre-run protocol tests (Issue #77).

These tests perform **zero optimizer steps** and never train: they exercise config and
module identity, the deterministic generator, the frozen plan as pure data, durable
ledger semantics with dummy no-fit events, the fail-closed guards, and the static
guards that keep rendering and fitting apart.

Authority: Issue #77 ``DLH-WL-P2B``; activation comment ``5740223593``; marker
``DLH_WL_P2B_CLEAN_IMMUTABLE_REPLICATION_AUTHORIZED``.
"""

from __future__ import annotations

import ast
import json
import sys
import tomllib
from dataclasses import replace
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
for path in (str(SRC), str(ROOT / "scripts")):
    if path not in sys.path:
        sys.path.insert(0, path)

import run_dlh_wl_p2b_replication_science as science  # noqa: E402
import render_dlh_wl_p2b_replication as renderer  # noqa: E402
from deep_learning_hank.regional import labor_destination_p2 as sci  # noqa: E402

CONFIG_PATH = ROOT / science.CONFIG_RELPATH
MODULE_PATH = ROOT / science.SCIENTIFIC_MODULE_RELPATH
SCIENCE_RUNNER = ROOT / renderer.SCIENCE_RUNNER_RELPATH
RENDERER = ROOT / renderer.RENDERER_RELPATH
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
    assert science.TERMINAL_PASS == "DLH_WL_P2B_CLEAN_REPLICATION__PASS__P2_METHOD_GATE_COMPLETE"
    assert science.TERMINAL_GATE_FAIL == (
        "DLH_WL_P2B_CLEAN_REPLICATION__GATE_FAIL__NO_SCIENCE_RERUN_AUTHORIZED")
    assert science.TERMINAL_BLOCKED == "BLOCKED_DLH_WL_P2B_PRE_RUN_OR_ENVIRONMENT"
    assert science.EXPERIMENT_ID == "EXP-20260919-DLH-WL-P2B-001"


def test_frozen_config_identity(config: sci.P2Config):
    raw = tomllib.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    assert raw["authority"]["config_revision"] == 4
    assert config.config_revision == 4
    assert science.blob_sha1_lf(CONFIG_PATH) == science.EXPECTED_CONFIG_BLOB
    assert config.neural_seeds == (0, 1, 2)
    assert config.hidden_widths == (16, 8)
    assert config.max_steps == 1500 and config.eval_every == 50
    assert config.early_stop_patience == 200
    assert config.absolute_attempt_ceiling == 13
    assert config.planned_fit_executions == 12
    assert config.wall_clock_seconds_max == 1800.0


def test_scientific_module_blob_is_the_accepted_76_module():
    blob = science.blob_sha1_lf(MODULE_PATH)
    assert blob == science.EXPECTED_SCIENTIFIC_MODULE_BLOB == (
        "b1f2cd043605c511e4965254657d12306170609b")


def test_frozen_inputs_are_read_only_declarations():
    for relpath in (science.CONFIG_RELPATH, science.CONTRACT_RELPATH, science.SCHEMA_RELPATH,
                    science.P1A_MODULE_RELPATH, science.SCIENTIFIC_MODULE_RELPATH):
        assert (ROOT / relpath).is_file(), relpath
    text = SCIENCE_RUNNER.read_text(encoding="utf-8")
    assert "must not be modified" in text or "never modified" in text


# ------------------------------------------------------------- 2. generator checks
def test_generator_reference_shares(universe: sci.SyntheticUniverse):
    report = sci.validate_only_report(universe)
    got_s0 = report["reference_shares"]["S0:r00_t1"]
    got_s1 = report["reference_shares"]["S1:r04_t4"]
    assert all(abs(a - b) < 5e-9 for a, b in zip(got_s0, FROZEN_S0_R00_T1))
    assert all(abs(a - b) < 5e-9 for a, b in zip(got_s1, FROZEN_S1_R04_T4))
    assert report["contrast_rank"] == 6
    assert report["s0_contrast_residual"] <= report["residual_precision_floor"]
    assert report["optimizer_steps_performed"] == 0


def test_split_counts_and_interpretation_ceiling(universe: sci.SyntheticUniverse):
    counts = {state: len(universe.blocks_for(state))
              for state in ("TRAIN", "VALIDATION", "TEST", "EXCLUDED_REFERENCE_ONLY")}
    assert counts == {"TRAIN": 9, "VALIDATION": 3, "TEST": 2, "EXCLUDED_REFERENCE_ONLY": 6}
    assert sum(counts.values()) == 20
    train_origins = {b.origin_id for b in universe.blocks_for("TRAIN")}
    test_origins = {b.origin_id for b in universe.blocks_for("TEST")}
    assert train_origins == {"R00", "R01", "R02"}
    assert test_origins.isdisjoint(train_origins)
    train_destinations = {universe.config.region_ids[j]
                          for b in universe.blocks_for("TRAIN") for j in b.allowed}
    assert test_origins <= train_destinations, "R03/R04 must appear as TRAIN destinations"
    assert {b.time_id for b in universe.blocks_for("TEST")} == {4}
    assert {b.time_id for b in universe.blocks_for("TRAIN")} == {1, 2, 3}


def test_no_unseen_region_claim_in_code_or_tests():
    for path in (SCIENCE_RUNNER, RENDERER, Path(__file__)):
        text = path.read_text(encoding="utf-8")
        if "UNSEEN_REGION" in text:
            assert ("forbidden" in text.lower()) or ("is_unseen_regions" in text)
    text = RENDERER.read_text(encoding="utf-8")
    assert "test_regions_are_unseen_regions" in text


# ------------------------------------------------------------------ 3. fit plan data
def test_fit_plan_is_exactly_twelve_frozen_attempts(config: sci.P2Config):
    plan = science.build_fit_plan(config)
    assert len(plan) == 12
    assert [entry["attempt_index"] for entry in plan] == list(range(1, 13))
    families = [entry["family"] for entry in plan]
    assert families.count("parametric") == 4
    assert families.count("neural") == 8
    kinds = [entry["kind"] for entry in plan]
    assert kinds.count("primary") == 8
    assert kinds.count("verification_repeat") == 4
    neural = [entry for entry in plan if entry["family"] == "neural"]
    seed_zero = [entry for entry in neural if entry["seed"] == 0 and entry["kind"] == "primary"]
    assert len(seed_zero) == 2
    assert {entry["fit_key"] for entry in neural} == {
        "S0:neural:seed0", "S0:neural:seed1", "S0:neural:seed2",
        "S1:neural:seed0", "S1:neural:seed1", "S1:neural:seed2",
        "S0:neural:seed0:repeat", "S1:neural:seed0:repeat"}


def test_fit_plan_rejects_a_non_frozen_seed_list(config: sci.P2Config):
    with pytest.raises(ValueError):
        science.build_fit_plan(replace(config, neural_seeds=(0, 1, 2, 3)))
    with pytest.raises(ValueError):
        science.build_fit_plan(replace(config, neural_seeds=(0, 1)))


def test_science_runner_has_no_retry_or_extra_seed_switches():
    text = SCIENCE_RUNNER.read_text(encoding="utf-8")
    for forbidden in ("--retry", "--extra-seed", "--tune", "--search", "--force"):
        assert forbidden not in text, forbidden
    assert "--execute-science" in text and "--validate-only" in text


# ------------------------------------------------------- 4. durable ledger semantics
def test_ledger_append_is_durable_and_parseable(tmp_path: Path):
    ledger = tmp_path / "ledger.jsonl"
    science.append_ledger_record(ledger, {"event": "FIT_ATTEMPT_STARTED", "attempt_index": 1,
                                          "fit_key": "S0:parametric"})
    science.append_ledger_record(ledger, {"event": "FIT_COMPLETED", "attempt_index": 1,
                                          "fit_key": "S0:parametric", "runtime_seconds": 0.0})
    raw_lines = ledger.read_text(encoding="utf-8").splitlines()
    assert len(raw_lines) == 2
    records = science.read_ledger(ledger)
    assert [r["event"] for r in records] == ["FIT_ATTEMPT_STARTED", "FIT_COMPLETED"]
    summary = science.ledger_summary(records)
    assert summary["started_count"] == 1 and summary["completed_count"] == 1
    assert summary["failed_count"] == 0 and summary["science_retries"] == 0


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
    assert summary["attempt_indices_started"] == [1, 2]


def test_refuse_science_start_when_outputs_exist(tmp_path: Path):
    ledger = tmp_path / "ledger.jsonl"
    raw = tmp_path / "raw.json"
    assert science.refuse_if_outputs_exist(ledger, raw) is None
    ledger.write_text("", encoding="utf-8")
    assert "ledger already exists" in science.refuse_if_outputs_exist(ledger, raw)
    ledger.unlink()
    raw.write_text("{}", encoding="utf-8")
    assert "raw result already exists" in science.refuse_if_outputs_exist(ledger, raw)


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
    exit_code = science.execute_science("TESTFREEZE")
    assert exit_code == 3
    assert calls == []


# --------------------------------------- 5. metrics/constraint helpers on raw numbers
def test_constraint_diagnostics_and_determinism_helpers(universe: sci.SyntheticUniverse):
    cfg = universe.config
    class _Stub:
        def __init__(self, predictions, **extra):
            self.predictions = predictions
            self.objective = extra.get("objective", 1.0)
            self.coefficients = extra.get("coefficients", [0.0] * 6)
            self.best_step = extra.get("best_step", 1)
            self.best_validation_loss = extra.get("best_validation_loss", 1.0)

    outcomes = {}
    for name in ("S0", "S1"):
        baseline = sci.fixed_baseline_predictions(universe, name)
        outcomes[f"fit::{name}:parametric"] = _Stub(baseline)
        outcomes[f"fit::{name}:parametric:repeat"] = _Stub(baseline)
        outcomes[f"fit::{name}:neural:seed0"] = _Stub(baseline)
        outcomes[f"fit::{name}:neural:seed0:repeat"] = _Stub(baseline)
    metrics = {}
    fixed = {}
    for regime in ("S0", "S1"):
        pred = sci.fixed_baseline_predictions(universe, regime)
        per_split = {
            split: sci.evaluate_predictions(universe, regime, pred, universe.blocks_for(split))
            for split in ("TRAIN", "VALIDATION", "TEST", "EXCLUDED_REFERENCE_ONLY")}
        # the diagnostics helper consumes the same shape the science runner records:
        # fit key -> {"metrics": {split: metrics}}
        metrics[f"{regime}:parametric"] = {"metrics": per_split}
        fixed[regime] = {"metrics": per_split}
    constraints = science._constraint_diagnostics(universe, metrics, fixed)
    assert constraints["row_normalization_ok"] is True
    assert constraints["negativity_ok"] is True
    assert constraints["support_ok"] is True
    assert constraints["split_counts_ok"] is True
    assert constraints["excluded_block_count"] == 6

    determinism = science._determinism_comparisons(universe, outcomes)
    assert determinism["all_within_tolerance"] is True
    assert determinism["parametric_S0"]["deviation"] == 0.0
    assert determinism["determinism_tolerance"] == cfg.determinism_tolerance


# ------------------------------------------------- 6. render-only cannot fit
def test_renderer_never_references_fitting_entry_points():
    tree = ast.parse(RENDERER.read_text(encoding="utf-8"))
    # only actual call targets matter: this catches a renderer that would train, while
    # ignoring harmless mentions inside docstrings or guard strings
    calls: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name):
                calls.add(func.id)
            elif isinstance(func, ast.Attribute):
                calls.add(func.attr)
    for forbidden in ("fit_parametric", "fit_neural", "run_scientific_program",
                      "_adam_step", "_backward", "_forward", "_train_only_zscore"):
        assert forbidden not in calls, forbidden


def test_renderer_validate_only_reports_zero_fits():
    payload = {
        "optimizer_steps_performed": 0,
        "fit_attempts_performed": 0,
    }
    text = RENDERER.read_text(encoding="utf-8")
    assert '"optimizer_steps_performed": 0' in text
    assert '"fit_attempts_performed": 0' in text
    assert payload["optimizer_steps_performed"] == 0


# ------------------------------------------------- 7. static import / content guards
def test_no_forbidden_scientific_imports(tmp_path: Path):
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
    text = SCIENCE_RUNNER.read_text(encoding="utf-8")
    for symbol in ("solve_household_steady_state", "solve_matlab_faithful_hjb",
                   "BoundaryHJBSolver", "matlab_contaminated_row_index"):
        assert symbol not in text


def test_declarations_present_in_science_runner():
    text = SCIENCE_RUNNER.read_text(encoding="utf-8")
    assert "no real data, no HJB/KFE/GE/MATLAB/household code, no tuning, no extra seed" in text
    assert "immutable" in text


def test_renderer_declares_zero_fit_contract():
    text = RENDERER.read_text(encoding="utf-8")
    assert "zero fits" in text
    assert "never" in text and "train" in text
    assert "manifest_canonical_sha256" in text
    assert "results_canonical_sha256" in text


def test_raw_and_results_schema_expectations():
    """The renderer must consume exactly the documented raw keys and emit the documented set."""
    text = RENDERER.read_text(encoding="utf-8")
    for key in ('"metrics"', '"fixed_baseline_metrics"', '"fit_outcomes"',
                '"determinism"', '"constraint_diagnostics"', '"p1a_accounting_checks"',
                '"attempt_ledger_summary"', '"science_wall_clock_seconds"',
                '"frozen_split_interpretation"', '"code_identity"', '"pre_run_freeze_sha"'):
        assert key in text, key
    for emitted in ("metrics_by_split", "audit_context_vs_issue_76", "acceptance_gate_checks",
                    "interpretation_ceiling", "artifact_hashes", "provenance_chain"):
        assert emitted in text, emitted


def test_render_only_refuses_without_science_outputs(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(renderer, "ROOT", tmp_path)
    assert renderer.render() == 3
