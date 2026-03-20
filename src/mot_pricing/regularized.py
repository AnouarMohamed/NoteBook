"""Entropic martingale OT solved with Sinkhorn-style fixed-point updates."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray
from scipy.optimize import brentq
from scipy.special import logsumexp

from .exact import constraint_errors


Array1D = NDArray[np.float64]
Array2D = NDArray[np.float64]


def update_u1(
    payoff_matrix: Array2D,
    displacement_matrix: Array2D,
    u2: Array1D,
    h: Array1D,
    beta: Array1D,
    eps: float,
) -> Array1D:
    """Henry-Labordere Eq. 5."""
    exponent = (payoff_matrix - u2[None, :] - h[:, None] * displacement_matrix) / eps
    return eps * logsumexp(np.log(beta)[None, :] + exponent, axis=1)


def update_u2(
    payoff_matrix: Array2D,
    displacement_matrix: Array2D,
    u1: Array1D,
    h: Array1D,
    alpha: Array1D,
    eps: float,
) -> Array1D:
    """Henry-Labordere Eq. 6."""
    exponent = (payoff_matrix - u1[:, None] - h[:, None] * displacement_matrix) / eps
    return eps * logsumexp(np.log(alpha)[:, None] + exponent, axis=0)


def _scaled_signed_difference(log_positive: float, log_negative: float) -> float:
    if np.isneginf(log_positive) and np.isneginf(log_negative):
        return 0.0
    pivot = max(log_positive, log_negative)
    return float(np.exp(log_positive - pivot) - np.exp(log_negative - pivot))


def _row_balance(
    theta: float,
    base: Array1D,
    displacement_row: Array1D,
    log_beta: Array1D,
    eps: float,
) -> float:
    positive = displacement_row > 0.0
    negative = displacement_row < 0.0

    if not np.any(positive):
        return -1.0
    if not np.any(negative):
        return 1.0

    pos_terms = (
        log_beta[positive]
        + np.log(displacement_row[positive])
        + base[positive]
        - theta * displacement_row[positive] / eps
    )
    neg_terms = (
        log_beta[negative]
        + np.log(-displacement_row[negative])
        + base[negative]
        - theta * displacement_row[negative] / eps
    )

    log_positive = float(logsumexp(pos_terms))
    log_negative = float(logsumexp(neg_terms))
    return _scaled_signed_difference(log_positive, log_negative)


def _find_root_bracket(
    func,
    *,
    start: float = 1.0,
    growth: float = 2.0,
    max_abs: float = 1e6,
    max_steps: int = 50,
) -> tuple[float, float]:
    left = -start
    right = start
    f_left = func(left)
    f_right = func(right)

    for _ in range(max_steps):
        if f_left == 0.0:
            return left, left
        if f_right == 0.0:
            return right, right
        if f_left * f_right < 0.0:
            return left, right

        left *= growth
        right *= growth
        if abs(left) > max_abs or abs(right) > max_abs:
            break
        f_left = func(left)
        f_right = func(right)

    raise RuntimeError("failed to bracket the martingale root for a Sinkhorn row")


def update_h(
    payoff_matrix: Array2D,
    displacement_matrix: Array2D,
    u2: Array1D,
    beta: Array1D,
    eps: float,
) -> Array1D:
    """Henry-Labordere Eq. 7 solved row-by-row with stable log-space balances."""
    h_new = np.zeros(payoff_matrix.shape[0], dtype=float)
    log_beta = np.log(beta)

    for row in range(payoff_matrix.shape[0]):
        base = (payoff_matrix[row] - u2) / eps
        displacement_row = displacement_matrix[row]

        def row_balance(theta: float) -> float:
            return _row_balance(theta, base, displacement_row, log_beta, eps)

        if not np.any(displacement_row > 0.0) or not np.any(displacement_row < 0.0):
            h_new[row] = 0.0
            continue

        left, right = _find_root_bracket(row_balance)
        if left == right:
            h_new[row] = left
        else:
            h_new[row] = brentq(row_balance, left, right, xtol=1e-12, maxiter=300)

    return h_new


def reconstruct_plan(
    payoff_matrix: Array2D,
    displacement_matrix: Array2D,
    u1: Array1D,
    u2: Array1D,
    h: Array1D,
    alpha: Array1D,
    beta: Array1D,
    eps: float,
) -> Array2D:
    """Reconstruct the regularized transport plan from the dual variables."""
    log_plan = (
        np.log(alpha)[:, None]
        + np.log(beta)[None, :]
        + (
            payoff_matrix
            - u1[:, None]
            - u2[None, :]
            - h[:, None] * displacement_matrix
        )
        / eps
    )
    return np.exp(log_plan)


def relative_entropy_with_prior(plan: Array2D, prior: Array2D) -> float:
    """Compute H(P|P0) = E^P[log(dP/dP0) - 1]."""
    mask = plan > 0.0
    log_ratio = np.zeros_like(plan)
    log_ratio[mask] = np.log(plan[mask] / prior[mask])
    return float(np.sum(plan[mask] * (log_ratio[mask] - 1.0)))


def regularized_primal_value(
    plan: Array2D,
    payoff_matrix: Array2D,
    prior: Array2D,
    eps: float,
) -> tuple[float, float]:
    """Return the raw expectation and the entropy-regularized primal objective."""
    expected_payoff = float(np.sum(plan * payoff_matrix))
    entropy = relative_entropy_with_prior(plan, prior)
    return expected_payoff, float(expected_payoff - eps * entropy)


def regularized_dual_value(
    payoff_matrix: Array2D,
    displacement_matrix: Array2D,
    u1: Array1D,
    u2: Array1D,
    h: Array1D,
    alpha: Array1D,
    beta: Array1D,
    eps: float,
) -> float:
    """Evaluate the dual objective that matches the entropy-regularized primal."""
    log_prior = np.log(alpha)[:, None] + np.log(beta)[None, :]
    log_integrand = log_prior + (
        payoff_matrix
        - u1[:, None]
        - u2[None, :]
        - h[:, None] * displacement_matrix
    ) / eps
    return float(
        np.dot(alpha, u1)
        + np.dot(beta, u2)
        + eps * np.exp(logsumexp(log_integrand))
    )


@dataclass(frozen=True)
class RegularizedMOTResult:
    eps: float
    iterations: int
    converged: bool
    plan: Array2D
    expected_payoff: float
    regularized_primal: float
    dual_value: float
    dual_gap: float
    marginal_1_error: float
    marginal_2_error: float
    martingale_error: float
    u1: Array1D
    u2: Array1D
    h: Array1D
    history: dict[str, list[float]]


def sinkhorn_mot(
    x_atoms: Array1D,
    alpha: Array1D,
    y_atoms: Array1D,
    beta: Array1D,
    payoff_matrix: Array2D,
    eps: float,
    *,
    n_iter: int = 500,
    tol: float = 1e-7,
) -> RegularizedMOTResult:
    """Run the Henry-Labordere fixed-point updates for the regularized MOT problem."""
    if eps <= 0.0:
        raise ValueError("eps must be positive")
    if payoff_matrix.shape != (len(x_atoms), len(y_atoms)):
        raise ValueError("payoff_matrix shape does not match the atom grids")

    displacement_matrix = y_atoms[None, :] - x_atoms[:, None]
    prior = alpha[:, None] * beta[None, :]

    u1 = np.zeros(len(x_atoms), dtype=float)
    u2 = np.zeros(len(y_atoms), dtype=float)
    h = np.zeros(len(x_atoms), dtype=float)

    history: dict[str, list[float]] = {
        "expected_payoff": [],
        "regularized_primal": [],
        "dual_gap": [],
        "marginal_1_error": [],
        "marginal_2_error": [],
        "martingale_error": [],
    }

    converged = False
    plan = np.zeros_like(payoff_matrix)

    for iteration in range(1, n_iter + 1):
        u1 = update_u1(payoff_matrix, displacement_matrix, u2, h, beta, eps)
        h = update_h(payoff_matrix, displacement_matrix, u2, beta, eps)
        u2 = update_u2(payoff_matrix, displacement_matrix, u1, h, alpha, eps)

        plan = reconstruct_plan(
            payoff_matrix, displacement_matrix, u1, u2, h, alpha, beta, eps
        )
        marginal_1_error, marginal_2_error, martingale_error = constraint_errors(
            plan, alpha, beta, x_atoms, y_atoms
        )
        expected_payoff, regularized_primal = regularized_primal_value(
            plan, payoff_matrix, prior, eps
        )
        dual_value = regularized_dual_value(
            payoff_matrix, displacement_matrix, u1, u2, h, alpha, beta, eps
        )
        dual_gap = dual_value - regularized_primal

        history["expected_payoff"].append(expected_payoff)
        history["regularized_primal"].append(regularized_primal)
        history["dual_gap"].append(dual_gap)
        history["marginal_1_error"].append(marginal_1_error)
        history["marginal_2_error"].append(marginal_2_error)
        history["martingale_error"].append(martingale_error)

        if max(marginal_1_error, marginal_2_error, martingale_error) < tol:
            converged = True
            break

    return RegularizedMOTResult(
        eps=eps,
        iterations=iteration,
        converged=converged,
        plan=plan,
        expected_payoff=expected_payoff,
        regularized_primal=regularized_primal,
        dual_value=dual_value,
        dual_gap=dual_gap,
        marginal_1_error=marginal_1_error,
        marginal_2_error=marginal_2_error,
        martingale_error=martingale_error,
        u1=u1,
        u2=u2,
        h=h,
        history=history,
    )
