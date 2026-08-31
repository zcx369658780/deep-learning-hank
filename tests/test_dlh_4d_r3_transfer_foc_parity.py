"""DLH-4D-R3 (Issue #23) transfer-FOC parity and regression tests.

Issue #23 authorizes the sole narrow repair of the MATLAB-faithful household
oracle: the transfer-FOC handling of non-positive RAW liquid derivatives.  These
tests pin the repaired semantics to the literal MATLAB sources:

- HANK_2ASSETS_HJB.m L124-128: the ``max(Vb, 1e-6)`` derivative floor applies to
  consumption and labor ONLY; the four ``HANK3_FOC`` calls (L137-140) receive
  the RAW ``VbB``/``VbF``.
- HANK3_FOC.m L19: ``d = (min(pa./pb - 1 + chi0, 0) + max(pa./pb - 1 - chi0,
  0)).*a/chi1`` with NO ``pb > 0`` guard and NO floor on ``pb``.
- HANK3_cost.m L22: ``chi0.*abs(d) + chi1.*d.^2/2.*(max(a,a_bar)).^(-1)``
  (unchanged; ``max(a,a_bar)`` floor lives in the cost, not in the FOC).
- HANK_2ASSETS_HJB.m L142-147: ``dh_B``/``dh_F`` are assembled with logical
  masks ``(x>0).*x`` / ``(x<0).*x``, so an Inf/NaN candidate is absorbed by the
  downstream Idh masks as zero-transfer (Idh_0) evidence and is never replaced by
  an invented epsilon floor.

The former Python-only strict-positive raw-liquid-derivative guards are removed;
the exact-zero-denominator path is asserted to be deterministic and IEEE-faithful.
"""

from __future__ import annotations

import math
import warnings

import numpy as np
import pytest

from deep_learning_hank.two_asset import (
    EconomicParams,
    HouseholdInputs,
    adjustment_cost,
    select_matlab_faithful_local_policy,
    transfer_candidate,
)


# ---------------------------------------------------------------------------
# Shared fixture (mirrors the accepted validation fixture:
# VALIDATION_FIXTURE_NOT_CALIBRATION).
# ---------------------------------------------------------------------------
def _params():
    return EconomicParams(0.02, 2.0, 5.0, 0.1, 2.0, 1e-6, 0.0, 0.0)


def _inputs():
    return HouseholdInputs(
        r_a=0.03,
        r_b=0.015,
        tau=0.15,
        wages=np.array([1.0]),
        migration_costs=np.array([0.0]),
        labor_weights=np.array([1.0]),
    )


def _cell():
    """Interior cell at b[10] (positive, so no borrowing-rate gap) and a[10]."""
    grid_b = np.linspace(-2.0, 5.0, 20)
    grid_a = np.linspace(0.0, 10.0, 20)
    db = float(grid_b[1] - grid_b[0])
    da = float(grid_a[1] - grid_a[0])
    return {
        "b": float(grid_b[10]),
        "a": float(grid_a[10]),
        "db": db,
        "da": da,
        "a_max": float(grid_a[-1]),
        "transfer_income": 0.0,
        "gap": 0.01,
    }


def _select(**overrides):
    """Call the production local-policy selector on the interior cell."""
    cell = _cell()
    args = dict(
        a=cell["a"],
        b=cell["b"],
        z=0.8,
        v_a_forward=1.2,
        v_a_backward=1.1,
        v_b_forward=1.0,
        v_b_backward=1.0,
        baseline_labor=1.0,
        transfer_income=cell["transfer_income"],
        borrowing_rate_gap=cell["gap"],
        a_max=cell["a_max"],
        da=cell["da"],
        db=cell["db"],
        at_lower_a=False,
        at_upper_a=False,
        at_lower_b=False,
        at_upper_b=False,
        inputs=_inputs(),
        params=_params(),
    )
    args.update(overrides)
    return select_matlab_faithful_local_policy(**args)


