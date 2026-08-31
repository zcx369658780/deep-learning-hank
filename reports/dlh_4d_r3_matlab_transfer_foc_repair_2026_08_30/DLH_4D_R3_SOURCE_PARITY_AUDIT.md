# DLH-4D-R3 — MATLAB Transfer-FOC Raw Liquid-Derivative Parity Audit (Phase A)

**Issue:** #23 — DLH-4D-R3: Repair MATLAB-faithful transfer-FOC liquid-derivative semantics and revalidate frozen GE path
**Owner session instruction:** strictly per Issue body and all authoritative comments; only the MATLAB source-proven transfer-FOC raw liquid-derivative fidelity mismatch is authorized for repair.
**Branch:** `dsh/issue-23-dlh-4d-r3-matlab-transfer-foc-repair-2026-08-30` (from fresh `origin/main` `d010d1c`)
**Date:** 2026-08-30
**Status:** PARITY PREMISE CONFIRMED (all five Phase A audit items verified at source level)

---

## 1. Authority and scope

Issue #23 authorizes the **sole narrow exception** to the immutable MATLAB-faithful
household oracle: only the transfer-FOC handling of non-positive **raw** liquid
derivatives may be repaired. Everything else (fixture, GE economics, solver
domains, household/KFE redesign, Option A) is frozen and read-only.

The MATLAB sources and the current Python oracle were read side-by-side at the
exact source level. All four MATLAB source files are byte-verified against the
Issue #23 authority hashes (Section 3), and the pre-repair Python oracle identity
is byte-verified (Section 6).

---

## 2. Files audited

| Role | File |
|---|---|
| MATLAB source | `D:\MatlabProgram\2023年12月2日 多省份神经网络HANK\HANK_2ASSETS_HJB.m` |
| MATLAB source | `D:\MatlabProgram\2023年12月2日 多省份神经网络HANK\HANK3_FOC.m` |
| MATLAB source | `D:\MatlabProgram\2023年12月2日 多省份神经网络HANK\HANK3_cost.m` |
| MATLAB source | `D:\MatlabProgram\2023年12月2日 多省份神经网络HANK\lab_solve2.m` |
| Python oracle (pre-repair) | `src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py` |

---

## 3. MATLAB source integrity (SHA-256, all match Issue #23 authority)

| File | SHA-256 | Match |
|---|---|---|
| `HANK_2ASSETS_HJB.m` | `049136B769560040BC678F828F5D3EC5338DDCAA2090D6BED4E40732F56C3EAE` | ✅ (equals embedded oracle provenance) |
| `HANK3_FOC.m` | `772B7B7BBF528DFDD246BD152B3E3026035012FE50F30DA808C1EE18C0F8463D` | ✅ |
| `HANK3_cost.m` | `3504A74BB2DB9FBEE3B292AB68D758954248643D6A5178E42554E0D4794F9A3C` | ✅ |
| `lab_solve2.m` | `74FD6AE8D76AB50A571831FAB95464AE4FCE919F3E70B660E5ABF6B9C5662C20` | ✅ |

---

## 4. Source-to-source findings (the five Phase A audit items)

### 4.1 MATLAB applies the `1e-6` derivative floor to consumption and labor ONLY
`HANK_2ASSETS_HJB.m` L124–128:

```matlab
C_B = max(VbB/alphac,10^(-6)/alphac).^(-1/ga);   % L124 (alphac = 1)
C_F = max(VbF/alphac,10^(-6)/alphac).^(-1/ga);   % L125
l_B = (max(VbB,10^(-6))*(1-tau)*w.*zzz/alphal).^frisch_l;  % L127 (alphal = 1)
l_F = (max(VbF,10^(-6))*(1-tau)*w.*zzz/alphal).^frisch_l;  % L128
```

