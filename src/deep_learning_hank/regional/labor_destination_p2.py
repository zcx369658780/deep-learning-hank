"""DLH-WL-P2A — frozen offline synthetic prototype harness (Issue #76).

Method-only implementation of the design frozen by Issue #75 / P1B:

- ``docs/specifications/DLH_WL_P2_OFFLINE_PROTOTYPE_CONTRACT_2026_09_18.md``
- ``configs/dlh_wl_p2_offline_prototype.toml`` (configuration revision 4)
- accepted P1A accounting interface: ``deep_learning_hank.regional.labor_destination``

Scope ceiling (binding, from the frozen contract and the Issue #76 body):

- offline synthetic method validation only; **no real data**, no download, no HJB,
  no KFE, no GE, no MATLAB, no household coupling, no selected-Q work;
- no hyper-parameter, architecture or seed search; every value below is read from
  the frozen TOML, never chosen here;
- the neural score mapping is implemented in NumPy because the environment provides
  SciPy (used for the parametric fit) but not PyTorch; the frozen design is a plain
  MLP plus Adam, so this is an implementation substitution, not a design change;
- interpretation ceiling: pipeline/method statements, held-out-time and
  held-out-origin-role observations only. No empirical China claim, no OD data
  availability claim, no unseen-region claim, no causal or welfare claim.
"""

from __future__ import annotations

import math
import random
import time
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterable, Sequence

import numpy as np

__all__ = [
    "P2Config",
    "SyntheticUniverse",
    "Block",
    "FitOutcome",
    "load_frozen_config",
    "build_universe",
    "fixed_baseline_predictions",
    "fit_parametric",
    "fit_neural",
    "evaluate_predictions",
    "validate_only_report",
    "run_scientific_program",
    "TERMINAL_PASS",
    "TERMINAL_GATE_FAIL",
    "TERMINAL_BLOCKED",
]

TERMINAL_PASS = "DLH_WL_P2A_OFFLINE_SYNTHETIC_PROTOTYPE__PASS__RESULT_INTERPRETABLE"
TERMINAL_GATE_FAIL = "DLH_WL_P2A_OFFLINE_SYNTHETIC_PROTOTYPE__GATE_FAIL__NO_TUNING_AUTHORIZED"
TERMINAL_BLOCKED = "BLOCKED_DLH_WL_P2A_IMPLEMENTATION_ENVIRONMENT_OR_BUDGET"


# --------------------------------------------------------------------------- config
@dataclass(frozen=True)
class P2Config:
    """Frozen configuration values read verbatim from the Issue #75 TOML."""

    path: str
    git_blob: str
    sha256: str
    config_revision: int
    activation_comment: int
    operative_baseline: str
    region_ids: tuple[str, ...]
    time_ids: tuple[int, ...]
    blocked_pairs: tuple[tuple[int, int], ...]
    gdp_intercept: float
    gdp_region_step: float
    gdp_time_step: float
    wage_intercept: float
    wage_region_step: float
    wage_time_step: float
    urbanization_base: float
    urbanization_region_step: float
    urbanization_time_step: float
    w_ij_by_destination: tuple[float, ...]
    ell_base_vector: tuple[float, ...]
    ell_time_growth: float
    m_base_vector: tuple[float, ...]
    m_time_step: float
    m_region_offset: tuple[float, ...]
    fitted_columns: tuple[str, ...]
    pair_features: tuple[str, ...]
    node_features: tuple[str, ...]
    time_features: tuple[str, ...]
    static_features: tuple[str, ...]
    zscored_features: tuple[str, ...]
    raw_features: tuple[str, ...]
    s0_coefficients: dict[str, float]
    beta_sq: float
    beta_relu: float
    d_star: float
    hidden_widths: tuple[int, ...]
    activations: tuple[str, ...]
    learning_rate: float
    max_steps: int
    eval_every: int
    early_stop_patience: int
    early_stop_min_delta: float
    neural_seeds: tuple[int, ...]
    determinism_configs: tuple[str, ...]
    split_times: dict[str, tuple[int, ...]]
    split_origins: dict[str, tuple[str, ...]]
    split_counts: dict[str, int]
    row_normalization_tolerance: float
    determinism_tolerance: float
    excluded_block_count_expected: int
    wall_clock_seconds_max: float
    primary_fit_configurations: int
    planned_fit_executions: int
    absolute_attempt_ceiling: int
    max_engineering_retries: int
    contract_path: str
    schema_path: str
    p1a_interface_path: str


