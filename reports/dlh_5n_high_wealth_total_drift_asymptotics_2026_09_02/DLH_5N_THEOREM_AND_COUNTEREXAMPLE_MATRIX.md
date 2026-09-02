# DLH-5N Phase D — Theorem / Conditional-Theorem / Counterexample Matrix

**Issue #40 Phase D (rev 2).** Builds the matrix of what is provable, what is provable
only under an explicit (unproven) assumption, and whether a source-consistent
asymptotic counterexample family exists. All statements are about the fixed-`a`
liquid tail (`a in [0,10]` fixed, `z in {0.8,1.3}`, `b -> +infinity`), derived only
from the accepted source identities and frozen D0 inputs (read-only). No HJB/grid
run. Rev 2 applies the asymptotic-order corrections of fresh ChatGPT review comment
`5503060588`.

Controlling identity (frozen fixture `transfer_income = 0.0`):

```text
mu_W = r_a_eff(a)*a + r_b*b + labor_income - chi(d,a) - consumption
```

Notation: `q = V_a/V_b - 1`, `T(q) = min(q+chi_0,0) + max(q-chi_0,0)`,
`d = a*T(q)/chi_1`, `chi(d,a) = chi_0|d| + 0.5 chi_1 d^2 / max(a,a_bar)`,
`consumption = V_b^(-1/2)`. The quadratic term of `chi` is `d^2/max(a,a_bar)`, so
**`chi = o(b)` requires `d = o(sqrt(b))`, not merely `d = o(b)`** (a uniform
`T(q) = o(sqrt(b))`, e.g. the simpler bounded-ratio `V_a/V_b = O(1)`, is sufficient).

---

## M1. Provable source facts (no assumptions)

**M1.1** `r_b*b = 0.015*b = O(b)`, strictly positive, `-> +inf`. *(frozen r_b > 0)*

**M1.2** `0 <= r_a_eff(a)*a <= 0.27` for all `a in [0,10]`. *(compact support, taper
frozen; maximum at `a=10`: `0.03*10*(1-0.1) = 0.27`)*

**M1.3** `transfer_income = 0.0` (fixed scalar, region 0) is `O(1)` and
state-independent.

**M1.4** `V_b > 0` wherever the consumption FOC applies.

**M1.5 (no unconditional theorem)** There is **no accepted-authority proof** that
`mu_W < 0` for all large `b`: the terms `consumption`, `labor_income`, `d`, `chi`
are not characterized by accepted authority (Phase C: C4, C8 unidentified).

**M1.6 (remainder order not identified)** Absent explicit tail assumptions, the
b-orders of `labor_income` (= `O(V_b^(1/5))`), `consumption` (= `O(V_b^(-1/2))`),
`d` and `chi` (through `V_a/V_b`) are **NOT_IDENTIFIED_BY_CURRENT_ACCEPTED_AUTHORITY**.
In particular the unconditional remainder `mu_W - r_b*b` is **not** known to be
`O(1) + o(b)`; it can in principle be of any order in `b` through `V_b` and `V_a/V_b`.
Outcome B follows precisely because the remainder is not known to be `o(b)`.

> Status: **PROVABLE** (M1.1-M1.4); **Outcome A not provable** (M1.5);
> **remainder unidentified** (M1.6).

---

## M2. Conditional theorem (general net inwardness condition; sufficient fast-`V_b` case)

**Exact net-condition identity (algebraic, not an assumption).** From the accepted
accounting identity,

```text
mu_W <= -eta*b  <==>  consumption + chi(d,a) - labor_income - transfer_income
                            >= (r_b + eta)*b + r_a_eff(a)*a        (eventually, eta > 0)
```

i.e. `mu_W` is strictly negative with margin `eta` iff the **net** object
`consumption + chi - labor_income - transfer_income` dominates
`r_b*b + r_a_eff(a)*a` with a positive margin. This is an exact rearrangement of the
identity; it is the **general** condition and does **not** reduce to any
`c/b`-criterion without extra assumptions.

**Conditional Theorem (net, general):** If there exist `eta > 0` and `b0 > 0` such
that, uniformly over `a in [0,10]` and `z in {0.8,1.3}`,

```text
consumption + chi(d,a) - labor_income - transfer_income
    >= (r_b + eta)*b + r_a_eff(a)*a        (eventually)
```

