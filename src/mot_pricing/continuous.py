"""Discrete continuous-limit studies for causal MOT experiments."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from .experiments import CausalExperimentResult, run_causal_experiment
from .marginals import CausalMarginalChain
from .payoffs import make_builtin_payoff


Array1D = NDArray[np.float64]


@dataclass(frozen=True)
class ContinuousLimitResult:
    T_values: Array1D
    upper_bounds: Array1D
    lower_bounds: Array1D
    convergence_rate: float
    experiments: tuple[CausalExperimentResult, ...]
    payoff_name: str
    eps: float


def _interpolate_intervals(
    x_interval: tuple[float, float],
    y_interval: tuple[float, float],
    time_steps: int,
    n_atoms: int,
) -> tuple[tuple[float, float, int], ...]:
    """
    Generate a sequence of interpolated interval triplets between two endpoint intervals for a given number of time steps.
    
    Parameters:
        x_interval (tuple[float, float]): Left and right endpoints of the starting interval.
        y_interval (tuple[float, float]): Left and right endpoints of the ending interval.
        time_steps (int): Number of interpolation points to produce; must be at least 2.
        n_atoms (int): Number of atoms to include in each returned triplet.
    
    Returns:
        tuple[tuple[float, float, int], ...]: A tuple of length `time_steps` where each element is
        `(left, right, n_atoms)`. `left` and `right` are linear interpolations of the corresponding
        endpoints of `x_interval` and `y_interval` using weights uniformly spaced from 0.0 to 1.0.
    
    Raises:
        ValueError: If `time_steps` is less than 2.
    """
    if time_steps < 2:
        raise ValueError("time_steps must be at least 2")
    weights = np.linspace(0.0, 1.0, time_steps)
    return tuple(
        (
            (1.0 - weight) * x_interval[0] + weight * y_interval[0],
            (1.0 - weight) * x_interval[1] + weight * y_interval[1],
            n_atoms,
        )
        for weight in weights
    )


def _estimate_convergence_rate(T_values: Array1D, widths: Array1D) -> float:
    """
    Estimate the convergence exponent from widths measured at discrete time-step counts.
    
    Parameters:
        T_values (Array1D): Array of time-step counts corresponding to each width.
        widths (Array1D): Array of interval widths (upper - lower) for each time step.
    
    Returns:
        float: Fitted slope of a linear regression on log(widths) vs log(1/T_values); returns `0.0` if fewer than two positive widths are available.
    """
    positive = widths > 0.0
    if int(np.count_nonzero(positive)) < 2:
        return 0.0
    x = np.log(1.0 / T_values[positive])
    y = np.log(widths[positive])
    slope, _ = np.polyfit(x, y, deg=1)
    return float(slope)


def ot_bound_vs_timestep(
    x_interval: tuple[float, float],
    y_interval: tuple[float, float],
    payoff_name: str,
    n_atoms: int,
    T_values: tuple[int, ...] = (2, 3, 5),
    eps: float = 0.1,
) -> ContinuousLimitResult:
    """
    Study how causal optimal-transport bounds evolve as the number of time steps increases.
    
    This runs causal MOT experiments for each time-step count in `T_values`, collecting exact upper and lower bounds and estimating a convergence exponent from the bound widths.
    
    Parameters:
        x_interval (tuple[float, float]): Left and right endpoints of the source uniform interval.
            The sum of `x_interval` must match the sum of `y_interval`.
        y_interval (tuple[float, float]): Left and right endpoints of the target uniform interval.
        payoff_name (str): Identifier of a built-in payoff to use for each experiment.
        n_atoms (int): Number of atoms per marginal used to construct the chains.
        T_values (tuple[int, ...], optional): Sequence of time-step counts to evaluate.
            Defaults to (2, 3, 5).
        eps (float, optional): Epsilon value passed to each causal experiment. Defaults to 0.1.
    
    Returns:
        ContinuousLimitResult: Contains:
            - T_values: array of tested time-step counts (float).
            - upper_bounds: array of exact upper bound values for each `T`.
            - lower_bounds: array of exact lower bound values for each `T`.
            - convergence_rate: estimated convergence exponent computed from bound widths.
            - experiments: tuple of the underlying `CausalExperimentResult` objects.
            - payoff_name: the `payoff_name` passed to this function.
            - eps: the `eps` value passed to this function.
    
    Raises:
        ValueError: If the sums of `x_interval` and `y_interval` do not match within 1e-10.
    """
    if not np.isclose(sum(x_interval), sum(y_interval), atol=1e-10):
        raise ValueError("x_interval and y_interval must have matching midpoint means")

    payoff = make_builtin_payoff(payoff_name)
    experiments = []
    upper_bounds = []
    lower_bounds = []
    for time_steps in T_values:
        chain = CausalMarginalChain.from_uniform_intervals(
            _interpolate_intervals(x_interval, y_interval, time_steps, n_atoms)
        )
        experiment = run_causal_experiment(
            chain,
            payoff,
            eps_values=(eps,),
            sinkhorn_iterations=600,
            sinkhorn_tolerance=1e-8,
        )
        experiments.append(experiment)
        upper_bounds.append(experiment.exact_upper.value)
        lower_bounds.append(experiment.exact_lower.value)

    t_array = np.asarray(T_values, dtype=float)
    upper_array = np.asarray(upper_bounds, dtype=float)
    lower_array = np.asarray(lower_bounds, dtype=float)
    convergence_rate = _estimate_convergence_rate(t_array, upper_array - lower_array)

    return ContinuousLimitResult(
        T_values=t_array,
        upper_bounds=upper_array,
        lower_bounds=lower_array,
        convergence_rate=convergence_rate,
        experiments=tuple(experiments),
        payoff_name=payoff_name,
        eps=eps,
    )
