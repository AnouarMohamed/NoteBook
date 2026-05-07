# Causal MOT Benchmarks

The causal benchmark compares the exact multi-period martingale LP with the
regularized causal Sinkhorn approximation on a three-step uniform chain:

```text
[1, 3] -> [0.5, 3.5] -> [0, 4]
```

The benchmark payoff is additive across adjacent transitions:

```text
|S2 - S1| + |S3 - S2|
```

Run it from a local checkout with the package on `PYTHONPATH`:

```bash
PYTHONPATH=src python scripts/benchmark_causal.py
```

The script evaluates `n = 5, 10, 15, 20` atoms per step by default and prints a
markdown table with:

- exact causal upper bound from `solve_exact_causal_mot`
- regularized expected payoff from `causal_sinkhorn_mot`
- absolute objective gap
- wall-clock time for each method
- convergence status for the regularized solver

The exact LP scales over the full joint tensor and is intended as a small-grid
benchmark. The Sinkhorn path is the practical approximation route for larger
causal chains.
