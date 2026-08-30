"""MATLAB-faithful two-asset HA standalone numerical baseline/oracle.

Designated MATLAB source: HANK_2ASSETS_HJB.m
MATLAB SHA-256: 049136B769560040BC678F828F5D3EC5338DDCAA2090D6BED4E40732F56C3EAE
Repository: zcx369658780/dissertation-ch5-two-asset-hank
Export authority: 6469e5a87a00366c1b2af38f27efaa3014206936
Accepted authorities: MATLAB_FAITHFUL_HJB_PROPAGATION_AWARE_PARITY_CONTRACT_ACCEPTED;
MATLAB_PYTHON_TWO_ASSET_HA_FAITHFUL_HJB_OPERATOR_PARITY_ACCEPTED;
MATLAB_PYTHON_TWO_ASSET_HA_FAITHFUL_KFE_DENSITY_PARITY_ACCEPTED;
MATLAB_PYTHON_TWO_ASSET_HA_FAITHFUL_END_TO_END_STATIONARY_DISTRIBUTION_PARITY_ACCEPTED;
MATLAB_PYTHON_TWO_ASSET_HA_FAITHFUL_HOUSEHOLD_AGGREGATE_PARITY_ACCEPTED.

This is a faithful numerical baseline, not a redesigned solver. GE closure and
dynamics are intentionally excluded. Dependencies: Python, NumPy, SciPy only.

MATLAB_FAITHFUL_TRANSFER_FOC_USES_BARE_A
MATLAB_FAITHFUL_ILLIQUID_RETURN_TAPER_IS_REQUIRED_NUMERICAL_STABILIZATION
MATLAB_FAITHFUL_HJB_ITERATION_OPERATOR_FOLLOWS_EXACT_SPDIAGS_BOUNDARY_TRUNCATION
MATLAB_FAITHFUL_HJB_ITERATION_BB_MAY_HAVE_SIGNED_OFFDIAGONALS_AND_NONZERO_BOUNDARY_ROW_SUMS
MATLAB_FAITHFUL_STATIONARY_KFE_CONTAMINATED_ROW_SOLVE_IS_REQUIRED
"""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from scipy import sparse
from scipy.sparse import linalg

@dataclass(frozen=True)
class EconomicParams:
    rho: float
    gamma_c: float
    phi: float
    chi_0: float
    chi_1: float
    a_bar: float
    mu_z: float
    sigma_z: float

    def __post_init__(self) -> None:
        values = np.array(
            [self.rho, self.gamma_c, self.phi, self.chi_0, self.chi_1, self.a_bar, self.mu_z, self.sigma_z]
        )
        if not np.all(np.isfinite(values)):
            raise ValueError("economic parameters must be finite")
        if self.rho <= 0 or self.gamma_c <= 0 or self.phi <= 0:
            raise ValueError("rho, gamma_c, and phi must be positive")
        if self.chi_0 < 0 or self.chi_1 <= 0 or self.a_bar <= 0:
            raise ValueError("adjustment parameters violate the frozen domain")
        if self.mu_z < 0 or self.sigma_z < 0:
            raise ValueError("diffusion parameters must be non-negative")

@dataclass(frozen=True)
class HouseholdInputs:
    r_a: float
    r_b: float
    tau: float
    wages: np.ndarray
    migration_costs: np.ndarray
    labor_weights: np.ndarray

    def __post_init__(self) -> None:
        for name in ("wages", "migration_costs", "labor_weights"):
            array = np.array(getattr(self, name), dtype=float, copy=True)
            if array.ndim != 1 or array.size == 0 or not np.all(np.isfinite(array)):
                raise ValueError(f"{name} must be a non-empty finite vector")
            array.flags.writeable = False
            object.__setattr__(self, name, array)
        if not (self.wages.shape == self.migration_costs.shape == self.labor_weights.shape):
            raise ValueError("province input vectors must share one shape")
        if not np.all(self.wages >= 0) or not np.all(self.labor_weights > 0):
            raise ValueError("wages must be non-negative and labor weights positive")
        if not np.isfinite([self.r_a, self.r_b, self.tau]).all():
            raise ValueError("rates and tax must be finite")
        if np.any(1.0 - self.tau - self.migration_costs < 0.0):
            raise ValueError("after-tax migration wedges must be non-negative")
        effective_wages = self.wages * (1.0 - self.tau - self.migration_costs)
        if not np.any(effective_wages > 0.0):
            raise ValueError("at least one province must have a strictly positive effective wage")

