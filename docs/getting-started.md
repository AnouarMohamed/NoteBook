# Getting Started

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

For docs work:

```bash
pip install -e .[docs]
```

## Quick CLI Run

Default robust pricing example:

```bash
mot-uniform --n 50 --x-interval 1 3 --y-interval 0 4 --payoff abs_spread --eps 1.0 0.3 0.1 0.03 0.01 --output-dir artifacts
```

Custom spread call example:

```bash
mot-uniform --n 60 --x-interval 1 3 --y-interval 0 4 --payoff call_on_spread --strike 0.25 --eps 0.3 0.1 --output-dir artifacts_call
```

Curated gallery generation:

```bash
mot-gallery --output-dir gallery_artifacts
```

## Python API

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
print(experiment.convex_order.feasible)
```

For batch examples:

```python
from mot_pricing import builtin_gallery_specs, save_gallery_assets
from pathlib import Path

save_gallery_assets(Path("gallery_artifacts"), builtin_gallery_specs())
```

## Local Verification

```bash
pytest
python -m build
mkdocs build --strict
```
