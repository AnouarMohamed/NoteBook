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
    return np.abs(s2 - s1) + np.abs(s3 - s2)


def additive_abs_spread_pair(s_t, s_next):
    return np.abs(s_next - s_t)


def main() -> None:
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
