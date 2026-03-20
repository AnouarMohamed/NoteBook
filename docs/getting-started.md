# Getting Started

If I only had five minutes to show someone this repo, I would install the package, run one exact-plus-regularized example, and inspect the generated figures. Everything else is refinement.
{: .lead }

## The Shortest Useful Path

Install the package:

```bash
pip install mot-pricing
```

Run the reference experiment:

```bash
mot-uniform --n 50 --x-interval 1 3 --y-interval 0 4 --payoff abs_spread --eps 1.0 0.3 0.1 0.03 0.01 --output-dir artifacts
```

That command writes a small research packet to `artifacts/`:

- `exact_uniform_summary.png`
- `regularization_path.png`
- `stability_diagnostics.png`
- `summary.json`

If you only do one thing on this site, do that first.

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

For docs work:

```bash
pip install -e .[docs]
```

## A Few Runs I Actually Recommend

The original reference problem:

```bash
mot-uniform --n 50 --x-interval 1 3 --y-interval 0 4 --payoff abs_spread --eps 0.3 0.1 --output-dir artifacts_ref
```

A directional spread option:

```bash
mot-uniform --n 60 --x-interval 1 3 --y-interval 0 4 --payoff call_on_spread --strike 0.25 --eps 0.3 0.1 --output-dir artifacts_call
```

A slightly meaner absolute-spread setup with a wider second marginal:

```bash
mot-uniform --n 40 --x-interval 0 2 --y-interval -1.5 3.5 --payoff abs_spread --eps 0.4 0.15 --output-dir artifacts_wide
```

Curated gallery generation:

```bash
mot-gallery --output-dir gallery_artifacts
```

## What I Expect To See

For the default uniform absolute-spread example, I expect the following qualitative behavior:

- the exact upper value sits near `1.0`
- the exact lower value sits near `0.6`
- the regularized expected payoff rises toward the LP upper benchmark as `eps` gets smaller
- the dual gap and martingale error remain tiny when the run is healthy

If those broad features disappear, I assume something is off and I start investigating before I start theorizing.

## Python API

If I want to script experiments rather than stay in the CLI, this is the high-level entry point I reach for:

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

For batch examples and docs-style outputs:

```python
from mot_pricing import builtin_gallery_specs, save_gallery_assets
from pathlib import Path

save_gallery_assets(Path("gallery_artifacts"), builtin_gallery_specs())
```

## What I Check Before I Trust A Result

My usual checklist is boring, which is exactly why it is useful:

- the convex-order check is feasible
- marginal errors are tiny
- martingale errors are tiny
- the regularized path moves in the expected direction as `eps` decreases
- the exact LP value remains the reference point for interpretation

The repo writes all of that into `summary.json`, because memory is unreliable and confidence should have receipts.

## Local Verification

```bash
pytest
python -m build
mkdocs build --strict
```

That is the local pre-flight I use before treating a change as real.
