# MOT Pricing

![CI](https://github.com/AnouarMohamed/NoteBook/actions/workflows/ci.yml/badge.svg)
![Docs](https://github.com/AnouarMohamed/NoteBook/actions/workflows/docs.yml/badge.svg)
![PyPI](https://img.shields.io/pypi/v/mot-pricing)
![Python](https://img.shields.io/pypi/pyversions/mot-pricing)

`mot-pricing` is a small research-oriented Python package for robust pricing with martingale optimal transport (MOT). It began as a single notebook and was reorganized into a reusable library with exact discrete solvers, entropy-regularized approximations, reporting utilities, and a documented gallery of experiments.

## Mathematical Setting

The package studies couplings `P` such that:

- `S1 ~ mu1`
- `S2 ~ mu2`
- `E[S2 | S1] = S1`

and computes extremal values of `E_P[payoff(S1, S2)]` over all such couplings.

For discrete marginals, the exact problem is formulated as a linear program over a nonnegative coupling matrix `Pi = (pi_ij)` with:

- row sums equal to the first marginal weights
- column sums equal to the second marginal weights
- row-wise martingale constraints `sum_j pi_ij (y_j - x_i) = 0`

The exact LP solution is used as the benchmark for the discrete problem, while the entropy-regularized solver provides approximation paths across values of `eps`.

## Main Features

The repository includes:

- an exact linear-programming solver for discrete MOT
- a numerically stabilized entropy-regularized solver
- discrete marginal utilities and convex-order feasibility checks
- a built-in payoff library for spread-type payoffs
- experiment runners for arbitrary discrete marginals and two-uniform systems
- reporting helpers for figures, diagnostics, JSON summaries, and markdown reports
- a curated gallery runner with cross-example summary files
- tests for exact, regularized, and reporting workflows
- documentation, CI, release workflows, and package publishing workflows

## Current Gallery

The shipped gallery currently contains nine built-in examples:

- uniform absolute spread
- call on spread
- put on spread
- quadratic spread
- centered spread straddle
- centered call on spread
- wide absolute spread
- wide put on spread
- broad spread straddle

These examples cover directional payoffs, symmetric payoffs, widened second marginals, and a quadratic case whose interval nearly collapses in the present discretization.

## Standard Artifacts

A single experiment run produces:

- `exact_uniform_summary.png`
- `regularization_path.png`
- `stability_diagnostics.png`
- `structural_diagnostics.png`
- `summary.json`
- `experiment_report.md`

A gallery run additionally produces:

- `gallery_overview.png`
- `gallery_summary.json`
- `gallery_summary.md`
- `gallery_casebook.md`

## Installation

From PyPI:

```bash
pip install mot-pricing
```

For local development:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .[dev]
```

For documentation work:

```bash
pip install -e .[docs]
```

## Command-Line Usage

Reference experiment:

```bash
mot-uniform --n 50 --x-interval 1 3 --y-interval 0 4 --payoff abs_spread --eps 1.0 0.3 0.1 0.03 0.01 --output-dir artifacts
```

Curated gallery generation:

```bash
mot-gallery --output-dir gallery_artifacts
```

Custom payoff example:

```bash
mot-uniform --n 60 --x-interval 1 3 --y-interval 0 4 --payoff call_on_spread --strike 0.25 --eps 0.3 0.1 --output-dir artifacts_call
```

## Python Usage

```python
from mot_pricing import run_two_uniform_experiment, save_experiment_artifacts
from pathlib import Path

experiment = run_two_uniform_experiment(
    x_interval=(1.0, 3.0),
    y_interval=(0.0, 4.0),
    n=40,
    payoff_name="abs_spread",
    eps_values=(0.3, 0.1),
)

save_experiment_artifacts(Path("artifacts_demo"), experiment)
print(experiment.exact_lower.value, experiment.exact_upper.value)
```

## Documentation

The documentation site is available at `https://anouarmohamed.github.io/NoteBook/` and includes:

- a discrete formulation page
- research notes and numerical notes
- getting-started instructions and CLI reference
- a gallery overview and generated casebook
- API notes and publishing guidance

## Repository Layout

- `src/mot_pricing/`: library code
- `scripts/`: script wrappers for the CLI entry points
- `tests/`: regression and numerical checks
- `docs/`: source for the GitHub Pages site
- `notebooks/`: notebook material preserved from the original exploration
- `.github/workflows/`: CI, docs deployment, release, and publishing workflows

## Validation

A minimal local validation routine is:

```bash
pytest
python -m build
python -m twine check dist/*
mkdocs build --strict
```

## Project Status

The notebook remains part of the project history, but the library and generated artifacts are now the source of truth for reproducible experiments.
