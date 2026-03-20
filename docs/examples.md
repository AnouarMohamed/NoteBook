# Examples

This page summarizes the shipped gallery examples and highlights the main numerical patterns in each case.
{: .lead }

## Gallery Overview

The built-in gallery currently contains seven examples covering directional payoffs, symmetric payoffs, wider marginals, and a quadratic case with a nearly degenerate interval.

![Gallery overview](assets/gallery/gallery_overview.png)

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

Machine-readable summary files:

- [`docs/assets/gallery/gallery_summary.md`](assets/gallery/gallery_summary.md)
- [`docs/assets/gallery/gallery_summary.json`](assets/gallery/gallery_summary.json)

## Interpretation Framework

The examples are read using the following conventions:

- the exact LP bounds are treated as the benchmark
- interval width is interpreted as a measure of residual model uncertainty under the martingale constraint
- the smallest shipped `eps` value is treated as an approximation diagnostic rather than as a replacement for the LP value
- diagnostic plots are used to assess convergence quality and constraint satisfaction

## Uniform Absolute Spread

Reference problem:

- `S1 ~ Uniform[1, 3]`
- `S2 ~ Uniform[0, 4]`
- payoff `|S2 - S1|`

Key values:

- lower bound `0.6087`
- upper bound `0.9975`
- interval width `0.3888`
- smallest shipped `eps = 0.1` gives expected payoff `0.9538`

This is the baseline case in which the martingale constraint still permits a substantial interval. The unrestricted upper benchmark remains materially larger, indicating that the martingale restriction has a significant effect.

![Uniform abs spread exact summary](assets/gallery/uniform_abs_spread/exact_uniform_summary.png)

Reference files:

- [`docs/assets/gallery/uniform_abs_spread/summary.json`](assets/gallery/uniform_abs_spread/summary.json)
- [`docs/assets/gallery/uniform_abs_spread/regularization_path.png`](assets/gallery/uniform_abs_spread/regularization_path.png)
- [`docs/assets/gallery/uniform_abs_spread/stability_diagnostics.png`](assets/gallery/uniform_abs_spread/stability_diagnostics.png)

## Call On Spread

- payoff `max(S2 - S1 - 0.25, 0)`
- lower bound `0.1894`
- upper bound `0.3841`
- interval width `0.1947`

Relative to the absolute-spread reference case, this interval is narrower. The payoff emphasizes one directional tail and therefore reduces the range of admissible values under the martingale constraint.

![Call spread exact summary](assets/gallery/call_spread/exact_uniform_summary.png)

Reference file:

- [`docs/assets/gallery/call_spread/summary.json`](assets/gallery/call_spread/summary.json)

## Put On Spread

- payoff `max(0.25 - (S2 - S1), 0)`
- lower bound `0.4394`
- upper bound `0.6341`
- interval width `0.1947`

This example has the same width as the call-on-spread case but a higher interval level. It is useful for comparing directional asymmetry while holding the general setup fixed.

![Put spread exact summary](assets/gallery/put_spread/exact_uniform_summary.png)

Reference file:

- [`docs/assets/gallery/put_spread/summary.json`](assets/gallery/put_spread/summary.json)

## Quadratic Spread

- payoff `(S2 - S1)^2`
- lower bound `0.9969`
- upper bound `0.9969`
- interval width `0.0000`

In the current discrete setting, the robust interval collapses numerically. This example illustrates that some payoffs are substantially more rigid than the spread-option cases.

![Quadratic spread exact summary](assets/gallery/quadratic_spread/exact_uniform_summary.png)

Reference file:

- [`docs/assets/gallery/quadratic_spread/summary.json`](assets/gallery/quadratic_spread/summary.json)

## Centered Spread Straddle

- `S1 ~ Uniform[-1, 1]`
- `S2 ~ Uniform[-2, 2]`
- payoff `|(S2 - S1) - 0.5|`
- lower bound `0.6739`
- upper bound `1.0894`

This example produces one of the widest intervals in the gallery. It is useful for studying a symmetric geometric setup with a nontrivial robust range.

![Centered straddle exact summary](assets/gallery/centered_straddle/exact_uniform_summary.png)

Reference files:

- [`docs/assets/gallery/centered_straddle/summary.json`](assets/gallery/centered_straddle/summary.json)
- [`docs/assets/gallery/centered_straddle/regularization_path.png`](assets/gallery/centered_straddle/regularization_path.png)

## Centered Call On Spread

- payoff `max(S2 - S1 - 0.5, 0)`
- lower bound `0.0869`
- upper bound `0.2947`
- interval width `0.2078`

This example shows that a centered geometry can still produce a meaningful robust interval for a directional payoff.

![Centered call exact summary](assets/gallery/centered_call/exact_uniform_summary.png)

Reference file:

- [`docs/assets/gallery/centered_call/summary.json`](assets/gallery/centered_call/summary.json)

## Wide Absolute Spread

- `S1 ~ Uniform[0, 2]`
- `S2 ~ Uniform[-1.5, 3.5]`
- payoff `|S2 - S1|`
- lower bound `0.8754`
- upper bound `1.3101`
- interval width `0.4347`

Increasing the dispersion of the second marginal widens the robust interval and raises the upper bound. This example serves as a useful stress test while remaining numerically stable.

![Wide abs exact summary](assets/gallery/wide_abs/exact_uniform_summary.png)

Reference files:

- [`docs/assets/gallery/wide_abs/summary.json`](assets/gallery/wide_abs/summary.json)
- [`docs/assets/gallery/wide_abs/regularization_path.png`](assets/gallery/wide_abs/regularization_path.png)

## Regularization Diagnostics

The following plots are particularly useful for assessing regularized behavior.

### Uniform Absolute Spread Path

![Uniform abs spread regularization path](assets/gallery/uniform_abs_spread/regularization_path.png)

### Uniform Absolute Spread Diagnostics

![Uniform abs spread diagnostics](assets/gallery/uniform_abs_spread/stability_diagnostics.png)

### Wide Absolute Spread Path

![Wide abs regularization path](assets/gallery/wide_abs/regularization_path.png)

### Centered Straddle Diagnostics

![Centered straddle diagnostics](assets/gallery/centered_straddle/stability_diagnostics.png)

Across the gallery, the main pattern is consistent:

- expected payoff approaches the LP upper value as `eps` decreases
- smaller `eps` values require more iterations
- constraint errors remain small in stable runs
- the entropic objective differs from the raw expected payoff and should be interpreted separately

## Concluding Remark

The gallery is intended to show several qualitatively different forms of uncertainty within a compact set of reproducible examples.
