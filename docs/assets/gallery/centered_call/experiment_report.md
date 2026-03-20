# Experiment Report: Call on spread max(S2 - S1 - K, 0)

## Setup

- marginal 1: `S1` with support size `18`
- marginal 2: `S2` with support size `18`
- payoff: `call_on_spread`
- strike: `0.500000`

## Marginal Moments

| Marginal | Mean | Variance |
|---|---:|---:|
| `S1` | -0.000000 | 0.332305 |
| `S2` | -0.000000 | 1.329218 |

## Exact Bounds

| Objective | Value | Marginal-1 error | Marginal-2 error | Martingale error |
|---|---:|---:|---:|---:|
| lower | 0.086947 | 6.94e-18 | 2.78e-17 | 8.24e-18 |
| upper | 0.294702 | 1.39e-17 | 7.63e-17 | 2.78e-17 |

## Convex-Order Diagnostic

- feasible: `True`
- mean gap: `-3.47e-17`
- minimum call gap: `0.00e+00`
- maximum call gap: `2.50e-01`

## Regularized Runs

| eps | Expected payoff | Regularized primal | Dual gap | Iterations | Converged |
|---:|---:|---:|---:|---:|---:|
| 0.15 | 0.246243 | 0.357941 | -1.64e-08 | 22 | True |
| 0.4 | 0.225061 | 0.560261 | -1.17e-08 | 15 | True |

## Artifact Files

- `exact_uniform_summary.png`
- `regularization_path.png`
- `stability_diagnostics.png`
- `structural_diagnostics.png`
- `summary.json`
