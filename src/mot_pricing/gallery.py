"""Curated galleries of MOT experiments for docs and exploration."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from .experiments import DiscreteExperimentResult, run_two_uniform_experiment
from .reporting import save_experiment_artifacts


@dataclass(frozen=True)
class GallerySpec:
    slug: str
    title: str
    description: str
    x_interval: tuple[float, float]
    y_interval: tuple[float, float]
    n: int
    payoff_name: str
    strike: float = 0.0
    eps_values: tuple[float, ...] = (0.3, 0.1)


@dataclass(frozen=True)
class GalleryEntry:
    spec: GallerySpec
    experiment: DiscreteExperimentResult


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
    )


def run_gallery(specs: tuple[GallerySpec, ...]) -> list[GalleryEntry]:
    """Run a list of curated experiment specs."""
    entries: list[GalleryEntry] = []
    for spec in specs:
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


def gallery_rows(entries: list[GalleryEntry]) -> list[GalleryRow]:
    """Collect summary rows for a gallery."""
    rows: list[GalleryRow] = []
    for entry in entries:
        smallest_eps = None
        smallest_eps_expected = None
        smallest_eps_bias = None
        if entry.experiment.regularized_results:
            smallest_eps = min(entry.experiment.regularized_results)
            smallest_result = entry.experiment.regularized_results[smallest_eps]
            smallest_eps_expected = smallest_result.expected_payoff
            smallest_eps_bias = smallest_result.expected_payoff - entry.experiment.exact_upper.value

        rows.append(
            GalleryRow(
                slug=entry.spec.slug,
                title=entry.spec.title,
                payoff_name=entry.spec.payoff_name,
                strike=entry.spec.strike,
                exact_lower=entry.experiment.exact_lower.value,
                exact_upper=entry.experiment.exact_upper.value,
                width=entry.experiment.exact_upper.value - entry.experiment.exact_lower.value,
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
        smallest_eps = None
        smallest_expected = None
        smallest_bias = None
        if entry.experiment.regularized_results:
            smallest_eps = min(entry.experiment.regularized_results)
            result = entry.experiment.regularized_results[smallest_eps]
            smallest_expected = result.expected_payoff
            smallest_bias = result.expected_payoff - entry.experiment.exact_upper.value

        lines.extend(
            [
                f"## {entry.spec.title}",
                "",
                entry.spec.description,
                "",
                "### Configuration",
                "",
                f"- `x_interval = {entry.spec.x_interval}`",
                f"- `y_interval = {entry.spec.y_interval}`",
                f"- `n = {entry.spec.n}`",
                f"- `payoff = {entry.spec.payoff_name}`",
                f"- `strike = {entry.spec.strike:.6f}`",
                "",
                "### Exact Results",
                "",
                "| Lower | Upper | Width |",
                "|---:|---:|---:|",
                (
                    f"| {entry.experiment.exact_lower.value:.6f} | "
                    f"{entry.experiment.exact_upper.value:.6f} | "
                    f"{entry.experiment.exact_upper.value - entry.experiment.exact_lower.value:.6f} |"
                ),
            ]
        )

        if smallest_eps is not None and smallest_expected is not None and smallest_bias is not None:
            lines.extend(
                [
                    "",
                    "### Smallest Regularization Level",
                    "",
                    "| eps | Expected payoff | Bias to upper |",
                    "|---:|---:|---:|",
                    f"| {smallest_eps:g} | {smallest_expected:.6f} | {smallest_bias:+.6f} |",
                ]
            )

        lines.extend(
            [
                "",
                "### Figures",
                "",
                f"![{entry.spec.title} exact summary]({entry.spec.slug}/exact_uniform_summary.png)",
                "",
                f"![{entry.spec.title} structural diagnostics]({entry.spec.slug}/structural_diagnostics.png)",
                "",
                "### Files",
                "",
                f"- [`{entry.spec.slug}/experiment_report.md`]({entry.spec.slug}/experiment_report.md)",
                f"- [`{entry.spec.slug}/summary.json`]({entry.spec.slug}/summary.json)",
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