def adjustment_cost(d: np.ndarray | float, a: np.ndarray | float, params: EconomicParams) -> np.ndarray:
    d_array = np.asarray(d, dtype=float)
    scale = np.maximum(np.asarray(a, dtype=float), params.a_bar)
    return params.chi_0 * np.abs(d_array) + 0.5 * params.chi_1 * d_array**2 / scale

def transfer_candidate(v_a: float, v_b: float, a: float, params: EconomicParams) -> float:
    """Return the production MATLAB-faithful bare-a transfer candidate."""
    if not np.isfinite([v_a, v_b, a]).all() or v_b <= 0:
        raise ValueError("transfer FOC requires finite derivatives and V_b > 0")
    q = v_a / v_b - 1.0
    threshold = min(q + params.chi_0, 0.0) + max(q - params.chi_0, 0.0)
    return a * threshold / params.chi_1

def matlab_faithful_illiquid_return(
    a: np.ndarray | float,
    a_max: float,
    r_a: float,
) -> np.ndarray:
    """Apply the designated MATLAB finite-grid illiquid-return taper."""
    a_array = np.asarray(a, dtype=float)
    if not np.all(np.isfinite(a_array)) or not np.isfinite([a_max, r_a]).all():
        raise ValueError("faithful illiquid-return inputs must be finite")
    if a_max <= 0.0:
        raise ValueError("faithful illiquid-return taper requires a_max > 0")
    if np.any(a_array < 0.0) or np.any(a_array > a_max):
        raise ValueError("faithful illiquid-return taper requires 0 <= a <= a_max")
    return r_a * (1.0 - 0.1 * (a_array / a_max) ** 9)

def consumption_from_vb(v_b: float, params: EconomicParams) -> float:
    if not np.isfinite(v_b) or v_b <= 0:
        raise ValueError("consumption FOC requires V_b > 0")
    return float(v_b ** (-1.0 / params.gamma_c))

def labor_from_vb(v_b: float, z: float, inputs: HouseholdInputs, params: EconomicParams) -> np.ndarray:
    if v_b <= 0 or z < 0:
        raise ValueError("labor FOC requires V_b > 0 and z >= 0")
    net_wage = inputs.wages * (1.0 - inputs.tau - inputs.migration_costs) * z
    labor = np.power(v_b * net_wage / inputs.labor_weights, 1.0 / params.phi)
    return np.asarray(labor, dtype=float)

def flow_utility(consumption: float, labor: np.ndarray, inputs: HouseholdInputs, params: EconomicParams) -> float:
    if consumption <= 0 or np.any(labor < 0):
        return -np.inf
    if np.isclose(params.gamma_c, 1.0):
        consumption_utility = np.log(consumption)
    else:
        consumption_utility = consumption ** (1.0 - params.gamma_c) / (1.0 - params.gamma_c)
    disutility = np.sum(inputs.labor_weights * labor ** (1.0 + params.phi) / (1.0 + params.phi))
    return float(consumption_utility - disutility)

def asset_drifts_matlab_faithful(
    a: float,
    b: float,
    z: float,
    consumption: float,
    labor: np.ndarray,
    transfer: float,
    inputs: HouseholdInputs,
    params: EconomicParams,
    a_max: float,
) -> tuple[float, float, float]:
    """Use the MATLAB taper in mu_a while preserving the existing liquid budget."""
    cost = float(adjustment_cost(transfer, a, params))
    labor_income = float(
        np.sum(inputs.wages * (1.0 - inputs.tau - inputs.migration_costs) * z * labor)
    )
    mu_b = inputs.r_b * b + labor_income - transfer - cost - consumption
    r_a_effective = float(matlab_faithful_illiquid_return(a, a_max, inputs.r_a))
    mu_a = r_a_effective * a + transfer
    return mu_a, mu_b, cost

