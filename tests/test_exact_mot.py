import numpy as np

from mot_pricing import (
    CausalMarginalChain,
    abs_spread_uniform_benchmarks,
    compute_causal_bound_gap,
    make_uniform_grid,
    solve_exact_causal_mot,
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


def test_exact_causal_solver_matches_two_period_exact_solver():
    chain = CausalMarginalChain.from_uniform_intervals(
        (
            (1.0, 3.0, 6),
            (0.0, 4.0, 6),
        )
    )
    marginal_1, marginal_2 = chain.marginals

    exact = solve_exact_mot(
        marginal_1.atoms,
        marginal_1.weights,
        marginal_2.atoms,
        marginal_2.weights,
        lambda x, y: np.abs(y - x),
        objective="max",
    )
    causal = solve_exact_causal_mot(
        chain,
        lambda s1, s2: np.abs(s2 - s1),
        objective="max",
    )
    gap = compute_causal_bound_gap(causal, exact)

    assert np.isclose(causal.value, exact.value)
    assert np.allclose(causal.plan, exact.plan)
    assert causal.causal_plan is causal.plan
    assert abs(gap.absolute_gap) < 1e-10
    assert abs(gap.relative_gap) < 1e-10


def test_exact_causal_solver_enforces_multiperiod_constraints():
    chain = CausalMarginalChain.from_uniform_intervals(
        (
            (1.0, 3.0, 4),
            (0.5, 3.5, 4),
            (0.0, 4.0, 4),
        )
    )

    result = solve_exact_causal_mot(
        chain,
        lambda s1, s2, s3: np.abs(s2 - s1) + np.abs(s3 - s2),
        objective="max",
    )

    assert result.plan.shape == (4, 4, 4)
    assert np.isclose(result.plan.sum(), 1.0)
    assert result.value > 0.0
    assert result.marginal_1_error < 1e-10
    assert result.marginal_2_error < 1e-10
    assert result.martingale_error < 1e-10
