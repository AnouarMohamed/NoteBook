"""Discretization helpers for one-dimensional MOT examples."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


Array1D = NDArray[np.float64]


def make_uniform_grid(a: float, b: float, n: int) -> tuple[Array1D, Array1D]:
    """Return midpoint atoms and uniform weights on [a, b]."""
    if n <= 0:
        raise ValueError("n must be positive")
    if b <= a:
        raise ValueError("expected b > a")

    edges = np.linspace(a, b, n + 1, dtype=float)
    atoms = 0.5 * (edges[:-1] + edges[1:])
    weights = np.full(n, 1.0 / n, dtype=float)
    return atoms, weights
