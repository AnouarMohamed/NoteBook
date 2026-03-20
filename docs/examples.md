# Examples

## Gallery Overview

The repository now ships with a curated gallery generator that runs multiple interesting experiments and writes both plots and machine-readable summaries.

### Overview Plot

![Gallery overview](assets/gallery/gallery_overview.png)

### Summary Files

- [`docs/assets/gallery/gallery_summary.md`](assets/gallery/gallery_summary.md)
- [`docs/assets/gallery/gallery_summary.json`](assets/gallery/gallery_summary.json)

## Uniform Absolute Spread

Parameters:

- `S1 ~ Uniform[1, 3]`
- `S2 ~ Uniform[0, 4]`
- payoff `|S2 - S1|`
- exact martingale constraint

### Exact Summary Plot

![Uniform abs spread exact summary](assets/gallery/uniform_abs_spread/exact_uniform_summary.png)

### Regularization Path

![Uniform abs spread regularization path](assets/gallery/uniform_abs_spread/regularization_path.png)

### Stability Diagnostics

![Uniform abs spread stability diagnostics](assets/gallery/uniform_abs_spread/stability_diagnostics.png)

### Summary Data

The underlying machine-readable run summary is stored in:

- [`docs/assets/gallery/uniform_abs_spread/summary.json`](assets/gallery/uniform_abs_spread/summary.json)

## Call-On-Spread

Parameters:

- `S1 ~ Uniform[1, 3]`
- `S2 ~ Uniform[0, 4]`
- payoff `max(S2 - S1 - 0.25, 0)`

### Exact Summary Plot

![Call spread exact summary](assets/gallery/call_spread/exact_uniform_summary.png)

### Regularization Path

![Call spread regularization path](assets/gallery/call_spread/regularization_path.png)

### Stability Diagnostics

![Call spread stability diagnostics](assets/gallery/call_spread/stability_diagnostics.png)

### Summary Data

- [`docs/assets/gallery/call_spread/summary.json`](assets/gallery/call_spread/summary.json)

## Quadratic Spread

This example emphasizes variance amplification by using `(S2 - S1)^2` as the payoff.

### Exact Summary Plot

![Quadratic spread exact summary](assets/gallery/quadratic_spread/exact_uniform_summary.png)

### Regularization Path

![Quadratic spread regularization path](assets/gallery/quadratic_spread/regularization_path.png)

### Stability Diagnostics

![Quadratic spread stability diagnostics](assets/gallery/quadratic_spread/stability_diagnostics.png)

### Summary Data

- [`docs/assets/gallery/quadratic_spread/summary.json`](assets/gallery/quadratic_spread/summary.json)

## Centered Spread Straddle

This example uses centered supports with a wider second marginal and a spread straddle payoff.

### Exact Summary Plot

![Centered straddle exact summary](assets/gallery/centered_straddle/exact_uniform_summary.png)

### Regularization Path

![Centered straddle regularization path](assets/gallery/centered_straddle/regularization_path.png)

### Stability Diagnostics

![Centered straddle stability diagnostics](assets/gallery/centered_straddle/stability_diagnostics.png)

### Summary Data

- [`docs/assets/gallery/centered_straddle/summary.json`](assets/gallery/centered_straddle/summary.json)

## Notes

- The exact solver gives the discrete LP benchmark.
- The regularized solver converges toward the exact result as `eps` decreases.
- The diagnostics plot makes it easier to compare dual gaps, martingale errors, and iteration counts.
- The JSON summaries make it easy to compare runs or feed results into external tooling.
