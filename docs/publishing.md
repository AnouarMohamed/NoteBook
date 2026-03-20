# Publishing

## GitHub Releases

Tag pushes like `v0.2.0` trigger the release workflow and attach the built wheel and source distribution to a GitHub release.

## PyPI Workflow

This repository now includes a manual GitHub Actions workflow for package publishing.

It supports:

- `TestPyPI` publishing
- `PyPI` publishing

The workflow is designed for trusted publishing via GitHub OIDC.

## One-Time Setup On PyPI

Before publishing can succeed, create the project on:

- `https://test.pypi.org/`
- `https://pypi.org/`

Then add this repository as a trusted publisher in each project’s settings.

Recommended mapping:

- owner: `AnouarMohamed`
- repository: `JavaFinalJee`
- workflow: `publish-package.yml`

## How To Publish

1. Build confidence first:

   ```bash
   pytest
   python -m build
   ```

2. Open GitHub Actions.
3. Run the `Publish Package` workflow.
4. Choose `testpypi` or `pypi`.

## Docs Site

The docs site is deployed from GitHub Actions using the `Docs` workflow and GitHub Pages.

If GitHub Pages is not already configured:

1. Open repository settings.
2. Go to Pages.
3. Set the source to `GitHub Actions`.
