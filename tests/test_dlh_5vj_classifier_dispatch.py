"""DLH-5V-J Gate 2: Route-A classifier coverage and sector-dispatch algebra.

Covers (Issue #58 Gate 2):
- exactly one family per represented state over the W_max window sweep
  (N_m = 190..198 and the validation-instance 228);
- exclusive ownership of the F9 cells (19m-7, 9) and (19m, 0) at N_m = 190m;
  F4 at (19m, 0) for 191m..196m; F11 at (19m, 0) for N_m >= 197m;
  F8 sub-top cells (i_t(j) == 10, i = i_t - 1) in the 7..12 band;
- sector dispatch truth table per family: one authorized represented sector or
  a documented 5V-F representability exclusion (whole candidate);
- accepted sector rates and exact first moments sum(q w) == (mu_a, mu_b);
- genuine active-face admissibility laws (no global mu_b >= 0, no budget).
"""

import numpy as np
import pytest

from deep_learning_hank.two_asset.boundary_hjb_selected_q import (
    BoundaryHJBGrid,
    drift_admissible,
    sector_dispatch,
)

M = 1
B_MIN = -2.0
A_MAX = 10.0
TOL = 1e-12
K = 19.0 * M


def grid_for(w_max: float) -> BoundaryHJBGrid:
    return BoundaryHJBGrid(M, w_max, B_MIN, A_MAX)


def test_classifier_single_family_over_window_sweep():
    for k in range(10):
        w_max = 8.0 + k / 19.0 if k < 8 else (10.0 if k == 8 else 9.0)
        if k == 8:
            w_max = 10.0
        if k == 9:
            w_max = 8.0 + 8.0 / 19.0
        g = grid_for(w_max)
        for (j, i) in g.nodes:
            fam = g.classify(j, i)
            assert fam in (
                "F0", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11"
            ), (j, i, fam)
        # family_count == 1: classification is a total single-valued function
        assert len(g.nodes) == len(set(g.node_of)) == g.n_nodes


def test_classifier_windows_and_exclusive_ownership():
    # N_m = 190 at w_max = 8 -> F9 cells (12, 9) and (19, 0)
    g = grid_for(8.0)
    assert g.N_m == 190
    assert g.classify(12, 9) == "F9"
    assert g.classify(19, 0) == "F9"
    # F4 window at (19, 0): N_m in 191..196
    for w in (8.0 + 1 / 19, 8.0 + 6 / 19):
        g = grid_for(w)
        assert 191 <= g.N_m <= 196
        assert g.classify(19, 0) == "F4"
    # F11 at (19, 0): N_m >= 197
    for w in (8.0 + 7 / 19, 8.0 + 8 / 19, 10.0):
        g = grid_for(w)
        assert g.N_m >= 197
        assert g.classify(19, 0) == "F11"
    # F8 sub-top cells: i_t(j) == 10 with i = 9, j in 7..12 (e.g. N_m = 191)
    g = grid_for(8.0 + 1 / 19)
    assert g.i_t[12] == 10
    assert g.classify(12, 9) == "F8"
    assert g.classify(12, 10) == "F1"  # top is F1 (i = 10 >= 10)
    # F2 band (j <= 6) and F3 band (j >= 13) at the validation instance N_m = 228
    g = grid_for(10.0)
    assert g.N_m == 228
    assert g.classify(1, g.i_t[1]) == "F2"
    assert g.classify(6, g.i_t[6]) == "F2"
    assert g.classify(13, g.i_t[13]) == "F3"
    assert g.classify(19, g.i_t[19]) == "F3"
    # corners and faces
    assert g.classify(0, 0) == "F10"
    assert g.classify(19, 0) == "F11"
    assert g.classify(0, 1) == "F5"
    assert g.classify(19, 1) == "F6"
    assert g.classify(1, 0) == "F7"
    assert g.classify(7, g.i_t[7] - 2) == "F0"  # interior non-W below sub-top
    # a_max face law states: F3a only at j = 19 with i >= 1 (W-active)
    assert g.classify(19, g.i_t[19] - 1) in ("F3", "F6")


def test_classifier_validation_instance_histogram():
    # Predeclared family counts at the validation instance (m=1, w_max=10, N_m=228).
    g = grid_for(10.0)
    from collections import Counter

    hist = Counter(g.families.tolist())
    expected = {"F10": 1, "F5": 30, "F2": 14, "F7": 18, "F0": 298,
                "F1": 12, "F3": 14, "F11": 1, "F6": 3}
    assert dict(hist) == expected
    assert sum(hist.values()) == g.n_nodes == 391


