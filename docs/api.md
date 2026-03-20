# API Guide

This page is intentionally practical. I am not trying to list every symbol in alphabetical order; I am trying to tell you which imports matter when you sit down to run an experiment and would prefer not to grep the source tree like a detective.
{: .lead }

## The Import Path I Use Most

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

If you only want one high-level entry point, use `run_two_uniform_experiment(...)`.

## Exact Solver

### `solve_exact_mot(...)`

Use this when I want the discrete LP benchmark.

What it needs:

- atom locations for `S1`
- weights for `S1`
- atom locations for `S2`
- weights for `S2`
- a payoff function evaluated on the atom grid
- an objective direction: `"max"` or `"min"`

What it gives back:

- the exact objective value
- the optimal transport plan
- the payoff matrix
- marginal constraint errors
- martingale constraint error

Why I care: this is the reference answer in the repo. When the exact solver speaks, the regularized solver should explain itself relative to that answer.

## Regularized Solver

### `sinkhorn_mot(...)`

Use this when I want a smoother, faster approximation path across several values of `eps`.

Key outputs:

- `expected_payoff`
- `regularized_primal`
- `dual_value`
- `dual_gap`
- `iterations`
- marginal and martingale errors

A small but important note: `expected_payoff` and `regularized_primal` are different objects. The entropy term matters. I keep both precisely because I do not enjoy accidental category mistakes.

## Marginals And Feasibility

### `DiscreteMarginal`

This is the one-dimensional discrete law container used across the repo.

Useful properties:

- `atoms`
- `weights`
- `mean`
- `variance`
- `size`

### `make_uniform_marginal(...)`

This is the quickest way to build a marginal on an evenly spaced grid. I use it constantly in the gallery and CLI.

### `check_convex_order_discrete(...)`

This is the pre-flight check for martingale feasibility.

It reports:

- whether the pair looks feasible in convex order
- mean gap
- minimum and maximum call-price gap across the strike grid

If this says the setup is infeasible, I stop there. No optimizer deserves to be blamed for an impossible problem.

## Built-In Payoffs

### `make_builtin_payoff(...)`

Supported names:

- `abs_spread`
- `squared_distance`
- `call_on_spread`
- `put_on_spread`
- `straddle_on_spread`

These are intentionally simple and spread-centric. The point is not to imitate an entire derivatives library; the point is to make the transport geometry legible.

Example:

```python
from mot_pricing import make_builtin_payoff

payoff = make_builtin_payoff("call_on_spread", strike=0.25)
print(payoff.description)
```

## High-Level Experiment Runners

### `run_discrete_experiment(...)`

Use this for arbitrary discrete marginals when I already know the atoms and weights I want.

### `run_two_uniform_experiment(...)`

Use this when the experiment is built from two uniform intervals and a named payoff. This is the workhorse for most demos, docs pages, and quick tests.

### `run_uniform_abs_spread_experiment(...)`

This is the backward-compatible wrapper around the original notebook's reference case.

## Reporting And Gallery

### `save_experiment_artifacts(...)`

This writes the standard artifact set for a single run:

- `exact_uniform_summary.png`
- `regularization_path.png`
- `stability_diagnostics.png`
- `summary.json`

That function is the reason the repo feels reproducible instead of anecdotal.

### `builtin_gallery_specs()`

Returns the curated experiment set used by the docs. Right now it includes:

- the original absolute-spread benchmark
- call and put spread examples
- a quadratic spread case
- centered straddle and centered call cases
- a wider absolute-spread stress test

### `save_gallery_assets(...)`

Runs the curated gallery and writes:

- per-example folders with plots and JSON summaries
- `gallery_overview.png`
- `gallery_summary.json`
- `gallery_summary.md`

## A Minimal End-To-End Script

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

That script is usually enough to tell me whether the setup is interesting before I start adding anything fancier.
