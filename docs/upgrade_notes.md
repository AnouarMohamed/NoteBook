# Upgrade Notes

This repository began as a single exploratory notebook and was later reorganized into a small Python project.
{: .lead }

## Main Structural Changes

The project was upgraded by introducing:

- solver logic in `src/mot_pricing/`
- tests for exact, regularized, reporting, and gallery workflows
- packaging metadata and CLI entry points
- gallery generation and machine-readable summaries
- per-experiment markdown reports and structural diagnostics plots
- documentation, CI, release workflows, and publishing workflows

## Correctness And Numerical Fixes

Several fixes were especially important:

- unrestricted benchmark interpretation was corrected
- the regularized dual was compared against the appropriate regularized primal quantity
- the overflow-prone regularized update was replaced with a log-space implementation
- convex-order feasibility became an explicit diagnostic rather than an implicit assumption

## Effect Of The Upgrade

The package structure makes it easier to:

- rerun experiments reproducibly
- compare exact and regularized results systematically
- inspect diagnostics rather than relying on notebook state
- add new payoffs and gallery examples without restructuring earlier work
- publish the project in a stable form suitable for reuse

The legacy notebook remains part of the project history, but the library now serves as the source of truth.
