import json
from pathlib import Path

from mot_pricing import (
    CausalMarginalChain,
    make_builtin_payoff,
    run_causal_experiment,
    save_causal_experiment_artifacts,
)


def test_run_causal_experiment_returns_exact_and_regularized_results():
    chain = CausalMarginalChain.from_uniform_intervals(
        (
            (1.0, 3.0, 4),
            (0.5, 3.5, 4),
            (0.0, 4.0, 4),
        )
    )
    payoff = make_builtin_payoff("abs_spread")

    result = run_causal_experiment(
        chain,
        payoff,
        eps_values=(0.2,),
        sinkhorn_iterations=250,
        sinkhorn_tolerance=1e-6,
    )

    assert result.step_count == 2
    assert result.feasibility.feasible
    assert result.exact_upper.value >= result.exact_lower.value
    assert result.pairwise_upper_bound >= result.exact_upper.value
    assert result.causal_bound_gap.absolute_gap >= -1e-10
    assert 0.2 in result.regularized_results
    assert len(result.per_step_plans[0.2]) == 2


def test_save_causal_experiment_artifacts_writes_expected_files(tmp_path: Path):
    chain = CausalMarginalChain.from_uniform_intervals(
        (
            (1.0, 3.0, 4),
            (0.5, 3.5, 4),
            (0.0, 4.0, 4),
        )
    )
    result = run_causal_experiment(
        chain,
        make_builtin_payoff("abs_spread"),
        eps_values=(0.2,),
        sinkhorn_iterations=250,
        sinkhorn_tolerance=1e-6,
    )

    save_causal_experiment_artifacts(tmp_path, result)

    assert (tmp_path / "causal_transport_chain.png").exists()
    assert (tmp_path / "causal_bound_convergence.png").exists()
    assert (tmp_path / "marginal_evolution.png").exists()
    assert (tmp_path / "causal_vs_unconstrained.png").exists()
    assert (tmp_path / "causal_summary.json").exists()
    assert (tmp_path / "causal_experiment_report.md").exists()

    summary = json.loads((tmp_path / "causal_summary.json").read_text())
    assert summary["step_count"] == 2
    assert summary["regularized"]["0.2"]["converged"]
