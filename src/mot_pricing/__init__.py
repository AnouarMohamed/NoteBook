"""Utilities for robust pricing with martingale optimal transport."""

from .benchmarks import UniformAbsSpreadBenchmarks, abs_spread_uniform_benchmarks
from .discretization import make_uniform_grid
from .exact import ExactMOTResult, constraint_errors, solve_exact_mot
from .experiments import UniformExperimentResult, run_uniform_abs_spread_experiment
from .regularized import RegularizedMOTResult, sinkhorn_mot

__all__ = [
    "ExactMOTResult",
    "RegularizedMOTResult",
    "UniformAbsSpreadBenchmarks",
    "UniformExperimentResult",
    "abs_spread_uniform_benchmarks",
    "constraint_errors",
    "make_uniform_grid",
    "run_uniform_abs_spread_experiment",
    "sinkhorn_mot",
    "solve_exact_mot",
]