then `mu_W <= -eta*b < 0` for all large `b` (strict fixed-`a` liquid-tail
inwardness). The premise is an explicit assumption that is **NOT established** by
current accepted authority (it concerns the HJB solution tail, deferred to Route
N-B); it is not a free theorem.

**Special `c/b` criterion (a special case only).** If one separately assumes
`labor_income = o(b)` and `chi(d,a) = o(b)` (e.g. bounded transfer ratio
`V_a/V_b = O(1)`, which gives `d = O(1)` and `chi = O(1)`, plus `V_b -> 0` so labor
decays) and bounded fixed terms, then the net condition reduces to the asymptotic
consumption-wealth ratio criterion `c/b >= r_b + eta` eventually. This `c/b` form is
**not equivalent to the general net condition** (adjustment cost can itself provide an
`O(b)` or superlinear negative contribution, and labor can provide an `O(b)` or larger
positive contribution) and is **not necessary** in general.

**Sufficient fast-`V_b` inwardness condition (value-derivative form).** Assume
uniformly over accepted `(a,z)`: `V_b = O(b^{-(2+delta)})` for some `delta > 0`
(an upper bound on `V_b`), a bounded transfer ratio `V_a/V_b = O(1)` (so `d = O(1)`,
`chi = O(1)`), and the implied labor decay (so `labor_income -> 0`). Since
`V_b > 0`,

```text
consumption = V_b^(-1/2) = Omega(b^{1 + delta/2}),
```

which grows faster than linearly, so the net condition holds and
`mu_W <= -eta*b < 0` eventually. Note **sufficiency, not necessity**: fast `V_b`
decay is one sufficient route to inwardness; `p = 2` with a large enough linear
consumption coefficient, or sufficiently large adjustment-cost growth, can also make
the tail inward even when consumption is sublinear.

> Status: **PROVABLE AS A CONDITIONAL** — the premises are explicit assumptions not
> established by current accepted authority.

---

## M3. Conditional theorem (sufficient condition for outwardness)

**Statement (Conditional Outwardness / non-mean-reversion):** Assume uniformly over
accepted `(a,z)`:
- `V_b ~ K(a,z) * b^{-p}` with `0 < p < 2` and positive finite uniform coefficient
  bounds, so `consumption = O(b^{p/2}) = o(b)` and
  `labor_income = O(V_b^(1/5)) = o(1)`; and
- `d = o(sqrt(b))`, for which a sufficient transfer-ratio condition is
  `T(V_a/V_b - 1) = o(sqrt(b))`, e.g. the simpler bounded ratio `V_a/V_b = O(1)`
  (giving `d = O(1)`, `chi = O(1)`); this ensures `chi = o(b)`.

Then

```text
mu_W/b -> r_b > 0   (fixed-a liquid tail is OUTWARD; mu_W -> +infinity).
```

The key order facts: `chi = o(b)` follows from `d = o(sqrt(b))` (because of the
quadratic term `d^2/max(a,a_bar)`); **`d = o(b)` alone does NOT give `chi = o(b)`**
(since `d^2 = o(b^2)` only).

> Status: **PROVABLE AS A CONDITIONAL** — valid under explicit unproven assumptions
> about `V_b` and `V_a/V_b`.

---

## M4. Source-consistent asymptotic family (counterexample direction)

**Construction:** choose any positive, increasing (in `b`), concave value function
`V(b,a,z)` on the fixed `a`-support with

```text
V_b ~ K_z(a) * b^{-p},  0 < p < 2,   and   V_a/V_b = O(1)  (e.g. the concrete V_a = 0),
```

and evaluate the accepted formulas pointwise:
`c = V_b^(-1/2)`, `l = (V_b*0.85*z)^(1/5)`, `d = a*T(V_a/V_b-1)/chi_1`,
`chi = 0.1|d| + d^2/max(a,a_bar)`. With `V_a/V_b = O(1)` the transfer ratio is
bounded, so `d = O(1)` and `chi = O(1)` are bounded; then:

- `c = o(b)`, `l/labor_income = o(b)`, `d = O(1)`, `chi = O(1)`; and
- `mu_W/b -> r_b > 0`, i.e. `mu_W -> +infinity > 0`.

This family **satisfies every accepted pointwise control formula and the accepted
drift identity** (no accepted equation is violated), yet produces a non-inward
(`mu_W > 0`) fixed-`a` liquid tail.

