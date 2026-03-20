# Getting Started

This page summarizes the shortest path from installation to a reproducible experiment run.
{: .lead }

## Minimal Workflow

Install the package:

```bash
pip install mot-pricing
```

Run the reference experiment:

```bash
mot-uniform --n 50 --x-interval 1 3 --y-interval 0 4 --payoff abs_spread --eps 1.0 0.3 0.1 0.03 0.01 --output-dir artifacts
```

This command writes the standard artifact set to `artifacts/`:

- `exact_uniform_summary.png`
- `regularization_path.png`
- `stability_diagnostics.png`
- `structural_diagnostics.png`
- `summary.json`
- `experiment_report.md`

## Installation Modes

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

## Recommended CLI Runs

Reference absolute-spread example:

```bash
mot-uniform --n 50 --x-interval 1 3 --y-interval 0 4 --payoff abs_spread --eps 0.3 0.1 --output-dir artifacts_ref
```

Directional spread option:

```bash
mot-uniform --n 60 --x-interval 1 3 --y-interval 0 4 --payoff call_on_spread --strike 0.25 --eps 0.3 0.1 --output-dir artifacts_call
```

Wider second marginal with absolute spread:

```bash
mot-uniform --n 40 --x-interval 0 2 --y-interval -1.5 3.5 --payoff abs_spread --eps 0.4 0.15 --output-dir artifacts_wide
```

Curated gallery generation:

```bash
mot-gallery --output-dir gallery_artifacts
```

## Expected Qualitative Behavior

For the default uniform absolute-spread example:

- the exact upper value is close to `1.0`
- the exact lower value is close to `0.6`
- the regularized expected payoff approaches the LP upper benchmark as `eps` decreases
- dual gaps and martingale errors remain small in stable runs
- structural diagnostics show a nonnegative convex-order call gap

Substantial deviations from this pattern generally indicate either a different discretization regime or a numerical issue that warrants inspection.

## Python API

The principal high-level entry point for scripting is `run_two_uniform_experiment(...)`:

```python
from mot_pricing import run_two_uniform_experiment

experiment = run_two_uniform_experiment(
    x_interval=(1.0, 3.0),
    y_interval=(0.0, 4.0),
    n=40,
    payoff_name="abs_spread",
    eps_values=(0.3, 0.1),
)

print(experiment.exact_upper.value)
print(experiment.exact_lower.value)
print(experiment.convex_order.feasible)
```

For batch examples and documentation assets:

```python
from mot_pricing import builtin_gallery_specs, save_gallery_assets
from pathlib import Path

save_gallery_assets(Path("gallery_artifacts"), builtin_gallery_specs())
```

## Basic Validation Checklist

Before interpreting a result, the following checks are useful:

- convex-order feasibility is satisfied
- marginal errors are small
- martingale errors are small
- the regularization path moves in the expected direction as `eps` decreases
- the exact LP value is used as the benchmark for interpretation

All of these quantities are recorded in `summary.json`, while the main figures are summarized again in `experiment_report.md`.

## Local Verification

```bash
pytest
python -m build
mkdocs build --strict
```

These commands provide a minimal local verification routine.
