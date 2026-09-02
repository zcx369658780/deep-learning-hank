# DLH-5M — State-Constraint Classification (Economic vs Computational)

**Issue #39 §3.** Every current boundary must be classified as structural/economic,
computational truncation, numerical-stabilization/taper-related, or
unresolved/Owner decision. The review must not silently treat a computational
truncation as an economic borrowing/saving constraint.

**Revision (2026-09-02, reviewer comment `5501914968`):** a finite rectangular
state-constraint condition at a computational truncation is distinguished from an
economic asset cap — a numerical state-constraint closure need not be interpreted as
an economic law if its influence is shown to vanish with truncation. The taper effect
is stated precisely (depends only on `a`; does not strengthen as `b`/`W` increases).

Frozen objects (accepted D0): `wbar=1.0`, `r_a=0.03`, `a_max=10`, `b_min=-2.0`
(`b_lo`), `db=7/19`, accepted taper `r_a_eff(a)=r_a*(1-0.1*(a/a_max)^9)`.

---

## Classification table

| Boundary / object | Class | Rationale | Consequence for domain design |
|---|---|---|---|
| `a >= 0` (numerical floor `a_bar = 1e-6`) | **Structural / economic non-negativity** | Illiquid capital cannot be negative; the floor is the numerical representation of `a >= 0`. | Retained in every candidate (R and W). |
| `b >= b_min = -2.0` | **Structural / economic borrowing floor** | A liquidity/borrowing limit is a genuine economic stock constraint (contrast the transfer flow `d`, which is a rate). | Retained in every candidate (R and W). |
| `a <= a_max = 10` | **Computational truncation + modeling normalization anchor (taper)** | No economic reason caps illiquid holdings at 10; `a_max` also serves as the normalization anchor of the accepted illiquid-return taper. Note `r_a_eff(a_max)=0.9*r_a` (taper decays but does not extinguish returns at the cap). | Retained as a separate face in both R and W; its inwardness is enforced by `mu_a <= 0`. |
| `b <= b_max` (route ceiling; b160 = 1075/19) | **Computational truncation (pure)** | No economic reason bars liquid wealth above `b_max`; the outward liquid drift at this face is a truncation response. This face is the object of the DLH-5M review. | Under R it becomes a constrained face (`mu_b <= 0`) — legitimate either as a numerical closure whose influence must be shown to vanish with truncation, or as an economic law only if the Owner accepts the rectangle as the true state domain; under W it is removed and replaced by the (symbolic) joint-wealth cap `a+b <= W_max`, whose activity is unresolved until `W_max` is chosen. |
| accepted `a_max`-normalized illiquid-return taper | **Numerical stabilization / modeling normalization** | Anchors illiquid-return decay on `a`; not a state constraint. Because it depends **only on `a`** and does not strengthen as `b` or `W` increases, it does not stabilize the `b`-face or a `W`-face. | Unchanged in every candidate; cannot substitute for a boundary law on `b` or `W`. |

---

## Why the classification is decisive

1. **The upper-b face is a truncation, not an established economic constraint.**
   Imposing a rectangular tangent-cone law `mu_b <= 0` at `b = b_max` (Design R) is
   legitimate in either of two ways: as a numerical boundary closure at a
   computational truncation whose influence is shown to vanish as the truncation
   recedes, or as an economic law if the Owner accepts the rectangle as the true
   state domain. The accepted evidence establishes **neither** — no truncation-
   vanishing argument exists, and the offenders violate R's componentwise law while
   satisfying total-wealth inwardness.
2. **The accepted evidence separates the two facts:** some high-wealth states violate
   componentwise `mu_b <= 0` (rectangular upper-b condition) while all inspected
   states satisfy `mu_W <= 0` (total-wealth inward). This is evidence *about the
   truncation response*, not a theorem that the rectangle is wrong or right.
3. **`W = a + b` is an accounting coordinate, not yet a production truncation
   variable.** The `d`-cancellation in `mu_W` is a source-accounting fact; whether
   `W` is the correct variable against which to truncate is an economic modeling
   question reserved to the Owner.

The classification therefore does **not** authorize replacing the domain; it
structures the comparison in Sections 2–3 of the design review.

---

## Summary

- Structural/economic: `a >= 0`, `b >= b_min`.
- Computational truncation + modeling anchor: `a <= a_max` (taper-anchored).
- Computational truncation (pure): `b <= b_max`.
- Numerical stabilization: the accepted `a_max`-normalized taper.
- Unresolved/Owner decision: whether the upper-`b` truncation should be retained as a
  constraint (R), replaced by a joint-wealth cap (W), or left unresolved pending
  further theory (U-path).

No boundary is reclassified silently; all four candidate-gate boundaries are
explicitly labeled above.
