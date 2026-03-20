"""Utilities for robust pricing with martingale optimal transport."""

from .benchmarks import UniformAbsSpreadBenchmarks, abs_spread_uniform_benchmarks
from .discretization import make_uniform_grid
from .exact import ExactMOTResult, constraint_errors, solve_exact_mot
from .experiments import (
    DiscreteExperimentResult,
    UniformExperimentResult,
    run_discrete_experiment,
    run_two_uniform_experiment,
    run_uniform_abs_spread_experiment,
)
from .marginals import (
    ConvexOrderCheck,
    DiscreteMarginal,
    check_convex_order_discrete,
    make_discrete_marginal,
    make_uniform_marginal,
)
from .payoffs import PayoffSpec, builtin_payoff_names, make_builtin_payoff
from .regularized import RegularizedMOTResult, sinkhorn_mot

__version__ = "0.3.0"

__all__ = [
    "__version__",
    "ConvexOrderCheck",
    "DiscreteExperimentResult",
    "DiscreteMarginal",
    "ExactMOTResult",
    "PayoffSpec",
    "RegularizedMOTResult",
    "UniformAbsSpreadBenchmarks",
    "UniformExperimentResult",
    "abs_spread_uniform_benchmarks",
    "builtin_payoff_names",
    "check_convex_order_discrete",
    "constraint_errors",
    "make_builtin_payoff",
    "make_discrete_marginal",
    "make_uniform_grid",
    "make_uniform_marginal",
    "run_discrete_experiment",
    "run_two_uniform_experiment",
    "run_uniform_abs_spread_experiment",
    "sinkhorn_mot",
    "solve_exact_mot",
]
