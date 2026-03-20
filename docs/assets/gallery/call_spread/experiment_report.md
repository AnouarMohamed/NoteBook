# Experiment Report: Call on spread max(S2 - S1 - K, 0)

## Setup

- marginal 1: `S1` with support size `16`
- marginal 2: `S2` with support size `16`
- payoff: `call_on_spread`
- strike: `0.250000`

## Marginal Moments

| Marginal | Mean | Variance |
|---|---:|---:|
| `S1` | 2.000000 | 0.332031 |
| `S2` | 2.000000 | 1.328125 |

## Exact Bounds

| Objective | Value | Marginal-1 error | Marginal-2 error | Martingale error |
|---|---:|---:|---:|---:|
| lower | 0.189376 | 1.94e-16 | 2.50e-16 | 1.11e-16 |
| upper | 0.384103 | 1.39e-17 | 2.08e-17 | 1.25e-16 |

## Convex-Order Diagnostic

- feasible: `True`
- mean gap: `0.00e+00`
- minimum call gap: `0.00e+00`
- maximum call gap: `2.50e-01`

## Regularized Runs

| eps | Expected payoff | Regularized primal | Dual gap | Iterations | Converged |
|---:|---:|---:|---:|---:|---:|
| 0.1 | 0.346851 | 0.413906 | -1.82e-08 | 33 | True |
| 0.3 | 0.321785 | 0.570143 | -2.43e-08 | 17 | True |

## Artifact Files

- `exact_uniform_summary.png`
- `regularization_path.png`
- `stability_diagnostics.png`
- `structural_diagnostics.png`
- `summary.json`
