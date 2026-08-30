"""Canonical two-asset HA household kernel package (DLH-4B, Issue #18).

This package hosts the **accepted MATLAB-faithful two-asset HA oracle** as the
canonical DeepLearning-HANK household foundation:

- ``matlab_faithful_two_asset_ha`` — the accepted standalone implementation
  (byte-equivalent import of the accepted export
  ``zcx369658780/dissertation-ch5-two-asset-hank:exports/matlab_faithful_two_asset_ha.py``,
  export authority ``6469e5a87a00366c1b2af38f27efaa3014206936``, SHA-256
  ``276D2244B389D6EDE140DAF8B1F9B0BE1F4AA859368941CED1A12BA8A5831AB8``).

Scientific labels (Owner clarification comment id ``IC_kwDOT9FOGc8AAAABReN_dA``):
- ``ECONOMIC_STRUCTURE``: state ``(b,a,z)``, liquid/illiquid assets, transfer
  control ``d``, adjustment cost, labor/consumption FOCs;
- ``NUMERICAL_REGULARIZATION / MATLAB_FAITHFUL_IMPLEMENTATION``: the
  illiquid-return taper, the bare-``a`` transfer FOC pairing, the exact
  spdiags-equivalent HJB iteration operator, and the contaminated-row KFE
  solve — preserved for parity, not primitive economic equations.

GE closure and dynamics are intentionally outside this package.
"""

from deep_learning_hank.two_asset import matlab_faithful_two_asset_ha as matlab_faithful_two_asset_ha

from deep_learning_hank.two_asset.matlab_faithful_two_asset_ha import (  # noqa: F401
    EconomicParams,
    HouseholdInputs,
    HouseholdSteadyStateResult,
    MatlabFaithfulHJBGrid,
    MatlabFaithfulHJBNumerics,
    MatlabFaithfulHJBResult,
    MatlabFaithfulKFEResult,
    MatlabFaithfulLocalPolicy,
    MatlabFaithfulOperator,
    StationaryHouseholdAggregates,
    adjustment_cost,
    aggregate_stationary_household,
    asset_drifts_matlab_faithful,
    assemble_source_axis,
    assemble_source_operator,
    consumption_from_vb,
    flow_utility,
    labor_from_vb,
    matlab_contaminated_row_index,
    matlab_faithful_illiquid_return,
    select_matlab_faithful_local_policy,
    solve_household_steady_state,
    solve_matlab_faithful_hjb,
    solve_matlab_faithful_stationary_kfe,
    transfer_candidate,
)

__all__ = [
    "matlab_faithful_two_asset_ha",
    "EconomicParams",
    "HouseholdInputs",
    "HouseholdSteadyStateResult",
    "MatlabFaithfulHJBGrid",
    "MatlabFaithfulHJBNumerics",
    "MatlabFaithfulHJBResult",
    "MatlabFaithfulKFEResult",
    "MatlabFaithfulLocalPolicy",
    "MatlabFaithfulOperator",
    "StationaryHouseholdAggregates",
    "adjustment_cost",
    "aggregate_stationary_household",
    "asset_drifts_matlab_faithful",
    "assemble_source_axis",
    "assemble_source_operator",
    "consumption_from_vb",
    "flow_utility",
    "labor_from_vb",
    "matlab_contaminated_row_index",
    "matlab_faithful_illiquid_return",
    "select_matlab_faithful_local_policy",
    "solve_household_steady_state",
    "solve_matlab_faithful_hjb",
    "solve_matlab_faithful_stationary_kfe",
    "transfer_candidate",
]