def load_frozen_config(
    repo_root: str | Path,
    *,
    config_relpath: str = "configs/dlh_wl_p2_offline_prototype.toml",
    git_blob: str = "",
) -> P2Config:
    """Parse the frozen TOML with stdlib ``tomllib`` and validate its identity."""
    import hashlib

    root = Path(repo_root)
    path = root / config_relpath
    raw = path.read_bytes()
    data = tomllib.loads(raw.decode("utf-8"))
    auth = data["authority"]
    if auth.get("config_revision") != 4:
        raise ValueError(f"unexpected frozen config revision {auth.get('config_revision')!r}")
    return P2Config(
        path=config_relpath,
        git_blob=git_blob,
        sha256=hashlib.sha256(raw).hexdigest().upper(),
        config_revision=int(auth["config_revision"]),
        activation_comment=int(auth["activation_comment"]),
        operative_baseline=str(auth["operative_baseline"]),
        region_ids=tuple(data["universe"]["region_ids"]),
        time_ids=tuple(int(t) for t in data["universe"]["time_ids"]),
        blocked_pairs=tuple((int(a), int(b)) for a, b in data["support"]["blocked_pairs"]),
        gdp_intercept=float(data["inputs"]["gdp_intercept"]),
        gdp_region_step=float(data["inputs"]["gdp_region_step"]),
        gdp_time_step=float(data["inputs"]["gdp_time_step"]),
        wage_intercept=float(data["inputs"]["wage_intercept"]),
        wage_region_step=float(data["inputs"]["wage_region_step"]),
        wage_time_step=float(data["inputs"]["wage_time_step"]),
        urbanization_base=float(data["inputs"]["urbanization_base"]),
        urbanization_region_step=float(data["inputs"]["urbanization_region_step"]),
        urbanization_time_step=float(data["inputs"]["urbanization_time_step"]),
        w_ij_by_destination=tuple(float(v) for v in data["inputs"]["w_ij_by_destination"]),
        ell_base_vector=tuple(float(v) for v in data["inputs"]["ell_base_vector"]),
        ell_time_growth=float(data["inputs"]["ell_time_growth"]),
        m_base_vector=tuple(float(v) for v in data["inputs"]["m_base_vector"]),
        m_time_step=float(data["inputs"]["m_time_step"]),
        m_region_offset=tuple(float(v) for v in data["inputs"]["m_region_offset"]),
        fitted_columns=tuple(data["features"]["parametric_fitted_vocabulary"]),
        pair_features=tuple(data["features"]["pair_features"]),
        node_features=tuple(data["features"]["node_features"]),
        time_features=tuple(data["features"]["time_features"]),
        static_features=tuple(data["features"]["static_features"]),
        zscored_features=tuple(data["features"]["zscored_features"]),
        raw_features=tuple(data["features"]["raw_features"]),
        s0_coefficients={k: float(v) for k, v in data["regime_s0"]["s0_coefficients"].items()},
        beta_sq=float(data["regime_s1"]["beta_sq"]),
        beta_relu=float(data["regime_s1"]["beta_relu"]),
        d_star=float(data["regime_s1"]["d_star"]),
        hidden_widths=tuple(int(w) for w in data["architecture_neural"]["hidden_widths"]),
        activations=tuple(data["architecture_neural"]["activations"]),
        learning_rate=float(data["train_protocol"]["learning_rate"]),
        max_steps=int(data["train_protocol"]["max_steps"]),
        eval_every=int(data["train_protocol"]["eval_every"]),
        early_stop_patience=int(data["train_protocol"]["early_stop_patience"]),
        early_stop_min_delta=float(data["train_protocol"]["early_stop_min_delta"]),
        neural_seeds=tuple(int(s) for s in data["train_protocol"]["neural_seeds"]),
        determinism_configs=tuple(data["train_protocol"]["determinism_verification_configs"]),
        split_times={
            "TRAIN": tuple(int(t) for t in data["split"]["train"]["times"]),
            "VALIDATION": tuple(int(t) for t in data["split"]["validation"]["times"]),
            "TEST": tuple(int(t) for t in data["split"]["test"]["times"]),
            "EXCLUDED_REFERENCE_ONLY": tuple(int(t) for t in data["split"]["excluded_reference_only"]["times"]),
        },
        split_origins={
            "TRAIN": tuple(data["split"]["train"]["origins"]),
            "VALIDATION": tuple(data["split"]["validation"]["origins"]),
            "TEST": tuple(data["split"]["test"]["origins"]),
            "EXCLUDED_REFERENCE_ONLY": tuple(data["split"]["excluded_reference_only"]["origins"]),
        },
        split_counts={k: int(v) for k, v in data["split"]["split_counts"].items()},
        row_normalization_tolerance=float(data["metrics"]["row_normalization_tolerance"]),
        determinism_tolerance=float(data["metrics"]["determinism_tolerance"]),
        excluded_block_count_expected=int(data["metrics"]["excluded_block_count_expected"]),
        wall_clock_seconds_max=float(data["budget"]["wall_clock_seconds_max"]),
        primary_fit_configurations=int(data["budget"]["primary_fit_configurations"]),
        planned_fit_executions=int(data["budget"]["planned_fit_executions"]),
        absolute_attempt_ceiling=int(data["budget"]["absolute_attempt_ceiling"]),
        max_engineering_retries=int(data["budget"]["max_engineering_retries"]),
        contract_path=str(auth["prototype_contract_path"]),
        schema_path=str(auth["label_schema_path"]),
        p1a_interface_path=str(auth["p1a_interface_path"]),
    )


# --------------------------------------------------------------------------- blocks
@dataclass(frozen=True)
class Block:
    """One allocation block: key ``(time_index, origin)`` with its allowed targets."""

    time_index: int
    time_id: int
    origin: int
    origin_id: str
    allowed: tuple[int, ...]
    split: str

    @property
    def key(self) -> tuple[int, int]:
        return (self.time_index, self.origin)


@dataclass
class SyntheticUniverse:
    """Deterministic synthetic universe with S0/S1 targets and frozen features."""

    config: P2Config
    gdp: np.ndarray            # (T, R)
    wage: np.ndarray           # (T, R)
    access: np.ndarray         # (T, R)
    urbanization: np.ndarray   # (T, R)
    m: np.ndarray              # (T, R)
    ell: np.ndarray            # (T, R)
    support: np.ndarray        # (R, R) bool
    blocks: tuple[Block, ...]
    targets: dict[str, np.ndarray]        # regime -> (T, R, R) shares
    design_rows: dict[str, list[list[float]]]
    design_meta: list[tuple[int, int, int]]
    pair_values: np.ndarray
    node_origin_values: np.ndarray
    node_dest_values: np.ndarray
    time_values: np.ndarray
    static_values: np.ndarray
    raw_design: np.ndarray
    dist: np.ndarray
    w_ij: np.ndarray
    p1a_diagnostics: dict[str, Any] = field(default_factory=dict)

    # -- convenience -------------------------------------------------------
    @property
    def design_matrix(self) -> np.ndarray:
        """Model input matrix; z-scored features use TRAIN-only statistics."""
        if getattr(self, "_design_matrix", None) is None:
            self._design_matrix = self.raw_design
        return self._design_matrix

    @design_matrix.setter
    def design_matrix(self, value: np.ndarray) -> None:
        self._design_matrix = value

    def row(self, t: int, i: int, j: int) -> int:
        return self.design_meta.index((t, i, j))
    def blocks_for(self, split: str) -> list[Block]:
        return [b for b in self.blocks if b.split == split]

    def design_indices(self, blocks: Iterable[Block]) -> np.ndarray:
        wanted: set[tuple[int, int, int]] = set()
        for b in blocks:
            for j in b.allowed:
                wanted.add((b.time_index, b.origin, j))
        return np.array([i for i, meta in enumerate(self.design_meta) if meta in wanted], dtype=int)

    def features(self) -> np.ndarray:
        return self.raw_design

    def split_assignments(self) -> dict[tuple[int, int, int], str]:
        mapping: dict[tuple[int, int, int], str] = {}
        for b in self.blocks:
            for j in b.allowed:
                mapping[(b.time_index, b.origin, j)] = b.split
        return mapping


