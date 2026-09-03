# DLH-5U — Tangential Reallocation and Consistency (Issue #47, Phase 9 + 14)

**Design only.** This report carries the central scientific analysis of Route F:
how the face-adapted finite-volume process transports the DLH-5T admissible
tangential drift on the W frontier, and the precise consistency audit. It states
exactly what is frozen and what remains a bounded unresolved object.

---

## 1. The test object (DLH-5T ambiguity, re-stated)

At the physical W frontier the accepted continuous boundary law admits the tangential
drift

```text
mu_a < 0,  mu_b > 0,  mu_W = mu_a + mu_b <= 0
```

i.e. illiquid assets decrease, liquid assets increase, total wealth `W = a+b` does
not increase. On the W1 masked lattice with `da = 10/19 != db = 7/19` the face tangent
`(1,-1)` is off-axis: the `+b` axial destination of a W-frontier cell may lie outside
the mask. DLH-5T Outcome B established that pure axial node-to-node transitions do
not uniquely preserve this local process. Route F replaces the node-transition
primitive with the clipped-control-volume face-flux primitive.

## 2. Local geometry used by the analysis (symbolic `W_max`)

Use the W-frontier cut cell `s=(i,j)` with the node on the W line
(`a_j + b_i = W_max`); the general (off-line) cut cell follows by continuity of the
face-flux formula. With `da,db` arbitrary (accepted `da=10/19`, `db=7/19`):

- base cell `[a_j-da/2, a_j+da/2] x [b_i-db/2, b_i+db/2]`;
- clipped cell `C_s = {a+b <= W_max} ∩ base`; the W line cuts the `+a`/`+b` corner;
- `-a` face to `(i,j-1)` (length `db`), `-b` face to `(i-1,j)` (length `da`);
- physical W segment `F_s^W` (length `sqrt(2)*db` on the `-a` side, the slanted line);
- `+a` and `+b` neighbors are masked (not represented);
- `omega_s = area(C_s) = (da*db)/2` for the node-on-line cut cell (half-cell).

Cell diagram (projected in the `(a,b)` plane; `z` is an independent finite state):

```text
          b
          ^
    b_i+db|   (masked)   (masked)
          |       o----x      <- W line a+b=W_max
          |      /    / W segment
    b_i+db/2|  /    /  F_s^W
          | /    /
    b_i  s*----x      <- -a face length db  -> (i,j-1)
          |\    \
          | \    \
    b_i-db/2|  \    \
          |   +----+   <- -b face length da -> (i-1,j)
          +----------------------> a
          a_j-da/2   a_j   a_j+da/2
```

## 3. Frozen primary construction: the conservative face-flux cascade

### 3.1 Rates at the cut cell (Phase-4 rule, source-state upwind)

```text
q_{s -> (i,j-1)} = |F_{s,(i,j-1)}| * max(-mu_a,0)/omega_s = db*(-mu_a)/( (da*db)/2 ) = -2 mu_a/da
q_{s -> (i-1,j)} = |F_{s,(i-1,j)}| * max(-mu_b,0)/omega_s = 0            (mu_b > 0)
+a, +b: no represented destination -> no rate assembled (and NOT in the diagonal)
W segment: boundary, no flux (KKT gives max(mu_W,0) = 0)
diagonal: Q[s,s] = -sum(rates) = +2 mu_a/da  (< 0)
```

All off-diagonal rates `>= 0`; row sum exactly `0`. The cut cell's only outflow is
the `-a` (illiquid-down) face; the `+b` (liquid-up) motion is not a rate at `s`
because the `+b` destination is masked.

### 3.2 The local transition sequence (the tangential transport)

The `+b` motion is not suppressed and not reflected: it is **transported inward by the
corner-transport cascade**. Concretely:

```text
step 1: s --(-a face, rate -2 mu_a/da)--> (i,j-1)   [interior cell, full +b face]
step 2: (i,j-1) --(+b face, rate mu_b/db)--> (i+1,j-1)  [in D_W: a_{j-1}+b_{i+1} = W_max - da + db <= W_max]
step 3: continue along the inward chain
```

Net displacement of the two-step composition is `(-da, +db)`, i.e. along `-tau` (the
W-face tangent), reproducing the tangential reallocation (illiquid down, liquid up)
with total wealth conserved to `O(|db-da|)` per step and exactly at `da=db`. The
`+b` inflow into the cut cell from `(i-1,j)` (rate `mu_b/db` at the source cell,
through the `-b` face) supplies the b-up motion; the `-a` outflow is the a-down
motion. The cut cell is a conservative conduit, not a reflector.

### 3.3 Why not suppressed / leaked / reflected / distorted

- **Not suppressed:** the `+b` motion continues at `(i,j-1)` and inward cells; no
  b-motion is dropped (the `+b` rate exists at the interior cells).
- **Not leaked:** row sums are exactly zero; the W segment carries zero flux (KKT
  `mu_W <= 0`); omitted masked destinations are not assembled and not in the diagonal.
- **Not reflected:** no rate redirects the `+b` drift into a `-b` drift; there is no
  `-b` rate induced by the `+b` drift at any cell.
- **Not distorted:** each rate uses only the drift component along its own face
  normal (`mu_a` on a-faces, `mu_b` on b-faces); no cross-term transfers b-motion
  into a-motion at the same cell. The b-motion is *deferred* to the inward cell, not
  *converted* into a-motion.

