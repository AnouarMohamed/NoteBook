# Upgrade Notes

This repository was upgraded from a single exploratory notebook into a small Python project.

Main changes:

- extracted solver logic into `src/mot_pricing/`
- added tests and packaging metadata
- corrected unrestricted benchmark interpretation
- fixed the regularized dual/primal comparison
- replaced the overflow-prone `h` update with a log-space implementation

The legacy notebook is preserved for reference, but the library code is now the source of truth.
