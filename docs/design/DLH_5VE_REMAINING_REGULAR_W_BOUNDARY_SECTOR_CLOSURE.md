# DLH-5V-E — Remaining Regular W-Boundary Sector Closure (Umbrella Design)

**Issue:** deep-learning-hank #53 (DLH-5V-E) · **Task type:** `SCIENTIFIC_DESIGN__REMAINING_REGULAR_W_BOUNDARY_SECTORS_AND_FULL_REGULAR_SCORING_CLOSURE`
**Branch:** `dsh/issue-53-dlh-5ve-remaining-regular-sector-2026-09-11` · **Activation:** comment `5631685581`
(`DLH_5VE_REMAINING_REGULAR_W_BOUNDARY_SECTOR_CLOSURE_AUTHORIZED`), activation `origin/main` = `72b0b4d7c0a24d7ebeb2f670f9e26ef25f8ba1ee`
**Status:** both remaining regular sectors audited and closed with exact nonnegative contracts; full regular coverage
proved; future global composition frozen (design semantics only) — submitted for fresh ChatGPT review, **NOT
scientific acceptance**. Owner decision: `APPROVE_DLH_5VE_REMAINING_REGULAR_W_BOUNDARY_SECTOR_CLOSURE_GATE`.

## 1. Frozen inputs (accepted — not reopened)

`T_W = {mu_W = mu_a + mu_b <= 0}`; accepted `T_realloc = {mu_a<=0, mu_b>=0, mu_W<=0}` with
`w_in = (-10/19,0)`, `w_T = (-70/19,+70/19)`, `q_in = 19(-mu_W)/10`, `q_T = 19 mu_b/70` (DLH-5V-D).
Remaining: `T_rem = {mu_b<0, mu_W<=0} = R_reverse union R_deplete` with
`R_reverse = {mu_a>0, mu_b<0, mu_W<=0}`, `R_deplete = {mu_a<=0, mu_b<0}`.
Grid: `da=10/19`, `db=7/19`, nodes `10j+7i<=N`; native tangent `10 Delta j + 7 Delta i = 0`;
accepted class formulas `i_t(j)=floor((N-10j)/7)`, `r_j=(N-10j) mod 7`, `r_{j+7}=r_j` (DLH-5V-A).
Declared **regular region** (this closure): recurring regular W-active states with `j >= 7` and `i >= 10`.

## 2. Reverse-reallocation sector (Issue §5) — proved and frozen

- Mirror exact tangent `(Delta j, Delta i) = (+7,-10)`, `w_RT = (+70/19,-70/19)`, transition `(j,i)->(j+7,i-10)`.
- **Destination/path proved**: `10(j+7)+7(i-10)=10j+7i` (same W-index; W preserved exactly); binding condition
  `i >= 10` (lower-b face; upper-a `j+7 <= N/10` follows automatically on the frontier); W-domain membership and
  full straight segment in `D_W` (monotone a/b with W constant, convex domain); no other economic-boundary
  crossing in the declared regular region. Finite deferred band: `i in {0..9}` (b-low/a-high end incl. the
  a-max/b-min joint) — endpoint/joint-boundary object, not a regular failure, not silently clamped.
- **Class preservation proved**: `r_{j+7}=r_j`; `i_t(j+7)=i_t(j)-10`; same top/sub-top offset `k`; destination
  represented iff `i >= 10` and `i <= i_t(j)`; W-active status preserved.
- **Rates proved exact**: `q_RT = 19 mu_a/70`, `q_down = 19 (-mu_W)/7` on `w_RT`, `w_down=(0,-7/19)`;
  first moment `q_RT w_RT + q_down w_down = (mu_a, mu_b)` exact; nonnegative on `R_reverse`;
  `det[w_RT w_down] = -490/361 != 0` (unique, no tie-breaking); equality cases (`mu_a=0`, `mu_W=0`) vanish
  continuously and match adjacent sectors.
