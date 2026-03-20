# Experiment Report: Spread straddle |(S2 - S1) - K|

## Setup

- marginal 1: `S1` with support size `18`
- marginal 2: `S2` with support size `18`
- payoff: `straddle_on_spread`
- strike: `0.500000`

## Marginal Moments

| Marginal | Mean | Variance |
|---|---:|---:|
| `S1` | -0.000000 | 0.332305 |
| `S2` | -0.000000 | 1.329218 |

## Exact Bounds

| Objective | Value | Marginal-1 error | Marginal-2 error | Martingale error |
|---|---:|---:|---:|---:|
| lower | 0.673894 | 6.94e-18 | 2.78e-17 | 2.56e-17 |
| upper | 1.089403 | 1.39e-17 | 6.94e-17 | 2.78e-17 |

## Convex-Order Diagnostic

- feasible: `True`
- mean gap: `-3.47e-17`
- minimum call gap: `0.00e+00`
- maximum call gap: `2.50e-01`

## Regularized Runs

| eps | Expected payoff | Regularized primal | Dual gap | Iterations | Converged |
|---:|---:|---:|---:|---:|---:|
| 0.15 | 1.028888 | 1.114402 | +3.43e-08 | 27 | True |
| 0.4 | 0.978078 | 1.292668 | -6.04e-08 | 17 | True |

## Artifact Files

- `exact_uniform_summary.png`
- `regularization_path.png`
- `stability_diagnostics.png`
- `structural_diagnostics.png`
- `summary.json`
