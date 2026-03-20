# Examples

This page summarizes the built-in gallery and highlights the principal numerical patterns across the current experiment set.
{: .lead }

## Gallery Overview

The built-in gallery currently contains nine examples. These include directional payoffs, symmetric payoffs, widened marginals, and a quadratic case whose interval nearly collapses in the present discretization.

![Gallery overview](assets/gallery/gallery_overview.png)

Long-form generated notes are available in the [Gallery Casebook](assets/gallery/gallery_casebook.md).

## Summary Table

| Example | Lower | Upper | Width | Smallest `eps` value |
|---|---:|---:|---:|---:|
| Uniform absolute spread | 0.6087 | 0.9975 | 0.3888 | 0.9538 |
| Call on spread | 0.1894 | 0.3841 | 0.1947 | 0.3469 |
| Put on spread | 0.4394 | 0.6341 | 0.1947 | 0.5969 |
| Quadratic spread | 0.9969 | 0.9969 | 0.0000 | 0.9969 |
| Centered spread straddle | 0.6739 | 1.0894 | 0.4155 | 1.0289 |
| Centered call on spread | 0.0869 | 0.2947 | 0.2078 | 0.2462 |
| Wide absolute spread | 0.8754 | 1.3101 | 0.4347 | 1.2487 |
| Wide put on spread | 0.7133 | 0.9382 | 0.2249 | 0.8868 |
| Broad spread straddle | 0.6217 | 1.0194 | 0.3977 | 0.9587 |

Machine-readable summary files:

- [`docs/assets/gallery/gallery_summary.md`](assets/gallery/gallery_summary.md)
- [`docs/assets/gallery/gallery_summary.json`](assets/gallery/gallery_summary.json)

## Reading Conventions

The examples are interpreted according to the following conventions:

- the exact LP bounds are the benchmark
- interval width is used as a measure of residual model uncertainty under the martingale restriction
- the smallest shipped `eps` value is treated as an approximation diagnostic rather than as a substitute for the LP benchmark
- structural diagnostics and convergence diagnostics are used together

## Selected Comparisons

### Reference Absolute Spread

- `S1 ~ Uniform[1, 3]`
- `S2 ~ Uniform[0, 4]`
- payoff `|S2 - S1|`
- exact interval `[0.6087, 0.9975]`

This remains the baseline experiment for the repository. The interval is substantial, and the unrestricted countermonotone benchmark is materially larger than the exact martingale upper value.

![Uniform abs spread exact summary](assets/gallery/uniform_abs_spread/exact_uniform_summary.png)

![Uniform abs spread structural diagnostics](assets/gallery/uniform_abs_spread/structural_diagnostics.png)

### Directional Spread Comparison

The call-on-spread and put-on-spread examples provide a useful directional comparison on the same support pair.

- call on spread: interval `[0.1894, 0.3841]`
- put on spread: interval `[0.4394, 0.6341]`

The widths coincide in the current discretization, but the interval levels differ. This separates directional asymmetry from overall interval scale.

![Call spread exact summary](assets/gallery/call_spread/exact_uniform_summary.png)

![Put spread exact summary](assets/gallery/put_spread/exact_uniform_summary.png)

### Centered Symmetric System

The centered straddle and centered call examples move to `S1 ~ Uniform[-1, 1]` and `S2 ~ Uniform[-2, 2]`.

- centered straddle: interval `[0.6739, 1.0894]`
- centered call: interval `[0.0869, 0.2947]`

These examples are useful when geometric symmetry is desirable without eliminating nontrivial pricing intervals.

![Centered straddle exact summary](assets/gallery/centered_straddle/exact_uniform_summary.png)

![Centered call exact summary](assets/gallery/centered_call/exact_uniform_summary.png)

### Wider-Marginal Regime

The wide absolute-spread and wide put-on-spread examples increase the variance of the second marginal.

- wide absolute spread: interval `[0.8754, 1.3101]`
- wide put on spread: interval `[0.7133, 0.9382]`

These examples show how increased dispersion in the second marginal broadens or shifts the robust pricing range.

![Wide abs exact summary](assets/gallery/wide_abs/exact_uniform_summary.png)

![Wide put exact summary](assets/gallery/wide_put/exact_uniform_summary.png)

### Broad Straddle

The broad spread straddle retains the original support pair but changes the payoff to `|(S2 - S1) - 0.25|`.

- lower bound `0.6217`
- upper bound `1.0194`
- interval width `0.3977`

This example complements the original absolute-spread benchmark by introducing a symmetric payoff around a nonzero strike.

![Broad straddle exact summary](assets/gallery/broad_straddle/exact_uniform_summary.png)

## Diagnostic Figures

Two diagnostic families are particularly useful in practice.

### Regularization Paths

- [`uniform_abs_spread/regularization_path.png`](assets/gallery/uniform_abs_spread/regularization_path.png)
- [`wide_abs/regularization_path.png`](assets/gallery/wide_abs/regularization_path.png)
- [`broad_straddle/regularization_path.png`](assets/gallery/broad_straddle/regularization_path.png)

### Structural Diagnostics

- [`uniform_abs_spread/structural_diagnostics.png`](assets/gallery/uniform_abs_spread/structural_diagnostics.png)
- [`centered_straddle/structural_diagnostics.png`](assets/gallery/centered_straddle/structural_diagnostics.png)
- [`wide_put/structural_diagnostics.png`](assets/gallery/wide_put/structural_diagnostics.png)

The structural diagnostics combine marginal profiles, conditional dispersion, and convex-order call gaps in a single figure.

## Per-Example Reports

Each example directory now includes:

- `experiment_report.md`
- `summary.json`
- exact, regularization, stability, and structural plots

These files are linked from the generated [Gallery Casebook](assets/gallery/gallery_casebook.md).
