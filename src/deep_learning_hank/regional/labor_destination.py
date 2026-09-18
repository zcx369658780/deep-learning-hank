"""DLH-WL-P1A — offline conditional labor-destination accounting interface.

Issue #74 / ``DLH-WL-P1A``; Owner route ``DLH-WL-V1-20260918``.
Authority marker: ``DLH_WL_P1A_OFFLINE_ACCOUNTING_AND_HOUSEHOLD_REGISTRY_AUTHORIZED``.

Scientific object (first version, Owner approved) — given exogenous origin
outflow shares ``m_i^L`` and given origin labor totals ``ell_i``, learn only the
foreign **conditional destination shares** ``W^L``.  ``m`` and ``ell`` are
inputs, never learned jointly; capital networks, household total labor and
end-to-end parameter learning are explicitly out of scope.

Conventions (binding, ``docs/contracts/DLH_WL_CONDITIONAL_DESTINATION_V1_CURRENT.md``):

- ``i`` is the origin, ``j`` is the destination; every array is indexed
  ``[origin, destination]``.
- ``m_i in [0, 1]`` is the given labor-outflow share of origin ``i``.
- ``ell_i >= 0`` is the given origin labor total (efficiency units; the caller
  owns the population/productivity unit declaration).
- ``W_ii = 0``; ``W_ij >= 0``; for allocation-required rows (``m_i > 0``)
  ``sum_{j != i} W_ij = 1`` over *allowed* foreign destinations.
- ``P_ii = 1 - m_i``; ``P_ij = m_i W_ij`` for ``j != i``.
- ``F_ij = ell_i P_ij`` (full bilateral flows, always retained).
- ``Ldest_j = sum_i F_ij``.
- If destination wages are supplied: ``wbar_i = sum_j P_ij w_j`` and the
  wage-bill identity ``sum_i ell_i wbar_i == sum_j Ldest_j w_j`` must close.

Scope guards implemented here:

- rows with ``m_i = 0`` remain well defined in ``W``/``P``/``F`` but carry **no
  identifiable conditional destination label**; the result reports that with
  ``rows_without_identifiable_target`` instead of fabricating a uniform target;
- a missing/zero-outflow row is never silently converted into a uniform target;
- ``support_mask`` marks structural availability, so an unavailable (structural
  zero) destination can never receive conditional mass; realised zero flow is
  *not* structural unavailability;
- a single region is only the ``m = 0``, ``P = [[1]]`` accounting limit;
- two regions are accounting-only for conditional-choice learning because the
  foreign destination is unique there (reported via ``conditional_choice_identified``);
- validation is fail-closed: invalid input raises before any array is built.

This module is deliberately standalone offline algebra.  It must not import or
trigger the household solver, HJB, KFE, GE, the training framework, MATLAB
bindings or any data download; it must not train a model or pick an
architecture.  Its only runtime dependency is ``numpy``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

__all__ = [
    "LaborDestinationAccountingError",
    "LaborDestinationAccounting",
    "build_labor_destination_accounting",
]

#: absolute tolerance used for share/row-sum validation and identity closure
_SHARE_ATOL = 1e-12
#: relative tolerance used on top of the absolute one
_SHARE_RTOL = 1e-12


class LaborDestinationAccountingError(ValueError):
    """Fail-closed error raised for invalid or inconsistent accounting input.

    Subclasses :class:`ValueError` so callers may catch either the specific
    error or the built-in one.  Distinct ``reason`` prefixes make the failure
    deterministic and machine-classifiable:

    ``DIMENSION_MISMATCH``, ``NON_FINITE``, ``NEGATIVE_MASS``, ``RANGE``,
    ``ILLEGAL_DIAGONAL``, ``ROW_SUM``, ``IMPOSSIBLE_SUPPORT``,
    ``SINGLE_REGION_OUTFLOW``, ``INCONSISTENT_INPUT``.
    """

    def __init__(self, reason: str, message: str) -> None:
        super().__init__(f"[{reason}] {message}")
        self.reason = reason


@dataclass(frozen=True)
class LaborDestinationAccounting:
    """Immutable result of the offline conditional labor-destination accounting.

    All array fields follow the ``[origin, destination]`` convention except the
    per-origin vectors ``m``, ``ell``, ``wbar`` and the per-destination vector
    ``destination_labor``.
    """

    # ---- identity / echoes (contract, units, provenance) ----
    contract_version: str
    units: str | None
    region_count: int

    # ---- given inputs (echoed, never learned) ----
    m: np.ndarray
    ell: np.ndarray
    W: np.ndarray
    destination_wages: np.ndarray | None

    # ---- derived accounting ----
    P: np.ndarray
    F: np.ndarray
    destination_labor: np.ndarray
    destination_wage_bill: np.ndarray | None
    wbar: np.ndarray | None
    total_labor: float

    # ---- masks and diagnostics ----
    support_mask: np.ndarray
    active_row_mask: np.ndarray
    valid_row_mask: np.ndarray
    rows_without_identifiable_target: np.ndarray
    rows_without_foreign_option: np.ndarray
    conditional_choice_identified: bool
    diagnostics: dict[str, Any]


def _as_float_vector(value: Any, name: str) -> np.ndarray:
    try:
        array = np.asarray(value, dtype=np.float64)
    except (TypeError, ValueError) as exc:  # pragma: no cover - numpy message
        raise LaborDestinationAccountingError(
            "INCONSISTENT_INPUT", f"{name} could not be read as a float array: {exc}"
        ) from exc
    if array.ndim != 1:
        raise LaborDestinationAccountingError(
            "DIMENSION_MISMATCH", f"{name} must be one-dimensional, got ndim={array.ndim}"
        )
    if not np.all(np.isfinite(array)):
        raise LaborDestinationAccountingError(
            "NON_FINITE", f"{name} contains non-finite entries"
        )
    return array


def _as_square_matrix(value: Any, name: str, region_count: int) -> np.ndarray:
    try:
        array = np.asarray(value, dtype=np.float64)
    except (TypeError, ValueError) as exc:  # pragma: no cover - numpy message
        raise LaborDestinationAccountingError(
            "INCONSISTENT_INPUT", f"{name} could not be read as a float array: {exc}"
        ) from exc
    if array.ndim != 2:
        raise LaborDestinationAccountingError(
            "DIMENSION_MISMATCH", f"{name} must be two-dimensional, got ndim={array.ndim}"
        )
    if array.shape != (region_count, region_count):
        raise LaborDestinationAccountingError(
            "DIMENSION_MISMATCH",
            f"{name} must have shape ({region_count}, {region_count}) "
            f"[origin, destination], got {array.shape}",
        )
    if not np.all(np.isfinite(array)):
        raise LaborDestinationAccountingError(
            "NON_FINITE", f"{name} contains non-finite entries"
        )
    return array


def _as_support_mask(value: Any, region_count: int) -> np.ndarray:
    if isinstance(value, np.ndarray) and value.dtype == bool:
        mask = value
    elif isinstance(value, np.ndarray) and np.issubdtype(value.dtype, np.number):
        if not np.all(np.isfinite(value.astype(np.float64, copy=False))):
            raise LaborDestinationAccountingError(
                "NON_FINITE", "support_mask contains non-finite entries"
            )
        if not np.all((value == 0) | (value == 1)):
            raise LaborDestinationAccountingError(
                "INCONSISTENT_INPUT", "support_mask must contain only 0/1 or boolean values"
            )
        mask = value.astype(bool)
    else:
        try:
            mask = np.asarray(value, dtype=bool)
        except (TypeError, ValueError) as exc:  # pragma: no cover - numpy message
            raise LaborDestinationAccountingError(
                "INCONSISTENT_INPUT", f"support_mask could not be read as boolean: {exc}"
            ) from exc
    if mask.ndim != 2 or mask.shape != (region_count, region_count):
        raise LaborDestinationAccountingError(
            "DIMENSION_MISMATCH",
            f"support_mask must have shape ({region_count}, {region_count}), got {mask.shape}",
        )
    return np.array(mask, dtype=bool, copy=True)


def build_labor_destination_accounting(
    m: Any,
    ell: Any,
    W: Any,
    *,
    support_mask: Any | None = None,
    destination_wages: Any | None = None,
    contract_version: str = "DLH-WL-V1-20260918/WL-CONDITIONAL-DESTINATION-V1.0",
    units: str | None = None,
) -> LaborDestinationAccounting:
    """Build the offline conditional labor-destination accounting.

    Parameters
    ----------
    m :
        Given origin labor-outflow shares, shape ``(n,)``, values in ``[0, 1]``.
        Not a learning target.
    ell :
        Given origin labor totals, shape ``(n,)``, non-negative.  Not a learning
        target; the caller declares the unit via ``units``.
    W :
        Conditional foreign destination shares, shape ``(n, n)``, indexed
        ``[origin, destination]``.  ``W_ii`` must be ``0``; entries must be
        non-negative; every allocation-required row (``m_i > 0``) must sum to
        ``1`` over allowed foreign destinations.
    support_mask :
        Optional boolean ``(n, n)`` structural-availability mask; ``True`` means
        destination ``j`` is structurally available to origin ``i``.  Defaults to
        "every foreign destination available, self unavailable".  Destinations
        marked unavailable are structural zeros: they must receive zero
        conditional mass and are excluded from the row sum.
    destination_wages :
        Optional given destination wage vector, shape ``(n,)``.  When supplied,
        ``wbar`` and the wage-bill identity are produced.
    contract_version, units :
        Provenance strings echoed into the result.  ``units`` is intentionally
        caller-supplied: population counts must not be silently treated as
        efficiency labor.

    Returns
    -------
    LaborDestinationAccounting
        Immutable accounting object with ``W``, ``P``, the full bilateral ``F``,
        destination totals, masks and diagnostics.  Never a bare array.

    Raises
    ------
    LaborDestinationAccountingError
        Fail-closed for dimension mismatch, non-finite values, negative mass,
        out-of-range ``m``, illegal diagonal, invalid row sums, impossible
        support, single-region outflow, or inconsistent inputs.
    """
    m_vec = _as_float_vector(m, "m")
    region_count = int(m_vec.shape[0])
    if region_count == 0:
        raise LaborDestinationAccountingError(
            "DIMENSION_MISMATCH", "m must contain at least one region"
        )

    ell_vec = _as_float_vector(ell, "ell")
    if ell_vec.shape != m_vec.shape:
        raise LaborDestinationAccountingError(
            "DIMENSION_MISMATCH",
            f"ell must match m shape {m_vec.shape}, got {ell_vec.shape}",
        )

    if np.any(m_vec < 0.0) or np.any(m_vec > 1.0):
        raise LaborDestinationAccountingError(
            "RANGE", "m must lie in [0, 1]"
        )
    if np.any(ell_vec < 0.0):
        raise LaborDestinationAccountingError(
            "NEGATIVE_MASS", "ell must be non-negative"
        )

    w_mat = _as_square_matrix(W, "W", region_count)
    if np.any(w_mat < 0.0):
        raise LaborDestinationAccountingError(
            "NEGATIVE_MASS", "W must be non-negative"
        )
    diagonal = np.diag(w_mat)
    if np.any(diagonal != 0.0):
        raise LaborDestinationAccountingError(
            "ILLEGAL_DIAGONAL", "W must have zero diagonal (W_ii = 0)"
        )

    if support_mask is None:
        effective_support = ~np.eye(region_count, dtype=bool)
    else:
        if region_count == 1:
            raise LaborDestinationAccountingError(
                "IMPOSSIBLE_SUPPORT",
                "support_mask is not meaningful with a single region; omit it",
            )
        effective_support = _as_support_mask(support_mask, region_count)
        if np.any(np.diag(effective_support)):
            raise LaborDestinationAccountingError(
                "IMPOSSIBLE_SUPPORT",
                "support_mask must mark the own region as unavailable (diagonal False)",
            )
    if np.any(w_mat[~effective_support] != 0.0):
        raise LaborDestinationAccountingError(
            "IMPOSSIBLE_SUPPORT",
            "W assigns conditional mass to a destination marked structurally unavailable",
        )

    active_rows = m_vec > 0.0
    if region_count == 1 and bool(active_rows[0]):
        raise LaborDestinationAccountingError(
            "SINGLE_REGION_OUTFLOW",
            "a single region admits only the m = 0 limit; m > 0 has no foreign destination",
        )

    available_counts = effective_support.sum(axis=1)
    has_conditional_row = w_mat.sum(axis=1) > 0.0
    valid_rows = active_rows & (available_counts > 0)
    foreign_option_rows = available_counts > 0
    foreign_labor_rows = active_rows & (ell_vec > 0.0) & has_conditional_row

    row_sums = w_mat.sum(axis=1)
    # an allocation-required row must carry conditional mass at all: an all-zero W
    # row is a malformed conditional matrix for m_i > 0, whatever the support says
    zero_mass = active_rows & (row_sums <= 0.0)
    if np.any(zero_mass):
        offending = np.flatnonzero(zero_mass).tolist()
        raise LaborDestinationAccountingError(
            "ROW_SUM", f"allocation-required rows with zero conditional mass: {offending}"
        )
    # a row that allocates foreign labor but has no structurally available foreign
    # destination cannot be routed at all -> fail closed
    impossible = active_rows & (available_counts == 0) & (row_sums > 0.0)
    if np.any(impossible):
        offending = np.flatnonzero(impossible).tolist()
        raise LaborDestinationAccountingError(
            "IMPOSSIBLE_SUPPORT",
            "rows that allocate foreign labor but have no structurally available "
            f"destination: {offending}",
        )
    if not np.allclose(
        row_sums[valid_rows], 1.0, rtol=_SHARE_RTOL, atol=_SHARE_ATOL
    ):
        offending = np.flatnonzero(valid_rows & ~np.isclose(row_sums, 1.0, rtol=_SHARE_RTOL, atol=_SHARE_ATOL)).tolist()
        raise LaborDestinationAccountingError(
            "ROW_SUM",
            "allocation-required rows must sum to 1 over allowed foreign destinations; "
            f"offending origins {offending} with row sums {row_sums[offending].tolist()}",
        )

    if destination_wages is None:
        wages = None
    else:
        wages = _as_float_vector(destination_wages, "destination_wages")
        if wages.shape != m_vec.shape:
            raise LaborDestinationAccountingError(
                "DIMENSION_MISMATCH",
                f"destination_wages must match m shape {m_vec.shape}, got {wages.shape}",
            )

    # ---- derived accounting ----
    # Built element by element so that neither orientation nor row/column
    # broadcasting can be mis-read: P_ii = 1 - m_i and P_ij = m_i * W_ij.
    P = np.zeros((region_count, region_count), dtype=np.float64)
    for i in range(region_count):
        P[i, i] = 1.0 - m_vec[i]
        for j in range(region_count):
            if i != j:
                P[i, j] = m_vec[i] * w_mat[i, j]
    F = np.empty((region_count, region_count), dtype=np.float64)
    destination_labor = np.zeros(region_count, dtype=np.float64)
    for i in range(region_count):
        for j in range(region_count):
            F[i, j] = ell_vec[i] * P[i, j]
            destination_labor[j] += F[i, j]
    total_labor = float(ell_vec.sum())

    wbar = None
    destination_wage_bill = None
    if wages is not None:
        wbar = P @ wages
        destination_wage_bill = destination_labor * wages

    rows_without_foreign_option = ~foreign_option_rows
    rows_without_identifiable_target = ~foreign_labor_rows

    identity = {
        "contract_version": contract_version,
        "units": units,
        "region_count": region_count,
        "orientation": "origin_x_destination",
        "total_labor": total_labor,
        "origin_conservation_max_abs_deviation": float(
            np.max(np.abs(F.sum(axis=1) - ell_vec))
        ),
        "national_conservation_max_abs_deviation": float(abs(float(F.sum()) - total_labor)),
        "destination_aggregation_max_abs_deviation": float(
            np.max(np.abs(F.sum(axis=0) - destination_labor))
        ),
        "own_region_diagonal_max_abs_deviation": float(
            np.max(np.abs(np.diag(F) - (1.0 - m_vec) * ell_vec))
        ),
        "P_foreign_mass_max_abs_deviation": float(
            np.max(np.abs(P.sum(axis=1) - (1.0 - m_vec) - m_vec * w_mat.sum(axis=1)))
        ),
        "support_respected": bool(np.all(w_mat[~effective_support] == 0.0)),
        "active_row_count": int(active_rows.sum()),
        "valid_row_count": int(valid_rows.sum()),
        "foreign_option_row_count": int(foreign_option_rows.sum()),
        "foreign_labor_row_count": int(foreign_labor_rows.sum()),
        "rows_without_identifiable_target": np.flatnonzero(
            rows_without_identifiable_target
        ).tolist(),
        "rows_without_foreign_option": np.flatnonzero(rows_without_foreign_option).tolist(),
        "single_region_limit": bool(region_count == 1),
        "two_region_accounting_only": bool(region_count == 2),
        "n_regions_with_positive_labor": int((ell_vec > 0.0).sum()),
        "n_regions_available_per_origin_min": int(available_counts.min()),
        "n_regions_available_per_origin_max": int(available_counts.max()),
    }

    if wages is not None:
        wage_bill_left = float((ell_vec * wbar).sum())
        wage_bill_right = float((destination_labor * wages).sum())
        identity["wage_bill_left"] = wage_bill_left
        identity["wage_bill_right"] = wage_bill_right
        identity["wage_bill_abs_deviation"] = float(abs(wage_bill_left - wage_bill_right))
        identity["wage_bill_identity_closed"] = bool(
            np.isclose(wage_bill_left, wage_bill_right, rtol=1e-12, atol=1e-12)
        )

    # non-degenerate conditional destination learning needs >= 3 regions; training
    # itself is NOT authorized by Issue #74, so this is a reported gate only.
    conditional_choice_identified = bool(region_count >= 3 and np.any(valid_rows))

    return LaborDestinationAccounting(
        contract_version=contract_version,
        units=units,
        region_count=region_count,
        m=m_vec.copy(),
        ell=ell_vec.copy(),
        W=w_mat.copy(),
        destination_wages=None if wages is None else wages.copy(),
        P=P,
        F=F,
        destination_labor=destination_labor,
        destination_wage_bill=destination_wage_bill,
        wbar=wbar,
        total_labor=total_labor,
        support_mask=effective_support,
        active_row_mask=active_rows,
        valid_row_mask=valid_rows,
        rows_without_identifiable_target=rows_without_identifiable_target,
        rows_without_foreign_option=rows_without_foreign_option,
        conditional_choice_identified=conditional_choice_identified,
        diagnostics=identity,
    )
