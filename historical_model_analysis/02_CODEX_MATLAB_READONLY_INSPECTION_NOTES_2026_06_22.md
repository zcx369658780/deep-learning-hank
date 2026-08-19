# Matlab Read-Only Inspection Notes

Historical Codex notes recovered from commit `b63d152ca2e6185c6c444b3eb336860928eaa349`.

Inspected files:

- `HANK_2ASSETS_HJB.m`
- `HANK_firm.m`
- `HANK_mp_1eq.m`
- `HANK_mp_1turn.m`

Inspection mode:

- Text read-only.
- No Matlab execution.
- No `.m` file execution.
- No source modification.
- No output generation.

Important observations:

1. `HANK_2ASSETS_HJB.m` includes both the value-function solve and stationary distribution solve. The relevant algorithmic objects are `VbF/VbB`, `VahF/VahB`, `C_F/C_B`, `l_F/l_B`, `dh*`, `BB`, `AAH`, `Bswitch`, `A`, `B`, `AT`, and `g_stacked`.
2. `HANK_firm.m` maps province-level labor and capital supply into output, factor prices, returns, taxes, profits, and government income.
3. `HANK_mp_1turn.m` is where the single-province HJB blocks become a multi-province system through labor allocation, cross-province asset/capital return aggregation, firm updates, wage updates, and nominal/bond-rate updates.
4. `HANK_mp_1eq.m` is an outer fixed-point/convergence controller rather than a separate economic equation block.

Helpers identified as relevant for stronger interpretation:

- `HANK3_FOC.m`
- `HANK3_cost.m`
- `Lt_seperate.m`
- `wage_caculate.m`
- `lab_solve2.m`
- parameter/data-loading scripts for `sigmau_MAT`, distance weights, grids, and province initialization.

New-project disposition: read-only historical reference; no numerical authority.
