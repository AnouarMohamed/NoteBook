"""Artifact generation helpers for MOT experiments."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from .marginals import call_prices


def _conditional_std_from_plan(plan: np.ndarray, y_atoms: np.ndarray) -> np.ndarray:
    row_totals = plan.sum(axis=1)
    safe_totals = np.where(row_totals > 0.0, row_totals, 1.0)
    conditional_mean = (plan @ y_atoms) / safe_totals
    conditional_second = (plan @ (y_atoms**2)) / safe_totals
    variance = np.maximum(conditional_second - conditional_mean**2, 0.0)
    conditional_std = np.sqrt(variance)
    return np.where(row_totals > 0.0, conditional_std, np.nan)


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


def save_structural_diagnostics_plot(output_dir: Path, experiment) -> None:
    """Save plots that describe marginals, conditional dispersion, and convex order."""
    figure, axes = plt.subplots(1, 3, figsize=(16, 4.5))

    axes[0].plot(
        experiment.marginal_1.atoms,
        experiment.marginal_1.weights,
        "o-",
        linewidth=2,
        color="#3182bd",
        label=experiment.marginal_1.name or "marginal 1",
    )
    axes[0].plot(
        experiment.marginal_2.atoms,
        experiment.marginal_2.weights,
        "s-",
        linewidth=2,
        color="#e6550d",
        label=experiment.marginal_2.name or "marginal 2",
    )
    axes[0].set_title("Discrete marginals")
    axes[0].set_xlabel("atom")
    axes[0].set_ylabel("weight")
    axes[0].grid(alpha=0.3)
    axes[0].legend()

    x_atoms = experiment.marginal_1.atoms
    y_atoms = experiment.marginal_2.atoms
    axes[1].plot(
        x_atoms,
        _conditional_std_from_plan(experiment.exact_lower.plan, y_atoms),
        "o-",
        linewidth=2,
        color="#8c6d31",
        label="exact lower",
    )
    axes[1].plot(
        x_atoms,
        _conditional_std_from_plan(experiment.exact_upper.plan, y_atoms),
        "o-",
        linewidth=2,
        color="#756bb1",
        label="exact upper",
    )
    if experiment.regularized_results:
        smallest_eps = min(experiment.regularized_results)
        axes[1].plot(
            x_atoms,
            _conditional_std_from_plan(
                experiment.regularized_results[smallest_eps].plan,
                y_atoms,
            ),
            "o--",
            linewidth=1.8,
            color="#31a354",
            label=f"regularized eps={smallest_eps:g}",
        )
    axes[1].set_title("Conditional standard deviation")
    axes[1].set_xlabel("s1")
    axes[1].set_ylabel("std[S2 | S1 = s1]")
    axes[1].grid(alpha=0.3)
    axes[1].legend(fontsize=8)

    call_gap = call_prices(experiment.marginal_2, experiment.convex_order.strikes) - call_prices(
        experiment.marginal_1, experiment.convex_order.strikes
    )
    axes[2].plot(
        experiment.convex_order.strikes,
        call_gap,
        linewidth=2,
        color="#dd1c77",
    )
    axes[2].axhline(0.0, color="black", linestyle="--", linewidth=1.0)
    axes[2].set_title("Convex-order call gap")
    axes[2].set_xlabel("strike")
    axes[2].set_ylabel("C_mu2(K) - C_mu1(K)")
    axes[2].grid(alpha=0.3)

    figure.tight_layout()
    figure.savefig(output_dir / "structural_diagnostics.png", bbox_inches="tight")
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


def write_experiment_markdown(output_dir: Path, experiment) -> None:
    """Write a compact markdown report for a single experiment."""
    lines = [
        f"# Experiment Report: {experiment.payoff.description}",
        "",
        "## Setup",
        "",
        f"- marginal 1: `{experiment.marginal_1.name or 'S1'}` with support size `{experiment.marginal_1.size}`",
        f"- marginal 2: `{experiment.marginal_2.name or 'S2'}` with support size `{experiment.marginal_2.size}`",
        f"- payoff: `{experiment.payoff.name}`",
        f"- strike: `{experiment.payoff.strike:.6f}`",
        "",
        "## Marginal Moments",
        "",
        "| Marginal | Mean | Variance |",
        "|---|---:|---:|",
        (
            f"| `{experiment.marginal_1.name or 'S1'}` | {experiment.marginal_1.mean:.6f} | "
            f"{experiment.marginal_1.variance:.6f} |"
        ),
        (
            f"| `{experiment.marginal_2.name or 'S2'}` | {experiment.marginal_2.mean:.6f} | "
            f"{experiment.marginal_2.variance:.6f} |"
        ),
        "",
        "## Exact Bounds",
        "",
        "| Objective | Value | Marginal-1 error | Marginal-2 error | Martingale error |",
        "|---|---:|---:|---:|---:|",
        (
            f"| lower | {experiment.exact_lower.value:.6f} | "
            f"{experiment.exact_lower.marginal_1_error:.2e} | "
            f"{experiment.exact_lower.marginal_2_error:.2e} | "
            f"{experiment.exact_lower.martingale_error:.2e} |"
        ),
        (
            f"| upper | {experiment.exact_upper.value:.6f} | "
            f"{experiment.exact_upper.marginal_1_error:.2e} | "
            f"{experiment.exact_upper.marginal_2_error:.2e} | "
            f"{experiment.exact_upper.martingale_error:.2e} |"
        ),
        "",
        "## Convex-Order Diagnostic",
        "",
        f"- feasible: `{experiment.convex_order.feasible}`",
        f"- mean gap: `{experiment.convex_order.mean_gap:.2e}`",
        f"- minimum call gap: `{experiment.convex_order.min_call_gap:.2e}`",
        f"- maximum call gap: `{experiment.convex_order.max_call_gap:.2e}`",
    ]

    if experiment.unrestricted_benchmarks is not None:
        lines.extend(
            [
                "",
                "## Unrestricted Benchmarks",
                "",
                "| Benchmark | Value |",
                "|---|---:|",
                (
                    f"| comonotone minimum | "
                    f"{experiment.unrestricted_benchmarks.unrestricted_min_comonotone:.6f} |"
                ),
                f"| independent | {experiment.unrestricted_benchmarks.independent:.6f} |",
                (
                    f"| countermonotone maximum | "
                    f"{experiment.unrestricted_benchmarks.unrestricted_max_countermonotone:.6f} |"
                ),
            ]
        )

    if experiment.regularized_results:
        lines.extend(
            [
                "",
                "## Regularized Runs",
                "",
                "| eps | Expected payoff | Regularized primal | Dual gap | Iterations | Converged |",
                "|---:|---:|---:|---:|---:|---:|",
            ]
        )
        for eps, result in sorted(experiment.regularized_results.items()):
            lines.append(
                f"| {eps:g} | {result.expected_payoff:.6f} | {result.regularized_primal:.6f} | "
                f"{result.dual_gap:+.2e} | {result.iterations} | {result.converged} |"
            )

    lines.extend(
        [
            "",
            "## Artifact Files",
            "",
            "- `exact_uniform_summary.png`",
            "- `regularization_path.png`",
            "- `stability_diagnostics.png`",
            "- `structural_diagnostics.png`",
            "- `summary.json`",
        ]
    )

    (output_dir / "experiment_report.md").write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


def save_experiment_artifacts(output_dir: Path, experiment) -> None:
    """Save all standard artifacts for a single experiment."""
    output_dir.mkdir(parents=True, exist_ok=True)
    save_exact_summary_plot(output_dir, experiment)
    save_regularization_path_plot(output_dir, experiment)
    save_stability_diagnostics_plot(output_dir, experiment)
    save_structural_diagnostics_plot(output_dir, experiment)
    write_summary_json(output_dir, experiment)
    write_experiment_markdown(output_dir, experiment)


def plot_causal_transport_chain(output_dir: Path, result) -> None:
    """
    Save a grid of per-step causal transport heatmaps to causal_transport_chain.png in output_dir.
    
    Creates one subplot per step showing the (step, step+1) coupling plan over the atom ranges of the corresponding marginals. If regularized results are available, uses the plans from the smallest regularization epsilon; otherwise aggregates the exact plan to each adjacent pair of time steps.
    
    Parameters:
        output_dir (Path): Directory where causal_transport_chain.png will be written.
        result: Result object containing a time chain and coupling data. Expected attributes:
            - chain.marginals: sequence of marginals where each marginal has `atoms` (1-D array-like).
            - chain.step_count (int): number of steps (subplots).
            - regularized_results (optional): mapping of eps -> regularization result, where the chosen entry should provide `.steps[*].plan`.
            - exact_upper.plan: fallback multidimensional coupling used when regularized results are not present.
    """
    plans = []
    if result.regularized_results:
        smallest_eps = min(result.regularized_results)
        plans = [step.plan for step in result.regularized_results[smallest_eps].steps]
    else:
        plan = result.exact_upper.plan
        for step in range(result.chain.step_count):
            axes = tuple(
                axis for axis in range(plan.ndim) if axis not in {step, step + 1}
            )
            plans.append(plan.sum(axis=axes) if axes else plan)

    figure, axes = plt.subplots(
        1, result.step_count, figsize=(5 * result.step_count, 4.5)
    )
    axes_array = np.atleast_1d(axes)
    for step, (axis, plan) in enumerate(zip(axes_array, plans), start=1):
        marginal_1, marginal_2 = result.chain.marginals[step - 1 : step + 1]
        image = axis.imshow(
            plan.T,
            origin="lower",
            aspect="auto",
            extent=[
                marginal_1.atoms[0],
                marginal_1.atoms[-1],
                marginal_2.atoms[0],
                marginal_2.atoms[-1],
            ],
            cmap="YlGnBu",
            interpolation="nearest",
        )
        axis.set_title(f"S{step} to S{step + 1}")
        axis.set_xlabel(f"s{step}")
        axis.set_ylabel(f"s{step + 1}")
        figure.colorbar(image, ax=axis)
    figure.tight_layout()
    figure.savefig(output_dir / "causal_transport_chain.png", bbox_inches="tight")
    plt.close(figure)


def plot_causal_bound_convergence(output_dir: Path, result) -> None:
    """
    Plot and save the convergence of the causal bound as a function of regularization strength.
    
    Creates a semilog-x plot of the overall expected payoff from each regularized run versus epsilon, overlays a horizontal reference at the exact causal upper bound, and writes the figure to "causal_bound_convergence.png" in output_dir. If result.regularized_results is empty or falsy, the function does nothing.
    
    Parameters:
        output_dir (Path): Directory where the PNG file will be saved.
        result: Experiment/result object with attributes
            - regularized_results: a mapping from epsilon to per-epsilon results containing `overall_expected_payoff`.
            - exact_upper.value: numeric exact causal upper bound used for the reference line.
    """
    if not result.regularized_results:
        return
    eps_values = sorted(result.regularized_results)
    expected = [
        result.regularized_results[eps].overall_expected_payoff for eps in eps_values
    ]
    figure, axis = plt.subplots(figsize=(7, 4.5))
    axis.semilogx(eps_values, expected, "o-", linewidth=2, color="#3182bd")
    axis.axhline(
        result.exact_upper.value,
        linestyle="--",
        linewidth=1.5,
        color="#cb181d",
        label=f"exact causal upper = {result.exact_upper.value:.6f}",
    )
    axis.set_title("Causal bound convergence")
    axis.set_xlabel("eps")
    axis.set_ylabel("expected payoff")
    axis.grid(alpha=0.3)
    axis.legend()
    figure.tight_layout()
    figure.savefig(output_dir / "causal_bound_convergence.png", bbox_inches="tight")
    plt.close(figure)


def plot_marginal_evolution(output_dir: Path, result) -> None:
    """
    Plot the evolution of marginal distributions across causal time steps and save the figure.
    
    Parameters:
        output_dir (Path): Directory where "marginal_evolution.png" will be written.
        result: Object containing a `chain.marginals` sequence; each marginal must provide
            `atoms` (array-like), `weights` (array-like), and an optional `name` (str) used
            for the plot legend.
    """
    figure, axis = plt.subplots(figsize=(8, 4.5))
    for index, marginal in enumerate(result.chain.marginals, start=1):
        axis.plot(
            marginal.atoms,
            marginal.weights,
            "o-",
            linewidth=2,
            label=marginal.name or f"S{index}",
        )
    axis.set_title("Marginal evolution")
    axis.set_xlabel("atom")
    axis.set_ylabel("weight")
    axis.grid(alpha=0.3)
    axis.legend()
    figure.tight_layout()
    figure.savefig(output_dir / "marginal_evolution.png", bbox_inches="tight")
    plt.close(figure)


def plot_causal_vs_unconstrained(output_dir: Path, result) -> None:
    """
    Save a bar chart comparing causal and pairwise bounds for the experiment.
    
    Parameters:
        output_dir (Path): Directory where "causal_vs_unconstrained.png" will be written.
        result: Result object providing `pairwise_lower_bound`, `exact_lower.value`, `exact_upper.value`, and `pairwise_upper_bound` used to build the bars.
    """
    labels = ["pairwise lower", "causal lower", "causal upper", "pairwise upper"]
    values = [
        result.pairwise_lower_bound,
        result.exact_lower.value,
        result.exact_upper.value,
        result.pairwise_upper_bound,
    ]
    figure, axis = plt.subplots(figsize=(8, 4.5))
    axis.bar(labels, values, color=["#9ecae1", "#74c476", "#fd8d3c", "#756bb1"])
    axis.set_title("Causal vs pairwise bounds")
    axis.set_ylabel("expected payoff")
    axis.tick_params(axis="x", rotation=15)
    axis.grid(alpha=0.3, axis="y")
    figure.tight_layout()
    figure.savefig(output_dir / "causal_vs_unconstrained.png", bbox_inches="tight")
    plt.close(figure)


def write_causal_summary_json(output_dir: Path, result) -> None:
    """
    Write a machine-readable JSON summary of a causal experiment to output_dir/causal_summary.json.
    
    The JSON contains:
    - step_count: number of time steps in the causal chain.
    - payoff: object with `name`, `description`, and `strike`.
    - marginals: list of marginal metadata objects (`name`, `size`, `mean`, `variance`) for each time step.
    - feasibility: feasibility flag and arrays converted to lists (`mean_gaps`, `min_call_gaps`, `max_call_gaps`) plus a textual `summary`.
    - exact: exact causal bounds (`lower`, `upper`) and `martingale_error`.
    - pairwise_bounds: unconstrained pairwise lower and upper bounds.
    - causal_bound_gap: `absolute` and `relative` gap between pairwise and causal bounds.
    - regularized: mapping keyed by formatted epsilon strings to objects containing `overall_expected_payoff`, `converged`, `per_step_dual_gap` (as a list), and maximum constraint errors (`max_marginal_error`, `max_martingale_error`).
    """
    summary = {
        "step_count": result.step_count,
        "payoff": {
            "name": result.payoff.name,
            "description": result.payoff.description,
            "strike": result.payoff.strike,
        },
        "marginals": [
            {
                "name": marginal.name,
                "size": marginal.size,
                "mean": marginal.mean,
                "variance": marginal.variance,
            }
            for marginal in result.chain.marginals
        ],
        "feasibility": {
            "feasible": result.feasibility.feasible,
            "mean_gaps": result.feasibility.mean_gaps.tolist(),
            "min_call_gaps": result.feasibility.min_call_gaps.tolist(),
            "max_call_gaps": result.feasibility.max_call_gaps.tolist(),
            "summary": result.feasibility.summary,
        },
        "exact": {
            "lower": result.exact_lower.value,
            "upper": result.exact_upper.value,
            "martingale_error": result.exact_upper.martingale_error,
        },
        "pairwise_bounds": {
            "lower": result.pairwise_lower_bound,
            "upper": result.pairwise_upper_bound,
        },
        "causal_bound_gap": {
            "absolute": result.causal_bound_gap.absolute_gap,
            "relative": result.causal_bound_gap.relative_gap,
        },
        "regularized": {
            f"{eps:g}": {
                "overall_expected_payoff": regularized.overall_expected_payoff,
                "converged": regularized.converged,
                "per_step_dual_gap": regularized.per_step_dual_gap.tolist(),
                "max_marginal_error": regularized.constraint_errors.max_marginal_error,
                "max_martingale_error": regularized.constraint_errors.max_martingale_error,
            }
            for eps, regularized in sorted(result.regularized_results.items())
        },
    }
    (output_dir / "causal_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )


def write_causal_experiment_markdown(output_dir: Path, result) -> None:
    """Write a compact markdown report for a causal experiment."""
    lines = [
        f"# Causal Experiment Report: {result.payoff.description}",
        "",
        "## Setup",
        "",
        f"- steps: `{result.step_count}`",
        f"- payoff: `{result.payoff.name}`",
        f"- feasibility: `{result.feasibility.feasible}`",
        "",
        "## Exact Bounds",
        "",
        "| Bound | Value |",
        "|---|---:|",
        f"| causal lower | {result.exact_lower.value:.6f} |",
        f"| causal upper | {result.exact_upper.value:.6f} |",
        f"| pairwise lower | {result.pairwise_lower_bound:.6f} |",
        f"| pairwise upper | {result.pairwise_upper_bound:.6f} |",
        "",
        "## Causal Bound Gap",
        "",
        f"- absolute: `{result.causal_bound_gap.absolute_gap:.6f}`",
        f"- relative: `{result.causal_bound_gap.relative_gap:.6f}`",
    ]
    if result.regularized_results:
        lines.extend(
            [
                "",
                "## Regularized Runs",
                "",
                "| eps | Expected payoff | Max marginal error | Max martingale error | Converged |",
                "|---:|---:|---:|---:|---:|",
            ]
        )
        for eps, regularized in sorted(result.regularized_results.items()):
            lines.append(
                f"| {eps:g} | {regularized.overall_expected_payoff:.6f} | "
                f"{regularized.constraint_errors.max_marginal_error:.2e} | "
                f"{regularized.constraint_errors.max_martingale_error:.2e} | "
                f"{regularized.converged} |"
            )
    lines.extend(
        [
            "",
            "## Artifact Files",
            "",
            "- `causal_transport_chain.png`",
            "- `causal_bound_convergence.png`",
            "- `marginal_evolution.png`",
            "- `causal_vs_unconstrained.png`",
            "- `causal_summary.json`",
        ]
    )
    (output_dir / "causal_experiment_report.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def save_causal_experiment_artifacts(output_dir: Path, result) -> None:
    """
    Save all standard artifacts for a causal (multi-step) MOT experiment into output_dir.
    
    This creates plots and reports used for analysis and reproducibility. Generated files:
    - causal_transport_chain.png
    - causal_bound_convergence.png (only if regularized results exist)
    - marginal_evolution.png
    - causal_vs_unconstrained.png
    - causal_summary.json
    - causal_experiment_report.md
    
    Parameters:
        output_dir (Path): Directory where artifacts will be written; created if it does not exist.
        result: Causal experiment result object containing chain, bounds, regularized results, and payoff metadata.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    plot_causal_transport_chain(output_dir, result)
    plot_causal_bound_convergence(output_dir, result)
    plot_marginal_evolution(output_dir, result)
    plot_causal_vs_unconstrained(output_dir, result)
    write_causal_summary_json(output_dir, result)
    write_causal_experiment_markdown(output_dir, result)


