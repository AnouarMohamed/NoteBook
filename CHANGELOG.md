# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog and this project follows Semantic Versioning.

## [0.5.0] - 2026-03-20

### Added
- structural diagnostics plots for each experiment, combining marginal profiles, conditional dispersion, and convex-order call gaps
- per-experiment markdown reports generated alongside JSON summaries and figures
- two new gallery examples: wide put on spread and broad spread straddle
- a generated gallery casebook for long-form per-example notes
- documentation pages for the discrete formulation and CLI reference

### Changed
- expanded the README into a fuller academic project overview
- expanded the documentation with additional research-facing content and generated gallery material
- bumped package metadata from `0.4.1` to `0.5.0`

## [0.4.1] - 2026-03-20

### Changed
- bumped package metadata from `0.4.0` to `0.4.1` so TestPyPI and PyPI receive a new immutable release
- made the publish workflow idempotent on reruns by enabling `skip-existing` for package uploads

## [0.4.0] - 2026-03-20

### Added
- reusable reporting helpers for experiment figures and diagnostics
- a curated gallery system with built-in example specs and summary generation
- a new `mot-gallery` CLI entry point and gallery generation script
- stability diagnostics plots for regularized experiments
- richer examples documentation with a cross-example gallery overview
- tests for gallery and artifact generation

### Changed
- bumped package metadata from `0.3.1` to `0.4.0`
- refactored the single-experiment CLI to reuse the shared reporting layer
- expanded the README and docs to highlight the exploratory workflow

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
