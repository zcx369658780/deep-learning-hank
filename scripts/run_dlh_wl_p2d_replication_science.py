"""DLH-WL-P2D — minimal preprocessing-corrected durable replication: science runner (#79).

This is the **only** authorized science path for Issue #79. It executes the frozen #75 fit
program exactly once, makes every completed fit's *complete scientific output* durable
before the next fit begins, and — the single authorized science-path repair of Issue #79 —
propagates the TRAIN-only z-scored design into the accepted neural prediction path.
Publication is a separate, strictly zero-fit stage
(``scripts/render_dlh_wl_p2d_replication.py``).

Binding rules implemented here (Issue #79 sections 2, 4, 5, 6):

* exactly one ``--execute-science`` invocation is authorized; there is no science retry,
  no second invocation and no patch-and-rerun after the first optimizer step;
* exactly 12 fit attempts in the frozen order: 2 parametric primaries, 2 parametric
  verification repeats, 6 neural primaries (seeds 0/1/2 x S0/S1) and 2 neural seed-0
  verification repeats;
* **the only scientific execution repair** (Issue #79 section 2): after the TRAIN-only
  z-score design is built and before any neural fit,
  ``universe._design_matrix = design`` is executed by ``setup_preprocessing_state``, so
  optimization, early stopping and the final persisted predictions all consume the same
  TRAIN-only z-scored design through ``universe.design_matrix``. Issue #78 failed because
  the runner omitted exactly this assignment, so neural parameters were trained on
  z-scored inputs while the persisted predictions were generated from the raw fallback;
* the runner **fails closed before fitting** if the installed prediction design does not
  equal the TRAIN-only z-scored design, so that defect can no longer happen silently;
* for every fit: append + flush + fsync ``FIT_ATTEMPT_STARTED``, execute exactly one
  frozen fit, serialize the complete ``FitOutcome`` (full 4x5x5 prediction tensor,
  coefficients when present, objective, convergence, best step, best validation loss,
  backend, diagnostics) plus the neural preprocessing-contract evidence and a canonical
  scientific-payload SHA-256, append + flush + fsync ``FIT_COMPLETED``, and only then
  allow the next fit to begin;
* the runner refuses to start if the P2D ledger or seal already exists, so no
  cross-invocation reset is possible;
* a fit or persistence failure after ``FIT_ATTEMPT_STARTED`` stops science immediately
  (no rerun) and is recorded durably;
* the accepted scientific module ``labor_destination_p2.py`` is imported and used
  byte-for-byte; it is never modified here;
* no real data, no HJB/KFE/GE/MATLAB/household code, no tuning, no extra seed, no full
  suite, no change to the frozen #75 scientific design.

This runner computes **no metric**: metrics, constraints, determinism and publication are
reconstructed from the durable ledger by the zero-fit renderer, so a later reporting
defect can never require another fit.

The scientific execution identity is the PRE_RUN_FREEZE commit SHA passed on the command
line, not this file's later commit.
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

import numpy as np  # noqa: E402

from deep_learning_hank.regional import labor_destination_p2 as sci  # noqa: E402

SCIENTIFIC_MODULE_RELPATH = "src/deep_learning_hank/regional/labor_destination_p2.py"
P1A_MODULE_RELPATH = "src/deep_learning_hank/regional/labor_destination.py"
CONFIG_RELPATH = "configs/dlh_wl_p2_offline_prototype.toml"
CONTRACT_RELPATH = "docs/specifications/DLH_WL_P2_OFFLINE_PROTOTYPE_CONTRACT_2026_09_18.md"
SCHEMA_RELPATH = "docs/data/DLH_WL_P1B_LABEL_AND_SAMPLE_SCHEMA_2026_09_18.md"

OUTDIR_RELPATH = "reports/dlh_wl_p2d_2026_09_19"
LEDGER_RELPATH = f"{OUTDIR_RELPATH}/DLH_WL_P2D_ATTEMPT_LEDGER.jsonl"
SEAL_RELPATH = f"{OUTDIR_RELPATH}/DLH_WL_P2D_SCIENCE_SEAL.json"

EXPECTED_SCIENTIFIC_MODULE_BLOB = "b1f2cd043605c511e4965254657d12306170609b"
EXPECTED_CONFIG_BLOB = "bb5dbbd0746e9d92874f94b03a1d54f3d382c4a8"

EXPERIMENT_ID = "EXP-20260919-DLH-WL-P2D-001"
TASK_ID = "DLH_WL_P2D_PREPROCESSING_CORRECTED_REPLICATION"
AUTHORITY_MARKER = "DLH_WL_P2D_PREPROCESSING_CORRECTED_DURABLE_REPLICATION_AUTHORIZED"
ROUTE = "DLH-WL-V1-20260918"
OWNER_ROUTE_LOCK = "DLH_WL_V1_20260918"
OPERATIVE_BASELINE = "a12caa1eb90afb07c368c5390a4f2ac751786672"
PUBLICATION_BASELINE = "4ae19abc9e951e2d4803a1239bb411f7a8798009"
PLANNED_FIT_ATTEMPTS = 12
SCIENCE_WALL_CLOCK_CEILING_SECONDS = 1800.0

SPLIT_STATES = ("TRAIN", "VALIDATION", "TEST", "EXCLUDED_REFERENCE_ONLY")

TERMINAL_PASS = ("DLH_WL_P2D_PREPROCESSING_CORRECTED_REPLICATION__PASS__"
                 "P2_METHOD_GATE_COMPLETE")
TERMINAL_GATE_FAIL = ("DLH_WL_P2D_PREPROCESSING_CORRECTED_REPLICATION__GATE_FAIL__"
                      "NO_SCIENCE_RERUN_AUTHORIZED")
TERMINAL_BLOCKED = "BLOCKED_DLH_WL_P2D_PRE_RUN_OR_ENVIRONMENT"

TRAINING_DESIGN_LABEL = "TRAIN_ONLY_ZSCORED"
PREDICTION_DESIGN_LABEL = "TRAIN_ONLY_ZSCORED"
REQUIRED_ASSIGNMENT = "universe._design_matrix = design"

# The scientific payload of one completed fit: everything a zero-fit recovery needs.
# Deliberately excludes environment-dependent timing (``runtime_seconds``), wall-clock
# bookkeeping (``recorded_utc``) and provenance (``pre_run_freeze_sha``), so the payload
# digest is a pure function of the reproducible scientific content.
PAYLOAD_SCIENTIFIC_KEYS = (
    "attempt_index",
    "fit_key",
    "kind",
    "repeat_of",
    "regime",
    "family",
    "seed",
    "backend",
    "objective",
    "convergence",
    "best_step",
    "best_validation_loss",
    "coefficients",
    "diagnostics",
    "predictions",
    "prediction_shape",
    "preprocessing_contract",
    "non_finite_originals",
)
PAYLOAD_CANONICALIZATION = (
    "sha256 over json.dumps(payload, sort_keys=True, separators=(',', ':'), "
    "ensure_ascii=True).encode('utf-8'), where payload is exactly PAYLOAD_SCIENTIFIC_KEYS "
    "taken from the FIT_COMPLETED record after JSON-safe float normalization"
)


# --------------------------------------------------------------------------- helpers
def sha256_lf(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest().upper()


def blob_sha1_lf(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def array_sha256(array: Any) -> str:
    """Platform-stable SHA-256 of a numeric design matrix.

    The dtype, shape and C-contiguity are part of the header and the buffer is cast to
    ``float64``, so the digest is identical in the science runner and in the zero-fit
    renderer, which separately recomputes it. This is what lets a Reviewer verify from
    the ledger that the trained and predicted design really were the same array.
    """
    a = np.ascontiguousarray(np.asarray(array, dtype=np.float64))
    header = f"{a.shape}|{a.dtype.str}|C".encode("ascii")
    return hashlib.sha256(header + b"\0" + a.tobytes()).hexdigest().upper()


def environment_summary() -> dict[str, Any]:
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


def dump_json_bytes(obj: Any) -> bytes:
    """Canonical serialization: indent 2, sorted keys, one trailing LF."""
    return json.dumps(obj, indent=2, sort_keys=True).encode("utf-8") + b"\n"


def write_json_durable(path: Path, obj: Any) -> None:
    """Write ``obj`` atomically and fsync the file before returning."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    payload = dump_json_bytes(obj)
    with tmp.open("wb") as handle:
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(tmp, path)


