from pathlib import Path

import pytest

from soulseek_cleaner.cli import CleaningConfig, cleanup_directory


def create_partial_files(root: Path) -> list[Path]:
    filenames = [
        "track1.mp3.incomplete",
        "album/track2.mp3.failed",
        "album/disc2/track3.mp3.part",
        "notes.txt",
    ]
    created = []
    for name in filenames:
        file_path = root / name
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text("placeholder")
        created.append(file_path)
    return created


def test_cleanup_dry_run_keeps_files(tmp_path: Path):
    created = create_partial_files(tmp_path)

    config = CleaningConfig(root=tmp_path, dry_run=True)
    report = cleanup_directory(config)

    assert report.planned_count == 3
    assert report.removed_count == 0
    assert report.failed_count == 0
    for file_path in created:
        assert file_path.exists()


def test_cleanup_removes_incomplete_files(tmp_path: Path):
    created = create_partial_files(tmp_path)

    config = CleaningConfig(root=tmp_path, dry_run=False)
    report = cleanup_directory(config)

    assert report.planned_count == 3
    assert sorted(report.removed) == sorted(created[:-1])
    assert report.failed_count == 0
    assert not created[0].exists()
    assert created[-1].exists()


if __name__ == "__main__":
    pytest.main([__file__])
