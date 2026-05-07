import numpy as np
import pytest

from mot_pricing import (
    CausalMarginalChain,
    check_causal_feasibility,
    make_uniform_marginal,
)


def test_causal_chain_accepts_feasible_three_step_uniform_chain():
    chain = CausalMarginalChain.from_uniform_intervals(
        (
            (1.0, 3.0, 20),
            (0.5, 3.5, 20),
            (0.0, 4.0, 20),
        )
    )

    report = check_causal_feasibility(chain)

    assert chain.marginal_count == 3
    assert chain.step_count == 2
    assert len(chain.pairs()) == 2
    assert report.feasible
    assert np.all(np.abs(report.mean_gaps) < 1e-10)
    assert np.all(report.min_call_gaps >= -1e-10)
    assert "feasible across 2 steps" in report.summary


def test_causal_chain_rejects_consecutive_mean_mismatch():
    marginal_1 = make_uniform_marginal(1.0, 3.0, 10, name="S1")
    marginal_2 = make_uniform_marginal(1.0, 4.0, 10, name="S2")

    with pytest.raises(ValueError, match="consecutive matching means"):
        CausalMarginalChain((marginal_1, marginal_2))


def test_causal_feasibility_reports_convex_order_failure():
    wide = make_uniform_marginal(0.0, 4.0, 20, name="wide")
    narrow = make_uniform_marginal(1.0, 3.0, 20, name="narrow")
    chain = CausalMarginalChain((wide, narrow))

    report = check_causal_feasibility(chain)

    assert not report.feasible
    assert report.min_call_gaps[0] < 0.0
    assert report.step_checks[0].min_call_gap < 0.0
    assert "infeasible at step(s) 1" in report.summary


def test_causal_chain_from_uniform_intervals_names_marginals_and_builds_grids():
    chain = CausalMarginalChain.from_uniform_intervals(
        (
            (1.0, 3.0, 5),
            (0.0, 4.0, 5),
        )
    )

    assert tuple(marginal.name for marginal in chain.marginals) == ("S1", "S2")
    assert chain.marginals[0].size == 5
    assert chain.marginals[1].size == 5
    assert np.allclose(chain.marginals[0].weights, np.full(5, 0.2))