def json_safe(value: Any) -> tuple[Any, dict[str, str]]:
    """Recursively make ``value`` JSON-safe, collecting non-finite floats.

    ``NaN``/``+inf``/``-inf`` are legal Python floats but are *not* legal JSON, so they
    are replaced by ``None`` and their original spelling is recorded alongside. The
    substitution is applied identically at write and at verify time, so the recorded
    payload digest stays recomputable.
    """
    originals: dict[str, str] = {}

    def walk(node: Any, path: str) -> Any:
        if isinstance(node, dict):
            return {str(k): walk(v, f"{path}.{k}" if path else str(k))
                    for k, v in node.items()}
        if isinstance(node, (list, tuple)):
            return [walk(v, f"{path}[{i}]") for i, v in enumerate(node)]
        if isinstance(node, bool) or node is None:
            return node
        if isinstance(node, float):
            if node != node:
                originals[path or "<root>"] = "nan"
                return None
            if node == float("inf"):
                originals[path or "<root>"] = "inf"
                return None
            if node == float("-inf"):
                originals[path or "<root>"] = "-inf"
                return None
            return node
        if isinstance(node, (int, str)):
            return node
        raise TypeError(f"non-serializable value at {path!r}: {type(node).__name__}")

    return walk(value, ""), originals


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
        "science_invocations": 1,
        "science_retries": 0,
    }