- **Scoring frozen**: `H_h^reverse(c,l,d) = u(c)-v(l) + q_RT[V_{s_RT}-V_s] + q_down[V_{s_down}-V_s] + switch_z`,
  rates before maximization; sector-candidate scoring only.

## 3. Both-inward depletion sector (Issue §6) — proved and frozen

- `cone{w_left, w_down} = {mu_a<=0, mu_b<=0} = closure(R_deplete)`; rates
  `q_left = 19(-mu_a)/10`, `q_down = 19(-mu_b)/7` on `w_left=(-10/19,0)`, `w_down=(0,-7/19)`; first moment exact;
  nonnegative on `R_deplete`; `det[w_left w_down] = 70/361 != 0` (unique).
- Destinations `(j-1,i)` (j>=1) and `(j,i-1)` (i>=1) represented throughout the declared regular region;
  endpoint faces deferred.
- Scoring frozen: `H_h^deplete(c,l,d) = u(c)-v(l) + q_left[V_{s_left}-V_s] + q_down[V_{s_down}-V_s] + switch_z`,
  rates before maximization.

## 4. Full regular coverage (Issue §8) — proved

`T_W = T_realloc union R_reverse union R_deplete` (sign-casing on `mu_b`), with explicit boundary ownership
(`B1: mu_b=0` -> T_realloc = depletion limit; `B2: mu_a=0` -> R_deplete = reverse limit; `B3: mu_W=0` sliding ray
consistent with the accepted sliding rate `19|mu_b|/70`; `mu=(0,0)` trivial). Every continuously admissible
regular W-face candidate has **exactly one** applicable sector contract; single-valued scoring; **no omission, no
double counting**. Canonical per-sector bases + unique decompositions + proven boundary identity.

## 5. Future global composition (Issue §9) — frozen (design semantics only)

```
all continuously admissible regular W-boundary candidate controls
 -> exactly one accepted sector-specific rate/scoring contract
 -> each candidate's discrete H_h score BEFORE selection
 -> ONE global argmax over all regular candidates
 -> selected control + its already-defined rates
 -> ONE conservative backward row / generator Q
 -> future KFE consumes exactly Q^T.
```

No sector drop, no independent per-sector optimization. Same-process safeguards (Issue §10) preserved; future
SCC/closed-class/source-free-residual/mass/density/pin gates recorded only. No HJB/KFE solved.

## 6. Interpretation ceiling (Issue §11)

Outcome A establishes only: every recurring **regular** W-frontier tangent-admissible drift sector
(`T_W = {mu_W <= 0}`) now has a coherent nonnegative candidate-control transition/rate/scoring contract, and the
future global regular-sector discrete-Hamiltonian composition is well-defined. It does **not** establish
endpoint/joint-boundary closure (`j in {0..6}` and `i in {0..9}` bands + corners remain deferred), implementation
correctness, numerical `W_max` adequacy, stationary existence/uniqueness, or stationary KFE authorization.

## 7. File map (exact five-file allowlist)

1. This umbrella design document.
2. `reports/dlh_5ve_remaining_regular_sector_2026_09_11/DLH_5VE_AUTHORITY_CAPSULE.md` — authority digest.
3. `reports/dlh_5ve_remaining_regular_sector_2026_09_11/DLH_5VE_REVERSE_REALLOCATION_MIRROR_WIDE_AUDIT.md` — mirror-wide destination/path/class/rate/scoring audit (Issue §4–§5).
4. `reports/dlh_5ve_remaining_regular_sector_2026_09_11/DLH_5VE_BOTH_INWARD_AND_FULL_REGULAR_CLOSURE.md` — both-inward audit (Issue §6), no-double-counting/conservative rows (§7), full coverage (§8), global composition (§9), same-process safeguards (§10).
5. `reports/dlh_5ve_remaining_regular_sector_2026_09_11/DLH_5VE_TERMINAL_AND_FORBIDDEN_CHECK.md` — single terminal (Outcome A) + forbidden-operation check + fresh state report.
