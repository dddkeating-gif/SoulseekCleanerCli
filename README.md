SoulseekCleanerCli – initial placeholder
# SoulseekCleanerCli

A tiny command-line helper for cleaning up incomplete Soulseek downloads. It scans a directory for common partial file patterns (for example `.incomplete`, `.failed`, or `.part`) and optionally deletes them.

## Installation

The project is packaged as a simple Python module. From the repository root you can install it in editable mode:

```bash
pip install -e .
```

## Usage

Run the cleaner by pointing it at your Soulseek downloads folder:

```bash
python -m soulseek_cleaner.cli /path/to/Downloads --dry-run
```

- Omit `--dry-run` to actually delete matching files.
- Override the glob patterns with `-e`/`--extensions` if you use different incomplete file suffixes.

The script prints a short report listing how many files were targeted, removed, or failed to remove.
