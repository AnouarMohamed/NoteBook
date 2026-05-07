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


@dataclass(frozen=True)
class CausalMarginalChain:
    marginals: tuple[DiscreteMarginal, ...]

    def __post_init__(self) -> None:
        """
        Validate and normalize marginals when initializing a CausalMarginalChain.
        
        Ensures the instance has at least two marginals and that each consecutive pair
        has matching means within an absolute tolerance of 1e-10. On success, stores
        the provided marginals as an immutable tuple on the dataclass.
        
        Raises:
            ValueError: if fewer than two marginals are provided.
            ValueError: if any consecutive pair of marginals has a mean difference
                greater than 1e-10; the exception message includes the 1-based step
                index and the observed mean gap.
        """
        marginals = tuple(self.marginals)
        if len(marginals) < 2:
            raise ValueError("causal marginal chains require at least two marginals")

        for step, (marginal_1, marginal_2) in enumerate(
            zip(marginals[:-1], marginals[1:]), start=1
        ):
            mean_gap = marginal_2.mean - marginal_1.mean
            if not np.isclose(mean_gap, 0.0, atol=1e-10):
                raise ValueError(
                    "martingale feasibility requires consecutive matching means: "
                    f"step={step}, mean_gap={mean_gap:.3e}"
                )

        object.__setattr__(self, "marginals", marginals)

    @property
    def marginal_count(self) -> int:
        """
        Number of marginals in the causal chain.
        
        Returns:
            The number of marginals stored in the chain.
        """
        return len(self.marginals)

    @property
    def step_count(self) -> int:
        """
        Number of transition steps between consecutive marginals in the chain.
        
        Returns:
            The number of steps, equal to one less than the number of marginals.
        """
        return self.marginal_count - 1

    def pairs(self) -> tuple[tuple[DiscreteMarginal, DiscreteMarginal], ...]:
        """
        Provide consecutive pairs of marginals from the chain in chain order.
        
        Returns:
            tuple[tuple[DiscreteMarginal, DiscreteMarginal], ...]: Tuple of consecutive (marginal_i, marginal_{i+1}) pairs; length equals `step_count`.
        """
        return tuple(zip(self.marginals[:-1], self.marginals[1:]))

    @classmethod
    def from_uniform_intervals(
        cls,
        intervals: list[tuple[float, float, int]]
        | tuple[tuple[float, float, int], ...],
    ) -> "CausalMarginalChain":
        """
        Constructs a CausalMarginalChain from a sequence of uniform-interval specifications.
        
        Parameters:
            intervals (list[tuple[float, float, int]] | tuple[tuple[float, float, int], ...]):
                Sequence of (a, b, n) tuples where `a` and `b` are the interval endpoints and `n`
                is the number of atoms to place uniformly on [a, b]. Each tuple produces a
                DiscreteMarginal representing a uniform grid over the interval; marginals are
                named "S1", "S2", ... in the same order as the provided intervals.
        
        Returns:
            CausalMarginalChain: A chain whose `marginals` are the discrete uniform marginals
            constructed from the provided intervals.
        """
        marginals = tuple(
            make_uniform_marginal(a, b, n, name=f"S{index}")
            for index, (a, b, n) in enumerate(intervals, start=1)
        )
        return cls(marginals=marginals)


@dataclass(frozen=True)
class CausalFeasibilityReport:
    feasible: bool
    mean_gaps: Array1D
    min_call_gaps: Array1D
    max_call_gaps: Array1D
    step_checks: tuple[ConvexOrderCheck, ...]
    summary: str


def check_convex_order_discrete(
    marginal_1: DiscreteMarginal,
    marginal_2: DiscreteMarginal,
    *,
    strikes: Array1D | None = None,
    tol: float = 1e-10,
) -> ConvexOrderCheck:
    """
    Determine whether two discrete marginals satisfy the convex-order condition by comparing their means and call-option prices at specified strikes.
    
    Parameters:
        marginal_1 (DiscreteMarginal): The earlier marginal in the convex-order comparison.
        marginal_2 (DiscreteMarginal): The later marginal to compare against `marginal_1`.
        strikes (Array1D | None): Strike prices at which to evaluate call prices. If `None`, strikes are chosen from the union of both supports augmented by one point below and above the combined support.
        tol (float): Numerical tolerance for mean equality and nonnegativity of call-price gaps.
    
    Returns:
        ConvexOrderCheck: Result object containing:
            - `feasible`: `True` if the mean difference is within `tol` and all call-price gaps are >= `-tol`, `False` otherwise.
            - `mean_gap`: `marginal_2.mean - marginal_1.mean`.
            - `min_call_gap`: Minimum value of `call_price(marginal_2, strikes) - call_price(marginal_1, strikes)`.
            - `max_call_gap`: Maximum value of the call-price gap across strikes.
            - `strikes`: The strike vector used for the check.
    """
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


def check_causal_feasibility(
    chain: CausalMarginalChain,
    *,
    tol: float = 1e-10,
) -> CausalFeasibilityReport:
    """
    Evaluate convex-order feasibility for each consecutive step in a causal marginal chain.
    
    Performs convex-order checks between each pair of consecutive marginals in `chain`, aggregates per-step mean and call-price gaps, and returns a report summarizing overall feasibility.
    
    Parameters:
        tol (float): Numerical tolerance used to decide mean equality and to allow small negative call-price gaps when determining feasibility.
    
    Returns:
        CausalFeasibilityReport: Contains `feasible` (overall boolean), `mean_gaps`, `min_call_gaps`, `max_call_gaps`, the tuple of per-step `ConvexOrderCheck` results, and a human-readable `summary`.
    """
    step_checks = tuple(
        check_convex_order_discrete(marginal_1, marginal_2, tol=tol)
        for marginal_1, marginal_2 in chain.pairs()
    )
    mean_gaps = np.array([check.mean_gap for check in step_checks], dtype=float)
    min_call_gaps = np.array(
        [check.min_call_gap for check in step_checks], dtype=float
    )
    max_call_gaps = np.array(
        [check.max_call_gap for check in step_checks], dtype=float
    )
    feasible = all(check.feasible for check in step_checks)

    if feasible:
        summary = (
            f"causal chain feasible across {chain.step_count} steps; "
            f"max_abs_mean_gap={np.max(np.abs(mean_gaps)):.3e}, "
            f"min_call_gap={np.min(min_call_gaps):.3e}"
        )
    else:
        failed_steps = [
            str(index)
            for index, check in enumerate(step_checks, start=1)
            if not check.feasible
        ]
        summary = (
            f"causal chain infeasible at step(s) {', '.join(failed_steps)}; "
            f"max_abs_mean_gap={np.max(np.abs(mean_gaps)):.3e}, "
            f"min_call_gap={np.min(min_call_gaps):.3e}"
        )

    return CausalFeasibilityReport(
        feasible=feasible,
        mean_gaps=mean_gaps,
        min_call_gaps=min_call_gaps,
        max_call_gaps=max_call_gaps,
        step_checks=step_checks,
        summary=summary,
    )
