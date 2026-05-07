from pathlib import Path

import numpy as np

from mot_pricing import ot_bound_vs_timestep, plot_continuous_limit


def test_ot_bound_vs_timestep_runs_small_convergence_study():
    result = ot_bound_vs_timestep(
        (1.0, 3.0),
        (0.0, 4.0),
        "abs_spread",
        n_atoms=3,
        T_values=(2, 3),
        eps=0.2,
    )

    assert np.allclose(result.T_values, [2.0, 3.0])
    assert result.upper_bounds.shape == (2,)
    assert result.lower_bounds.shape == (2,)
    assert len(result.experiments) == 2
    assert result.payoff_name == "abs_spread"


def test_plot_continuous_limit_writes_expected_file(tmp_path: Path):
    result = ot_bound_vs_timestep(
        (1.0, 3.0),
        (0.0, 4.0),
        "abs_spread",
        n_atoms=3,
        T_values=(2, 3),
        eps=0.2,
    )

    plot_continuous_limit(tmp_path, result)

    assert (tmp_path / "continuous_limit.png").exists()