MATLAB_DRIFT_TOLERANCE = 1.0e-12

MATLAB_DERIVATIVE_FLOOR = 1.0e-6

@dataclass(frozen=True)
class MatlabFaithfulLocalPolicy:
    """One cell of the designated MATLAB policy/upwind construction."""

    liquid_label: str
    transfer_label: str
    consumption: float
    labor: float
    transfer: float
    adjustment_cost: float
    effective_illiquid_return: float
    mu_a: float
    mu_b: float
    utility: float
    liquid_direction: str
    illiquid_direction: str
    b_backward_rate: float
    b_forward_rate: float
    a_backward_rate: float
    a_forward_rate: float
    iteration_b_backward_rate: float
    iteration_b_forward_rate: float

def _direction(value: float, tolerance: float) -> str:
    if value > tolerance:
        return "F"
    if value < -tolerance:
        return "B"
    return "0"

def select_matlab_faithful_local_policy(
    *,
    a: float,
    b: float,
    z: float,
    v_a_forward: float,
    v_a_backward: float,
    v_b_forward: float,
    v_b_backward: float,
    baseline_labor: float,
    transfer_income: float,
    borrowing_rate_gap: float,
    a_max: float,
    da: float,
    db: float,
    at_lower_a: bool,
    at_upper_a: bool,
    at_lower_b: bool,
    at_upper_b: bool,
    inputs: HouseholdInputs,
    params: EconomicParams,
    tolerance: float = MATLAB_DRIFT_TOLERANCE,
) -> MatlabFaithfulLocalPolicy:
    """Evaluate MATLAB lines 124--198 and 262--267 for one local cell.

    This is deliberately separate from the corrected/reference candidate and KKT
    selector.  Boundary booleans are explicit because this bounded entry point
    consumes a frozen local case rather than running an HJB grid iteration.
    """
    scalars = np.array(
        [
            a,
            b,
            z,
            v_a_forward,
            v_a_backward,
            v_b_forward,
            v_b_backward,
            baseline_labor,
            transfer_income,
            borrowing_rate_gap,
            a_max,
            da,
            db,
            tolerance,
        ],
        dtype=float,
    )
    if not np.all(np.isfinite(scalars)):
        raise ValueError("faithful local-policy inputs must be finite")
    if inputs.wages.size != 1:
        raise ValueError("designated MATLAB local policy requires one wage/labor type")
    if a < 0.0 or a > a_max or a_max <= 0.0 or da <= 0.0 or db <= 0.0:
        raise ValueError("faithful local-policy state/grid domain is invalid")
    if z <= 0.0 or baseline_labor < 0.0 or tolerance <= 0.0:
        raise ValueError("faithful local-policy productivity/labor/tolerance is invalid")
    if at_lower_a != np.isclose(a, 0.0) or at_upper_a != np.isclose(a, a_max):
        raise ValueError("illiquid boundary flags must match a and a_max")
    if at_lower_a and at_upper_a:
        raise ValueError("faithful local policy requires a nondegenerate illiquid grid")
    if at_lower_b and at_upper_b:
        raise ValueError("faithful local policy requires a nondegenerate liquid grid")
    if min(v_b_forward, v_b_backward) <= 0.0:
        raise ValueError("designated transfer FOCs require positive liquid derivatives")

    effective_r_b = inputs.r_b + (borrowing_rate_gap if b < 0.0 else 0.0)
    local_inputs = HouseholdInputs(
        inputs.r_a,
        effective_r_b,
        inputs.tau,
        inputs.wages,
        inputs.migration_costs,
        inputs.labor_weights,
    )
    vb_b = max(v_b_backward, MATLAB_DERIVATIVE_FLOOR)
    vb_f = max(v_b_forward, MATLAB_DERIVATIVE_FLOOR)
    consumption_b = consumption_from_vb(vb_b, params)
    consumption_f = consumption_from_vb(vb_f, params)
    labor_b = float(labor_from_vb(vb_b, z, local_inputs, params)[0])
    labor_f = float(labor_from_vb(vb_f, z, local_inputs, params)[0])
    net_wage = float(
        local_inputs.wages[0]
        * (1.0 - local_inputs.tau - local_inputs.migration_costs[0])
        * z
    )
    liquid_resources_b = net_wage * labor_b + transfer_income + effective_r_b * b
    liquid_resources_f = net_wage * labor_f + transfer_income + effective_r_b * b
    sc_b = liquid_resources_b - consumption_b
    sc_f = liquid_resources_f - consumption_f
    use_liquid_b = sc_b < -tolerance
    use_liquid_f = sc_f > tolerance and not use_liquid_b
    if use_liquid_b:
        liquid_label = "B"
        consumption = consumption_b
        labor = labor_b
    elif use_liquid_f:
        liquid_label = "F"
        consumption = consumption_f
        labor = labor_f
    else:
        liquid_label = "0"
        labor = baseline_labor
        consumption = net_wage * baseline_labor + transfer_income + effective_r_b * b
    if consumption <= 0.0:
        raise ValueError("MATLAB zero/liquid branch produced non-positive consumption")

    d_bb = transfer_candidate(v_a_backward, v_b_backward, a, params)
    d_bf = transfer_candidate(v_a_forward, v_b_backward, a, params)
    d_fb = transfer_candidate(v_a_backward, v_b_forward, a, params)
    d_ff = transfer_candidate(v_a_forward, v_b_forward, a, params)
    d_b = (d_bf if d_bf > 0.0 else 0.0) + (d_bb if d_bb < 0.0 else 0.0)
    d_f = (d_ff if d_ff > 0.0 else 0.0) + (d_fb if d_fb < 0.0 else 0.0)
    if at_lower_a:
        d_b = d_bf if d_bf > tolerance else 0.0
        d_f = d_ff if d_ff > tolerance else 0.0
        if at_lower_b:
            d_b = max(d_b, 0.0)
    if at_upper_a:
        d_b = d_bb if d_bb < -tolerance else 0.0
        d_f = d_fb if d_fb < -tolerance else 0.0

    sdh_b = -d_b - float(
        # The accepted cost helper retains MATLAB's max(a, a_bar) denominator floor.
        asset_drifts_matlab_faithful(
            a,
            b,
            z,
            0.0,
            np.array([0.0]),
            d_b,
            local_inputs,
            params,
            a_max,
        )[2]
    )
    sdh_f = -d_f - float(
        asset_drifts_matlab_faithful(
            a,
            b,
            z,
            0.0,
            np.array([0.0]),
            d_f,
            local_inputs,
            params,
            a_max,
        )[2]
    )
    use_transfer_f = sdh_f > tolerance
    use_transfer_b = sdh_b < -tolerance and not use_transfer_f
    if at_lower_b:
        use_transfer_b = False
    if at_upper_b:
        use_transfer_f = False
        use_transfer_b = True
    if use_transfer_b:
        transfer_label = "B"
        transfer = d_b
        shadow_transfer_b = d_bb
        shadow_transfer_f = d_bf
    elif use_transfer_f:
        transfer_label = "F"
        transfer = d_f
        shadow_transfer_b = d_fb
        shadow_transfer_f = d_ff
    else:
        transfer_label = "0"
        transfer = 0.0
        shadow_transfer_b = 0.0
        shadow_transfer_f = 0.0

    effective_return = float(matlab_faithful_illiquid_return(a, a_max, inputs.r_a))
    mh_b = min(shadow_transfer_b, 0.0)
    mh_f = max(shadow_transfer_f, 0.0) + effective_return * a
    if at_upper_a:
        mh_b = shadow_transfer_b + effective_return * a_max
        mh_f = 0.0

    mu_a, mu_b, cost = asset_drifts_matlab_faithful(
        a,
        b,
        z,
        consumption - transfer_income,
        np.array([labor]),
        transfer,
        local_inputs,
        params,
        a_max,
    )
    utility = flow_utility(consumption, np.array([labor]), local_inputs, params)
    return MatlabFaithfulLocalPolicy(
        liquid_label=liquid_label,
        transfer_label=transfer_label,
        consumption=float(consumption),
        labor=float(labor),
        transfer=float(transfer),
        adjustment_cost=float(cost),
        effective_illiquid_return=effective_return,
        mu_a=float(mu_a),
        mu_b=float(mu_b),
        utility=float(utility),
        liquid_direction=_direction(float(mu_b), tolerance),
        illiquid_direction=_direction(float(mu_a), tolerance),
        b_backward_rate=max(-float(mu_b), 0.0) / db,
        b_forward_rate=max(float(mu_b), 0.0) / db,
        a_backward_rate=-float(mh_b) / da,
        a_forward_rate=float(mh_f) / da,
        iteration_b_backward_rate=-float(
            (sc_b if use_liquid_b else 0.0) + (sdh_b if use_transfer_b else 0.0)
        )
        / db,
        iteration_b_forward_rate=float(
            (sc_f if use_liquid_f else 0.0) + (sdh_f if use_transfer_f else 0.0)
        )
        / db,
    )

