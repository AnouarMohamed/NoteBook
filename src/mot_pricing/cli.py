"""Command-line entry points for reproducible MOT experiments."""

from __future__ import annotations

import argparse
from pathlib import Path

from .experiments import run_two_uniform_experiment
from .payoffs import builtin_payoff_names
from .reporting import save_experiment_artifacts


def build_parser() -> argparse.ArgumentParser:
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


if __name__ == "__main__":
    main()
