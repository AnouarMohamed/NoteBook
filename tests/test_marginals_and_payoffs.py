import numpy as np

from mot_pricing import (
    check_convex_order_discrete,
    make_builtin_payoff,
    make_uniform_marginal,
    run_two_uniform_experiment,
)


def test_convex_order_accepts_reference_uniform_example():
    marginal_1 = make_uniform_marginal(1.0, 3.0, 20, name="S1")
    marginal_2 = make_uniform_marginal(0.0, 4.0, 20, name="S2")

    check = check_convex_order_discrete(marginal_1, marginal_2)

    assert check.feasible
    assert abs(check.mean_gap) < 1e-10
    assert check.min_call_gap >= -1e-10


def test_convex_order_rejects_more_concentrated_second_marginal():
    marginal_1 = make_uniform_marginal(0.0, 4.0, 20, name="wide")
    marginal_2 = make_uniform_marginal(1.0, 3.0, 20, name="narrow")

    check = check_convex_order_discrete(marginal_1, marginal_2)

    assert not check.feasible
    assert check.min_call_gap < 0.0


def test_builtin_payoffs_match_expected_pointwise_values():
    s1 = np.array([[1.0, 2.0]])
    s2 = np.array([[3.0, 1.0]])

    call = make_builtin_payoff("call_on_spread", strike=0.5)
    put = make_builtin_payoff("put_on_spread", strike=0.5)
    straddle = make_builtin_payoff("straddle_on_spread", strike=0.5)

    assert np.allclose(call.function(s1, s2), [[1.5, 0.0]])
    assert np.allclose(put.function(s1, s2), [[0.0, 1.5]])
    assert np.allclose(straddle.function(s1, s2), [[1.5, 1.5]])


def test_generic_two_uniform_experiment_supports_other_payoffs():
    experiment = run_two_uniform_experiment(
        x_interval=(1.0, 3.0),
        y_interval=(0.0, 4.0),
        n=12,
        payoff_name="call_on_spread",
        strike=0.25,
        eps_values=(),
    )

    assert experiment.payoff.name == "call_on_spread"
    assert experiment.unrestricted_benchmarks is None
    assert experiment.exact_upper.value >= experiment.exact_lower.value
