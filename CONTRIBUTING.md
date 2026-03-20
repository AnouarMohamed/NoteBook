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
python -m twine check dist/*
mkdocs build --strict
python scripts/run_uniform_abs_spread.py --output-dir artifacts
```

## Release Flow

1. Update `CHANGELOG.md`.
2. Bump the version in `pyproject.toml` and `src/mot_pricing/__init__.py`.
3. Commit the release changes.
4. Create an annotated tag such as `v0.3.1`.
5. Push the branch and tag.

Pushing a `v*` tag triggers the GitHub release workflow, which builds the wheel and source distribution and attaches them to a GitHub release.

## Package Publishing

PyPI publishing is handled by the `Publish Package` GitHub Actions workflow.

Before using it:

1. Create the project on TestPyPI and PyPI.
2. Configure this repository as a trusted publisher for each index.
3. Run the workflow manually and choose the target index.

## Docs Publishing

The `Docs` workflow builds the MkDocs site and deploys it to GitHub Pages from the `main` branch.
