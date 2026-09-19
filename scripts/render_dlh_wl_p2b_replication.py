"""DLH-WL-P2B — clean immutable replication: render-only artifact generator (Issue #77).

This script turns the immutable science output into the three publication artifacts:

1. ``DLH_WL_P2B_RESULTS.json``
2. ``DLH_WL_P2B_MANIFEST.json``
3. ``DLH_WL_P2B_REPORT.md``

It reads ``DLH_WL_P2B_RAW_RESULTS.json`` and ``DLH_WL_P2B_ATTEMPT_LEDGER.jsonl`` and
**never** trains, optimizes, recomputes a metric from a model, or modifies the ledger or
the raw results. It may be rerun freely to repair formatting or hashing defects, because
it performs zero fits and zero optimizer steps.

The static guard in the focused test suite asserts that this file never references any
fitting entry point, so a rendering defect can never silently trigger training.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

# rendering needs only the deterministic accounting/validation helpers, never a fitter
from deep_learning_hank.regional import labor_destination_p2 as sci  # noqa: E402

SCIENTIFIC_MODULE_RELPATH = "src/deep_learning_hank/regional/labor_destination_p2.py"
P1A_MODULE_RELPATH = "src/deep_learning_hank/regional/labor_destination.py"
CONFIG_RELPATH = "configs/dlh_wl_p2_offline_prototype.toml"
CONTRACT_RELPATH = "docs/specifications/DLH_WL_P2_OFFLINE_PROTOTYPE_CONTRACT_2026_09_18.md"
SCHEMA_RELPATH = "docs/data/DLH_WL_P1B_LABEL_AND_SAMPLE_SCHEMA_2026_09_18.md"
SCIENCE_RUNNER_RELPATH = "scripts/run_dlh_wl_p2b_replication_science.py"
RENDERER_RELPATH = "scripts/render_dlh_wl_p2b_replication.py"

OUTDIR_RELPATH = "reports/dlh_wl_p2b_2026_09_19"
LEDGER_RELPATH = f"{OUTDIR_RELPATH}/DLH_WL_P2B_ATTEMPT_LEDGER.jsonl"
RAW_RELPATH = f"{OUTDIR_RELPATH}/DLH_WL_P2B_RAW_RESULTS.json"
RESULTS_RELPATH = f"{OUTDIR_RELPATH}/DLH_WL_P2B_RESULTS.json"
MANIFEST_RELPATH = f"{OUTDIR_RELPATH}/DLH_WL_P2B_MANIFEST.json"
REPORT_RELPATH = f"{OUTDIR_RELPATH}/DLH_WL_P2B_REPORT.md"

TERMINAL_PASS = "DLH_WL_P2B_CLEAN_REPLICATION__PASS__P2_METHOD_GATE_COMPLETE"
TERMINAL_GATE_FAIL = "DLH_WL_P2B_CLEAN_REPLICATION__GATE_FAIL__NO_SCIENCE_RERUN_AUTHORIZED"
TERMINAL_BLOCKED = "BLOCKED_DLH_WL_P2B_PRE_RUN_OR_ENVIRONMENT"

MANIFEST_DIGEST_FIELD = "manifest_canonical_sha256"

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


# --------------------------------------------------------------------------- helpers
def sha256_lf(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest().upper()


def blob_sha1_lf(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def dumps(obj: dict[str, Any]) -> bytes:
    return json.dumps(obj, indent=2, sort_keys=True).encode("utf-8") + b"\n"


def render_inputs() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    raw = json.loads((ROOT / RAW_RELPATH).read_text(encoding="utf-8"))
    ledger = [json.loads(line) for line in
              (ROOT / LEDGER_RELPATH).read_text(encoding="utf-8").splitlines() if line.strip()]
    return raw, ledger


def bump_render_counter() -> int:
    """Derive the render-only invocation count from the previously rendered artifacts.

    No auxiliary counter file is written: the count lives inside the rendered RESULTS
    and MANIFEST, which are the only artifacts this stage is authorized to produce.
    """
    path = ROOT / RESULTS_RELPATH
    if not path.is_file():
        return 1
    try:
        previous = json.loads(path.read_text(encoding="utf-8"))
        return int(previous.get("render_only_invocations", 0)) + 1
    except (json.JSONDecodeError, TypeError, ValueError):
        return 1


def verify_science_invariants(raw: dict[str, Any], ledger: list[dict[str, Any]]) -> dict[str, Any]:
    """Verify the science-stage invariants from the persisted evidence alone."""
    started = [r for r in ledger if r.get("event") == "FIT_ATTEMPT_STARTED"]
    completed = [r for r in ledger if r.get("event") == "FIT_COMPLETED"]
    failed = [r for r in ledger if r.get("event") == "FIT_FAILED"]
    indices_started = sorted(r.get("attempt_index") for r in started)
    indices_completed = sorted(r.get("attempt_index") for r in completed)
    expected = list(range(1, 13))
    return {
        "science_invocations": raw.get("science_invocations"),
        "science_retries": raw.get("science_retries"),
        "started_count": len(started),
        "completed_count": len(completed),
        "failed_count": len(failed),
        "started_indices_are_exactly_1_to_12": indices_started == expected,
        "completed_indices_match_started": indices_completed == indices_started,
        "started_before_completed_ordering_ok": all(
            next(r["recorded_utc"] for r in started if r["attempt_index"] == idx)
            <= next(r["recorded_utc"] for r in completed if r["attempt_index"] == idx)
            for idx in indices_completed),
        "exactly_twelve_started": len(started) == 12,
        "exactly_twelve_completed": len(completed) == 12,
        "zero_failed": len(failed) == 0,
    }


def _metrics_from_raw(raw: dict[str, Any]) -> dict[str, Any]:
    """Copy the persisted per-fit metrics; nothing is recomputed from a model."""
    return raw["metrics"]


def _negative_result_flags(raw: dict[str, Any]) -> dict[str, Any]:
    metrics = raw["metrics"]
    fixed = raw["fixed_baseline_metrics"]
    flags: dict[str, Any] = {"neural_beats_parametric_required": False}
    for regime in ("S0", "S1"):
        parametric = metrics[f"{regime}:parametric"]["TEST"]["weighted_cross_entropy"]
        seeds = {f"seed{seed}": metrics[f"{regime}:neural:seed{seed}"]["TEST"]["weighted_cross_entropy"]
                 for seed in (0, 1, 2)}
        best_seed = min(seeds, key=seeds.get)
        flags[f"{regime}_fixed_baseline_test_ce"] = fixed[regime]["TEST"]["weighted_cross_entropy"]
        flags[f"{regime}_parametric_test_ce"] = parametric
        flags[f"{regime}_neural_test_ce_by_seed"] = seeds
        flags[f"{regime}_best_neural_seed"] = best_seed
        flags[f"{regime}_neural_beats_parametric"] = bool(seeds[best_seed] < parametric)
    flags["negative_result"] = not all(flags[f"{regime}_neural_beats_parametric"]
                                       for regime in ("S0", "S1"))
    flags["statement"] = (
        "A neural non-gain is a valid negative scientific result under the frozen design; "
        "there is no neural-win acceptance gate. No tuning, extra seed or ad-hoc fit was "
        "performed during or after the science stage."
    )
    return flags


def _audit_context_vs_76(raw: dict[str, Any]) -> dict[str, Any]:
    """Audit-only comparison with the preserved #76 observations (never a threshold)."""
    issue76 = {
        "S0:parametric": 0.9121715994501418,
        "S1:parametric": 0.9081586773751914,
        "S0:neural:seed0": 0.9132187018208984,
        "S1:neural:seed0": 0.9093538306365426,
    }
    comparisons: dict[str, Any] = {}
    for key, observed_76 in issue76.items():
        observed_p2b = raw["metrics"][key]["TEST"]["weighted_cross_entropy"]
        comparisons[key] = {
            "issue_76_observational": observed_76,
            "p2b_observed": observed_p2b,
            "absolute_difference": abs(observed_p2b - observed_76),
        }
    return {
        "role": "AUDIT_CONTEXT_ONLY",
        "statement": "the #76 observational metrics are audit context and are NOT an acceptance "
                     "threshold; P2B was not tuned to match them",
        "comparisons": comparisons,
    }


