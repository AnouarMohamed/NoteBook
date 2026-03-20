# MOT Pricing

`mot-pricing` is a compact research-oriented package for robust pricing with martingale optimal transport. The repository combines exact discrete linear-programming solvers, entropy-regularized approximations, reporting utilities, and a gallery of reproducible examples.
{: .lead }

Public links:

- PyPI: `https://pypi.org/project/mot-pricing/`
- TestPyPI: `https://test.pypi.org/project/mot-pricing/`
- Docs: `https://anouarmohamed.github.io/NoteBook/`
- Repository: `https://github.com/AnouarMohamed/NoteBook`

## Core Problem

The package studies couplings `P` satisfying:

- `S1 ~ mu1`
- `S2 ~ mu2`
- `E[S2 | S1] = S1`

and computes extremal values of `E_P[payoff(S1, S2)]` under this martingale restriction.

In discrete form, the associated optimization problem is a linear program over a coupling matrix `Pi = (pi_ij)`.

## Main Components

### Exact Optimization

The exact solver computes the discrete benchmark by solving the full martingale OT linear program.

### Regularized Approximation

The regularized solver computes entropy-penalized approximations across a grid of `eps` values and records convergence diagnostics.

### Reporting

Each experiment produces figures, structural diagnostics, JSON summaries, and a markdown experiment report.

### Gallery

The gallery provides curated examples for cross-example comparison and documentation.

## Current Gallery Scope

The shipped gallery currently contains nine examples spanning:

- absolute-spread benchmarks
- call and put spread payoffs
- straddle-type payoffs
- centered systems
- wider second marginals
- a quadratic example with a nearly degenerate interval

The gallery therefore covers several qualitatively different regimes rather than a single canned demonstration.

## Documentation Map

- [Discrete Formulation](discrete-formulation.md)
- [Research Notes](research-notes.md)
- [Regularization Notes](regularization-notes.md)
- [Numerical Notes](numerical-notes.md)
- [Getting Started](getting-started.md)
- [CLI Reference](cli-reference.md)
- [Artifact Guide](artifact-guide.md)
- [Examples](examples.md)
- [Gallery Table](assets/gallery/gallery_summary.md)
- [Gallery Casebook](assets/gallery/gallery_casebook.md)
- [API Guide](api.md)
- [Upgrade Notes](upgrade_notes.md)
- [Publishing](publishing.md)

## Typical Uses

- exact discrete MOT bounds for two-step problems
- comparison of regularized approximations against LP benchmarks
- payoff sensitivity studies under fixed marginals
- generation of figures and summaries for notes or reports
- structured experimentation with small martingale systems

## Suggested Starting Point

1. [Getting Started](getting-started.md)
2. [CLI Reference](cli-reference.md)
3. [Artifact Guide](artifact-guide.md)
4. [Examples](examples.md)
5. [Gallery Casebook](assets/gallery/gallery_casebook.md)
6. [Numerical Notes](numerical-notes.md)

This sequence moves from execution to inspection to interpretation.
