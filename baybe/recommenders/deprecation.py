"""Temporary functionality for backward compatibility."""

from __future__ import annotations

import warnings
from typing import TYPE_CHECKING

from cattrs.gen import make_dict_structure_fn

from baybe.serialization import converter
from baybe.utils import get_subclasses

if TYPE_CHECKING:
    from baybe.recommenders.base import RecommenderProtocol


def structure_recommender_protocol(val: dict, _) -> RecommenderProtocol:
    """A structure hook using ``TwoPhaseStrategy`` as fallback type."""  # noqa: D401 (imperative mood)
    from baybe.recommenders.base import RecommenderProtocol
    from baybe.strategies.composite import TwoPhaseStrategy

    try:
        _type = val["type"]
        cls = next(
            (cl for cl in get_subclasses(RecommenderProtocol) if cl.__name__ == _type),
            None,
        )
        if cls is None:
            raise ValueError(f"Unknown subclass '{_type}'.")
    except KeyError:
        cls = TwoPhaseStrategy
        warnings.warn(
            f"A recommender has been specified without a corresponding type. "
            f"As a fallback, '{TwoPhaseStrategy.__name__}' is used. "
            f"However, this behavior is deprecated and will be disabled in "
            f"a future version.",
            DeprecationWarning,
        )
    fun = make_dict_structure_fn(cls, converter)

    return fun(val, cls)