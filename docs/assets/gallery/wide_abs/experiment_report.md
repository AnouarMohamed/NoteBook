# Experiment Report: Absolute spread |S2 - S1|

## Setup

- marginal 1: `S1` with support size `18`
- marginal 2: `S2` with support size `18`
- payoff: `abs_spread`
- strike: `0.000000`

## Marginal Moments

| Marginal | Mean | Variance |
|---|---:|---:|
| `S1` | 1.000000 | 0.332305 |
| `S2` | 1.000000 | 2.076903 |

## Exact Bounds

| Objective | Value | Marginal-1 error | Marginal-2 error | Martingale error |
|---|---:|---:|---:|---:|
| lower | 0.875361 | 2.78e-17 | 6.94e-17 | 1.99e-17 |
| upper | 1.310082 | 2.78e-17 | 2.78e-17 | 9.71e-17 |

## Convex-Order Diagnostic

- feasible: `True`
- mean gap: `0.00e+00`
- minimum call gap: `0.00e+00`
- maximum call gap: `3.75e-01`

## Unrestricted Benchmarks

| Benchmark | Value |
|---|---:|
| comonotone minimum | 0.750000 |
| independent | 1.316667 |
| countermonotone maximum | 1.750000 |

## Regularized Runs

| eps | Expected payoff | Regularized primal | Dual gap | Iterations | Converged |
|---:|---:|---:|---:|---:|---:|
| 0.15 | 1.248650 | 1.335649 | -2.95e-08 | 38 | True |
| 0.4 | 1.189883 | 1.521231 | -2.43e-08 | 18 | True |

## Artifact Files

- `exact_uniform_summary.png`
- `regularization_path.png`
- `stability_diagnostics.png`
- `structural_diagnostics.png`
- `summary.json`