def _literal_transfer(v_a: float, v_b: float, a: float, p: EconomicParams) -> float:
    """Literal MATLAB HANK3_FOC.m L19 formula (no guard, no floor on pb)."""
    q = v_a / v_b - 1.0
    threshold = min(q + p.chi_0, 0.0) + max(q - p.chi_0, 0.0)
    return a * threshold / p.chi_1


# ---------------------------------------------------------------------------
# transfer_candidate parity
# ---------------------------------------------------------------------------
def test_transfer_candidate_matches_literal_matlab_formula_for_finite_vb():
    p = _params()
    for v_a in (-2.0, -0.5, 0.1, 1.5, 3.0):
        for v_b in (-3.0, -1.0, -0.25, 0.5, 1.0, 2.0):
            for a in (0.0, 0.7, 5.0):
                assert transfer_candidate(v_a, v_b, a, p) == _literal_transfer(v_a, v_b, a, p)


def test_transfer_candidate_accepts_finite_negative_vb():
    p = _params()
    # Previously raised "transfer FOC requires finite derivatives and V_b > 0";
    # MATLAB evaluates the literal pa./pb formula with no positivity guard.
    assert transfer_candidate(1.5, -0.5, 5.0, p) == _literal_transfer(1.5, -0.5, 5.0, p)
    assert transfer_candidate(0.3, -2.0, 1.0, p) == _literal_transfer(0.3, -2.0, 1.0, p)
    assert transfer_candidate(-1.5, -0.5, 3.0, p) == _literal_transfer(-1.5, -0.5, 3.0, p)


def test_transfer_candidate_uses_raw_vb_not_derivative_floor():
    p = _params()
    # A positive v_b below the 1e-6 derivative floor is used RAW in the FOC (the
    # floor applies to consumption/labor only, per HANK_2ASSETS_HJB L124-128).
    v_b = 1e-7
    assert transfer_candidate(0.05, v_b, 2.0, p) == _literal_transfer(0.05, v_b, 2.0, p)
    assert transfer_candidate(0.05, v_b, 2.0, p) != _literal_transfer(0.05, 1e-6, 2.0, p)


def test_transfer_candidate_exact_zero_denominator_ieee_deterministic():
    p = _params()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")  # IEEE divide-by-zero / invalid warnings are expected
        pos = transfer_candidate(1.5, 0.0, 5.0, p)
        neg = transfer_candidate(-1.5, 0.0, 5.0, p)
        both = transfer_candidate(0.0, 0.0, 5.0, p)
        pos2 = transfer_candidate(1.5, 0.0, 5.0, p)
        both2 = transfer_candidate(0.0, 0.0, 5.0, p)
    # MATLAB pa./pb with pb == 0: sign(pa) * Inf; 0/0 -> NaN. No invented epsilon.
    assert pos == float("inf") and pos2 == float("inf")
    assert neg == float("-inf")
    assert math.isnan(both) and math.isnan(both2)


def test_transfer_candidate_bare_a_scaling():
    p = _params()
    # The transfer FOC scales by bare a (HANK3_FOC.m L19: .*a/chi1); the
    # max(a, a_bar) floor lives ONLY in the cost (HANK3_cost.m L22).
    a_tiny = 1e-7
    assert transfer_candidate(1.5, 1.0, a_tiny, p) == _literal_transfer(1.5, 1.0, a_tiny, p)
    assert transfer_candidate(1.5, 1.0, a_tiny, p) == a_tiny * 0.4 / p.chi_1
    assert transfer_candidate(1.5, 1.0, 0.0, p) == 0.0


