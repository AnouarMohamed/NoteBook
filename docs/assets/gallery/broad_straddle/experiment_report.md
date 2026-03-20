# Experiment Report: Spread straddle |(S2 - S1) - K|

## Setup

- marginal 1: `S1` with support size `18`
- marginal 2: `S2` with support size `18`
- payoff: `straddle_on_spread`
- strike: `0.250000`

## Marginal Moments

| Marginal | Mean | Variance |
|---|---:|---:|
| `S1` | 2.000000 | 0.332305 |
| `S2` | 2.000000 | 1.329218 |

## Exact Bounds

| Objective | Value | Marginal-1 error | Marginal-2 error | Martingale error |
|---|---:|---:|---:|---:|
| lower | 0.621678 | 3.89e-16 | 5.83e-16 | 2.78e-17 |
| upper | 1.019361 | 1.39e-17 | 1.39e-16 | 6.25e-17 |

## Convex-Order Diagnostic

- feasible: `True`
- mean gap: `0.00e+00`
- minimum call gap: `0.00e+00`
- maximum call gap: `2.50e-01`

## Regularized Runs

| eps | Expected payoff | Regularized primal | Dual gap | Iterations | Converged |
|---:|---:|---:|---:|---:|---:|
| 0.15 | 0.958709 | 1.046513 | -4.98e-08 | 39 | True |
| 0.4 | 0.909925 | 1.227611 | -4.25e-08 | 20 | True |

## Artifact Files

- `exact_uniform_summary.png`
- `regularization_path.png`
- `stability_diagnostics.png`
- `structural_diagnostics.png`
- `summary.json`