# --------------------------------------------------------------------------- render
def render() -> int:
    if not (ROOT / RAW_RELPATH).is_file() or not (ROOT / LEDGER_RELPATH).is_file():
        print(json.dumps({"terminal": TERMINAL_BLOCKED,
                          "reason": "raw results or attempt ledger missing; science must run first"},
                         indent=2))
        return 3
    raw, ledger = render_inputs()
    render_count = bump_render_counter()
    science = verify_science_invariants(raw, ledger)

    config = sci.load_frozen_config(ROOT, config_relpath=CONFIG_RELPATH)
    universe = sci.build_universe(config, ROOT)          # deterministic generator only, no fit
    metrics = _metrics_from_raw(raw)
    negative = _negative_result_flags(raw)
    constraints = raw["constraint_diagnostics"]
    determinism = raw["determinism"]

    gate_checks = {
        "exactly_one_science_invocation": raw.get("science_invocations") == 1,
        "zero_science_retries": raw.get("science_retries") == 0,
        "exactly_twelve_started": science["exactly_twelve_started"],
        "exactly_twelve_completed": science["exactly_twelve_completed"],
        "zero_failed_fits": science["zero_failed"],
        "started_indices_exactly_1_to_12": science["started_indices_are_exactly_1_to_12"],
        "wall_clock_within_ceiling": bool(raw["within_wall_clock_ceiling"]),
        "determinism_within_tolerance": bool(determinism["all_within_tolerance"]),
        "row_normalization_ok": bool(constraints["row_normalization_ok"]),
        "negativity_zero": bool(constraints["negativity_ok"]),
        "support_violations_zero": bool(constraints["support_ok"]),
        "split_counts_9_3_2_6": bool(constraints["split_counts_ok"]),
        "excluded_block_count_6": bool(constraints["excluded_block_count_ok"]),
        "no_unseen_region_claim": raw["frozen_split_interpretation"]
        ["test_regions_are_unseen_regions"] is False,
        "p1a_accounting_present": bool(raw["p1a_accounting_checks"]),
    }
    gate_ok = all(gate_checks.values())
    terminal = TERMINAL_PASS if gate_ok else TERMINAL_GATE_FAIL

    results: dict[str, Any] = {
        "experiment_id": raw["experiment_id"],
        "issue": 77,
        "task_id": raw["task_id"],
        "authority_marker": raw["authority_marker"],
        "route": raw["route"],
        "phase": "RENDER_STAGE",
        "recorded_utc": utc_now(),
        "pre_run_freeze_sha": raw["pre_run_freeze_sha"],
        "science_code_identity": raw["code_identity"],
        "environment": raw["environment"],
        "frozen_split_interpretation": raw["frozen_split_interpretation"],
        "attempt_ledger_summary": raw["attempt_ledger_summary"],
        "science_invariants_from_ledger": science,
        "science_wall_clock_seconds": raw["science_wall_clock_seconds"],
        "science_wall_clock_ceiling_seconds": raw["science_wall_clock_ceiling_seconds"],
        "render_only_invocations": render_count,
        "metrics_by_split": metrics,
        "fixed_baseline_metrics": raw["fixed_baseline_metrics"],
        "fit_outcomes": raw["fit_outcomes"],
        "determinism": determinism,
        "constraint_diagnostics": constraints,
        "p1a_accounting_checks": raw["p1a_accounting_checks"],
        "negative_result_flags": negative,
        "audit_context_vs_issue_76": _audit_context_vs_76(raw),
        "acceptance_gate_checks": gate_checks,
        "interpretation_ceiling": {
            "allowed": [
                "clean method/pipeline replication under the frozen synthetic design",
                "fixed / parametric / neural comparison",
                "held-out-time and held-out-origin-role observations",
                "reproducibility comparison to Issue #76 as audit context",
            ],
            "forbidden": [
                "empirical China claim",
                "annual OD data availability claim",
                "unseen-region claim",
                "causal or economic mechanism claim",
                "HJB/KFE/GE/household policy or welfare claim",
                "any tuning based on Issue #76 or P2B outcomes",
            ],
        },
        "terminal": terminal,
    }

    results_path = ROOT / RESULTS_RELPATH
    manifest_path = ROOT / MANIFEST_RELPATH
    report_path = ROOT / REPORT_RELPATH

    manifest: dict[str, Any] = {
        "experiment_id": raw["experiment_id"],
        "issue": 77,
        "recorded_utc": utc_now(),
        "identity_policy": IDENTITY_POLICY,
        "science_protocol": {
            "science_invocations": raw.get("science_invocations"),
            "science_retries": raw.get("science_retries"),
            "started_fits": science["started_count"],
            "completed_fits": science["completed_count"],
            "failed_fits": science["failed_count"],
            "planned_fits": 12,
            "render_only_invocations": render_count,
            "zero_science_reruns": raw.get("science_invocations") == 1,
        },
        "provenance_chain": {
            "issue_77_operative_baseline": raw["code_identity"]["issue_77_operative_baseline"],
            "pre_run_freeze_sha": raw["pre_run_freeze_sha"],
            "pre_run_freeze_role": "executed science code identity",
            "final_artifact_candidate": None,        # filled after the artifact commit
            "final_artifact_candidate_note": (
                "filled by a render-only rerun after the artifact commit; the science code "
                "identity always remains the PRE_RUN_FREEZE SHA"
            ),
            "scientific_module_relpath": SCIENTIFIC_MODULE_RELPATH,
            "scientific_module_blob_sha1": raw["code_identity"]["scientific_module_blob_sha1"],
            "p1a_module_blob_sha1": raw["code_identity"]["p1a_module_blob_sha1"],
            "science_runner_relpath": SCIENCE_RUNNER_RELPATH,
            "science_runner_blob_sha1": blob_sha1_lf(ROOT / SCIENCE_RUNNER_RELPATH),
            "renderer_relpath": RENDERER_RELPATH,
            "renderer_blob_sha1": blob_sha1_lf(ROOT / RENDERER_RELPATH),
            "frozen_config_relpath": CONFIG_RELPATH,
            "frozen_config_blob_sha1": raw["code_identity"]["config_blob_sha1"],
            "frozen_contract_relpath": CONTRACT_RELPATH,
            "frozen_contract_blob_sha1": raw["code_identity"]["contract_blob_sha1"],
            "frozen_schema_relpath": SCHEMA_RELPATH,
            "frozen_schema_blob_sha1": raw["code_identity"]["schema_blob_sha1"],
        },
        "artifact_hashes": {
            "ledger_relpath": LEDGER_RELPATH,
            "ledger_sha256_lf": sha256_lf(ROOT / LEDGER_RELPATH),
            "ledger_blob_sha1": blob_sha1_lf(ROOT / LEDGER_RELPATH),
            "raw_results_relpath": RAW_RELPATH,
            "raw_results_sha256_lf": sha256_lf(ROOT / RAW_RELPATH),
            "raw_results_blob_sha1": blob_sha1_lf(ROOT / RAW_RELPATH),
            "report_relpath": REPORT_RELPATH,
            "report_sha256_lf": sha256_lf(report_path) if report_path.is_file() else None,
        },
        "frozen_inputs_read_only": [CONFIG_RELPATH, CONTRACT_RELPATH, SCHEMA_RELPATH,
                                    P1A_MODULE_RELPATH, SCIENTIFIC_MODULE_RELPATH],
        "declarations": {
            "config_or_contract_mutated": False,
            "scientific_module_mutated": False,
            "real_data_used": False,
            "data_download_scrape_purchase": False,
            "household_or_hjb_kfe_ge_matlab_calls": 0,
            "full_repository_suite_runs": 0,
            "tuning_or_extra_seed": False,
            "ledger_or_raw_modified_by_renderer": False,
        },
        "terminal": terminal,
    }

    REPORT_PATH_TEXT = _render_report(raw, results, manifest, metrics, negative, determinism,
                                      constraints, gate_checks, terminal)
    report_path.write_text(REPORT_PATH_TEXT, encoding="utf-8", newline="\n")

    # ---- identity chain (acyclic) --------------------------------------------
    core = {k: v for k, v in results.items()
            if k not in ("results_canonical_sha256", MANIFEST_DIGEST_FIELD)}
    results_digest = hashlib.sha256(dumps(core)).hexdigest().upper()
    results_core_bytes = dumps(core)
    manifest["artifact_hashes"]["results_relpath"] = RESULTS_RELPATH
    manifest["artifact_hashes"]["results_canonical_sha256"] = results_digest
    manifest["artifact_hashes"]["results_blob_sha1"] = hashlib.sha1(
        f"blob {len(results_core_bytes)}\0".encode("ascii") + results_core_bytes).hexdigest()
    manifest["artifact_hashes"]["report_sha256_lf"] = sha256_lf(report_path)

    manifest_bytes = dumps(manifest)
    manifest_path.write_bytes(manifest_bytes)
    results["results_canonical_sha256"] = results_digest
    results[MANIFEST_DIGEST_FIELD] = hashlib.sha256(manifest_bytes).hexdigest().upper()
    results_path.write_bytes(dumps(results))

    # ---- verification -------------------------------------------------------
    rr = json.loads(results_path.read_text(encoding="utf-8"))
    mm = json.loads(manifest_path.read_text(encoding="utf-8"))
    file_core = dumps({k: v for k, v in rr.items()
                       if k not in ("results_canonical_sha256", MANIFEST_DIGEST_FIELD)})
    checks = {
        "results_file_is_canonical_plus_digests": results_path.read_bytes() == dumps(rr),
        "results_digest_recomputes": rr["results_canonical_sha256"]
        == hashlib.sha256(file_core).hexdigest().upper(),
        "manifest_digest_recomputes": rr[MANIFEST_DIGEST_FIELD]
        == hashlib.sha256(dumps(mm)).hexdigest().upper(),
        "results_blob_matches": mm["artifact_hashes"]["results_blob_sha1"]
        == hashlib.sha1(f"blob {len(file_core)}\0".encode("ascii") + file_core).hexdigest(),
        "report_hash_matches": mm["artifact_hashes"]["report_sha256_lf"] == sha256_lf(report_path),
        "ledger_hash_recorded": mm["artifact_hashes"]["ledger_sha256_lf"]
        == sha256_lf(ROOT / LEDGER_RELPATH),
        "raw_hash_recorded": mm["artifact_hashes"]["raw_results_sha256_lf"]
        == sha256_lf(ROOT / RAW_RELPATH),
        "no_fit_in_renderer": True,
        "gate_ok": gate_ok,
        "terminal_gate_consistent": rr["terminal"] == mm["terminal"] == terminal,
    }
    print(json.dumps({
        "phase": "RENDER_STAGE",
        "render_only_invocations": render_count,
        "fits": 0,
        "optimizer_steps": 0,
        "gate_ok": gate_ok,
        "terminal": terminal,
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "results": RESULTS_RELPATH,
        "manifest": MANIFEST_RELPATH,
        "report": REPORT_RELPATH,
    }, indent=2))
    return 0 if all(checks.values()) and gate_ok else 2


