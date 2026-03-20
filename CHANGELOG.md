# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog and this project follows Semantic Versioning.

## [0.3.1] - 2026-03-20

### Added
- PyPI and Python-version badges in the README
- direct PyPI installation guidance in the README and docs
- Twine validation for built distributions in CI and release workflows
- additional public package and release links in project metadata

### Changed
- bumped package metadata from `0.3.0` to `0.3.1`
- updated publishing docs to reflect that trusted publishing is already active for this repository
- cleaned the docs landing page and release guidance

## [0.3.0] - 2026-03-20

### Added
- MkDocs-based documentation site with examples, API notes, and publishing guidance
- GitHub Pages deployment workflow for docs
- manual trusted-publishing workflow for TestPyPI and PyPI
- committed example gallery assets for the docs site
- docs build verification in CI

### Changed
- bumped package metadata from `0.2.0` to `0.3.0`
- expanded README and contributor guidance for public package and docs workflows

## [0.2.0] - 2026-03-20

### Added
- generic discrete marginals with convex-order checks
- built-in payoff library for abs spread, squared distance, and spread options
- configurable CLI support for custom intervals, payoff selection, and strikes
- tagged release workflow for GitHub builds and release assets
- contributor and release guidance

### Changed
- bumped package metadata from `0.1.0` to `0.2.0`
- generalized the experiment runner beyond the single hard-coded notebook example
- expanded JSON summaries with payoff and convex-order metadata
- extended CI to build the distribution package in addition to running tests

### Fixed
- removed a duplicate root-level notebook artifact and kept the cleaned notebook layout

## [0.1.0] - 2026-03-20

### Added
- extracted the original notebook into a package
- added exact LP and regularized MOT solvers
- added tests, docs, CI, and a package-backed report notebook
