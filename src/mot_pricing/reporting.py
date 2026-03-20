"""Artifact generation helpers for MOT experiments."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def save_exact_summary_plot(output_dir: Path, experiment) -> None:
    """Save the exact plan summary plot for a single experiment."""
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


def save_regularization_path_plot(output_dir: Path, experiment) -> None:
    """Save the regularization path figure for a single experiment."""
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
    axes[0].set_ylabel("E[payoff]")
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


def save_stability_diagnostics_plot(output_dir: Path, experiment) -> None:
    """Save a diagnostics figure that highlights convergence quality."""
    if not experiment.regularized_results:
        return

    eps_values = sorted(experiment.regularized_results)
    dual_gaps = [
        abs(experiment.regularized_results[eps].dual_gap) for eps in eps_values
    ]
    martingale_errors = [
        experiment.regularized_results[eps].martingale_error for eps in eps_values
    ]
    iterations = [
        experiment.regularized_results[eps].iterations for eps in eps_values
    ]

    figure, axes = plt.subplots(1, 3, figsize=(16, 4.5))

    axes[0].loglog(eps_values, dual_gaps, "o-", color="#756bb1", linewidth=2)
    axes[0].set_title("Absolute dual gap")
    axes[0].set_xlabel("eps")
    axes[0].set_ylabel("|dual - primal|")
    axes[0].grid(alpha=0.3, which="both")

    axes[1].loglog(
        eps_values,
        np.maximum(martingale_errors, np.full(len(martingale_errors), 1e-18)),
        "o-",
        color="#e6550d",
        linewidth=2,
    )
    axes[1].set_title("Martingale constraint error")
    axes[1].set_xlabel("eps")
    axes[1].set_ylabel("max row error")
    axes[1].grid(alpha=0.3, which="both")

    axes[2].semilogx(eps_values, iterations, "o-", color="#238b45", linewidth=2)
    axes[2].set_title("Iterations to converge")
    axes[2].set_xlabel("eps")
    axes[2].set_ylabel("iterations")
    axes[2].grid(alpha=0.3)

    figure.tight_layout()
    figure.savefig(output_dir / "stability_diagnostics.png", bbox_inches="tight")
    plt.close(figure)


def write_summary_json(output_dir: Path, experiment) -> None:
    """Write a machine-readable experiment summary."""
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


def save_experiment_artifacts(output_dir: Path, experiment) -> None:
    """Save all standard artifacts for a single experiment."""
    output_dir.mkdir(parents=True, exist_ok=True)
    save_exact_summary_plot(output_dir, experiment)
    save_regularization_path_plot(output_dir, experiment)
    save_stability_diagnostics_plot(output_dir, experiment)
    write_summary_json(output_dir, experiment)