**Note on the whole class `V_a/V_b = o(b)`:** it is NOT claimed that every such family
has `chi = o(b)`; only `d = o(sqrt(b))` (or bounded `V_a/V_b = O(1)`) is sufficient
for `chi = o(b)`. The construction above uses the bounded-ratio case explicitly.

**Crucial caveat:** this family is constructed at the **formula level** — it is not
shown to satisfy the full HJB Bellman equation (the accepted model includes the HJB
PDE, not only the pointwise FOCs). Whether an HJB-consistent solution with such a
slow `V_b` decay exists is **UNIDENTIFIED** (it is precisely the Route N-B question).
Therefore M4 is a **conditional / formula-level counterexample**, **not an
established model-level counterexample**, and does **not** justify Outcome C.

---

## M5. Special-case knife-edge (bounded transfer ratio) and the decisive object

Under the special-case assumptions `V_a/V_b = O(1)` (so `d = O(1)`, `chi = O(1)`)
and `labor_income = o(b)`, with `V_b ~ b^{-p}`:

| `p` | `consumption ~ b^{p/2}` | Leading-order `mu_W` | Fixed-`a` liquid tail |
|---|---|---|---|
| `0 < p < 2` | `o(b)` | `r_b*b + O(1)` | OUTWARD (`+inf`) |
| `p = 2` | `O(b)` | `(r_b - c/b)*b` | BORDERLINE (sign = sign(r_b - c/b)) |
| `p > 2` | `Omega(b^{1+delta/2})` | `-inf` | INWARD |

The `p = 2` row is the special-case `c/b` criterion and is **not** the general net
condition (see M2). The mean-reversion hypothesis corresponds to `p = 2` with
`c/b > r_b` (consumption a constant fraction of liquid wealth exceeding the liquid
return). This is the natural conjecture for a constant-return CRRA household, but it
is a conjecture about the HJB solution tail, **not accepted authority**. The decisive
missing object is the tail decay exponent `p` of `V_b` (equivalently the asymptotic
`c/b`), and the tail behavior of `V_a/V_b`.

---

## M6. Uniformity and the two-asset caveat

- **Uniformity is an assumption/proved fact, not automatic from compactness:** `a`
  is compact and `z` is finite, which **helps** but does **not** by itself make
  pointwise asymptotic rates uniform. Where a theorem needs a uniform conclusion
  (M2 net condition, M3 outward condition), the uniform bounds/constants are stated
  explicitly (e.g. `V_b = O(b^{-(2+delta)})` uniformly over `(a,z)`, uniform `K`
  bounds in M3); compactness is **not** used as a substitute for a proved uniformity
  argument (uniform convergence / equicontinuity or another explicit bound).
- **Fixed-`a` vs two-asset theorem:** even a positive M2-type result establishes only
  a fixed-`a` liquid-tail statement. A full two-asset infinite-domain theorem requires
  characterizing both coordinates to infinity and is strictly outside DLH-5N.

---

## Matrix summary

| Row | Statement | Status |
|---|---|---|
| M1 | `r_b*b = O(b)>0`, `r_a_eff*a = O(1)>=0`, `transfer_income = O(1)`; **no unconditional inwardness theorem; remainder order not identified** | PROVABLE |
| M2 | general net inwardness condition (exact identity); sufficient fast-`V_b` case `V_b = O(b^{-(2+delta)})` ⇒ `c = Omega(b^{1+delta/2})`; `c/b` is a special case only | CONDITIONAL THEOREM (premises not established; sufficiency, not necessity) |
| M3 | `mu_W/b -> r_b > 0` under slow `V_b` decay + `d = o(sqrt(b))` (`V_a/V_b = O(1)` or `o(sqrt(b))`) | CONDITIONAL THEOREM (premises not established) |
| M4 | formula-level source-consistent family with bounded transfer ratio, `mu_W -> +inf` | CONDITIONAL COUNTEREXAMPLE (not HJB-verified; Outcome C not justified) |
| M5 | special-case knife-edge `p = 2`, sign = `sign(r_b - c/b)` (bounded transfer, labor `o(b)`) | UNRESOLVED (decisive missing object) |
| M6 | uniformity must be assumed/proved uniformly; fixed-`a` only, not two-asset | META-STATEMENT |

**Conclusion:** the sign of `mu_W` in the fixed-`a` liquid tail is **conditional** on
the (unestablished) tail decay of `V_b` and the tail behavior of `V_a/V_b`; accepted
authority does not determine it, and the unconditional remainder is not identified.
This selects **Outcome B**.
