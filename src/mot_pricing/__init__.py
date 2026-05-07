"""Utilities for robust pricing with martingale optimal transport."""

from .benchmarks import UniformAbsSpreadBenchmarks, abs_spread_uniform_benchmarks
from .causal_regularized import (
    CausalConstraintErrors,
    CausalMOTResult,
    causal_constraint_errors,
    causal_sinkhorn_mot,
    reconstruct_causal_plan,
)
from .continuous import ContinuousLimitResult, ot_bound_vs_timestep
from .discretization import make_uniform_grid
from .exact import (
    CausalBoundGap,
    ExactMOTResult,
    compute_causal_bound_gap,
    constraint_errors,
    solve_exact_causal_mot,
    solve_exact_mot,
)
from .experiments import (
    CausalExperimentResult,
    DiscreteExperimentResult,
    UniformExperimentResult,
    run_causal_experiment,
    run_discrete_experiment,
    run_two_uniform_experiment,
    run_uniform_abs_spread_experiment,
)
from .gallery import (
    GalleryEntry,
    GalleryRow,
    GallerySpec,
    builtin_gallery_specs,
    gallery_rows,
    run_gallery,
    save_gallery_assets,
)
from .marginals import (
    CausalFeasibilityReport,
    CausalMarginalChain,
    ConvexOrderCheck,
    DiscreteMarginal,
    check_causal_feasibility,
    check_convex_order_discrete,
    make_discrete_marginal,
    make_uniform_marginal,
)
from .payoffs import PayoffSpec, builtin_payoff_names, make_builtin_payoff
from .regularized import RegularizedMOTResult, sinkhorn_mot
from .reporting import (
    plot_continuous_limit,
    save_causal_experiment_artifacts,
    save_experiment_artifacts,
)

__version__ = "0.5.0"

__all__ = [
    "__version__",
    "CausalConstraintErrors",
    "CausalFeasibilityReport",
    "CausalMarginalChain",
    "CausalMOTResult",
    "CausalBoundGap",
    "CausalExperimentResult",
    "ContinuousLimitResult",
    "ConvexOrderCheck",
    "DiscreteExperimentResult",
    "DiscreteMarginal",
    "ExactMOTResult",
    "GalleryEntry",
    "GalleryRow",
    "GallerySpec",
    "PayoffSpec",
    "RegularizedMOTResult",
    "UniformAbsSpreadBenchmarks",
    "UniformExperimentResult",
    "abs_spread_uniform_benchmarks",
    "builtin_gallery_specs",
    "builtin_payoff_names",
    "causal_constraint_errors",
    "causal_sinkhorn_mot",
    "check_causal_feasibility",
    "check_convex_order_discrete",
    "compute_causal_bound_gap",
    "constraint_errors",
    "make_builtin_payoff",
    "make_discrete_marginal",
    "make_uniform_grid",
    "make_uniform_marginal",
    "ot_bound_vs_timestep",
    "plot_continuous_limit",
    "gallery_rows",
    "run_causal_experiment",
    "run_discrete_experiment",
    "run_gallery",
    "run_two_uniform_experiment",
    "run_uniform_abs_spread_experiment",
    "reconstruct_causal_plan",
    "save_experiment_artifacts",
    "save_causal_experiment_artifacts",
    "save_gallery_assets",
    "sinkhorn_mot",
    "solve_exact_causal_mot",
    "solve_exact_mot",
]
