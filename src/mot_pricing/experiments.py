"""Reproducible experiment runners for discrete and uniform MOT problems."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .benchmarks import UniformAbsSpreadBenchmarks, abs_spread_uniform_benchmarks
from .exact import ExactMOTResult, solve_exact_mot
from .marginals import (
    ConvexOrderCheck,
    DiscreteMarginal,
    check_convex_order_discrete,
    make_uniform_marginal,
)
from .payoffs import PayoffSpec, make_builtin_payoff
from .regularized import RegularizedMOTResult, sinkhorn_mot


@dataclass(frozen=True)
class DiscreteExperimentResult:
    marginal_1: DiscreteMarginal
    marginal_2: DiscreteMarginal
    payoff: PayoffSpec
    convex_order: ConvexOrderCheck
    payoff_matrix: np.ndarray
    exact_upper: ExactMOTResult
    exact_lower: ExactMOTResult
    unrestricted_benchmarks: UniformAbsSpreadBenchmarks | None
    regularized_results: dict[float, RegularizedMOTResult]


UniformExperimentResult = DiscreteExperimentResult


def run_discrete_experiment(
    marginal_1: DiscreteMarginal,
    marginal_2: DiscreteMarginal,
    payoff: PayoffSpec,
    *,
    eps_values: tuple[float, ...] = (),
    sinkhorn_iterations: int = 600,
    sinkhorn_tolerance: float = 1e-8,
    unrestricted_benchmarks: UniformAbsSpreadBenchmarks | None = None,
) -> DiscreteExperimentResult:
    """Run an exact-plus-regularized MOT experiment on two discrete marginals."""
    convex_order = check_convex_order_discrete(marginal_1, marginal_2)
    if not convex_order.feasible:
        raise ValueError(
            "no martingale coupling detected by the discrete convex-order check: "
            f"mean_gap={convex_order.mean_gap:.3e}, "
            f"min_call_gap={convex_order.min_call_gap:.3e}"
        )

    exact_upper = solve_exact_mot(
        marginal_1.atoms,
        marginal_1.weights,
        marginal_2.atoms,
        marginal_2.weights,
        payoff.function,
        objective="max",
    )
    exact_lower = solve_exact_mot(
        marginal_1.atoms,
        marginal_1.weights,
        marginal_2.atoms,
        marginal_2.weights,
        payoff.function,
        objective="min",
    )

    regularized_results: dict[float, RegularizedMOTResult] = {}
    for eps in eps_values:
        regularized_results[eps] = sinkhorn_mot(
            marginal_1.atoms,
            marginal_1.weights,
            marginal_2.atoms,
            marginal_2.weights,
            exact_upper.payoff_matrix,
            eps,
            n_iter=sinkhorn_iterations,
            tol=sinkhorn_tolerance,
        )

    return DiscreteExperimentResult(
        marginal_1=marginal_1,
        marginal_2=marginal_2,
        payoff=payoff,
        convex_order=convex_order,
        payoff_matrix=exact_upper.payoff_matrix,
        exact_upper=exact_upper,
        exact_lower=exact_lower,
        unrestricted_benchmarks=unrestricted_benchmarks,
        regularized_results=regularized_results,
    )


def run_two_uniform_experiment(
    *,
    x_interval: tuple[float, float] = (1.0, 3.0),
    y_interval: tuple[float, float] = (0.0, 4.0),
    n: int = 50,
    payoff_name: str = "abs_spread",
    strike: float = 0.0,
    eps_values: tuple[float, ...] = (),
    sinkhorn_iterations: int = 600,
    sinkhorn_tolerance: float = 1e-8,
) -> DiscreteExperimentResult:
    """Run a two-uniform experiment with configurable payoff and strike."""
    marginal_1 = make_uniform_marginal(*x_interval, n, name="S1")
    marginal_2 = make_uniform_marginal(*y_interval, n, name="S2")
    payoff = make_builtin_payoff(payoff_name, strike=strike)

    unrestricted_benchmarks = None
    if payoff_name == "abs_spread":
        unrestricted_benchmarks = abs_spread_uniform_benchmarks(x_interval, y_interval)

    return run_discrete_experiment(
        marginal_1,
        marginal_2,
        payoff,
        eps_values=eps_values,
        sinkhorn_iterations=sinkhorn_iterations,
        sinkhorn_tolerance=sinkhorn_tolerance,
        unrestricted_benchmarks=unrestricted_benchmarks,
    )


def run_uniform_abs_spread_experiment(
    *,
    n: int = 50,
    eps_values: tuple[float, ...] = (),
    sinkhorn_iterations: int = 600,
    sinkhorn_tolerance: float = 1e-8,
) -> DiscreteExperimentResult:
    """Backward-compatible wrapper for the original reference experiment."""
    return run_two_uniform_experiment(
        n=n,
        payoff_name="abs_spread",
        strike=0.0,
        eps_values=eps_values,
        sinkhorn_iterations=sinkhorn_iterations,
        sinkhorn_tolerance=sinkhorn_tolerance,
    )
