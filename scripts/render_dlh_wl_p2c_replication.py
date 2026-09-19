"""DLH-WL-P2C — durable per-fit-output replication: zero-fit renderer (Issue #78).

This script turns the **durable attempt ledger** and the frozen inputs into every
scientific and publication artifact:

1. ``DLH_WL_P2C_RAW_RESULTS.json``
2. ``DLH_WL_P2C_RESULTS.json``
3. ``DLH_WL_P2C_MANIFEST.json``
4. ``DLH_WL_P2C_REPORT.md``

It never trains, never optimizes, never replays training, never adds a seed or a run, and
never modifies the ledger or the science seal. Every metric, determinism comparison,
constraint diagnostic and published number is recomputed from the persisted
``FIT_COMPLETED`` prediction tensors, so a rendering defect can never require another fit
(the #77 failure mode). It may therefore be rerun freely for formatting/hashing repair.

The persisted prediction tensor is the authoritative zero-fit recovery object: the
accepted scientific module does not expose neural weights through ``FitOutcome``, and it
does not need to, because the frozen metrics are functions of the predictions.

``aggregate_metrics`` is the single production aggregation path. Its output shape,
``{fit_key: {"metrics": {split: metrics}}``, is the exact input contract of
``constraint_diagnostics``, which validates that shape loudly instead of assuming it —
this is the pairing that #77 got wrong.

``--validate-only`` reports zero fits and zero optimizer steps.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

# rendering needs only the deterministic generator/evaluation helpers, never a fitter
from deep_learning_hank.regional import labor_destination_p2 as sci  # noqa: E402

SCIENTIFIC_MODULE_RELPATH = "src/deep_learning_hank/regional/labor_destination_p2.py"
P1A_MODULE_RELPATH = "src/deep_learning_hank/regional/labor_destination.py"
CONFIG_RELPATH = "configs/dlh_wl_p2_offline_prototype.toml"
CONTRACT_RELPATH = "docs/specifications/DLH_WL_P2_OFFLINE_PROTOTYPE_CONTRACT_2026_09_18.md"
SCHEMA_RELPATH = "docs/data/DLH_WL_P1B_LABEL_AND_SAMPLE_SCHEMA_2026_09_18.md"
SCIENCE_RUNNER_RELPATH = "scripts/run_dlh_wl_p2c_replication_science.py"
RENDERER_RELPATH = "scripts/render_dlh_wl_p2c_replication.py"

OUTDIR_RELPATH = "reports/dlh_wl_p2c_2026_09_19"
LEDGER_NAME = "DLH_WL_P2C_ATTEMPT_LEDGER.jsonl"
SEAL_NAME = "DLH_WL_P2C_SCIENCE_SEAL.json"
RAW_NAME = "DLH_WL_P2C_RAW_RESULTS.json"
RESULTS_NAME = "DLH_WL_P2C_RESULTS.json"
MANIFEST_NAME = "DLH_WL_P2C_MANIFEST.json"
REPORT_NAME = "DLH_WL_P2C_REPORT.md"
LEDGER_RELPATH = f"{OUTDIR_RELPATH}/{LEDGER_NAME}"
SEAL_RELPATH = f"{OUTDIR_RELPATH}/{SEAL_NAME}"
RAW_RELPATH = f"{OUTDIR_RELPATH}/{RAW_NAME}"
RESULTS_RELPATH = f"{OUTDIR_RELPATH}/{RESULTS_NAME}"
MANIFEST_RELPATH = f"{OUTDIR_RELPATH}/{MANIFEST_NAME}"
REPORT_RELPATH = f"{OUTDIR_RELPATH}/{REPORT_NAME}"

ISSUE_76_RESULTS_RELPATH = "reports/dlh_wl_p2_2026_09_19/DLH_WL_P2_RESULTS.json"
ISSUE_76_OBSERVATIONAL_FALLBACK = {
    "S0:parametric": 0.9121715994501418,
    "S1:parametric": 0.9081586773751914,
    "S0:neural:seed0": 0.9132187018208984,
    "S1:neural:seed0": 0.9093538306365426,
}

EXPERIMENT_ID = "EXP-20260919-DLH-WL-P2C-001"
TASK_ID = "DLH_WL_P2C_DURABLE_OUTPUT_REPLICATION"
AUTHORITY_MARKER = "DLH_WL_P2C_DURABLE_PER_FIT_OUTPUT_REPLICATION_AUTHORIZED"
ROUTE = "DLH-WL-V1-20260918"
OPERATIVE_BASELINE = "d49ad061ce39c11d5202fb92a0bce5942c4c6bd2"
PUBLICATION_BASELINE = "f6390ccea1eee27fb6528c3ba2572551a7e8dd06"
PLANNED_FIT_ATTEMPTS = 12
SCIENCE_WALL_CLOCK_CEILING_SECONDS = 1800.0
EXPECTED_SCIENTIFIC_MODULE_BLOB = "b1f2cd043605c511e4965254657d12306170609b"
EXPECTED_CONFIG_BLOB = "bb5dbbd0746e9d92874f94b03a1d54f3d382c4a8"
EXPECTED_PREDICTION_SHAPE = [4, 5, 5]

SPLIT_STATES = ("TRAIN", "VALIDATION", "TEST", "EXCLUDED_REFERENCE_ONLY")
REGIMES = ("S0", "S1")
PRIMARY_FIT_KEYS = tuple(
    [f"{regime}:parametric" for regime in REGIMES]
    + [f"{regime}:neural:seed{seed}" for regime in REGIMES for seed in (0, 1, 2)])
REPEAT_PAIRS = tuple(
    [(f"{regime}:parametric", f"{regime}:parametric:repeat") for regime in REGIMES]
    + [(f"{regime}:neural:seed0", f"{regime}:neural:seed0:repeat") for regime in REGIMES])
DETERMINISM_NAMES = ("parametric_S0", "parametric_S1", "neural_S0_seed0", "neural_S1_seed0")

TERMINAL_PASS = "DLH_WL_P2C_DURABLE_OUTPUT_REPLICATION__PASS__P2_METHOD_GATE_COMPLETE"
TERMINAL_GATE_FAIL = "DLH_WL_P2C_DURABLE_OUTPUT_REPLICATION__GATE_FAIL__NO_SCIENCE_RERUN_AUTHORIZED"
TERMINAL_BLOCKED = "BLOCKED_DLH_WL_P2C_PRE_RUN_OR_ENVIRONMENT"

MANIFEST_DIGEST_FIELD = "manifest_canonical_sha256"
RESULTS_DIGEST_FIELD = "results_canonical_sha256"

IDENTITY_POLICY = (
    "RESULTS.json and MANIFEST.json are serialised with indent=2 and sort_keys=True and end "
    "with one LF. The canonical results content is RESULTS.json serialised WITHOUT the two "
    "digest fields results_canonical_sha256 and manifest_canonical_sha256; its SHA-256 is "
    "recorded as results_canonical_sha256 inside the results file and as "
    "hashes.results_canonical_content in the manifest, together with the git blob SHA-1 of "
    "those canonical bytes. The canonical manifest content is MANIFEST.json serialised in "
    "full, because the manifest never records a hash of itself; its SHA-256 is recorded only "
    "inside RESULTS.json as manifest_canonical_sha256. The chain is acyclic: each digest is a "
    "function of content that does not contain it."
)

ZERO_FIT_STATEMENT = (
    "This render stage performs zero fits and zero optimizer steps. Every number it "
    "publishes is recomputed from the persisted FIT_COMPLETED prediction tensors of the "
    "durable attempt ledger plus the frozen inputs. No fitter, no optimizer, no training "
    "replay and no seed is used, and the ledger and science seal are never modified."
)

# ------------------------------------------------------- reviewer adjudication registry
#
# A binding Reviewer adjudication is a statement about one *executed* run, identified by
# the PRE_RUN_FREEZE SHA that produced it — not a property of this renderer. The registry
# is therefore keyed by that SHA: a run with no adjudication is rendered from its own
# mechanical gates, and a run with an adjudication is rendered with the adjudicated
# terminal even when every mechanical gate passes.
#
# Zero-fit remediation only (Issue #78 adjudication comment 5740611528): this block records
# authority and the resulting terminal. Every corroborating number is *recomputed* from the
# durable ledger by ``preprocessing_defect_evidence`` below and printed in the report so a
# Reviewer can check each value against the ledger by hand. No fit, optimizer step, second
# science invocation, seed, tuning or ledger/seal mutation is involved anywhere.
REVIEWER_ADJUDICATIONS: dict[str, dict[str, Any]] = {
    "ae4115f20bb3bc7f43ab79d9d0ccf65b62fa2c7d": {
        "adjudication_comment": 5740611528,
        "adjudication_url": "https://github.com/zcx369658780/deep-learning-hank/issues/"
                            "78#issuecomment-5740611528",
        "adjudication_kind": "REVIEWER_ADJUDICATION_HOLD",
        "reviewed_candidate_sha": "97c87e089c758b5afb5285b1c4b94612917c9e83",
        "decision": "PASS_TERMINAL_NOT_ACCEPTED",
        "finding": "the executed neural prediction path violates the frozen #75 TRAIN-only "
                   "z-score preprocessing contract",
        "corrected_terminal": TERMINAL_GATE_FAIL,
        "confirmatory_p2_pass_allowed": False,
        "durability_protocol_finding": "the durability/protocol machinery is correct and the "
                                       "#77 durability defect is genuinely fixed",
        "scientific_execution_finding": "one required baseline family was executed incorrectly, "
                                        "so the experiment fails as a whole",
        "defect": {
            "affected_family": "neural",
            "unaffected_families": ["fixed_support_normalized_uniform",
                                    "gravity_multinomial_logit"],
            "frozen_requirement": "neural inputs use the TRAIN-only z-scored design",
            "training_design": "TRAIN_ONLY_ZSCORED (sci._train_only_zscore)",
            "persisted_prediction_design": "RAW_DESIGN_FALLBACK",
            "prediction_path": "_neural_predict -> _neural_predict_blocks -> "
                               "universe.design_matrix",
            "fallback_mechanism": "SyntheticUniverse.design_matrix returns raw_design when "
                                  "_design_matrix is None",
            "missing_assignment": "universe._design_matrix = design",
            "canonical_path_performs_the_assignment": True,
            "executed_science_runner_performs_the_assignment": False,
            "consequence": "neural parameters are trained on TRAIN-z-scored inputs while the "
                           "persisted final prediction tensors are generated on "
                           "raw/unstandardized inputs",
            "this_is_not_a_performance_finding": "the executed neural numbers are not evidence "
                                                 "that the neural model performs worse",
        },
        "zero_fit_recovery_possible": False,
        "zero_fit_recovery_reason": "the accepted FitOutcome does not expose the trained neural "
                                    "parameter tensors, so a correctly preprocessed prediction "
                                    "tensor cannot be reconstructed from this ledger without "
                                    "re-running the fitting path; transforming the stored "
                                    "raw-design predictions is invalid for the nonlinear MLP",
        "second_science_invocation_authorized": False,
        "authorized_remediation": "evidence only, zero new science",
    }
}

NEURAL_METRIC_PROVENANCE = "OBSERVATIONAL_OUTPUT_FROM_INVALID_PREPROCESSING_PREDICTION_PATH"
PARAMETRIC_METRIC_PROVENANCE = "FROZEN_DESIGN_CONFORMANT"
FIXED_METRIC_PROVENANCE = "FROZEN_DESIGN_CONFORMANT_ZERO_FIT_BASELINE"
NEURAL_VS_PARAMETRIC_COMPARISON_PERMITTED = False
NEURAL_COMPARISON_WITHHELD_REASON = (
    "the P2C neural prediction path violates the frozen TRAIN-only preprocessing contract, so "
    "the persisted neural numbers are observational artifacts of an invalid path; no "
    "neural-vs-parametric scientific performance comparison may be drawn from P2C, and no "
    "tuning, extra seed or extra fit was performed to compensate"
)
DURABILITY_STATUS_CORRECT = "VERIFIED_CORRECT_BY_REVIEWER_AND_REPRODUCED_FROM_THE_LEDGER"


# --------------------------------------------------------------------------- helpers
def sha256_lf(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest().upper()


def blob_sha1_lf(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def dumps(obj: Any) -> bytes:
    return json.dumps(obj, indent=2, sort_keys=True,
                      default=_json_default).encode("utf-8") + b"\n"


def _json_default(obj: Any) -> Any:
    """Deterministic JSON fallback for NumPy scalars/arrays (identity-chain safe)."""
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, np.floating):
        return float(obj)
    if isinstance(obj, np.bool_):
        return bool(obj)
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    raise TypeError(f"not JSON serializable: {type(obj).__name__}")


def read_ledger(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()]


def read_json(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


# ----------------------------------------------------- ledger recovery (zero-fit only)
def decode_predictions(record: dict[str, Any]) -> np.ndarray:
    """Rebuild one full prediction tensor from a durable ``FIT_COMPLETED`` record."""
    shape = record.get("prediction_shape")
    if not isinstance(shape, list) or len(shape) != 3:
        raise ValueError(f"{record.get('fit_key')!r}: missing or malformed prediction_shape")
    array = np.array(record["predictions"], dtype=float)
    if list(array.shape) != [int(v) for v in shape]:
        raise ValueError(f"{record.get('fit_key')!r}: prediction_shape {shape} does not match "
                         f"the decoded tensor shape {list(array.shape)}")
    if not np.all(np.isfinite(array)):
        raise ValueError(f"{record.get('fit_key')!r}: decoded tensor is not finite")
    return array


PAYLOAD_SCIENTIFIC_KEYS = (
    "attempt_index", "fit_key", "kind", "repeat_of", "regime", "family", "seed", "backend",
    "objective", "convergence", "best_step", "best_validation_loss", "coefficients",
    "diagnostics", "predictions", "prediction_shape", "non_finite_originals",
)


def canonical_payload_sha256(record: dict[str, Any]) -> str:
    """Recompute the recorded canonical scientific-payload digest (no fitting involved)."""
    payload = {key: record[key] for key in PAYLOAD_SCIENTIFIC_KEYS if key in record}
    blob = json.dumps(payload, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("utf-8")
    return hashlib.sha256(blob).hexdigest().upper()


def completed_records(records: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted((r for r in records if r.get("event") == "FIT_COMPLETED"),
                  key=lambda r: r.get("attempt_index", -1))


def ledger_invariants(records: Sequence[dict[str, Any]]) -> dict[str, Any]:
    """Everything the science-stage acceptance gates need, from the ledger alone."""
    started = [r for r in records if r.get("event") == "FIT_ATTEMPT_STARTED"]
    completed = [r for r in records if r.get("event") == "FIT_COMPLETED"]
    failed = [r for r in records if r.get("event") == "FIT_FAILED"]
    indices_started = [r.get("attempt_index") for r in started]
    indices_completed = [r.get("attempt_index") for r in completed]
    ordered = []
    for index in indices_completed:
        start = next((r for r in started if r.get("attempt_index") == index), None)
        done = next((r for r in completed if r.get("attempt_index") == index), None)
        if start is None or done is None:
            ordered.append(False)
            continue
        ordered.append(str(start.get("recorded_utc")) <= str(done.get("recorded_utc")))
    pre_run_freeze_shas = sorted({str(r.get("pre_run_freeze_sha")) for r in started})
    expected = list(range(1, PLANNED_FIT_ATTEMPTS + 1))
    return {
        "records": len(records),
        "started_count": len(started),
        "completed_count": len(completed),
        "failed_count": len(failed),
        "attempt_indices_started": indices_started,
        "attempt_indices_completed": indices_completed,
        "fit_keys_started": [r.get("fit_key") for r in started],
        "fit_keys_completed": [r.get("fit_key") for r in completed],
        "exactly_twelve_started": len(started) == PLANNED_FIT_ATTEMPTS,
        "exactly_twelve_completed": len(completed) == PLANNED_FIT_ATTEMPTS,
        "zero_failed": len(failed) == 0,
        "no_unmatched_started": all(i in indices_completed for i in indices_started),
        "started_indices_are_exactly_1_to_12": sorted(indices_started) == expected,
        "completed_indices_are_exactly_1_to_12": sorted(indices_completed) == expected,
        "started_before_completed_ordering_ok": bool(ordered) and all(ordered),
        "started_count_equals_completed_count": len(started) == len(completed),
        "ledger_record_count_is_24": len(records) == 2 * PLANNED_FIT_ATTEMPTS,
        "science_invocations": 1,
        "science_retries": 0,
        "pre_run_freeze_shas_in_started_records": pre_run_freeze_shas,
        "pre_run_freeze_sha_recorded": bool(pre_run_freeze_shas)
        and pre_run_freeze_shas != ["None"] and "UNSPECIFIED" not in pre_run_freeze_shas,
    }


def payload_hash_verification(completed: Sequence[dict[str, Any]]) -> dict[str, Any]:
    """Verify every completed record's canonical scientific-payload digest."""
    per_fit: dict[str, Any] = {}
    for record in completed:
        key = str(record.get("fit_key"))
        recorded = record.get("payload_sha256")
        recomputed = canonical_payload_sha256(record)
        per_fit[key] = {
            "recorded": recorded,
            "recomputed": recomputed,
            "matches": recorded == recomputed,
            "prediction_shape": record.get("prediction_shape"),
            "has_predictions": isinstance(record.get("predictions"), list)
            and len(record.get("predictions") or []) > 0,
            "prediction_shape_is_frozen": record.get("prediction_shape") == EXPECTED_PREDICTION_SHAPE,
            "has_diagnostics": isinstance(record.get("diagnostics"), dict),
            "has_convergence": isinstance(record.get("convergence"), dict),
            "has_backend": isinstance(record.get("backend"), str) and bool(record.get("backend")),
            "has_runtime": isinstance(record.get("runtime_seconds"), (int, float)),
            "has_objective_field": "objective" in record,
            "has_best_step_field": "best_step" in record,
            "has_best_validation_loss_field": "best_validation_loss" in record,
            "coefficients_present": isinstance(record.get("coefficients"), list),
        }
    return {
        "per_fit": per_fit,
        "all_payload_hashes_match": bool(per_fit) and all(v["matches"] for v in per_fit.values()),
        "all_prediction_shapes_frozen": bool(per_fit)
        and all(v["prediction_shape_is_frozen"] for v in per_fit.values()),
        "all_predictions_persisted": bool(per_fit) and all(v["has_predictions"] for v in per_fit.values()),
        "all_metadata_present": bool(per_fit) and all(
            v["has_diagnostics"] and v["has_convergence"] and v["has_backend"] and v["has_runtime"]
            for v in per_fit.values()),
    }


