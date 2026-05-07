"""Reproducible experiment runners for discrete and uniform MOT problems."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .benchmarks import UniformAbsSpreadBenchmarks, abs_spread_uniform_benchmarks
from .causal_regularized import CausalMOTResult, causal_sinkhorn_mot
from .exact import (
    CausalBoundGap,
    ExactMOTResult,
    solve_exact_causal_mot,
    solve_exact_mot,
)
from .marginals import (
    CausalFeasibilityReport,
    CausalMarginalChain,
    ConvexOrderCheck,
    DiscreteMarginal,
    check_causal_feasibility,
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


@dataclass(frozen=True)
class CausalExperimentResult:
    chain: CausalMarginalChain
    payoff: PayoffSpec
    feasibility: CausalFeasibilityReport
    exact_upper: ExactMOTResult
    exact_lower: ExactMOTResult
    pairwise_upper_bound: float
    pairwise_lower_bound: float
    causal_bound_gap: CausalBoundGap
    regularized_results: dict[float, CausalMOTResult]

    @property
    def step_count(self) -> int:
        return self.chain.step_count

    @property
    def per_step_plans(self) -> dict[float, tuple[np.ndarray, ...]]:
        return {
            eps: tuple(step.plan for step in result.steps)
            for eps, result in self.regularized_results.items()
        }


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


def _additive_causal_payoff(payoff: PayoffSpec):
    def additive_payoff(*grids):
        total = np.zeros_like(grids[0], dtype=float)
        for left, right in zip(grids[:-1], grids[1:]):
            total = total + payoff.function(left, right)
        return total

    return additive_payoff


def _pairwise_exact_bound(
    chain: CausalMarginalChain,
    payoff: PayoffSpec,
    objective: str,
) -> float:
    return float(
        sum(
            solve_exact_mot(
                marginal_1.atoms,
                marginal_1.weights,
                marginal_2.atoms,
                marginal_2.weights,
                payoff.function,
                objective=objective,
            ).value
            for marginal_1, marginal_2 in chain.pairs()
        )
    )


def run_causal_experiment(
    chain: CausalMarginalChain,
    payoff: PayoffSpec,
    *,
    eps_values: tuple[float, ...] = (),
    sinkhorn_iterations: int = 600,
    sinkhorn_tolerance: float = 1e-8,
) -> CausalExperimentResult:
    """Run exact and regularized causal MOT over a marginal chain."""
    feasibility = check_causal_feasibility(chain)
    if not feasibility.feasible:
        raise ValueError(f"causal chain is infeasible: {feasibility.summary}")

    causal_payoff = _additive_causal_payoff(payoff)
    exact_upper = solve_exact_causal_mot(
        chain,
        causal_payoff,
        objective="max",
    )
    exact_lower = solve_exact_causal_mot(
        chain,
        causal_payoff,
        objective="min",
    )
    pairwise_upper_bound = _pairwise_exact_bound(chain, payoff, "max")
    pairwise_lower_bound = _pairwise_exact_bound(chain, payoff, "min")
    causal_bound_gap = CausalBoundGap(
        absolute_gap=pairwise_upper_bound - exact_upper.value,
        relative_gap=(
            0.0
            if pairwise_upper_bound == 0.0
            else (pairwise_upper_bound - exact_upper.value) / abs(pairwise_upper_bound)
        ),
    )

    regularized_results: dict[float, CausalMOTResult] = {}
    for eps in eps_values:
        regularized_results[eps] = causal_sinkhorn_mot(
            chain,
            payoff.function,
            eps,
            n_iter=sinkhorn_iterations,
            tol=sinkhorn_tolerance,
        )

    return CausalExperimentResult(
        chain=chain,
        payoff=payoff,
        feasibility=feasibility,
        exact_upper=exact_upper,
        exact_lower=exact_lower,
        pairwise_upper_bound=pairwise_upper_bound,
        pairwise_lower_bound=pairwise_lower_bound,
        causal_bound_gap=causal_bound_gap,
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