# ---------------------------------------------------------------------------
# Sector dispatch truth table (pure algebra; exact first moments)
# ---------------------------------------------------------------------------


def _check_first_moment(g, j, i, mu_a, mu_b, dests):
    ma = sum(q * ((dj - j) * g.da) for (dj, di), q in dests)
    mb = sum(q * ((di - i) * g.db) for (dj, di), q in dests)
    assert abs(ma - mu_a) <= 1e-9, (j, i, mu_a, mu_b, ma)
    assert abs(mb - mu_b) <= 1e-9, (j, i, mu_a, mu_b, mb)


def test_dispatch_f1():
    g = grid_for(10.0)
    # mu_b >= 0 -> T_realloc
    sec, dests = sector_dispatch(g, "F1", 10, 17, -0.1, 0.05)
    assert sec == "T_REALLOC"
    assert dests == [((3, 27), K * 0.05 / 70.0), ((9, 17), K * 0.05 / 10.0)]
    _check_first_moment(g, 10, 17, -0.1, 0.05, dests)
    # mu_b < 0, mu_a > 0 (with mu_w <= 0) -> R_reverse
    sec, dests = sector_dispatch(g, "F1", 10, 17, 0.1, -0.2)
    assert sec == "R_REVERSE"
    assert dests == [((17, 7), K * 0.1 / 70.0), ((10, 16), K * 0.1 / 7.0)]
    _check_first_moment(g, 10, 17, 0.1, -0.2, dests)
    # mu_w > 0 violates the F1 W-face tangent law (inadmissible, not dispatched)
    assert not drift_admissible(g, "F1", 10, 17, 0.1, -0.05)
    # mu_b < 0, mu_a <= 0 -> R_deplete
    sec, dests = sector_dispatch(g, "F1", 10, 17, -0.1, -0.05)
    assert sec == "R_DEPLETE"
    assert dests == [((9, 17), K * 0.1 / 10.0), ((10, 16), K * 0.05 / 7.0)]
    _check_first_moment(g, 10, 17, -0.1, -0.05, dests)
    # zero cases: mu_b == 0 stays T_realloc with q_T == 0; mu_a == 0 -> R_deplete q_left == 0
    sec, dests = sector_dispatch(g, "F1", 10, 17, -0.1, 0.0)
    assert sec == "T_REALLOC" and dests[0][1] == 0.0
    sec, dests = sector_dispatch(g, "F1", 10, 17, 0.0, -0.05)
    assert sec == "R_DEPLETE" and dests[0][1] == 0.0


def test_dispatch_f2():
    g = grid_for(10.0)
    # F2a (j = 0): REV (cone {mu_a >= 0, mu_w <= 0})
    sec, dests = sector_dispatch(g, "F2", 0, 32, 0.1, -0.2)
    assert sec == "REV"
    assert dests == [((7, 22), K * 0.1 / 70.0), ((0, 31), K * 0.1 / 7.0)]
    _check_first_moment(g, 0, 32, 0.1, -0.2, dests)
    assert not drift_admissible(g, "F2", 0, 32, 0.1, -0.05)  # mu_w > 0
    # F2b (j in 1..6): mu_b >= 0 -> documented exclusion (forward T needs j >= 7)
    assert sector_dispatch(g, "F2", 1, 31, -0.1, 0.02) is None
    # F2b: mu_b < 0, mu_a > 0 -> R_reverse
    sec, dests = sector_dispatch(g, "F2", 1, 31, 0.1, -0.05)
    assert sec == "R_REVERSE"
    _check_first_moment(g, 1, 31, 0.1, -0.05, dests)
    # F2b: mu_b < 0, mu_a <= 0 -> R_deplete
    sec, dests = sector_dispatch(g, "F2", 1, 31, -0.1, -0.05)
    assert sec == "R_DEPLETE"
    _check_first_moment(g, 1, 31, -0.1, -0.05, dests)


def test_dispatch_f3():
    g = grid_for(10.0)
    sec, dests = sector_dispatch(g, "F3", 19, 4, -0.1, 0.05)
    assert sec == "T_REALLOC"
    assert dests == [((12, 14), K * 0.05 / 70.0), ((18, 4), K * 0.05 / 10.0)]
    _check_first_moment(g, 19, 4, -0.1, 0.05, dests)
    sec, dests = sector_dispatch(g, "F3", 19, 4, -0.1, -0.05)
    assert sec == "R_DEPLETE"
    _check_first_moment(g, 19, 4, -0.1, -0.05, dests)


