"""DLH-4A two-asset KFE machinery tests (Issue #17).

Verifies the stationary-KFE machinery on a constructed irreducible generator:
mass conservation against the grid measure, non-negativity, uniqueness
(nullity of ``G^T`` equal to one), and the separate ``A_hh``/``B_hh``
aggregates.  The non-uniqueness observed on the reference fixture is a
reported diagnostic (see the execution report), not asserted here.
"""

from __future__ import annotations

import numpy as np

from deep_learning_hank.two_asset.kfe import solve_two_asset_kfe


def _irreducible_two_asset_generator():
    """Small irreducible two-asset chain: b ∈ {-1,0,1}, a ∈ {0,2,5}, z ∈ {0,1}.

    Reflecting boundary rates keep every node connected (single closed class).
    """
    b = np.array([-1.0, 0.0, 1.0])
    a = np.array([0.0, 2.0, 5.0])
    I, J, Nz = 3, 3, 2
    size = I * J * Nz
    rows, cols, vals = [], [], []
    db, da = 1.0, 2.5
    for nz in range(Nz):
        for j in range(J):
            for i in range(I):
                r = nz * I * J + j * I + i
                # rightward flow at rate 0.5 except at the top b node
                if i < I - 1:
                    rows += [r, r]; cols += [r + 1, r]; vals += [0.5, -0.5]
                else:
                    rows += [r]; cols += [r - 1]; vals += [0.5]
                    rows += [r]; cols += [r]; vals += [-0.5]
                # upward flow in a at rate 0.3 except at the top a node
                if j < J - 1:
                    rows += [r, r]; cols += [r + I, r]; vals += [0.3, -0.3]
                else:
                    rows += [r]; cols += [r - I]; vals += [0.3]
                    rows += [r]; cols += [r]; vals += [-0.3]
    # z-switch rate 0.25 both ways
    for nzf in range(Nz):
        for nzt in range(Nz):
            rate = 0.25 if nzf != nzt else -0.25
            base = nzf * I * J
            for r in range(I * J):
                rows.append(base + r)
                cols.append(nzt * I * J + r)
                vals.append(rate)
    return b, a, np.array([0, 1]), _coo(rows, cols, vals, size)


def _coo(rows, cols, vals, size):
    from scipy import sparse

    return sparse.coo_matrix((vals, (rows, cols)), shape=(size, size)).tocsr()


def test_kfe_unique_and_mass_conserving():
    b, a, z, generator = _irreducible_two_asset_generator()
    I, J, Nz = 3, 3, 2
    consumption = np.ones((I, J, Nz))
    labor = np.ones((I, J, Nz))
    kfe = solve_two_asset_kfe(
        generator=generator,
        b_grid=b,
        a_grid=a,
        z_states=z,
        consumption=consumption,
        labor=labor,
        mass_tolerance=1e-10,
        negative_mass_threshold=-1e-12,
    )
    assert kfe.unique
    assert kfe.nullity == 1
    db, da = b[1] - b[0], a[1] - a[0]
    assert abs(kfe.mass_error) <= 1e-10
    assert kfe.minimum_mass >= -1e-12
    assert kfe.negative_mass_count == 0
    assert kfe.nan_inf_count == 0


def test_kfe_aggregates_separate():
    b, a, z, generator = _irreducible_two_asset_generator()
    I, J, Nz = 3, 3, 2
    consumption = np.ones((I, J, Nz))
    labor = np.ones((I, J, Nz))
    kfe = solve_two_asset_kfe(
        generator=generator,
        b_grid=b,
        a_grid=a,
        z_states=z,
        consumption=consumption,
        labor=labor,
        mass_tolerance=1e-10,
        negative_mass_threshold=-1e-12,
    )
    assert np.isfinite(kfe.A_hh) and np.isfinite(kfe.B_hh)
    assert abs(kfe.A_hh - kfe.B_hh) > 1e-12  # separate objects
    assert kfe.A_hh > 0.0
    assert np.isfinite(kfe.L_hh) and np.isfinite(kfe.C_hh)