@dataclass(frozen=True)
class MatlabFaithfulOperator:
    bb: sparse.csr_matrix
    aah: sparse.csr_matrix
    bswitch: sparse.csr_matrix
    full: sparse.csr_matrix

def assemble_source_axis(
    backward: np.ndarray, forward: np.ndarray, axis: int
) -> sparse.csr_matrix:
    """Place signed source components, truncating outward entries but not their diagonal."""
    backward = np.asarray(backward, dtype=float)
    forward = np.asarray(forward, dtype=float)
    if backward.shape != forward.shape or backward.ndim != 3:
        raise ValueError("source axis components must share a three-dimensional shape")
    if axis not in (0, 1) or not np.isfinite(backward).all() or not np.isfinite(forward).all():
        raise ValueError("invalid source axis components")
    i_count, j_count, z_count = backward.shape
    rows: list[int] = []
    cols: list[int] = []
    data: list[float] = []
    for nz in range(z_count):
        for j in range(j_count):
            for i in range(i_count):
                row = i + j * i_count + nz * i_count * j_count
                rb = float(backward[i, j, nz])
                rf = float(forward[i, j, nz])
                if rb != 0.0 and ((axis == 0 and i > 0) or (axis == 1 and j > 0)):
                    rows.append(row); cols.append(row - (1 if axis == 0 else i_count)); data.append(rb)
                if rf != 0.0 and ((axis == 0 and i + 1 < i_count) or (axis == 1 and j + 1 < j_count)):
                    rows.append(row); cols.append(row + (1 if axis == 0 else i_count)); data.append(rf)
                rows.append(row); cols.append(row); data.append(-(rb + rf))
    size = i_count * j_count * z_count
    return sparse.coo_matrix((data, (rows, cols)), shape=(size, size)).tocsr()