# ---------------------------------------------------------------------------
# select_matlab_faithful_local_policy regression + parity
# ---------------------------------------------------------------------------
def test_negative_vb_select_policy_floored_controls_raw_transfer():
    # Regression: the former guard raised "designated transfer FOCs require
    # positive liquid derivatives" for v_b <= 0.  Issue #23 removes it; the
    # selector must now return a policy with MATLAB-faithful controls.
    cell = _cell()
    p = select_matlab_faithful_local_policy(
        a=cell["a"], b=cell["b"], z=0.8,
        v_a_forward=1.5, v_a_backward=1.1,
        v_b_forward=-0.5, v_b_backward=-0.5,
        baseline_labor=1.0, transfer_income=0.0, borrowing_rate_gap=0.01,
        a_max=cell["a_max"], da=cell["da"], db=cell["db"],
        at_lower_a=False, at_upper_a=False, at_lower_b=False, at_upper_b=False,
        inputs=_inputs(), params=_params(),
    )
    # Consumption/labor use the 1e-6 derivative floor (HANK_2ASSETS_HJB L124-128).
    assert p.consumption == 1000.0  # (1e-6)^(-1/2)
    net_wage = 1.0 * (1.0 - 0.15) * 0.8
    assert p.labor == pytest.approx((1e-6 * net_wage) ** (1.0 / 5.0), rel=1e-15)
    assert p.liquid_label == "B"
    # The transfer uses the RAW negative v_b by the literal MATLAB formula; all
    # four candidates are negative, so d_b selects the backward pair.
    assert p.transfer_label == "B"
    assert p.transfer == _literal_transfer(1.1, -0.5, cell["a"], _params())
    assert np.isfinite(p.transfer)


def test_exact_zero_vb_select_policy_absorbs_as_zero_transfer():
    # v_b == 0.0 makes every transfer candidate +Inf; the MATLAB Idh masks turn
    # that into zero-transfer (Idh_0) evidence, never an invented epsilon floor.
    cell = _cell()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")  # IEEE divide-by-zero / invalid warnings are expected
        p = select_matlab_faithful_local_policy(
            a=cell["a"], b=cell["b"], z=0.8,
            v_a_forward=1.5, v_a_backward=1.5,
            v_b_forward=0.0, v_b_backward=0.0,
            baseline_labor=1.0, transfer_income=0.0, borrowing_rate_gap=0.01,
            a_max=cell["a_max"], da=cell["da"], db=cell["db"],
            at_lower_a=False, at_upper_a=False, at_lower_b=False, at_upper_b=False,
            inputs=_inputs(), params=_params(),
        )
    assert p.transfer_label == "0"
    assert p.transfer == 0.0
    # Controls remain floored-positive (MATLAB L124-128).
    assert p.consumption == 1000.0
    assert p.liquid_label == "B"


def test_positive_vb_select_policy_predecessor_contract():
    # The repair must not alter any positive-v_b behavior: this fixture mirrors
    # the predecessor Issue #18 selector contract exactly.
    cell = _cell()
    p = _select()
    net_wage = 1.0 * (1.0 - 0.15) * 0.8
    assert p.liquid_label == "B"
    assert p.consumption == 1.0  # v_b = 1.0 >= floor -> raw consumption FOC
    assert p.labor == pytest.approx((1.0 * net_wage) ** (1.0 / 5.0), rel=1e-15)
    # Transfer candidate d_bf = literal(1.2, 1.0, a) is the only positive one;
    # d_b selects it exactly as the predecessor ternary did (mask-multiply and
    # ternary coincide for finite values).
    assert p.transfer_label == "B"
    assert p.transfer == _literal_transfer(1.2, 1.0, cell["a"], _params())


# ---------------------------------------------------------------------------
# Unchanged MATLAB-faithful pieces (guard that the repair did not touch them)
# ---------------------------------------------------------------------------
def test_adjustment_cost_preserves_max_a_abar_floor():
    p = _params()
    # HANK3_cost.m L22: chi0*|d| + chi1*d^2/2*(max(a,a_bar))^-1.
    assert adjustment_cost(0.4, 0.05, p) == 0.1 * 0.4 + 0.5 * 2.0 * 0.4**2 / 0.05
    assert adjustment_cost(0.4, 0.0, p) == 0.1 * 0.4 + 0.5 * 2.0 * 0.4**2 / 1e-6
    # The floor lives in the cost scale, not in the bare-a transfer FOC.
    assert adjustment_cost(0.4, 0.05, p) != adjustment_cost(0.4, 1e-6, p)
