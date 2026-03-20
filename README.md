# MOT Pricing

`mot-pricing` turns the original one-off notebook into a reproducible Python project for robust pricing with martingale optimal transport (MOT).

The reference experiment in this repository studies:

- `S1 ~ Uniform[1, 3]`
- `S2 ~ Uniform[0, 4]`
- payoff `|S1 - S2|`
- exact martingale constraint `E[S2 | S1] = S1`

The codebase includes:

- an exact linear-programming solver for discrete MOT
- a numerically stable entropic regularization solver
- corrected unrestricted coupling benchmarks
- a CLI and script to reproduce the uniform example
- tests for the exact and regularized solvers

## Why this repo exists

The original notebook had strong ideas but mixed together derivation, experimentation, plotting, and solver logic. It also had a few correctness and presentation issues:

- unrestricted benchmark labels were flipped
- the dual value was compared to the wrong primal quantity in the regularized section
- the `h` update used direct exponentials and produced overflow warnings

This project keeps the same experiment while packaging it into reusable, testable code.

## Quick Start

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .[dev]
pytest
mot-uniform --n 50 --eps 1.0 0.3 0.1 0.03 0.01 --output-dir artifacts
```

If you prefer not to install the package in editable mode:

```bash
pip install -r requirements.txt
python scripts/run_uniform_abs_spread.py --output-dir artifacts
```

## Expected Results

For the default uniform example:

- the exact MOT upper value converges toward `1.0`
- the lower value is about `0.6`
- the unrestricted comonotone coupling is the minimum benchmark
- the unrestricted countermonotone coupling is the maximum benchmark
- the regularized value approaches the exact LP value as `eps -> 0`

## Repo Layout

- `src/mot_pricing/`: solver library
- `scripts/`: runnable entry script
- `tests/`: regression and numerical checks
- `notebooks/`: notebook material preserved from the original exploration

## Notebook Status

The original notebook is preserved under `notebooks/` as legacy exploratory work. The library and CLI are now the canonical implementation.
