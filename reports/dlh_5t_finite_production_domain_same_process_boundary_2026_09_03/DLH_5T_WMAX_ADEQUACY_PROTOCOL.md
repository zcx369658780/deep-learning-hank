# DLH-5T — `W_max` Adequacy Protocol (Issue #46, Phase F)

**Design only.** Freezes the future METHOD for selecting a numerical production
domain `W_max`; it does **not** select a number. No execution.

---

## 1. Purpose and scope

`W_max` is a numerical production-domain truncation parameter, not a household
primitive, not a calibrated structural parameter, not an economic wealth ceiling.
Because stationary KFE is not authorized in this Issue, no stationary-based selection
is possible here; DLH-5T freezes the pre-registered nested-domain comparison protocol
that a successor (under separate, later authority) must apply.

## 2. Nested candidate domains (pre-registered)

Freeze a strictly increasing sequence of candidate caps, to be chosen (not here) such
that:

```text
W_max^(1) < W_max^(2) < W_max^(3)
```

Each candidate defines the same geometry `D_W(W_max^(k)) = {0<=a<=a_max, b>=b_min,
a+b<=W_max^(k)}` on the same native lattice resolution family (the lattice `b`-extent
must cover the largest candidate). The future accepted production `W_max` is the
**smallest candidate that passes all applicable accepted adequacy gates**.

The protocol distinguishes the scientific stage of each gate:

| Stage | Class | When applicable |
|---|---|---|
| A | HJB-stage | immediately after a boundary-HJB implementation is separately authorized |
| B | HJB-stage | same gate as A |
| C | KFE-stage | only after stationary KFE is separately authorized |
| D | KFE-stage (aggregates) | after C passes |
| E | GE-stage | only after household stationary validation and two-region authority |

## 3. Stage A — shared-interior policy stability (HJB-stage)

On aligned states common to adjacent candidate domains, compare at least:

```text
c, l, d, mu_a, mu_b, mu_W
```

and selected HJB value/derivative diagnostics. Requirement: the interior policies of
`W_max^(k+1)` restricted to the shared interior agree with those of `W_max^(k)`
within the frozen tolerance family (Section 7), i.e. the truncation does not change
the shared-interior policy.

## 4. Stage B — boundary influence localization (HJB-stage)

Verify that moving `W_max` changes the solution primarily near the artificial `W`
boundary, and that the influence decays to the frozen tolerance on a **pre-defined
common interior region** (registered before the comparison). A candidate whose
influence does not decay on the common interior fails the gate.

## 5. Stage C — stationary-tail influence (future KFE-stage, design only)

After stationary KFE is separately authorized: compare boundary/tail mass near the
`W` face across nested candidates and verify that stationary conclusions
(including any tail quantities) are not boundary dominated. This gate is **design-only
now**; no execution in this Issue.

## 6. Stage D — aggregate stability (future KFE-stage, design only)

After Stage C passes and household stationary validation is separately authorized,
compare at least:

```text
C, L, A, B
```

across accepted nested candidate domains, within the frozen tolerance family.

## 7. Stage E — GE/anchor stability (future downstream stage, design only)

After household stationary validation, compare relevant equilibrium prices/states
across nested candidates, including at minimum regional wages and illiquid returns
(and the two-region fixed-point states when two-region authority is separately
granted).

## 8. Acceptance logic (frozen)

- Each stage has a pre-registered comparison set and a pre-registered tolerance
  family (Section 9).
- A candidate passes a stage only if the comparison is within tolerance.
- The accepted production `W_max` = smallest `W_max^(k)` passing **all applicable**
  accepted gates in order A -> B -> (C -> D -> E when authorized).
- **Do not invent or loosen tolerances merely to obtain PASS.** A tolerance change
  requires an explicit numerical-scaling analysis documented under the relevant
  authority, consistent with the accepted DLH-5D tolerance policy.
- DLH-5T explicitly does not pre-commit a particular tolerance for the future
  HJB-stage beyond requiring pre-registration; the accepted DLH-5D numerical
  tolerances remain the controlling defaults where applicable.

## 9. Pre-registration requirements

The successor gate must pre-register, before any run:

- the nested candidate set `W_max^(1) < W_max^(2) < W_max^(3)` (and the common
  interior region for Stage B);
- the comparison quantities per stage (at least those of Sections 3-7);
- the tolerance family per stage (not loosened from accepted defaults without a
  documented numerical-scaling analysis).

## 10. No-selection statement

No numerical `W_max` is selected in DLH-5T. This protocol is the frozen method; the
number is a successor (later, separately authorized) determination.