def assemble_source_operator(
    b_backward: np.ndarray,
    b_forward: np.ndarray,
    a_backward: np.ndarray,
    a_forward: np.ndarray,
    switch_matrix: np.ndarray,
) -> MatlabFaithfulOperator:
    bb = assemble_source_axis(b_backward, b_forward, 0)
    aah = assemble_source_axis(a_backward, a_forward, 1)
    state_size = int(np.prod(b_backward.shape[:2]))
    bswitch = sparse.kron(sparse.csr_matrix(switch_matrix), sparse.eye(state_size), format="csr")
    return MatlabFaithfulOperator(bb, aah, bswitch, (bb + aah + bswitch).tocsr())

@dataclass(frozen=True)
class MatlabFaithfulHJBGrid:
    b: np.ndarray
    a: np.ndarray
    z: np.ndarray
    switch_matrix: np.ndarray

    def __post_init__(self) -> None:
        for name in ("b", "a", "z"):
            value = np.asarray(getattr(self, name), dtype=float)
            if value.ndim != 1 or value.size < 2 or not np.isfinite(value).all() or not np.all(np.diff(value) > 0):
                raise ValueError(f"{name} must be finite and strictly increasing")
            object.__setattr__(self, name, value)
        switch = np.asarray(self.switch_matrix, dtype=float)
        if switch.shape != (self.z.size, self.z.size) or not np.isfinite(switch).all():
            raise ValueError("switch matrix shape is incompatible with z")
        object.__setattr__(self, "switch_matrix", switch)