def _logit_terms(cfg: P2Config, gdp: np.ndarray, wage: np.ndarray, access: np.ndarray,
                 dist: np.ndarray, w_ij: np.ndarray, t: int, i: int, j: int,
                 target: np.ndarray, allowed: Sequence[int]) -> tuple[float, float]:
    """S1 nonlinear terms, within-block centred over the allowed destinations."""
    ld = math.log1p(dist[i, j])
    ld_bar = sum(math.log1p(dist[i, k]) for k in allowed) / len(allowed)
    g_bar = sum(math.log(gdp[t, k]) for k in allowed) / len(allowed)
    x2 = (ld - ld_bar) ** 2
    x3 = max(0.0, dist[i, j] - cfg.d_star) * (math.log(gdp[t, j]) - g_bar)
    return x2, x3


def build_universe(config: P2Config, repo_root: str | Path) -> SyntheticUniverse:
    """Construct all 20 blocks, the frozen support and the S0/S1 targets."""
    root = Path(repo_root)
    ids = config.region_ids
    R = len(ids)
    T = len(config.time_ids)

    gdp = np.array([[config.gdp_intercept + config.gdp_region_step * i + config.gdp_time_step * t
                     for i in range(R)] for t in range(T)], dtype=float)
    wage = np.array([[config.wage_intercept + config.wage_region_step * i + config.wage_time_step * t
                      for i in range(R)] for t in range(T)], dtype=float)
    urb = np.array([[config.urbanization_base + config.urbanization_region_step * i
                     + config.urbanization_time_step * t for i in range(R)] for t in range(T)], dtype=float)
    dist = np.array([[abs(i - j) for j in range(R)] for i in range(R)], dtype=float)
    w_ij = np.array([[config.w_ij_by_destination[j] for j in range(R)] for _ in range(R)], dtype=float)
    access = np.array([[sum(gdp[t, k] / (1.0 + dist[i, k]) for k in range(R)) for i in range(R)]
                       for t in range(T)], dtype=float)
    m = np.array([[config.m_base_vector[i] + config.m_time_step * t + config.m_region_offset[i]
                   for i in range(R)] for t in range(T)], dtype=float)
    ell = np.array([[config.ell_base_vector[i] * (1.0 + config.ell_time_growth * t)
                     for i in range(R)] for t in range(T)], dtype=float)

    support = np.ones((R, R), dtype=bool)
    np.fill_diagonal(support, False)
    for i, j in config.blocked_pairs:
        support[i, j] = False

    blocks: list[Block] = []
    for t in range(T):
        for i in range(R):
            origin_id = ids[i]
            split = next(state for state in ("TRAIN", "VALIDATION", "TEST", "EXCLUDED_REFERENCE_ONLY")
                         if config.time_ids[t] in config.split_times[state]
                         and origin_id in config.split_origins[state])
            allowed = tuple(j for j in range(R) if support[i, j])
            blocks.append(Block(t, config.time_ids[t], i, origin_id, allowed, split))
    blocks_t = tuple(blocks)

    targets: dict[str, np.ndarray] = {"S0": np.zeros((T, R, R)), "S1": np.zeros((T, R, R))}
    for b in blocks_t:
        for regime in ("S0", "S1"):
            logits = []
            for j in b.allowed:
                score = sum(config.s0_coefficients[c] * value for c, value in (
                    ("log_gdp_dest", math.log(gdp[b.time_index, j])),
                    ("log_wage_gap", math.log(wage[b.time_index, j]) - math.log(wage[b.time_index, b.origin])),
                    ("log_adj_distance", math.log1p(dist[b.origin, j])),
                    ("adjacency", 1.0 if dist[b.origin, j] == 1.0 else 0.0),
                    ("log_accessibility_dest", math.log(access[b.time_index, j])),
                    ("w_ij", w_ij[b.origin, j]),
                ))
                if regime == "S1":
                    x2, x3 = _logit_terms(config, gdp, wage, access, dist, w_ij,
                                          b.time_index, b.origin, j, targets["S0"], b.allowed)
                    score += config.beta_sq * x2 + config.beta_relu * x3
                logits.append(score)
            arr = np.array(logits)
            exp = np.exp(arr - arr.max())
            shares = exp / exp.sum()
            for pos, j in enumerate(b.allowed):
                targets[regime][b.time_index, b.origin, j] = shares[pos]

    # ---- features (frozen order) ----------------------------------------
    design_meta: list[tuple[int, int, int]] = []
    pair_rows: list[list[float]] = []
    node_i_rows: list[list[float]] = []
    node_j_rows: list[list[float]] = []
    time_rows: list[list[float]] = []
    static_rows: list[list[float]] = []
    for b in blocks_t:
        for j in b.allowed:
            t, i = b.time_index, b.origin
            pair_rows.append([
                math.log(gdp[t, j]),
                math.log(wage[t, j]) - math.log(wage[t, i]),
                math.log1p(dist[i, j]),
                1.0 if dist[i, j] == 1.0 else 0.0,
                math.log(access[t, j]),
            ])
            node_i_rows.append([math.log(gdp[t, i]), math.log(wage[t, i]), math.log(access[t, i]), urb[t, i]])
            node_j_rows.append([math.log(gdp[t, j]), math.log(wage[t, j]), math.log(access[t, j]), urb[t, j]])
            time_rows.append([t / (T - 1)])
            static_rows.append([w_ij[i, j]])
            design_meta.append((t, i, j))

    pair_values = np.array(pair_rows)
    node_origin_values = np.array(node_i_rows)
    node_dest_values = np.array(node_j_rows)
    time_values = np.array(time_rows)
    static_values = np.array(static_rows)
    raw_design = np.hstack([pair_values, node_origin_values, node_dest_values, time_values, static_values])

    design_rows = {
        "S0": [row[:] for row in pair_values[:, [0, 1, 2, 3, 4]]],
        "S1": [row[:] for row in pair_values[:, [0, 1, 2, 3, 4]]],
    }

    universe = SyntheticUniverse(
        config=config, gdp=gdp, wage=wage, access=access, urbanization=urb, m=m, ell=ell,
        support=support, blocks=blocks_t, targets=targets, design_rows=design_rows,
        design_meta=design_meta, pair_values=pair_values, node_origin_values=node_origin_values,
        node_dest_values=node_dest_values, time_values=time_values, static_values=static_values,
        raw_design=raw_design, dist=dist, w_ij=w_ij,
    )
    universe._design_matrix = None
    universe.p1a_diagnostics = _p1a_accounting_check(universe, root)
    return universe


