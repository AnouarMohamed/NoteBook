# MOT Pricing

`mot-pricing` is a small research-oriented package for robust pricing under martingale optimal transport constraints. It grew out of a single exploratory notebook and is now organized as a reproducible library with exact solvers, regularized solvers, reporting utilities, and a documented experiment gallery.
{: .lead }

Public links:

- PyPI: `https://pypi.org/project/mot-pricing/`
- TestPyPI: `https://test.pypi.org/project/mot-pricing/`
- Docs: `https://anouarmohamed.github.io/NoteBook/`
- Repository: `https://github.com/AnouarMohamed/NoteBook`

## Core Problem

The package studies couplings `P` such that:

- `S1 ~ mu1`
- `S2 ~ mu2`
- `E[S2 | S1] = S1`

and optimizes `E_P[payoff(S1, S2)]` over all such couplings.

In discrete form, the associated linear program is:

```text
maximize or minimize   sum_{i,j} pi_ij c(x_i, y_j)
subject to             sum_j pi_ij = mu_i
                       sum_i pi_ij = nu_j
                       sum_j pi_ij (y_j - x_i) = 0    for each i
                       pi_ij >= 0
```

This formulation makes the marginal constraints, martingale restrictions, and payoff functional explicit.

## Current Gallery Summary

The built-in gallery currently includes seven examples with distinct numerical characteristics:

- The reference `|S2 - S1|` experiment has discrete bounds `0.6087` and `0.9975`.
- The call-on-spread example has bounds `0.1894` and `0.3841`.
- The put-on-spread example has bounds `0.4394` and `0.6341`.
- The centered spread straddle has interval width approximately `0.4155`.
- The wide absolute-spread example raises the upper bound to `1.3101`.
- The quadratic spread example collapses numerically to a nearly degenerate interval.

Taken together, these examples illustrate directional, symmetric, and variance-sensitive payoff structures.

## Why The Package Exists

The original notebook combined derivation, experimentation, plotting, and solver logic in a single environment. The package version separates these concerns and addresses several issues from the notebook stage:

- unrestricted coupling benchmarks are labeled correctly
- the regularized dual is compared against the regularized primal rather than raw `E[payoff]`
- the regularized update is handled in log space for improved numerical stability
- convex-order feasibility is checked explicitly before solving
- experiments produce plots and machine-readable summaries as standard artifacts

## Documentation Structure

- [Research Notes](research-notes.md): modeling assumptions and interpretation of exact versus regularized results
- [Numerical Notes](numerical-notes.md): diagnostics, convergence behavior, and practical numerical considerations
- [Getting Started](getting-started.md): installation, CLI usage, and artifact generation
- [Examples](examples.md): the experiment gallery with numerical summaries and interpretation
- [API Guide](api.md): principal public entry points for scripting and analysis
- [Upgrade Notes](upgrade_notes.md): transition from notebook to package
- [Publishing](publishing.md): release and trusted-publisher configuration notes

## Typical Uses

- computing exact discrete MOT bounds for two-step problems
- comparing regularized approximations against LP benchmarks
- studying the effect of different payoff structures under common marginals
- generating reproducible figures and JSON summaries for notes or reports
- exploring basic martingale geometry in a compact computational setting

## Suggested Reading Order

1. [Getting Started](getting-started.md)
2. [Examples](examples.md)
3. [Numerical Notes](numerical-notes.md)
4. [Research Notes](research-notes.md)

This order moves from execution to interpretation.
