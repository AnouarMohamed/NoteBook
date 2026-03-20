# Publishing

This page summarizes the package publishing workflow and the associated one-time configuration steps.
{: .lead }

## GitHub Releases

Tag pushes such as `v0.5.0` trigger the release workflow and attach the wheel and source distribution to a GitHub release.

## PyPI Workflow

This repository includes a manual GitHub Actions workflow for package publishing.

Supported targets:

- `TestPyPI`
- `PyPI`

The workflow uses trusted publishing via GitHub OIDC.

## Current Status

For this repository:

- GitHub Pages is enabled
- TestPyPI publishing is configured
- PyPI publishing is configured

## One-Time Setup For A New Repository

For a different repository, the one-time setup is:

1. Create the project on:
   - `https://test.pypi.org/`
   - `https://pypi.org/`
2. Add the repository as a trusted publisher in each project's settings.

Recommended mapping for this project:

- owner: `AnouarMohamed`
- repository: `NoteBook`
- workflow: `publish-package.yml`
- environment: `testpypi` or `pypi`

If the GitHub repository is renamed later, the trusted publisher entry on PyPI and TestPyPI must be updated to match the new repository name.

## Rename Troubleshooting

If publishing fails after a repository rename, check the following values on both TestPyPI and PyPI:

- owner: `AnouarMohamed`
- repository: `NoteBook`
- workflow: `publish-package.yml`
- environment: `testpypi` for TestPyPI and `pypi` for PyPI

Repository URLs in local git configuration, documentation, and package metadata should also be updated.

## Publishing Procedure

1. Run local verification:

   ```bash
   pytest
   python -m build
   python -m twine check dist/*
   ```

2. Open GitHub Actions.
3. Run the `Publish Package` workflow.
4. Choose `testpypi` or `pypi`.

## Docs Site

The documentation site is deployed from GitHub Actions using the `Docs` workflow and GitHub Pages.

If GitHub Pages is not already configured:

1. Open repository settings.
2. Go to Pages.
3. Set the source to `GitHub Actions`.
