"""Exact discrete martingale optimal transport solved as a linear program."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Literal

import numpy as np
from numpy.typing import NDArray
from scipy.optimize import linprog


Array1D = NDArray[np.float64]
Array2D = NDArray[np.float64]
ArrayND = NDArray[np.float64]
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
    plan: ArrayND
    payoff_matrix: ArrayND
    marginal_1_error: float
    marginal_2_error: float
    martingale_error: float
    causal_plan: ArrayND | None = None


@dataclass(frozen=True)
class CausalBoundGap:
    absolute_gap: float
    relative_gap: float


def solve_exact_mot(
    x_atoms: Array1D,
    alpha: Array1D,
    y_atoms: Array1D,
    beta: Array1D,
    payoff_fn: Callable[[Array2D, Array2D], Array2D],
    objective: Objective = "max",
) -> ExactMOTResult:
    """
    Solve the discrete martingale optimal transport (MOT) problem for two marginals and return the exact optimal coupling.
    
    Given source atoms `x_atoms` with weights `alpha` and target atoms `y_atoms` with weights `beta`, builds and solves a linear program that enforces the marginal constraints and the martingale constraint E[Y | X] = X. The provided `payoff_fn` is evaluated on the atom grid to form the linear objective; `objective` selects maximization or minimization of the expected payoff.
    
    Parameters:
        x_atoms: 1-D array of source atom locations.
        alpha: 1-D probability weights for `x_atoms`.
        y_atoms: 1-D array of target atom locations.
        beta: 1-D probability weights for `y_atoms`.
        payoff_fn: Callable that accepts two 2-D meshgrid arrays (X, Y) and returns a 2-D payoff array shaped (len(x_atoms), len(y_atoms)).
        objective: Either `"max"` or `"min"`, selecting whether to maximize or minimize the expected payoff.
    
    Returns:
        ExactMOTResult: Contains the solved `plan` (shape (len(x_atoms), len(y_atoms))), the evaluated `payoff_matrix`, the optimal `value` (objective value), `objective` string, and constraint fit errors (`marginal_1_error`, `marginal_2_error`, `martingale_error`). For maximization, `value` is the maximum expected payoff; for minimization, it is the minimum.
    
    Raises:
        ValueError: If `objective` is not `"max"` or `"min"`, if input validation fails (shape/weights/martingale feasibility), or if `payoff_fn` returns an array of incorrect shape.
        RuntimeError: If the linear program solver fails to find an optimal solution.
    """
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


def _evaluate_multiperiod_payoff(chain, payoff_fn: Callable[..., ArrayND]) -> ArrayND:
    """
    Evaluate the multi-period payoff on the Cartesian product of marginal atoms.
    
    Parameters:
        chain: An object with a `marginals` sequence where each marginal exposes `atoms` (1D array-like)
            and `size` (number of atoms). The function will form a grid over these atoms in the same
            order as `chain.marginals`.
        payoff_fn (callable): A function that accepts N arrays (one per marginal) representing the mesh
            grid coordinates and returns a numeric array whose shape must equal the tuple of marginal
            sizes.
    
    Returns:
        payoff_tensor (ndarray): A NumPy array of dtype float with shape equal to
            (marginal.size for marginal in chain.marginals), containing payoff_fn evaluated on the grid.
    
    Raises:
        ValueError: If the array returned by `payoff_fn` does not match the expected grid shape.
    """
    grids = np.meshgrid(
        *(marginal.atoms for marginal in chain.marginals),
        indexing="ij",
    )
    payoff_tensor = np.asarray(payoff_fn(*grids), dtype=float)
    expected_shape = tuple(marginal.size for marginal in chain.marginals)
    if payoff_tensor.shape != expected_shape:
        raise ValueError("payoff_fn must return an array shaped like the atom grid")
    return payoff_tensor


def _flat_index(indices: tuple[int, ...], shape: tuple[int, ...]) -> int:
    """
    Convert a multi-dimensional index into its flat (raveled) index for an array with the given shape.
    
    Parameters:
        indices (tuple[int, ...]): Multi-dimensional index (one integer per axis).
        shape (tuple[int, ...]): Shape of the array for which the flat index is computed.
    
    Returns:
        flat_index (int): Integer flat index corresponding to `indices` under row-major (C-style) ordering.
    
    Raises:
        ValueError: If any index is out of bounds for the corresponding dimension in `shape`.
    """
    return int(np.ravel_multi_index(indices, shape))


def solve_exact_causal_mot(
    chain,
    payoff_fn: Callable[..., ArrayND],
    objective: Objective = "max",
) -> ExactMOTResult:
    """
    Solve the multi-period discrete martingale optimal transport (causal MOT) problem exactly and return the LP solution.
    
    Parameters:
        chain: A multistep marginal chain object with attributes:
            - marginals: sequence of marginal distributions (each with .atoms and .weights)
            - step_count: number of transitions (len(marginals) - 1)
        payoff_fn: Callable that accepts N arrays (one per marginal) produced by an N-dimensional meshgrid and returns an N-dimensional payoff tensor matching the marginals' shape.
        objective: Either "max" to maximize the expected payoff or "min" to minimize it.
    
    Returns:
        ExactMOTResult containing the solved objective, optimal plan (ND array), the evaluated payoff tensor as `payoff_matrix`, marginal fit errors, martingale fit error, and `causal_plan` set to the ND plan.
    
    Raises:
        ValueError: if `objective` is not "max" or "min".
        RuntimeError: if the underlying linear program fails to find an optimal solution.
    """
    if objective not in {"max", "min"}:
        raise ValueError("objective must be 'max' or 'min'")

    shape = tuple(marginal.size for marginal in chain.marginals)
    flat_size = int(np.prod(shape))
    payoff_tensor = _evaluate_multiperiod_payoff(chain, payoff_fn)
    sign = -1.0 if objective == "max" else 1.0
    c = sign * payoff_tensor.ravel()

    marginal_rows = sum(shape)
    martingale_rows = sum(
        int(np.prod(shape[: step + 1])) for step in range(chain.step_count)
    )
    a_eq = np.zeros((marginal_rows + martingale_rows, flat_size), dtype=float)
    b_eq = np.zeros(marginal_rows + martingale_rows, dtype=float)
    row = 0

    all_indices = list(np.ndindex(shape))
    for axis, marginal in enumerate(chain.marginals):
        for atom_index, weight in enumerate(marginal.weights):
            for index in all_indices:
                if index[axis] == atom_index:
                    a_eq[row, _flat_index(index, shape)] = 1.0
            b_eq[row] = weight
            row += 1

    for step in range(chain.step_count):
        current_atoms = chain.marginals[step].atoms
        next_atoms = chain.marginals[step + 1].atoms
        prefix_shape = shape[: step + 1]
        for prefix in np.ndindex(prefix_shape):
            current_atom = current_atoms[prefix[-1]]
            for suffix in np.ndindex(shape[step + 1 :]):
                index = prefix + suffix
                next_atom = next_atoms[suffix[0]]
                a_eq[row, _flat_index(index, shape)] = next_atom - current_atom
            row += 1

    result = linprog(
        c,
        A_eq=a_eq,
        b_eq=b_eq,
        bounds=[(0.0, None)] * flat_size,
        method="highs",
    )
    if result.status != 0:
        raise RuntimeError(f"causal LP solve failed: {result.message}")

    value = float(-result.fun if objective == "max" else result.fun)
    plan = result.x.reshape(shape)
    marginal_errors = []
    for axis, marginal in enumerate(chain.marginals):
        axes = tuple(i for i in range(plan.ndim) if i != axis)
        marginal_errors.append(
            float(np.max(np.abs(plan.sum(axis=axes) - marginal.weights)))
        )

    martingale_errors = []
    for step in range(chain.step_count):
        keep_axes = {step, step + 1}
        sum_axes = tuple(axis for axis in range(plan.ndim) if axis not in keep_axes)
        adjacent = plan.sum(axis=sum_axes) if sum_axes else plan
        _, _, martingale_error = constraint_errors(
            adjacent,
            chain.marginals[step].weights,
            chain.marginals[step + 1].weights,
            chain.marginals[step].atoms,
            chain.marginals[step + 1].atoms,
        )
        martingale_errors.append(martingale_error)

    return ExactMOTResult(
        objective=objective,
        value=value,
        plan=plan,
        payoff_matrix=payoff_tensor,
        marginal_1_error=marginal_errors[0],
        marginal_2_error=float(max(marginal_errors[1:], default=0.0)),
        martingale_error=float(max(martingale_errors, default=0.0)),
        causal_plan=plan,
    )


def compute_causal_bound_gap(
    exact_causal: ExactMOTResult,
    exact_unconstrained: ExactMOTResult,
) -> CausalBoundGap:
    """
    Compute the absolute and relative gap between an unconstrained solution and a causal solution.
    
    Parameters:
        exact_causal (ExactMOTResult): Result produced by the causal solver.
        exact_unconstrained (ExactMOTResult): Result produced by the unconstrained solver.
    
    Returns:
        CausalBoundGap: `absolute_gap` is exact_unconstrained.value - exact_causal.value;
        `relative_gap` is `absolute_gap / abs(exact_unconstrained.value)` or `0.0` if
        `exact_unconstrained.value` is zero.
    """
    absolute_gap = exact_unconstrained.value - exact_causal.value
    denominator = abs(exact_unconstrained.value)
    relative_gap = 0.0 if denominator == 0.0 else absolute_gap / denominator
    return CausalBoundGap(
        absolute_gap=float(absolute_gap),
        relative_gap=float(relative_gap),
    )
