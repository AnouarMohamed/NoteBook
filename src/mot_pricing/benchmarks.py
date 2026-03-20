"""Unrestricted coupling benchmarks for the reference uniform example."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.integrate import dblquad


@dataclass(frozen=True)
class UniformAbsSpreadBenchmarks:
    unrestricted_min_comonotone: float
    independent: float
    unrestricted_max_countermonotone: float


def _uniform_quantile(a: float, b: float, u: np.ndarray) -> np.ndarray:
    return a + (b - a) * u


def abs_spread_uniform_benchmarks(
    x_interval: tuple[float, float],
    y_interval: tuple[float, float],
    *,
    num_points: int = 200_000,
) -> UniformAbsSpreadBenchmarks:
    """Benchmark E[|X-Y|] under classic unrestricted one-dimensional couplings."""
    x_a, x_b = x_interval
    y_a, y_b = y_interval
    if x_b <= x_a or y_b <= y_a:
        raise ValueError("expected proper intervals")

    u = np.linspace(0.0, 1.0, num_points, dtype=float)
    x_quantile = _uniform_quantile(x_a, x_b, u)
    y_comonotone = _uniform_quantile(y_a, y_b, u)
    y_countermonotone = _uniform_quantile(y_a, y_b, 1.0 - u)

    unrestricted_min = float(np.trapezoid(np.abs(x_quantile - y_comonotone), u))
    unrestricted_max = float(
        np.trapezoid(np.abs(x_quantile - y_countermonotone), u)
    )

    density_x = 1.0 / (x_b - x_a)
    density_y = 1.0 / (y_b - y_a)
    independent, _ = dblquad(
        lambda y, x: abs(x - y) * density_x * density_y,
        x_a,
        x_b,
        lambda _x: y_a,
        lambda _x: y_b,
    )

    return UniformAbsSpreadBenchmarks(
        unrestricted_min_comonotone=unrestricted_min,
        independent=float(independent),
        unrestricted_max_countermonotone=unrestricted_max,
    )
