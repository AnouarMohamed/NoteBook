# Artifact Guide

This page describes the files produced by the standard experiment and gallery workflows.
{: .lead }

## Single-Experiment Artifacts

A call to `save_experiment_artifacts(...)` or `mot-uniform` writes the following files.

| File | Type | Purpose |
|---|---|---|
| `exact_uniform_summary.png` | figure | exact upper plan and payoff or benchmark summary |
| `regularization_path.png` | figure | expected payoff and regularized objective across `eps` |
| `stability_diagnostics.png` | figure | dual gap, martingale error, and iteration count |
| `structural_diagnostics.png` | figure | marginal profiles, conditional dispersion, and convex-order gap |
| `summary.json` | structured data | machine-readable numerical output for the run |
| `experiment_report.md` | markdown report | compact human-readable summary of the run |

## Gallery Artifacts

A call to `save_gallery_assets(...)` or `mot-gallery` writes gallery-level files in addition to per-example directories.

| File | Type | Purpose |
|---|---|---|
| `gallery_overview.png` | figure | cross-example comparison of intervals and widths |
| `gallery_summary.json` | structured data | machine-readable table of gallery rows |
| `gallery_summary.md` | markdown table | compact gallery summary for documentation |
| `gallery_casebook.md` | markdown report | long-form per-example notes and links |

## Per-Example Directory Structure

Typical example directories include:

- `docs/assets/gallery/uniform_abs_spread/`
- `docs/assets/gallery/wide_put/`
- `docs/assets/gallery/broad_straddle/`

Typical contents are:

- exact summary figure
- regularization path
- stability diagnostics
- structural diagnostics
- `summary.json`
- `experiment_report.md`

## Recommended Reading Order

For a single experiment, a useful review order is:

1. `experiment_report.md`
2. `exact_uniform_summary.png`
3. `structural_diagnostics.png`
4. `stability_diagnostics.png`
5. `summary.json`

For the full gallery, a useful order is:

1. `gallery_summary.md`
2. `gallery_overview.png`
3. `gallery_casebook.md`
4. selected per-example reports

## Relation To The Documentation Site

The documentation site directly reuses generated gallery files. This keeps the public pages aligned with the experiment outputs committed to the repository, rather than duplicating the same summaries by hand.
