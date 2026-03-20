# Research Notes

This page is the conceptual center of the project. It is where I say, plainly, what I think I am solving and what I am not pretending to solve.
{: .lead }

## The Question

I start with two marginals, `mu1` and `mu2`, and I look for couplings of `S1` and `S2` such that:

- `S1 ~ mu1`
- `S2 ~ mu2`
- `E[S2 | S1] = S1`

Then I optimize a payoff under that martingale restriction.

This is a robust-pricing problem in the most literal sense: I do not commit to a full model, only to marginals and the martingale structure. Everything I can price must survive that uncertainty.

## Why The Martingale Constraint Matters

Without the martingale condition, the transport problem is still interesting, but it is not the object I wanted. The martingale constraint forces the second step to preserve conditional mean. That is a very rigid demand, and it changes the optimizer's room to move in a way that is mathematically and financially meaningful.

In plain language: I do not merely ask for a coupling of two distributions. I ask for a coupling that behaves like a fair price process from one time step to the next.

## The Exact Discrete Formulation

The exact solver uses a discrete LP. On grids `x_i` and `y_j`, with coupling weights `pi_ij`, the problem is:

```text
maximize or minimize   sum_{i,j} pi_ij c(x_i, y_j)
subject to             sum_j pi_ij = mu_i
                       sum_i pi_ij = nu_j
                       sum_j pi_ij (y_j - x_i) = 0    for each i
                       pi_ij >= 0
```

I like this formulation because it has no mystical layer. The marginals are explicit. The martingale condition is explicit. The objective is explicit. If a numerical result looks strange, I know where to interrogate it.

## Why I Keep The Entropic Solver Around

The regularized solver is not there to replace the LP benchmark. It is there because approximation paths are useful, smooth, and often much easier to explore across parameter values.

That said, I keep a firm boundary in my head:

- the LP value is the benchmark
- the entropic value is an approximation path
- the regularized objective includes entropy and is not the same as raw expected payoff

Entropy regularization is a very useful numerical device. I am fond of it. I do not worship it.

## What The Current Gallery Taught Me

A few examples are worth keeping in memory:

- In the reference `|S2 - S1|` case, the exact interval is roughly `[0.6087, 0.9975]`, which is wide enough to be genuinely interesting.
- The call-on-spread and put-on-spread examples have the same interval width in the shipped discretization, but they sit at very different levels.
- The centered straddle case has one of the widest intervals in the gallery, which makes it a good illustration of how much optionality the martingale still leaves.
- The quadratic spread nearly collapses to a single value, which is the kind of example that keeps me from overgeneralizing from the dramatic cases.
- Widening the second marginal in the absolute-spread setup pushes the upper bound above `1.31`, which is a clean way to see how dispersion reshapes the robust interval.

## What I Trust Most

I trust results most when all of the following line up:

- convex order says a martingale should exist
- the exact LP solves cleanly
- marginal and martingale errors are tiny
- the regularized path approaches the LP benchmark as `eps` decreases
- the story stays consistent across nearby discretizations

That last point matters. A single beautiful plot is not evidence; it is an invitation to ask better questions.

## What This Repo Is Not

This repo is not:

- a continuous-time MOT library
- a giant derivatives engine
- a universal answer to transport problems beyond the small, deliberate scope here
- a claim that entropic regularization has solved numerical analysis forever

It is a compact research-grade workbench for two-step discrete MOT experiments. I would rather it be precise than grand.

## Why The Rewrite Was Worth It

The original notebook had the right instincts but also a few implementation and interpretation issues. Turning it into a package forced me to separate three layers that were previously tangled together:

- mathematics
- numerics
- presentation

Once those are separated, it becomes much easier to say what I know, what I approximate, and what I still need to check.
