"""Built-in payoff helpers for two-step MOT experiments."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Literal

import numpy as np
from numpy.typing import NDArray


Array2D = NDArray[np.float64]
BuiltinPayoffName = Literal[
    "abs_spread",
    "squared_distance",
    "call_on_spread",
    "put_on_spread",
    "straddle_on_spread",
]


@dataclass(frozen=True)
class PayoffSpec:
    name: str
    description: str
    function: Callable[[Array2D, Array2D], Array2D]
    strike: float = 0.0


def builtin_payoff_names() -> tuple[str, ...]:
    return (
        "abs_spread",
        "squared_distance",
        "call_on_spread",
        "put_on_spread",
        "straddle_on_spread",
    )


def make_builtin_payoff(name: BuiltinPayoffName, *, strike: float = 0.0) -> PayoffSpec:
    if name == "abs_spread":
        return PayoffSpec(
            name=name,
            description="Absolute spread |S2 - S1|",
            function=lambda s1, s2: np.abs(s2 - s1),
            strike=strike,
        )
    if name == "squared_distance":
        return PayoffSpec(
            name=name,
            description="Quadratic spread (S2 - S1)^2",
            function=lambda s1, s2: (s2 - s1) ** 2,
            strike=strike,
        )
    if name == "call_on_spread":
        return PayoffSpec(
            name=name,
            description="Call on spread max(S2 - S1 - K, 0)",
            function=lambda s1, s2: np.maximum(s2 - s1 - strike, 0.0),
            strike=strike,
        )
    if name == "put_on_spread":
        return PayoffSpec(
            name=name,
            description="Put on spread max(K - (S2 - S1), 0)",
            function=lambda s1, s2: np.maximum(strike - (s2 - s1), 0.0),
            strike=strike,
        )
    if name == "straddle_on_spread":
        return PayoffSpec(
            name=name,
            description="Spread straddle |(S2 - S1) - K|",
            function=lambda s1, s2: np.abs((s2 - s1) - strike),
            strike=strike,
        )
    raise ValueError(
        f"unknown payoff '{name}', expected one of: {', '.join(builtin_payoff_names())}"
    )
