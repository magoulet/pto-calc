# Agent Notes

## Quick Start

1. Copy example config: `cp config.toml.example config.toml`
2. Ensure `amazon_vacation_schedule.ods` exists and set its absolute path in `config.toml` under `schedule_file`
3. Install deps: `make install` (or `pip install -r requirements.txt`)
4. Run: `python main.py`

## Architecture

- **Flat script repo** — no package structure. Entry point is `main.py`, run from repo root.
- **Core modules:**
  - `main.py` — reads ODS spreadsheet, drives `FlexiblePTO` / `StandardPTO`, generates plotly chart
  - `pto_classes.py` — PTO accrual, rollover, and cap logic
  - `config_loader.py` — loads and validates `config.toml`
- **Data source:** `amazon_vacation_schedule.ods` (OpenDocument Spreadsheet, gitignored). Path is read from `config['schedule_file']`; sheet name is hardcoded as `'baseline'` in `main.py`.

## Critical Gotchas

- **`config.toml` is required at import time.** `config_loader.py` loads it at module level (`config = load_config()`). Any import of `pto_classes` or `config_loader` will crash if `config.toml` is missing — this affects testing, REPL imports, etc.
- **Direct dependency gap:** `pto_classes.py` imports `dateutil.relativedelta`, but `python-dateutil` is not listed in `requirements.txt`. It installs transitively via `pandas`, but do not remove it without adding the explicit dependency.
- **`*.toml` and `*.ods` are gitignored.** Never commit `config.toml` or the vacation spreadsheet.
- **No tests exist.** There is no test runner config (`pytest`, `tox`, etc.).

## Environment

- Python version is managed externally (`.python-version` contains `global`).
- `Makefile` uses hardcoded `/usr/bin/python3` for venv creation.
- `.venv/` is already present in this workspace; use `source .venv/bin/activate` or call `.venv/bin/python` directly.

## Verification

- There is no lint, typecheck, or test command defined. The only verification step is running `python main.py` and checking the plotly output.
