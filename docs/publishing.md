# Publishing

This page is intentionally plainspoken. Package publishing is not where I look for poetry; it is where I look for exact strings that either match or fail.
{: .lead }

## GitHub Releases

Tag pushes like `v0.4.0` trigger the release workflow and attach the wheel and source distribution to a GitHub release.

## PyPI Workflow

This repository includes a manual GitHub Actions workflow for package publishing.

It supports:

- `TestPyPI` publishing
- `PyPI` publishing

The workflow uses trusted publishing via GitHub OIDC, which is the setup I prefer because it avoids long-lived upload tokens quietly aging in a drawer.

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
- repository: `NoteBook`
- workflow: `publish-package.yml`
- environment: `testpypi` or `pypi`

If the GitHub repository is renamed later, the trusted publisher entry on PyPI and TestPyPI must be updated to match. OIDC is very exact about identity, which is good for security and occasionally irritating for people who rename repositories on a Tuesday.

## Rename Troubleshooting

If publishing starts failing right after a repository rename, check these exact values on both TestPyPI and PyPI:

- owner: `AnouarMohamed`
- repository: `NoteBook`
- workflow: `publish-package.yml`
- environment: `testpypi` for TestPyPI and `pypi` for PyPI

Also update the local Git remote and any repository URLs in docs or package metadata so badges, docs links, and Pages URLs point at the renamed repository.

## How I Publish

1. Build confidence first:

   ```bash
   pytest
   python -m build
   python -m twine check dist/*
   ```

2. Open GitHub Actions.
3. Run the `Publish Package` workflow.
4. Choose `testpypi` or `pypi`.

That is the whole routine. If those verification commands fail locally, I do not bother asking the workflow to be brave on my behalf.

## Docs Site

The docs site is deployed from GitHub Actions using the `Docs` workflow and GitHub Pages.

If GitHub Pages is not already configured:

1. Open repository settings.
2. Go to Pages.
3. Set the source to `GitHub Actions`.
