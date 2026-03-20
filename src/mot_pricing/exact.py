"""Exact discrete martingale optimal transport solved as a linear program."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Literal

import numpy as np
from numpy.typing import NDArray
from scipy.optimize import linprog


Array1D = NDArray[np.float64]
Array2D = NDArray[np.float64]
Objective = Literal["max", "min"]


def _as_prob_vector(name: str, values: Array1D) -> Array1D:
    vector = np.asarray(values, dtype=float)
    if vector.ndim != 1:
        raise ValueError(f"{name} must be one-dimensional")
    if np.any(vector < 0):
        raise ValueError(f"{name} must be non-negative")
    total = float(vector.sum())
    if not np.isclose(total, 1.0, atol=1e-10):
        raise ValueError(f"{name} must sum to 1.0, got {total}")
    return vector


def _as_atom_vector(name: str, values: Array1D) -> Array1D:
    vector = np.asarray(values, dtype=float)
    if vector.ndim != 1:
        raise ValueError(f"{name} must be one-dimensional")
    if len(vector) == 0:
        raise ValueError(f"{name} must be non-empty")
    return vector


def _validate_problem(
    x_atoms: Array1D,
    alpha: Array1D,
    y_atoms: Array1D,
    beta: Array1D,
) -> tuple[Array1D, Array1D, Array1D, Array1D]:
    x_atoms = _as_atom_vector("x_atoms", x_atoms)
    y_atoms = _as_atom_vector("y_atoms", y_atoms)
    alpha = _as_prob_vector("alpha", alpha)
    beta = _as_prob_vector("beta", beta)
    if len(x_atoms) != len(alpha):
        raise ValueError("x_atoms and alpha must have matching lengths")
    if len(y_atoms) != len(beta):
        raise ValueError("y_atoms and beta must have matching lengths")

    mean_x = float(np.dot(x_atoms, alpha))
    mean_y = float(np.dot(y_atoms, beta))
    if not np.isclose(mean_x, mean_y, atol=1e-10):
        raise ValueError(
            "martingale feasibility requires matching means: "
            f"mean_x={mean_x}, mean_y={mean_y}"
        )
    return x_atoms, alpha, y_atoms, beta


def constraint_errors(
    plan: Array2D,
    alpha: Array1D,
    beta: Array1D,
    x_atoms: Array1D,
    y_atoms: Array1D,
) -> tuple[float, float, float]:
    """Return the max absolute errors of both marginals and the martingale rows."""
    marginal_1 = float(np.max(np.abs(plan.sum(axis=1) - alpha)))
    marginal_2 = float(np.max(np.abs(plan.sum(axis=0) - beta)))
    martingale_row_values = plan @ y_atoms
    martingale_target = alpha * x_atoms
    martingale = float(np.max(np.abs(martingale_row_values - martingale_target)))
    return marginal_1, marginal_2, martingale


@dataclass(frozen=True)
class ExactMOTResult:
    objective: Objective
    value: float
    plan: Array2D
    payoff_matrix: Array2D
    marginal_1_error: float
    marginal_2_error: float
    martingale_error: float


def solve_exact_mot(
    x_atoms: Array1D,
    alpha: Array1D,
    y_atoms: Array1D,
    beta: Array1D,
    payoff_fn: Callable[[Array2D, Array2D], Array2D],
    objective: Objective = "max",
) -> ExactMOTResult:
    """Solve the discrete martingale optimal transport problem exactly."""
    if objective not in {"max", "min"}:
        raise ValueError("objective must be 'max' or 'min'")

    x_atoms, alpha, y_atoms, beta = _validate_problem(x_atoms, alpha, y_atoms, beta)

    m1, m2 = len(x_atoms), len(y_atoms)
    flat_size = m1 * m2

    x_grid, y_grid = np.meshgrid(x_atoms, y_atoms, indexing="ij")
    payoff_matrix = np.asarray(payoff_fn(x_grid, y_grid), dtype=float)
    if payoff_matrix.shape != (m1, m2):
        raise ValueError("payoff_fn must return an array shaped like the atom grid")

    sign = -1.0 if objective == "max" else 1.0
    c = sign * payoff_matrix.ravel()

    n_eq = m1 + m2 + m1
    a_eq = np.zeros((n_eq, flat_size), dtype=float)
    b_eq = np.zeros(n_eq, dtype=float)
    row = 0

    for i in range(m1):
        a_eq[row, i * m2 : (i + 1) * m2] = 1.0
        b_eq[row] = alpha[i]
        row += 1

    for j in range(m2):
        a_eq[row, j::m2] = 1.0
        b_eq[row] = beta[j]
        row += 1

    for i in range(m1):
        a_eq[row, i * m2 : (i + 1) * m2] = y_atoms
        b_eq[row] = alpha[i] * x_atoms[i]
        row += 1

    result = linprog(
        c,
        A_eq=a_eq,
        b_eq=b_eq,
        bounds=[(0.0, None)] * flat_size,
        method="highs",
    )
    if result.status != 0:
        raise RuntimeError(f"LP solve failed: {result.message}")

    value = float(-result.fun if objective == "max" else result.fun)
    plan = result.x.reshape(m1, m2)
    marginal_1_error, marginal_2_error, martingale_error = constraint_errors(
        plan, alpha, beta, x_atoms, y_atoms
    )

    return ExactMOTResult(
        objective=objective,
        value=value,
        plan=plan,
        payoff_matrix=payoff_matrix,
        marginal_1_error=marginal_1_error,
        marginal_2_error=marginal_2_error,
        martingale_error=martingale_error,
    )