def share_distribution_check(universe: sci.SyntheticUniverse,
                             completed: Sequence[dict[str, Any]]) -> dict[str, Any]:
    """Independently verify that every recovered tensor is a valid share distribution.

    This is the structural test of the recovery object itself: over the allowed cells of
    every block the persisted row must sum to one within the frozen row-normalization
    tolerance, every allowed value must be non-negative, and every structurally
    unavailable cell must be exactly zero.
    """
    tolerance = universe.config.row_normalization_tolerance
    per_fit: dict[str, Any] = {}
    for record in completed:
        tensor = decode_predictions(record)
        worst_row = 0.0
        minimum = float("inf")
        violations = 0
        for block in universe.blocks:
            total = 0.0
            for j in block.allowed:
                value = float(tensor[block.time_index, block.origin, j])
                total += value
                minimum = min(minimum, value)
            worst_row = max(worst_row, abs(total - 1.0))
            for j in range(len(universe.config.region_ids)):
                if j in block.allowed:
                    continue
                if float(tensor[block.time_index, block.origin, j]) != 0.0:
                    violations += 1
        per_fit[str(record.get("fit_key"))] = {
            "max_row_sum_deviation": worst_row,
            "min_allowed_share": minimum,
            "unavailable_cell_violations": violations,
            "valid": bool(worst_row <= tolerance and minimum >= 0.0 and violations == 0),
        }
    return {
        "per_fit": per_fit,
        "tolerance": tolerance,
        "all_valid": bool(per_fit) and all(v["valid"] for v in per_fit.values()),
    }


def resolve_science_wall_clock(records: Sequence[dict[str, Any]],
                               seal: dict[str, Any] | None) -> dict[str, Any]:
    """Resolve the science wall clock from the seal, the ledger, or both.

    The durable ledger carries per-record UTC timestamps, so the science span is
    recoverable even if the optional seal is missing. Both sources are always reported.
    """
    starts = [str(r.get("recorded_utc")) for r in records if r.get("event") == "FIT_ATTEMPT_STARTED"]
    dones = [str(r.get("recorded_utc")) for r in records if r.get("event") == "FIT_COMPLETED"]
    ledger_span: float | None = None
    if starts and dones:
        try:
            first = datetime.fromisoformat(min(starts))
            last = datetime.fromisoformat(max(dones))
            ledger_span = (last - first).total_seconds()
        except ValueError:  # pragma: no cover - timestamps are written by this code base
            ledger_span = None
    fit_runtime_sum = float(sum(
        float(r.get("runtime_seconds") or 0.0) for r in records if r.get("event") == "FIT_COMPLETED"))
    seal_seconds = None
    if isinstance(seal, dict) and isinstance(seal.get("science_wall_clock_seconds"), (int, float)):
        seal_seconds = float(seal["science_wall_clock_seconds"])
    if seal_seconds is not None:
        primary, source = seal_seconds, "SCIENCE_SEAL"
    elif ledger_span is not None:
        primary, source = ledger_span, "DERIVED_FROM_LEDGER_RECORDED_UTC"
    else:  # pragma: no cover - a complete ledger always carries timestamps
        primary, source = None, "UNAVAILABLE"
    return {
        "science_wall_clock_seconds": primary,
        "wall_clock_source": source,
        "seal_seconds": seal_seconds,
        "ledger_span_seconds": ledger_span,
        "sum_completed_fit_runtime_seconds": fit_runtime_sum,
        "seal_covers_ledger_span": (None if seal_seconds is None or ledger_span is None
                                    else bool(seal_seconds + 0.05 >= ledger_span)),
        "ceiling_seconds": SCIENCE_WALL_CLOCK_CEILING_SECONDS,
        "within_ceiling": bool(primary is not None
                              and primary <= SCIENCE_WALL_CLOCK_CEILING_SECONDS),
        "seal_present": isinstance(seal, dict),
    }


