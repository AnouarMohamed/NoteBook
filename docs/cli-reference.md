# CLI Reference

This page summarizes the command-line interfaces shipped with the project and the artifact files they generate.
{: .lead }

<div class="metric-grid" markdown>
<div class="metric-card" markdown>
<div class="metric-label">Commands</div>
<div class="metric-value">2</div>
<div class="metric-note">`mot-uniform` for single experiments and `mot-gallery` for the curated example set.</div>
</div>
<div class="metric-card" markdown>
<div class="metric-label">Single-Run Artifacts</div>
<div class="metric-value">6</div>
<div class="metric-note">Figures, JSON summary, and markdown report written per experiment.</div>
</div>
<div class="metric-card" markdown>
<div class="metric-label">Gallery Files</div>
<div class="metric-value">4</div>
<div class="metric-note">Overview plot, summary table, JSON summary, and generated casebook.</div>
</div>
</div>

## `mot-uniform`

`mot-uniform` runs a two-uniform experiment with a configurable payoff and writes the standard artifact set.

### Usage

```bash
mot-uniform [options]
```

### Main Options

| Option | Meaning | Default |
|---|---|---|
| `--n` | number of midpoint atoms in each marginal | `50` |
| `--x-interval A B` | support interval for `S1` | `1 3` |
| `--y-interval C D` | support interval for `S2` | `0 4` |
| `--payoff` | built-in payoff name | `abs_spread` |
| `--strike` | strike for spread option payoffs | `0.0` |
| `--eps` | regularization strengths | `1.0 0.3 0.1 0.03 0.01` |
| `--output-dir` | directory for generated artifacts | `artifacts` |

### Supported Payoffs

- `abs_spread`
- `squared_distance`
- `call_on_spread`
- `put_on_spread`
- `straddle_on_spread`

### Example

```bash
mot-uniform --n 60 --x-interval 1 3 --y-interval 0 4 --payoff call_on_spread --strike 0.25 --eps 0.3 0.1 --output-dir artifacts_call
```

### Standard Output Files

<div class="card-grid" markdown>
<div class="card" markdown>
- `exact_uniform_summary.png`
- `regularization_path.png`
- `stability_diagnostics.png`
</div>
<div class="card" markdown>
- `structural_diagnostics.png`
- `summary.json`
- `experiment_report.md`
</div>
</div>

## `mot-gallery`

`mot-gallery` runs the curated experiment set used by the documentation and writes a gallery directory.

### Usage

```bash
mot-gallery --output-dir gallery_artifacts
```

### Output Structure

The gallery output contains:

- one subdirectory per example
- `gallery_overview.png`
- `gallery_summary.json`
- `gallery_summary.md`
- `gallery_casebook.md`

Each example subdirectory contains the same standard files produced by `mot-uniform`.

## Script Entry Points

The repository also includes script wrappers:

- `python scripts/run_uniform_abs_spread.py`
- `python scripts/generate_example_gallery.py`

These call the same library entry points as the installed CLI commands.

## Typical Workflow

1. run `mot-uniform` for a single experiment
2. inspect `summary.json` and the diagnostics plots
3. run `mot-gallery` for cross-example comparison
4. review `gallery_summary.md` and `gallery_casebook.md`

This is usually sufficient for basic exploration and documentation generation.
