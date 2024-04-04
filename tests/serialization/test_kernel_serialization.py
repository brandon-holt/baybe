"""Test serialization of Kernels."""

import pytest

from baybe.kernels import Kernel, MaternKernel

KERNELS = [
    MaternKernel(nu=0.5),
    MaternKernel(nu=1.5),
    MaternKernel(nu=2.5),
]


@pytest.mark.parametrize("kernel", KERNELS)
def test_objective_serialization(kernel):
    string = kernel.to_json()
    kernel2 = Kernel.from_json(string)
    assert kernel == kernel2
