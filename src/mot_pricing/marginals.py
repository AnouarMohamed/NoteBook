"""Discrete marginal helpers and convex-order checks."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from .discretization import make_uniform_grid


Array1D = NDArray[np.float64]


def _as_float_vector(name: str, values: Array1D) -> Array1D:
    vector = np.asarray(values, dtype=float)
    if vector.ndim != 1:
        raise ValueError(f"{name} must be one-dimensional")
    if len(vector) == 0:
        raise ValueError(f"{name} must be non-empty")
    return vector


@dataclass(frozen=True)
class DiscreteMarginal:
    atoms: Array1D
    weights: Array1D
    name: str | None = None

    def __post_init__(self) -> None:
        atoms = _as_float_vector("atoms", self.atoms)
        weights = _as_float_vector("weights", self.weights)
        if len(atoms) != len(weights):
            raise ValueError("atoms and weights must have matching lengths")
        if np.any(weights < 0.0):
            raise ValueError("weights must be non-negative")
        total = float(weights.sum())
        if not np.isclose(total, 1.0, atol=1e-10):
            raise ValueError(f"weights must sum to 1.0, got {total}")
        object.__setattr__(self, "atoms", atoms)
        object.__setattr__(self, "weights", weights)

    @property
    def size(self) -> int:
        return len(self.atoms)

    @property
    def mean(self) -> float:
        return float(np.dot(self.atoms, self.weights))

    @property
    def variance(self) -> float:
        second_moment = float(np.dot(self.atoms**2, self.weights))
        return second_moment - self.mean**2


def make_discrete_marginal(
    atoms: Array1D,
    weights: Array1D,
    *,
    name: str | None = None,
) -> DiscreteMarginal:
    return DiscreteMarginal(
        atoms=np.asarray(atoms, dtype=float),
        weights=np.asarray(weights, dtype=float),
        name=name,
    )


def make_uniform_marginal(
    a: float,
    b: float,
    n: int,
    *,
    name: str | None = None,
) -> DiscreteMarginal:
    atoms, weights = make_uniform_grid(a, b, n)
    return DiscreteMarginal(atoms=atoms, weights=weights, name=name)


def call_prices(marginal: DiscreteMarginal, strikes: Array1D) -> Array1D:
    strike_vector = np.asarray(strikes, dtype=float)
    return (
        (marginal.atoms[:, None] - strike_vector[None, :]).clip(min=0.0)
        * marginal.weights[:, None]
    ).sum(axis=0)


@dataclass(frozen=True)
class ConvexOrderCheck:
    feasible: bool
    mean_gap: float
    min_call_gap: float
    max_call_gap: float
    strikes: Array1D


def check_convex_order_discrete(
    marginal_1: DiscreteMarginal,
    marginal_2: DiscreteMarginal,
    *,
    strikes: Array1D | None = None,
    tol: float = 1e-10,
) -> ConvexOrderCheck:
    """Check the discrete convex-order condition via call prices."""
    if strikes is None:
        support = np.unique(np.concatenate((marginal_1.atoms, marginal_2.atoms)))
        strike_vector = np.concatenate(
            (
                np.array([support[0] - 1.0], dtype=float),
                support,
                np.array([support[-1] + 1.0], dtype=float),
            )
        )
    else:
        strike_vector = np.asarray(strikes, dtype=float)

    mean_gap = marginal_2.mean - marginal_1.mean
    call_gap = call_prices(marginal_2, strike_vector) - call_prices(
        marginal_1, strike_vector
    )
    min_call_gap = float(call_gap.min())
    max_call_gap = float(call_gap.max())
    feasible = abs(mean_gap) <= tol and min_call_gap >= -tol
    return ConvexOrderCheck(
        feasible=feasible,
        mean_gap=float(mean_gap),
        min_call_gap=min_call_gap,
        max_call_gap=max_call_gap,
        strikes=strike_vector,
    )
