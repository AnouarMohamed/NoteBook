# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog and this project follows Semantic Versioning.

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