def test_dispatch_f4():
    g = grid_for(10.0)
    sec, dests = sector_dispatch(g, "F4", 10, 0, -1.0, 0.5)
    assert sec == "CASE_B"
    assert dests == [((3, 10), K * 0.5 / 70.0), ((9, 0), K * 0.5 / 10.0)]
    _check_first_moment(g, 10, 0, -1.0, 0.5, dests)


def test_dispatch_f8():
    g = grid_for(10.0)
    sec, dests = sector_dispatch(g, "F8", 8, 8, -0.1, 0.02)
    assert sec == "T_REALLOC"
    _check_first_moment(g, 8, 8, -0.1, 0.02, dests)
    sec, dests = sector_dispatch(g, "F8", 8, 8, -0.1, -0.02)
    assert sec == "R_DEPLETE"
    _check_first_moment(g, 8, 8, -0.1, -0.02, dests)
    # mu_a > 0, mu_b < 0 (mu_w <= 0): documented exclusion (R_reverse mirror i >= 10 fails)
    assert sector_dispatch(g, "F8", 8, 8, 0.05, -0.1) is None


def test_dispatch_f9():
    g = grid_for(8.0)  # N_m = 190 -> F9 ownership
    sec, dests = sector_dispatch(g, "F9", 12, 9, -0.5, 0.3)
    assert sec == "CASE_B"
    # q_left = K * (-mu_w) / 10 with mu_w = -0.2
    assert dests == [((5, 19), K * 0.3 / 70.0), ((11, 9), K * 0.2 / 10.0)]
    _check_first_moment(g, 12, 9, -0.5, 0.3, dests)
    sec, dests = sector_dispatch(g, "F9", 19, 0, -0.5, 0.3)
    assert sec == "T_REALLOC"
    assert dests == [((12, 10), K * 0.3 / 70.0), ((18, 0), K * 0.2 / 10.0)]
    _check_first_moment(g, 19, 0, -0.5, 0.3, dests)


def test_dispatch_faces():
    g = grid_for(10.0)
    sec, dests = sector_dispatch(g, "F5", 0, 3, 0.1, 0.05)
    assert sec == "FACE" and dests == [((1, 3), K * 0.1 / 10.0), ((0, 4), K * 0.05 / 7.0)]
    _check_first_moment(g, 0, 3, 0.1, 0.05, dests)
    sec, dests = sector_dispatch(g, "F5", 0, 3, 0.1, -0.05)
    assert sec == "FACE" and dests == [((1, 3), K * 0.1 / 10.0), ((0, 2), K * 0.05 / 7.0)]
    _check_first_moment(g, 0, 3, 0.1, -0.05, dests)
    sec, dests = sector_dispatch(g, "F6", 19, 2, -0.1, 0.05)
    assert sec == "FACE" and dests == [((18, 2), K * 0.1 / 10.0), ((19, 3), K * 0.05 / 7.0)]
    _check_first_moment(g, 19, 2, -0.1, 0.05, dests)
    sec, dests = sector_dispatch(g, "F6", 19, 2, -0.1, -0.05)
    assert sec == "FACE" and dests == [((18, 2), K * 0.1 / 10.0), ((19, 1), K * 0.05 / 7.0)]
    _check_first_moment(g, 19, 2, -0.1, -0.05, dests)
    sec, dests = sector_dispatch(g, "F7", 10, 0, 0.05, 0.1)
    assert sec == "FACE" and dests == [((10, 1), K * 0.1 / 7.0), ((11, 0), K * 0.05 / 10.0)]
    _check_first_moment(g, 10, 0, 0.05, 0.1, dests)
    sec, dests = sector_dispatch(g, "F7", 10, 0, -0.05, 0.1)
    assert sec == "FACE" and dests == [((10, 1), K * 0.1 / 7.0), ((9, 0), K * 0.05 / 10.0)]
    _check_first_moment(g, 10, 0, -0.05, 0.1, dests)
    sec, dests = sector_dispatch(g, "F10", 0, 0, 0.1, 0.05)
    assert sec == "FACE" and dests == [((1, 0), K * 0.1 / 10.0), ((0, 1), K * 0.05 / 7.0)]
    _check_first_moment(g, 0, 0, 0.1, 0.05, dests)
    sec, dests = sector_dispatch(g, "F11", 19, 0, -0.1, 0.05)
    assert sec == "FACE" and dests == [((18, 0), K * 0.1 / 10.0), ((19, 1), K * 0.05 / 7.0)]
    _check_first_moment(g, 19, 0, -0.1, 0.05, dests)


