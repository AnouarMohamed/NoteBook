"""Command-line entry points for reproducible MOT experiments."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt

from .experiments import run_two_uniform_experiment
from .payoffs import builtin_payoff_names


def _save_exact_plan(output_dir: Path, experiment) -> None:
    figure, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    diagonal_start = float(experiment.marginal_1.atoms[0])
    diagonal_end = float(experiment.marginal_1.atoms[-1])

    image = axes[0].imshow(
        experiment.exact_upper.plan.T,
        origin="lower",
        aspect="auto",
        extent=[
            experiment.marginal_1.atoms[0],
            experiment.marginal_1.atoms[-1],
            experiment.marginal_2.atoms[0],
            experiment.marginal_2.atoms[-1],
        ],
        cmap="YlOrRd",
        interpolation="nearest",
    )
    axes[0].plot(
        [diagonal_start, diagonal_end],
        [diagonal_start, diagonal_end],
        "k--",
        linewidth=1.0,
        label="martingale diagonal",
    )
    axes[0].set_title("Exact MOT upper plan")
    axes[0].set_xlabel("s1")
    axes[0].set_ylabel("s2")
    axes[0].legend(loc="upper left", fontsize=8)
    figure.colorbar(image, ax=axes[0])

    if experiment.unrestricted_benchmarks is not None:
        axes[1].bar(
            ["Lower", "Comonotone", "Independent", "Upper", "Countermonotone"],
            [
                experiment.exact_lower.value,
                experiment.unrestricted_benchmarks.unrestricted_min_comonotone,
                experiment.unrestricted_benchmarks.independent,
                experiment.exact_upper.value,
                experiment.unrestricted_benchmarks.unrestricted_max_countermonotone,
            ],
            color=["#8c6d31", "#6baed6", "#74c476", "#fd8d3c", "#cb181d"],
        )
        axes[1].set_title("Coupling benchmarks")
        axes[1].set_ylabel("Expected payoff")
        axes[1].tick_params(axis="x", rotation=20)
    else:
        payoff_image = axes[1].imshow(
            experiment.payoff_matrix.T,
            origin="lower",
            aspect="auto",
            extent=[
                experiment.marginal_1.atoms[0],
                experiment.marginal_1.atoms[-1],
                experiment.marginal_2.atoms[0],
                experiment.marginal_2.atoms[-1],
            ],
            cmap="Blues",
            interpolation="nearest",
        )
        axes[1].set_title(experiment.payoff.description)
        axes[1].set_xlabel("s1")
        axes[1].set_ylabel("s2")
        figure.colorbar(payoff_image, ax=axes[1])

    figure.suptitle(
        f"MOT example ({experiment.payoff.name}, n1={experiment.marginal_1.size}, n2={experiment.marginal_2.size})"
    )
    figure.tight_layout()
    figure.savefig(output_dir / "exact_uniform_summary.png", bbox_inches="tight")
    plt.close(figure)


def _save_regularization_path(output_dir: Path, experiment) -> None:
    if not experiment.regularized_results:
        return

    eps_values = sorted(experiment.regularized_results)
    expected_values = [
        experiment.regularized_results[eps].expected_payoff for eps in eps_values
    ]
    regularized_values = [
        experiment.regularized_results[eps].regularized_primal for eps in eps_values
    ]

    figure, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    axes[0].semilogx(eps_values, expected_values, "o-", linewidth=2, color="#3182bd")
    axes[0].axhline(
        experiment.exact_upper.value,
        color="#cb181d",
        linestyle="--",
        linewidth=1.5,
        label=f"exact LP = {experiment.exact_upper.value:.6f}",
    )
    axes[0].set_title("Expected payoff versus eps")
    axes[0].set_xlabel("eps")
    axes[0].set_ylabel("E[|S1-S2|]")
    axes[0].legend()
    axes[0].grid(alpha=0.3)

    axes[1].semilogx(
        eps_values,
        regularized_values,
        "o-",
        linewidth=2,
        color="#31a354",
        label="regularized primal",
    )
    axes[1].set_title("Regularized objective versus eps")
    axes[1].set_xlabel("eps")
    axes[1].set_ylabel("regularized objective")
    axes[1].grid(alpha=0.3)
    axes[1].legend()

    figure.tight_layout()
    figure.savefig(output_dir / "regularization_path.png", bbox_inches="tight")
    plt.close(figure)


def _write_summary_json(output_dir: Path, experiment) -> None:
    benchmarks = None
    if experiment.unrestricted_benchmarks is not None:
        benchmarks = {
            "unrestricted_min_comonotone": (
                experiment.unrestricted_benchmarks.unrestricted_min_comonotone
            ),
            "independent": experiment.unrestricted_benchmarks.independent,
            "unrestricted_max_countermonotone": (
                experiment.unrestricted_benchmarks.unrestricted_max_countermonotone
            ),
        }

    summary = {
        "marginal_1": {
            "name": experiment.marginal_1.name,
            "size": experiment.marginal_1.size,
            "mean": experiment.marginal_1.mean,
            "variance": experiment.marginal_1.variance,
        },
        "marginal_2": {
            "name": experiment.marginal_2.name,
            "size": experiment.marginal_2.size,
            "mean": experiment.marginal_2.mean,
            "variance": experiment.marginal_2.variance,
        },
        "payoff": {
            "name": experiment.payoff.name,
            "description": experiment.payoff.description,
            "strike": experiment.payoff.strike,
        },
        "convex_order": {
            "feasible": experiment.convex_order.feasible,
            "mean_gap": experiment.convex_order.mean_gap,
            "min_call_gap": experiment.convex_order.min_call_gap,
            "max_call_gap": experiment.convex_order.max_call_gap,
        },
        "exact_upper": {
            "value": experiment.exact_upper.value,
            "marginal_1_error": experiment.exact_upper.marginal_1_error,
            "marginal_2_error": experiment.exact_upper.marginal_2_error,
            "martingale_error": experiment.exact_upper.martingale_error,
        },
        "exact_lower": {
            "value": experiment.exact_lower.value,
            "marginal_1_error": experiment.exact_lower.marginal_1_error,
            "marginal_2_error": experiment.exact_lower.marginal_2_error,
            "martingale_error": experiment.exact_lower.martingale_error,
        },
        "benchmarks": benchmarks,
        "regularized": {
            f"{eps:g}": {
                "expected_payoff": result.expected_payoff,
                "regularized_primal": result.regularized_primal,
                "dual_value": result.dual_value,
                "dual_gap": result.dual_gap,
                "converged": result.converged,
                "iterations": result.iterations,
                "marginal_1_error": result.marginal_1_error,
                "marginal_2_error": result.marginal_2_error,
                "martingale_error": result.martingale_error,
            }
            for eps, result in sorted(experiment.regularized_results.items())
        },
    }
    (output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )


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

    _save_exact_plan(args.output_dir, experiment)
    _save_regularization_path(args.output_dir, experiment)
    _write_summary_json(args.output_dir, experiment)


if __name__ == "__main__":
    main()