### 3.4 Refinement consistency of the cascade

At the cut cell the discrete generator is

```text
(Q V)_s = q_{s->(i,j-1)}(V_{(i,j-1)}-V_s) ~ (-2 mu_a/da)(-da dV/da) = 2 mu_a dV/da
```

i.e. pointwise truncation is `O(1)` (a-moment doubled by the half-cell factor `2`,
b-term absent at `s`). This is the standard cut-cell property: the cut band has
`O(h)` thickness, the face FLUXES are first-order consistent, and the global
first-order accuracy holds as `h -> 0`. The local transition **sequence** (Section
3.2) approaches `(mu_a,mu_b)` under refinement: the composed displacement per cycle
tends to the tangential drift and the scheme's flux integral is first-order
consistent with `-div(mu g)` in the divergence form.

## 4. The oblique (diagonal) one-step construction

Route F additionally audited an oblique/diagonal transition `s -> (i+1,j-1)`
(`Delta a = -da`, `Delta b = +db`) that is exactly moment-consistent:

```text
r_diag = mu_b/db              (b-moment: db*r_diag = mu_b)
r_a    = -mu_a/da - mu_b/db   (a-moment: -da*(r_a + r_diag) = mu_a)
```

Then `(Q V)_s ~ mu_a dV/da + mu_b dV/db` exactly (pointwise generator consistency).
Monotonicity requires `r_a >= 0`, i.e.

```text
|mu_a| * db  >=  mu_b * da      <=>      |mu_a|/mu_b >= da/db = (10/19)/(7/19) = 10/7
```

The a-dominant sub-cone `|mu_a| >= (10/7) mu_b` is exactly representable.

## 5. The bounded unresolved object (impossibility for the b-dominant sub-cone)

For the **b-dominant** sub-cone `mu_b <= |mu_a| < (10/7) mu_b` (admissible: `mu_W <= 0`
only requires `|mu_a| >= mu_b`), no one-step monotone pointwise-consistent scheme
exists on the W1 lattice:

- the only represented one-step moves in the needed quadrant are
  `(i,j-1)` `(Delta=-da, 0)` and `(i+1,j-1)` `(Delta=-da, +db)` (and their lattice
  multiples with slope `db/da`), so the achievable generator cone has
  `mu_b/|mu_a| <= db/da = 7/10`;
- any rate assignment giving `(mu_a, mu_b)` in the generator action requires a
  negative rate for `r_a` in the b-dominant case (Section 4), breaking monotonicity;
- the cascade (Section 3) is unconditionally monotone and conservative but is only
  sequence/first-order consistent (Section 3.4), not pointwise-consistent.

**Frozen statement.** Route F is scientifically viable and freezes the conservative
monotone face-flux cascade as the primary discrete process (a specific, implementable
resolution of the DLH-5T non-uniqueness). It additionally freezes the oblique
one-step construction for the a-dominant sub-cone as a documented exact-moment
variant. **One bounded discrete-geometry object remains unresolved:** an
unconditionally monotone, conservative, *pointwise*-generator-consistent tangential
boundary transition covering the full admissible tangential cone (`mu_b <= |mu_a|`)
on the accepted `da != db` grid. This object cannot exist within one-step monotone
schemes on the W1 lattice (Section 5); its resolution would require either a
second-order / higher-moment boundary stencil (a successor implementation-validation
gate), an alternate admissible treatment of the b-dominant sub-cone, or a change to
the lattice geometry (out of scope, would reopen the accepted W1 representation).
This is the **single bounded unresolved object** that triggers the DLH-5U Outcome B
terminal (Phase 17); it is NOT a Route-F failure (no conservation / same-process /
no-flux violation), so Outcome C is not triggered.

## 6. Consistency audit (Issue #47 §14, item by item)

| # | Requirement | Status under frozen scheme |
|---|---|---|
| 14.1 | Markov monotonicity | OK: all rates `>= 0` by `max(.,0)`; oblique variant monotone on a-dominant sub-cone only |
| 14.2 | Conservation (row sums 0) | OK: diagonal `= -sum(assembled rates)`; masked destinations excluded |
| 14.3 | Adjoint mass conservation | OK: `(Q1)=0` implies `d/dt sum p = 0` |
| 14.4 | Local first-moment / drift consistency toward `(mu_a,mu_b)` | Sequence-level OK (Section 3.4); pointwise exact only on a-dominant sub-cone (Section 4); **b-dominant sub-cone pointwise exactness unresolved (Section 5)** |
| 14.5 | Physical W-normal boundary consistency | OK: W segment carries zero flux; KKT `mu_W <= 0` excludes outward flux; no KFE clipping |
| 14.6 | Tangential asset-composition consistency | OK in the sequence limit; no arbitrary b-to-a transfer at any single cell |
| 14.7 | Refinement consistency `h -> 0` | OK first-order global; cut-band pointwise truncation `O(1)` (standard cut-cell property) |
| 14.8 | Interior-operator junction | OK: identical face-flux formula; interior cell is the full-adjacency special case |
| 14.9 | z-switch preservation | OK: accepted finite-state Markov switch combined additively, unchanged |
| 14.10 | Negative-b effective liquid return / borrowing gap | OK: lives in `mu_b` accounting; untouched by Route F |

## 7. Compliance

No generator assembled, no HJB/KFE solved, no execution. The analysis is
symbolic/local analytic only.
