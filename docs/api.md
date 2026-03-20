# API Guide

This page summarizes the principal public entry points for scripting experiments and generating artifacts.
{: .lead }

## Common Import Pattern

```python
from mot_pricing import (
    run_two_uniform_experiment,
    make_builtin_payoff,
    make_uniform_marginal,
    solve_exact_mot,
    sinkhorn_mot,
    save_experiment_artifacts,
)
```

For most workflows, `run_two_uniform_experiment(...)` is the most convenient high-level entry point.

## Exact Solver

### `solve_exact_mot(...)`

This function solves the discrete LP benchmark.

Inputs:

- atom locations for `S1`
- weights for `S1`
- atom locations for `S2`
- weights for `S2`
- a payoff function evaluated on the atom grid
- an objective direction: `"max"` or `"min"`

Outputs:

- exact objective value
- optimal transport plan
- payoff matrix
- marginal constraint errors
- martingale constraint error

This is the reference solver used throughout the package.

## Regularized Solver

### `sinkhorn_mot(...)`

This function computes the entropy-regularized approximation for a fixed `eps`.

Key outputs:

- `expected_payoff`
- `regularized_primal`
- `dual_value`
- `dual_gap`
- `iterations`
- marginal and martingale errors

`expected_payoff` and `regularized_primal` are distinct quantities. The latter includes the entropy term and should be interpreted separately.

## Marginals And Feasibility

### `DiscreteMarginal`

Container for a one-dimensional discrete law.

Key properties:

- `atoms`
- `weights`
- `mean`
- `variance`
- `size`

### `make_uniform_marginal(...)`

Convenience constructor for a uniform marginal on an evenly spaced grid.

### `check_convex_order_discrete(...)`

Discrete feasibility diagnostic for martingale couplings.

Reported quantities:

- feasibility flag
- mean gap
- minimum and maximum call-price gap over the strike grid

If this check fails, the setup should not be treated as martingale-feasible.

## Built-In Payoffs

### `make_builtin_payoff(...)`

Supported names:

- `abs_spread`
- `squared_distance`
- `call_on_spread`
- `put_on_spread`
- `straddle_on_spread`

These payoffs are intentionally compact and centered on spread-type structures.

Example:

```python
from mot_pricing import make_builtin_payoff

payoff = make_builtin_payoff("call_on_spread", strike=0.25)
print(payoff.description)
```

## High-Level Experiment Runners

### `run_discrete_experiment(...)`

Runs the exact and regularized workflow for arbitrary discrete marginals.

### `run_two_uniform_experiment(...)`

Convenience wrapper for experiments based on two uniform intervals and a named payoff.

### `run_uniform_abs_spread_experiment(...)`

Backward-compatible wrapper for the original reference example.

## Reporting And Gallery

### `save_experiment_artifacts(...)`

Writes the standard artifact set for a single run:

- `exact_uniform_summary.png`
- `regularization_path.png`
- `stability_diagnostics.png`
- `summary.json`

### `builtin_gallery_specs()`

Returns the curated example set used throughout the documentation. The current set includes:

- the reference absolute-spread example
- call and put spread examples
- a quadratic spread example
- centered straddle and centered call examples
- a wider absolute-spread example

### `save_gallery_assets(...)`

Runs the gallery and writes:

- per-example folders with plots and JSON summaries
- `gallery_overview.png`
- `gallery_summary.json`
- `gallery_summary.md`

## Minimal End-To-End Script

```python
from pathlib import Path
from mot_pricing import run_two_uniform_experiment, save_experiment_artifacts

experiment = run_two_uniform_experiment(
    x_interval=(1.0, 3.0),
    y_interval=(0.0, 4.0),
    n=30,
    payoff_name="abs_spread",
    eps_values=(0.3, 0.1),
)

save_experiment_artifacts(Path("artifacts_demo"), experiment)
print(experiment.exact_lower.value, experiment.exact_upper.value)
```

This script is sufficient for a basic exact-plus-regularized experiment.
