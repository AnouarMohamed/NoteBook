# Upgrade Notes

This project started as a single exploratory notebook. I liked the mathematics, but the code was doing what notebooks often do: derivation, experiments, plotting, and numerical bookkeeping were all leaning on each other a little too hard.
{: .lead }

## What Changed

The rewrite pulled the project into a cleaner shape:

- solver logic moved into `src/mot_pricing/`
- tests were added for exact, regularized, and reporting workflows
- packaging metadata and CLI entry points were added
- gallery generation and machine-readable summaries were added
- docs, CI, release workflows, and publishing workflows were added

## What Was Corrected

A few fixes mattered more than the rest:

- unrestricted benchmark interpretation was corrected
- the regularized dual was compared against the proper regularized primal quantity
- the overflow-prone update in the regularized solver was replaced with a log-space implementation
- convex-order feasibility became an explicit check rather than an implicit hope

## Why The Upgrade Matters

The difference is not cosmetic. The package version makes it easier to:

- rerun experiments reproducibly
- compare exact and regularized results honestly
- inspect diagnostics instead of trusting notebook state
- add new payoffs and gallery examples without re-threading old cells
- publish the work in a form that survives beyond one machine and one afternoon

The notebook is still preserved as part of the story, but the library is now the source of truth. That is a better arrangement for both mathematics and memory.