def _p1a_accounting_check(universe: SyntheticUniverse, root: Path) -> dict[str, Any]:
    """Validate W/P/F invariants through the accepted P1A interface (read-only)."""
    import sys

    src = str(root / "src")
    if src not in sys.path:
        sys.path.insert(0, src)
    from deep_learning_hank.regional.labor_destination import (  # noqa: WPS433 (local import by design)
        build_labor_destination_accounting,
    )

    out: dict[str, Any] = {}
    for regime in ("S0", "S1"):
        per_time = []
        for t in range(len(universe.config.time_ids)):
            result = build_labor_destination_accounting(
                m=universe.m[t],
                ell=universe.ell[t],
                W=universe.targets[regime][t],
                support_mask=universe.support,
            )
            per_time.append({
                "time_id": universe.config.time_ids[t],
                "origin_conservation_max_abs_deviation": result.diagnostics["origin_conservation_max_abs_deviation"],
                "national_conservation_max_abs_deviation": result.diagnostics["national_conservation_max_abs_deviation"],
                "destination_aggregation_max_abs_deviation": result.diagnostics["destination_aggregation_max_abs_deviation"],
                "active_row_count": result.diagnostics["active_row_count"],
                "valid_row_count": result.diagnostics["valid_row_count"],
                "identifiable_rows": int((~result.rows_without_identifiable_target).sum()),
                "conditional_choice_identified": result.conditional_choice_identified,
                "total_labor": result.total_labor,
            })
        out[regime] = per_time
    return out


# --------------------------------------------------------------------------- helpers
def _fitted_matrix(universe: SyntheticUniverse) -> np.ndarray:
    """The six fitted contrast-identifiable columns, in frozen vocabulary order."""
    cfg = universe.config
    cols = []
    for name in cfg.fitted_columns:
        if name in cfg.pair_features:
            cols.append(universe.pair_values[:, cfg.pair_features.index(name)])
        elif name == "w_ij":
            cols.append(universe.static_values[:, 0])
        else:  # pragma: no cover - guarded by config validation
            raise ValueError(f"unknown fitted column {name!r}")
    return np.column_stack(cols)


def _nonlinear_columns(universe: SyntheticUniverse) -> np.ndarray:
    """X2/X3 terms, within-block centred, aligned with ``design_meta`` rows."""
    cfg = universe.config
    out = np.zeros((len(universe.design_meta), 2))
    base_w = np.zeros_like(universe.w_ij)
    for idx, (t, i, j) in enumerate(universe.design_meta):
        b = universe.blocks[t * len(cfg.region_ids) + i]
        out[idx] = _logit_terms(cfg, universe.gdp, universe.wage, universe.access,
                                universe.dist, base_w, t, i, j, universe.targets["S0"], b.allowed)
    return out


def _block_weight_matrix(universe: SyntheticUniverse) -> dict[tuple[int, int], float]:
    return {b.key: float(universe.ell[b.time_index, b.origin]) for b in universe.blocks}


