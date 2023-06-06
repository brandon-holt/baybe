# pylint: disable=missing-module-docstring, missing-function-docstring

import pytest
from baybe.searchspace import SearchSpace


@pytest.mark.parametrize(
    "parameter_names",
    [
        ["Categorical_1", "Num_discrete_1"],
        ["Fraction_1"],
        ["Conti_infinite1"],
        ["Conti_finite1"],
        ["Custom_1"],
        ["Solvent_1"],
    ],
)
def test_searchspace_serialization(parameters):
    searchspace = SearchSpace.create(parameters)
    string = searchspace.to_json()
    searchspace2 = SearchSpace.from_json(string)
    assert searchspace == searchspace2