def plot_continuous_limit(output_dir: Path, result) -> None:
    """
    Create and save a plot showing causal upper and lower bounds across time discretizations with an inset visualizing the width convergence.
    
    Parameters:
        output_dir (Path): Directory where "continuous_limit.png" will be written; the directory is created if it does not exist.
        result: Object providing the plotting data with the following attributes:
            - T_values: sequence of time-discretization sizes (plotted on a log-x scale).
            - upper_bounds: sequence of upper bound values corresponding to T_values.
            - lower_bounds: sequence of lower bound values corresponding to T_values.
            - payoff_name: string identifier used to conditionally add a finest-grid horizontal reference (expects "abs_spread" for that behavior).
            - convergence_rate: numeric value displayed in the inset title describing the observed convergence slope.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    widths = result.upper_bounds - result.lower_bounds

    figure, axis = plt.subplots(figsize=(8, 5))
    axis.semilogx(
        result.T_values,
        result.upper_bounds,
        "o-",
        linewidth=2,
        color="#cb181d",
        label="upper",
    )
    axis.semilogx(
        result.T_values,
        result.lower_bounds,
        "s-",
        linewidth=2,
        color="#3182bd",
        label="lower",
    )
    if result.payoff_name == "abs_spread" and len(result.upper_bounds) > 0:
        axis.axhline(
            result.upper_bounds[-1],
            linestyle="--",
            linewidth=1.0,
            color="#636363",
            label="finest grid reference",
        )
    axis.set_title("Causal bounds versus time discretization")
    axis.set_xlabel("time steps")
    axis.set_ylabel("expected payoff")
    axis.grid(alpha=0.3, which="both")
    axis.legend()

    inset = axis.inset_axes([0.58, 0.13, 0.37, 0.35])
    inset.loglog(result.T_values, np.maximum(widths, 1e-18), "o-", color="#31a354")
    inset.set_title(f"width slope {result.convergence_rate:.2f}", fontsize=9)
    inset.set_xlabel("T", fontsize=8)
    inset.set_ylabel("width", fontsize=8)
    inset.grid(alpha=0.25, which="both")

    figure.tight_layout()
    figure.savefig(output_dir / "continuous_limit.png", bbox_inches="tight")
    plt.close(figure)
