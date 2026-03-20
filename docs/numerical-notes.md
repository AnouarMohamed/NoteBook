# Numerical Notes

This is the page where I admit that numerical work has moods. The objective here is not to romanticize that fact, only to keep it visible.
{: .lead }

## The Convex-Order Check Is The Bouncer

Before I solve anything, I run the discrete convex-order check.

Why I care:

- the means have to agree
- discrete call-price inequalities have to go the right way
- if those conditions fail, a martingale coupling is not supposed to exist

In other words, the convex-order check keeps me from blaming the solver for refusing to solve an impossible problem.

## How I Read `eps`

Smaller `eps` usually means:

- less smoothing
- a regularized expected payoff closer to the exact LP benchmark
- more iterations
- greater numerical stiffness

Larger `eps` usually means:

- easier convergence
- smoother behavior
- more bias relative to the exact objective

I like regularization paths because they make this tradeoff visible instead of philosophical.

## Why `expected_payoff` And `regularized_primal` Are Both Stored

This is one of the details that is easy to blur in a notebook and worth keeping distinct in code.

- `expected_payoff` is the raw expectation of the payoff under the regularized plan
- `regularized_primal` is the objective that includes the entropy term

Those are not interchangeable quantities. If I compare the wrong one to the dual, I can manufacture confusion very efficiently.

## Dual Gaps And Constraint Errors

When I inspect `summary.json`, I look at four diagnostic families:

- dual gap
- marginal-1 error
- marginal-2 error
- martingale error

My rule of thumb is simple:

- tiny errors mean the numerics are behaving
- large errors mean I should stop admiring the plot and start debugging

The current gallery runs are in the healthy regime. For example, the reference absolute-spread case at `eps = 0.1` has martingale error on the order of `1e-8`, which is exactly the kind of number I want to see.

## The Small-`eps` Temptation

The usual temptation is to push `eps` smaller and smaller until the approximation hugs the LP benchmark. Sometimes that works. Sometimes it just turns into a very expensive way to learn that floating-point arithmetic is not sentimental.

This repo already fixed one version of that story by moving the delicate update into log space. I prefer that approach to pretending overflow warnings are part of the scientific method.

## Reading The Gallery Diagnostics

The diagnostics plot has three panels:

- absolute dual gap
- martingale constraint error
- iteration count

I read them in exactly that order.

Why:

- the dual gap tells me whether primal and dual stories agree
- the martingale error tells me whether the defining constraint is being respected
- the iteration count tells me what the approximation is costing me

If the first two are small, I can live with the third being larger. If the first two are ugly, a low iteration count is not a consolation prize.

## A Few Numerical Personalities In The Gallery

The current examples have notably different behavior:

- `uniform_abs_spread`: clean benchmark, visible regularization bias, strong reference case
- `call_spread` and `put_spread`: narrower intervals, good for directional comparisons
- `quadratic_spread`: nearly rigid, which is almost funny after the more flexible examples
- `centered_straddle`: wider interval and a good reminder that symmetry does not imply simplicity
- `wide_abs`: larger variance in `S2`, larger robust interval, still numerically well-behaved

That range is useful because it keeps me from mistaking one problem's temperament for a law of nature.

## Known Sharp Edges

Things I still treat with appropriate caution:

- very small `eps` can become numerically stiff
- coarse discretizations can tell an oversimplified story
- a pretty plan plot is not proof of correctness by itself
- exactness here is exactness for the discrete LP, not a direct proof about the underlying continuous problem

Those are not defects so much as the terms of engagement.

## My Practical Rule

If I need one sentence to summarize my numerical attitude here, it is this:

Use the LP to decide what is true in the discrete model, use the entropic solver to explore how that truth is approached, and keep the diagnostics close enough that optimism has to earn permission.
