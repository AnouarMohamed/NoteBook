# API Guide

## Core Solver Functions

### `solve_exact_mot(...)`

Use this for the exact discrete LP problem.

Inputs:

- atom locations and weights for `S1`
- atom locations and weights for `S2`
- a payoff function on the atom grid
- objective direction: `"max"` or `"min"`

Returns:

- exact objective value
- optimal plan
- payoff matrix
- marginal and martingale constraint errors

### `sinkhorn_mot(...)`

Use this for the entropy-regularized MOT approximation.

Inputs:

- discrete marginals
- payoff matrix
- regularization level `eps`

Returns:

- primal expectation
- regularized primal objective
- dual objective
- dual gap
- iteration history

## Marginals And Feasibility

### `DiscreteMarginal`

Represents a one-dimensional discrete law with:

- `atoms`
- `weights`
- derived properties such as `mean`, `variance`, and `size`

### `check_convex_order_discrete(...)`

Checks martingale feasibility in practice by comparing:

- the means
- discrete call-price inequalities across a strike grid

## Built-In Payoffs

### `make_builtin_payoff(...)`

Supported names:

- `abs_spread`
- `squared_distance`
- `call_on_spread`
- `put_on_spread`
- `straddle_on_spread`

## High-Level Experiment Runners

### `run_discrete_experiment(...)`

Run the exact and regularized workflow on arbitrary discrete marginals.

### `run_two_uniform_experiment(...)`

Convenience wrapper for two-uniform experiments with configurable intervals and payoff choice.

### `run_uniform_abs_spread_experiment(...)`

Backward-compatible wrapper for the original notebook example.