def test_dispatch_exactly_one_or_zero_sectors_per_class():
    """Every admissible drift class maps to exactly one sector (or a documented
    whole-candidate exclusion) — no drift class reaches two sectors."""
    g = grid_for(10.0)
    cases = [
        ("F1", 10, 17), ("F2", 0, 32), ("F2", 1, 31), ("F3", 19, 4), ("F3", 13, 13),
        ("F4", 10, 0), ("F8", 8, 8), ("F5", 0, 3), ("F6", 19, 2), ("F7", 10, 0),
        ("F10", 0, 0), ("F11", 19, 0),
    ]
    for family, j, i in cases:
        for ma in (-0.2, -1e-13, 0.0, 1e-13, 0.2):
            for mb in (-0.2, -1e-13, 0.0, 1e-13, 0.2):
                sec = sector_dispatch(g, family, j, i, ma, mb)
                assert sec is None or sec[0] is not None
                if sec is None:
                    # admissible classes without a sector are ONLY the documented
                    # whole-candidate exclusions (F2b forward-sliding; F3/F8
                    # reverse-sliding obstruction)
                    if drift_admissible(g, family, j, i, ma, mb):
                        assert (family == "F2" and j != 0 and mb >= -1e-12) or \
                               ((family in ("F3", "F8")) and ma > 1e-12 and mb < -1e-12), \
                            (family, (j, i), (ma, mb))
                else:
                    # a usable sector needs nonnegative rates; where a sign-dispatch
                    # would produce a negative rate the drift is inadmissible
                    if min(x[1] for x in sec[1]) < -1e-12:
                        assert not drift_admissible(g, family, j, i, ma, mb), \
                            (family, (j, i), (ma, mb), sec)


def test_drift_admissibility_laws():
    g = grid_for(10.0)
    # F1/F2b/F3b/F8: W-face law mu_w <= 0 only
    assert drift_admissible(g, "F1", 10, 17, 0.1, -0.2)
    assert not drift_admissible(g, "F1", 10, 17, 0.1, -0.05)  # mu_w = +0.05
    assert not drift_admissible(g, "F8", 8, 8, -0.1, 0.2)
    # F3a (j = 19): mu_a <= 0 and mu_w <= 0
    assert drift_admissible(g, "F3", 19, 4, -0.1, -0.05)
    assert not drift_admissible(g, "F3", 19, 4, 0.1, -0.05)
    # F4/F9: mu_b >= 0 and mu_w <= 0 (mu_a <= 0 implied)
    assert drift_admissible(g, "F4", 10, 0, -0.5, 0.1)
    assert not drift_admissible(g, "F4", 10, 0, -0.5, -0.1)
    assert not drift_admissible(g, "F4", 10, 0, 0.5, 0.1)
    # F5/F10: mu_a >= 0
    assert drift_admissible(g, "F5", 0, 3, 0.1, -0.2)
    assert not drift_admissible(g, "F5", 0, 3, -0.1, 0.2)
    # F6/F11: mu_a <= 0
    assert drift_admissible(g, "F6", 19, 2, -0.1, 0.2)
    assert not drift_admissible(g, "F6", 19, 2, 0.1, -0.2)
    # F7: mu_b >= 0
    assert drift_admissible(g, "F7", 10, 0, -0.1, 0.1)
    assert not drift_admissible(g, "F7", 10, 0, 0.1, -0.1)
    # F10: mu_a >= 0 and mu_b >= 0
    assert drift_admissible(g, "F10", 0, 0, 0.1, 0.1)
    assert not drift_admissible(g, "F10", 0, 0, 0.1, -0.1)
    # F11: mu_a <= 0 and mu_b >= 0
    assert drift_admissible(g, "F11", 19, 0, -0.1, 0.1)
    assert not drift_admissible(g, "F11", 19, 0, -0.1, -0.1)


def test_sector_destinations_are_represented():
    """Every dispatched destination of the served classes is a represented node
    (W-index preservation); defensive runtime checks must not trip."""
    g = grid_for(10.0)
    cases = [
        ("F1", 10, 17), ("F2", 0, 32), ("F2", 1, 31), ("F3", 19, 4), ("F3", 13, 13),
        ("F4", 10, 0), ("F5", 0, 3), ("F6", 19, 2), ("F7", 10, 0),
        ("F10", 0, 0), ("F11", 19, 0),
    ]
    drifts = [(-0.1, 0.05), (0.1, -0.05), (-0.1, -0.05)]
    for family, j, i in cases:
        for ma, mb in drifts:
            sec = sector_dispatch(g, family, j, i, ma, mb)
            if sec is None:
                continue
            for (dj, di), _ in sec[1]:
                assert (dj, di) in g.node_of, (family, (j, i), sec[0], (dj, di))
