"""Command-line entry points for reproducible MOT experiments."""

from __future__ import annotations

import argparse
from pathlib import Path

from .experiments import run_causal_experiment, run_two_uniform_experiment
from .marginals import CausalMarginalChain
from .payoffs import builtin_payoff_names, make_builtin_payoff
from .reporting import save_causal_experiment_artifacts, save_experiment_artifacts


def build_parser() -> argparse.ArgumentParser:
    """
    Constructs an ArgumentParser configured for running two-uniform martingale optimal transport experiments.
    
    The parser includes options to set the number of midpoint atoms, the two support intervals (S1 and S2), a built-in payoff name and strike, a list of regularization strengths, and an output directory for generated artifacts.
    
    Returns:
        argparse.ArgumentParser: A configured parser for the two-uniform MOT experiment CLI.
    """
    parser = argparse.ArgumentParser(
        description="Run configurable two-uniform martingale optimal transport experiments."
    )
    parser.add_argument("--n", type=int, default=50, help="number of midpoint atoms")
    parser.add_argument(
        "--x-interval",
        nargs=2,
        type=float,
        default=[1.0, 3.0],
        metavar=("A", "B"),
        help="support interval for S1",
    )
    parser.add_argument(
        "--y-interval",
        nargs=2,
        type=float,
        default=[0.0, 4.0],
        metavar=("C", "D"),
        help="support interval for S2",
    )
    parser.add_argument(
        "--payoff",
        choices=list(builtin_payoff_names()),
        default="abs_spread",
        help="built-in payoff to evaluate",
    )
    parser.add_argument(
        "--strike",
        type=float,
        default=0.0,
        help="strike used by spread option payoffs",
    )
    parser.add_argument(
        "--eps",
        nargs="*",
        type=float,
        default=[1.0, 0.3, 0.1, 0.03, 0.01],
        help="regularization strengths to evaluate",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("artifacts"),
        help="directory used for generated figures",
    )
    return parser


def main() -> None:
    """
    Run the two-uniform MOT experiment from command-line arguments and save its artifacts.
    
    Parses CLI arguments, executes the configurable two-uniform experiment, ensures the configured output directory exists, prints summary results (exact bounds, payoff description, convex-order diagnostics, optional unrestricted benchmarks, and optional regularized results), and writes experiment artifacts to disk.
    """
    parser = build_parser()
    args = parser.parse_args()

    experiment = run_two_uniform_experiment(
        x_interval=tuple(args.x_interval),
        y_interval=tuple(args.y_interval),
        n=args.n,
        payoff_name=args.payoff,
        strike=args.strike,
        eps_values=tuple(args.eps),
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)

    print("Exact MOT")
    print(f"  upper value: {experiment.exact_upper.value:.6f}")
    print(f"  lower value: {experiment.exact_lower.value:.6f}")
    print(f"Payoff: {experiment.payoff.description}")
    print(
        "Convex order check: "
        f"feasible={experiment.convex_order.feasible}, "
        f"mean_gap={experiment.convex_order.mean_gap:.2e}, "
        f"min_call_gap={experiment.convex_order.min_call_gap:.2e}"
    )

    if experiment.unrestricted_benchmarks is not None:
        print("Unrestricted benchmarks")
        print(
            "  comonotone minimum: "
            f"{experiment.unrestricted_benchmarks.unrestricted_min_comonotone:.6f}"
        )
        print(f"  independent: {experiment.unrestricted_benchmarks.independent:.6f}")
        print(
            "  countermonotone maximum: "
            f"{experiment.unrestricted_benchmarks.unrestricted_max_countermonotone:.6f}"
        )

    if experiment.regularized_results:
        print("Regularized MOT")
        for eps, result in sorted(experiment.regularized_results.items()):
            print(
                f"  eps={eps:.4f}: expected={result.expected_payoff:.6f}, "
                f"regularized={result.regularized_primal:.6f}, "
                f"dual_gap={result.dual_gap:.2e}, converged={result.converged}"
            )

    save_experiment_artifacts(args.output_dir, experiment)


