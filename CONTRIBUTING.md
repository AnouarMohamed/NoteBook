# Contributing

## Local Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .[dev]
```

On macOS or Linux:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## Useful Commands

```bash
pytest
python -m build
python scripts/run_uniform_abs_spread.py --output-dir artifacts
```

## Release Flow

1. Update `CHANGELOG.md`.
2. Bump the version in `pyproject.toml` and `src/mot_pricing/__init__.py`.
3. Commit the release changes.
4. Create an annotated tag such as `v0.2.0`.
5. Push the branch and tag.

Pushing a `v*` tag triggers the GitHub release workflow, which builds the wheel and source distribution and attaches them to a GitHub release.
