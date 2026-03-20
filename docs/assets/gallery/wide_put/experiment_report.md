# Experiment Report: Put on spread max(K - (S2 - S1), 0)

## Setup

- marginal 1: `S1` with support size `18`
- marginal 2: `S2` with support size `18`
- payoff: `put_on_spread`
- strike: `0.500000`

## Marginal Moments

| Marginal | Mean | Variance |
|---|---:|---:|
| `S1` | 1.000000 | 0.332305 |
| `S2` | 1.000000 | 2.076903 |

## Exact Bounds

| Objective | Value | Marginal-1 error | Marginal-2 error | Martingale error |
|---|---:|---:|---:|---:|
| lower | 0.713319 | 2.78e-17 | 4.16e-17 | 2.12e-16 |
| upper | 0.938204 | 1.39e-17 | 9.71e-17 | 1.39e-16 |

## Convex-Order Diagnostic

- feasible: `True`
- mean gap: `0.00e+00`
- minimum call gap: `0.00e+00`
- maximum call gap: `3.75e-01`

## Regularized Runs

| eps | Expected payoff | Regularized primal | Dual gap | Iterations | Converged |
|---:|---:|---:|---:|---:|---:|
| 0.15 | 0.886793 | 1.002415 | +2.21e-08 | 19 | True |
| 0.4 | 0.860437 | 1.215079 | -3.00e-08 | 11 | True |

## Artifact Files

- `exact_uniform_summary.png`
- `regularization_path.png`
- `stability_diagnostics.png`
- `structural_diagnostics.png`
- `summary.json`
