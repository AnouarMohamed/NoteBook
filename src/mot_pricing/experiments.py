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
        """
        Number of steps in the causal marginal chain.
        
        Returns:
            int: The chain's step count.
        """
        return self.chain.step_count

    @property
    def per_step_plans(self) -> dict[float, tuple[np.ndarray, ...]]:
        """
        Mapping from each regularization `eps` to the per-step transport plans for that result.
        
        For every entry in `self.regularized_results`, extracts the `plan` array from each step in `result.steps` and returns them as a tuple.
        
        Returns:
            dict[float, tuple[np.ndarray, ...]]: Mapping from regularization epsilon to a tuple of per-step plan arrays (one ndarray per chain step).
        """
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
    """
    Run an exact and (optionally) regularized MOT experiment for two discrete marginals.
    
    Computes a discrete convex-order feasibility check and, if feasible, solves the exact
    maximization and minimization MOT problems for the provided payoff. For each value in
    `eps_values` runs a Sinkhorn regularized solve using the payoff matrix from the exact
    upper solve and returns a mapping of `eps -> RegularizedMOTResult`.
    
    Parameters:
        marginal_1 (DiscreteMarginal): First discrete marginal (atoms and weights).
        marginal_2 (DiscreteMarginal): Second discrete marginal (atoms and weights).
        payoff (PayoffSpec): Payoff specification whose `.function` is applied to atom grids.
        eps_values (tuple[float, ...], optional): Regularization strengths for which to run
            Sinkhorn; defaults to empty tuple (no regularized runs).
        sinkhorn_iterations (int, optional): Maximum iterations passed to the Sinkhorn solver.
        sinkhorn_tolerance (float, optional): Convergence tolerance passed to the Sinkhorn solver.
        unrestricted_benchmarks (UniformAbsSpreadBenchmarks | None, optional): Optional
            precomputed unrestricted benchmarks (used for uniform abs-spread experiments).
    
    Returns:
        DiscreteExperimentResult: Result container with the input marginals and payoff,
        the convex-order check, exact upper/lower solutions, the payoff matrix from the
        exact upper solve, optional unrestricted benchmarks, and a mapping of regularized
        results keyed by `eps`.
    
    Raises:
        ValueError: If the discrete convex-order check reports infeasibility (no martingale
            coupling), with `mean_gap` and `min_call_gap` reported in the error message.
    """
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
    """
    Create an additive payoff function that applies a pairwise payoff across adjacent grids and sums the results.
    
    Parameters:
        payoff (PayoffSpec): A payoff specification with a `function(left_grid, right_grid)` that returns an array compatible with the input grids.
    
    Returns:
        callable: A function `additive_payoff(*grids)` that returns an array equal to the elementwise sum of `payoff.function(left, right)` evaluated on each adjacent pair of `grids`.
    """
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
    """
    Compute the sum of exact pairwise MOT objective values across adjacent marginals in a causal chain.
    
    Parameters:
        chain (CausalMarginalChain): Marginal chain whose adjacent pairs will be solved.
        payoff (PayoffSpec): Payoff specification applied to each pair.
        objective (str): Objective direction for each pair, e.g., "max" or "min".
    
    Returns:
        float: Sum of the exact MOT objective values for each adjacent pair in the chain.
    """
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
    """
    Run exact and regularized causal MOT on a marginal chain using a pairwise additive payoff.
    
    Parameters:
        chain (CausalMarginalChain): Marginal chain describing the causal/martingale structure across steps.
        payoff (PayoffSpec): Payoff applied pairwise and summed across adjacent steps of the chain.
        eps_values (tuple[float, ...], optional): Regularization strengths for which to run causal Sinkhorn; each value is used to compute and store a `CausalMOTResult`. Defaults to ().
        sinkhorn_iterations (int, optional): Maximum Sinkhorn iterations for each regularized solve. Defaults to 600.
        sinkhorn_tolerance (float, optional): Convergence tolerance for Sinkhorn iterations. Defaults to 1e-8.
    
    Returns:
        CausalExperimentResult: Contains the input chain and payoff, causal feasibility report, exact upper and lower causal MOT solutions, per-pair exact upper and lower bounds, the computed causal bound gap (absolute and relative), and a mapping of `eps` to regularized `CausalMOTResult` objects.
    
    Raises:
        ValueError: If the causal feasibility check fails; the exception message includes `feasibility.summary`.
    """
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
    """
    Run a two-uniform discrete MOT experiment using built-in payoff specifications.
    
    Parameters:
        x_interval (tuple[float, float]): Interval (min, max) for the first uniform marginal.
        y_interval (tuple[float, float]): Interval (min, max) for the second uniform marginal.
        n (int): Number of support points (atoms) for each discrete uniform marginal.
        payoff_name (str): Name of a built-in payoff to use (e.g., "abs_spread").
        strike (float): Strike parameter passed to the payoff constructor.
        eps_values (tuple[float, ...]): Sequence of entropic regularization strengths for which to run Sinkhorn; empty tuple disables regularized runs.
        sinkhorn_iterations (int): Maximum iterations for Sinkhorn solver when running regularized experiments.
        sinkhorn_tolerance (float): Convergence tolerance for the Sinkhorn solver.
    
    Returns:
        DiscreteExperimentResult: Results containing the two marginals, payoff, exact upper/lower solutions, payoff matrix from the exact upper solve, optional unrestricted benchmarks (for the "abs_spread" payoff), and a mapping of `eps ->` regularized results.
    """
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