def _parse_interval(value: str) -> tuple[float, float]:
    """
    Parse an interval string of the form "A,B" into a pair of floats.
    
    Parameters:
        value (str): Interval formatted as "A,B" where A and B are numeric.
    
    Returns:
        tuple[float, float]: The parsed interval bounds (A, B).
    
    Raises:
        argparse.ArgumentTypeError: If the input is not exactly two comma-separated parts or if either bound cannot be converted to float.
    """
    parts = value.split(",")
    if len(parts) != 2:
        raise argparse.ArgumentTypeError("intervals must be formatted as a,b")
    try:
        return float(parts[0]), float(parts[1])
    except ValueError as exc:
        raise argparse.ArgumentTypeError("interval bounds must be numeric") from exc


def build_causal_parser() -> argparse.ArgumentParser:
    """
    Create an ArgumentParser configured for causal multi-period martingale optimal transport (MOT) experiments.
    
    The parser includes options for atoms per time step (`--n`), per-time-step support intervals (`--intervals`, each formatted as "A,B" and parsed by `_parse_interval`), built-in payoff selection (`--payoff`), payoff strike (`--strike`), regularization strengths (`--eps`), and an output directory (`--output-dir`).
    
    Returns:
        argparse.ArgumentParser: Configured parser for the causal experimental CLI.
    """
    parser = argparse.ArgumentParser(
        description="Run causal multi-period martingale optimal transport experiments."
    )
    parser.add_argument("--n", type=int, default=30, help="atoms per time step")
    parser.add_argument(
        "--intervals",
        nargs="+",
        type=_parse_interval,
        default=[(1.0, 3.0), (0.5, 3.5), (0.0, 4.0)],
        metavar="A,B",
        help="one interval per time step, formatted as a,b",
    )
    parser.add_argument(
        "--payoff",
        choices=list(builtin_payoff_names()),
        default="abs_spread",
        help="built-in adjacent-step payoff to evaluate",
    )
    parser.add_argument(
        "--strike",
        type=float,
        default=0.0,
        help="strike used by spread option payoffs",
    )
    parser.add_argument(
        "--eps",
        nargs="*",
        type=float,
        default=[0.3, 0.1, 0.03],
        help="regularization strengths to evaluate",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("causal_artifacts"),
        help="directory used for generated causal artifacts",
    )
    return parser


def main_causal() -> None:
    """
    Run a causal multi-period MOT experiment driven by command-line arguments.
    
    Parses CLI options, constructs a causal marginal chain and payoff, executes the causal experiment for the requested regularization strengths, prints exact and regularized summary statistics (exact lower/upper values, pairwise upper benchmark, causal gap, and per-epsilon expected payoff and convergence), and writes experiment artifacts to the configured output directory.
    """
    parser = build_causal_parser()
    args = parser.parse_args()
    interval_specs = tuple((a, b, args.n) for a, b in args.intervals)
    chain = CausalMarginalChain.from_uniform_intervals(interval_specs)
    payoff = make_builtin_payoff(args.payoff, strike=args.strike)
    experiment = run_causal_experiment(
        chain,
        payoff,
        eps_values=tuple(args.eps),
    )

    print("Exact causal MOT")
    print(f"  lower value: {experiment.exact_lower.value:.6f}")
    print(f"  upper value: {experiment.exact_upper.value:.6f}")
    print(f"  pairwise upper benchmark: {experiment.pairwise_upper_bound:.6f}")
    print(
        "  causal gap to pairwise upper: "
        f"{experiment.causal_bound_gap.absolute_gap:.6f}"
    )
    if experiment.regularized_results:
        print("Regularized causal MOT")
        for eps, result in sorted(experiment.regularized_results.items()):
            print(
                f"  eps={eps:.4f}: expected={result.overall_expected_payoff:.6f}, "
                f"converged={result.converged}"
            )

    save_causal_experiment_artifacts(args.output_dir, experiment)


if __name__ == "__main__":
    main()
