import numpy as np

from mot_pricing import (
    CausalMarginalChain,
    causal_constraint_errors,
    causal_sinkhorn_mot,
    reconstruct_causal_plan,
    sinkhorn_mot,
)


def test_causal_sinkhorn_t2_matches_regularized_solver():
    chain = CausalMarginalChain.from_uniform_intervals(
        (
            (1.0, 3.0, 10),
            (0.0, 4.0, 10),
        )
    )
    marginal_1, marginal_2 = chain.marginals
    x_grid, y_grid = np.meshgrid(marginal_1.atoms, marginal_2.atoms, indexing="ij")
    payoff_matrix = np.abs(y_grid - x_grid)

    expected = sinkhorn_mot(
        marginal_1.atoms,
        marginal_1.weights,
        marginal_2.atoms,
        marginal_2.weights,
        payoff_matrix,
        eps=0.1,
        n_iter=300,
        tol=1e-6,
    )
    actual = causal_sinkhorn_mot(
        chain,
        lambda s_t, s_next: np.abs(s_next - s_t),
        eps=0.1,
        n_iter=300,
        tol=1e-6,
    )

    assert len(actual.steps) == 1
    assert actual.converged == expected.converged
    assert np.isclose(actual.overall_expected_payoff, expected.expected_payoff)
    assert np.allclose(actual.causal_plan, expected.plan)
    assert np.allclose(actual.per_step_dual_gap, [expected.dual_gap])


def test_causal_sinkhorn_reconstructs_three_step_joint_plan():
    chain = CausalMarginalChain.from_uniform_intervals(
        (
            (1.0, 3.0, 8),
            (0.5, 3.5, 8),
            (0.0, 4.0, 8),
        )
    )

    result = causal_sinkhorn_mot(
        chain,
        lambda s_t, s_next: np.abs(s_next - s_t),
        eps=0.15,
        n_iter=350,
        tol=1e-6,
    )
    reconstructed = reconstruct_causal_plan(chain, result.steps)
    errors = causal_constraint_errors(chain, result.causal_plan)

    assert len(result.steps) == 2
    assert result.causal_plan.shape == (8, 8, 8)
    assert np.isclose(result.causal_plan.sum(), 1.0)
    assert np.allclose(result.causal_plan, reconstructed)
    assert result.overall_expected_payoff == sum(
        step.expected_payoff for step in result.steps
    )
    assert errors.max_marginal_error < 1e-5
    assert errors.max_martingale_error < 1e-5
    assert result.constraint_errors.max_marginal_error < 1e-5
    assert result.constraint_errors.max_martingale_error < 1e-5
