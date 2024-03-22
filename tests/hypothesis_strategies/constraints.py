"""Hypothesis strategies for constraints."""

from typing import List, Optional

import hypothesis.strategies as st

from baybe.constraints.conditions import (
    SubSelectionCondition,
    ThresholdCondition,
    _valid_logic_combiners,
)
from baybe.constraints.discrete import (
    DiscreteExcludeConstraint,
    DiscreteLinkedParametersConstraint,
    DiscreteNoLabelDuplicatesConstraint,
    DiscreteProductConstraint,
    DiscreteSumConstraint,
)
from baybe.parameters.base import DiscreteParameter
from baybe.parameters.numerical import NumericalDiscreteParameter

from .parameters import discrete_parameters

_disc_params = st.lists(discrete_parameters, min_size=1, unique_by=lambda p: p.name)


def sub_selection_conditions(p: DiscreteParameter):
    """Generate :class:`baybe.constraints.conditions.SubSelectionCondition`."""
    return st.builds(
        SubSelectionCondition, st.lists(st.sampled_from(p.values), unique=True)
    )


threshold_conditions = st.builds(
    ThresholdCondition, threshold=st.floats(allow_infinity=False, allow_nan=False)
)
"""Generate :class:`baybe.constraints.conditions.ThresholdCondition`."""


@st.composite
def discrete_excludes_constraints(
    draw: st.DrawFn, parameters: Optional[List[DiscreteParameter]] = None
):
    """Generate :class:`baybe.constraints.discrete.DiscreteExcludeConstraint`."""
    if parameters is None:
        parameters = draw(_disc_params)

    parameter_names = [p.name for p in parameters]

    # Threshold conditions only make sense for numerical parameters
    conditions = [
        draw(st.one_of([sub_selection_conditions(p), threshold_conditions]))
        if isinstance(p, NumericalDiscreteParameter)
        else draw(sub_selection_conditions(p))
        for p in parameters
    ]

    combiner = draw(st.sampled_from(list(_valid_logic_combiners)))
    return DiscreteExcludeConstraint(parameter_names, conditions, combiner)


@st.composite
def discrete_sum_constraints(
    draw: st.DrawFn, parameters: Optional[List[DiscreteParameter]] = None
):
    """Generate :class:`baybe.constraints.discrete.DiscreteSumConstraint`."""
    if parameters is None:
        parameters = draw(_disc_params)

    parameter_names = [p.name for p in parameters]
    conditions = draw(threshold_conditions)
    return DiscreteSumConstraint(parameter_names, conditions)


@st.composite
def discrete_product_constraints(
    draw: st.DrawFn, parameters: Optional[List[DiscreteParameter]] = None
):
    """Generate :class:`baybe.constraints.discrete.DiscreteProductConstraint`."""
    if parameters is None:
        parameters = draw(_disc_params)

    parameter_names = [p.name for p in parameters]
    conditions = draw(threshold_conditions)
    return DiscreteProductConstraint(parameter_names, conditions)


@st.composite
def discrete_no_label_duplicates_constraints(
    draw: st.DrawFn, parameters: Optional[List[DiscreteParameter]] = None
):
    """Generate :class:`baybe.constraints.discrete.DiscreteNoLabelDuplicatesConstraint`."""  # noqa:E501
    if parameters is None:
        parameters = draw(_disc_params)

    parameter_names = [p.name for p in parameters]
    return DiscreteNoLabelDuplicatesConstraint(parameter_names)


@st.composite
def discrete_linked_parameters_constraints(
    draw: st.DrawFn, parameters: Optional[List[DiscreteParameter]] = None
):
    """Generate :class:`baybe.constraints.discrete.DiscreteLinkedParametersConstraint`."""  # noqa:E501
    if parameters is None:
        parameters = draw(_disc_params)

    parameter_names = [p.name for p in parameters]
    return DiscreteLinkedParametersConstraint(parameter_names)
