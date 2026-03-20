from mot_pricing import make_uniform_grid, sinkhorn_mot, solve_exact_mot


def test_regularized_solver_has_small_duality_gap():
    x_atoms, alpha = make_uniform_grid(1.0, 3.0, 10)
    y_atoms, beta = make_uniform_grid(0.0, 4.0, 10)
    exact = solve_exact_mot(
        x_atoms, alpha, y_atoms, beta, lambda x, y: abs(x - y), objective="max"
    )

    result = sinkhorn_mot(
        x_atoms,
        alpha,
        y_atoms,
        beta,
        exact.payoff_matrix,
        eps=0.1,
        n_iter=300,
        tol=1e-6,
    )

    assert result.expected_payoff > 0.8
    assert result.regularized_primal <= result.dual_value + 5e-6
    assert abs(result.dual_gap) < 5e-6
    assert result.marginal_1_error < 1e-5
    assert result.marginal_2_error < 1e-5
    assert result.martingale_error < 1e-5
