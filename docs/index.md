# MOT Pricing

`mot-pricing` is a compact research-oriented package for robust pricing with martingale optimal transport. The repository combines exact discrete linear-programming solvers, entropy-regularized approximations, reporting utilities, and a gallery of reproducible examples.
{: .lead }

<div class="card-grid" markdown>
<div class="card" markdown>
### Public Links

- PyPI: `https://pypi.org/project/mot-pricing/`
- TestPyPI: `https://test.pypi.org/project/mot-pricing/`
- Docs: `https://anouarmohamed.github.io/NoteBook/`
- Repository: `https://github.com/AnouarMohamed/NoteBook`
</div>
<div class="card" markdown>
### Standard Workflow

1. run `mot-uniform`
2. inspect the generated figures and `summary.json`
3. compare against the gallery casebook
4. use the LP value as the benchmark for interpretation
</div>
</div>

<div class="metric-grid" markdown>
<div class="metric-card" markdown>
<div class="metric-label">Gallery Examples</div>
<div class="metric-value">9</div>
<div class="metric-note">Built-in cases covering directional, symmetric, and wide-marginal regimes.</div>
</div>
<div class="metric-card" markdown>
<div class="metric-label">Artifact Types</div>
<div class="metric-value">6</div>
<div class="metric-note">Each run writes figures, JSON summaries, and a markdown report.</div>
</div>
<div class="metric-card" markdown>
<div class="metric-label">Core Solvers</div>
<div class="metric-value">2</div>
<div class="metric-note">Exact discrete LP and entropy-regularized approximation layers.</div>
</div>
</div>

## Core Problem

The package studies couplings `P` satisfying:

- `S1 ~ mu1`
- `S2 ~ mu2`
- `E[S2 | S1] = S1`

and computes extremal values of `E_P[payoff(S1, S2)]` under this martingale restriction.

In discrete form, the associated optimization problem is a linear program over a coupling matrix `Pi = (pi_ij)`.

## Main Components

<div class="card-grid" markdown>
<div class="card" markdown>
### Exact Optimization

The exact solver computes the discrete benchmark by solving the full martingale OT linear program.
</div>
<div class="card" markdown>
### Regularized Approximation

The regularized solver computes entropy-penalized approximations across a grid of `eps` values and records convergence diagnostics.
</div>
<div class="card" markdown>
### Reporting

Each experiment produces figures, structural diagnostics, JSON summaries, and a markdown experiment report.
</div>
<div class="card" markdown>
### Gallery

The gallery provides curated examples for cross-example comparison and documentation.
</div>
</div>

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

<div class="card-grid" markdown>
<div class="card" markdown>
### Foundations

- [Discrete Formulation](discrete-formulation.md)
- [Research Notes](research-notes.md)
- [Regularization Notes](regularization-notes.md)
- [Numerical Notes](numerical-notes.md)
</div>
<div class="card" markdown>
### Usage

- [Getting Started](getting-started.md)
- [CLI Reference](cli-reference.md)
- [Artifact Guide](artifact-guide.md)
- [API Guide](api.md)
</div>
<div class="card" markdown>
### Experiments

- [Examples](examples.md)
- [Gallery Table](assets/gallery/gallery_summary.md)
- [Gallery Casebook](assets/gallery/gallery_casebook.md)
</div>
<div class="card" markdown>
### Project Notes

- [Upgrade Notes](upgrade_notes.md)
- [Publishing](publishing.md)
</div>
</div>

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
