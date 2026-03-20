# MOT Pricing

`mot-pricing` is a small research-oriented Python package for robust pricing with martingale optimal transport.

It started as a single notebook and is now a reproducible project with:

- exact LP-based discrete MOT solvers
- entropy-regularized Sinkhorn-style solvers
- convex-order feasibility diagnostics
- a configurable CLI for two-uniform experiments
- tests, release workflows, and GitHub Pages documentation

## Core Problem

Given two marginals `mu1` and `mu2`, the package studies couplings `P` such that:

- `S1 ~ mu1`
- `S2 ~ mu2`
- `E[S2 | S1] = S1`

and optimizes an expected payoff such as:

- `|S2 - S1|`
- `(S2 - S1)^2`
- `max(S2 - S1 - K, 0)`

## Why The Package Is Useful

- It gives an exact discrete benchmark using linear programming.
- It gives a regularized approximation that is faster and smoother to explore.
- It makes martingale feasibility explicit through convex-order checks.
- It turns exploratory research code into something reusable and testable.

## Project Highlights

- Clean Python API in `src/mot_pricing/`
- CLI entry point: `mot-uniform`
- Package-backed notebooks in `notebooks/`
- Release assets built from tags
- GitHub Pages docs built from this `docs/` directory

## Next Steps

- Start with the [Getting Started](getting-started.md) page if you want to run the package.
- Open the [Examples](examples.md) page if you want concrete outputs and plots.
- Use the [Publishing](publishing.md) page if you want to enable PyPI trusted publishing for this repository.