def refuse_if_outputs_exist(ledger_path: Path, seal_path: Path | None = None) -> str | None:
    """Fail closed when a previous P2D ledger (or seal) is present."""
    if ledger_path.exists():
        return f"ledger already exists: {ledger_path}"
    if seal_path is not None and seal_path.exists():
        return f"science seal already exists: {seal_path}"
    return None


# --------------------------------------------------------------------------- payload
def payload_of(record: dict[str, Any]) -> dict[str, Any]:
    """The canonical scientific payload of a record (see ``PAYLOAD_SCIENTIFIC_KEYS``)."""
    return {key: record[key] for key in PAYLOAD_SCIENTIFIC_KEYS if key in record}


def canonical_payload_sha256(record: dict[str, Any]) -> str:
    """SHA-256 over the canonical serialization of the scientific payload."""
    blob = json.dumps(payload_of(record), sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("utf-8")
    return hashlib.sha256(blob).hexdigest().upper()


def encode_predictions(predictions: Any, universe: sci.SyntheticUniverse) -> dict[str, Any]:
    """Serialise a full prediction tensor as JSON-safe nested lists, with validation.

    The tensor is the authoritative zero-fit recovery object, so it is validated here:
    it must be finite, it must have the frozen ``(T, R, R)`` shape, every allowed cell of
    every block must be present, and every structurally unavailable cell must be exactly
    ``0.0`` (otherwise a support violation would be silently persisted).
    """
    cfg = universe.config
    R = len(cfg.region_ids)
    T = len(cfg.time_ids)
    arr = np.asarray(predictions, dtype=float)
    if arr.shape != (T, R, R):
        raise ValueError(f"prediction tensor shape {arr.shape} != frozen {(T, R, R)}")
    if not np.all(np.isfinite(arr)):
        raise ValueError("prediction tensor contains a non-finite value")
    for block in universe.blocks:
        for j in range(R):
            if j in block.allowed:
                continue
            if arr[block.time_index, block.origin, j] != 0.0:
                raise ValueError(
                    f"structurally unavailable cell ({block.time_index},{block.origin},{j}) "
                    f"is not zero")
    safe, non_finite = json_safe(arr.tolist())
    if non_finite:  # pragma: no cover - guarded by the isfinite check above
        raise ValueError(f"non-finite prediction values: {non_finite}")
    return {"predictions": safe, "prediction_shape": [T, R, R]}


def decode_predictions(record: dict[str, Any]) -> np.ndarray:
    """Rebuild the full prediction tensor from a durable ``FIT_COMPLETED`` record."""
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


def setup_preprocessing_state(universe: sci.SyntheticUniverse,
                              blocks: Sequence[sci.Block] | None = None
                              ) -> tuple[np.ndarray, dict[str, Any]]:
    """THE single place where the frozen TRAIN-only preprocessing state is installed.

    Issue #79 section 2 — the only authorized science-path repair. The accepted module
    computes the TRAIN-only z-scored design and then, in its canonical
    ``run_scientific_program`` path, assigns it to the universe:

    ``design, preprocess_meta = _train_only_zscore(universe, universe.blocks_for("TRAIN"))``
    ``universe._design_matrix = design``

    That assignment is load-bearing: ``fit_neural(..., design=design)`` optimizes on the
    supplied design, but the module's final prediction path is
    ``_neural_predict -> _neural_predict_blocks -> universe.design_matrix``, and
    ``SyntheticUniverse.design_matrix`` silently falls back to ``raw_design`` when
    ``_design_matrix`` is None. Issue #78 omitted the assignment, so neural parameters were
    trained on TRAIN-z-scored inputs while the persisted prediction tensors were generated
    on raw inputs.

    This helper performs the assignment and returns ``(design, metadata)`` describing the
    installed state. Both the science execution and the pre-run focused tests call this
    exact function, so the tested path is the executed path.
    """
    design, meta = sci._train_only_zscore(
        universe, universe.blocks_for("TRAIN") if blocks is None else blocks)
    universe._design_matrix = design            # <- the Issue #79 repair
    installed = universe.design_matrix
    meta = {
        **meta,
        "assignment_performed": REQUIRED_ASSIGNMENT,
        "training_design": TRAINING_DESIGN_LABEL,
        "prediction_design": PREDICTION_DESIGN_LABEL,
        "design_installed_on_universe": bool(np.array_equal(design, installed)),
        "design_sha256": array_sha256(design),
        "raw_design_sha256": array_sha256(universe.raw_design),
        "zscored_differs_from_raw": bool(not np.array_equal(design, universe.raw_design)),
        "design_shape": list(np.asarray(design).shape),
    }
    return design, meta


def preprocessing_evidence_block(universe: sci.SyntheticUniverse, design: np.ndarray,
                                 preprocessing: dict[str, Any]) -> dict[str, Any]:
    """Durable preprocessing-contract evidence for one neural fit (Issue #79 section 4).

    Evaluated immediately before the fit runs with no optimizer step: it records the
    TRAIN-z-scored design used for optimization and early stopping, the array the final
    prediction path will actually read (``universe.design_matrix``), whether the two are
    the same array, and the raw design separately.

    It **fails closed**: if the installed prediction design is not the TRAIN-only z-scored
    design, the runner refuses to fit instead of silently persisting predictions produced
    through the raw fallback. That is the Issue #78 defect made impossible.
    """
    installed = np.asarray(universe.design_matrix, dtype=float)
    reference = np.asarray(design, dtype=float)
    raw = np.asarray(universe.raw_design, dtype=float)
    block = {
        "applies": True,
        "training_design": TRAINING_DESIGN_LABEL,
        "prediction_design": PREDICTION_DESIGN_LABEL,
        "required_assignment": REQUIRED_ASSIGNMENT,
        "fitted_on": "TRAIN_ONLY",
        "train_row_count": int(preprocessing.get("train_row_count", 0)),
        "zscored_features": list(preprocessing.get("zscored_features", [])),
        "zscored_design_sha256": array_sha256(reference),
        "universe_design_matrix_sha256_before_fit": array_sha256(installed),
        "design_equality_flag": bool(np.array_equal(reference, installed)),
        "raw_design_sha256": array_sha256(raw),
        "zscored_differs_from_raw": bool(not np.array_equal(reference, raw)),
        "design_shape": list(reference.shape),
        "raw_design_shape": list(raw.shape),
        "design_max_abs_difference_from_raw": float(np.abs(reference - raw).max()),
        "prediction_path": ("_neural_predict -> _neural_predict_blocks -> "
                            "universe.design_matrix"),
    }
    if not block["design_equality_flag"]:
        raise RuntimeError(
            "refusing to fit: the installed prediction design is not the TRAIN-only "
            "z-scored design, so the persisted predictions would come from the raw-design "
            "fallback (the Issue #78 defect). Missing assignment: " + REQUIRED_ASSIGNMENT)
    if not block["zscored_differs_from_raw"]:
        raise RuntimeError(
            "refusing to fit: the TRAIN-only z-scored design is identical to the raw "
            "design, so the frozen preprocessing contract was not actually applied")
    return block


def parametric_preprocessing_block() -> dict[str, Any]:
    """The parametric family never reads ``universe.design_matrix``; recorded explicitly."""
    return {
        "applies": False,
        "reason": "PARAMETRIC_PATH_USES_THE_FROZEN_CONTRAST_FITTED_MATRIX",
        "fitted_on": "TRAIN_ONLY",
        "prediction_path": "_parametric_predict -> _fitted_matrix (six fitted columns)",
        "training_design": "NOT_APPLICABLE",
        "prediction_design": "NOT_APPLICABLE",
    }


def build_completed_record(entry: dict[str, Any], outcome: sci.FitOutcome,
                           universe: sci.SyntheticUniverse, runtime_seconds: float,
                           pre_run_freeze_sha: str,
                           preprocessing_contract: dict[str, Any] | None = None
                           ) -> dict[str, Any]:
    """Assemble the complete, JSON-safe ``FIT_COMPLETED`` record for one fit."""
    encoded = encode_predictions(outcome.predictions, universe)
    if preprocessing_contract is None:
        preprocessing_contract = parametric_preprocessing_block()
    raw_payload: dict[str, Any] = {
        "attempt_index": entry["attempt_index"],
        "fit_key": entry["fit_key"],
        "kind": entry["kind"],
        "repeat_of": entry.get("repeat_of"),
        "regime": entry["regime"],
        "family": entry["family"],
        "seed": entry["seed"],
        "backend": outcome.backend,
        "objective": outcome.objective,
        "convergence": outcome.convergence,
        "best_step": outcome.best_step,
        "best_validation_loss": outcome.best_validation_loss,
        "coefficients": outcome.coefficients,
        "diagnostics": outcome.diagnostics,
        "predictions": encoded["predictions"],
        "prediction_shape": encoded["prediction_shape"],
        "preprocessing_contract": preprocessing_contract,
    }
    safe, non_finite = json_safe(raw_payload)
    if not isinstance(safe, dict):  # pragma: no cover - raw_payload is a dict
        raise TypeError("payload must serialize to a JSON object")
    safe["non_finite_originals"] = non_finite
    record: dict[str, Any] = {
        "event": "FIT_COMPLETED",
        "recorded_utc": utc_now(),
        "pre_run_freeze_sha": pre_run_freeze_sha,
        "planned_attempts": PLANNED_FIT_ATTEMPTS,
        "runtime_seconds": float(runtime_seconds),
        "attempts": int(outcome.attempts),
        "payload_canonicalization": PAYLOAD_CANONICALIZATION,
    }
    record.update(safe)
    record["payload_sha256"] = canonical_payload_sha256(record)
    return record


# --------------------------------------------------------------------------- plan
def build_fit_plan(config: sci.P2Config) -> list[dict[str, Any]]:
    """The frozen 12-attempt program, in order, as pure data (no fit is executed)."""
    plan: list[dict[str, Any]] = []
    index = 0
    for regime in ("S0", "S1"):
        index += 1
        plan.append({"attempt_index": index, "kind": "primary", "family": "parametric",
                     "regime": regime, "seed": None, "repeat_of": None,
                     "fit_key": f"{regime}:parametric"})
    for regime in ("S0", "S1"):
        index += 1
        plan.append({"attempt_index": index, "kind": "verification_repeat",
                     "family": "parametric", "regime": regime, "seed": None,
                     "repeat_of": f"{regime}:parametric",
                     "fit_key": f"{regime}:parametric:repeat"})
    for regime in ("S0", "S1"):
        for seed in config.neural_seeds:
            index += 1
            plan.append({"attempt_index": index, "kind": "primary", "family": "neural",
                         "regime": regime, "seed": int(seed), "repeat_of": None,
                         "fit_key": f"{regime}:neural:seed{int(seed)}"})
    for regime in ("S0", "S1"):
        index += 1
        plan.append({"attempt_index": index, "kind": "verification_repeat",
                     "family": "neural", "regime": regime, "seed": 0,
                     "repeat_of": f"{regime}:neural:seed0",
                     "fit_key": f"{regime}:neural:seed0:repeat"})
    if len(plan) != PLANNED_FIT_ATTEMPTS:
        raise ValueError(f"frozen plan must have exactly {PLANNED_FIT_ATTEMPTS} attempts "
                         f"(got {len(plan)})")
    if [e["attempt_index"] for e in plan] != list(range(1, PLANNED_FIT_ATTEMPTS + 1)):
        raise ValueError("frozen plan attempt indices must be 1..12")
    if len({e["fit_key"] for e in plan}) != PLANNED_FIT_ATTEMPTS:
        raise ValueError("frozen plan fit keys must be unique")
    return plan


def primary_fit_keys(plan: Sequence[dict[str, Any]]) -> list[str]:
    return [e["fit_key"] for e in plan if e["kind"] == "primary"]


def repeat_pairs(plan: Sequence[dict[str, Any]]) -> list[tuple[str, str]]:
    return [(e["repeat_of"], e["fit_key"]) for e in plan
            if e["kind"] == "verification_repeat"]


# --------------------------------------------------------------------------- science
def run_one_fit(universe: sci.SyntheticUniverse, entry: dict[str, Any],
                design: Any) -> sci.FitOutcome:
    """Execute exactly one frozen fit.

    This is the **only** place in the P2D code base where an optimizer can run. The
    zero-fit renderer is statically guarded against ever reaching it.
    """
    family, regime, seed = entry["family"], entry["regime"], entry["seed"]
    if family == "parametric":
        return sci.fit_parametric(universe, regime)
    if family == "neural":
        return sci.fit_neural(universe, regime, int(seed), design=design)
    raise ValueError(f"unknown fit family {family!r}")


def verify_module_blob() -> tuple[str, str]:
    """Return ``(observed_blob, status)`` for the accepted scientific module."""
    blob = blob_sha1_lf(ROOT / SCIENTIFIC_MODULE_RELPATH)
    return blob, ("MATCH" if blob == EXPECTED_SCIENTIFIC_MODULE_BLOB else "MISMATCH")


def build_science_seal(pre_run_freeze_sha: str, summary: dict[str, Any],
                       wall_clock: float, ledger_path: Path,
                       module_blob: str, terminal: str, notes: str) -> dict[str, Any]:
    """Identities, counts, timing and the ledger hash only — no metric is computed."""
    return {
        "experiment_id": EXPERIMENT_ID,
        "issue": 79,
        "task_id": TASK_ID,
        "authority_marker": AUTHORITY_MARKER,
        "route": ROUTE,
        "phase": "SCIENCE_STAGE_SEAL",
        "recorded_utc": utc_now(),
        "pre_run_freeze_sha": pre_run_freeze_sha,
        "science_invocations": 1,
        "science_retries": 0,
        "planned_fit_executions": PLANNED_FIT_ATTEMPTS,
        "started_count": summary["started_count"],
        "completed_count": summary["completed_count"],
        "failed_count": summary["failed_count"],
        "science_wall_clock_seconds": float(wall_clock),
        "science_wall_clock_ceiling_seconds": SCIENCE_WALL_CLOCK_CEILING_SECONDS,
        "within_wall_clock_ceiling": bool(wall_clock <= SCIENCE_WALL_CLOCK_CEILING_SECONDS),
        "scientific_module_relpath": SCIENTIFIC_MODULE_RELPATH,
        "scientific_module_blob_sha1": module_blob,
        "expected_scientific_module_blob_sha1": EXPECTED_SCIENTIFIC_MODULE_BLOB,
        "ledger_relpath": LEDGER_RELPATH,
        "ledger_sha256_lf": sha256_lf(ledger_path),
        "ledger_record_count": summary["records"],
        "terminal": terminal,
        "notes": notes,
        "not_an_acceptance": "science-stage accounting seal; acceptance is decided by the "
                             "Reviewer, not by this artifact",
        "no_metric_computed_here": True,
    }


def execute_science(pre_run_freeze_sha: str) -> int:
    ledger_path = ROOT / LEDGER_RELPATH
    seal_path = ROOT / SEAL_RELPATH

    refusal = refuse_if_outputs_exist(ledger_path, seal_path)
    if refusal is not None:
        print(json.dumps({"terminal": TERMINAL_GATE_FAIL,
                          "reason": f"refusing to run science: {refusal}",
                          "science_invocations": 0}, indent=2))
        return 3

    config = sci.load_frozen_config(ROOT, config_relpath=CONFIG_RELPATH)
    module_blob, module_status = verify_module_blob()
    config_blob = blob_sha1_lf(ROOT / CONFIG_RELPATH)
    if module_status != "MATCH":
        print(json.dumps({"terminal": TERMINAL_BLOCKED,
                          "reason": f"scientific module blob {module_blob} != expected "
                                    f"{EXPECTED_SCIENTIFIC_MODULE_BLOB}"}, indent=2))
        return 3
    if config_blob != EXPECTED_CONFIG_BLOB:
        print(json.dumps({"terminal": TERMINAL_BLOCKED,
                          "reason": f"frozen config blob {config_blob} != expected "
                                    f"{EXPECTED_CONFIG_BLOB}"}, indent=2))
        return 3

    universe = sci.build_universe(config, ROOT)
    # Issue #79 section 2: the single authorized science-path repair. The TRAIN-only
    # z-scored design is computed AND installed on the universe before any fit, so
    # optimization, early stopping and the final persisted predictions all consume the
    # same design through universe.design_matrix.
    design, preprocessing = setup_preprocessing_state(universe)
    plan = build_fit_plan(config)

    started_at = time.perf_counter()
    science_terminal = TERMINAL_PASS
    notes = "all 12 frozen fits completed and were made durable one by one"
    try:
        for entry in plan:
            if entry["attempt_index"] > PLANNED_FIT_ATTEMPTS:
                raise RuntimeError("attempt index beyond the frozen plan")
            # preprocessing evidence captured immediately before the fit, with no
            # optimizer step; fails closed if the TRAIN-z-scored state is not installed
            if entry["family"] == "neural":
                preprocessing_contract = preprocessing_evidence_block(
                    universe, design, preprocessing)
            else:
                preprocessing_contract = parametric_preprocessing_block()
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
                "repeat_of": entry.get("repeat_of"),
                "pre_run_freeze_sha": pre_run_freeze_sha,
                "started_monotonic_seconds": time.perf_counter() - started_at,
                "training_design": preprocessing_contract["training_design"],
                "prediction_design": preprocessing_contract["prediction_design"],
                "design_equality_flag": preprocessing_contract.get("design_equality_flag"),
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
                notes = (f"fit {entry['fit_key']} failed after FIT_ATTEMPT_STARTED "
                         f"({type(exc).__name__}); science stopped, no rerun authorized")
                break
            runtime = time.perf_counter() - attempt_started
            try:
                record = build_completed_record(entry, outcome, universe, runtime,
                                                pre_run_freeze_sha,
                                                preprocessing_contract)
                append_ledger_record(ledger_path, record)
            except Exception as exc:
                append_ledger_record(ledger_path, {
                    "event": "FIT_FAILED",
                    "recorded_utc": utc_now(),
                    "attempt_index": entry["attempt_index"],
                    "fit_key": entry["fit_key"],
                    "error_type": f"PERSISTENCE_{type(exc).__name__}",
                    "error": str(exc)[:500],
                    "runtime_seconds": runtime,
                })
                science_terminal = TERMINAL_GATE_FAIL
                notes = (f"persistence of fit {entry['fit_key']} failed after "
                         f"FIT_ATTEMPT_STARTED ({type(exc).__name__}); science stopped, "
                         f"no rerun authorized")
                break
            print(json.dumps({
                "fit_completed": entry["fit_key"],
                "attempt_index": entry["attempt_index"],
                "runtime_seconds": round(runtime, 6),
                "payload_sha256": record["payload_sha256"],
            }, sort_keys=True), flush=True)
    except Exception as exc:  # pragma: no cover - accounting failure of last resort
        science_terminal = TERMINAL_GATE_FAIL
        notes = f"science runner aborted: {type(exc).__name__}: {str(exc)[:300]}"

    science_wall_clock = time.perf_counter() - started_at
    records = read_ledger(ledger_path)
    summary = ledger_summary(records)

    complete = (summary["started_count"] == PLANNED_FIT_ATTEMPTS
                and summary["completed_count"] == PLANNED_FIT_ATTEMPTS
                and summary["failed_count"] == 0)
    within_ceiling = science_wall_clock <= SCIENCE_WALL_CLOCK_CEILING_SECONDS
    if not (complete and within_ceiling):
        science_terminal = TERMINAL_GATE_FAIL
    if complete and not within_ceiling:
        notes = (f"all 12 fits completed but the science wall clock {science_wall_clock:.3f} s "
                 f"exceeds the {SCIENCE_WALL_CLOCK_CEILING_SECONDS:.0f} s ceiling")

    seal = build_science_seal(pre_run_freeze_sha, summary, science_wall_clock, ledger_path,
                              module_blob, science_terminal, notes)
    seal_written = True
    try:
        write_json_durable(seal_path, seal)
    except Exception as exc:  # pragma: no cover - durability failure of last resort
        seal_written = False
        print(json.dumps({"warning": "science seal could not be written",
                          "error": f"{type(exc).__name__}: {str(exc)[:300]}"}, indent=2))

    gate_ok = bool(complete and within_ceiling)
    print(json.dumps({
        "phase": "SCIENCE_STAGE",
        "pre_run_freeze_sha": pre_run_freeze_sha,
        "science_invocations": 1,
        "science_retries": 0,
        "started": summary["started_count"],
        "completed": summary["completed_count"],
        "failed": summary["failed_count"],
        "science_wall_clock_seconds": science_wall_clock,
        "within_wall_clock_ceiling": within_ceiling,
        "preprocessing_train_rows": preprocessing["train_row_count"],
        "preprocessing_assignment": preprocessing["assignment_performed"],
        "training_design": TRAINING_DESIGN_LABEL,
        "prediction_design": PREDICTION_DESIGN_LABEL,
        "zscored_design_sha256": preprocessing["design_sha256"],
        "raw_design_sha256": preprocessing["raw_design_sha256"],
        "zscored_differs_from_raw": preprocessing["zscored_differs_from_raw"],
        "seal_written": seal_written,
        "ledger": LEDGER_RELPATH,
        "seal": SEAL_RELPATH if seal_written else None,
        "gate_ok": gate_ok,
        "terminal": science_terminal,
        "next_stage": "zero-fit render-only reconstruction from the durable ledger",
    }, indent=2))
    return 0 if gate_ok else 2


# --------------------------------------------------------------------------- validate
def validate_only() -> int:
    """Config/generator/module identity and persistence-format checks; zero fits."""
    config = sci.load_frozen_config(ROOT, config_relpath=CONFIG_RELPATH)
    universe = sci.build_universe(config, ROOT)
    report = sci.validate_only_report(universe)
    plan = build_fit_plan(config)
    module_blob, module_status = verify_module_blob()
    ledger_path = ROOT / LEDGER_RELPATH
    seal_path = ROOT / SEAL_RELPATH

    # zero-fit proof of the Issue #79 repair: the setup helper installs the TRAIN-only
    # z-scored design, the prediction path reads it, and no optimizer is touched
    design_before = universe._design_matrix
    design, preprocessing = setup_preprocessing_state(universe)
    design_installed = bool(np.array_equal(design, universe.design_matrix))
    design_is_raw = bool(universe.design_matrix is universe.raw_design)
    neural_evidence = preprocessing_evidence_block(universe, design, preprocessing)

    # zero-fit proof that the durable payload format round-trips, using the frozen fixed
    # baseline as a stand-in prediction tensor (no optimizer is touched)
    fixed = sci.fixed_baseline_predictions(universe, "S0")
    encoded = encode_predictions(fixed, universe)
    decoded = decode_predictions({
        "fit_key": "VALIDATE_ONLY_FIXED_BASELINE",
        "predictions": encoded["predictions"],
        "prediction_shape": encoded["prediction_shape"],
    })
    roundtrip = bool(np.array_equal(np.asarray(fixed, dtype=float), decoded))
    probe = {
        "attempt_index": 0, "fit_key": "VALIDATE_ONLY_PROBE", "kind": "probe",
        "repeat_of": None, "regime": "S0", "family": "parametric", "seed": None,
        "backend": "NO_BACKEND_VALIDATE_ONLY", "objective": 0.0,
        "convergence": {"success": True, "status": 0, "message": "probe",
                        "iterations": 0, "function_evaluations": 0,
                        "gradient_norm_inf": 0.0},
        "best_step": None, "best_validation_loss": None, "coefficients": [0.0] * 6,
        "diagnostics": {"probe": True},
        "predictions": encoded["predictions"], "prediction_shape": encoded["prediction_shape"],
        "preprocessing_contract": neural_evidence,
        "non_finite_originals": {},
    }
    probe["payload_sha256"] = canonical_payload_sha256(probe)
    hash_stable = canonical_payload_sha256(probe) == probe["payload_sha256"]
    json.dumps(probe, sort_keys=True)  # raises if the record is not JSON-safe

    payload = {
        "phase": "VALIDATE_ONLY",
        "optimizer_steps_performed": 0,
        "fit_attempts_performed": 0,
        "config_revision": config.config_revision,
        "config_blob_sha1": blob_sha1_lf(ROOT / CONFIG_RELPATH),
        "expected_config_blob_sha1": EXPECTED_CONFIG_BLOB,
        "config_blob_status": ("MATCH" if blob_sha1_lf(ROOT / CONFIG_RELPATH)
                              == EXPECTED_CONFIG_BLOB else "MISMATCH"),
        "scientific_module_blob_sha1": module_blob,
        "expected_scientific_module_blob_sha1": EXPECTED_SCIENTIFIC_MODULE_BLOB,
        "module_blob_status": module_status,
        "contract_blob_sha1": blob_sha1_lf(ROOT / CONTRACT_RELPATH),
        "schema_blob_sha1": blob_sha1_lf(ROOT / SCHEMA_RELPATH),
        "p1a_module_blob_sha1": blob_sha1_lf(ROOT / P1A_MODULE_RELPATH),
        "planned_fit_attempts": len(plan),
        "primary_fit_keys": primary_fit_keys(plan),
        "repeat_pairs": repeat_pairs(plan),
        # ---- Issue #79 preprocessing-path state (zero-fit) ------------------
        "preprocessing_required_assignment": REQUIRED_ASSIGNMENT,
        "preprocessing_assignment_performed": preprocessing["assignment_performed"],
        "design_matrix_unset_before_setup": design_before is None,
        "design_installed_equals_zscored_design": design_installed,
        "design_matrix_is_not_raw_fallback": not design_is_raw,
        "training_design": TRAINING_DESIGN_LABEL,
        "prediction_design": PREDICTION_DESIGN_LABEL,
        "zscored_design_sha256": preprocessing["design_sha256"],
        "before_fit_design_sha256": neural_evidence[
            "universe_design_matrix_sha256_before_fit"],
        "design_equality_flag": neural_evidence["design_equality_flag"],
        "raw_design_sha256": preprocessing["raw_design_sha256"],
        "zscored_differs_from_raw": preprocessing["zscored_differs_from_raw"],
        "design_max_abs_difference_from_raw": neural_evidence[
            "design_max_abs_difference_from_raw"],
        "design_shape": preprocessing["design_shape"],
        # ---- persistence format ---------------------------------------------
        "prediction_tensor_shape": encoded["prediction_shape"],
        "prediction_roundtrip_exact": roundtrip,
        "payload_hash_verifies": hash_stable,
        "payload_record_is_json_safe": True,
        "contrast_rank": report["contrast_rank"],
        "s0_contrast_residual": report["s0_contrast_residual"],
        "s1_contrast_residual": report["s1_contrast_residual"],
        "x2_contrast_residual": report["x2_contrast_residual"],
        "x3_contrast_residual": report["x3_contrast_residual"],
        "split_counts": report["split_counts"],
        "reference_shares": report["reference_shares"],
        "ledger_present": ledger_path.exists(),
        "seal_present": seal_path.exists(),
        "science_start_allowed": refuse_if_outputs_exist(ledger_path, seal_path) is None,
        "environment": environment_summary(),
    }
    print(json.dumps(payload, indent=2, sort_keys=True)[:6000])
    print("\nVALIDATE_ONLY_COMPLETE__ZERO_OPTIMIZER_STEPS__ZERO_FITS")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="DLH-WL-P2D science runner (Issue #79)")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--validate-only", action="store_true",
                       help="config/generator/module/payload-format checks; zero fits")
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
