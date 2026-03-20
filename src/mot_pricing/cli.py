"""Command-line entry points for reproducible MOT experiments."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt

from .experiments import run_uniform_abs_spread_experiment


def _save_exact_plan(output_dir: Path, experiment) -> None:
    figure, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    image = axes[0].imshow(
        experiment.exact_upper.plan.T,
        origin="lower",
        aspect="auto",
        extent=[
            experiment.x_atoms[0],
            experiment.x_atoms[-1],
            experiment.y_atoms[0],
            experiment.y_atoms[-1],
        ],
        cmap="YlOrRd",
        interpolation="nearest",
    )
    axes[0].plot([1, 3], [1, 3], "k--", linewidth=1.0, label="martingale diagonal")
    axes[0].set_title("Exact MOT upper plan")
    axes[0].set_xlabel("s1")
    axes[0].set_ylabel("s2")
    axes[0].legend(loc="upper left", fontsize=8)
    figure.colorbar(image, ax=axes[0])

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

    figure.suptitle(f"Uniform MOT example (n={experiment.n})")
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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the uniform |S1-S2| martingale optimal transport experiment."
    )
    parser.add_argument("--n", type=int, default=50, help="number of midpoint atoms")
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

    experiment = run_uniform_abs_spread_experiment(
        n=args.n,
        eps_values=tuple(args.eps),
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)

    print("Exact MOT")
    print(f"  upper value: {experiment.exact_upper.value:.6f}")
    print(f"  lower value: {experiment.exact_lower.value:.6f}")
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


if __name__ == "__main__":
    main()