@dataclass(frozen=True)
class MatlabFaithfulHJBNumerics:
    delta: float
    convergence_tolerance: float
    max_iterations: int
    drift_tolerance: float

@dataclass(frozen=True)
class MatlabFaithfulHJBResult:
    value: np.ndarray
    initial_value: np.ndarray
    consumption: np.ndarray
    labor: np.ndarray
    transfer: np.ndarray
    adjustment_cost: np.ndarray
    effective_illiquid_return: np.ndarray
    mu_a: np.ndarray
    mu_b: np.ndarray
    utility: np.ndarray
    liquid_label: np.ndarray
    transfer_label: np.ndarray
    operator: MatlabFaithfulOperator
    post_convergence_operator: MatlabFaithfulOperator
    iterations: int
    converged: bool
    convergence_statistic: float

def solve_matlab_faithful_hjb(
    grid: MatlabFaithfulHJBGrid,
    params: EconomicParams,
    inputs: HouseholdInputs,
    initial_value: np.ndarray,
    baseline_labor: np.ndarray,
    transfer_income: float,
    borrowing_rate_gap: float,
    numerics: MatlabFaithfulHJBNumerics,
) -> MatlabFaithfulHJBResult:
    shape = (grid.b.size, grid.a.size, grid.z.size)
    value = np.asarray(initial_value, dtype=float).copy()
    labor0 = np.asarray(baseline_labor, dtype=float)
    if value.shape != shape or labor0.shape != shape or not np.isfinite(value).all() or not np.isfinite(labor0).all():
        raise ValueError("initial arrays do not match the faithful MATLAB grid")
    if inputs.wages.size != 1 or numerics.delta <= 0 or numerics.convergence_tolerance <= 0 or numerics.max_iterations < 1:
        raise ValueError("invalid faithful HJB inputs")
    initial = value.copy(); db = float(grid.b[1] - grid.b[0]); da = float(grid.a[1] - grid.a[0])
    arrays: dict[str, np.ndarray] = {}; operator = None; statistic = np.inf; converged = False
    for iteration in range(1, numerics.max_iterations + 1):
        old = value.copy()
        vb_f = np.zeros(shape); vb_b = np.zeros(shape); va_f = np.zeros(shape); va_b = np.zeros(shape)
        vb_f[:-1] = (old[1:] - old[:-1]) / db; vb_b[1:] = vb_f[:-1]
        for j, a in enumerate(grid.a):
            for nz, z in enumerate(grid.z):
                for i in (0, grid.b.size - 1):
                    rb = inputs.r_b + (borrowing_rate_gap if grid.b[i] < 0 else 0.0)
                    resources = (1-inputs.tau)*inputs.wages[0]*z*labor0[i,j,nz] + transfer_income + rb*grid.b[i]
                    marginal = resources ** (-params.gamma_c)
                    if i == 0: vb_b[i,j,nz] = marginal
                    else: vb_f[i,j,nz] = marginal
        va_f[:, :-1] = (old[:, 1:] - old[:, :-1]) / da; va_b[:, 1:] = va_f[:, :-1]
        names = ("consumption","labor","transfer","adjustment_cost","effective_illiquid_return","mu_a","mu_b","utility")
        arrays = {name: np.empty(shape) for name in names}
        liquid = np.empty(shape, dtype="U1"); transfer_label = np.empty(shape, dtype="U1")
        bb = np.empty(shape); bf = np.empty(shape); ab = np.empty(shape); af = np.empty(shape)
        for nz, z in enumerate(grid.z):
            for j, a in enumerate(grid.a):
                for i, b in enumerate(grid.b):
                    policy = select_matlab_faithful_local_policy(a=float(a),b=float(b),z=float(z),v_a_forward=float(va_f[i,j,nz]),v_a_backward=float(va_b[i,j,nz]),v_b_forward=float(vb_f[i,j,nz]),v_b_backward=float(vb_b[i,j,nz]),baseline_labor=float(labor0[i,j,nz]),transfer_income=transfer_income,borrowing_rate_gap=borrowing_rate_gap,a_max=float(grid.a[-1]),da=da,db=db,at_lower_a=j==0,at_upper_a=j+1==grid.a.size,at_lower_b=i==0,at_upper_b=i+1==grid.b.size,inputs=inputs,params=params,tolerance=numerics.drift_tolerance)
                    for name in names: arrays[name][i,j,nz] = getattr(policy, name)
                    liquid[i,j,nz]=policy.liquid_label; transfer_label[i,j,nz]=policy.transfer_label
                    bb[i,j,nz]=policy.iteration_b_backward_rate; bf[i,j,nz]=policy.iteration_b_forward_rate
                    ab[i,j,nz]=policy.a_backward_rate; af[i,j,nz]=policy.a_forward_rate
        operator = assemble_source_operator(bb,bf,ab,af,grid.switch_matrix)
        matrix = (1/numerics.delta + params.rho)*sparse.eye(np.prod(shape),format="csr") - operator.full
        rhs = arrays["utility"].ravel(order="F") + old.ravel(order="F")/numerics.delta
        value = linalg.spsolve(matrix,rhs).reshape(shape,order="F")
        statistic = float(np.max(np.abs(value-old)))
        if statistic < numerics.convergence_tolerance: converged=True; break
    assert operator is not None
    post = assemble_source_operator(np.maximum(-arrays["mu_b"],0)/db,np.maximum(arrays["mu_b"],0)/db,np.maximum(-arrays["mu_a"],0)/da,np.maximum(arrays["mu_a"],0)/da,grid.switch_matrix)
    return MatlabFaithfulHJBResult(value,initial,arrays["consumption"],arrays["labor"],arrays["transfer"],arrays["adjustment_cost"],arrays["effective_illiquid_return"],arrays["mu_a"],arrays["mu_b"],arrays["utility"],liquid,transfer_label,operator,post,iteration,converged,statistic)

