"""Issue #58 / DLH-5V-J: boundary-HJB selected-Q implementation of the accepted
Issue #57 design contract.

Implements (Route A, accepted Issue #57 Rev 2):

- finite ``D_W`` triangle grid / represented-state map (``10*j + 7*i <= N_m``);
- Route-A state-family classifier F0..F11 (F9 exclusive-first; F4 before F3;
  corners before faces; exactly one family per represented state);
- economic admissibility (only genuine active-face tangent laws) strictly
  separated from algorithmic search brackets;
- candidate dispatch to exactly one authorized represented sector per candidate
  (documented 5V-F representability exclusions exclude the WHOLE candidate;
  no lost-diagonal escape);
- deterministic algorithmic search brackets (cone-aware initialization from
  effective-gradient FOC anchors + family feasibility; expansion on artificial
  bound contact; persistent contact -> ``OPTIMIZER_SEARCH_FAILURE``);
- candidate local drift / destinations / nonnegative rates (exact first
  moment) BEFORE maximization;
- discrete Bellman score ``H_h = u - v + sum q [V(dest)-V(s)] + z-switch``
  (z-switch authority = accepted ``grid.switch_matrix`` only);
- ONE deterministic statewise selection with exact/machine-identical tie
  semantics and the frozen precedence;
- conservative backward Q rows (``Q[row,col] > 0`` iff actual represented
  transition; diagonal = -sum of actual outgoing; row sums zero);
- implicit/pseudo-time HJB iteration
  ``[(1/delta + rho)I - Q_selected(V_old)] V_new = u_selected(V_old) + V_old/delta``
  with F0 rows on the accepted interior path (oracle local-policy function,
  read-only) and boundary rows on the new conservative path;
- post-convergence re-selection from final V, final conservative Q, and the
  mandatory final Bellman residual
  ``R_Bellman(V) = rho*V - [u_selected(V) + Q_selected(V) V]``;
- frozen failure taxonomy (8 names), no silent fallback.

Theory ceiling: Issue #56 Outcome-B unbounded-control convergence-application
block remains explicit and UNSOLVED. Stationary KFE remains NOT AUTHORIZED;
this module never invokes it. The accepted household oracle
``matlab_faithful_two_asset_ha.py`` is consumed read-only (blob
``76ae5b149993a7edeeb8eb337f1b02b3fe33c51e``) and never mutated.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np
from scipy import sparse
from scipy.sparse import linalg
from scipy.optimize import brentq

from deep_learning_hank.two_asset.matlab_faithful_two_asset_ha import (
    EconomicParams,
    HouseholdInputs,
    MatlabFaithfulLocalPolicy,
    MATLAB_DRIFT_TOLERANCE,
    asset_drifts_matlab_faithful,
    flow_utility,
    matlab_faithful_illiquid_return,
    select_matlab_faithful_local_policy,
)

# ---------------------------------------------------------------------------
# Frozen names
# ---------------------------------------------------------------------------

FAMILIES = ("F0", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11")

SECTORS = ("T_REALLOC", "R_REVERSE", "R_DEPLETE", "REV", "CASE_B", "FACE")

# Frozen deterministic tie-precedence order (Issue #57 report 4 §4).
SECTOR_RANK = {name: rank for rank, name in enumerate(SECTORS)}

FAILURE_NAMES = (
    "SCIENTIFIC_ADMISSIBILITY_FAILURE",
    "REPRESENTATION_FAILURE",
    "OPTIMIZER_SEARCH_FAILURE",
    "DERIVATIVE_EFFECTIVE_DOMAIN_FAILURE",
    "GENERATOR_CONSERVATION_FAILURE",
    "HJB_LINEAR_SOLVE_FAILURE",
    "HJB_NONCONVERGENCE",
    "REGRESSION_FAILURE",
)


class BoundaryHJBFailure(RuntimeError):
    """Frozen taxonomy failure object (no silent fallback)."""

    def __init__(self, failure_name: str, message: str, detail: Optional[dict] = None) -> None:
        if failure_name not in FAILURE_NAMES:
            raise ValueError(f"unknown failure name: {failure_name!r}")
        super().__init__(message)
        self.failure_name = failure_name
        self.message = message
        self.detail = dict(detail) if detail else {}


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class BoundaryHJBConfig:
    """Fully frozen validation configuration (predeclared before first run)."""

    m: int
    w_max: float
    b_min: float
    a_max: float
    params: EconomicParams
    inputs: HouseholdInputs
    z: np.ndarray
    switch_matrix: np.ndarray
    delta: float
    tolerance_iter: float
    tolerance_bellman: float
    max_iterations: int
    # algorithmic search (not economics)
    n_c_grid: int = 9
    n_d_grid: int = 9
    bracket_expand_factor: float = 4.0
    max_bracket_expansions: int = 3
    c_floor: float = 1.0e-6
    d_wide_min: float = 20.0
    # declared tolerances
    drift_tolerance: float = MATLAB_DRIFT_TOLERANCE
    row_sum_tolerance: float = 1.0e-9
    first_moment_atol: float = 1.0e-9
    bellman_norm: str = "inf"
    # diagnostic window for policy/family switching
    switching_window: int = 5

    def __post_init__(self) -> None:
        if self.m < 1:
            raise ValueError("m must be >= 1")
        if not (self.w_max > self.b_min):
            raise ValueError("w_max must exceed b_min")
        if self.a_max <= 0.0 or self.b_min >= 0.0:
            raise ValueError("domain bounds are invalid")
        if self.delta <= 0.0 or self.tolerance_iter <= 0.0 or self.tolerance_bellman <= 0.0:
            raise ValueError("numerics must be positive")
        if self.max_iterations < 1 or self.n_c_grid < 3 or self.n_d_grid < 3:
            raise ValueError("iteration/grid counts are invalid")
        if self.bracket_expand_factor <= 1.0 or self.max_bracket_expansions < 0:
            raise ValueError("bracket expansion rule is invalid")
        if self.c_floor <= 0.0 or self.d_wide_min <= 0.0:
            raise ValueError("algorithmic search constants must be positive")
        if self.bellman_norm not in ("inf",):
            raise ValueError("only the declared inf-norm Bellman criterion is supported here")
        z = np.asarray(self.z, dtype=float)
        if z.ndim != 1 or z.size < 2 or not np.all(np.isfinite(z)) or not np.all(np.diff(z) > 0):
            raise ValueError("z must be finite and strictly increasing")
        switch = np.asarray(self.switch_matrix, dtype=float)
        if switch.shape != (z.size, z.size) or not np.isfinite(switch).all():
            raise ValueError("switch_matrix shape is incompatible with z")
        if not np.all(switch[np.eye(z.size, dtype=bool)] <= 0.0):
            raise ValueError("switch_matrix diagonal entries must be non-positive (generator form)")
        if not np.all(np.abs(switch.sum(axis=1)) < 1.0e-9):
            raise ValueError("switch_matrix rows must sum to zero (generator form)")
        if self.inputs.wages.size != 1:
            raise ValueError(
                "the accepted interior (F0) path requires a single-wage HouseholdInputs "
                "(source select_matlab_faithful_local_policy contract)"
            )


# ---------------------------------------------------------------------------
# Grid / classifier
# ---------------------------------------------------------------------------


class BoundaryHJBGrid:
    """Finite D_W triangle at symbolic level m (frozen geometry)."""

    def __init__(self, m: int, w_max: float, b_min: float, a_max: float) -> None:
        self.m = m
        self.jmax = 19 * m
        self.da = 10.0 / (19.0 * m)
        self.db = 7.0 / (19.0 * m)
        self.a_max = a_max
        self.b_min = b_min
        self.w_max = w_max
        self.N_m = int(np.floor(19.0 * m * (w_max - b_min)))
        nodes: list[tuple[int, int]] = []
        for j in range(self.jmax + 1):
            it = (self.N_m - 10 * j) // 7
            if it < 0:
                continue
            for i in range(it + 1):
                nodes.append((j, i))
        self.nodes = nodes
        self.n_nodes = len(nodes)
        self.node_of = {(j, i): k for k, (j, i) in enumerate(nodes)}
        self.j_arr = np.array([j for (j, i) in nodes], dtype=int)
        self.i_arr = np.array([i for (j, i) in nodes], dtype=int)
        self.i_t = np.array([max((self.N_m - 10 * j) // 7, -1) for j in range(self.jmax + 1)], dtype=int)
        self.a_arr = self.j_arr * self.da
        self.b_arr = self.b_min + self.i_arr * self.db
        self.families = np.array([self._classify(j, i) for (j, i) in nodes], dtype=object)

    def w_active(self, j: int, i: int) -> bool:
        it = self.i_t[j]
        return (i == it) or (i == it - 1 and it >= 2)

    def _classify(self, j: int, i: int) -> str:
        """Route-A classifier (accepted Issue #57 Rev 2) — exactly one family."""
        it = self.i_t[j]
        wactive = (i == it) or (i == it - 1 and it >= 2)
        if not wactive:
            if j == 0 and i == 0:
                return "F10"
            if j == self.jmax and i == 0:
                return "F11"
            if j == 0:
                return "F5"
            if j == self.jmax:
                return "F6"
            if i == 0:
                return "F7"
            return "F0"
        if self.N_m == 190 * self.m and (j, i) in {(self.jmax - 7, 9), (self.jmax, 0)}:
            return "F9"
        if i == 0:
            return "F4"
        if j <= 6:
            return "F2"
        if j >= self.jmax - 6:
            return "F3"
        if i >= 10:
            return "F1"
        return "F8"

    def classify(self, j: int, i: int) -> str:
        return self._classify(j, i)

    def neighbors(self, j: int, i: int) -> dict[str, Optional[int]]:
        return {
            "up": self.node_of.get((j, i + 1)),
            "down": self.node_of.get((j, i - 1)),
            "right": self.node_of.get((j + 1, i)),
            "left": self.node_of.get((j - 1, i)),
        }


# ---------------------------------------------------------------------------
# Sector dispatch (pure algebra; exact first moments; documented exclusions)
# ---------------------------------------------------------------------------


def drift_admissible(grid: BoundaryHJBGrid, family: str, j: int, i: int,
                     mu_a: float, mu_b: float, tol: float = MATLAB_DRIFT_TOLERANCE) -> bool:
    """Genuine active-face tangent laws only (no global mu_b >= 0, no budget)."""
    mu_w = mu_a + mu_b
    if family == "F0":
        return True
    if family == "F1":
        return mu_w <= tol
    if family == "F2":
        if j == 0:
            return mu_a >= -tol and mu_w <= tol
        return mu_w <= tol
    if family == "F3":
        if j == grid.jmax:
            return mu_a <= tol and mu_w <= tol
        return mu_w <= tol
    if family == "F4":
        return mu_b >= -tol and mu_w <= tol
    if family == "F8":
        return mu_w <= tol
    if family == "F9":
        return mu_b >= -tol and mu_w <= tol
    if family == "F5":
        return mu_a >= -tol
    if family == "F6":
        return mu_a <= tol
    if family == "F7":
        return mu_b >= -tol
    if family == "F10":
        return mu_a >= -tol and mu_b >= -tol
    if family == "F11":
        return mu_a <= tol and mu_b >= -tol
    raise BoundaryHJBFailure("REPRESENTATION_FAILURE", f"drift_admissible: no law for family {family!r}")


def sector_dispatch(
    grid: BoundaryHJBGrid,
    family: str,
    j: int,
    i: int,
    mu_a: float,
    mu_b: float,
    tol: float = MATLAB_DRIFT_TOLERANCE,
) -> Optional[tuple[str, list[tuple[int, int, float]]]]:
    """Dispatch drift (mu_a, mu_b) to exactly one sector for the family.

    Returns ``(sector, [(dest_j, dest_i, rate), ...])`` or ``None`` when the
    candidate class is a documented representability exclusion (5V-F content /
    unavailable destination direction). Rates are the accepted sector formulas
    with exact first moment ``sum q w = (mu_a, mu_b)``.
    """
    mu_w = mu_a + mu_b
    K = 19.0 * grid.m
    if family == "F1":
        if mu_b >= -tol:
            return "T_REALLOC", [((j - 7, i + 10), K * mu_b / 70.0), ((j - 1, i), K * (-mu_w) / 10.0)]
        if mu_a > tol:
            return "R_REVERSE", [((j + 7, i - 10), K * mu_a / 70.0), ((j, i - 1), K * (-mu_w) / 7.0)]
        return "R_DEPLETE", [((j - 1, i), K * (-mu_a) / 10.0), ((j, i - 1), K * (-mu_b) / 7.0)]
    if family == "F2":
        if j == 0:
            return "REV", [((j + 7, i - 10), K * mu_a / 70.0), ((j, i - 1), K * (-mu_w) / 7.0)]
        # j in {1..6}: T_realloc forward needs j >= 7 -> excluded (5V-F forward-sliding content)
        if mu_b >= -tol:
            return None
        if mu_a > tol:
            return "R_REVERSE", [((j + 7, i - 10), K * mu_a / 70.0), ((j, i - 1), K * (-mu_w) / 7.0)]
        return "R_DEPLETE", [((j - 1, i), K * (-mu_a) / 10.0), ((j, i - 1), K * (-mu_b) / 7.0)]
    if family == "F3":
        if mu_b >= -tol:
            return "T_REALLOC", [((j - 7, i + 10), K * mu_b / 70.0), ((j - 1, i), K * (-mu_w) / 10.0)]
        if mu_a <= tol:
            return "R_DEPLETE", [((j - 1, i), K * (-mu_a) / 10.0), ((j, i - 1), K * (-mu_b) / 7.0)]
        return None  # {mu_b < 0, mu_a > 0}: reverse-sliding obstruction, excluded whole (5V-F content)
    if family == "F4":
        return "CASE_B", [((j - 7, 10), K * mu_b / 70.0), ((j - 1, 0), K * (-mu_w) / 10.0)]
    if family == "F8":
        if mu_b >= -tol:
            return "T_REALLOC", [((j - 7, i + 10), K * mu_b / 70.0), ((j - 1, i), K * (-mu_w) / 10.0)]
        if mu_a <= tol:
            return "R_DEPLETE", [((j - 1, i), K * (-mu_a) / 10.0), ((j, i - 1), K * (-mu_b) / 7.0)]
        return None  # R_reverse mirror needs i >= 10 -> excluded
    if family == "F9":
        if (j, i) == (grid.jmax - 7, 9):
            return "CASE_B", [((j - 7, i + 10), K * mu_b / 70.0), ((j - 1, i), K * (-mu_w) / 10.0)]
        return "T_REALLOC", [((j - 7, 10), K * mu_b / 70.0), ((j - 1, 0), K * (-mu_w) / 10.0)]
    if family == "F5":
        out: list[tuple[int, int, float]] = [((1, i), K * mu_a / 10.0)]
        if mu_b >= -tol:
            out.append(((0, i + 1), K * mu_b / 7.0))
        else:
            out.append(((0, i - 1), K * (-mu_b) / 7.0))
        return "FACE", out
    if family == "F6":
        out = [((j - 1, i), K * (-mu_a) / 10.0)]
        if mu_b >= -tol:
            out.append(((j, i + 1), K * mu_b / 7.0))
        else:
            out.append(((j, i - 1), K * (-mu_b) / 7.0))
        return "FACE", out
    if family == "F7":
        out = [((j, 1), K * mu_b / 7.0)]
        if mu_a >= -tol:
            out.append(((j + 1, 0), K * mu_a / 10.0))
        else:
            out.append(((j - 1, 0), K * (-mu_a) / 10.0))
        return "FACE", out
    if family == "F10":
        return "FACE", [((1, 0), K * mu_a / 10.0), ((0, 1), K * mu_b / 7.0)]
    if family == "F11":
        return "FACE", [((j - 1, 0), K * (-mu_a) / 10.0), ((j, 1), K * mu_b / 7.0)]
    raise BoundaryHJBFailure("REPRESENTATION_FAILURE", f"sector_dispatch: no contract for family {family!r}")


# ---------------------------------------------------------------------------
# Solver
# ---------------------------------------------------------------------------


@dataclass
class _PolicyRecord:
    family: str
    sector: str
    consumption: float
    labor: float
    transfer: float
    mu_a: float
    mu_b: float
    utility: float
    row_entries: list[tuple[int, float]]  # (dest_node, rate) within z-block
    diagonal: float
    artificial_binding: bool
    economic_binding: bool
    expansions: int
    c_lo: float = 0.0
    c_hi: float = 0.0
    d_lo: float = 0.0
    d_hi: float = 0.0


@dataclass
class BoundaryHJBResult:
    value: np.ndarray
    initial_value: np.ndarray
    converged: bool
    iterations: int
    convergence_statistic: float
    families: np.ndarray
    consumption: np.ndarray
    labor: np.ndarray
    transfer: np.ndarray
    mu_a: np.ndarray
    mu_b: np.ndarray
    utility: np.ndarray
    sector: np.ndarray
    q_final: sparse.csr_matrix
    u_final: np.ndarray
    bellman_residual: float
    bellman_norm: str
    tolerance_bellman: float
    bellman_pass: bool
    q_structural: dict
    bracket_diagnostics: dict
    policy_switching: dict
    node_j: np.ndarray
    node_i: np.ndarray
    n_z: int


class BoundaryHJBSolver:
    """Implements the accepted boundary-HJB scheme on the frozen triangle grid."""

    def __init__(self, config: BoundaryHJBConfig) -> None:
        self.config = config
        self.grid = BoundaryHJBGrid(config.m, config.w_max, config.b_min, config.a_max)
        self.n = self.grid.n_nodes
        self.nz = config.z.size
        self.state_size = self.n * self.nz
        self.da = self.grid.da
        self.db = self.grid.db

    # -- derivatives (declared convention, deterministic) ---------------------
    def compute_derivatives(self, V: np.ndarray, labor0: np.ndarray,
                            transfer_income: float, borrowing_rate_gap: float,
                            ) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """vb_f, vb_b, va_f, va_b over (n_nodes, n_z).

        Declared convention: vb_f[i] = (V[up]-V[i])/db when up exists; vb_b[i] =
        vb_f[i-1] when down exists; vb_b at i=0 uses the accepted b_min
        marginal-resources formula (source solve lines 534-541); top cells use
        vb_b (backward) as their effective v_b. va_f[j] = (V[right]-V[j])/da
        when right exists else 0.0 (a_max face); va_b[j] = va_f[j-1] when left
        exists else 0.0 (a=0 face) — matching the source convention.
        """
        cfg = self.config
        g = self.grid
        V = np.asarray(V, dtype=float)
        vb_f = np.empty((self.n, self.nz))
        vb_b = np.empty((self.n, self.nz))
        va_f = np.empty((self.n, self.nz))
        va_b = np.empty((self.n, self.nz))
        for node in range(self.n):
            j, i = int(g.j_arr[node]), int(g.i_arr[node])
            up = g.node_of.get((j, i + 1))
            down = g.node_of.get((j, i - 1))
            right = g.node_of.get((j + 1, i))
            left = g.node_of.get((j - 1, i))
            for nz in range(self.nz):
                if up is not None:
                    vb_f[node, nz] = (V[up, nz] - V[node, nz]) / self.db
                if down is not None:
                    vb_b[node, nz] = (V[node, nz] - V[down, nz]) / self.db
                if i == 0:
                    rb = cfg.inputs.r_b + (borrowing_rate_gap if g.b_arr[node] < 0.0 else 0.0)
                    resources = (
                        (1.0 - cfg.inputs.tau) * cfg.inputs.wages[0] * cfg.z[nz]
                        * labor0[node, nz] + transfer_income + rb * g.b_arr[node]
                    )
                    vb_b[node, nz] = resources ** (-cfg.params.gamma_c)
                if right is not None:
                    va_f[node, nz] = (V[right, nz] - V[node, nz]) / self.da
                else:
                    va_f[node, nz] = 0.0
                if left is not None:
                    va_b[node, nz] = (V[node, nz] - V[left, nz]) / self.da
                else:
                    va_b[node, nz] = 0.0
        for node in range(self.n):
            j, i = int(g.j_arr[node]), int(g.i_arr[node])
            if i == g.i_t[j]:
                vb_f[node, :] = vb_b[node, :]
        return vb_f, vb_b, va_f, va_b

    # -- interior (F0) row: accepted oracle path, read-only --------------------
    def local_interior_row(self, node: int, nz: int, V: np.ndarray,
                           vb_f: np.ndarray, vb_b: np.ndarray, va_f: np.ndarray, va_b: np.ndarray,
                           labor0: np.ndarray, transfer_income: float, borrowing_rate_gap: float,
                           ) -> tuple[MatlabFaithfulLocalPolicy, list[tuple[int, float]], float]:
        """F0 row via the accepted source local-policy function (read-only).

        Returns (policy, [(dest_node, rate)], diagonal). Outward moves are
        truncated but their diagonal is retained (source truncation convention).
        """
        cfg = self.config
        g = self.grid
        j, i = int(g.j_arr[node]), int(g.i_arr[node])
        policy = select_matlab_faithful_local_policy(
            a=float(g.a_arr[node]), b=float(g.b_arr[node]), z=float(cfg.z[nz]),
            v_a_forward=float(va_f[node, nz]), v_a_backward=float(va_b[node, nz]),
            v_b_forward=float(vb_f[node, nz]), v_b_backward=float(vb_b[node, nz]),
            baseline_labor=float(labor0[node, nz]), transfer_income=transfer_income,
            borrowing_rate_gap=borrowing_rate_gap, a_max=cfg.a_max, da=self.da, db=self.db,
            at_lower_a=(j == 0), at_upper_a=(j == g.jmax), at_lower_b=(i == 0),
            at_upper_b=False, inputs=cfg.inputs, params=cfg.params,
            tolerance=cfg.drift_tolerance,
        )
        neigh = g.neighbors(j, i)
        entries: list[tuple[int, float]] = []
        rb = policy.iteration_b_backward_rate
        rf = policy.iteration_b_forward_rate
        ab = policy.a_backward_rate
        af = policy.a_forward_rate
        if rb != 0.0 and neigh["down"] is not None:
            entries.append((neigh["down"], rb))
        if rf != 0.0 and neigh["up"] is not None:
            entries.append((neigh["up"], rf))
        if ab != 0.0 and neigh["left"] is not None:
            entries.append((neigh["left"], ab))
        if af != 0.0 and neigh["right"] is not None:
            entries.append((neigh["right"], af))
        diagonal = -(rb + rf + ab + af)  # source truncation convention (kept on diagonal)
        return policy, entries, diagonal

    # -- boundary candidate search (deterministic; cone-aware brackets) --------
    def _d_feasible_interval(self, family: str, j: int, i: int, a: float, b: float,
                             LI: float) -> tuple[float, float]:
        """Deterministic cone-aware d-interval [Dlo, Dhi] for the family.

        Uses only the genuine active tangent laws and c > 0 feasibility.
        """
        cfg = self.config
        g = self.grid
        ra_eff = float(matlab_faithful_illiquid_return(a, cfg.a_max, cfg.inputs.r_a))
        d_bound = -ra_eff * a  # mu_a <= 0 / >= 0 boundary (d <= / >= this)
        S = LI + cfg.inputs.r_b * b
        a_eff = max(a, cfg.params.a_bar)
        chi1 = cfg.params.chi_1
        chi0 = cfg.params.chi_0
        disc_pos = (1.0 + chi0) ** 2 + 2.0 * chi1 * S / a_eff
        disc_neg = (1.0 - chi0) ** 2 + 2.0 * chi1 * S / a_eff
        if disc_pos >= 0.0:
            d_pos_root = a_eff / chi1 * (-(1.0 + chi0) + np.sqrt(disc_pos))
        else:
            d_pos_root = 0.0
        if disc_neg >= 0.0:
            d_neg_root = a_eff / chi1 * (-(1.0 - chi0) - np.sqrt(disc_neg))
        else:
            d_neg_root = -np.inf
        d_wide = cfg.d_wide_min
        if family in ("F1", "F8"):
            dlo, dhi = -d_wide, d_wide
        elif family == "F2":
            if j == 0:
                dlo, dhi = 0.0, d_wide
            else:
                dlo, dhi = -d_wide, d_wide
        elif family == "F3":
            if j == g.jmax:
                dlo, dhi = -d_wide, min(d_bound, d_wide)
            else:
                dlo, dhi = -d_wide, d_wide
        elif family in ("F4", "F9"):
            dhi = min(d_bound, d_pos_root)
            dlo = max(d_neg_root, -d_wide)
        elif family == "F5":
            dlo, dhi = 0.0, d_wide
        elif family == "F6":
            dlo, dhi = -d_wide, min(d_bound, d_wide)
        elif family == "F7":
            dlo, dhi = max(d_neg_root, -d_wide), min(d_pos_root, d_wide)
        elif family == "F10":
            dlo, dhi = 0.0, min(d_pos_root, d_wide)
        elif family == "F11":
            dlo, dhi = max(d_neg_root, -d_wide), min(d_bound, d_pos_root, d_wide)
        else:
            raise BoundaryHJBFailure("REPRESENTATION_FAILURE", f"no candidate grid for family {family!r}")
        if not (np.isfinite(dlo) and np.isfinite(dhi)) or dhi < dlo - cfg.drift_tolerance:
            raise BoundaryHJBFailure(
                "OPTIMIZER_SEARCH_FAILURE",
                f"family {family!r} at (j,i)=({j},{i}): cone-feasible d-interval is empty",
            )
        return float(dlo), float(dhi)

    def _grid_lin(self, lo: float, hi: float, n: int, extra: Optional[list[float]] = None) -> list[float]:
        if hi < lo:
            return []
        vals = list(np.linspace(lo, hi, n))
        if extra:
            for v in extra:
                if lo <= v <= hi:
                    vals.append(v)
        out: list[float] = []
        for v in vals:
            if not any(abs(v - o) <= 1.0e-12 * max(1.0, abs(v)) for o in out):
                out.append(float(v))
        return out

    def _boundary_row(self, node: int, nz: int, V: np.ndarray,
                      vb_f: np.ndarray, vb_b: np.ndarray, va_f: np.ndarray, va_b: np.ndarray,
                      labor0: np.ndarray, transfer_income: float, borrowing_rate_gap: float,
                      ) -> _PolicyRecord:
        """Deterministic candidate search + ONE selection + conservative Q row."""
        cfg = self.config
        g = self.grid
        j, i = int(g.j_arr[node]), int(g.i_arr[node])
        a, b = float(g.a_arr[node]), float(g.b_arr[node])
        family = g.families[node]
        p_b = float(vb_b[node, nz])  # declared backward convention (marginal at i=0)
        # Accepted boundary effective-domain guard (frozen Issue #57 Rev-2 rule):
        # the boundary optimizer/coercivity contract requires POSITIVE effective
        # liquid marginal evidence; non-finite or non-positive p_b means the value
        # iterate has left the accepted effective domain. Surface the frozen
        # DERIVATIVE_EFFECTIVE_DOMAIN_FAILURE BEFORE any raw unbounded
        # candidate/bracket search. p_b is NEVER clipped or floored here; the
        # accepted interior-source derivative-floor behavior remains interior
        # authority only (the F0 path via the oracle is untouched), and no
        # bracket enlargement is used to disguise an invalid effective-domain
        # state. Detail carries family/state/z and the offending derivative
        # evidence; iteration is attached by _step.
        if not np.isfinite(p_b) or p_b <= 0.0:
            raise BoundaryHJBFailure(
                "DERIVATIVE_EFFECTIVE_DOMAIN_FAILURE",
                "family '{}' at (j,i)=({},{}): z={}: non-positive effective liquid "
                "marginal p_b={:.6g} (boundary optimizer effective-domain guard, "
                "before candidate/bracket search)".format(family, j, i, nz, p_b),
                {"family": family, "j": j, "i": i, "z": nz, "p_b": float(p_b)},
            )
        net_wage = float(
            cfg.inputs.wages[0] * (1.0 - cfg.inputs.tau - cfg.inputs.migration_costs[0]) * cfg.z[nz]
        )
        if p_b > 0.0 and np.isfinite(p_b):
            l_anchor = float((p_b * net_wage / cfg.inputs.labor_weights[0]) ** (1.0 / cfg.params.phi))
            c_anchor = float(p_b ** (-1.0 / cfg.params.gamma_c))
        else:
            l_anchor = 0.0
            c_anchor = None
        l_values = [l_anchor]
        if l_anchor > 0.0:
            l_values.append(0.0)
        c_hi = 100.0 if c_anchor is None else max(2.0 * cfg.c_floor, c_anchor * 100.0)
        d_wide = cfg.d_wide_min
        expansions = 0
        ra_eff = float(matlab_faithful_illiquid_return(a, cfg.a_max, cfg.inputs.r_a))
        a_eff = max(a, cfg.params.a_bar)
        chi0 = cfg.params.chi_0
        chi1 = cfg.params.chi_1
        vs = V[node, nz]
        zsw = 0.0
        for nz2 in range(self.nz):
            zsw += cfg.switch_matrix[nz, nz2] * (V[node, nz2] - V[node, nz])
        # sector geometry for this state (fixed destinations per family)
        K = 19.0 * cfg.m
        geom: list[tuple[str, int, int, int, int, str]] = []  # (base, d1j, d1i, d2j, d2i, mask_kind)
        if family == "F1":
            geom = [("T_REALLOC", j - 7, i + 10, j - 1, i, "BGE0"),
                    ("R_REVERSE", j + 7, i - 10, j, i - 1, "BLT0AGT0"),
                    ("R_DEPLETE", j - 1, i, j, i - 1, "BLT0ALE0")]
        elif family == "F2":
            if j == 0:
                geom = [("REV", j + 7, i - 10, j, i - 1, "ALL")]
            else:
                geom = [("R_REVERSE", j + 7, i - 10, j, i - 1, "BLT0AGT0"),
                        ("R_DEPLETE", j - 1, i, j, i - 1, "BLT0ALE0")]
        elif family == "F3":
            geom = [("T_REALLOC", j - 7, i + 10, j - 1, i, "BGE0"),
                    ("R_DEPLETE", j - 1, i, j, i - 1, "BLT0ALE0")]
        elif family == "F4":
            geom = [("CASE_B", j - 7, 10, j - 1, 0, "ALL")]
        elif family == "F8":
            geom = [("T_REALLOC", j - 7, i + 10, j - 1, i, "BGE0"),
                    ("R_DEPLETE", j - 1, i, j, i - 1, "BLT0ALE0")]
        elif family == "F9":
            if (j, i) == (g.jmax - 7, 9):
                geom = [("CASE_B", j - 7, i + 10, j - 1, i, "ALL")]
            else:
                geom = [("T_REALLOC", j - 7, 10, j - 1, 0, "ALL")]
        elif family == "F5":
            geom = [("FACE", 1, i, 0, i + 1, "BGE0"), ("FACE", 1, i, 0, i - 1, "BLT0")]
        elif family == "F6":
            geom = [("FACE", j - 1, i, j, i + 1, "BGE0"), ("FACE", j - 1, i, j, i - 1, "BLT0")]
        elif family == "F7":
            geom = [("FACE", j + 1, 0, j, 1, "AGE0"), ("FACE", j - 1, 0, j, 1, "ALT0")]
        elif family == "F10":
            geom = [("FACE", 1, 0, 0, 1, "ALL")]
        elif family == "F11":
            geom = [("FACE", j - 1, 0, j, 1, "ALL")]
        # defensive representability of fixed sector destinations
        for _, d1j, d1i, d2j, d2i, _ in geom:
            if g.node_of.get((d1j, d1i)) is None or g.node_of.get((d2j, d2i)) is None:
                raise BoundaryHJBFailure(
                    "REPRESENTATION_FAILURE",
                    f"family {family!r} at (j,i)=({j},{i}): sector destination not represented",
                )
        while True:
            D_all: list[float] = []
            C_all: list[float] = []
            L_all: list[float] = []
            rank_all: list[int] = []
            for l in l_values:
                LI = net_wage * l
                dlo, dhi = self._d_feasible_interval(family, j, i, a, b, LI)
                lo = min(dlo, -d_wide)
                hi = max(dhi, d_wide)
                d_grid = self._grid_lin(lo, hi, cfg.n_d_grid,
                                        extra=[0.0] if lo < 0.0 < hi else None)
                S = LI + cfg.inputs.r_b * b
                for d in d_grid:
                    chi_d = chi0 * abs(d) + 0.5 * chi1 * d * d / a_eff
                    c_min = ra_eff * a + S - chi_d      # mu_W <= 0 bound
                    c_max = S - d - chi_d               # mu_b >= 0 bound
                    if family in ("F4", "F7", "F9", "F10", "F11"):
                        c_lo_d = max(cfg.c_floor, c_min) if family in ("F4", "F9") else cfg.c_floor
                        c_hi_d = min(c_max, c_hi)
                        if c_hi_d < c_lo_d:
                            continue
                        c_vals = self._grid_lin(c_lo_d, c_hi_d, cfg.n_c_grid,
                                                extra=[c_anchor] if c_anchor is not None else None)
                    elif family == "F2":
                        if j == 0:
                            c_lo_d = max(cfg.c_floor, c_min)
                            c_vals = self._grid_lin(c_lo_d, c_hi, cfg.n_c_grid,
                                                    extra=[c_anchor] if c_anchor is not None else None)
                        else:
                            c_lo_d = max(cfg.c_floor, c_min, c_max)
                            c_vals = self._grid_lin(c_lo_d, c_hi, cfg.n_c_grid,
                                                    extra=[c_anchor] if c_anchor is not None else None)
                    else:  # F1, F3, F8 mixed mu_b sign: split at c_max
                        c_lo_d = max(cfg.c_floor, c_min)
                        half = max(2, cfg.n_c_grid // 2)
                        upper = self._grid_lin(max(c_lo_d, c_max), c_hi, cfg.n_c_grid - half)
                        lower = (self._grid_lin(c_lo_d, min(c_max, c_hi), half)
                                 if min(c_max, c_hi) > c_lo_d else [])
                        c_vals = lower + upper
                        if c_anchor is not None and c_lo_d <= c_anchor <= c_hi and \
                                not any(abs(c_anchor - v) <= 1.0e-12 for v in c_vals):
                            c_vals.append(c_anchor)
                    for c in c_vals:
                        D_all.append(d)
                        C_all.append(c)
                        L_all.append(l)
            if not D_all:
                raise BoundaryHJBFailure(
                    "DERIVATIVE_EFFECTIVE_DOMAIN_FAILURE",
                    f"family {family!r} at (j,i)=({j},{i}): empty candidate set",
                )
            D = np.asarray(D_all, dtype=float)
            C = np.asarray(C_all, dtype=float)
            L = np.asarray(L_all, dtype=float)
            chi = chi0 * np.abs(D) + 0.5 * chi1 * D * D / a_eff
            mu_a = ra_eff * a + D
            mu_b = cfg.inputs.r_b * b + net_wage * L - D - chi - C
            mu_w = mu_a + mu_b
            ad = np.array([
                drift_admissible(g, family, j, i, float(ma), float(mb), cfg.drift_tolerance)
                for ma, mb in zip(mu_a, mu_b)
            ], dtype=bool)
            # utility: u(c) - v(l) (single province)
            gamma = cfg.params.gamma_c
            util = np.where(gamma == 1.0, np.log(C),
                            C ** (1.0 - gamma) / (1.0 - gamma))
            v_l = cfg.inputs.labor_weights[0] * L ** (1.0 + cfg.params.phi) / (1.0 + cfg.params.phi)
            score = util - v_l + zsw
            sector_of = np.empty(len(D), dtype=object)
            geom_masks: list[np.ndarray] = []
            for base, d1j, d1i, d2j, d2i, mask_kind in geom:
                if mask_kind == "ALL":
                    m = np.ones(len(D), dtype=bool)
                elif mask_kind == "BGE0":
                    m = mu_b >= -cfg.drift_tolerance
                elif mask_kind == "BLT0":
                    m = mu_b < -cfg.drift_tolerance
                elif mask_kind == "BLT0AGT0":
                    m = (mu_b < -cfg.drift_tolerance) & (mu_a > cfg.drift_tolerance)
                elif mask_kind == "BLT0ALE0":
                    m = (mu_b < -cfg.drift_tolerance) & (mu_a <= cfg.drift_tolerance)
                elif mask_kind == "AGE0":
                    m = mu_a >= -cfg.drift_tolerance
                elif mask_kind == "ALT0":
                    m = mu_a < -cfg.drift_tolerance
                else:
                    raise RuntimeError(mask_kind)
                geom_masks.append(m)
                if base == "T_REALLOC":
                    q1 = K * mu_b / 70.0
                    q2 = K * (-mu_w) / 10.0
                elif base == "R_REVERSE":
                    q1 = K * mu_a / 70.0
                    q2 = K * (-mu_w) / 7.0
                elif base == "R_DEPLETE":
                    q1 = K * (-mu_a) / 10.0
                    q2 = K * (-mu_b) / 7.0
                elif base == "REV":
                    q1 = K * mu_a / 70.0
                    q2 = K * (-mu_w) / 7.0
                elif base == "CASE_B":
                    q1 = K * mu_b / 70.0
                    q2 = K * (-mu_w) / 10.0
                elif base == "FACE":
                    # d1 = a-face move, d2 = b move (both entries of the family geometry)
                    if family in ("F5", "F6"):
                        q1 = K * (mu_a if family == "F5" else -mu_a) / 10.0
                        q2 = np.where(mu_b >= -cfg.drift_tolerance, K * mu_b / 7.0, K * (-mu_b) / 7.0)
                    elif family == "F7":
                        q1 = np.where(mu_a >= -cfg.drift_tolerance, K * mu_a / 10.0, K * (-mu_a) / 10.0)
                        q2 = K * mu_b / 7.0
                    else:  # F10, F11
                        q1 = K * (mu_a if family == "F10" else -mu_a) / 10.0
                        q2 = K * mu_b / 7.0
                else:
                    raise RuntimeError(base)
                # FACE: the b-move is q2 with sign split already in q2; mask selects the branch
                if base == "FACE" and family in ("F5", "F6"):
                    if mask_kind == "BGE0":
                        m = m & (mu_b >= -cfg.drift_tolerance)
                    elif mask_kind == "BLT0":
                        m = m & (mu_b < -cfg.drift_tolerance)
                if base == "FACE" and family == "F7":
                    if mask_kind == "AGE0":
                        m = m & (mu_a >= -cfg.drift_tolerance)
                    elif mask_kind == "ALT0":
                        m = m & (mu_a < -cfg.drift_tolerance)
                part = q1 * (V[g.node_of[(d1j, d1i)], nz] - vs) + q2 * (V[g.node_of[(d2j, d2i)], nz] - vs)
                score[m] = score[m] + part[m]
                sector_of[m] = base
            score[~ad] = -np.inf
            score[sector_of == None] = -np.inf  # noqa: E711 — documented exclusion excludes the WHOLE candidate
            valid = np.isfinite(score)
            if not valid.any():
                raise BoundaryHJBFailure(
                    "DERIVATIVE_EFFECTIVE_DOMAIN_FAILURE",
                    f"family {family!r} at (j,i)=({j},{i}): no admissible + representable candidate",
                )
            # exact-tie selection with frozen precedence (sector rank, c, l, d)
            rank_arr = np.array([SECTOR_RANK.get(s, 10**9) for s in sector_of], dtype=int)
            s_max = float(np.max(score[valid]))
            tie = valid & (score == s_max)
            tie_idx = np.flatnonzero(tie)
            chosen = tie_idx[np.lexsort((D[tie_idx], L[tie_idx], C[tie_idx], rank_arr[tie_idx]))[0]]
            c_star = float(C[chosen])
            d_star = float(D[chosen])
            l_star = float(L[chosen])
            # artificial bracket binding (algorithmic bounds only)
            art_bind = (c_star >= c_hi * (1.0 - 1.0e-12)) or (c_star <= cfg.c_floor + 1.0e-12)
            art_bind = art_bind or (abs(d_star) >= d_wide * (1.0 - 1.0e-12))
            if art_bind and expansions < cfg.max_bracket_expansions:
                c_hi = c_hi * cfg.bracket_expand_factor
                d_wide = d_wide * cfg.bracket_expand_factor
                expansions += 1
                continue
            if art_bind:
                raise BoundaryHJBFailure(
                    "OPTIMIZER_SEARCH_FAILURE",
                    f"family {family!r} at (j,i)=({j},{i}) z={nz}: artificial bracket "
                    f"binding after {expansions} expansions",
                )
            # conservative row entries from the selected candidate's own rates
            sname = sector_of[chosen]
            b_idx = int(next(k for k, mk in enumerate(geom_masks) if mk[chosen]))
            _, d1j, d1i, d2j, d2i, _ = geom[b_idx]
            entries: list[tuple[int, float]] = []
            if sname == "T_REALLOC":
                q1 = K * mu_b[chosen] / 70.0
                q2 = K * (-mu_w[chosen]) / 10.0
            elif sname == "R_REVERSE":
                q1 = K * mu_a[chosen] / 70.0
                q2 = K * (-mu_w[chosen]) / 7.0
            elif sname == "R_DEPLETE":
                q1 = K * (-mu_a[chosen]) / 10.0
                q2 = K * (-mu_b[chosen]) / 7.0
            elif sname == "REV":
                q1 = K * mu_a[chosen] / 70.0
                q2 = K * (-mu_w[chosen]) / 7.0
            elif sname == "CASE_B":
                q1 = K * mu_b[chosen] / 70.0
                q2 = K * (-mu_w[chosen]) / 10.0
            elif sname == "FACE":
                if family in ("F5", "F6"):
                    q1 = K * (mu_a[chosen] if family == "F5" else -mu_a[chosen]) / 10.0
                    q2 = K * (mu_b[chosen] if mu_b[chosen] >= -cfg.drift_tolerance else -mu_b[chosen]) / 7.0
                elif family == "F7":
                    q1 = K * (mu_a[chosen] if mu_a[chosen] >= -cfg.drift_tolerance else -mu_a[chosen]) / 10.0
                    q2 = K * mu_b[chosen] / 7.0
                else:
                    q1 = K * (mu_a[chosen] if family == "F10" else -mu_a[chosen]) / 10.0
                    q2 = K * mu_b[chosen] / 7.0
            else:
                raise RuntimeError(sname)
            for (dj, di), q in (((d1j, d1i), float(q1)), ((d2j, d2i), float(q2))):
                    if q < -cfg.drift_tolerance or not np.isfinite(q):
                        raise BoundaryHJBFailure(
                            "REPRESENTATION_FAILURE",
                            f"family {family!r} at (j,i)=({j},{i}): negative/non-finite rate",
                        )
                    if q > 0.0:
                        entries.append((g.node_of[(dj, di)], float(q)))
            # first-moment verification (exact formulas; defensive)
            ma = sum(rate * ((g.j_arr[dn] - j) * self.da) for dn, rate in entries)
            mb = sum(rate * ((g.i_arr[dn] - i) * self.db) for dn, rate in entries)
            if abs(ma - float(mu_a[chosen])) > cfg.first_moment_atol or \
               abs(mb - float(mu_b[chosen])) > cfg.first_moment_atol:
                raise BoundaryHJBFailure(
                    "GENERATOR_CONSERVATION_FAILURE",
                    f"family {family!r} first-moment mismatch at (j,i)=({j},{i})",
                )
            diag = -sum(rate for _, rate in entries)
            util_star = flow_utility(c_star, np.array([l_star]), cfg.inputs, cfg.params)
            # economic binding = at the cone bounds (informational diagnostic)
            econ_bind = False
            for l in l_values:
                dlo_c, dhi_c = self._d_feasible_interval(family, j, i, a, b, net_wage * l)
                if abs(d_star - dlo_c) <= 1.0e-9 or abs(d_star - dhi_c) <= 1.0e-9:
                    econ_bind = True
            return _PolicyRecord(
                family=family, sector=sname, consumption=c_star, labor=l_star,
                transfer=d_star, mu_a=float(mu_a[chosen]), mu_b=float(mu_b[chosen]),
                utility=util_star, row_entries=entries, diagonal=diag,
                artificial_binding=False, economic_binding=econ_bind, expansions=expansions,
                c_lo=0.0, c_hi=c_hi, d_lo=0.0, d_hi=0.0,
            )

    # -- operator / u assembly ------------------------------------------------
    def build_operator_and_u(self, V: np.ndarray, labor0: np.ndarray, transfer_income: float,
                             borrowing_rate_gap: float, final: bool = False,
                             f0_policies: Optional[list[Optional[_PolicyRecord]]] = None,
                             ) -> tuple[sparse.csr_matrix, np.ndarray, dict, list]:
        """Assemble the selected backward operator Q and u vector from V.

        ``final=True`` uses the accepted post-convergence pattern for F0 rows
        (upwind max(mu,0)/step on the converged policies) and re-selected
        conservative rows for boundary families; ``final=False`` uses the
        accepted per-iteration pattern for F0 rows (iteration sc/sdh + mh rates).
        ``f0_policies`` (rows from the last iteration) supplies the converged
        F0 policies for the final recomputation.
        """
        cfg = self.config
        g = self.grid
        rows: list[int] = []
        cols: list[int] = []
        data: list[float] = []
        u = np.zeros(self.state_size)
        policy_records: list[Optional[_PolicyRecord]] = [None] * self.state_size
        families = g.families
        consumption = np.zeros((self.n, self.nz))
        labor = np.zeros((self.n, self.nz))
        transfer = np.zeros((self.n, self.nz))
        mu_a_arr = np.zeros((self.n, self.nz))
        mu_b_arr = np.zeros((self.n, self.nz))
        utility = np.zeros((self.n, self.nz))
        sector_arr = np.empty((self.n, self.nz), dtype=object)
        vb_f, vb_b, va_f, va_b = self.compute_derivatives(V, labor0, transfer_income,
                                                          borrowing_rate_gap)
        for node in range(self.n):
            j, i = int(g.j_arr[node]), int(g.i_arr[node])
            fam = families[node]
            for nz in range(self.nz):
                row = nz * self.n + node
                if fam == "F0":
                    if final and f0_policies is not None and f0_policies[row] is not None:
                        rec = f0_policies[row]
                        a_v = float(g.a_arr[node])
                        b_v = float(g.b_arr[node])
                        z_v = float(cfg.z[nz])
                        mu_a_v, mu_b_v, _ = asset_drifts_matlab_faithful(
                            a_v, b_v, z_v, rec.consumption, np.array([rec.labor]), rec.transfer,
                            cfg.inputs, cfg.params, cfg.a_max,
                        )
                        ab = max(-mu_a_v, 0.0) / self.da
                        af = max(mu_a_v, 0.0) / self.da
                        bb = max(-mu_b_v, 0.0) / self.db
                        bf = max(mu_b_v, 0.0) / self.db
                        neigh = g.neighbors(j, i)
                        entries: list[tuple[int, float]] = []
                        for dn, rate in ((neigh["down"], bb), (neigh["up"], bf),
                                         (neigh["left"], ab), (neigh["right"], af)):
                            if dn is not None and rate != 0.0:
                                entries.append((dn, float(rate)))
                        diag = -(bb + bf + ab + af)
                        for dn, rate in entries:
                            rows.append(row); cols.append(dn); data.append(rate)
                        rows.append(row); cols.append(row); data.append(diag)
                        u[row] = rec.utility
                        rec2 = _PolicyRecord(
                            family="F0", sector="INTERIOR_FINAL", consumption=rec.consumption,
                            labor=rec.labor, transfer=rec.transfer, mu_a=mu_a_v, mu_b=mu_b_v,
                            utility=rec.utility, row_entries=entries, diagonal=diag,
                            artificial_binding=False, economic_binding=False, expansions=0,
                        )
                        consumption[node, nz] = rec.consumption
                        labor[node, nz] = rec.labor
                        transfer[node, nz] = rec.transfer
                        mu_a_arr[node, nz] = mu_a_v
                        mu_b_arr[node, nz] = mu_b_v
                        utility[node, nz] = rec.utility
                        sector_arr[node, nz] = "INTERIOR_FINAL"
                        policy_records[row] = rec2
                        continue
                    policy, entries, diag = self.local_interior_row(
                        node, nz, V, vb_f, vb_b, va_f, va_b, labor0, transfer_income,
                        borrowing_rate_gap,
                    )
                    consumption[node, nz] = policy.consumption
                    labor[node, nz] = policy.labor
                    transfer[node, nz] = policy.transfer
                    mu_a_arr[node, nz] = policy.mu_a
                    mu_b_arr[node, nz] = policy.mu_b
                    utility[node, nz] = policy.utility
                    sector_arr[node, nz] = policy.transfer_label
                    for dn, rate in entries:
                        rows.append(row); cols.append(nz * self.n + dn); data.append(rate)
                    rows.append(row); cols.append(row); data.append(diag)
                    u[row] = policy.utility
                    policy_records[row] = _PolicyRecord(
                        family="F0", sector=policy.transfer_label,
                        consumption=policy.consumption, labor=policy.labor,
                        transfer=policy.transfer, mu_a=policy.mu_a, mu_b=policy.mu_b,
                        utility=policy.utility, row_entries=entries, diagonal=diag,
                        artificial_binding=False, economic_binding=False, expansions=0,
                    )
                else:
                    rec = self._boundary_row(node, nz, V, vb_f, vb_b, va_f, va_b, labor0,
                                             transfer_income, borrowing_rate_gap)
                    consumption[node, nz] = rec.consumption
                    labor[node, nz] = rec.labor
                    transfer[node, nz] = rec.transfer
                    mu_a_arr[node, nz] = rec.mu_a
                    mu_b_arr[node, nz] = rec.mu_b
                    utility[node, nz] = rec.utility
                    sector_arr[node, nz] = rec.sector
                    for dn, rate in rec.row_entries:
                        rows.append(row); cols.append(nz * self.n + dn); data.append(rate)
                    rows.append(row); cols.append(row); data.append(rec.diagonal)
                    u[row] = rec.utility
                    policy_records[row] = rec
        Q = sparse.coo_matrix((data, (rows, cols)), shape=(self.state_size, self.state_size)).tocsr()
        B = sparse.kron(sparse.csr_matrix(cfg.switch_matrix),
                        sparse.eye(self.n, format="csr"), format="csr")
        Q = (Q + B).tocsr()
        diagnostics = {
            "boundary_rows": int(sum(1 for r in policy_records if r is not None and r.family != "F0")),
            "f0_rows": int(sum(1 for r in policy_records if r is not None and r.family == "F0")),
            "total_expansions": int(sum(r.expansions for r in policy_records if r is not None)),
            "artificial_binding": int(sum(
                1 for r in policy_records if r is not None and r.artificial_binding)),
            "economic_binding": int(sum(
                1 for r in policy_records if r is not None and r.economic_binding)),
        }
        return Q, u, diagnostics, policy_records

    # -- HJB iteration ---------------------------------------------------------
    def _step(self, V: np.ndarray, labor0: np.ndarray, transfer_income: float,
              borrowing_rate_gap: float, iteration: int,
              ) -> tuple[np.ndarray, float, list[Optional[_PolicyRecord]]]:
        """One implicit/pseudo-time iteration: build operator from current V,
        solve for the next V. Raises the frozen taxonomy failures with the
        iteration number attached."""
        cfg = self.config
        old = V.copy()
        try:
            Q, u, diag, records = self.build_operator_and_u(
                old, labor0, transfer_income, borrowing_rate_gap, final=False
            )
        except BoundaryHJBFailure as exc:
            if exc.failure_name in ("OPTIMIZER_SEARCH_FAILURE",
                                    "DERIVATIVE_EFFECTIVE_DOMAIN_FAILURE"):
                raise BoundaryHJBFailure(
                    exc.failure_name, exc.message,
                    {"iteration": iteration, **exc.detail},
                ) from exc
            raise
        if not np.isfinite(Q.data).all() or not np.isfinite(u).all():
            raise BoundaryHJBFailure(
                "GENERATOR_CONSERVATION_FAILURE",
                "non-finite operator/u at iteration", {"iteration": iteration},
            )
        matrix = (1.0 / cfg.delta + cfg.params.rho) * sparse.eye(
            self.state_size, format="csr") - Q
        rhs = u + old.ravel(order="F") / cfg.delta
        try:
            v_new = linalg.spsolve(matrix, rhs)
        except Exception as exc:  # pragma: no cover - defensive
            raise BoundaryHJBFailure(
                "HJB_LINEAR_SOLVE_FAILURE",
                f"linear solve raised: {exc!r}", {"iteration": iteration},
            ) from exc
        if v_new.shape != (self.state_size,) or not np.isfinite(v_new).all():
            raise BoundaryHJBFailure(
                "HJB_LINEAR_SOLVE_FAILURE",
                "non-finite solve output", {"iteration": iteration},
            )
        # state vector layout is z-major, node-fastest (row = nz*n + node)
        newV = v_new.reshape((self.n, self.nz), order="F")
        statistic = float(np.max(np.abs(newV - old)))
        return newV, statistic, records

    def _iteration_one_value(self, labor0: np.ndarray, transfer_income: float,
                             borrowing_rate_gap: float) -> np.ndarray:
        """Deterministic iteration-1 value iterate (diagnostic / test helper)."""
        cfg = self.config
        initial = self.build_initial_value(labor0, transfer_income, borrowing_rate_gap)
        V1, _, _ = self._step(initial, labor0, transfer_income, borrowing_rate_gap, 1)
        return V1

    def solve(self, initial_value: np.ndarray, labor0: np.ndarray,
              transfer_income: float = 0.0, borrowing_rate_gap: float = 0.0,
              ) -> BoundaryHJBResult:
        cfg = self.config
        V = np.asarray(initial_value, dtype=float).copy()
        if V.shape != (self.n, self.nz) or not np.isfinite(V).all():
            raise ValueError("initial value must be finite with shape (n_nodes, n_z)")
        last_family_seq: list[str] = []
        switch_history: list[int] = []
        converged = False
        statistic = np.inf
        iterations = 0
        records: list[Optional[_PolicyRecord]] = [None] * self.state_size
        for iteration in range(1, cfg.max_iterations + 1):
            V, statistic, records = self._step(
                V, labor0, transfer_income, borrowing_rate_gap, iteration)
            fam_seq = [r.family if r is not None else "?" for r in records]
            if len(last_family_seq) == self.state_size:
                changes = sum(1 for x, y in zip(last_family_seq, fam_seq) if x != y)
                switch_history.append(changes)
            last_family_seq = fam_seq
            iterations = iteration
            if statistic < cfg.tolerance_iter:
                converged = True
                break
        if not converged:
            raise BoundaryHJBFailure(
                "HJB_NONCONVERGENCE",
                f"iterate change {statistic:.3e} >= tolerance_iter {cfg.tolerance_iter:.3e} "
                f"after {cfg.max_iterations} iterations",
            )
        # post-convergence re-selection from final V (F0 rows use converged policies)
        final_Q, final_u, diag_final, records_final = self.build_operator_and_u(
            V, labor0, transfer_income, borrowing_rate_gap, final=True, f0_policies=records
        )
        R = cfg.params.rho * V.ravel(order="F") - (final_u + final_Q.dot(V.ravel(order="F")))
        bellman_residual = float(np.max(np.abs(R)))
        bellman_pass = bellman_residual <= cfg.tolerance_bellman
        # Q structural diagnostics (boundary rows conservative; F0 accepted rows)
        max_row_sum_boundary = 0.0
        offdiag_min_boundary = 0.0
        lost_diag = 0
        for row in range(self.state_size):
            r = records_final[row]
            if r is None or r.family == "F0":
                continue
            start = final_Q.indptr[row]
            end = final_Q.indptr[row + 1]
            off = [(final_Q.indices[k], final_Q.data[k]) for k in range(start, end)
                   if final_Q.indices[k] != row]
            if off:
                offdiag_min_boundary = min(offdiag_min_boundary, min(v for _, v in off))
            row_sum = final_Q.data[start:end].sum()
            max_row_sum_boundary = max(max_row_sum_boundary, abs(float(row_sum)))
            placed = {c for c, _ in off}
            if len(placed) != len(off):
                lost_diag += 1
        fam_hist: dict[str, int] = {}
        for r in records_final:
            if r is not None:
                fam_hist[r.family] = fam_hist.get(r.family, 0) + 1
        q_structural = {
            "max_abs_row_sum_boundary": max_row_sum_boundary,
            "row_sum_tolerance": cfg.row_sum_tolerance,
            "offdiag_min_boundary": offdiag_min_boundary,
            "lost_diagonal_exits": lost_diag,
            "boundary_row_count": diag_final["boundary_rows"],
            "f0_row_count": diag_final["f0_rows"],
            "family_histogram": fam_hist,
        }
        bracket_diagnostics = {
            "total_expansions": diag_final["total_expansions"],
            "artificial_binding_accepted": diag_final["artificial_binding"],
            "economic_binding_accepted": diag_final["economic_binding"],
        }
        policy_switching = {
            "window": cfg.switching_window,
            "changes_by_iteration": switch_history[-cfg.switching_window:],
        }
        nz = self.nz
        n = self.n
        def _arr(field: str) -> np.ndarray:
            out = np.empty((n, nz))
            for node in range(n):
                for zz in range(nz):
                    r = records_final[zz * n + node]
                    out[node, zz] = np.nan if r is None else float(getattr(r, field))
            return out
        return BoundaryHJBResult(
            value=V, initial_value=np.asarray(initial_value, dtype=float).copy(),
            converged=converged, iterations=iterations, convergence_statistic=statistic,
            families=self.grid.families,
            consumption=_arr("consumption"), labor=_arr("labor"), transfer=_arr("transfer"),
            mu_a=_arr("mu_a"), mu_b=_arr("mu_b"), utility=_arr("utility"),
            sector=np.asarray([(records_final[zz * n + node].sector
                                if records_final[zz * n + node] else "?")
                               for node in range(n) for zz in range(nz)]
                              ).reshape((n, nz), order="C"),
            q_final=final_Q, u_final=final_u,
            bellman_residual=bellman_residual, bellman_norm=cfg.bellman_norm,
            tolerance_bellman=cfg.tolerance_bellman, bellman_pass=bellman_pass,
            q_structural=q_structural, bracket_diagnostics=bracket_diagnostics,
            policy_switching=policy_switching,
            node_j=self.grid.j_arr, node_i=self.grid.i_arr, n_z=nz,
        )

    # -- deterministic initial value (validation instance) ---------------------
    def build_initial_value(self, labor0: np.ndarray, transfer_income: float = 0.0,
                            borrowing_rate_gap: float = 0.0) -> np.ndarray:
        """Utility-based deterministic initial V (accepted fixture construction)."""
        cfg = self.config
        g = self.grid
        V = np.empty((self.n, self.nz))
        for node in range(self.n):
            a = float(g.a_arr[node])
            b = float(g.b_arr[node])
            rb = cfg.inputs.r_b + (borrowing_rate_gap if b < 0.0 else 0.0)
            base = rb * b
            net = (1.0 - cfg.inputs.tau) * cfg.inputs.wages[0]
            for nz in range(self.nz):
                z = float(cfg.z[nz])
                f = lambda l: l ** cfg.params.phi - net * z * (net * z * l + base) ** (-cfg.params.gamma_c)
                l0 = float(brentq(f, 1e-8, 5.0))
                ra = float(matlab_faithful_illiquid_return(a, cfg.a_max, cfg.inputs.r_a))
                c_full = net * z * l0 + base + ra * a
                V[node, nz] = flow_utility(c_full, np.array([l0]), cfg.inputs, cfg.params) / cfg.params.rho
        return V

    def build_labor0(self, transfer_income: float = 0.0,
                     borrowing_rate_gap: float = 0.0) -> np.ndarray:
        """Deterministic baseline labor0 (accepted fixture brentq construction)."""
        cfg = self.config
        g = self.grid
        labor0 = np.empty((self.n, self.nz))
        for node in range(self.n):
            b = float(g.b_arr[node])
            rb = cfg.inputs.r_b + (borrowing_rate_gap if b < 0.0 else 0.0)
            base = rb * b
            net = (1.0 - cfg.inputs.tau) * cfg.inputs.wages[0]
            for nz in range(self.nz):
                z = float(cfg.z[nz])
                f = lambda l: l ** cfg.params.phi - net * z * (net * z * l + base) ** (-cfg.params.gamma_c)
                labor0[node, nz] = float(brentq(f, 1e-8, 5.0))
        return labor0


__all__ = [
    "BoundaryHJBConfig", "BoundaryHJBGrid", "BoundaryHJBSolver", "BoundaryHJBResult",
    "BoundaryHJBFailure", "sector_dispatch", "drift_admissible",
    "FAMILIES", "SECTORS", "SECTOR_RANK", "FAILURE_NAMES",
]
