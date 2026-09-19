"""DLH-WL-P2B — clean immutable replication: science runner (Issue #77).

This script is the **only** authorized science path for Issue #77. It performs exactly
the frozen #75 fit program once, under a durable cross-invocation attempt ledger, and
writes exactly one raw scientific artifact. Publication artifacts are produced later by
``scripts/render_dlh_wl_p2b_replication.py --render-only``, which performs zero fits.

Binding rules implemented here (Issue #77 sections 2-6):

* exactly one ``--execute-science`` invocation is authorized; there is no science
  retry and no second invocation;
* exactly 12 fit attempts: 2 parametric primaries, 2 parametric verification repeats,
  6 neural primaries (seeds 0/1/2 x S0/S1) and 2 neural seed-0 verification repeats;
* one durable ``FIT_ATTEMPT_STARTED`` record is appended and fsynced **before** each
  fit, followed by ``FIT_COMPLETED``; the runner fails closed before any attempt that
  would exceed the 12-attempt plan;
* ``--execute-science`` refuses to run if a ledger or raw result already exists, so no
  cross-invocation reset is possible;
* the frozen scientific module ``labor_destination_p2.py`` is imported and used
  byte-for-byte; it is never modified here;
* no real data, no HJB/KFE/GE/MATLAB/household code, no tuning, no extra seed.

The scientific execution identity is the PRE_RUN_FREEZE commit SHA passed on the
command line, not this file's later commit.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

# deterministic single-threaded execution, set before NumPy is imported by the module
for _var in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
             "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_var, "1")
os.environ.setdefault("PYTHONHASHSEED", "0")

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from deep_learning_hank.regional import labor_destination_p2 as sci  # noqa: E402

SCIENTIFIC_MODULE_RELPATH = "src/deep_learning_hank/regional/labor_destination_p2.py"
P1A_MODULE_RELPATH = "src/deep_learning_hank/regional/labor_destination.py"
CONFIG_RELPATH = "configs/dlh_wl_p2_offline_prototype.toml"
CONTRACT_RELPATH = "docs/specifications/DLH_WL_P2_OFFLINE_PROTOTYPE_CONTRACT_2026_09_18.md"
SCHEMA_RELPATH = "docs/data/DLH_WL_P1B_LABEL_AND_SAMPLE_SCHEMA_2026_09_18.md"

OUTDIR_RELPATH = "reports/dlh_wl_p2b_2026_09_19"
LEDGER_RELPATH = f"{OUTDIR_RELPATH}/DLH_WL_P2B_ATTEMPT_LEDGER.jsonl"
RAW_RELPATH = f"{OUTDIR_RELPATH}/DLH_WL_P2B_RAW_RESULTS.json"

EXPECTED_SCIENTIFIC_MODULE_BLOB = "b1f2cd043605c511e4965254657d12306170609b"
EXPECTED_CONFIG_BLOB = "bb5dbbd0746e9d92874f94b03a1d54f3d382c4a8"

EXPERIMENT_ID = "EXP-20260919-DLH-WL-P2B-001"
PLANNED_FIT_ATTEMPTS = 12
SCIENCE_WALL_CLOCK_CEILING_SECONDS = 1800.0

TERMINAL_PASS = "DLH_WL_P2B_CLEAN_REPLICATION__PASS__P2_METHOD_GATE_COMPLETE"
TERMINAL_GATE_FAIL = "DLH_WL_P2B_CLEAN_REPLICATION__GATE_FAIL__NO_SCIENCE_RERUN_AUTHORIZED"
TERMINAL_BLOCKED = "BLOCKED_DLH_WL_P2B_PRE_RUN_OR_ENVIRONMENT"


# --------------------------------------------------------------------------- helpers
def sha256_lf(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest().upper()


def blob_sha1_lf(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def environment_summary() -> dict[str, Any]:
    import numpy as np
    import scipy

    return {
        "versions": {
            "python": sys.version.split()[0],
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "platform": platform.platform(),
            "machine": platform.machine(),
        },
        "torch": "NOT_INSTALLED_NEURAL_BACKEND_IS_NUMPY",
        "thread_pinning": {v: os.environ.get(v) for v in
                           ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS",
                            "MKL_NUM_THREADS", "PYTHONHASHSEED")},
        "cpu_logical_cores": os.cpu_count(),
    }


# --------------------------------------------------------------------------- ledger
def append_ledger_record(path: Path, record: dict[str, Any]) -> dict[str, Any]:
    """Append one durable JSONL record and flush + fsync it before returning."""
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(record, sort_keys=True) + "\n"
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(line)
        handle.flush()
        os.fsync(handle.fileno())
    return record


def read_ledger(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    records: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            records.append(json.loads(line))
    return records


def ledger_summary(records: Sequence[dict[str, Any]]) -> dict[str, Any]:
    started = [r for r in records if r.get("event") == "FIT_ATTEMPT_STARTED"]
    completed = [r for r in records if r.get("event") == "FIT_COMPLETED"]
    failed = [r for r in records if r.get("event") == "FIT_FAILED"]
    return {
        "records": len(records),
        "started_count": len(started),
        "completed_count": len(completed),
        "failed_count": len(failed),
        "attempt_indices_started": [r.get("attempt_index") for r in started],
        "attempt_indices_completed": [r.get("attempt_index") for r in completed],
        "fit_keys_started": [r.get("fit_key") for r in started],
        "fit_keys_completed": [r.get("fit_key") for r in completed],
        "science_retries": 0,
    }


def refuse_if_outputs_exist(ledger_path: Path, raw_path: Path) -> str | None:
    """Fail closed when a previous P2B ledger or raw result is present."""
    if ledger_path.exists():
        return f"ledger already exists: {ledger_path}"
    if raw_path.exists():
        return f"raw result already exists: {raw_path}"
    return None


# --------------------------------------------------------------------------- plan
def build_fit_plan(config: sci.P2Config) -> list[dict[str, Any]]:
    """The frozen 12-attempt program, in order, as pure data (no fit is executed)."""
    plan: list[dict[str, Any]] = []
    index = 0
    for regime in ("S0", "S1"):
        index += 1
        plan.append({"attempt_index": index, "kind": "primary", "family": "parametric",
                     "regime": regime, "seed": None,
                     "fit_key": f"{regime}:parametric"})
    for regime in ("S0", "S1"):
        index += 1
        plan.append({"attempt_index": index, "kind": "verification_repeat",
                     "family": "parametric", "regime": regime, "seed": None,
                     "fit_key": f"{regime}:parametric:repeat"})
    for regime in ("S0", "S1"):
        for seed in config.neural_seeds:
            index += 1
            plan.append({"attempt_index": index, "kind": "primary", "family": "neural",
                         "regime": regime, "seed": int(seed),
                         "fit_key": f"{regime}:neural:seed{int(seed)}"})
    for regime in ("S0", "S1"):
        index += 1
        plan.append({"attempt_index": index, "kind": "verification_repeat",
                     "family": "neural", "regime": regime, "seed": 0,
                     "fit_key": f"{regime}:neural:seed0:repeat"})
    if len(plan) != PLANNED_FIT_ATTEMPTS:  # pragma: no cover - guarded by the frozen config
        raise ValueError(f"frozen plan must have exactly {PLANNED_FIT_ATTEMPTS} attempts "
                         f"(got {len(plan)})")
    return plan


# --------------------------------------------------------------------------- science
def run_one_fit(universe: sci.SyntheticUniverse, entry: dict[str, Any],
                design: Any) -> sci.FitOutcome:
    """Execute exactly one frozen fit (this is the only place an optimizer can run)."""
    family, regime, seed = entry["family"], entry["regime"], entry["seed"]
    if family == "parametric":
        return sci.fit_parametric(universe, regime)
    if family == "neural":
        return sci.fit_neural(universe, regime, int(seed), design=design)
    raise ValueError(f"unknown fit family {family!r}")


def _constraint_diagnostics(universe: sci.SyntheticUniverse, outcomes: dict[str, Any],
                            fixed: dict[str, Any]) -> dict[str, Any]:
    cfg = universe.config
    row_max, negativity, support = 0.0, 0, 0
    for registry in (outcomes, fixed):
        for entry in registry.values():
            for split in ("TRAIN", "VALIDATION", "TEST", "EXCLUDED_REFERENCE_ONLY"):
                block = entry["metrics"][split]
                row_max = max(row_max, block["row_normalization_violation_max"])
                negativity += block["negativity_violation_count"]
                support += block["support_violation_count"]
    return {
        "row_normalization_violation_max": row_max,
        "row_normalization_tolerance": cfg.row_normalization_tolerance,
        "row_normalization_ok": bool(row_max <= cfg.row_normalization_tolerance),
        "negativity_violation_count": int(negativity),
        "negativity_ok": negativity == 0,
        "support_violation_count": int(support),
        "support_ok": support == 0,
        "split_counts": dict(cfg.split_counts),
        "split_counts_ok": (cfg.split_counts.get("TRAIN") == 9
                            and cfg.split_counts.get("VALIDATION") == 3
                            and cfg.split_counts.get("TEST") == 2
                            and cfg.split_counts.get("EXCLUDED_REFERENCE_ONLY") == 6),
        "excluded_block_count": cfg.split_counts.get("EXCLUDED_REFERENCE_ONLY"),
        "excluded_block_count_ok": cfg.split_counts.get("EXCLUDED_REFERENCE_ONLY")
        == cfg.excluded_block_count_expected,
    }


def _determinism_comparisons(universe: sci.SyntheticUniverse,
                             outcomes: dict[str, Any]) -> dict[str, Any]:
    cfg = universe.config
    comparisons: dict[str, Any] = {}
    for regime in ("S0", "S1"):
        primary = outcomes[f"fit::{regime}:parametric"]
        repeat = outcomes[f"fit::{regime}:parametric:repeat"]
        comparisons[f"parametric_{regime}"] = {
            "deviation": float(abs(primary.predictions - repeat.predictions).max()),
            "primary_objective": primary.objective,
            "repeat_objective": repeat.objective,
            "coefficient_deviation": float(abs(
                __import__("numpy").asarray(primary.coefficients)
                - __import__("numpy").asarray(repeat.coefficients)).max()),
        }
        key = f"fit::{regime}:neural:seed0"
        rep = f"fit::{regime}:neural:seed0:repeat"
        comparisons[f"neural_{regime}_seed0"] = {
            "deviation": float(abs(outcomes[key].predictions - outcomes[rep].predictions).max()),
            "primary_best_step": outcomes[key].best_step,
            "repeat_best_step": outcomes[rep].best_step,
            "primary_best_validation_loss": outcomes[key].best_validation_loss,
            "repeat_best_validation_loss": outcomes[rep].best_validation_loss,
        }
    comparisons["determinism_tolerance"] = cfg.determinism_tolerance
    comparisons["all_within_tolerance"] = all(
        info["deviation"] <= cfg.determinism_tolerance
        for name, info in comparisons.items() if isinstance(info, dict))
    return comparisons


def execute_science(pre_run_freeze_sha: str) -> int:
    ledger_path = ROOT / LEDGER_RELPATH
    raw_path = ROOT / RAW_RELPATH

    refusal = refuse_if_outputs_exist(ledger_path, raw_path)
    if refusal is not None:
        print(json.dumps({"terminal": TERMINAL_GATE_FAIL,
                          "reason": f"refusing to run science: {refusal}"}, indent=2))
        return 3

    config = sci.load_frozen_config(ROOT, config_relpath=CONFIG_RELPATH)
    module_blob = blob_sha1_lf(ROOT / SCIENTIFIC_MODULE_RELPATH)
    config_blob = blob_sha1_lf(ROOT / CONFIG_RELPATH)
    if module_blob != EXPECTED_SCIENTIFIC_MODULE_BLOB:
        print(json.dumps({"terminal": TERMINAL_BLOCKED,
                          "reason": f"scientific module blob {module_blob} != expected "
                                    f"{EXPECTED_SCIENTIFIC_MODULE_BLOB}"}, indent=2))
        return 3

    universe = sci.build_universe(config, ROOT)
    design, preprocessing = sci._train_only_zscore(universe, universe.blocks_for("TRAIN"))
    plan = build_fit_plan(config)

    outcomes: dict[str, Any] = {}
    prediction_store: dict[str, Any] = {}
    metrics_store: dict[str, Any] = {}
    started_at = time.perf_counter()
    science_terminal = TERMINAL_PASS

    for entry in plan:
        if entry["attempt_index"] > PLANNED_FIT_ATTEMPTS:
            raise RuntimeError("attempt index beyond the frozen plan")
        append_ledger_record(ledger_path, {
            "event": "FIT_ATTEMPT_STARTED",
            "recorded_utc": utc_now(),
            "attempt_index": entry["attempt_index"],
            "planned_attempts": PLANNED_FIT_ATTEMPTS,
            "kind": entry["kind"],
            "family": entry["family"],
            "regime": entry["regime"],
            "seed": entry["seed"],
            "fit_key": entry["fit_key"],
            "pre_run_freeze_sha": pre_run_freeze_sha,
        })
        attempt_started = time.perf_counter()
        try:
            outcome = run_one_fit(universe, entry, design)
        except Exception as exc:  # fail closed: no retry, no rerun
            append_ledger_record(ledger_path, {
                "event": "FIT_FAILED",
                "recorded_utc": utc_now(),
                "attempt_index": entry["attempt_index"],
                "fit_key": entry["fit_key"],
                "error_type": type(exc).__name__,
                "error": str(exc)[:500],
                "runtime_seconds": time.perf_counter() - attempt_started,
            })
            science_terminal = TERMINAL_GATE_FAIL
            break
        runtime = time.perf_counter() - attempt_started
        append_ledger_record(ledger_path, {
            "event": "FIT_COMPLETED",
            "recorded_utc": utc_now(),
            "attempt_index": entry["attempt_index"],
            "fit_key": entry["fit_key"],
            "runtime_seconds": runtime,
            "objective": outcome.objective,
            "best_step": outcome.best_step,
            "best_validation_loss": outcome.best_validation_loss,
        })
        outcomes[f"fit::{entry['fit_key']}"] = outcome
        prediction_store[entry["fit_key"]] = outcome.predictions.tolist()
        metrics_store[entry["fit_key"]] = {
            split: sci.evaluate_predictions(universe, entry["regime"], outcome.predictions,
                                            universe.blocks_for(split))
            for split in ("TRAIN", "VALIDATION", "TEST", "EXCLUDED_REFERENCE_ONLY")
        }

    science_wall_clock = time.perf_counter() - started_at

    fixed_metrics: dict[str, Any] = {}
    fixed_predictions: dict[str, Any] = {}
    for regime in ("S0", "S1"):
        pred = sci.fixed_baseline_predictions(universe, regime)
        fixed_predictions[regime] = pred.tolist()
        fixed_metrics[regime] = {
            split: sci.evaluate_predictions(universe, regime, pred, universe.blocks_for(split))
            for split in ("TRAIN", "VALIDATION", "TEST", "EXCLUDED_REFERENCE_ONLY")
        }

    ledger_records = read_ledger(ledger_path)
    summary = ledger_summary(ledger_records)
    constraints = _constraint_diagnostics(universe, metrics_store, fixed_metrics)
    determinism = _determinism_comparisons(universe, outcomes)

    complete = (summary["started_count"] == PLANNED_FIT_ATTEMPTS
                and summary["completed_count"] == PLANNED_FIT_ATTEMPTS
                and summary["failed_count"] == 0)
    gate_ok = bool(complete and science_wall_clock <= SCIENCE_WALL_CLOCK_CEILING_SECONDS
                   and constraints["row_normalization_ok"] and constraints["negativity_ok"]
                   and constraints["support_ok"] and constraints["split_counts_ok"]
                   and constraints["excluded_block_count_ok"]
                   and determinism["all_within_tolerance"])
    if not gate_ok:
        science_terminal = TERMINAL_GATE_FAIL

    raw = {
        "experiment_id": EXPERIMENT_ID,
        "issue": 77,
        "task_id": "DLH_WL_P2B_CLEAN_REPLICATION",
        "authority_marker": "DLH_WL_P2B_CLEAN_IMMUTABLE_REPLICATION_AUTHORIZED",
        "route": "DLH-WL-V1-20260918",
        "phase": "SCIENCE_STAGE",
        "recorded_utc": utc_now(),
        "pre_run_freeze_sha": pre_run_freeze_sha,
        "code_identity": {
            "operative_baseline": config.operative_baseline,
            "issue_77_operative_baseline": "38e8d75a918e859b36a363d309589a8bd6cf2b1b",
            "scientific_module_relpath": SCIENTIFIC_MODULE_RELPATH,
            "scientific_module_blob_sha1": module_blob,
            "p1a_module_blob_sha1": blob_sha1_lf(ROOT / P1A_MODULE_RELPATH),
            "config_relpath": CONFIG_RELPATH,
            "config_blob_sha1": config_blob,
            "config_sha256_lf": sha256_lf(ROOT / CONFIG_RELPATH),
            "contract_blob_sha1": blob_sha1_lf(ROOT / CONTRACT_RELPATH),
            "schema_blob_sha1": blob_sha1_lf(ROOT / SCHEMA_RELPATH),
            "config_revision": config.config_revision,
        },
        "environment": environment_summary(),
        "frozen_split_interpretation": {
            "split_counts": dict(config.split_counts),
            "blocking": "time and origin role only",
            "test_touches_train_time": False,
            "test_touches_train_origin": False,
            "test_regions_appear_as_train_destinations": True,
            "test_regions_are_unseen_regions": False,
            "generalization_claims_allowed": ["HELD_OUT_TIME", "HELD_OUT_ORIGIN_ROLE"],
            "generalization_claims_forbidden": ["FULLY_REGION_BLOCKED", "UNSEEN_REGION"],
        },
        "fit_plan": plan,
        "attempt_ledger_summary": summary,
        "attempt_ledger_records": ledger_records,
        "science_invocations": 1,
        "science_retries": 0,
        "science_wall_clock_seconds": science_wall_clock,
        "science_wall_clock_ceiling_seconds": SCIENCE_WALL_CLOCK_CEILING_SECONDS,
        "within_wall_clock_ceiling": bool(science_wall_clock <= SCIENCE_WALL_CLOCK_CEILING_SECONDS),
        "preprocessing": preprocessing,
        "targets": {"S0": universe.targets["S0"].tolist(),
                    "S1": universe.targets["S1"].tolist()},
        "m": universe.m.tolist(),
        "ell": universe.ell.tolist(),
        "support": universe.support.astype(int).tolist(),
        "predictions": prediction_store,
        "fixed_baseline_predictions": fixed_predictions,
        "metrics": metrics_store,
        "fixed_baseline_metrics": fixed_metrics,
        "fit_outcomes": {key: outcome.identity() for key, outcome in outcomes.items()},
        "determinism": determinism,
        "constraint_diagnostics": constraints,
        "p1a_accounting_checks": universe.p1a_diagnostics,
        "gate_ok": gate_ok,
        "terminal": science_terminal,
        "immutability": {
            "statement": "once written, this RAW_RESULTS file and the ATTEMPT_LEDGER are "
                         "immutable; rendering must never modify them",
            "science_runner_immutable_after_first_fit": True,
            "scientific_module_immutable_after_first_fit": True,
        },
        "not_an_acceptance": "raw scientific output; acceptance is decided by the Reviewer, "
                             "not by this artifact",
    }
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = raw_path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(raw, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    os.replace(tmp, raw_path)
    print(json.dumps({
        "phase": "SCIENCE_STAGE",
        "pre_run_freeze_sha": pre_run_freeze_sha,
        "science_invocations": 1,
        "started": summary["started_count"],
        "completed": summary["completed_count"],
        "failed": summary["failed_count"],
        "science_wall_clock_seconds": science_wall_clock,
        "gate_ok": gate_ok,
        "terminal": science_terminal,
        "ledger": LEDGER_RELPATH,
        "raw": RAW_RELPATH,
    }, indent=2))
    return 0 if gate_ok else 2


# --------------------------------------------------------------------------- validate
def validate_only() -> int:
    """Config/generator/module identity checks with zero optimizer steps."""
    config = sci.load_frozen_config(ROOT, config_relpath=CONFIG_RELPATH)
    universe = sci.build_universe(config, ROOT)
    report = sci.validate_only_report(universe)
    plan = build_fit_plan(config)
    ledger_path = ROOT / LEDGER_RELPATH
    payload = {
        "phase": "VALIDATE_ONLY",
        "optimizer_steps_performed": 0,
        "fit_attempts_performed": 0,
        "config_revision": config.config_revision,
        "config_blob_sha1": blob_sha1_lf(ROOT / CONFIG_RELPATH),
        "scientific_module_blob_sha1": blob_sha1_lf(ROOT / SCIENTIFIC_MODULE_RELPATH),
        "expected_scientific_module_blob_sha1": EXPECTED_SCIENTIFIC_MODULE_BLOB,
        "module_blob_status": (
            "MATCH" if blob_sha1_lf(ROOT / SCIENTIFIC_MODULE_RELPATH)
            == EXPECTED_SCIENTIFIC_MODULE_BLOB else "MISMATCH"),
        "planned_fit_attempts": len(plan),
        "fit_plan": plan,
        "contrast_rank": report["contrast_rank"],
        "s0_contrast_residual": report["s0_contrast_residual"],
        "s1_contrast_residual": report["s1_contrast_residual"],
        "split_counts": report["split_counts"],
        "reference_shares": report["reference_shares"],
        "ledger_present": ledger_path.exists(),
        "raw_present": (ROOT / RAW_RELPATH).exists(),
        "science_start_allowed": refuse_if_outputs_exist(ledger_path, ROOT / RAW_RELPATH) is None,
    }
    print(json.dumps(payload, indent=2)[:4000])
    print("\nVALIDATE_ONLY_COMPLETE__ZERO_OPTIMIZER_STEPS__ZERO_FITS")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="DLH-WL-P2B science runner (Issue #77)")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--validate-only", action="store_true",
                       help="config/generator/module identity checks; zero fits")
    group.add_argument("--execute-science", action="store_true",
                       help="the single authorized science invocation (exactly 12 fits)")
    parser.add_argument("--pre-run-freeze-sha", default="UNSPECIFIED",
                        help="PRE_RUN_FREEZE commit SHA this execution is identified by")
    args = parser.parse_args(argv)
    if args.validate_only:
        return validate_only()
    return execute_science(args.pre_run_freeze_sha)


if __name__ == "__main__":
    raise SystemExit(main())
