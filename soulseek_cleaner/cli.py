from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Sequence, Set

DEFAULT_PATTERNS: tuple[str, ...] = (
    "*.incomplete",
    "*.failed",
    "*.tmp",
    "*.bak",
    "*.part",
)


@dataclass
class CleaningConfig:
    """Configuration for a cleanup run."""

    root: Path
    dry_run: bool = False
    patterns: Sequence[str] = field(default_factory=lambda: list(DEFAULT_PATTERNS))


@dataclass
class CleaningReport:
    """Outcome of a cleanup run."""

    targets: List[Path]
    removed: List[Path]
    failed: List[Path]
    dry_run: bool

    @property
    def planned_count(self) -> int:
        return len(self.targets)

    @property
    def removed_count(self) -> int:
        return len(self.removed)

    @property
    def failed_count(self) -> int:
        return len(self.failed)


def _gather_targets(root: Path, patterns: Sequence[str]) -> List[Path]:
    seen: Set[Path] = set()
    for pattern in patterns:
        for path in root.rglob(pattern):
            if path.is_file():
                seen.add(path)
    return sorted(seen)


def cleanup_directory(config: CleaningConfig) -> CleaningReport:
    """Find and remove partial Soulseek downloads.

    Args:
        config: Settings describing where and how cleanup should occur.

    Returns:
        CleaningReport describing what happened.

    Raises:
        FileNotFoundError: if the configured root does not exist.
    """

    if not config.root.exists():
        raise FileNotFoundError(f"Directory does not exist: {config.root}")

    targets = _gather_targets(config.root, config.patterns)
    removed: List[Path] = []
    failed: List[Path] = []

    if not config.dry_run:
        for path in targets:
            try:
                path.unlink()
                removed.append(path)
            except OSError:
                failed.append(path)

    return CleaningReport(targets=targets, removed=removed, failed=failed, dry_run=config.dry_run)


def format_report(report: CleaningReport) -> str:
    verb = "Would remove" if report.dry_run else "Removed"
    lines = [
        f"{verb} {report.planned_count} file(s)",
        f"Removed: {report.removed_count}",
        f"Failed: {report.failed_count}",
    ]

    if report.targets:
        lines.append("")
        lines.append("Targets:")
        lines.extend(f"- {path}" for path in report.targets)

    return "\n".join(lines)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Remove incomplete Soulseek downloads")
    parser.add_argument("path", type=Path, help="Root directory to scan")
    parser.add_argument(
        "-e",
        "--extensions",
        nargs="*",
        default=list(DEFAULT_PATTERNS),
        help="Glob patterns to consider incomplete",
    )
    parser.add_argument("--dry-run", action="store_true", help="List files without deleting them")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    config = CleaningConfig(root=args.path, dry_run=args.dry_run, patterns=args.extensions)
    report = cleanup_directory(config)
    print(format_report(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
