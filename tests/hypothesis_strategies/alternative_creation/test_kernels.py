"""Test alternative ways of creation not considered in the strategies."""

from fractions import Fraction

import hypothesis.strategies as st
import pytest
from hypothesis import given

from baybe.kernels import MaternKernel

# Strategies for creating (hopefully different) representations of the fractions that
# can be used to create the MaternKernel
one_half_fraction_strategy = st.fractions(min_value=0.5, max_value=0.5)
three_halves_fraction_strategy = st.fractions(min_value=1.5, max_value=1.5)
five_halves_fraction_strategy = st.fractions(min_value=2.5, max_value=2.5)

# Putting all of the fraction strategies together
fraction_strategy = st.one_of(
    one_half_fraction_strategy,
    three_halves_fraction_strategy,
    five_halves_fraction_strategy,
)


@given(fraction_strategy)
def test_different_fractions(nu: Fraction):
    """Test different representations of the same fractions."""
    MaternKernel(nu=nu)


@pytest.mark.parametrize("nu", ["1/2", "3/2", "5/2"])
def test_fraction_string_creation(nu: str):
    """The nu parameter can be a str representing a fraction."""
    MaternKernel(nu=nu)


@pytest.mark.parametrize("nu", ["0.5", "1.5", "2.5"])
def test_float_string_creation(nu: str):
    """The nu parameter can be a str representing a float."""
    MaternKernel(nu=nu)
