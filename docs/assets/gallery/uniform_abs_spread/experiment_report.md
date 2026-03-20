# Experiment Report: Absolute spread |S2 - S1|

## Setup

- marginal 1: `S1` with support size `20`
- marginal 2: `S2` with support size `20`
- payoff: `abs_spread`
- strike: `0.000000`

## Marginal Moments

| Marginal | Mean | Variance |
|---|---:|---:|
| `S1` | 2.000000 | 0.332500 |
| `S2` | 2.000000 | 1.330000 |

## Exact Bounds

| Objective | Value | Marginal-1 error | Marginal-2 error | Martingale error |
|---|---:|---:|---:|---:|
| lower | 0.608724 | 2.01e-16 | 3.82e-16 | 9.51e-16 |
| upper | 0.997500 | 4.16e-17 | 4.16e-17 | 1.25e-16 |

## Convex-Order Diagnostic

- feasible: `True`
- mean gap: `0.00e+00`
- minimum call gap: `0.00e+00`
- maximum call gap: `2.50e-01`

## Unrestricted Benchmarks

| Benchmark | Value |
|---|---:|
| comonotone minimum | 0.500000 |
| independent | 1.083333 |
| countermonotone maximum | 1.500000 |

## Regularized Runs

| eps | Expected payoff | Regularized primal | Dual gap | Iterations | Converged |
|---:|---:|---:|---:|---:|---:|
| 0.1 | 0.953833 | 0.997883 | -4.21e-08 | 62 | True |
| 0.3 | 0.900543 | 1.128000 | -3.83e-08 | 25 | True |

## Artifact Files

- `exact_uniform_summary.png`
- `regularization_path.png`
- `stability_diagnostics.png`
- `structural_diagnostics.png`
- `summary.json`