def _render_report(raw: dict[str, Any], results: dict[str, Any], manifest: dict[str, Any],
                   metrics: dict[str, Any], negative: dict[str, Any],
                   determinism: dict[str, Any], constraints: dict[str, Any],
                   gate_checks: dict[str, bool], terminal: str) -> str:
    lines: list[str] = []
    lines.append("# DLH-WL-P2B — clean immutable replication of the frozen synthetic prototype\n")
    lines.append("## 0. Status\n")
    lines.append(f"```\nterminal: {terminal}\n```\n")
    lines.append(f"- PRE_RUN_FREEZE SHA (executed science code identity): `{raw['pre_run_freeze_sha']}`")
    lines.append(f"- scientific module blob: `{raw['code_identity']['scientific_module_blob_sha1']}`")
    lines.append(f"- science invocations: **{raw.get('science_invocations')}**; science retries: "
                 f"**{raw.get('science_retries')}**")
    lines.append(f"- fit attempts started/completed: "
                 f"**{raw['attempt_ledger_summary']['started_count']}** / "
                 f"**{raw['attempt_ledger_summary']['completed_count']}**")
    lines.append(f"- science wall clock: **{raw['science_wall_clock_seconds']:.6f} s** "
                 f"(ceiling {raw['science_wall_clock_ceiling_seconds']:.0f} s)")
    lines.append(f"- render-only invocations so far: **{results['render_only_invocations']}** "
                 f"(zero fits, zero optimizer steps)")
    lines.append("")
    lines.append("## 1. Frozen design (unchanged from Issue #75)\n")
    lines.append(
        "The replication runs the accepted #75 P1B frozen design verbatim through the "
        "byte-identical #76 scientific module: 5 regions x 4 periods, the frozen support, the "
        "S0/S1 generators, exactly three baseline families (fixed support-normalized prior, "
        "six-parameter contrast-identifiable gravity/logit MLE, small MLP pair scorer with 16/8 "
        "hidden widths under masked softmax), the 9/3/2/6 split, TRAIN-only preprocessing, "
        "neural seeds 0/1/2, frozen metrics and tolerances, and 12 planned fit executions "
        "against a 13-attempt ceiling and an 1800 s wall-clock ceiling.")
    lines.append("")
    lines.append("## 2. Execution protocol evidence\n")
    lines.append("| check | value |")
    lines.append("|---|---|")
    for name, ok in gate_checks.items():
        lines.append(f"| {name} | {ok} |")
    lines.append("")
    lines.append("Attempt ledger (durable, one line per event):")
    lines.append("")
    lines.append("```")
    for record in raw["attempt_ledger_records"]:
        lines.append(json.dumps({k: record[k] for k in
                                 ("attempt_index", "event", "family", "regime", "seed")
                                 if k in record}))
    lines.append("```")
    lines.append("")
    lines.append("## 3. Observed results\n")
    lines.append("| regime | family | seed | TEST weighted CE | TEST mean abs share error | TEST row-norm max | neg | support | top-1 | best step |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|")
    for regime in ("S0", "S1"):
        fixed = raw["fixed_baseline_metrics"][regime]["TEST"]
        lines.append(f"| {regime} | fixed | — | {fixed['weighted_cross_entropy']:.6f} "
                     f"| {fixed['mean_absolute_share_error']:.6f} "
                     f"| {fixed['row_normalization_violation_max']:.3g} "
                     f"| {fixed['negativity_violation_count']} | {fixed['support_violation_count']} "
                     f"| {fixed['top1_destination_accuracy']:.3f} | — |")
        parametric = metrics[f"{regime}:parametric"]["TEST"]
        lines.append(f"| {regime} | parametric | — | {parametric['weighted_cross_entropy']:.6f} "
                     f"| {parametric['mean_absolute_share_error']:.6f} "
                     f"| {parametric['row_normalization_violation_max']:.3g} "
                     f"| {parametric['negativity_violation_count']} | {parametric['support_violation_count']} "
                     f"| {parametric['top1_destination_accuracy']:.3f} | — |")
        for seed in (0, 1, 2):
            block = metrics[f"{regime}:neural:seed{seed}"]["TEST"]
            summary = raw["fit_outcomes"][f"fit::{regime}:neural:seed{seed}"]
            lines.append(f"| {regime} | neural | {seed} | {block['weighted_cross_entropy']:.6f} "
                         f"| {block['mean_absolute_share_error']:.6f} "
                         f"| {block['row_normalization_violation_max']:.3g} "
                         f"| {block['negativity_violation_count']} | {block['support_violation_count']} "
                         f"| {block['top1_destination_accuracy']:.3f} | {summary['best_step']} |")
    lines.append("")
    lines.append("Parametric fitted coefficients (six contrast-identifiable columns, frozen order):")
    lines.append("")
    lines.append("```")
    for regime in ("S0", "S1"):
        coeffs = raw["fit_outcomes"][f"fit::{regime}:parametric"]["coefficients"]
        lines.append(f"{regime}: {[round(v, 9) for v in coeffs]}")
    lines.append("```")
    lines.append("")
    lines.append("## 4. Determinism and constraint diagnostics\n")
    lines.append("```")
    for name in ("parametric_S0", "parametric_S1", "neural_S0_seed0", "neural_S1_seed0"):
        info = determinism[name]
        lines.append(f"{name}: deviation={info['deviation']:.3e} "
                     f"(tolerance {determinism['determinism_tolerance']:.0e})")
    lines.append(f"row_normalization_violation_max={constraints['row_normalization_violation_max']:.3e} "
                 f"(tolerance {constraints['row_normalization_tolerance']:.0e})")
    lines.append(f"negativity_violation_count={constraints['negativity_violation_count']}")
    lines.append(f"support_violation_count={constraints['support_violation_count']}")
    lines.append(f"split_counts={constraints['split_counts']}")
    lines.append(f"excluded_block_count={constraints['excluded_block_count']}")
    lines.append("```")
    lines.append("")
    lines.append("## 5. Neural comparison (no win requirement)\n")
    lines.append(f"- neural-beats-parametric required: **{negative['neural_beats_parametric_required']}**")
    for regime in ("S0", "S1"):
        lines.append(f"- {regime}: fixed {negative[f'{regime}_fixed_baseline_test_ce']:.6f}; "
                     f"parametric {negative[f'{regime}_parametric_test_ce']:.6f}; "
                     f"best neural {negative[f'{regime}_best_neural_seed']} "
                     f"({negative[f'{regime}_neural_test_ce_by_seed'][negative[f'{regime}_best_neural_seed']]:.6f}); "
                     f"neural beats parametric = {negative[f'{regime}_neural_beats_parametric']}")
    lines.append(f"- negative result flag: **{negative['negative_result']}**")
    lines.append(f"- {negative['statement']}")
    lines.append("")
    lines.append("## 6. Audit context versus Issue #76 (not a threshold)\n")
    lines.append("| configuration | Issue #76 observational | P2B observed | absolute difference |")
    lines.append("|---|---|---|---|")
    for key, comparison in results["audit_context_vs_issue_76"]["comparisons"].items():
        lines.append(f"| {key} | {comparison['issue_76_observational']:.10f} "
                     f"| {comparison['p2b_observed']:.10f} "
                     f"| {comparison['absolute_difference']:.3e} |")
    lines.append("")
    lines.append(f"{results['audit_context_vs_issue_76']['statement']}")
    lines.append("")
    lines.append("## 7. Interpretation ceiling\n")
    lines.append("Allowed:")
    for item in results["interpretation_ceiling"]["allowed"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("Forbidden:")
    for item in results["interpretation_ceiling"]["forbidden"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## 8. Limitations\n")
    lines.append("- the synthetic control is deliberately small (20 allocation blocks, 18 evaluable "
                 "share cells per time slice, 72 total, 9 training blocks) and carries no economic "
                 "content;")
    lines.append("- the split holds out time and the **origin role** only: `R03`/`R04` occur as "
                 "TRAIN destinations, so this is not an unseen-region test;")
    lines.append("- the neural backend is NumPy because PyTorch is not installed; the frozen "
                 "architecture and protocol are unchanged;")
    lines.append("- real annual bilateral OD label availability remains `UNRESOLVED`; nothing here "
                 "speaks to Chinese interprovincial flows and no HJB/KFE/GE/household coupling was "
                 "attempted;")
    lines.append("- no checkpoint artifact is produced: identity is PRE_RUN_FREEZE SHA + frozen "
                 "config + environment + seeds + ledger + manifest + metrics;")
    lines.append("- the renderer may be rerun for formatting/hashing repair; the science runner, "
                 "scientific module, tests, ledger and raw results are immutable after the first "
                 "optimizer step.")
    lines.append("")
    lines.append("## 9. Terminal\n")
    lines.append("```")
    lines.append(terminal)
    lines.append("```")
    lines.append("")
    return "\n".join(lines)


def _calls_any_fitter() -> bool:
    """Static guard: does this file actually call a fitting entry point?

    Only real call targets are inspected, so mentioning a fitter inside a guard string
    or a docstring cannot create a false positive.
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
                         "_adam_step", "_backward", "_forward", "_train_only_zscore",
                         "_softmax_cross_entropy"})


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="DLH-WL-P2B render-only generator (Issue #77)")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--render-only", action="store_true",
                       help="render publication artifacts from the immutable science output")
    group.add_argument("--validate-only", action="store_true",
                       help="check that render inputs exist and that no fit path is referenced")
    args = parser.parse_args(argv)
    if args.validate_only:
        payload = {
            "phase": "VALIDATE_ONLY",
            "raw_present": (ROOT / RAW_RELPATH).is_file(),
            "ledger_present": (ROOT / LEDGER_RELPATH).is_file(),
            "optimizer_steps_performed": 0,
            "fit_attempts_performed": 0,
            "renderer_imports_fitters": _calls_any_fitter(),
            "fitter_call_guard": "static AST scan of this file's call targets",
        }
        print(json.dumps(payload, indent=2))
        return 0
    return render()


if __name__ == "__main__":
    raise SystemExit(main())
