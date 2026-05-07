"""Benchmark exact causal LP against causal Sinkhorn approximations."""

from __future__ import annotations

import argparse
import time

import numpy as np

from mot_pricing import (
    CausalMarginalChain,
    causal_sinkhorn_mot,
    solve_exact_causal_mot,
)


def build_parser() -> argparse.ArgumentParser:
    """
    Create an ArgumentParser preconfigured for the causal MOT vs causal Sinkhorn benchmark.
    
    Configures the following command-line options:
    - --n-values: list of atom counts per time step to benchmark (default: [5, 10, 15, 20]).
    - --eps: regularization strength for the causal Sinkhorn solver (default: 0.1).
    - --sinkhorn-iterations: maximum Sinkhorn iterations per adjacent step (default: 600).
    - --sinkhorn-tolerance: convergence tolerance for the Sinkhorn solver (default: 1e-8).
    
    Returns:
        argparse.ArgumentParser: Parser with the above options configured.
    """
    parser = argparse.ArgumentParser(
        description="Benchmark exact causal MOT LP against causal Sinkhorn."
    )
    parser.add_argument(
        "--n-values",
        nargs="*",
        type=int,
        default=[5, 10, 15, 20],
        help="atom counts to benchmark for each time step",
    )
    parser.add_argument(
        "--eps",
        type=float,
        default=0.1,
        help="regularization strength for causal Sinkhorn",
    )
    parser.add_argument(
        "--sinkhorn-iterations",
        type=int,
        default=600,
        help="maximum causal Sinkhorn iterations per adjacent step",
    )
    parser.add_argument(
        "--sinkhorn-tolerance",
        type=float,
        default=1e-8,
        help="causal Sinkhorn convergence tolerance",
    )
    return parser


def additive_abs_spread_exact(s1, s2, s3):
    """
    Compute the sum of absolute differences across three consecutive states.
    
    Parameters:
        s1: value at time t (scalar or array-like).
        s2: value at time t+1 (scalar or array-like).
        s3: value at time t+2 (scalar or array-like).
    
    Returns:
        The value of |s2 - s1| + |s3 - s2| (elementwise if inputs are arrays), returned with the same shape as the inputs.
    """
    return np.abs(s2 - s1) + np.abs(s3 - s2)


def additive_abs_spread_pair(s_t, s_next):
    """
    Compute the absolute difference between two adjacent states.
    
    Parameters:
        s_t (array_like or float): Value(s) at time t.
        s_next (array_like or float): Value(s) at time t+1.
    
    Returns:
        abs_diff (array_like or float): Elementwise absolute difference |s_next - s_t|.
    """
    return np.abs(s_next - s_t)


def main() -> None:
    """
    Run the CLI benchmark that compares an exact causal MOT linear program to a causal Sinkhorn approximation over configured atom counts and print a Markdown-formatted results table.
    
    Reads CLI options from the module parser (e.g., `--n-values`, `--eps`, `--sinkhorn-iterations`, `--sinkhorn-tolerance`), for each `n` constructs a three-step CausalMarginalChain from uniform intervals, times and solves the exact and regularized problems, computes the absolute objective gap, and prints rows with the following columns: `n`, exact objective (upper), Sinkhorn expected payoff, objective gap, exact runtime (s), sinkhorn runtime (s), and convergence flag.
    """
    args = build_parser().parse_args()
    rows = []
    for n in args.n_values:
        chain = CausalMarginalChain.from_uniform_intervals(
            (
                (1.0, 3.0, n),
                (0.5, 3.5, n),
                (0.0, 4.0, n),
            )
        )

        exact_start = time.perf_counter()
        exact = solve_exact_causal_mot(
            chain,
            additive_abs_spread_exact,
            objective="max",
        )
        exact_seconds = time.perf_counter() - exact_start

        sinkhorn_start = time.perf_counter()
        regularized = causal_sinkhorn_mot(
            chain,
            additive_abs_spread_pair,
            args.eps,
            n_iter=args.sinkhorn_iterations,
            tol=args.sinkhorn_tolerance,
        )
        sinkhorn_seconds = time.perf_counter() - sinkhorn_start
        objective_gap = abs(exact.value - regularized.overall_expected_payoff)

        rows.append(
            (
                n,
                exact.value,
                regularized.overall_expected_payoff,
                objective_gap,
                exact_seconds,
                sinkhorn_seconds,
                regularized.converged,
            )
        )

    print("| n | exact upper | sinkhorn expected | objective gap | exact seconds | sinkhorn seconds | converged |")
    print("|---:|---:|---:|---:|---:|---:|:---:|")
    for row in rows:
        print(
            f"| {row[0]} | {row[1]:.8f} | {row[2]:.8f} | {row[3]:.3e} | "
            f"{row[4]:.3f} | {row[5]:.3f} | {row[6]} |"
        )


if __name__ == "__main__":
    main()
