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
    """Run causal experiments as the number of time steps increases."""
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
