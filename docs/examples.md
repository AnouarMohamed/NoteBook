# Examples

This page summarizes the built-in gallery and highlights the principal numerical patterns across the current experiment set.
{: .lead }

## Gallery Overview

The built-in gallery currently contains twelve examples. These include directional payoffs, symmetric payoffs, widened marginals, a quadratic case whose interval nearly collapses in the present discretization, and causal multi-period studies.

![Gallery overview](assets/gallery/gallery_overview.png)
<div class="caption">Cross-example view of robust lower and upper values together with interval widths.</div>

Related files:

- [Gallery Table](assets/gallery/gallery_summary.md)
- [Gallery Summary JSON](assets/gallery/gallery_summary.json)
- [Gallery Casebook](assets/gallery/gallery_casebook.md)

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
| Causal absolute spread T3 | see generated gallery | see generated gallery | see generated gallery | see generated gallery |
| Causal call T4 | see generated gallery | see generated gallery | see generated gallery | see generated gallery |
| Causal convergence study | see generated gallery | see generated gallery | see generated gallery | n/a |

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
<div class="caption">Exact upper plan together with the benchmark comparison panel.</div>

![Uniform abs spread structural diagnostics](assets/gallery/uniform_abs_spread/structural_diagnostics.png)
<div class="caption">Marginal profiles, conditional dispersion, and convex-order call gap.</div>

### Directional Spread Comparison

The call-on-spread and put-on-spread examples provide a useful directional comparison on the same support pair.

- call on spread: interval `[0.1894, 0.3841]`
- put on spread: interval `[0.4394, 0.6341]`

The widths coincide in the current discretization, but the interval levels differ. This separates directional asymmetry from overall interval scale.

![Call spread exact summary](assets/gallery/call_spread/exact_uniform_summary.png)
<div class="caption">Directional payoff emphasizing upward spread moves.</div>

![Put spread exact summary](assets/gallery/put_spread/exact_uniform_summary.png)
<div class="caption">Directional payoff emphasizing downward spread moves.</div>

### Centered Symmetric System

The centered straddle and centered call examples move to `S1 ~ Uniform[-1, 1]` and `S2 ~ Uniform[-2, 2]`.

- centered straddle: interval `[0.6739, 1.0894]`
- centered call: interval `[0.0869, 0.2947]`

These examples are useful when geometric symmetry is desirable without eliminating nontrivial pricing intervals.

![Centered straddle exact summary](assets/gallery/centered_straddle/exact_uniform_summary.png)
<div class="caption">Symmetric setup with one of the widest intervals in the current gallery.</div>

![Centered call exact summary](assets/gallery/centered_call/exact_uniform_summary.png)
<div class="caption">Directional payoff on the centered support pair.</div>

### Wider-Marginal Regime

The wide absolute-spread and wide put-on-spread examples increase the variance of the second marginal.

- wide absolute spread: interval `[0.8754, 1.3101]`
- wide put on spread: interval `[0.7133, 0.9382]`

These examples show how increased dispersion in the second marginal broadens or shifts the robust pricing range.

![Wide abs exact summary](assets/gallery/wide_abs/exact_uniform_summary.png)
<div class="caption">Absolute-spread behavior under a noticeably wider second marginal.</div>

![Wide put exact summary](assets/gallery/wide_put/exact_uniform_summary.png)
<div class="caption">Downside-oriented payoff in the wider-marginal regime.</div>

### Broad Straddle

The broad spread straddle retains the original support pair but changes the payoff to `|(S2 - S1) - 0.25|`.

- lower bound `0.6217`
- upper bound `1.0194`
- interval width `0.3977`

This example complements the original absolute-spread benchmark by introducing a symmetric payoff around a nonzero strike.

![Broad straddle exact summary](assets/gallery/broad_straddle/exact_uniform_summary.png)
<div class="caption">Symmetric spread sensitivity around a shifted center.</div>

![Broad straddle structural diagnostics](assets/gallery/broad_straddle/structural_diagnostics.png)
<div class="caption">Structural diagnostics for the shifted straddle configuration.</div>

### Causal Multi-Period Examples

The causal gallery entries use chains of marginals rather than a single two-period pair.

- causal absolute spread T3: three uniform marginals widening from `[1, 3]` to `[0, 4]`
- causal call T4: four marginals with an adjacent call-on-spread payoff
- causal convergence study: selected `T` values for an additive absolute-spread time-step study

These entries write causal artifact names such as:

- `causal_transport_chain.png`
- `causal_summary.json`
- `causal_experiment_report.md`
- `continuous_limit.png` for convergence studies

## Diagnostic Figures

Useful diagnostics include:

- [`uniform_abs_spread/regularization_path.png`](assets/gallery/uniform_abs_spread/regularization_path.png)
- [`wide_abs/regularization_path.png`](assets/gallery/wide_abs/regularization_path.png)
- [`broad_straddle/regularization_path.png`](assets/gallery/broad_straddle/regularization_path.png)
- [`uniform_abs_spread/structural_diagnostics.png`](assets/gallery/uniform_abs_spread/structural_diagnostics.png)
- [`centered_straddle/structural_diagnostics.png`](assets/gallery/centered_straddle/structural_diagnostics.png)
- [`wide_put/structural_diagnostics.png`](assets/gallery/wide_put/structural_diagnostics.png)

The structural diagnostics combine marginal profiles, conditional dispersion, and convex-order call gaps in a single figure.

## Per-Example Reports

Each example directory includes:

- `experiment_report.md` and `summary.json` for two-period entries
- `causal_experiment_report.md` and `causal_summary.json` for causal entries
- `continuous_summary.json` for convergence entries
- matching exact, regularization, causal, or continuous-limit plots

These files are linked from the generated [Gallery Casebook](assets/gallery/gallery_casebook.md).