The `max(.,1e-6)` floor is applied **inside the consumption and labor FOCs only**.
The Python oracle mirrors this exactly and **unchanged** by the repair:
`vb_b = max(v_b_backward, MATLAB_DERIVATIVE_FLOOR)` (floor constant = `1.0e-6`,
line 153) feeding `consumption_from_vb` / `labor_from_vb`. ✅ **Audit item 1 PASS.**

### 4.2 The four designated transfer-FOC calls receive the RAW `VbB`/`VbF`
`HANK_2ASSETS_HJB.m` L137–140:

```matlab
dhBB = HANK3_FOC(results,CHIh,VahB,VbB,aaah,0);
dhBF = HANK3_FOC(results,CHIh,VahF,VbB,aaah,0);
dhFB = HANK3_FOC(results,CHIh,VahB,VbF,aaah,0);
dhFF = HANK3_FOC(results,CHIh,VahF,VbF,aaah,0);
```

All four calls pass the **raw** `VbB`/`VbF` (not the floored values used for
consumption/labor). The Python oracle passes the raw `v_b_backward`/`v_b_forward`
into the four `transfer_candidate` calls (`d_bb`, `d_bf`, `d_fb`, `d_ff`).
✅ **Audit item 2 PASS.**

### 4.3 `HANK3_FOC.m` has NO `pb > 0` guard and NO floor on `pb`
`HANK3_FOC.m` L19 (domestic transfer):

```matlab
d = (min(pa./pb-1+chi0,0)+max(pa./pb-1-chi0,0)).*a/chi1;
```

`pa./pb` is evaluated directly with **no strict-positivity guard and no `1e-6`
floor on `pb`**. A negative `pb` produces a literal (finite) IEEE ratio; a zero
`pb` produces `±Inf`/`NaN` per IEEE 754. ✅ **Audit item 3 PASS.**

### 4.4 Python added two strict-positive raw-liquid-derivative guards ABSENT from MATLAB
Pre-repair Python oracle contained two Python-only guards that MATLAB does not have:

1. `transfer_candidate` (pre-repair lines 85–91):
   ```python
   if not np.isfinite([v_a, v_b, a]).all() or v_b <= 0:
       raise ValueError("transfer FOC requires finite derivatives and V_b > 0")
   ```
2. `select_matlab_faithful_local_policy` (pre-repair lines 247–248):
   ```python
   if min(v_b_forward, v_b_backward) <= 0.0:
       raise ValueError("designated transfer FOCs require positive liquid derivatives")
   ```

