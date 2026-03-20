# Experiment Report: Quadratic spread (S2 - S1)^2

## Setup

- marginal 1: `S1` with support size `18`
- marginal 2: `S2` with support size `18`
- payoff: `squared_distance`
- strike: `0.000000`

## Marginal Moments

| Marginal | Mean | Variance |
|---|---:|---:|
| `S1` | 2.000000 | 0.332305 |
| `S2` | 2.000000 | 1.329218 |

## Exact Bounds

| Objective | Value | Marginal-1 error | Marginal-2 error | Martingale error |
|---|---:|---:|---:|---:|
| lower | 0.996914 | 4.16e-17 | 1.53e-16 | 4.86e-16 |
| upper | 0.996914 | 4.16e-17 | 1.53e-16 | 4.86e-16 |

## Convex-Order Diagnostic

- feasible: `True`
- mean gap: `0.00e+00`
- minimum call gap: `0.00e+00`
- maximum call gap: `2.50e-01`

## Regularized Runs

| eps | Expected payoff | Regularized primal | Dual gap | Iterations | Converged |
|---:|---:|---:|---:|---:|---:|
| 0.15 | 0.996914 | 1.125961 | -2.83e-08 | 12 | True |
| 0.4 | 0.996914 | 1.341041 | -3.11e-08 | 12 | True |

## Artifact Files

- `exact_uniform_summary.png`
- `regularization_path.png`
- `stability_diagnostics.png`
- `structural_diagnostics.png`
- `summary.json`
