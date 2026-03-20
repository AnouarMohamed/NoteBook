# Numerical Notes

This page summarizes the numerical conventions used to interpret exact and regularized results in the package.
{: .lead }

## Convex-Order Check

The discrete convex-order check is used before solving.

Its purpose is to verify that:

- the means agree
- discrete call-price inequalities have the correct sign
- the pair of marginals is consistent with martingale feasibility

If this check fails, the problem should not be treated as admitting a martingale coupling.

## Interpretation Of `eps`

Smaller `eps` typically implies:

- less smoothing
- a regularized expected payoff closer to the exact LP benchmark
- more iterations
- increased numerical stiffness

Larger `eps` typically implies:

- easier convergence
- smoother behavior
- more bias relative to the exact objective

Regularization paths make these tradeoffs explicit.

## `expected_payoff` Versus `regularized_primal`

The package records both quantities because they are distinct:

- `expected_payoff` is the raw expectation of the payoff under the regularized plan
- `regularized_primal` is the entropy-augmented objective

These should not be compared interchangeably to dual quantities.

## Dual Gaps And Constraint Errors

The main diagnostic quantities in `summary.json` are:

- dual gap
- marginal-1 error
- marginal-2 error
- martingale error

Small values indicate stable numerical behavior and good constraint satisfaction. Larger values indicate that the run requires further inspection.

For example, the reference absolute-spread case at `eps = 0.1` has martingale error on the order of `1e-8`, which is consistent with a stable regularized run.

## Small-`eps` Regime

Reducing `eps` moves the approximation closer to the LP benchmark, but also increases numerical difficulty. The package addresses part of this issue by carrying out the delicate update in log space rather than through a direct exponential form.

Even with this modification, very small `eps` values should be interpreted with care.

## Reading The Diagnostics Plot

The diagnostics plot contains three panels:

- absolute dual gap
- martingale constraint error
- iteration count

These panels together summarize:

- whether primal and dual values are consistent
- whether the defining martingale constraint is respected
- the computational cost required to reach convergence

## Numerical Variation Across Examples

The gallery examples illustrate several different numerical regimes:

- `uniform_abs_spread`: clear benchmark with visible regularization bias
- `call_spread` and `put_spread`: narrower intervals suitable for directional comparison
- `quadratic_spread`: nearly rigid interval in the current discretization
- `centered_straddle`: wide interval under a symmetric geometric setup
- `wide_abs`: increased second-marginal variance and a correspondingly wider robust interval

## Limitations And Caution Points

The following issues should be kept in view:

- very small `eps` values may be numerically stiff
- coarse discretizations may give an oversimplified picture
- visually appealing transport plans are not sufficient evidence of correctness
- exactness here refers to the discrete LP, not directly to the underlying continuous problem

## Practical Summary

A consistent interpretation strategy is:

- use the LP solution as the discrete benchmark
- use the entropic solver to study the approximation path
- keep diagnostics central to the interpretation of every run
