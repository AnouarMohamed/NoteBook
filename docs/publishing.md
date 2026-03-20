# Publishing

## GitHub Releases

Tag pushes like `v0.4.0` trigger the release workflow and attach the built wheel and source distribution to a GitHub release.

## PyPI Workflow

This repository includes a manual GitHub Actions workflow for package publishing.

It supports:

- `TestPyPI` publishing
- `PyPI` publishing

The workflow uses trusted publishing via GitHub OIDC.

## Current Status

For this repository:

- GitHub Pages is enabled
- TestPyPI publishing is configured
- PyPI publishing is configured

## One-Time Setup On PyPI For A New Repository

For a different repository, the one-time setup is:

1. Create the project on:
   - `https://test.pypi.org/`
   - `https://pypi.org/`
2. Add the repository as a trusted publisher in each project's settings.

Recommended mapping for this project:

- owner: `AnouarMohamed`
- repository: `JavaFinalJee`
- workflow: `publish-package.yml`

## How To Publish

1. Build confidence first:

   ```bash
   pytest
   python -m build
   python -m twine check dist/*
   ```

2. Open GitHub Actions.
3. Run the `Publish Package` workflow.
4. Choose `testpypi` or `pypi`.

## Docs Site

The docs site is deployed from GitHub Actions using the `Docs` workflow and GitHub Pages.

If GitHub Pages is not already configured for a different repository:

1. Open repository settings.
2. Go to Pages.
3. Set the source to `GitHub Actions`.