@dataclass(frozen=True)
class MatlabFaithfulKFEResult:
    original_operator: sparse.csr_matrix
    transpose: sparse.csr_matrix
    contaminated_row_index: int
    contaminated_matrix: sparse.csr_matrix
    rhs: np.ndarray
    raw_solve_vector: np.ndarray
    normalization_factor: float
    density_vector: np.ndarray
    density: np.ndarray
    db: float
    da: float
    cell_weight: float
    raw_residual_inf: float

def matlab_contaminated_row_index(state_count: int) -> int:
    if state_count < 3:
        raise ValueError("faithful KFE requires at least three states")
    return int(np.floor(0.37 * state_count)) - 1

def solve_matlab_faithful_stationary_kfe(post_convergence_operator, *, shape, db, da):
    operator=sparse.csr_matrix(post_convergence_operator,dtype=float)
    size=int(np.prod(shape))
    if operator.shape!=(size,size) or len(shape)!=3 or min(shape)<1:
        raise ValueError("operator and faithful (b,a,z) shape are incompatible")
    if not np.isfinite(operator.data).all() or not np.isfinite([db,da]).all() or db<=0 or da<=0:
        raise ValueError("faithful KFE inputs must be finite with positive spacings")
    transpose=operator.transpose().tocsr()
    row=matlab_contaminated_row_index(size)
    contaminated=transpose.tolil(copy=True); contaminated[row,:]=0.0; contaminated[row,row]=1.0; contaminated=contaminated.tocsr()
    rhs=np.zeros(size); rhs[row]=0.007
    raw=np.asarray(linalg.spsolve(contaminated,rhs),dtype=float)
    if not np.isfinite(raw).all(): raise ValueError("faithful contaminated-row solve is non-finite")
    factor=float(np.sum(raw)*db*da)
    if not np.isfinite(factor) or factor==0.0: raise ValueError("faithful density normalization is invalid")
    density=raw/factor
    residual=float(np.linalg.norm(contaminated@raw-rhs,ord=np.inf))
    return MatlabFaithfulKFEResult(operator,transpose,row,contaminated,rhs,raw,factor,density,density.reshape(tuple(shape),order="F"),float(db),float(da),float(db*da),residual)

