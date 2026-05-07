"""Curated galleries of MOT experiments for docs and exploration."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from .continuous import ContinuousLimitResult, ot_bound_vs_timestep
from .experiments import (
    CausalExperimentResult,
    DiscreteExperimentResult,
    run_causal_experiment,
    run_two_uniform_experiment,
)
from .marginals import CausalMarginalChain
from .payoffs import make_builtin_payoff
from .reporting import (
    plot_continuous_limit,
    save_causal_experiment_artifacts,
    save_experiment_artifacts,
)


@dataclass(frozen=True)
class GallerySpec:
    slug: str
    title: str
    description: str
    n: int = 20
    payoff_name: str = "abs_spread"
    x_interval: tuple[float, float] = (1.0, 3.0)
    y_interval: tuple[float, float] = (0.0, 4.0)
    strike: float = 0.0
    eps_values: tuple[float, ...] = (0.3, 0.1)
    causal_intervals: tuple[tuple[float, float], ...] | None = None
    convergence_t_values: tuple[int, ...] | None = None


@dataclass(frozen=True)
class GalleryEntry:
    spec: GallerySpec
    experiment: DiscreteExperimentResult | CausalExperimentResult | ContinuousLimitResult


@dataclass(frozen=True)
class GalleryRow:
    slug: str
    title: str
    payoff_name: str
    strike: float
    exact_lower: float
    exact_upper: float
    width: float
    smallest_eps: float | None
    smallest_eps_expected: float | None
    smallest_eps_bias: float | None


def builtin_gallery_specs() -> tuple[GallerySpec, ...]:
    """Return a curated set of interesting examples for docs and demos."""
    return (
        GallerySpec(
            slug="uniform_abs_spread",
            title="Uniform absolute spread",
            description="The reference experiment: exact robust bounds for |S2 - S1|.",
            x_interval=(1.0, 3.0),
            y_interval=(0.0, 4.0),
            n=20,
            payoff_name="abs_spread",
            eps_values=(0.3, 0.1),
        ),
        GallerySpec(
            slug="call_spread",
            title="Call on spread",
            description="A directional payoff that emphasizes upside spread scenarios.",
            x_interval=(1.0, 3.0),
            y_interval=(0.0, 4.0),
            n=16,
            payoff_name="call_on_spread",
            strike=0.25,
            eps_values=(0.3, 0.1),
        ),
        GallerySpec(
            slug="put_spread",
            title="Put on spread",
            description="The directional sibling of the call, useful when downside spread moves matter more.",
            x_interval=(1.0, 3.0),
            y_interval=(0.0, 4.0),
            n=16,
            payoff_name="put_on_spread",
            strike=0.25,
            eps_values=(0.3, 0.1),
        ),
        GallerySpec(
            slug="quadratic_spread",
            title="Quadratic spread",
            description="A variance-sensitive payoff that rewards larger deviations quadratically.",
            x_interval=(1.0, 3.0),
            y_interval=(0.0, 4.0),
            n=18,
            payoff_name="squared_distance",
            eps_values=(0.4, 0.15),
        ),
        GallerySpec(
            slug="centered_straddle",
            title="Centered spread straddle",
            description="A symmetric payoff on a centered martingale system with wider second-step risk.",
            x_interval=(-1.0, 1.0),
            y_interval=(-2.0, 2.0),
            n=18,
            payoff_name="straddle_on_spread",
            strike=0.5,
            eps_values=(0.4, 0.15),
        ),
        GallerySpec(
            slug="centered_call",
            title="Centered call on spread",
            description="A centered setup where upward spread moves still matter, but the geometry is more symmetric.",
            x_interval=(-1.0, 1.0),
            y_interval=(-2.0, 2.0),
            n=18,
            payoff_name="call_on_spread",
            strike=0.5,
            eps_values=(0.4, 0.15),
        ),
        GallerySpec(
            slug="wide_abs",
            title="Wide absolute spread",
            description="The reference absolute-spread experiment with a noticeably wider second marginal and a larger robust interval.",
            x_interval=(0.0, 2.0),
            y_interval=(-1.5, 3.5),
            n=18,
            payoff_name="abs_spread",
            eps_values=(0.4, 0.15),
        ),
        GallerySpec(
            slug="wide_put",
            title="Wide put on spread",
            description="A downside-oriented payoff on the wider-marginal system, useful for comparison against wide absolute spread.",
            x_interval=(0.0, 2.0),
            y_interval=(-1.5, 3.5),
            n=18,
            payoff_name="put_on_spread",
            strike=0.5,
            eps_values=(0.4, 0.15),
        ),
        GallerySpec(
            slug="broad_straddle",
            title="Broad spread straddle",
            description="A straddle-style payoff on the original supports, highlighting symmetric sensitivity around a nonzero strike.",
            x_interval=(1.0, 3.0),
            y_interval=(0.0, 4.0),
            n=18,
            payoff_name="straddle_on_spread",
            strike=0.25,
            eps_values=(0.4, 0.15),
        ),
        GallerySpec(
            slug="causal_abs_spread_T3",
            title="Causal absolute spread T3",
            description="A three-step causal chain with additive absolute adjacent spread.",
            n=6,
            payoff_name="abs_spread",
            eps_values=(0.2,),
            causal_intervals=((1.0, 3.0), (0.5, 3.5), (0.0, 4.0)),
        ),
        GallerySpec(
            slug="causal_call_T4",
            title="Causal call T4",
            description="A four-step causal chain for a call on adjacent spread.",
            n=5,
            payoff_name="call_on_spread",
            strike=0.25,
            eps_values=(0.25,),
            causal_intervals=(
                (1.0, 3.0),
                (0.67, 3.33),
                (0.33, 3.67),
                (0.0, 4.0),
            ),
        ),
        GallerySpec(
            slug="causal_convergence_study",
            title="Causal convergence study",
            description="A small T=2,3,5 convergence study for additive absolute spread.",
            x_interval=(1.0, 3.0),
            y_interval=(0.0, 4.0),
            n=3,
            payoff_name="abs_spread",
            eps_values=(0.2,),
            convergence_t_values=(2, 3, 5),
        ),
    )


def run_gallery(specs: tuple[GallerySpec, ...]) -> list[GalleryEntry]:
    """Run a list of curated experiment specs."""
    entries: list[GalleryEntry] = []
    for spec in specs:
        if spec.convergence_t_values is not None:
            experiment = ot_bound_vs_timestep(
                spec.x_interval,
                spec.y_interval,
                spec.payoff_name,
                spec.n,
                T_values=spec.convergence_t_values,
                eps=min(spec.eps_values),
            )
        elif spec.causal_intervals is not None:
            chain = CausalMarginalChain.from_uniform_intervals(
                tuple((a, b, spec.n) for a, b in spec.causal_intervals)
            )
            experiment = run_causal_experiment(
                chain,
                make_builtin_payoff(spec.payoff_name, strike=spec.strike),
                eps_values=spec.eps_values,
            )
        else:
            experiment = run_two_uniform_experiment(
                x_interval=spec.x_interval,
                y_interval=spec.y_interval,
                n=spec.n,
                payoff_name=spec.payoff_name,
                strike=spec.strike,
                eps_values=spec.eps_values,
            )
        entries.append(GalleryEntry(spec=spec, experiment=experiment))
    return entries


def _entry_bounds(entry: GalleryEntry) -> tuple[float, float, float | None, float | None]:
    experiment = entry.experiment
    if isinstance(experiment, ContinuousLimitResult):
        lower = float(experiment.lower_bounds[-1])
        upper = float(experiment.upper_bounds[-1])
        return lower, upper, None, None

    smallest_eps = None
    smallest_eps_expected = None
    if experiment.regularized_results:
        smallest_eps = min(experiment.regularized_results)
        smallest_result = experiment.regularized_results[smallest_eps]
        if isinstance(experiment, CausalExperimentResult):
            smallest_eps_expected = smallest_result.overall_expected_payoff
        else:
            smallest_eps_expected = smallest_result.expected_payoff
    return (
        experiment.exact_lower.value,
        experiment.exact_upper.value,
        smallest_eps,
        smallest_eps_expected,
    )


def gallery_rows(entries: list[GalleryEntry]) -> list[GalleryRow]:
    """Collect summary rows for a gallery."""
    rows: list[GalleryRow] = []
    for entry in entries:
        exact_lower, exact_upper, smallest_eps, smallest_eps_expected = _entry_bounds(
            entry
        )
        smallest_eps_bias = None
        if smallest_eps_expected is not None:
            smallest_eps_bias = smallest_eps_expected - exact_upper

        rows.append(
            GalleryRow(
                slug=entry.spec.slug,
                title=entry.spec.title,
                payoff_name=entry.spec.payoff_name,
                strike=entry.spec.strike,
                exact_lower=exact_lower,
                exact_upper=exact_upper,
                width=exact_upper - exact_lower,
                smallest_eps=smallest_eps,
                smallest_eps_expected=smallest_eps_expected,
                smallest_eps_bias=smallest_eps_bias,
            )
        )
    return rows


def render_gallery_markdown(rows: list[GalleryRow]) -> str:
    """Render a markdown table summarizing a gallery."""
    header = (
        "| Example | Payoff | Lower | Upper | Width | Smallest eps | "
        "Smallest-eps value | Bias to upper |\n"
        "|---|---:|---:|---:|---:|---:|---:|---:|"
    )
    body = [
        (
            f"| {row.title} | `{row.payoff_name}` | {row.exact_lower:.4f} | "
            f"{row.exact_upper:.4f} | {row.width:.4f} | "
            f"{row.smallest_eps if row.smallest_eps is not None else 'n/a'} | "
            f"{row.smallest_eps_expected:.4f} | {row.smallest_eps_bias:+.4f} |"
            if row.smallest_eps_expected is not None and row.smallest_eps_bias is not None
            else (
                f"| {row.title} | `{row.payoff_name}` | {row.exact_lower:.4f} | "
                f"{row.exact_upper:.4f} | {row.width:.4f} | n/a | n/a | n/a |"
            )
        )
        for row in rows
    ]
    return "\n".join([header, *body]) + "\n"


def render_gallery_casebook(entries: list[GalleryEntry]) -> str:
    """Render a longer markdown report for the full gallery."""
    lines = [
        "# Gallery Casebook",
        "",
        "This document summarizes the built-in gallery in a longer form than the summary table.",
        "",
    ]
    for entry in entries:
        exact_lower, exact_upper, smallest_eps, smallest_expected = _entry_bounds(entry)
        smallest_bias = None
        if smallest_expected is not None:
            smallest_bias = smallest_expected - exact_upper

        if isinstance(entry.experiment, ContinuousLimitResult):
            configuration = [
                f"- `x_interval = {entry.spec.x_interval}`",
                f"- `y_interval = {entry.spec.y_interval}`",
                f"- `T_values = {entry.spec.convergence_t_values}`",
            ]
            figure_lines = [
                f"![{entry.spec.title} continuous limit]({entry.spec.slug}/continuous_limit.png)"
            ]
            file_lines = [
                f"- [`{entry.spec.slug}/continuous_summary.json`]({entry.spec.slug}/continuous_summary.json)"
            ]
        elif isinstance(entry.experiment, CausalExperimentResult):
            configuration = [
                f"- `causal_intervals = {entry.spec.causal_intervals}`",
                f"- `n = {entry.spec.n}`",
                f"- `payoff = {entry.spec.payoff_name}`",
                f"- `strike = {entry.spec.strike:.6f}`",
            ]
            figure_lines = [
                f"![{entry.spec.title} transport chain]({entry.spec.slug}/causal_transport_chain.png)",
                "",
                f"![{entry.spec.title} marginal evolution]({entry.spec.slug}/marginal_evolution.png)",
            ]
            file_lines = [
                f"- [`{entry.spec.slug}/causal_experiment_report.md`]({entry.spec.slug}/causal_experiment_report.md)",
                f"- [`{entry.spec.slug}/causal_summary.json`]({entry.spec.slug}/causal_summary.json)",
            ]
        else:
            configuration = [
                f"- `x_interval = {entry.spec.x_interval}`",
                f"- `y_interval = {entry.spec.y_interval}`",
                f"- `n = {entry.spec.n}`",
                f"- `payoff = {entry.spec.payoff_name}`",
                f"- `strike = {entry.spec.strike:.6f}`",
            ]
            figure_lines = [
                f"![{entry.spec.title} exact summary]({entry.spec.slug}/exact_uniform_summary.png)",
                "",
                f"![{entry.spec.title} structural diagnostics]({entry.spec.slug}/structural_diagnostics.png)",
            ]
            file_lines = [
                f"- [`{entry.spec.slug}/experiment_report.md`]({entry.spec.slug}/experiment_report.md)",
                f"- [`{entry.spec.slug}/summary.json`]({entry.spec.slug}/summary.json)",
            ]

        lines.extend(
            [
                f"## {entry.spec.title}",
                "",
                entry.spec.description,
                "",
                "### Configuration",
                "",
                *configuration,
                "",
                "### Exact Results",
                "",
                '<div class="casebook-table casebook-table--numeric" markdown="1">',
                "",
                "| Lower | Upper | Width |",
                "|---|---|---|",
                f"| {exact_lower:.6f} | {exact_upper:.6f} | {exact_upper - exact_lower:.6f} |",
                "",
                "</div>",
            ]
        )

        if smallest_eps is not None and smallest_expected is not None and smallest_bias is not None:
            lines.extend(
                [
                    "",
                    "### Smallest Regularization Level",
                    "",
                    '<div class="casebook-table casebook-table--numeric" markdown="1">',
                    "",
                    "| eps | Expected payoff | Bias to upper |",
                    "|---|---|---|",
                    f"| {smallest_eps:g} | {smallest_expected:.6f} | {smallest_bias:+.6f} |",
                    "",
                    "</div>",
                ]
            )

        lines.extend(
            [
                "",
                "### Figures",
                "",
                *figure_lines,
                "",
                "### Files",
                "",
                *file_lines,
                "",
            ]
        )
    return "\n".join(lines)


def save_gallery_overview(output_dir: Path, rows: list[GalleryRow]) -> None:
    """Save a cross-example overview plot."""
    labels = [row.title for row in rows]
    lower_values = [row.exact_lower for row in rows]
    upper_values = [row.exact_upper for row in rows]
    widths = [row.width for row in rows]

    figure, axes = plt.subplots(1, 2, figsize=(14, 5))

    positions = np.arange(len(rows))
    axes[0].barh(positions, lower_values, color="#9ecae1", label="lower")
    axes[0].barh(
        positions,
        np.array(upper_values) - np.array(lower_values),
        left=lower_values,
        color="#fd8d3c",
        label="interval width",
    )
    axes[0].set_yticks(positions)
    axes[0].set_yticklabels(labels)
    axes[0].set_title("Robust price intervals across examples")
    axes[0].set_xlabel("value")
    axes[0].legend()

    axes[1].bar(labels, widths, color="#756bb1")
    axes[1].set_title("Interval width by example")
    axes[1].set_ylabel("upper - lower")
    axes[1].tick_params(axis="x", rotation=22)

    figure.tight_layout()
    figure.savefig(output_dir / "gallery_overview.png", bbox_inches="tight")
    plt.close(figure)


def save_gallery_assets(output_dir: Path, specs: tuple[GallerySpec, ...]) -> list[GalleryEntry]:
    """Run a gallery and write all per-example and summary artifacts."""
    output_dir.mkdir(parents=True, exist_ok=True)
    entries = run_gallery(specs)

    for entry in entries:
        example_dir = output_dir / entry.spec.slug
        if isinstance(entry.experiment, ContinuousLimitResult):
            example_dir.mkdir(parents=True, exist_ok=True)
            plot_continuous_limit(example_dir, entry.experiment)
            continuous_summary = {
                "T_values": entry.experiment.T_values.tolist(),
                "upper_bounds": entry.experiment.upper_bounds.tolist(),
                "lower_bounds": entry.experiment.lower_bounds.tolist(),
                "convergence_rate": entry.experiment.convergence_rate,
                "payoff_name": entry.experiment.payoff_name,
                "eps": entry.experiment.eps,
            }
            (example_dir / "continuous_summary.json").write_text(
                json.dumps(continuous_summary, indent=2), encoding="utf-8"
            )
        elif isinstance(entry.experiment, CausalExperimentResult):
            save_causal_experiment_artifacts(example_dir, entry.experiment)
        else:
            save_experiment_artifacts(example_dir, entry.experiment)

    rows = gallery_rows(entries)
    save_gallery_overview(output_dir, rows)
    (output_dir / "gallery_summary.json").write_text(
        json.dumps([asdict(row) for row in rows], indent=2), encoding="utf-8"
    )
    (output_dir / "gallery_summary.md").write_text(
        render_gallery_markdown(rows), encoding="utf-8"
    )
    (output_dir / "gallery_casebook.md").write_text(
        render_gallery_casebook(entries), encoding="utf-8"
    )
    return entries
