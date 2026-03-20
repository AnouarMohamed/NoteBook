# Experiment Report: Put on spread max(K - (S2 - S1), 0)

## Setup

- marginal 1: `S1` with support size `16`
- marginal 2: `S2` with support size `16`
- payoff: `put_on_spread`
- strike: `0.250000`

## Marginal Moments

| Marginal | Mean | Variance |
|---|---:|---:|
| `S1` | 2.000000 | 0.332031 |
| `S2` | 2.000000 | 1.328125 |

## Exact Bounds

| Objective | Value | Marginal-1 error | Marginal-2 error | Martingale error |
|---|---:|---:|---:|---:|
| lower | 0.439376 | 1.67e-16 | 1.87e-16 | 6.38e-16 |
| upper | 0.634103 | 1.39e-17 | 8.33e-17 | 5.55e-17 |

## Convex-Order Diagnostic

- feasible: `True`
- mean gap: `0.00e+00`
- minimum call gap: `0.00e+00`
- maximum call gap: `2.50e-01`

## Regularized Runs

| eps | Expected payoff | Regularized primal | Dual gap | Iterations | Converged |
|---:|---:|---:|---:|---:|---:|
| 0.1 | 0.596851 | 0.663906 | -2.94e-08 | 31 | True |
| 0.3 | 0.571785 | 0.820143 | -1.87e-08 | 17 | True |

## Artifact Files

- `exact_uniform_summary.png`
- `regularization_path.png`
- `stability_diagnostics.png`
- `structural_diagnostics.png`
- `summary.json`
