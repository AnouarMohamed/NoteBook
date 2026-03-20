# MOT Pricing

I built `mot-pricing` because the original notebook had a real mathematical question inside it, plus the usual notebook habit of doing six jobs at once. The question is serious: if I know the marginals of `S1` and `S2`, and I insist on the martingale condition `E[S2 | S1] = S1`, what can I honestly say about the price of a payoff? The package is my attempt to answer that cleanly, reproducibly, and without making the numerics sound wiser than they are.
{: .lead }

> The exact LP solver is the part I trust like a theorem. The entropic solver is the part I trust like a very talented approximation with good bedside manners.

Public links:

- PyPI: `https://pypi.org/project/mot-pricing/`
- TestPyPI: `https://test.pypi.org/project/mot-pricing/`
- Docs: `https://anouarmohamed.github.io/NoteBook/`
- Repository: `https://github.com/AnouarMohamed/NoteBook`

## The Problem In One Breath

The core object is a coupling `P` such that:

- `S1 ~ mu1`
- `S2 ~ mu2`
- `E[S2 | S1] = S1`

Then I maximize or minimize `E_P[payoff(S1, S2)]` over all such couplings.

In discrete form, that becomes the linear program I actually care about:

```text
maximize or minimize   sum_{i,j} pi_ij c(x_i, y_j)
subject to             sum_j pi_ij = mu_i
                       sum_i pi_ij = nu_j
                       sum_j pi_ij (y_j - x_i) = 0    for each i
                       pi_ij >= 0
```

That formulation is blunt in a good way. Every modeling commitment is sitting on the table.

## What The Gallery Is Saying Right Now

The current built-in gallery gives a nice spread of behaviors:

- The reference `|S2 - S1|` experiment lands at a discrete lower bound of `0.6087` and upper bound of `0.9975`.
- The call-on-spread case is narrower, with bounds `0.1894` to `0.3841`.
- The put-on-spread sibling sits higher, from `0.4394` to `0.6341`.
- The centered straddle is the most dramatic example in the shipped gallery, with interval width about `0.4155`.
- The wider absolute-spread system pushes the upper bound to `1.3101` and is the broadest absolute-spread experiment on the site.
- The quadratic spread behaves almost suspiciously well: lower and upper agree to four decimals, so the interval collapses numerically in this setup.

I like that mix because it shows more than one personality of the problem. Some payoffs care mostly about dispersion, some care about direction, and some turn out to be far more rigid than they first appear.

## Why I Bothered Packaging This

The notebook was a good start, but I did not want the final story to depend on which cell happened to be run last. The package version fixes a few important things:

- unrestricted coupling benchmarks are labeled correctly
- the regularized dual is compared to the regularized primal, not to raw `E[payoff]`
- the regularized update is handled in log space instead of asking exponentials to behave heroically
- convex-order feasibility is checked explicitly before I pretend a martingale should exist
- experiments now write plots and machine-readable summaries instead of evaporating into notebook state

## What Is On This Site

- [Research Notes](research-notes.md): the modeling point of view, what I think is exact, and what I treat as approximation.
- [Numerical Notes](numerical-notes.md): how I read dual gaps, martingale errors, and `eps`-dependent behavior without becoming mystical about it.
- [Getting Started](getting-started.md): the shortest path from `pip install` to actual artifacts on disk.
- [Examples](examples.md): the gallery, with commentary instead of plot-dumping.
- [API Guide](api.md): the functions I would actually import if I were scripting experiments.
- [Upgrade Notes](upgrade_notes.md): what changed when the notebook became a package.
- [Publishing](publishing.md): release and trusted-publisher notes for this repository.

## What I Think This Project Is Good For

- getting exact discrete MOT bounds for two-step experiments
- sanity-checking entropic approximations against an LP benchmark
- comparing how different spread-type payoffs respond to the same marginals
- producing reproducible plots and JSON summaries for research notes or small reports
- learning the geometry of simple martingale constraints without dragging in an entire industrial stack

## Start Here

If you want the fast route:

1. go to [Getting Started](getting-started.md)
2. run `mot-uniform` once
3. open [Examples](examples.md)
4. read [Numerical Notes](numerical-notes.md) before trusting very small `eps` too much

That order mirrors how I use the repo myself: first make it run, then make it interesting, then decide what deserves confidence.