These guards **disprove** the MATLAB-faithful semantics: MATLAB evaluates the raw
`pa./pb` formula for any finite `pb` (including negative) and lets IEEE
`±Inf`/`NaN` flow for `pb == 0`. ✅ **Audit item 4 — MISMATCH CONFIRMED** (this is
the exact mismatch Issue #23 authorizes to repair). The Issue #22 diagnostic
recorded 415 of 452 non-finite candidates terminating with the second guard's
message `designated transfer FOCs require positive liquid derivatives`.

### 4.5 `dh_B`/`dh_F` assembly uses logical masks, not ternaries that clamp NaN
`HANK_2ASSETS_HJB.m` L142–147:

```matlab
dh_B(:,1,:) = (dhBF(:,1,:)>10^(-12)).*dhBF(:,1,:);
dh_B(:,J,:) = (dhBB(:,J,:)<-10^(-12)).*dhBB(:,J,:);
dh_B(1,1,:) = max(dh_B(1,1,:),0);
dh_F(:,1,:) = (dhFF(:,1,:)>10^(-12)).*dhFF(:,1,:);
dh_F(:,J,:) = (dhFB(:,J,:)<-10^(-12)).*dhFB(:,J,:);
```

The `(x>t).*x` logical-mask multiply is IEEE-faithful: `0.*NaN = NaN`, `0.*Inf =
NaN`. The pre-repair Python used `x if x > t else 0.0` ternaries, which clamp
`NaN → 0`. For all-finite candidates the two forms coincide; the difference
matters only for the exact-zero/non-finite denominator path that Issue #23 item 5
requires to preserve fail-closed downstream evidence rather than change economics.
✅ **Audit item 5 PASS — mechanical compatibility edit required and separately
documented (Section 5.3).**

---

## 5. Narrow repair applied (Phase B), with unchanged pieces

### 5.1 `transfer_candidate` (raw-derivative semantics)
Removed the Python-only finiteness/positivity guard. The division is now performed
with `np.float64` so an exact-zero denominator yields the IEEE `±Inf`/`NaN`
exactly as MATLAB `pa./pb` (plain Python float division would raise
`ZeroDivisionError`). Finite negative `v_b` are evaluated by the literal MATLAB
formula. The `1e-6` floor is **not** applied (it belongs to consumption/labor).

### 5.2 `select_matlab_faithful_local_policy` guard removal
Removed the `min(v_b_forward, v_b_backward) <= 0.0` raise. The selector now accepts
finite negative `v_b`, floors only the consumption/labor control inputs
(`max(v_b, 1e-6)`), and evaluates the transfer FOC on the raw `v_b`.

### 5.3 `dh_B`/`dh_F` assembly — mechanical compatibility edit (separately documented)
Changed the four assembly ternaries to IEEE logical-mask multiplication
(`d_b = d_bf*(d_bf > 0.0) + d_bb*(d_bb < 0.0)`, and the boundary-a special cases
`x*(x > tolerance)` / `x*(x < -tolerance)`). This reproduces MATLAB `(x>0).*x`
NaN/Inf semantics for the exact-zero denominator path (item 5 of Phase B
contract). For all-finite candidates the result is bit-identical to the former
ternary (verified by the focused parity tests). This edit is **required by** and
**limited to** the narrow transfer-FOC repair; it does not touch operator
construction, boundary/upwind rates, or the KFE.

### 5.4 Preserved unchanged (guarded by focused tests)
- `max(Vb,1e-6)` consumption/labor floor (HANK_2ASSETS_HJB L124–128).
- Bare-`a` transfer-FOC scaling `.*a/chi1` (HANK3_FOC L19).
- `adjustment_cost(..., max(a,a_bar))` denominator floor (HANK3_cost L22).
- Illiquid-return taper `r_a*(1-0.1*(a/a_max)^9)` (HANK_2ASSETS_HJB L81).
- Boundary/upwind/source-operator construction and contaminated-row stationary KFE.
- `lab_solve2` / baseline-labor semantics (out of scope; no mismatch introduced).

---

## 6. Oracle identity (pre-repair → post-repair)

| | Pre-repair (frozen #20 config) | Post-repair (Issue #23-authorized) |
|---|---|---|
| Git blob | `57e32076f0e11c9a047e1f90f8c2446d4148e457` | `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e` |
| SHA-256 | `276D2244B389D6EDE140DAF8B1F9B0BE1F4AA859368941CED1A12BA8A5831AB8` | `1795718C469FC3B427CAB8E3D5957C133BEAD6EACC9EF0A25A3EDB7211D1A024` |

The frozen Issue #20 validation config retains the pre-repair identity (not
modified, per Issue #23). The GE identity gate therefore now fail-closes with the
exact authorized mismatch; this is expected and is verified by the updated
`test_dlh_4d_ge_equations.py::test_immutable_oracle_identity_detects_issue23_repair`.

---

## 7. Conclusion

All five Phase A audit items pass at source level. The parity premise is
**CONFIRMED**: MATLAB evaluates the transfer FOC on raw `pa./pb` with no
strict-positivity guard, the `1e-6` floor is reserved for consumption/labor, and
the pre-repair Python oracle added two strict-`v_b>0` guards absent from MATLAB.
The authorized narrow repair (Section 5) removes exactly those Python-only guards
and reproduces the IEEE semantics of the MATLAB logical-mask assembly.

Terminal guard if this had failed:
`BLOCKED_DLH_4D_R3_SOURCE_PARITY_PREMISE_NOT_CONFIRMED` — **not triggered.**
