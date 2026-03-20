import numpy as np

from mot_pricing import (
    abs_spread_uniform_benchmarks,
    make_uniform_grid,
    solve_exact_mot,
)


def test_exact_solver_enforces_constraints():
    x_atoms, alpha = make_uniform_grid(1.0, 3.0, 20)
    y_atoms, beta = make_uniform_grid(0.0, 4.0, 20)

    result = solve_exact_mot(
        x_atoms,
        alpha,
        y_atoms,
        beta,
        lambda x, y: np.abs(x - y),
        objective="max",
    )

    assert result.value > 0.99
    assert result.marginal_1_error < 1e-10
    assert result.marginal_2_error < 1e-10
    assert result.martingale_error < 1e-10


def test_uniform_benchmarks_are_correctly_ordered():
    benchmarks = abs_spread_uniform_benchmarks((1.0, 3.0), (0.0, 4.0), num_points=50_000)

    assert np.isclose(benchmarks.unrestricted_min_comonotone, 0.5, atol=1e-3)
    assert np.isclose(benchmarks.independent, 13.0 / 12.0, atol=1e-3)
    assert np.isclose(benchmarks.unrestricted_max_countermonotone, 1.5, atol=1e-3)
    assert (
        benchmarks.unrestricted_min_comonotone
        < benchmarks.independent
        < benchmarks.unrestricted_max_countermonotone
    )