def _stack(universe: SyntheticUniverse, blocks: Sequence[Block], regime: str,
           X: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Stack the allowed cells of ``blocks`` into the frozen masked-softmax layout.

    Returns ``(X_rows, Y_rows, block_weights, block_mask, cell_index)`` where every
    row is one allowed destination cell (so ``X_rows`` is compact), ``block_mask``
    is the ``(n_blocks, R)`` allowed-destination mask and ``cell_index`` maps each
    stacked cell back to its block. ``Y_rows`` is compact too; the frozen softmax
    for each block is evaluated on the full ``R``-wide mask and then restricted to
    the allowed cells.
    """
    R = len(universe.config.region_ids)
    xs, ys, ws, masks, index = [], [], [], [], []
    for bidx, b in enumerate(blocks):
        row_mask = np.zeros(R, dtype=bool)
        for j in b.allowed:
            row_mask[j] = True
        for j in b.allowed:
            xs.append(X[universe.row(b.time_index, b.origin, j)])
            ys.append(universe.targets[regime][b.time_index, b.origin, j])
            index.append(bidx)
        ws.append(universe.ell[b.time_index, b.origin])
        masks.append(row_mask)
    return (np.array(xs), np.array(ys), np.array(ws), np.array(masks),
            np.array(index, dtype=int))


def _masked_softmax(scores: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """Masked softmax over one block; returns a vector (no scalar coercion)."""
    masked = np.where(mask, scores, -np.inf)
    mx = np.max(masked)
    exp = np.where(mask, np.exp(masked - mx), 0.0)
    total = exp.sum()
    if not np.isfinite(total) or total <= 0.0:
        raise FloatingPointError("masked softmax produced a non-positive normalizer")
    return exp / total


def _softmax_cross_entropy(scores: np.ndarray, target: np.ndarray, weights: np.ndarray,
                           mask: np.ndarray, cell_index: np.ndarray) -> tuple[float, np.ndarray]:
    """Weighted cross entropy over the frozen masked per-block softmax.

    ``scores``/``target`` are the compact per-cell vectors; ``mask`` is the
    ``(n_blocks, R)`` allowed-destination mask and ``cell_index`` maps each cell to
    its block. Each block's softmax is evaluated over its full ``R``-wide mask and
    then restricted to the allowed cells, so the normalization is always within one
    block and never across blocks. ``weights`` holds one weight per block.
    """
    scores = np.asarray(scores, dtype=float).reshape(-1)
    target = np.asarray(target, dtype=float).reshape(-1)
    cell_index = np.asarray(cell_index).reshape(-1)
    mask = np.asarray(mask)
    if scores.shape != target.shape or scores.shape[0] != cell_index.shape[0]:
        raise ValueError("inconsistent stacked loss inputs")

    probs = np.zeros(scores.shape[0], dtype=float)
    for b in range(mask.shape[0]):
        rows = np.flatnonzero(cell_index == b)
        block_scores = np.zeros(mask.shape[1], dtype=float)
        block_scores[mask[b]] = scores[rows]
        block_prob = _masked_softmax(block_scores, mask[b])
        probs[rows] = block_prob[mask[b]]
    safe = np.maximum(probs, 1e-300)
    w_cell = np.asarray(weights, dtype=float).reshape(-1)[cell_index]
    loss = float(-(w_cell * target * np.log(safe)).sum())
    grad_compact = w_cell * (probs - target)
    return loss, grad_compact


def _train_only_zscore(universe: SyntheticUniverse, blocks: Sequence[Block]
                       ) -> tuple[np.ndarray, dict[str, Any]]:
    """Z-score the frozen z-scored features using TRAIN blocks only."""
    cfg = universe.config
    z_cols = [cfg.pair_features.index(name) for name in cfg.zscored_features
              if name in cfg.pair_features]
    train_idx = universe.design_indices(blocks)
    train_rows = universe.pair_values[train_idx]
    mean = train_rows[:, z_cols].mean(axis=0)
    std = train_rows[:, z_cols].std(axis=0)
    std = np.where(std > 0.0, std, 1.0)
    design = universe.raw_design.copy()
    design[:, z_cols] = (design[:, z_cols] - mean) / std
    meta = {
        "zscored_features": list(cfg.zscored_features),
        "pair_column_indices": z_cols,
        "mean": mean.tolist(),
        "std": std.tolist(),
        "fitted_on": "TRAIN_ONLY",
        "train_row_count": int(train_idx.size),
    }
    return design, meta


# --------------------------------------------------------------------------- fixed baseline
def fixed_baseline_predictions(universe: SyntheticUniverse, regime: str) -> np.ndarray:
    """Support-normalized uniform shares over allowed foreign destinations."""
    pred = np.zeros_like(universe.targets[regime])
    for b in universe.blocks:
        share = 1.0 / len(b.allowed)
        for j in b.allowed:
            pred[b.time_index, b.origin, j] = share
    return pred


# --------------------------------------------------------------------------- parametric
def _parametric_predict(universe: SyntheticUniverse, regime: str, theta: np.ndarray) -> np.ndarray:
    X_fit = _fitted_matrix(universe)
    pred = np.zeros_like(universe.targets[regime])
    for b in universe.blocks:
        idx = [universe.row(b.time_index, b.origin, j) for j in b.allowed]
        scores = X_fit[idx] @ theta
        shares = _masked_softmax(scores, np.ones(len(idx), dtype=bool))
        for pos, j in enumerate(b.allowed):
            pred[b.time_index, b.origin, j] = shares[pos]
    return pred


@dataclass
class FitOutcome:
    family: str
    regime: str
    seed: int | None
    predictions: np.ndarray
    coefficients: list[float] | None
    objective: float | None
    convergence: dict[str, Any]
    best_step: int | None
    best_validation_loss: float | None
    runtime_seconds: float
    attempts: int
    backend: str
    diagnostics: dict[str, Any] = field(default_factory=dict)

    def identity(self) -> dict[str, Any]:
        return {
            "family": self.family,
            "regime": self.regime,
            "seed": self.seed,
            "objective": self.objective,
            "best_step": self.best_step,
            "best_validation_loss": self.best_validation_loss,
            "runtime_seconds": self.runtime_seconds,
            "attempts": self.attempts,
            "backend": self.backend,
            "coefficients": self.coefficients,
        }


def fit_parametric(universe: SyntheticUniverse, regime: str, *,
                   scipy_optimizer: Callable[..., Any] | None = None) -> FitOutcome:
    """Six-column weighted conditional multinomial-logit MLE (deterministic)."""
    from scipy.optimize import minimize  # local import: environment already provides SciPy

    cfg = universe.config
    started = time.perf_counter()
    train = universe.blocks_for("TRAIN")
    X_fit = _fitted_matrix(universe)
    X, Y, raw_w, mask, cell_index = _stack(universe, train, regime, X_fit)
    w = raw_w / raw_w.sum()

    def neg_loglik(theta: np.ndarray) -> float:
        loss, _ = _softmax_cross_entropy(X @ theta, Y, w, mask, cell_index)
        return loss

    def grad(theta: np.ndarray) -> np.ndarray:
        _, g = _softmax_cross_entropy(X @ theta, Y, w, mask, cell_index)
        return X.T @ g

    res = minimize(neg_loglik, np.zeros(X.shape[1], dtype=float), jac=grad, method="L-BFGS-B",
                   options={"maxiter": 5000, "ftol": 1e-14, "gtol": 1e-12, "maxls": 50})
    runtime = time.perf_counter() - started

    pred = _parametric_predict(universe, regime, np.asarray(res.x))

    convergence = {
        "success": bool(res.success),
        "status": int(res.status),
        "message": str(res.message),
        "iterations": int(res.nit),
        "function_evaluations": int(res.nfev),
        "gradient_norm_inf": float(np.abs(res.jac).max()) if res.jac is not None else None,
    }
    return FitOutcome(
        family="parametric", regime=regime, seed=None, predictions=pred,
        coefficients=[float(v) for v in res.x], objective=float(res.fun),
        convergence=convergence, best_step=None, best_validation_loss=None,
        runtime_seconds=runtime, attempts=1, backend="scipy.optimize.minimize:L-BFGS-B",
        diagnostics={"fitted_columns": list(cfg.fitted_columns), "train_blocks": len(train)},
    )


# --------------------------------------------------------------------------- neural
def _init_mlp(seed: int, n_features: int, widths: Sequence[int]) -> dict[str, np.ndarray]:
    rng = np.random.default_rng(seed)
    shapes = [n_features, *widths, 1]
    params: dict[str, np.ndarray] = {}
    for layer in range(len(shapes) - 1):
        fan_in = shapes[layer]
        scale = math.sqrt(2.0 / fan_in) if layer == 0 else math.sqrt(1.0 / fan_in)
        params[f"W{layer}"] = rng.standard_normal((shapes[layer], shapes[layer + 1])) * scale
        params[f"b{layer}"] = np.zeros(shapes[layer + 1])
    return params


def _forward(params: dict[str, np.ndarray], X: np.ndarray, widths: Sequence[int]
             ) -> tuple[float, list[np.ndarray], list[np.ndarray]]:
    """Forward pass; returns score vector and cached activations for backprop."""
    acts: list[np.ndarray] = [X]
    pre: list[np.ndarray] = []
    h = X
    layers = len(widths) + 1
    for layer in range(layers):
        z = h @ params[f"W{layer}"] + params[f"b{layer}"]
        pre.append(z)
        if layer == 0:
            h = np.maximum(z, 0.0)          # ReLU
        elif layer == 1:
            h = np.tanh(z)                   # Tanh
        else:
            h = z                            # scalar output
        acts.append(h)
    return h, acts, pre


def _backward(params: dict[str, np.ndarray], acts: list[np.ndarray], pre: list[np.ndarray],
              grad_out: np.ndarray, widths: Sequence[int]) -> dict[str, np.ndarray]:
    grads: dict[str, np.ndarray] = {}
    delta = grad_out.reshape(-1, 1)
    layers = len(widths) + 1
    for layer in reversed(range(layers)):
        grads[f"W{layer}"] = acts[layer].T @ delta
        grads[f"b{layer}"] = delta.sum(axis=0)
        if layer > 0:
            upstream = delta @ params[f"W{layer}"].T
            if layer - 1 == 0:
                delta = upstream * (pre[layer - 1] > 0.0)
            else:
                delta = upstream * (1.0 - np.tanh(pre[layer - 1]) ** 2)
    return grads


def _adam_step(params: dict[str, np.ndarray], grads: dict[str, np.ndarray],
               state: dict[str, np.ndarray], step: int, lr: float,
               beta1: float = 0.9, beta2: float = 0.999, eps: float = 1e-8) -> None:
    for key in params:
        m = state.setdefault(f"m_{key}", np.zeros_like(params[key]))
        v = state.setdefault(f"v_{key}", np.zeros_like(params[key]))
        m *= beta1
        m += (1.0 - beta1) * grads[key]
        v *= beta2
        v += (1.0 - beta2) * grads[key] ** 2
        m_hat = m / (1.0 - beta1 ** step)
        v_hat = v / (1.0 - beta2 ** step)
        params[key] -= lr * m_hat / (np.sqrt(v_hat) + eps)


def _neural_predict(universe: SyntheticUniverse, regime: str, params: dict[str, np.ndarray],
                    widths: Sequence[int]) -> np.ndarray:
    return _neural_predict_blocks(universe, regime, params, widths, universe.blocks)


def fit_neural(universe: SyntheticUniverse, regime: str, seed: int, *,
               design: np.ndarray | None = None, max_steps: int | None = None) -> FitOutcome:
    """Frozen MLP pair scorer trained with full-batch Adam under the frozen protocol."""
    cfg = universe.config
    started = time.perf_counter()
    random.seed(seed)
    np.random.seed(seed)
    design = universe.design_matrix if design is None else design
    steps_limit = cfg.max_steps if max_steps is None else int(max_steps)

    widths = cfg.hidden_widths
    params = _init_mlp(seed, design.shape[1], widths)
    state: dict[str, np.ndarray] = {}

    train = universe.blocks_for("TRAIN")
    valid = universe.blocks_for("VALIDATION")
    Xtr, Ytr, raw_wtr, mask_tr, idx_tr = _stack(universe, train, regime, design)
    wtr = raw_wtr / raw_wtr.sum()
    Xva, Yva, raw_wva, mask_va, idx_va = _stack(universe, valid, regime, design)
    wva = raw_wva / raw_wva.sum()

    def loss_on(X: np.ndarray, Y: np.ndarray, w: np.ndarray, mask: np.ndarray, idx: np.ndarray) -> float:
        scores, _, _ = _forward(params, X, widths)
        value, _ = _softmax_cross_entropy(scores, Y, w, mask, idx)
        return value

    best = {"loss": float("inf"), "step": 0, "params": {k: v.copy() for k, v in params.items()},
            "valid_loss": float("inf")}
    history: list[dict[str, float]] = []
    steps_without_improvement = 0
    step = 0
    for step in range(1, steps_limit + 1):
        scores, acts, pre = _forward(params, Xtr, widths)
        _, grad_compact = _softmax_cross_entropy(scores, Ytr, wtr, mask_tr, idx_tr)
        grad_scores = grad_compact
        grads = _backward(params, acts, pre, grad_scores, widths)
        _adam_step(params, grads, state, step, cfg.learning_rate)
        train_loss = loss_on(Xtr, Ytr, wtr, mask_tr, idx_tr)
        if train_loss < best["loss"]:
            best["loss"] = train_loss
            best["step"] = step
        if step % cfg.eval_every == 0:
            valid_loss = loss_on(Xva, Yva, wva, mask_va, idx_va)
            history.append({"step": step, "train_loss": train_loss, "validation_loss": valid_loss})
            if valid_loss < best["valid_loss"] - cfg.early_stop_min_delta:
                best["valid_loss"] = valid_loss
                best["params"] = {k: v.copy() for k, v in params.items()}
                best["step"] = step
                steps_without_improvement = 0
            else:
                steps_without_improvement += cfg.eval_every
                if steps_without_improvement >= cfg.early_stop_patience:
                    break

    runtime = time.perf_counter() - started
    final_params = best["params"]
    pred = _neural_predict(universe, regime, final_params, widths)
    pred_train = _neural_predict_blocks(universe, regime, final_params, widths, train)
    train_ce = _weighted_cross_entropy(universe, regime, pred_train, universe.blocks_for("TRAIN"))
    return FitOutcome(
        family="neural", regime=regime, seed=seed, predictions=pred, coefficients=None,
        objective=float(train_ce), convergence={"early_stopped": step < steps_limit,
                                               "final_step": step},
        best_step=int(best["step"]), best_validation_loss=float(best["valid_loss"]),
        runtime_seconds=runtime, attempts=1, backend="numpy-adam-full-batch",
        diagnostics={
            "hidden_widths": list(widths),
            "activations": list(cfg.activations),
            "steps_executed": step,
            "learning_rate": cfg.learning_rate,
            "early_stop_patience": cfg.early_stop_patience,
            "early_stop_min_delta": cfg.early_stop_min_delta,
            "loss_history_every": cfg.eval_every,
            "history": history,
            "train_weighted_cross_entropy": float(train_ce),
        },
    )


def _neural_predict_blocks(universe: SyntheticUniverse, regime: str,
                           params: dict[str, np.ndarray], widths: Sequence[int],
                           blocks: Sequence[Block]) -> np.ndarray:
    pred = np.zeros_like(universe.targets[regime])
    design = universe.design_matrix
    for b in blocks:
        idx = [universe.row(b.time_index, b.origin, j) for j in b.allowed]
        scores, _, _ = _forward(params, design[idx], widths)
        shares = _masked_softmax(scores.reshape(-1), np.ones(len(idx), dtype=bool))
        for pos, j in enumerate(b.allowed):
            pred[b.time_index, b.origin, j] = shares[pos]
    return pred


# --------------------------------------------------------------------------- metrics
def _weighted_cross_entropy(universe: SyntheticUniverse, regime: str, pred: np.ndarray,
                            blocks: Sequence[Block]) -> float:
    if not blocks:
        return float("nan")
    w = np.array([universe.ell[b.time_index, b.origin] for b in blocks])
    w = w / w.sum()
    total = 0.0
    for weight, b in zip(w, blocks):
        for j in b.allowed:
            target = universe.targets[regime][b.time_index, b.origin, j]
            value = max(pred[b.time_index, b.origin, j], 1e-300)
            total += -weight * target * math.log(value)
    return float(total)


def evaluate_predictions(universe: SyntheticUniverse, regime: str, pred: np.ndarray,
                         blocks: Sequence[Block]) -> dict[str, Any]:
    """Frozen metrics on one split: primary and secondary."""
    cfg = universe.config
    if not blocks:
        raise ValueError("no blocks to evaluate")
    w = np.array([universe.ell[b.time_index, b.origin] for b in blocks])
    w = w / w.sum()

    weighted_ce = _weighted_cross_entropy(universe, regime, pred, blocks)
    abs_err, kl_values, top1_hits, top1_total = 0.0, [], 0, 0
    cells = 0
    row_norm_max = 0.0
    negativity = 0
    support_violation = 0
    for b in blocks:
        row_sum = 0.0
        target_row, pred_row = {}, {}
        for j in b.allowed:
            t_val = universe.targets[regime][b.time_index, b.origin, j]
            p_val = pred[b.time_index, b.origin, j]
            target_row[j], pred_row[j] = t_val, p_val
            row_sum += p_val
            abs_err += abs(p_val - t_val)
            cells += 1
            if t_val > 0.0:
                kl_values.append(t_val * math.log(t_val / max(p_val, 1e-300)))
            if p_val < 0.0:
                negativity += 1
        row_norm_max = max(row_norm_max, abs(row_sum - 1.0))
        top1_total += 1
        t_arg = max(target_row, key=target_row.get)
        p_arg = max(pred_row, key=pred_row.get)
        if t_arg == p_arg:
            top1_hits += 1
        for j in range(len(cfg.region_ids)):
            if j in b.allowed:
                continue
            if pred[b.time_index, b.origin, j] != 0.0:
                support_violation += 1

    occupied = np.zeros(len(cfg.region_ids), dtype=bool)
    for b in blocks:
        for j in b.allowed:
            occupied[j] = True
    return {
        "split_blocks": len(blocks),
        "evaluated_cells": cells,
        "weighted_cross_entropy": float(weighted_ce),
        "mean_absolute_share_error": float(abs_err / cells),
        "row_normalization_violation_max": float(row_norm_max),
        "negativity_violation_count": int(negativity),
        "support_violation_count": int(support_violation),
        "top1_destination_accuracy": float(top1_hits / top1_total),
        "share_kl_per_block_mean": float(sum(kl_values) / top1_total),
        "block_weight_policy": "ell_i_t_normalized_over_reported_split",
        "row_normalization_tolerance": cfg.row_normalization_tolerance,
        "row_normalization_within_tolerance": bool(row_norm_max <= cfg.row_normalization_tolerance),
        "occupied_destination_ids": [cfg.region_ids[i] for i in np.flatnonzero(occupied)],
    }


def _prediction_key(regime: str, family: str, seed: int | None) -> str:
    return f"{regime}:{family}" + (f":seed{seed}" if seed is not None else "")


# --------------------------------------------------------------------------- validate
def validate_only_report(universe: SyntheticUniverse) -> dict[str, Any]:
    """Config/generator validation with **no optimizer step**."""
    cfg = universe.config
    R = len(cfg.region_ids)

    def shares(regime: str, origin: int, time_index: int) -> list[float]:
        block = universe.blocks[time_index * R + origin]
        return [universe.targets[regime][time_index, origin, j] for j in block.allowed]

    reference = {}
    for regime in ("S0", "S1"):
        for origin, key in ((0, "r00"), (R - 1, "r04")):
            for time_index, suffix in ((0, "t1"), (len(cfg.time_ids) - 1, "t4")):
                reference[f"{regime}:{key}_{suffix}"] = shares(regime, origin, time_index)

    # contrast design over TRAIN blocks, in the six fitted columns
    X_fit = _fitted_matrix(universe)
    nl = _nonlinear_columns(universe)
    contrast_rows, s0_terms, s1_terms = [], [], []
    for b in universe.blocks_for("TRAIN"):
        base = b.allowed[0]
        base_row = X_fit[universe.row(b.time_index, b.origin, base)]
        for j in b.allowed[1:]:
            idx = universe.row(b.time_index, b.origin, j)
            contrast_rows.append(X_fit[idx] - base_row)
            s0_terms.append(0)
            s1_terms.append(0)
    contrast = np.array(contrast_rows)

    # S0 score = frozen coefficients on the fitted columns (block constants cancel)
    theta0 = np.array([cfg.s0_coefficients[name] for name in cfg.fitted_columns])
    rows, keys = [], []
    for b in universe.blocks_for("TRAIN"):
        for j in b.allowed:
            keys.append((b.time_index, b.origin, j))
            rows.append(X_fit[universe.row(b.time_index, b.origin, j)] @ theta0)
    s0_full = np.array(rows)
    s1_full = s0_full + cfg.beta_sq * nl[[universe.row(*k) for k in keys], 0] \
        + cfg.beta_relu * nl[[universe.row(*k) for k in keys], 1]

    def contrast_target(full: np.ndarray) -> np.ndarray:
        out, pos = [], 0
        for b in universe.blocks_for("TRAIN"):
            base_pos = pos
            base_val = full[base_pos]
            for _ in b.allowed[1:]:
                pos += 1
                out.append(full[pos] - base_val)
            pos += 1
        return np.array(out)

    y0 = contrast_target(s0_full)
    y1 = contrast_target(s1_full)

    def residual(y: np.ndarray) -> float:
        coef, *_ = np.linalg.lstsq(contrast, y, rcond=None)
        return float(np.abs(y - contrast @ coef).max())

    x2_res = residual(contrast_target(nl[[universe.row(*k) for k in keys], 0]))
    x3_res = residual(contrast_target(nl[[universe.row(*k) for k in keys], 1]))

    return {
        "config_revision": cfg.config_revision,
        "config_sha256": cfg.sha256,
        "route_activation_comment": cfg.activation_comment,
        "operative_baseline": cfg.operative_baseline,
        "region_count": R,
        "time_count": len(cfg.time_ids),
        "allocation_blocks": len(universe.blocks),
        "evaluable_cells": int(len(universe.design_meta)),
        "support_counts": [len(universe.blocks[i].allowed) for i in range(R)],
        "split_counts": dict(cfg.split_counts),
        "split_counts_sum": sum(cfg.split_counts.values()),
        "reference_shares": reference,
        "contrast_rows": int(contrast.shape[0]),
        "contrast_columns": int(contrast.shape[1]),
        "contrast_rank": int(np.linalg.matrix_rank(contrast)),
        "s0_contrast_residual": residual(y0),
        "s1_contrast_residual": residual(y1),
        "x2_contrast_residual": x2_res,
        "x3_contrast_residual": x3_res,
        "residual_precision_floor": 1e-12,
        "p1a_accounting": universe.p1a_diagnostics,
        "fixed_baseline_row_norm_max": max(
            abs(sum(1.0 / len(b.allowed) for _ in b.allowed) - 1.0) for b in universe.blocks),
        "optimizer_steps_performed": 0,
    }


# --------------------------------------------------------------------------- run
def _split_metrics(universe: SyntheticUniverse, regime: str, pred: np.ndarray) -> dict[str, Any]:
    return {state: evaluate_predictions(universe, regime, pred, universe.blocks_for(state))
            for state in ("TRAIN", "VALIDATION", "TEST", "EXCLUDED_REFERENCE_ONLY")}


def run_scientific_program(universe: SyntheticUniverse, *, attempt_log: list[dict[str, Any]],
                           retry_budget: dict[str, int]) -> dict[str, Any]:
    """Execute the frozen 8/12/<=13 plan. Returns the full results payload."""
    cfg = universe.config
    started = time.perf_counter()
    outcomes: dict[str, FitOutcome] = {}
    metrics: dict[str, dict[str, Any]] = {}
    determinism: dict[str, Any] = {}

    def record(kind: str, regime: str, family: str, seed: int | None) -> None:
        attempt_log.append({
            "index": len(attempt_log) + 1,
            "kind": kind,
            "regime": regime,
            "family": family,
            "seed": seed,
        })

    # ---- parametric: 2 primaries + 2 verification repeats ---------------
    for regime in ("S0", "S1"):
        record("primary", regime, "parametric", None)
        fit = fit_parametric(universe, regime)
        outcomes[_prediction_key(regime, "parametric", None)] = fit
        metrics[_prediction_key(regime, "parametric", None)] = _split_metrics(universe, regime, fit.predictions)
    for regime in ("S0", "S1"):
        record("verification_repeat", regime, "parametric", None)
        repeat = fit_parametric(universe, regime)
        determinism[f"parametric_{regime}"] = {
            "deviation": float(np.abs(repeat.predictions - outcomes[_prediction_key(regime, "parametric", None)].predictions).max()),
            "repeat_objective": repeat.objective,
            "primary_objective": outcomes[_prediction_key(regime, "parametric", None)].objective,
            "coefficient_deviation": float(np.abs(
                np.array(repeat.coefficients) - np.array(outcomes[_prediction_key(regime, "parametric", None)].coefficients)).max()),
        }

    # ---- neural: 6 primaries + 2 seed-0 verification repeats -----------
    design, preprocess_meta = _train_only_zscore(universe, universe.blocks_for("TRAIN"))
    universe._design_matrix = design        # frozen TRAIN-only preprocessing
    neural_repeats: dict[tuple[str, int], np.ndarray] = {}
    for regime in ("S0", "S1"):
        for seed in cfg.neural_seeds:
            record("primary", regime, "neural", seed)
            fit = fit_neural(universe, regime, seed, design=design)
            key = _prediction_key(regime, "neural", seed)
            if seed == 0:
                neural_repeats[(regime, seed)] = fit.predictions
                outcomes[key] = fit
                metrics[key] = _split_metrics(universe, regime, fit.predictions)
            else:
                outcomes[key] = fit
                metrics[key] = _split_metrics(universe, regime, fit.predictions)
    for regime in ("S0", "S1"):
        record("verification_repeat", regime, "neural", 0)
        repeat = fit_neural(universe, regime, 0, design=design)
        determinism[f"neural_{regime}_seed0"] = {
            "deviation": float(np.abs(repeat.predictions - neural_repeats[(regime, 0)]).max()),
            "repeat_best_step": repeat.best_step,
            "primary_best_step": outcomes[_prediction_key(regime, "neural", 0)].best_step,
            "repeat_best_validation_loss": repeat.best_validation_loss,
            "primary_best_validation_loss": outcomes[_prediction_key(regime, "neural", 0)].best_validation_loss,
        }

    # ---- fixed baseline: evaluation only, not a fit --------------------
    fixed_metrics = {}
    for regime in ("S0", "S1"):
        fixed_metrics[regime] = _split_metrics(universe, regime, fixed_baseline_predictions(universe, regime))

    total_runtime = time.perf_counter() - started
    return {
        "fit_outcomes": outcomes,
        "metrics": metrics,
        "fixed_baseline_metrics": fixed_metrics,
        "determinism": determinism,
        "preprocessing": preprocess_meta,
        "total_runtime_seconds": total_runtime,
    }
