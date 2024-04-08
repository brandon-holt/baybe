"""Collection of kernels."""

from fractions import Fraction
from typing import Union

from attrs import define, field
from attrs.validators import in_

from baybe.kernels.base import Kernel


def _convert_nu(nu: Union[str, float]) -> float:
    """Convert the provided value into a float.

    Since the nu parameter might be provided as a fraction, this function tries to
    convert the str first to a fraction and the to a str. This also works if the value
    is directly provided as a non-fraction str like '0.5'.
    Note that this does not validate whether `nu` is one of the three allowed values of
    0.5, 1.5 and 2.5 but only converts the parameter.

    Args:
        nu: The parameter that should be converted.

    Returns:
        The converted parameter.

    Raises:
        ValueError: If `nu` was provided as str but could not be interpreted as
            fraction.
    """
    if isinstance(nu, str):
        try:
            value_float = float(Fraction(nu))
        except ValueError as err:
            raise ValueError(
                f"Provided value of {nu} could not be interpreted as fraction"
            ) from err
    else:
        value_float = float(nu)
    return value_float


@define
class MaternKernel(Kernel):
    """A Matern kernel using a smoothness parameter."""

    nu: float = field(
        converter=_convert_nu, validator=in_([0.5, 1.5, 2.5]), default=2.5
    )
    """A smoothness parameter.

    Only takes the values 0.5, 1.5 or 2.5. Larger values yield smoother interpolations.
    """
