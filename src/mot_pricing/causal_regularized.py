"""Causal multi-period regularized MOT helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np
from numpy.typing import NDArray

from .exact import constraint_errors
from .marginals import CausalMarginalChain
from .regularized import RegularizedMOTResult, sinkhorn_mot


Array1D = NDArray[np.float64]
ArrayND = NDArray[np.float64]
PayoffFunction = Callable[[ArrayND, ArrayND], ArrayND]


@dataclass(frozen=True)
class CausalConstraintErrors:
    marginal_1_errors: Array1D
    marginal_2_errors: Array1D
    martingale_errors: Array1D

    @property
    def max_marginal_error(self) -> float:
        if len(self.marginal_1_errors) == 0:
            return 0.0
        return float(
            max(self.marginal_1_errors.max(), self.marginal_2_errors.max())
        )

    @property
    def max_martingale_error(self) -> float:
        if len(self.martingale_errors) == 0:
            return 0.0
        return float(self.martingale_errors.max())


@dataclass(frozen=True)
class CausalMOTResult:
    eps: float
    steps: tuple[RegularizedMOTResult, ...]
    causal_plan: ArrayND
    overall_expected_payoff: float
    converged: bool
    per_step_dual_gap: Array1D
    constraint_errors: CausalConstraintErrors


def _pair_payoff_matrix(
    marginal_1_atoms: Array1D,
    marginal_2_atoms: Array1D,
    payoff_fn: PayoffFunction,
) -> ArrayND:
    x_grid, y_grid = np.meshgrid(marginal_1_atoms, marginal_2_atoms, indexing="ij")
    payoff_matrix = np.asarray(payoff_fn(x_grid, y_grid), dtype=float)
    if payoff_matrix.shape != (len(marginal_1_atoms), len(marginal_2_atoms)):
        raise ValueError("payoff_fn must return an array shaped like the atom grid")
    return payoff_matrix


def reconstruct_causal_plan(
    chain: CausalMarginalChain,
    steps: tuple[RegularizedMOTResult, ...] | list[RegularizedMOTResult],
) -> ArrayND:
    """Recover the full Markov joint tensor from adjacent regularized couplings."""
    if len(steps) != chain.step_count:
        raise ValueError("number of step results must match chain.step_count")

    causal_plan: ArrayND = np.asarray(steps[0].plan, dtype=float)
    for step_index, step_result in enumerate(steps[1:], start=1):
        conditioning_weights = chain.marginals[step_index].weights
        kernel = np.zeros_like(step_result.plan)
        np.divide(
            step_result.plan,
            conditioning_weights[:, None],
            out=kernel,
            where=conditioning_weights[:, None] > 0.0,
        )
        causal_plan = np.einsum("...i,ij->...ij", causal_plan, kernel)
    return causal_plan


def _adjacent_plan_from_joint(causal_plan: ArrayND, step_index: int) -> ArrayND:
    keep_axes = {step_index, step_index + 1}
    sum_axes = tuple(axis for axis in range(causal_plan.ndim) if axis not in keep_axes)
    return causal_plan.sum(axis=sum_axes) if sum_axes else causal_plan


def causal_constraint_errors(
    chain: CausalMarginalChain,
    causal_plan: ArrayND,
) -> CausalConstraintErrors:
    """Return adjacent marginal and martingale errors across the full chain."""
    expected_shape = tuple(marginal.size for marginal in chain.marginals)
    if causal_plan.shape != expected_shape:
        raise ValueError(
            f"causal_plan shape {causal_plan.shape} does not match {expected_shape}"
        )

    marginal_1_errors = []
    marginal_2_errors = []
    martingale_errors = []
    for step_index, (marginal_1, marginal_2) in enumerate(chain.pairs()):
        adjacent_plan = _adjacent_plan_from_joint(causal_plan, step_index)
        marginal_1_error, marginal_2_error, martingale_error = constraint_errors(
            adjacent_plan,
            marginal_1.weights,
            marginal_2.weights,
            marginal_1.atoms,
            marginal_2.atoms,
        )
        marginal_1_errors.append(marginal_1_error)
        marginal_2_errors.append(marginal_2_error)
        martingale_errors.append(martingale_error)

    return CausalConstraintErrors(
        marginal_1_errors=np.asarray(marginal_1_errors, dtype=float),
        marginal_2_errors=np.asarray(marginal_2_errors, dtype=float),
        martingale_errors=np.asarray(martingale_errors, dtype=float),
    )


def causal_sinkhorn_mot(
    chain: CausalMarginalChain,
    payoff_fn: PayoffFunction,
    eps: float,
    *,
    n_iter: int = 500,
    tol: float = 1e-7,
) -> CausalMOTResult:
    """Run pairwise Sinkhorn MOT over each adjacent step of a causal chain.

    The Phase 2 implementation treats the multi-period payoff as additive over
    adjacent transitions, using ``payoff_fn(S_t, S_{t+1})`` at each step.
    """
    steps: list[RegularizedMOTResult] = []
    for marginal_1, marginal_2 in chain.pairs():
        payoff_matrix = _pair_payoff_matrix(
            marginal_1.atoms,
            marginal_2.atoms,
            payoff_fn,
        )
        steps.append(
            sinkhorn_mot(
                marginal_1.atoms,
                marginal_1.weights,
                marginal_2.atoms,
                marginal_2.weights,
                payoff_matrix,
                eps,
                n_iter=n_iter,
                tol=tol,
            )
        )

    step_tuple = tuple(steps)
    causal_plan = reconstruct_causal_plan(chain, step_tuple)
    errors = causal_constraint_errors(chain, causal_plan)
    per_step_dual_gap = np.asarray([step.dual_gap for step in step_tuple], dtype=float)

    return CausalMOTResult(
        eps=eps,
        steps=step_tuple,
        causal_plan=causal_plan,
        overall_expected_payoff=float(
            sum(step.expected_payoff for step in step_tuple)
        ),
        converged=all(step.converged for step in step_tuple),
        per_step_dual_gap=per_step_dual_gap,
        constraint_errors=errors,
    )
