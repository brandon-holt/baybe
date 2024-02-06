"""Numerical parameters."""

from functools import cached_property
from typing import Any, ClassVar, Tuple

import cattrs
import numpy as np
import pandas as pd
from attrs import define, field
from attrs.validators import ge, min_len

from baybe.parameters.base import DiscreteParameter, Parameter
from baybe.parameters.validation import validate_is_finite, validate_unique_values
from baybe.utils import InfiniteIntervalError, Interval, convert_bounds


@define(frozen=True, slots=False)
class NumericalDiscreteParameter(DiscreteParameter):
    """Parameter class for discrete numerical parameters (a.k.a. setpoints)."""

    # class variables
    is_numeric: ClassVar[bool] = True
    # See base class.

    # object variables
    # NOTE: The values are assumed to be sorted by the tolerance default method.
    _values: Tuple[float, ...] = field(
        # FIXME[typing]: https://github.com/python-attrs/cattrs/issues/111
        converter=lambda x: sorted(cattrs.structure(x, Tuple[float, ...])),  # type: ignore
        # FIXME[typing]: https://github.com/python-attrs/attrs/issues/1197
        validator=[
            min_len(2),
            validate_unique_values,  # type: ignore
            validate_is_finite,
        ],
    )
    """The values the parameter can take."""

    tolerance: float = field(validator=ge(0.0))
    """The absolute tolerance used for deciding whether a value is considered in range.
        A value is considered in range if its distance to the closest parameter value
        is smaller than the specified tolerance."""

    @tolerance.default
    def default_tolerance(self) -> float:
        """Set the tolerance to fraction of the smallest value distance."""
        fraction = 0.1
        return fraction * np.diff(self.values).min().item()

    @property
    def values(self) -> tuple:  # noqa: D102
        # See base class.
        return self._values

    @cached_property
    def comp_df(self) -> pd.DataFrame:  # noqa: D102
        # See base class.
        comp_df = pd.DataFrame({self.name: self.values}, index=self.values)
        return comp_df

    def is_in_range(self, item: float) -> bool:  # noqa: D102
        # See base class.
        differences_acceptable = [
            np.abs(val - item) <= self.tolerance for val in self.values
        ]
        return any(differences_acceptable)


@define(frozen=True, slots=False)
class NumericalContinuousParameter(Parameter):
    """Parameter class for continuous numerical parameters."""

    # class variables
    is_numeric: ClassVar[bool] = True
    # See base class.

    is_discrete: ClassVar[bool] = False
    # See base class.

    # object variables
    bounds: Interval = field(default=None, converter=convert_bounds)
    """The bounds of the parameter."""

    @bounds.validator
    def _validate_bounds(self, _: Any, value: Interval) -> None:  # noqa: DOC101, DOC103
        """Validate bounds.

        Raises:
            InfiniteIntervalError: If the provided interval is not finite.
        """
        if not value.is_bounded:
            raise InfiniteIntervalError(
                f"You are trying to initialize a parameter with an infinite range "
                f"of {value.to_tuple()}. Infinite intervals for parameters are "
                f"currently not supported."
            )

    def is_in_range(self, item: float) -> bool:  # noqa: D102
        # See base class.

        return self.bounds.contains(item)
