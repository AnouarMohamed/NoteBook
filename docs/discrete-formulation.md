# Discrete Formulation

This page records the discrete formulation implemented by the package and explains how the linear constraints correspond to the underlying martingale problem.
{: .lead }

## Continuous Statement

The starting point is a pair of marginals `mu1` and `mu2` and the class of couplings `P` such that:

- `S1 ~ mu1`
- `S2 ~ mu2`
- `E[S2 | S1] = S1`

Given a payoff `c(S1, S2)`, the objective is to compute extremal values of `E_P[c(S1, S2)]` over this admissible class.

## Discretization

The package uses midpoint-style uniform grids for the built-in uniform examples and arbitrary discrete atoms for the general discrete interface.

Let:

- `x_1, ..., x_m` denote the atoms of the first marginal
- `y_1, ..., y_n` denote the atoms of the second marginal
- `alpha_i` denote the weights of the first marginal
- `beta_j` denote the weights of the second marginal
- `pi_ij` denote the coupling weights

The coupling is represented as a nonnegative matrix `Pi = (pi_ij)`.

## Constraint Structure

The matrix `Pi` must satisfy three sets of linear constraints.

### First Marginal

For each `i`:

```text
sum_j pi_ij = alpha_i
```

This enforces the distribution of `S1`.

### Second Marginal

For each `j`:

```text
sum_i pi_ij = beta_j
```

This enforces the distribution of `S2`.

### Martingale Rows

For each `i`:

```text
sum_j pi_ij y_j = alpha_i x_i
```

Equivalently,

```text
sum_j pi_ij (y_j - x_i) = 0
```

This is the discrete form of the martingale condition `E[S2 | S1 = x_i] = x_i` whenever `alpha_i > 0`.

## Linear Objective

For a payoff matrix `c_ij = c(x_i, y_j)`, the exact optimization problem is:

```text
maximize or minimize   sum_{i,j} pi_ij c_ij
subject to             Pi satisfies the marginal and martingale constraints
                       pi_ij >= 0
```

The package solves this problem with `scipy.optimize.linprog` using the HiGHS backend.

## Why Convex Order Appears

A martingale coupling between two one-dimensional laws requires matching means and convex order. In the discrete setting used here, convex order is checked through call-price inequalities on a finite strike grid.

For strikes `K`, the comparison is:

```text
E[(S2 - K)+] - E[(S1 - K)+] >= 0
```

up to numerical tolerance, together with equality of means.

This check does not replace the LP solve, but it is a useful feasibility diagnostic before optimization begins.

## Exact Versus Regularized Problems

The package contains two computational layers.

### Exact Layer

The exact layer solves the discrete LP directly. This is the benchmark for the discretized problem.

### Regularized Layer

The regularized layer solves an entropy-penalized approximation indexed by `eps`.

This layer is useful for:

- tracing approximation paths
- studying convergence behavior
- producing smoother computational experiments

The regularized objective is not identical to the raw payoff expectation. Both are recorded explicitly in the output artifacts.

## Interpretation

The exact solution should be interpreted as exact for the chosen discrete problem, not as a direct theorem about the underlying continuous problem without additional analysis. The discretization is therefore part of the model used for computation, and not merely an implementation detail.
