# CLI Reference

This page summarizes the command-line interfaces shipped with the project and the artifact files they generate.
{: .lead }

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

- `exact_uniform_summary.png`
- `regularization_path.png`
- `stability_diagnostics.png`
- `structural_diagnostics.png`
- `summary.json`
- `experiment_report.md`

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

For causal gallery entries, subdirectories contain causal artifact names such as `causal_summary.json` and `causal_experiment_report.md`. Continuous convergence entries contain `continuous_limit.png` and `continuous_summary.json`.

## `mot-causal`

`mot-causal` runs a causal multi-period experiment on a chain of uniform marginals.

### Usage

```bash
mot-causal [options]
```

### Main Options

| Option | Meaning | Default |
|---|---|---|
| `--n` | atoms per time step | `30` |
| `--intervals A,B ...` | one support interval per time step, formatted as comma-separated bounds | `1,3 0.5,3.5 0,4` |
| `--payoff` | built-in adjacent-step payoff name | `abs_spread` |
| `--strike` | strike for spread option payoffs | `0.0` |
| `--eps` | regularization strengths | `0.3 0.1 0.03` |
| `--output-dir` | directory for generated causal artifacts | `causal_artifacts` |

### Example

```bash
mot-causal --n 30 --intervals 1,3 0.5,3.5 0,4 --payoff abs_spread --eps 0.3 0.1 --output-dir causal_out
```

### Output Files

- `causal_transport_chain.png`
- `causal_bound_convergence.png`
- `marginal_evolution.png`
- `causal_vs_unconstrained.png`
- `causal_summary.json`
- `causal_experiment_report.md`

## Script Entry Points

The repository also includes script wrappers:

- `python scripts/run_uniform_abs_spread.py`
- `python scripts/generate_example_gallery.py`
- `python scripts/benchmark_causal.py`

These call the same library entry points as the installed CLI commands.

## Typical Workflow

1. run `mot-uniform` for a single experiment
2. inspect `summary.json` and the diagnostics plots
3. run `mot-causal` for a multi-period chain when adapted constraints matter
4. run `mot-gallery` for cross-example comparison
5. review `gallery_summary.md` and `gallery_casebook.md`

This is usually sufficient for basic exploration and documentation generation.
