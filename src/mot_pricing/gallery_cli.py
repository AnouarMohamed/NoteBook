"""CLI for generating curated MOT galleries."""

from __future__ import annotations

import argparse
from pathlib import Path

from .gallery import builtin_gallery_specs, save_gallery_assets


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate the curated MOT example gallery."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("gallery_artifacts"),
        help="directory used for gallery artifacts",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    entries = save_gallery_assets(args.output_dir, builtin_gallery_specs())
    print(f"Generated gallery with {len(entries)} examples in {args.output_dir}")
    for entry in entries:
        print(
            f"  {entry.spec.slug}: upper={entry.experiment.exact_upper.value:.6f}, "
            f"lower={entry.experiment.exact_lower.value:.6f}, "
            f"payoff={entry.spec.payoff_name}"
        )


if __name__ == "__main__":
    main()
