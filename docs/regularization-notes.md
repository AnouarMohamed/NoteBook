# Regularization Notes

This page summarizes the entropy-regularized problem solved by the package and explains how the reported quantities should be interpreted.
{: .lead }

## Role Of Regularization

The exact LP defines the benchmark for the discretized martingale optimal transport problem. The regularized solver introduces an entropy penalty indexed by `eps` in order to obtain a smoother approximation path.

The regularized layer is useful for:

- tracing numerical behavior as smoothing is reduced
- comparing approximation quality across examples
- studying solver stability and constraint satisfaction

## Objects Recorded By The Solver

The regularized output includes the following principal quantities.

| Quantity | Meaning | Interpretation |
|---|---|---|
| `expected_payoff` | raw expectation of the payoff under the regularized plan | closest analogue of the exact objective value |
| `regularized_primal` | entropy-augmented objective | used for primal-dual consistency checks |
| `dual_value` | dual objective corresponding to the regularized problem | should be close to `regularized_primal` |
| `dual_gap` | `dual_value - regularized_primal` | small magnitude indicates internal consistency |
| `iterations` | number of iterations performed | rough measure of computational cost |
| `martingale_error` | maximum row-wise martingale deviation | checks enforcement of the defining constraint |

The distinction between `expected_payoff` and `regularized_primal` is essential. Only the latter includes the entropy contribution.

## Dependence On `eps`

The parameter `eps` controls the amount of smoothing.

| Regime | Typical Effect | Practical Consequence |
|---|---|---|
| large `eps` | smoother plans and easier convergence | more bias relative to the LP benchmark |
| moderate `eps` | stable approximation path | useful for exploratory comparison |
| small `eps` | closer approach to the LP benchmark | increased stiffness and iteration count |

This pattern is visible in the regularization-path figures shipped with the gallery.

## Internal Variables

The implementation records three dual-related arrays:

- `u1`
- `u2`
- `h`

Their purpose is summarized below.

| Variable | Role In The Solver |
|---|---|
| `u1` | first marginal dual potential |
| `u2` | second marginal dual potential |
| `h` | row-wise martingale multiplier |

These variables determine the reconstructed regularized plan and are therefore part of the full diagnostic state.

## Why Log-Space Updates Are Used

The numerically delicate update is carried out in log space rather than through a direct exponential form. This improves stability, especially in smaller-`eps` regimes where exponentials can become poorly scaled.

The current implementation therefore treats the regularized solver as a controlled approximation method rather than as a purely black-box transport routine.

## Reading The Regularization Path

A regularization-path figure should typically show:

- expected payoff moving toward the exact LP upper value as `eps` decreases
- regularized primal remaining distinct from raw expected payoff
- smaller `eps` values requiring more iterations
- dual gaps remaining small in magnitude

If this pattern breaks down, the diagnostics should be inspected before interpreting the corresponding values.

## Practical Use

In the current repository workflow, the regularized solver is most informative when used together with:

- the exact LP benchmark
- the stability diagnostics figure
- the structural diagnostics figure
- the per-example markdown report

This combination makes it possible to compare approximation quality, constraint accuracy, and geometric behavior in a single experiment directory.