@dataclass(frozen=True)
class StationaryHouseholdAggregates:
    c_ss: float
    l_ss: float
    a_ss: float
    b_ss: float
    total_assets: float
    density_normalization: float

@dataclass(frozen=True)
class HouseholdSteadyStateResult:
    hjb: MatlabFaithfulHJBResult
    kfe: MatlabFaithfulKFEResult
    aggregates: StationaryHouseholdAggregates

def aggregate_stationary_household(grid, consumption, labor, density):
    """Exact MATLAB sums; L is effective z-weighted household labor, not GE labor."""
    shape=(grid.b.size,grid.a.size,grid.z.size)
    C=np.asarray(consumption,dtype=float); l=np.asarray(labor,dtype=float); g=np.asarray(density,dtype=float)
    if C.shape!=shape or l.shape!=shape or g.shape!=shape or not np.isfinite(C).all() or not np.isfinite(l).all() or not np.isfinite(g).all():
        raise ValueError("aggregate arrays must be finite and match (b,a,z)")
    db=float(grid.b[1]-grid.b[0]); da=float(grid.a[1]-grid.a[0]); weight=db*da
    b=np.broadcast_to(grid.b[:,None,None],shape); a=np.broadcast_to(grid.a[None,:,None],shape); z=np.broadcast_to(grid.z[None,None,:],shape)
    c_ss=float(np.sum(C*g*weight)); l_ss=float(np.sum(z*l*g*weight))
    a_ss=float(np.sum(a*g*weight)); b_ss=float(np.sum(b*g*weight))
    return StationaryHouseholdAggregates(c_ss,l_ss,a_ss,b_ss,a_ss+b_ss,float(np.sum(g)*weight))

def solve_household_steady_state(grid,params,inputs,initial_value,baseline_labor,transfer_income,borrowing_rate_gap,numerics):
    hjb=solve_matlab_faithful_hjb(grid,params,inputs,initial_value,baseline_labor,transfer_income,borrowing_rate_gap,numerics)
    if not hjb.converged:
        raise RuntimeError("MATLAB-faithful HJB did not converge")
    shape=(grid.b.size,grid.a.size,grid.z.size); db=float(grid.b[1]-grid.b[0]); da=float(grid.a[1]-grid.a[0])
    kfe=solve_matlab_faithful_stationary_kfe(hjb.post_convergence_operator.full,shape=shape,db=db,da=da)
    aggregates=aggregate_stationary_household(grid,hjb.consumption,hjb.labor,kfe.density)
    return HouseholdSteadyStateResult(hjb,kfe,aggregates)

__all__=[
    "EconomicParams","HouseholdInputs","MatlabFaithfulHJBGrid","MatlabFaithfulHJBNumerics",
    "MatlabFaithfulHJBResult","MatlabFaithfulKFEResult","StationaryHouseholdAggregates",
    "HouseholdSteadyStateResult","adjustment_cost","transfer_candidate",
    "matlab_faithful_illiquid_return","consumption_from_vb","labor_from_vb","flow_utility",
    "asset_drifts_matlab_faithful","select_matlab_faithful_local_policy","assemble_source_axis",
    "assemble_source_operator","matlab_contaminated_row_index","solve_matlab_faithful_hjb",
    "solve_matlab_faithful_stationary_kfe","aggregate_stationary_household","solve_household_steady_state"
]