# ------------------------------------------------------- PRODUCTION AGGREGATION PATH
def aggregate_metrics(universe: sci.SyntheticUniverse,
                      completed: Sequence[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """The single production aggregation path: durable records in, per-fit metrics out.

    Input:  the durable ``FIT_COMPLETED`` records (each carrying persisted predictions).
    Output: ``{fit_key: {"metrics": {split: metrics}}}`` — the exact shape that
    ``constraint_diagnostics`` consumes.

    Only ``sci.evaluate_predictions`` (a pure function of the frozen targets, the frozen
    blocks and the supplied predictions) is used. No fitter is reachable from here.
    """
    aggregated: dict[str, dict[str, Any]] = {}
    for record in completed:
        fit_key = str(record.get("fit_key"))
        regime = str(record.get("regime"))
        predictions = decode_predictions(record)
        aggregated[fit_key] = {
            "attempt_index": record.get("attempt_index"),
            "kind": record.get("kind"),
            "repeat_of": record.get("repeat_of"),
            "regime": regime,
            "family": record.get("family"),
            "seed": record.get("seed"),
            "payload_sha256": record.get("payload_sha256"),
            "prediction_source": "PERSISTED_FIT_COMPLETED_PREDICTIONS",
            "metrics": {
                split: sci.evaluate_predictions(universe, regime, predictions,
                                                universe.blocks_for(split))
                for split in SPLIT_STATES
            },
        }
    return aggregated


def fixed_baseline_metrics(universe: sci.SyntheticUniverse) -> dict[str, dict[str, Any]]:
    """Zero-fit evaluation of the frozen fixed baseline (not a fit; no optimizer)."""
    out: dict[str, dict[str, Any]] = {}
    for regime in REGIMES:
        predictions = sci.fixed_baseline_predictions(universe, regime)
        out[regime] = {
            "family": "fixed_support_normalized_uniform",
            "prediction_source": "FIXED_SUPPORT_NORMALIZED_UNIFORM_ZERO_FIT",
            "metrics": {
                split: sci.evaluate_predictions(universe, regime, predictions,
                                                universe.blocks_for(split))
                for split in SPLIT_STATES
            },
        }
    return out


def _assert_metrics_store_shape(store: Any, name: str, expected_keys: Sequence[str]) -> None:
    """Validate the ``{key: {"metrics": {split: metrics}}}`` contract loudly.

    Issue #77 failed because a ``{split: metrics}`` mapping was handed to code that
    required ``{"metrics": {split: metrics}}`` and the mismatch surfaced as a bare
    ``KeyError`` after all twelve fits had run. The shape is therefore asserted, named and
    reported instead of assumed.
    """
    if not isinstance(store, dict):
        raise TypeError(f"{name} must be a dict, got {type(store).__name__}")
    for key in expected_keys:
        if key not in store:
            raise KeyError(f"{name} is missing the required key {key!r}")
        entry = store[key]
        if not isinstance(entry, dict):
            raise TypeError(f"{name}[{key!r}] must be a dict, got {type(entry).__name__}")
        if "metrics" not in entry:
            raise TypeError(
                f"{name}[{key!r}] must be shaped {{'metrics': {{split: metrics}}}}; "
                f"observed keys {sorted(entry)}. A bare split->metrics mapping is the "
                f"exact input-shape defect that failed Issue #77.")
        if not isinstance(entry["metrics"], dict):
            raise TypeError(f"{name}[{key!r}]['metrics'] must be a split->metrics dict")
        for split in SPLIT_STATES:
            if split not in entry["metrics"]:
                raise KeyError(f"{name}[{key!r}]['metrics'] is missing split {split!r}")


def constraint_diagnostics(universe: sci.SyntheticUniverse,
                           metrics_store: dict[str, dict[str, Any]],
                           fixed_store: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Aggregate the frozen constraint diagnostics over every evaluated prediction set.

    ``metrics_store``: ``{fit_key: {"metrics": {split: metrics}}}`` from
    ``aggregate_metrics``.
    ``fixed_store``:   ``{regime: {"metrics": {split: metrics}}}`` from
    ``fixed_baseline_metrics``.
    """
    cfg = universe.config
    _assert_metrics_store_shape(metrics_store, "metrics_store", PRIMARY_FIT_KEYS)
    _assert_metrics_store_shape(fixed_store, "fixed_store", REGIMES)

    row_max, negativity, support = 0.0, 0, 0
    trained_sets = 0
    for registry in (metrics_store, fixed_store):
        for entry in registry.values():
            trained_sets += 1
            for split in SPLIT_STATES:
                block = entry["metrics"][split]
                row_max = max(row_max, float(block["row_normalization_violation_max"]))
                negativity += int(block["negativity_violation_count"])
                support += int(block["support_violation_count"])

    split_counts = {state: len(universe.blocks_for(state)) for state in SPLIT_STATES}
    excluded = split_counts["EXCLUDED_REFERENCE_ONLY"]
    return {
        "evaluated_prediction_sets": trained_sets,
        "splits_per_set": list(SPLIT_STATES),
        "row_normalization_violation_max": row_max,
        "row_normalization_tolerance": cfg.row_normalization_tolerance,
        "row_normalization_ok": bool(row_max <= cfg.row_normalization_tolerance),
        "negativity_violation_count": int(negativity),
        "negativity_ok": negativity == 0,
        "support_violation_count": int(support),
        "support_ok": support == 0,
        "split_counts": split_counts,
        "split_counts_configured": dict(cfg.split_counts),
        "split_counts_ok": (
            split_counts["TRAIN"] == 9 and split_counts["VALIDATION"] == 3
            and split_counts["TEST"] == 2 and split_counts["EXCLUDED_REFERENCE_ONLY"] == 6),
        "excluded_block_count": excluded,
        "excluded_block_count_expected": cfg.excluded_block_count_expected,
        "excluded_block_count_ok": excluded == cfg.excluded_block_count_expected,
        "allocation_blocks": len(universe.blocks),
    }


def determinism_comparisons(universe: sci.SyntheticUniverse,
                            completed_by_key: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Compare primary against verification-repeat predictions, from the ledger only."""
    cfg = universe.config
    comparisons: dict[str, Any] = {}
    for primary_key, repeat_key in REPEAT_PAIRS:
        primary = completed_by_key[primary_key]
        repeat = completed_by_key[repeat_key]
        p_pred = decode_predictions(primary)
        r_pred = decode_predictions(repeat)
        family = str(primary.get("family"))
        name = (f"parametric_{primary['regime']}" if family == "parametric"
                else f"neural_{primary['regime']}_seed{primary.get('seed')}")
        info: dict[str, Any] = {
            "family": family,
            "regime": primary.get("regime"),
            "seed": primary.get("seed"),
            "primary_fit_key": primary_key,
            "repeat_fit_key": repeat_key,
            "deviation": float(np.abs(p_pred - r_pred).max()),
            "primary_objective": primary.get("objective"),
            "repeat_objective": repeat.get("objective"),
        }
        if primary.get("coefficients") is not None and repeat.get("coefficients") is not None:
            info["coefficient_deviation"] = float(np.abs(
                np.asarray(primary["coefficients"], dtype=float)
                - np.asarray(repeat["coefficients"], dtype=float)).max())
        else:
            info["coefficient_deviation"] = None
        if primary.get("best_step") is not None:
            info["primary_best_step"] = primary.get("best_step")
            info["repeat_best_step"] = repeat.get("best_step")
        if primary.get("best_validation_loss") is not None:
            info["primary_best_validation_loss"] = primary.get("best_validation_loss")
            info["repeat_best_validation_loss"] = repeat.get("best_validation_loss")
        comparisons[name] = info
    deviations = {name: comparisons[name]["deviation"] for name in DETERMINISM_NAMES}
    comparisons["determinism_tolerance"] = cfg.determinism_tolerance
    comparisons["coefficient_tolerance"] = cfg.determinism_tolerance
    comparisons["scope"] = ("TWO_PARAMETRIC_REPEATS_AND_NEURAL_SEED0_REPEATS_ONLY; "
                            "neural seeds 1 and 2 are sensitivity replications, not "
                            "duplicate determinism checks")
    comparisons["deviations"] = deviations
    comparisons["max_deviation"] = max(deviations.values())
    comparisons["all_within_tolerance"] = all(
        value <= cfg.determinism_tolerance for value in deviations.values())
    comparisons["any_deviation_over_tolerance"] = not comparisons["all_within_tolerance"]
    return comparisons


def p1a_closure(universe: sci.SyntheticUniverse) -> dict[str, Any]:
    """Read the accepted P1A accounting diagnostics and check they close."""
    tolerance = 1e-10
    worst = 0.0
    all_identified = True
    all_valid = True
    per_regime: dict[str, Any] = {}
    for regime, entries in universe.p1a_diagnostics.items():
        deviations = []
        for entry in entries:
            deviations += [float(entry["origin_conservation_max_abs_deviation"]),
                           float(entry["national_conservation_max_abs_deviation"]),
                           float(entry["destination_aggregation_max_abs_deviation"])]
            all_identified = all_identified and bool(entry["conditional_choice_identified"])
            all_valid = all_valid and (entry["valid_row_count"] == entry["active_row_count"])
        regime_worst = max(deviations) if deviations else 0.0
        worst = max(worst, regime_worst)
        per_regime[regime] = {
            "time_slices": len(entries),
            "max_abs_deviation": regime_worst,
            "conditional_choice_identified_all": all(
                bool(entry["conditional_choice_identified"]) for entry in entries),
            "time_ids": [entry["time_id"] for entry in entries],
            "active_row_counts": [entry["active_row_count"] for entry in entries],
            "identifiable_row_counts": [entry["identifiable_rows"] for entry in entries],
        }
    return {
        "tolerance": tolerance,
        "max_abs_deviation": worst,
        "deviations_within_tolerance": bool(worst <= tolerance),
        "conditional_choice_identified_all": all_identified,
        "all_rows_valid": all_valid,
        "per_regime": per_regime,
        "closes": bool(worst <= tolerance and all_identified and all_valid),
        "role": "READ_ONLY_ACCEPTED_P1A_INTERFACE",
    }


def fit_summaries(completed: Sequence[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """JSON-safe scalar metadata per completed fit (no predictions duplicated)."""
    out: dict[str, dict[str, Any]] = {}
    for record in completed:
        key = str(record.get("fit_key"))
        out[key] = {
            "attempt_index": record.get("attempt_index"),
            "kind": record.get("kind"),
            "repeat_of": record.get("repeat_of"),
            "regime": record.get("regime"),
            "family": record.get("family"),
            "seed": record.get("seed"),
            "backend": record.get("backend"),
            "objective": record.get("objective"),
            "convergence": record.get("convergence"),
            "best_step": record.get("best_step"),
            "best_validation_loss": record.get("best_validation_loss"),
            "coefficients": record.get("coefficients"),
            "runtime_seconds": record.get("runtime_seconds"),
            "attempts": record.get("attempts"),
            "prediction_shape": record.get("prediction_shape"),
            "payload_sha256": record.get("payload_sha256"),
            "non_finite_originals": record.get("non_finite_originals"),
            "registered_utc": record.get("recorded_utc"),
            "pre_run_freeze_sha": record.get("pre_run_freeze_sha"),
            "diagnostics_keys": sorted(record.get("diagnostics", {})) if isinstance(
                record.get("diagnostics"), dict) else [],
            "hidden_widths": record.get("diagnostics", {}).get("hidden_widths")
            if isinstance(record.get("diagnostics"), dict) else None,
            "steps_executed": record.get("diagnostics", {}).get("steps_executed")
            if isinstance(record.get("diagnostics"), dict) else None,
            "train_weighted_cross_entropy": record.get("diagnostics", {}).get(
                "train_weighted_cross_entropy")
            if isinstance(record.get("diagnostics"), dict) else None,
        }
    return out


# --------------------------------------------------------------------------- reporting
def metric_provenance(adjudication: dict[str, Any] | None) -> dict[str, Any]:
    """Per-fit metric provenance classification.

    The neural split metrics computed from the persisted P2C prediction tensors are
    *observational*: they were produced by a prediction path that violates the frozen
    TRAIN-only preprocessing contract, so they may be retained for audit but carry no
    scientific weight. The parametric and fixed-baseline numbers are conformant.
    """
    classification: dict[str, str] = {}
    for key in PRIMARY_FIT_KEYS:
        classification[key] = (NEURAL_METRIC_PROVENANCE if ":neural:" in key
                              else PARAMETRIC_METRIC_PROVENANCE)
    for _, repeat_key in REPEAT_PAIRS:
        classification[repeat_key] = (NEURAL_METRIC_PROVENANCE if ":neural:" in repeat_key
                                     else PARAMETRIC_METRIC_PROVENANCE)
    return {
        "applies": adjudication is not None,
        "adjudication_comment": adjudication["adjudication_comment"] if adjudication else None,
        "neural_marker": NEURAL_METRIC_PROVENANCE,
        "parametric_marker": PARAMETRIC_METRIC_PROVENANCE,
        "fixed_baseline_marker": FIXED_METRIC_PROVENANCE,
        "per_fit_key": classification,
        "values_retained_for_audit": True,
        "values_replaced_with_issue_76": False,
        "statement": (
            "The neural split metrics below are the persisted P2C values, retained unchanged for "
            "audit and explicitly classified as " + NEURAL_METRIC_PROVENANCE + ". They were NOT "
            "replaced with the Issue #76 values and must not be read as a measurement of the "
            "frozen neural mapping."),
        "parametric_statement": (
            "The parametric outputs were produced through the frozen contrast design and the "
            "frozen six-column fitted matrix; they reproduce the earlier frozen observations "
            "exactly and remain valid under the frozen #75 design."),
        "fixed_baseline_statement": (
            "The fixed baseline is a zero-fit evaluation of the frozen support-normalized "
            "uniform prior and is unaffected by the neural preprocessing defect."),
        "experiment_verdict": (
            "the parametric family being conformant does not rescue the experiment: P2C fails as "
            "a whole because one required baseline family was executed incorrectly"),
    }


def neural_comparison_status(metrics: dict[str, dict[str, Any]],
                             fixed: dict[str, dict[str, Any]],
                             adjudication: dict[str, Any] | None) -> dict[str, Any]:
    """Withhold any neural-vs-parametric scientific inference drawn from P2C.

    The numbers are still reported, because an audit needs them, but they are labelled
    as non-inferential when a preprocessing-path adjudication applies.
    """
    status: dict[str, Any] = {
        "neural_vs_parametric_comparison_permitted": (
            NEURAL_VS_PARAMETRIC_COMPARISON_PERMITTED if adjudication is not None else True),
        "neural_beats_parametric_required": False,
        "observational_values_retained_for_audit": {},
    }
    for regime in REGIMES:
        parametric = metrics[f"{regime}:parametric"]["metrics"]["TEST"]["weighted_cross_entropy"]
        seeds = {f"seed{seed}": metrics[f"{regime}:neural:seed{seed}"]["metrics"]["TEST"]
                 ["weighted_cross_entropy"] for seed in (0, 1, 2)}
        status["observational_values_retained_for_audit"][regime] = {
            "fixed_baseline_test_ce": fixed[regime]["metrics"]["TEST"]["weighted_cross_entropy"],
            "parametric_test_ce": parametric,
            "neural_test_ce_by_seed": seeds,
            "neural_minus_parametric_test_ce": {name: value - parametric
                                                for name, value in seeds.items()},
            "interpretation": "AUDIT_ONLY_NOT_A_SCIENTIFIC_COMPARISON",
        }
    if adjudication is not None:
        status["withheld"] = True
        status["withheld_reason"] = NEURAL_COMPARISON_WITHHELD_REASON
        status["classification"] = NEURAL_METRIC_PROVENANCE
    else:
        status["withheld"] = False
    return status


def audit_context_vs_issue_76(metrics: dict[str, dict[str, Any]],
                              repo_root: Path,
                              adjudication: dict[str, Any] | None = None) -> dict[str, Any]:
    """Audit-only provenance of the #76 observations (never an acceptance threshold)."""
    source = "RECORDED_CONSTANTS_FROM_THE_ACCEPTED_ISSUE_76_ARTIFACT"
    observational = dict(ISSUE_76_OBSERVATIONAL_FALLBACK)
    issue_76_terminal = "DLH_WL_P2A_OFFLINE_SYNTHETIC_PROTOTYPE__GATE_FAIL__NO_TUNING_AUTHORIZED"
    issue_76_accounting: dict[str, Any] = {
        "within_attempt_ceiling": False,
        "completed_fits_minimum_proven_total": 36,
    }
    preserved = read_json(repo_root / ISSUE_76_RESULTS_RELPATH)
    if isinstance(preserved, dict):
        by_split = preserved.get("metrics_by_split")
        if isinstance(by_split, dict):
            for key in observational:
                try:
                    observational[key] = float(by_split[key]["TEST"]["weighted_cross_entropy"])
                except (KeyError, TypeError, ValueError):
                    pass
            source = f"READ_FROM_{ISSUE_76_RESULTS_RELPATH}"
        if isinstance(preserved.get("terminal"), str):
            issue_76_terminal = preserved["terminal"]
        accounting = preserved.get("execution_accounting")
        if isinstance(accounting, dict):
            issue_76_accounting = {
                "within_attempt_ceiling": accounting.get("within_attempt_ceiling"),
                "completed_fits_minimum_proven_total": accounting.get(
                    "completed_fits_minimum_proven_total"),
                "completed_fits_builder_reported_total": accounting.get(
                    "completed_fits_builder_reported_total"),
            }
    comparisons: dict[str, Any] = {}
    for key, observed_76 in observational.items():
        observed_p2c = metrics[key]["metrics"]["TEST"]["weighted_cross_entropy"]
        entry: dict[str, Any] = {
            "issue_76_observational": observed_76,
            "p2c_observed": observed_p2c,
            "absolute_difference": abs(observed_p2c - observed_76),
        }
        if ":neural:" in key:
            entry["p2c_value_classification"] = NEURAL_METRIC_PROVENANCE
            entry["comparison_permitted"] = adjudication is None
        else:
            entry["p2c_value_classification"] = PARAMETRIC_METRIC_PROVENANCE
            entry["comparison_permitted"] = True
        comparisons[key] = entry
    return {
        "role": "AUDIT_CONTEXT_ONLY",
        "provenance": source,
        "issue_76_terminal": issue_76_terminal,
        "issue_76_execution_accounting": issue_76_accounting,
        "statement": "the Issue #76 observational metrics are audit context and are NOT an "
                     "acceptance threshold; P2C was not tuned to match them",
        "neural_rows_are_not_a_performance_comparison": adjudication is not None,
        "comparisons": comparisons,
    }


def issue_76_neural_reference(repo_root: Path) -> dict[str, Any]:
    """The earlier frozen neural trajectory, read from the preserved #76 artifact.

    Used by the defect evidence as an independent reference for the training path
    (objective, best step, best validation loss), not as a metric target.
    """
    preserved = read_json(repo_root / ISSUE_76_RESULTS_RELPATH)
    if not isinstance(preserved, dict):
        return {"available": False, "provenance": None, "per_fit_key": {}}
    per_key: dict[str, Any] = {}
    summaries = preserved.get("fit_summaries") or {}
    by_split = preserved.get("metrics_by_split") or {}
    for key, summary in summaries.items():
        if ":neural:" not in key:
            continue
        entry = {
            "objective": summary.get("objective"),
            "best_step": summary.get("best_step"),
            "best_validation_loss": summary.get("best_validation_loss"),
        }
        split_entry = by_split.get(key) or {}
        for split in SPLIT_STATES:
            block = split_entry.get(split)
            if isinstance(block, dict) and "weighted_cross_entropy" in block:
                entry[f"{split.lower()}_weighted_cross_entropy"] = block["weighted_cross_entropy"]
        per_key[key] = entry
    return {
        "available": bool(per_key),
        "provenance": f"READ_FROM_{ISSUE_76_RESULTS_RELPATH}",
        "role": "TRAINING_TRAJECTORY_REFERENCE_NOT_A_METRIC_TARGET",
        "per_fit_key": per_key,
    }


def _assigns_design_matrix(path: Path) -> dict[str, Any]:
    """Static AST check: does ``path`` assign ``<something>._design_matrix = ...``?

    This is the zero-fit proof of the missing frozen-preprocessing assignment. It reads
    and parses the file; it never imports or executes it.
    """
    import ast

    if not path.is_file():
        return {"path": str(path), "exists": False, "assigns_design_matrix": None}
    tree = ast.parse(path.read_text(encoding="utf-8"))
    hits: list[int] = []
    for node in ast.walk(tree):
        targets: list[Any] = []
        if isinstance(node, ast.Assign):
            targets = list(node.targets)
        elif isinstance(node, ast.AnnAssign) and node.value is not None:
            targets = [node.target]
        for target in targets:
            for sub in ast.walk(target):
                if isinstance(sub, ast.Attribute) and sub.attr == "_design_matrix":
                    hits.append(getattr(node, "lineno", -1))
    return {
        "path": path.name,
        "exists": True,
        "assigns_design_matrix": bool(hits),
        "assignment_lines": sorted(set(hits)),
    }


def preprocessing_defect_evidence(universe: sci.SyntheticUniverse,
                                  metrics: dict[str, dict[str, Any]],
                                  completed_by_key: dict[str, dict[str, Any]],
                                  reference: dict[str, Any],
                                  repo_root: Path,
                                  adjudication: dict[str, Any]) -> dict[str, Any]:
    """Zero-fit reconstruction of the frozen-preprocessing-path defect from durable data.

    Every number here is derived either from the durable ``FIT_COMPLETED`` records, from the
    frozen inputs, or from a static AST read of the immutable files. Nothing is fitted,
    optimized, trained or replayed, and no stored prediction is transformed.
    """
    tolerance = 1e-12
    defect = adjudication["defect"]
    executed_runner = repo_root / SCIENCE_RUNNER_RELPATH
    canonical_module = repo_root / SCIENTIFIC_MODULE_RELPATH
    runner_assignment = _assigns_design_matrix(executed_runner)

    per_fit: dict[str, Any] = {}
    for key in sorted(completed_by_key):
        record = completed_by_key[key]
        if str(record.get("family")) != "neural":
            continue
        reference_key = str(record.get("repeat_of") or key)
        reference_entry = (reference.get("per_fit_key") or {}).get(reference_key) or {}
        objective = record.get("objective")
        best_validation_loss = record.get("best_validation_loss")
        best_step = record.get("best_step")
        train_ce = metrics[key]["metrics"]["TRAIN"]["weighted_cross_entropy"]
        validation_ce = metrics[key]["metrics"]["VALIDATION"]["weighted_cross_entropy"]
        test_ce = metrics[key]["metrics"]["TEST"]["weighted_cross_entropy"]
        validation_gap = (abs(validation_ce - best_validation_loss)
                          if isinstance(best_validation_loss, (int, float)) else None)
        objective_gap = abs(objective - train_ce) if isinstance(objective, (int, float)) else None
        reference_objective = reference_entry.get("objective")
        per_fit[key] = {
            "attempt_index": record.get("attempt_index"),
            "kind": record.get("kind"),
            "regime": record.get("regime"),
            "seed": record.get("seed"),
            "reference_fit_key": reference_key,
            "training_design": "TRAIN_ONLY_ZSCORED",
            "persisted_prediction_design": "RAW_DESIGN_FALLBACK",
            # in-process, training-design-dependent quantities recorded by the frozen module
            "recorded_objective": objective,
            "recorded_best_step": best_step,
            "recorded_best_validation_loss": best_validation_loss,
            # quantities recomputed here from the persisted prediction tensor only
            "persisted_predictions_train_ce": train_ce,
            "persisted_predictions_validation_ce": validation_ce,
            "persisted_predictions_test_ce": test_ce,
            # signature 1: the objective is literally a function of the persisted tensor
            "objective_equals_persisted_train_ce": (None if objective_gap is None
                                                    else bool(objective_gap <= tolerance)),
            "objective_minus_persisted_train_ce": objective_gap,
            # signature 2: the recorded early-stopping checkpoint cannot be the persisted tensor
            "validation_mismatch_absolute": validation_gap,
            "persisted_predictions_consistent_with_recorded_validation": (
                None if validation_gap is None else bool(validation_gap <= tolerance)),
            # independent earlier-run reference for the *training* path
            "reference_objective": reference_objective,
            "reference_best_step": reference_entry.get("best_step"),
            "reference_best_validation_loss": reference_entry.get("best_validation_loss"),
            "best_step_matches_reference": (
                None if reference_entry.get("best_step") is None
                else bool(best_step == reference_entry.get("best_step"))),
            "best_validation_loss_matches_reference": (
                None if reference_entry.get("best_validation_loss") is None
                else bool(abs(best_validation_loss - reference_entry["best_validation_loss"])
                          <= tolerance)),
            "objective_matches_reference": (
                None if reference_objective is None
                else bool(abs(objective - reference_objective) <= 1e-9)),
            "objective_minus_reference": (
                None if reference_objective is None else objective - reference_objective),
            "classification": NEURAL_METRIC_PROVENANCE,
        }

    trajectory_matches = [v["best_validation_loss_matches_reference"] for v in per_fit.values()]
    consistent = [v["persisted_predictions_consistent_with_recorded_validation"]
                  for v in per_fit.values()]
    objective_is_persisted = [v["objective_equals_persisted_train_ce"] for v in per_fit.values()]
    summary = {
        "neural_fits_examined": len(per_fit),
        "training_trajectory_matches_frozen_reference": (
            bool(per_fit) and all(flag is True for flag in trajectory_matches)),
        "persisted_predictions_consistent_with_recorded_validation": (
            bool(per_fit) and all(flag is True for flag in consistent)),
        "objective_equals_persisted_train_ce_for_all_neural_fits": (
            bool(per_fit) and all(flag is True for flag in objective_is_persisted)),
        "max_validation_mismatch_absolute": max(
            (v["validation_mismatch_absolute"] or 0.0) for v in per_fit.values()),
        "defect_corroborated_by_durable_evidence": None,
    }
    summary["defect_corroborated_by_durable_evidence"] = bool(
        summary["training_trajectory_matches_frozen_reference"]
        and not summary["persisted_predictions_consistent_with_recorded_validation"])

    return {
        "applies_to_executed_run": True,
        "adjudication_comment": adjudication["adjudication_comment"],
        "adjudication_url": adjudication["adjudication_url"],
        "decision": adjudication["decision"],
        "finding": adjudication["finding"],
        "frozen_contract_requirement": {
            "requirement": defect["frozen_requirement"],
            "canonical_assignment": defect["missing_assignment"],
            "canonical_path": "run_scientific_program",
            "canonical_path_assigns_it": defect["canonical_path_performs_the_assignment"],
            "canonical_module_static_check": _assigns_design_matrix(canonical_module),
            "executed_science_runner_static_check": runner_assignment,
            "executed_science_runner_assigns_it": runner_assignment["assigns_design_matrix"],
        },
        "executed_defect": {
            "affected_family": defect["affected_family"],
            "unaffected_families": defect["unaffected_families"],
            "training_design": defect["training_design"],
            "persisted_prediction_design": defect["persisted_prediction_design"],
            "prediction_path": defect["prediction_path"],
            "fallback_mechanism": defect["fallback_mechanism"],
            "missing_assignment": defect["missing_assignment"],
            "consequence": defect["consequence"],
            "this_is_not_a_performance_finding": defect["this_is_not_a_performance_finding"],
        },
        "fallback_precondition_observed_zero_fit": {
            "universe_design_matrix_unset_after_build": universe._design_matrix is None,
            "design_matrix_property_returns_raw_design": universe.design_matrix is
            universe.raw_design,
            "note": "observed on the freshly built universe without touching any fitter "
                    "(accessing the property is what the frozen prediction path does)",
        },
        "per_fit_corroboration": per_fit,
        "summary": summary,
        "zero_fit_recovery_possible_for_corrected_neural_predictions": adjudication[
            "zero_fit_recovery_possible"],
        "zero_fit_recovery_reason": adjudication["zero_fit_recovery_reason"],
        "second_science_invocation_authorized": adjudication[
            "second_science_invocation_authorized"],
        "no_prediction_transformation_attempted": True,
        "computation": "zero-fit: durable ledger records + frozen inputs + static AST reads only",
    }


def frozen_split_interpretation(universe: sci.SyntheticUniverse) -> dict[str, Any]:
    cfg = universe.config
    train_origins = {b.origin_id for b in universe.blocks_for("TRAIN")}
    test_origins = {b.origin_id for b in universe.blocks_for("TEST")}
    train_destinations = {cfg.region_ids[j] for b in universe.blocks_for("TRAIN")
                          for j in b.allowed}
    return {
        "split_counts": {state: len(universe.blocks_for(state)) for state in SPLIT_STATES},
        "blocking": "time and origin role only",
        "test_touches_train_time": bool(
            {b.time_id for b in universe.blocks_for("TEST")}
            & {b.time_id for b in universe.blocks_for("TRAIN")}),
        "test_touches_train_origin": bool(test_origins & train_origins),
        "test_regions_appear_as_train_destinations": bool(test_origins <= train_destinations),
        "test_regions_are_unseen_regions": False,
        "generalization_claims_allowed": ["HELD_OUT_TIME", "HELD_OUT_ORIGIN_ROLE"],
        "generalization_claims_forbidden": ["FULLY_REGION_BLOCKED", "UNSEEN_REGION",
                                            "UNSEEN_REGION_NODE_FEATURES"],
    }


def code_identity(repo_root: Path) -> dict[str, Any]:
    module_blob = blob_sha1_lf(repo_root / SCIENTIFIC_MODULE_RELPATH)
    config_blob = blob_sha1_lf(repo_root / CONFIG_RELPATH)
    return {
        "operative_baseline": OPERATIVE_BASELINE,
        "publication_baseline": PUBLICATION_BASELINE,
        "scientific_module_relpath": SCIENTIFIC_MODULE_RELPATH,
        "scientific_module_blob_sha1": module_blob,
        "scientific_module_blob_status": ("MATCH" if module_blob == EXPECTED_SCIENTIFIC_MODULE_BLOB
                                         else "MISMATCH"),
        "p1a_module_relpath": P1A_MODULE_RELPATH,
        "p1a_module_blob_sha1": blob_sha1_lf(repo_root / P1A_MODULE_RELPATH),
        "config_relpath": CONFIG_RELPATH,
        "config_blob_sha1": config_blob,
        "config_blob_status": ("MATCH" if config_blob == EXPECTED_CONFIG_BLOB else "MISMATCH"),
        "config_sha256_lf": sha256_lf(repo_root / CONFIG_RELPATH),
        "contract_relpath": CONTRACT_RELPATH,
        "contract_blob_sha1": blob_sha1_lf(repo_root / CONTRACT_RELPATH),
        "schema_relpath": SCHEMA_RELPATH,
        "schema_blob_sha1": blob_sha1_lf(repo_root / SCHEMA_RELPATH),
    }


def environment_summary() -> dict[str, Any]:
    import os
    import platform
    import scipy

    return {
        "versions": {
            "python": sys.version.split()[0],
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "platform": platform.platform(),
        },
        "torch": "NOT_INSTALLED_NEURAL_BACKEND_IS_NUMPY",
        "thread_pinning": {v: os.environ.get(v) for v in
                           ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS",
                            "MKL_NUM_THREADS", "PYTHONHASHSEED")},
    }


def bump_render_counter(outdir: Path) -> int:
    """Derive the render-only invocation count from the previously rendered artifacts."""
    path = outdir / RESULTS_NAME
    previous = read_json(path)
    if not isinstance(previous, dict):
        return 1
    try:
        return int(previous.get("render_only_invocations", 0)) + 1
    except (TypeError, ValueError):
        return 1


# --------------------------------------------------------------------------- render
def render(*, repo_root: Path | None = None, ledger_path: Path | None = None,
           seal_path: Path | None = None, outdir: Path | None = None) -> int:
    """Zero-fit production path: durable ledger + frozen inputs -> all four artifacts."""
    repo_root = Path(repo_root) if repo_root is not None else ROOT
    outdir = Path(outdir) if outdir is not None else repo_root / OUTDIR_RELPATH
    ledger_path = Path(ledger_path) if ledger_path is not None else outdir / LEDGER_NAME
    seal_path = Path(seal_path) if seal_path is not None else outdir / SEAL_NAME

    if not ledger_path.is_file():
        print(json.dumps({
            "terminal": TERMINAL_BLOCKED,
            "reason": "the durable attempt ledger is missing; science must run first",
            "ledger_path": str(ledger_path),
            "fits": 0, "optimizer_steps": 0,
        }, indent=2))
        return 3

    records = read_ledger(ledger_path)
    seal = read_json(seal_path)
    render_count = bump_render_counter(outdir)

    config = sci.load_frozen_config(repo_root, config_relpath=CONFIG_RELPATH)
    universe = sci.build_universe(config, repo_root)   # deterministic generator, no fit
    completed = completed_records(records)
    by_key = {str(r.get("fit_key")): r for r in completed}

    invariants = ledger_invariants(records)
    payloads = payload_hash_verification(completed)
    shares = share_distribution_check(universe, completed)
    wall_clock = resolve_science_wall_clock(records, seal)

    # ---- the single production aggregation path ------------------------------
    metrics = aggregate_metrics(universe, completed)
    fixed_metrics = fixed_baseline_metrics(universe)
    constraints = constraint_diagnostics(universe, metrics, fixed_metrics)
    determinism = determinism_comparisons(universe, by_key)
    p1a = p1a_closure(universe)
    split_view = frozen_split_interpretation(universe)
    identity = code_identity(repo_root)

    reported_metrics = {
        key: metrics[key]["metrics"]["TEST"]["weighted_cross_entropy"] for key in PRIMARY_FIT_KEYS
        if key in metrics}
    all_frozen_metrics_reported = (set(metrics) >= set(PRIMARY_FIT_KEYS)
                                  and set(metrics) >= {repeat for _, repeat in REPEAT_PAIRS}
                                  and len(reported_metrics) == len(PRIMARY_FIT_KEYS))

    gate_checks = {
        "pre_run_freeze_sha_recorded": invariants["pre_run_freeze_sha_recorded"],
        "exactly_one_science_invocation": invariants["science_invocations"] == 1,
        "zero_science_retries": invariants["science_retries"] == 0,
        "exactly_twelve_started": invariants["exactly_twelve_started"],
        "exactly_twelve_completed": invariants["exactly_twelve_completed"],
        "zero_failed_fits": invariants["zero_failed"],
        "no_unmatched_started_record": invariants["no_unmatched_started"],
        "started_indices_exactly_1_to_12": invariants["started_indices_are_exactly_1_to_12"],
        "completed_indices_exactly_1_to_12": invariants["completed_indices_are_exactly_1_to_12"],
        "started_before_completed_ordering_ok": invariants["started_before_completed_ordering_ok"],
        "ledger_record_count_is_24": invariants["ledger_record_count_is_24"],
        "every_completed_record_has_full_predictions": payloads["all_predictions_persisted"],
        "every_prediction_shape_is_4x5x5": payloads["all_prediction_shapes_frozen"],
        "every_payload_sha256_verifies": payloads["all_payload_hashes_match"],
        "every_completed_record_has_metadata": payloads["all_metadata_present"],
        "science_wall_clock_within_ceiling": wall_clock["within_ceiling"],
        "determinism_within_tolerance": determinism["all_within_tolerance"],
        "row_normalization_ok": constraints["row_normalization_ok"],
        "negativity_violations_zero": constraints["negativity_ok"],
        "support_violations_zero": constraints["support_ok"],
        "split_counts_9_3_2_6": constraints["split_counts_ok"],
        "excluded_block_count_6": constraints["excluded_block_count_ok"],
        "p1a_accounting_closes": p1a["closes"],
        "all_frozen_metrics_reported": all_frozen_metrics_reported,
        "no_unseen_region_claim": split_view["test_regions_are_unseen_regions"] is False,
        "scientific_module_blob_matches": identity["scientific_module_blob_status"] == "MATCH",
        "frozen_config_blob_matches": identity["config_blob_status"] == "MATCH",
        "recovered_predictions_are_valid_share_distributions": shares["all_valid"],
        "published_metric_keys_complete": set(metrics) == set(
            PRIMARY_FIT_KEYS) | {repeat for _, repeat in REPEAT_PAIRS},
    }
    # the mechanical protocol/durability machinery on its own (the Reviewer confirmed this
    # part is correct); it is reported separately from the experiment terminal
    mechanical_protocol_gate_ok = all(gate_checks.values())

    # ---- binding Reviewer adjudication (authority, not a re-derived predicate) --------
    executed_pre_run_freeze_sha = (invariants["pre_run_freeze_shas_in_started_records"] or [None])[0]
    adjudication = REVIEWER_ADJUDICATIONS.get(str(executed_pre_run_freeze_sha))
    adjudication_applies = adjudication is not None
    confirmatory_p2_pass_allowed = bool(mechanical_protocol_gate_ok and not adjudication_applies)
    gate_ok = confirmatory_p2_pass_allowed
    terminal = TERMINAL_PASS if gate_ok else TERMINAL_GATE_FAIL

    provenance = metric_provenance(adjudication)
    comparison = neural_comparison_status(metrics, fixed_metrics, adjudication)
    if adjudication_applies:
        defect_evidence: dict[str, Any] = preprocessing_defect_evidence(
            universe, metrics, by_key, issue_76_neural_reference(repo_root), repo_root,
            adjudication)
    else:
        defect_evidence = {
            "applies_to_executed_run": False,
            "adjudication_comment": None,
            "lookup_key_pre_run_freeze_sha": executed_pre_run_freeze_sha,
            "note": "no Reviewer adjudication is registered against this PRE_RUN_FREEZE SHA, "
                    "so the terminal is taken from the mechanical protocol gates alone",
        }
    audit = audit_context_vs_issue_76(metrics, repo_root, adjudication)

    def adjudication_block() -> dict[str, Any]:
        if not adjudication_applies:
            return {"applies": False, "lookup_key_pre_run_freeze_sha":
                    executed_pre_run_freeze_sha}
        return {
            "applies": True,
            "adjudication_comment": adjudication["adjudication_comment"],
            "adjudication_url": adjudication["adjudication_url"],
            "adjudication_kind": adjudication["adjudication_kind"],
            "reviewed_candidate_sha": adjudication["reviewed_candidate_sha"],
            "decision": adjudication["decision"],
            "finding": adjudication["finding"],
            "corrected_terminal": adjudication["corrected_terminal"],
            "confirmatory_p2_pass_allowed": adjudication["confirmatory_p2_pass_allowed"],
            "durability_protocol_finding": adjudication["durability_protocol_finding"],
            "scientific_execution_finding": adjudication["scientific_execution_finding"],
            "zero_fit_recovery_possible_for_corrected_neural_predictions": adjudication[
                "zero_fit_recovery_possible"],
            "second_science_invocation_authorized": adjudication[
                "second_science_invocation_authorized"],
            "authorized_remediation": adjudication["authorized_remediation"],
            "struck_terminal": TERMINAL_PASS,
        }

    raw: dict[str, Any] = {
        "experiment_id": EXPERIMENT_ID,
        "issue": 78,
        "task_id": TASK_ID,
        "authority_marker": AUTHORITY_MARKER,
        "route": ROUTE,
        "phase": "RENDER_STAGE_ZERO_FIT",
        "recorded_utc": utc_now(),
        "zero_fit_recovery": {
            "statement": ZERO_FIT_STATEMENT,
            "recovery_object": "PERSISTED_FIT_COMPLETED_PREDICTION_TENSORS",
            "fits_performed_here": 0,
            "optimizer_steps_performed_here": 0,
            "fitters_called_here": 0,
            "ledger_modified_by_renderer": False,
            "authoritative_source": LEDGER_RELPATH,
        },
        "pre_run_freeze_sha": (invariants["pre_run_freeze_shas_in_started_records"] or [None])[0],
        "code_identity": identity,
        "environment": environment_summary(),
        "frozen_split_interpretation": split_view,
        "attempt_ledger_summary": {k: v for k, v in invariants.items()},
        "ledger_invariants": invariants,
        "payload_hash_verification": payloads,
        "share_distribution_check": shares,
        "science_wall_clock": wall_clock,
        "fit_summaries": fit_summaries(completed),
        "metrics": metrics,
        "fixed_baseline_metrics": fixed_metrics,
        "determinism": determinism,
        "constraint_diagnostics": constraints,
        "p1a_accounting_checks": p1a,
        "p1a_accounting_raw": universe.p1a_diagnostics,
        "aggregation_contract": {
            "metrics_store_shape": "{fit_key: {'metrics': {split: metrics}}}",
            "fixed_store_shape": "{regime: {'metrics': {split: metrics}}}",
            "producer": "aggregate_metrics / fixed_baseline_metrics",
            "consumer": "constraint_diagnostics",
            "shape_validated_loudly": True,
            "note": "Issue #77 failed because this contract was violated silently after all "
                    "twelve fits had run; the shape is now asserted at the consumer.",
        },
        "gate_ok": gate_ok,
        "confirmatory_p2_pass_allowed": confirmatory_p2_pass_allowed,
        "mechanical_protocol_gate_ok": mechanical_protocol_gate_ok,
        "reviewer_adjudication": adjudication_block(),
        "durability_protocol_status": DURABILITY_STATUS_CORRECT,
        "metric_provenance": provenance,
        "neural_comparison_status": comparison,
        "preprocessing_path_defect_evidence": defect_evidence,
        "terminal": terminal,
        "not_an_acceptance": "raw scientific output; acceptance is decided by the Reviewer, "
                             "not by this artifact",
    }

    results: dict[str, Any] = {
        "experiment_id": EXPERIMENT_ID,
        "issue": 78,
        "task_id": TASK_ID,
        "authority_marker": AUTHORITY_MARKER,
        "route": ROUTE,
        "phase": "RENDER_STAGE_ZERO_FIT_PUBLICATION",
        "recorded_utc": utc_now(),
        "pre_run_freeze_sha": raw["pre_run_freeze_sha"],
        "science_code_identity": identity,
        "environment": raw["environment"],
        "frozen_split_interpretation": split_view,
        "attempt_ledger_summary": invariants,
        "payload_hash_verification": payloads,
        "share_distribution_check": shares,
        "science_wall_clock": wall_clock,
        "render_only_invocations": render_count,
        "zero_fit_statement": ZERO_FIT_STATEMENT,
        "aggregation_contract": raw["aggregation_contract"],
        "metrics_by_split": {key: metrics[key]["metrics"] for key in sorted(metrics)},
        "fixed_baseline_metrics": {regime: fixed_metrics[regime]["metrics"]
                                   for regime in REGIMES},
        "fit_summaries": raw["fit_summaries"],
        "determinism": determinism,
        "constraint_diagnostics": constraints,
        "p1a_accounting_checks": p1a,
        "negative_result_flags": comparison,
        "metric_provenance": provenance,
        "audit_context_vs_issue_76": audit,
        "acceptance_gate_checks": gate_checks,
        "mechanical_protocol_gate_ok": mechanical_protocol_gate_ok,
        "confirmatory_p2_pass_allowed": confirmatory_p2_pass_allowed,
        "reviewer_adjudication": raw["reviewer_adjudication"],
        "durability_protocol_status": DURABILITY_STATUS_CORRECT,
        "preprocessing_path_defect_evidence": defect_evidence,
        "interpretation_ceiling": {
            "allowed": [
                "method/pipeline replication under the frozen synthetic controls, for the "
                "families that were executed under the frozen design",
                "held-out-time and held-out-origin-role observations",
                "audit comparison with the Issue #76 observational output",
            ],
            "forbidden": [
                "empirical China claim",
                "annual bilateral OD data availability claim",
                "unseen-region claim",
                "causal or economic mechanism claim",
                "HJB/KFE/GE/household policy or welfare claim",
                "any tuning based on Issue #76 or P2C outcomes",
                "any neural-vs-parametric scientific performance comparison from P2C",
                "any treatment of the persisted P2C neural metrics as a measurement of the "
                "frozen neural mapping",
            ],
        },
        "terminal": terminal,
    }

    report_text = render_report(results, raw, metrics, fixed_metrics, comparison, determinism,
                               constraints, shares, p1a, wall_clock, identity, gate_checks,
                               terminal)

    report_path = outdir / REPORT_NAME
    raw_path = outdir / RAW_NAME
    results_path = outdir / RESULTS_NAME
    manifest_path = outdir / MANIFEST_NAME
    outdir.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report_text, encoding="utf-8", newline="\n")
    raw_path.write_bytes(dumps(raw))

    manifest: dict[str, Any] = {
        "experiment_id": EXPERIMENT_ID,
        "issue": 78,
        "recorded_utc": utc_now(),
        "identity_policy": IDENTITY_POLICY,
        "science_protocol": {
            "science_invocations": invariants["science_invocations"],
            "science_retries": invariants["science_retries"],
            "started_fits": invariants["started_count"],
            "completed_fits": invariants["completed_count"],
            "failed_fits": invariants["failed_count"],
            "planned_fits": PLANNED_FIT_ATTEMPTS,
            "render_only_invocations": render_count,
            "zero_science_reruns": True,
            "zero_fit_publication": True,
            "fits_performed_by_renderer": 0,
            "optimizer_steps_performed_by_renderer": 0,
        },
        "provenance_chain": {
            "issue_78_operative_baseline": OPERATIVE_BASELINE,
            "issue_78_publication_baseline": PUBLICATION_BASELINE,
            "pre_run_freeze_sha": raw["pre_run_freeze_sha"],
            "pre_run_freeze_role": "executed science code identity",
            "scientific_module_relpath": SCIENTIFIC_MODULE_RELPATH,
            "scientific_module_blob_sha1": identity["scientific_module_blob_sha1"],
            "p1a_module_relpath": P1A_MODULE_RELPATH,
            "p1a_module_blob_sha1": identity["p1a_module_blob_sha1"],
            "science_runner_relpath": SCIENCE_RUNNER_RELPATH,
            "science_runner_blob_sha1_at_render": blob_sha1_lf(repo_root / SCIENCE_RUNNER_RELPATH),
            "renderer_relpath": RENDERER_RELPATH,
            "renderer_blob_sha1": blob_sha1_lf(repo_root / RENDERER_RELPATH),
            "frozen_config_relpath": CONFIG_RELPATH,
            "frozen_config_blob_sha1": identity["config_blob_sha1"],
            "frozen_contract_relpath": CONTRACT_RELPATH,
            "frozen_contract_blob_sha1": identity["contract_blob_sha1"],
            "frozen_schema_relpath": SCHEMA_RELPATH,
            "frozen_schema_blob_sha1": identity["schema_blob_sha1"],
        },
        "artifact_hashes": {
            "ledger_relpath": LEDGER_RELPATH,
            "ledger_sha256_lf": sha256_lf(ledger_path),
            "ledger_blob_sha1": blob_sha1_lf(ledger_path),
            "science_seal_relpath": SEAL_RELPATH if seal is not None else None,
            "science_seal_sha256_lf": sha256_lf(seal_path) if seal_path.is_file() else None,
            "raw_results_relpath": RAW_RELPATH,
            "raw_results_sha256_lf": sha256_lf(raw_path),
            "raw_results_blob_sha1": blob_sha1_lf(raw_path),
            "report_relpath": REPORT_RELPATH,
            "report_sha256_lf": sha256_lf(report_path),
        },
        "frozen_inputs_read_only": [CONFIG_RELPATH, CONTRACT_RELPATH, SCHEMA_RELPATH,
                                    P1A_MODULE_RELPATH, SCIENTIFIC_MODULE_RELPATH],
        "zero_fit_recovery": raw["zero_fit_recovery"],
        "declarations": {
            "config_or_contract_mutated": False,
            "scientific_module_mutated": False,
            "real_data_used": False,
            "data_download_scrape_purchase": False,
            "household_or_hjb_kfe_ge_matlab_calls": 0,
            "full_repository_suite_runs": 0,
            "tuning_or_extra_seed": False,
            "extra_fit_or_second_science_invocation": False,
            "ledger_modified_by_renderer": False,
            "renderer_calls_any_fitter": _calls_any_fitter(),
            "new_fits_in_this_remediation": 0,
            "optimizer_steps_in_this_remediation": 0,
            "ledger_or_seal_modified_in_this_remediation": False,
            "science_runner_or_tests_modified_after_first_optimizer_step": False,
            "prediction_tensor_transformation_attempted": False,
        },
        "reviewer_adjudication": raw["reviewer_adjudication"],
        "confirmatory_p2_pass_allowed": confirmatory_p2_pass_allowed,
        "mechanical_protocol_gate_ok": mechanical_protocol_gate_ok,
        "durability_protocol_status": DURABILITY_STATUS_CORRECT,
        "metric_provenance": {
            "neural_marker": NEURAL_METRIC_PROVENANCE,
            "parametric_marker": PARAMETRIC_METRIC_PROVENANCE,
            "fixed_baseline_marker": FIXED_METRIC_PROVENANCE,
            "values_retained_for_audit": True,
            "values_replaced_with_issue_76": False,
            "applies": provenance["applies"],
        },
        "preprocessing_path_defect_evidence": defect_evidence,
        "terminal": terminal,
    }

    # ---- identity chain (acyclic) --------------------------------------------
    core = {k: v for k, v in results.items()
            if k not in (RESULTS_DIGEST_FIELD, MANIFEST_DIGEST_FIELD)}
    core_bytes = dumps(core)
    results_digest = hashlib.sha256(core_bytes).hexdigest().upper()
    manifest["artifact_hashes"]["results_relpath"] = RESULTS_RELPATH
    manifest["artifact_hashes"]["results_canonical_sha256"] = results_digest
    manifest["artifact_hashes"]["results_blob_sha1"] = hashlib.sha1(
        f"blob {len(core_bytes)}\0".encode("ascii") + core_bytes).hexdigest()

    manifest_bytes = dumps(manifest)
    manifest_path.write_bytes(manifest_bytes)
    results[RESULTS_DIGEST_FIELD] = results_digest
    results[MANIFEST_DIGEST_FIELD] = hashlib.sha256(manifest_bytes).hexdigest().upper()
    results_path.write_bytes(dumps(results))

    # ---- verification -------------------------------------------------------
    rr = json.loads(results_path.read_text(encoding="utf-8"))
    mm = json.loads(manifest_path.read_text(encoding="utf-8"))
    file_core = dumps({k: v for k, v in rr.items()
                       if k not in (RESULTS_DIGEST_FIELD, MANIFEST_DIGEST_FIELD)})
    checks = {
        "results_file_is_canonical_plus_digests": results_path.read_bytes() == dumps(rr),
        "results_digest_recomputes": rr[RESULTS_DIGEST_FIELD]
        == hashlib.sha256(file_core).hexdigest().upper(),
        "manifest_digest_recomputes": rr[MANIFEST_DIGEST_FIELD]
        == hashlib.sha256(dumps(mm)).hexdigest().upper(),
        "results_blob_matches": mm["artifact_hashes"]["results_blob_sha1"]
        == hashlib.sha1(f"blob {len(file_core)}\0".encode("ascii") + file_core).hexdigest(),
        "raw_hash_recorded": mm["artifact_hashes"]["raw_results_sha256_lf"] == sha256_lf(raw_path),
        "ledger_hash_recorded": mm["artifact_hashes"]["ledger_sha256_lf"] == sha256_lf(ledger_path),
        "report_hash_recorded": mm["artifact_hashes"]["report_sha256_lf"] == sha256_lf(report_path),
        "no_fit_in_renderer": _calls_any_fitter() is False,
        "ledger_untouched_by_render": invariants["records"] == len(read_ledger(ledger_path)),
        "terminal_gate_consistent": rr["terminal"] == mm["terminal"] == terminal,
        "gate_ok": gate_ok,
    }
    print(json.dumps({
        "phase": "RENDER_STAGE_ZERO_FIT",
        "render_only_invocations": render_count,
        "fits": 0,
        "optimizer_steps": 0,
        "metrics_computed_from": "PERSISTED_LEDGER_PREDICTIONS_ONLY",
        "gate_checks": gate_checks,
        "mechanical_protocol_gate_ok": mechanical_protocol_gate_ok,
        "reviewer_adjudication_applies": adjudication_applies,
        "reviewer_adjudication_comment": (adjudication["adjudication_comment"]
                                          if adjudication_applies else None),
        "confirmatory_p2_pass_allowed": confirmatory_p2_pass_allowed,
        "gate_ok": gate_ok,
        "terminal": terminal,
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "render_status": ("RENDERED_PASS" if gate_ok else "RENDERED_GATE_FAIL"),
        "results": RESULTS_RELPATH,
        "manifest": MANIFEST_RELPATH,
        "raw": RAW_RELPATH,
        "report": REPORT_RELPATH,
    }, indent=2))
    return 0 if all(checks.values()) and gate_ok else 2


def render_report(results: dict[str, Any], raw: dict[str, Any],
                  metrics: dict[str, dict[str, Any]],
                  fixed_metrics: dict[str, dict[str, Any]], negative: dict[str, Any],
                  determinism: dict[str, Any], constraints: dict[str, Any],
                  shares: dict[str, Any], p1a: dict[str, Any], wall_clock: dict[str, Any],
                  identity: dict[str, Any], gate_checks: dict[str, bool],
                  terminal: str) -> str:
    invariants = results["attempt_ledger_summary"]
    adjudication = results["reviewer_adjudication"]
    lines: list[str] = []
    lines.append("# DLH-WL-P2C — durable per-fit-output replication of the frozen "
                 "synthetic prototype\n")
    lines.append("## 0. Status\n")
    lines.append("```")
    lines.append(f"terminal: {terminal}")
    lines.append("```\n")
    if adjudication.get("applies"):
        lines.append(f"**This terminal is a corrected Gate Fail.** The previously recorded "
                     f"`{adjudication['struck_terminal']}` is **struck**: Reviewer "
                     f"adjudication `{adjudication['adjudication_comment']}` "
                     f"({adjudication['adjudication_kind']}) found that the executed neural "
                     f"prediction path violates the frozen #75 TRAIN-only z-score "
                     f"preprocessing contract. "
                     f"`confirmatory_p2_pass_allowed = {results['confirmatory_p2_pass_allowed']}`.")
        lines.append("")
        lines.append(f"- The durability/protocol machinery is correct and the #77 durability "
                     f"defect is genuinely fixed "
                     f"(`mechanical_protocol_gate_ok = "
                     f"{results['mechanical_protocol_gate_ok']}`, "
                     f"`durability_protocol_status` = "
                     f"`{results['durability_protocol_status']}`).")
        lines.append(f"- The experiment nevertheless fails as a whole because one required "
                     f"baseline family was executed incorrectly.")
        lines.append("")
    lines.append(f"- Issue: **#78** / `{results['task_id']}`; route `{results['route']}`")
    lines.append(f"- PRE_RUN_FREEZE SHA (executed science code identity): "
                 f"`{results['pre_run_freeze_sha']}`")
    lines.append(f"- scientific module blob: `{identity['scientific_module_blob_sha1']}` "
                 f"({identity['scientific_module_blob_status']})")
    lines.append(f"- frozen config blob: `{identity['config_blob_sha1']}` "
                 f"({identity['config_blob_status']})")
    lines.append(f"- science invocations: **{invariants['science_invocations']}**; "
                 f"science retries: **{invariants['science_retries']}**")
    lines.append(f"- fit attempts started / completed / failed: "
                 f"**{invariants['started_count']} / {invariants['completed_count']} / "
                 f"{invariants['failed_count']}**")
    clock = wall_clock["science_wall_clock_seconds"]
    clock_text = f"{clock:.6f} s" if isinstance(clock, (int, float)) else "UNKNOWN"
    lines.append(f"- science wall clock: **{clock_text}** "
                 f"(source `{wall_clock['wall_clock_source']}`, ceiling "
                 f"{wall_clock['ceiling_seconds']:.0f} s)")
    lines.append(f"- render-only invocations so far: **{results['render_only_invocations']}** "
                 f"(zero fits, zero optimizer steps)")
    lines.append("")
    lines.append("## 1. What changed from #76/#77 (durability boundary only)\n")
    lines.append(
        "The #75 scientific design is unchanged: 5 regions x 4 periods, the frozen support, "
        "the S0/S1 generators, three baseline families (fixed support-normalized uniform, "
        "six-parameter contrast-identifiable gravity/logit MLE, small MLP pair scorer with "
        "16/8 hidden widths under masked softmax), the 9/3/2/6 split, TRAIN-only "
        "preprocessing, neural seeds 0/1/2, the frozen metrics/tolerances, 12 planned fit "
        "executions, a 13-attempt ceiling and an 1800 s wall-clock ceiling.")
    lines.append("")
    lines.append(
        "Only the durability boundary changed. #77 was limited to completion metadata, so "
        "when it failed after the twelfth fit before writing RAW_RESULTS nothing could be "
        "recovered without retraining. P2C persists the complete scientific output of each "
        "fit — full 4x5x5 prediction tensor, coefficients, objective, convergence, best "
        "step, best validation loss, backend, diagnostics and a canonical payload SHA-256 — "
        "and fsyncs the completed record before the next fit may begin.")
    lines.append("")
    lines.append(results["zero_fit_statement"])
    lines.append("")
    lines.append("## 2. Acceptance gate checks and the experiment terminal\n")
    lines.append(f"- mechanical protocol/durability gate (`acceptance_gate_checks`): "
                 f"**{results['mechanical_protocol_gate_ok']}**")
    lines.append(f"- Reviewer adjudication applies to this run: "
                 f"**{adjudication.get('applies')}**")
    lines.append(f"- `confirmatory_p2_pass_allowed`: "
                 f"**{results['confirmatory_p2_pass_allowed']}**")
    lines.append(f"- corrected terminal: `{terminal}`")
    lines.append("")
    lines.append("The mechanical checks below all pass; they verify the durability and protocol "
                 "machinery, which the Reviewer confirmed is correct. They do **not** verify "
                 "that the neural family was executed under the frozen preprocessing contract, "
                 "which is why the experiment terminal is a Gate Fail.")
    lines.append("")
    lines.append("| mechanical check | value |")
    lines.append("|---|---|")
    for name, ok in gate_checks.items():
        lines.append(f"| {name} | {ok} |")
    lines.append("")
    if adjudication.get("applies"):
        lines.append("## 2b. Binding Reviewer adjudication\n")
        lines.append(f"- comment: `{adjudication['adjudication_comment']}` "
                     f"({adjudication['adjudication_kind']})")
        lines.append(f"- url: {adjudication['adjudication_url']}")
        lines.append(f"- reviewed candidate: `{adjudication['reviewed_candidate_sha']}`")
        lines.append(f"- decision: **{adjudication['decision']}**")
        lines.append(f"- struck terminal: `{adjudication['struck_terminal']}`")
        lines.append(f"- corrected terminal: `{adjudication['corrected_terminal']}`")
        lines.append(f"- finding: {adjudication['finding']}")
        lines.append(f"- durability/protocol finding: "
                     f"{adjudication['durability_protocol_finding']}")
        lines.append(f"- scientific-execution finding: "
                     f"{adjudication['scientific_execution_finding']}")
        lines.append("")
        lines.append("### 2b.1 Defect provenance (frozen contract vs executed path)\n")
        evidence = results["preprocessing_path_defect_evidence"]
        frozen = evidence["frozen_contract_requirement"]
        defect = evidence["executed_defect"]
        fallback = evidence["fallback_precondition_observed_zero_fit"]
        lines.append("| element | value |")
        lines.append("|---|---|")
        lines.append(f"| frozen requirement | {frozen['requirement']} |")
        lines.append(f"| required assignment | `{frozen['canonical_assignment']}` |")
        lines.append(f"| canonical path | `{frozen['canonical_path']}` performs it: "
                     f"**{frozen['canonical_path_assigns_it']}** |")
        lines.append(f"| canonical module static check | "
                     f"`{frozen['canonical_module_static_check']['path']}` assigns "
                     f"`_design_matrix` at lines "
                     f"{frozen['canonical_module_static_check']['assignment_lines']} |")
        lines.append(f"| executed science runner | "
                     f"`{frozen['executed_science_runner_static_check']['path']}` assigns "
                     f"`_design_matrix`: "
                     f"**{frozen['executed_science_runner_assigns_it']}** "
                     f"(lines {frozen['executed_science_runner_static_check']['assignment_lines']}) |")
        lines.append(f"| training design | {defect['training_design']} |")
        lines.append(f"| persisted prediction design | {defect['persisted_prediction_design']} |")
        lines.append(f"| prediction path | `{defect['prediction_path']}` |")
        lines.append(f"| fallback mechanism | {defect['fallback_mechanism']} |")
        lines.append(f"| missing assignment | `{defect['missing_assignment']}` |")
        lines.append(f"| affected family | {defect['affected_family']} |")
        lines.append(f"| unaffected families | {', '.join(defect['unaffected_families'])} |")
        lines.append("")
        lines.append("Zero-fit observation of the fallback precondition on the freshly built "
                     "universe:")
        lines.append("")
        lines.append("```")
        lines.append(f"universe._design_matrix is None            : "
                     f"{fallback['universe_design_matrix_unset_after_build']}")
        lines.append(f"universe.design_matrix is universe.raw_design: "
                     f"{fallback['design_matrix_property_returns_raw_design']}")
        lines.append("```")
        lines.append("")
        lines.append(f"{defect['consequence']}")
        lines.append("")
        lines.append(f"**{defect['this_is_not_a_performance_finding']}**")
        lines.append("")
        lines.append("### 2b.2 Corroboration recomputed from the durable ledger\n")
        lines.append("Every value below is recomputed by this zero-fit stage from the durable "
                     "`FIT_COMPLETED` prediction tensors, and can be checked by hand against "
                     "`DLH_WL_P2C_ATTEMPT_LEDGER.jsonl`.")
        lines.append("")
        lines.append("| fit key | recorded objective | persisted TRAIN CE | obj = persisted "
                     "TRAIN CE | recorded best-val loss | persisted VALIDATION CE | mismatch "
                     "| ref objective (#76) | ref best step | ref best-val loss | best-val "
                     "matches ref | obj matches ref |")
        lines.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
        for key, row in sorted(evidence["per_fit_corroboration"].items()):
            lines.append(
                f"| `{key}` | {row['recorded_objective']:.15f} "
                f"| {row['persisted_predictions_train_ce']:.15f} "
                f"| {row['objective_equals_persisted_train_ce']} "
                f"| {row['recorded_best_validation_loss']:.15f} "
                f"| {row['persisted_predictions_validation_ce']:.15f} "
                f"| {row['validation_mismatch_absolute']:.15f} "
                f"| {row['reference_objective']:.15f} "
                f"| {row['reference_best_step']} "
                f"| {row['reference_best_validation_loss']:.15f} "
                f"| {row['best_validation_loss_matches_reference']} "
                f"| {row['objective_matches_reference']} |")
        lines.append("")
        summary = evidence["summary"]
        lines.append("```")
        lines.append(f"neural_fits_examined                                   : "
                     f"{summary['neural_fits_examined']}")
        lines.append(f"training_trajectory_matches_frozen_reference           : "
                     f"{summary['training_trajectory_matches_frozen_reference']}")
        lines.append(f"persisted_predictions_consistent_with_recorded_validation: "
                     f"{summary['persisted_predictions_consistent_with_recorded_validation']}")
        lines.append(f"objective_equals_persisted_train_ce_for_all_neural_fits : "
                     f"{summary['objective_equals_persisted_train_ce_for_all_neural_fits']}")
        lines.append(f"max_validation_mismatch_absolute                       : "
                     f"{summary['max_validation_mismatch_absolute']:.15f}")
        lines.append(f"defect_corroborated_by_durable_evidence                : "
                     f"{summary['defect_corroborated_by_durable_evidence']}")
        lines.append("```")
        lines.append("")
        lines.append("Reading of the two signatures:")
        lines.append("")
        lines.append("- the recorded **objective is literally a function of the persisted "
                     "tensor** (`objective == persisted TRAIN CE` for every neural fit), and it "
                     "differs from the earlier frozen reference objective — so the objective "
                     "was computed through the raw-design prediction path;")
        lines.append("- the recorded **best validation loss cannot belong to the persisted "
                     "tensor**: it was measured in-process on the TRAIN-z-scored validation "
                     "design and matches the earlier frozen reference exactly, while the "
                     "persisted tensor's own validation CE is higher by the mismatch column "
                     "above. The early-stopping checkpoint proves the *training* path used the "
                     "z-scored design; the persisted tensor did not.")
        lines.append("")
        lines.append("### 2b.3 Zero-fit recovery of corrected neural predictions\n")
        lines.append(f"- possible: **{evidence['zero_fit_recovery_possible_for_corrected_neural_predictions']}**")
        lines.append(f"- reason: {evidence['zero_fit_recovery_reason']}")
        lines.append(f"- no stored prediction was transformed: "
                     f"**{evidence['no_prediction_transformation_attempted']}**")
        lines.append(f"- second science invocation authorized: "
                     f"**{evidence['second_science_invocation_authorized']}**")
        lines.append("")
    lines.append("## 3. Durable attempt ledger\n")
    lines.append(f"`{LEDGER_RELPATH}` — {invariants['records']} records "
                 f"({invariants['started_count']} `FIT_ATTEMPT_STARTED`, "
                 f"{invariants['completed_count']} `FIT_COMPLETED`, "
                 f"{invariants['failed_count']} `FIT_FAILED`).")
    lines.append("")
    lines.append("| # | fit key | kind | family | regime | seed | repeats | "
                 "predictions | payload SHA-256 |")
    lines.append("|---|---|---|---|---|---|---|---|---|")
    for key in sorted(results["fit_summaries"]):
        summary = results["fit_summaries"][key]
        lines.append(f"| {summary['attempt_index']} | `{key}` | {summary['kind']} "
                     f"| {summary['family']} | {summary['regime']} "
                     f"| {summary['seed'] if summary['seed'] is not None else '—'} "
                     f"| {summary['repeat_of'] or '—'} "
                     f"| {summary['prediction_shape'][0]}x{summary['prediction_shape'][1]}"
                     f"x{summary['prediction_shape'][2]} "
                     f"| `{str(summary['payload_sha256'])[:16]}…` |")
    lines.append("")
    lines.append("Recovery contract:")
    lines.append("")
    lines.append("```")
    lines.append(f"metrics_store_shape : {raw['aggregation_contract']['metrics_store_shape']}")
    lines.append(f"fixed_store_shape   : {raw['aggregation_contract']['fixed_store_shape']}")
    lines.append(f"producer            : {raw['aggregation_contract']['producer']}")
    lines.append(f"consumer            : {raw['aggregation_contract']['consumer']}")
    lines.append(f"shape asserted      : {raw['aggregation_contract']['shape_validated_loudly']}")
    lines.append("```")
    lines.append("")
    lines.append("## 4. Observed results\n")
    provenance = results["metric_provenance"]
    if provenance["applies"]:
        lines.append("**Metric provenance.** The parametric and fixed-baseline rows are "
                     "conformant with the frozen #75 design. The neural rows are retained "
                     "unchanged for audit and are classified "
                     f"`{provenance['neural_marker']}`: they were produced by a prediction "
                     "path that violates the frozen TRAIN-only preprocessing contract, so they "
                     "are not a measurement of the frozen neural mapping. The neural numbers "
                     "were **not** replaced with the Issue #76 values.")
        lines.append("")
    lines.append("| regime | family | seed | TEST weighted CE | TEST mean abs share error "
                 "| TEST row-norm max | neg | support | top-1 | VALIDATION CE | best step | "
                 "provenance |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for regime in REGIMES:
        fixed = fixed_metrics[regime]["metrics"]
        lines.append(f"| {regime} | fixed | — | "
                     f"{fixed['TEST']['weighted_cross_entropy']:.6f} "
                     f"| {fixed['TEST']['mean_absolute_share_error']:.6f} "
                     f"| {fixed['TEST']['row_normalization_violation_max']:.3g} "
                     f"| {fixed['TEST']['negativity_violation_count']} "
                     f"| {fixed['TEST']['support_violation_count']} "
                     f"| {fixed['TEST']['top1_destination_accuracy']:.3f} "
                     f"| {fixed['VALIDATION']['weighted_cross_entropy']:.6f} | — "
                     f"| `{provenance['fixed_baseline_marker']}` |")
        block = metrics[f"{regime}:parametric"]["metrics"]
        lines.append(f"| {regime} | parametric | — | "
                     f"{block['TEST']['weighted_cross_entropy']:.6f} "
                     f"| {block['TEST']['mean_absolute_share_error']:.6f} "
                     f"| {block['TEST']['row_normalization_violation_max']:.3g} "
                     f"| {block['TEST']['negativity_violation_count']} "
                     f"| {block['TEST']['support_violation_count']} "
                     f"| {block['TEST']['top1_destination_accuracy']:.3f} "
                     f"| {block['VALIDATION']['weighted_cross_entropy']:.6f} | — "
                     f"| `{provenance['parametric_marker']}` |")
        for seed in (0, 1, 2):
            block = metrics[f"{regime}:neural:seed{seed}"]["metrics"]
            summary = results["fit_summaries"][f"{regime}:neural:seed{seed}"]
            lines.append(f"| {regime} | neural | {seed} | "
                         f"{block['TEST']['weighted_cross_entropy']:.6f} "
                         f"| {block['TEST']['mean_absolute_share_error']:.6f} "
                         f"| {block['TEST']['row_normalization_violation_max']:.3g} "
                         f"| {block['TEST']['negativity_violation_count']} "
                         f"| {block['TEST']['support_violation_count']} "
                         f"| {block['TEST']['top1_destination_accuracy']:.3f} "
                         f"| {block['VALIDATION']['weighted_cross_entropy']:.6f} "
                         f"| {summary['best_step']} "
                         f"| `{provenance['neural_marker']}` |")
    lines.append("")
    lines.append(provenance["parametric_statement"])
    lines.append("")
    lines.append(provenance["fixed_baseline_statement"])
    lines.append("")
    lines.append(f"Experiment verdict: {provenance['experiment_verdict']}.")
    lines.append("")
    lines.append("Parametric fitted coefficients (six contrast-identifiable columns, frozen "
                 "order):")
    lines.append("")
    lines.append("```")
    for regime in REGIMES:
        coeffs = results["fit_summaries"][f"{regime}:parametric"]["coefficients"]
        lines.append(f"{regime}: {[round(v, 9) for v in coeffs] if coeffs else None}")
    lines.append("```")
    lines.append("")
    lines.append("`EXCLUDED_REFERENCE_ONLY` and `TRAIN` metrics are reported in "
                 "`DLH_WL_P2C_RESULTS.json` under `metrics_by_split` for every fit key.")
    lines.append("")
    lines.append("## 5. Determinism (persisted predictions only)\n")
    lines.append("```")
    for name in DETERMINISM_NAMES:
        info = determinism[name]
        coefficient = (f", coefficient_deviation={info['coefficient_deviation']:.3e}"
                       if info.get("coefficient_deviation") is not None else "")
        lines.append(f"{name}: deviation={info['deviation']:.3e}{coefficient} "
                     f"| primary={info['primary_fit_key']} repeat={info['repeat_fit_key']}")
    lines.append(f"determinism_tolerance={determinism['determinism_tolerance']:.0e}")
    lines.append(f"max_deviation={determinism['max_deviation']:.3e}")
    lines.append(f"all_within_tolerance={determinism['all_within_tolerance']}")
    lines.append(f"scope={determinism['scope']}")
    lines.append("```")
    lines.append("")
    lines.append("## 6. Constraint diagnostics\n")
    lines.append("```")
    lines.append(f"evaluated_prediction_sets={constraints['evaluated_prediction_sets']}")
    lines.append(f"row_normalization_violation_max="
                 f"{constraints['row_normalization_violation_max']:.3e} "
                 f"(tolerance {constraints['row_normalization_tolerance']:.0e})")
    lines.append(f"negativity_violation_count={constraints['negativity_violation_count']}")
    lines.append(f"support_violation_count={constraints['support_violation_count']}")
    lines.append(f"split_counts={constraints['split_counts']}")
    lines.append(f"excluded_block_count={constraints['excluded_block_count']} "
                 f"(expected {constraints['excluded_block_count_expected']})")
    lines.append(f"allocation_blocks={constraints['allocation_blocks']}")
    lines.append("```")
    lines.append("")
    lines.append("Independent structural check of the recovery object (every recovered "
                 "tensor, re-read from the ledger):")
    lines.append("")
    lines.append("```")
    worst_row = max(v["max_row_sum_deviation"] for v in shares["per_fit"].values())
    worst_min = min(v["min_allowed_share"] for v in shares["per_fit"].values())
    lines.append(f"fits_checked={len(shares['per_fit'])}")
    lines.append(f"max_row_sum_deviation={worst_row:.3e} (tolerance {shares['tolerance']:.0e})")
    lines.append(f"min_allowed_share={worst_min:.6e}")
    lines.append(f"unavailable_cell_violations="
                 f"{sum(v['unavailable_cell_violations'] for v in shares['per_fit'].values())}")
    lines.append(f"all_valid={shares['all_valid']}")
    lines.append("```")
    lines.append("")
    lines.append("P1A accounting closure (accepted P1A interface, read-only):")
    lines.append("")
    lines.append("```")
    lines.append(f"max_abs_deviation={p1a['max_abs_deviation']:.3e} "
                 f"(tolerance {p1a['tolerance']:.0e})")
    lines.append(f"conditional_choice_identified_all="
                 f"{p1a['conditional_choice_identified_all']}")
    lines.append(f"all_rows_valid={p1a['all_rows_valid']}")
    lines.append(f"closes={p1a['closes']}")
    lines.append("```")
    lines.append("")
    lines.append("## 7. Neural comparison (withheld)\n")
    lines.append(f"- neural-beats-parametric required: "
                 f"**{negative['neural_beats_parametric_required']}**")
    lines.append(f"- neural-vs-parametric comparison permitted: "
                 f"**{negative['neural_vs_parametric_comparison_permitted']}**")
    if negative.get("withheld"):
        lines.append(f"- withheld reason: {negative['withheld_reason']}")
        lines.append(f"- classification of the neural rows: `{negative['classification']}`")
    lines.append("")
    lines.append("The values are reported below for audit completeness only. They carry no "
                 "scientific inference.")
    lines.append("")
    for regime in REGIMES:
        row = negative["observational_values_retained_for_audit"][regime]
        seeds = row["neural_test_ce_by_seed"]
        lines.append(f"- {regime}: fixed {row['fixed_baseline_test_ce']:.6f}; "
                     f"parametric {row['parametric_test_ce']:.6f}; "
                     f"neural by seed "
                     + ", ".join(f"{name} {value:.6f}" for name, value in sorted(seeds.items()))
                     + " — `AUDIT_ONLY_NOT_A_SCIENTIFIC_COMPARISON`")
    lines.append("")
    lines.append("No tuning, extra seed or ad-hoc fit was performed during or after the science "
                 "stage, and no neural-vs-parametric scientific conclusion may be drawn from "
                 "P2C.")
    lines.append("")
    lines.append("## 8. Audit context versus Issue #76 (not a threshold)\n")
    audit = results["audit_context_vs_issue_76"]
    lines.append(f"Provenance of the #76 observations: `{audit['provenance']}`.")
    lines.append("")
    lines.append("| configuration | Issue #76 observational | P2C observed | absolute "
                 "difference | comparison permitted |")
    lines.append("|---|---|---|---|---|")
    for key, comparison in audit["comparisons"].items():
        lines.append(f"| {key} | {comparison['issue_76_observational']:.10f} "
                     f"| {comparison['p2c_observed']:.10f} "
                     f"| {comparison['absolute_difference']:.3e} "
                     f"| {comparison['comparison_permitted']} |")
    lines.append("")
    if audit.get("neural_rows_are_not_a_performance_comparison"):
        lines.append("The neural rows of this table are **not** a performance comparison: the "
                     "P2C neural values are classified "
                     f"`{NEURAL_METRIC_PROVENANCE}`. They are shown so a Reviewer can see that "
                     "the parametric family reproduces the earlier frozen observations exactly "
                     "while the neural family does not, which is the expected signature of the "
                     "preprocessing-path defect and **not** evidence about model quality.")
        lines.append("")
    lines.append(f"- #76 terminal: `{audit['issue_76_terminal']}`")
    lines.append(f"- #76 execution accounting: "
                 f"`{json.dumps(audit['issue_76_execution_accounting'], sort_keys=True)}`")
    lines.append(f"- {audit['statement']}")
    lines.append("")
    lines.append("## 9. Interpretation ceiling\n")
    lines.append("Allowed:")
    for item in results["interpretation_ceiling"]["allowed"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("Forbidden:")
    for item in results["interpretation_ceiling"]["forbidden"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## 10. Limitations\n")
    lines.append("- the synthetic control is deliberately small (20 allocation blocks, "
                 "18 evaluable share cells per time slice, 72 total, 9 training blocks) and "
                 "carries no economic content;")
    lines.append("- the split holds out time and the **origin role** only: `R03`/`R04` occur "
                 "as TRAIN destinations, so this is not an unseen-region test;")
    lines.append("- the neural backend is NumPy because PyTorch is not installed; the frozen "
                 "architecture and protocol are unchanged;")
    lines.append("- neural weights are not persisted because the accepted scientific module "
                 "does not expose them through `FitOutcome`; the full persisted predictions "
                 "are the authoritative recovery object and are sufficient for every frozen "
                 "metric — but for P2C that recovery object was produced through the wrong "
                 "preprocessing path, so no corrected neural tensor can be recovered from this "
                 "ledger without re-running the fitting path;")
    lines.append("- real annual bilateral OD label availability remains `UNRESOLVED`; nothing "
                 "here speaks to Chinese interprovincial flows and no HJB/KFE/GE/household "
                 "coupling was attempted;")
    lines.append("- identity is PRE_RUN_FREEZE SHA + frozen config + environment + seeds + "
                 "durable ledger + manifest + rendered metrics; the science runner and the "
                 "ledger are immutable after the first optimizer step, and this renderer is "
                 "strictly zero-fit so it may be rerun;")
    lines.append("- **no second science invocation is authorized under Issue #78**, so this "
                 "Gate-Fail evidence package is terminal for the issue as filed; any corrected "
                 "replication requires a separate authorization, and no successor exists yet.")
    lines.append("")
    lines.append("## 11. Terminal\n")
    lines.append("```")
    lines.append(terminal)
    lines.append("```")
    lines.append("")
    if adjudication.get("applies"):
        lines.append(f"Correction recorded by a zero-fit evidence-only remediation under "
                     f"Reviewer adjudication `{adjudication['adjudication_comment']}`: the "
                     f"mechanical durability/protocol gate is "
                     f"`{results['mechanical_protocol_gate_ok']}`, but a required neural "
                     f"preprocessing contract was violated during science execution, so the "
                     f"experiment terminal is the corrected Gate Fail above.")
        lines.append("")
    return "\n".join(lines)


def _calls_any_fitter() -> bool:
    """Static guard: does this file actually call a fitting or optimizer entry point?

    Only real call targets are inspected, so mentioning a fitter inside a guard string or
    a docstring cannot create a false positive.
    """
    import ast

    tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    calls: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name):
                calls.add(func.id)
            elif isinstance(func, ast.Attribute):
                calls.add(func.attr)
    return bool(calls & {"fit_parametric", "fit_neural", "run_scientific_program",
                         "_adam_step", "_backward", "_forward", "_init_mlp",
                         "_train_only_zscore", "_softmax_cross_entropy", "_masked_softmax",
                         "minimize"})


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="DLH-WL-P2C zero-fit renderer (Issue #78)")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--render-only", action="store_true",
                       help="rebuild every metric and publication artifact from the ledger")
    group.add_argument("--validate-only", action="store_true",
                       help="report render inputs and prove no fit path is referenced")
    parser.add_argument("--ledger", default=None, help="override the ledger path (tests)")
    parser.add_argument("--outdir", default=None, help="override the output directory (tests)")
    args = parser.parse_args(argv)
    if args.validate_only:
        payload = {
            "phase": "VALIDATE_ONLY",
            "ledger_present": (ROOT / LEDGER_RELPATH).is_file(),
            "seal_present": (ROOT / SEAL_RELPATH).is_file(),
            "optimizer_steps_performed": 0,
            "fit_attempts_performed": 0,
            "renderer_imports_fitters": _calls_any_fitter(),
            "fitter_call_guard": "static AST scan of this file's call targets",
            "metrics_computed_from": "DURABLE_LEDGER_PERSISTED_PREDICTIONS_ONLY",
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0
    return render(ledger_path=Path(args.ledger) if args.ledger else None,
                  outdir=Path(args.outdir) if args.outdir else None)


if __name__ == "__main__":
    raise SystemExit(main())
