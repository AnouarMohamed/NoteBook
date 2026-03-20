"""Reproducible experiments for the reference uniform robust pricing problem."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .benchmarks import UniformAbsSpreadBenchmarks, abs_spread_uniform_benchmarks
from .discretization import make_uniform_grid
from .exact import ExactMOTResult, solve_exact_mot
from .regularized import RegularizedMOTResult, sinkhorn_mot


@dataclass(frozen=True)
class UniformExperimentResult:
    n: int
    x_atoms: np.ndarray
    alpha: np.ndarray
    y_atoms: np.ndarray
    beta: np.ndarray
    payoff_matrix: np.ndarray
    exact_upper: ExactMOTResult
    exact_lower: ExactMOTResult
    unrestricted_benchmarks: UniformAbsSpreadBenchmarks
    regularized_results: dict[float, RegularizedMOTResult]


def run_uniform_abs_spread_experiment(
    *,
    n: int = 50,
    eps_values: tuple[float, ...] = (),
    sinkhorn_iterations: int = 600,
    sinkhorn_tolerance: float = 1e-8,
) -> UniformExperimentResult:
    """Run the uniform abs-spread example end to end."""
    x_atoms, alpha = make_uniform_grid(1.0, 3.0, n)
    y_atoms, beta = make_uniform_grid(0.0, 4.0, n)

    payoff_fn = lambda x_grid, y_grid: np.abs(x_grid - y_grid)
    exact_upper = solve_exact_mot(
        x_atoms, alpha, y_atoms, beta, payoff_fn, objective="max"
    )
    exact_lower = solve_exact_mot(
        x_atoms, alpha, y_atoms, beta, payoff_fn, objective="min"
    )
    unrestricted_benchmarks = abs_spread_uniform_benchmarks((1.0, 3.0), (0.0, 4.0))

    regularized_results: dict[float, RegularizedMOTResult] = {}
    for eps in eps_values:
        regularized_results[eps] = sinkhorn_mot(
            x_atoms,
            alpha,
            y_atoms,
            beta,
            exact_upper.payoff_matrix,
            eps,
            n_iter=sinkhorn_iterations,
            tol=sinkhorn_tolerance,
        )

    return UniformExperimentResult(
        n=n,
        x_atoms=x_atoms,
        alpha=alpha,
        y_atoms=y_atoms,
        beta=beta,
        payoff_matrix=exact_upper.payoff_matrix,
        exact_upper=exact_upper,
        exact_lower=exact_lower,
        unrestricted_benchmarks=unrestricted_benchmarks,
        regularized_results=regularized_results,
    )
