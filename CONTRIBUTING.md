# Contributing to libreclient

Thanks for your interest in contributing! Here's how to get started.

## Quick Start

```bash
git clone https://github.com/jjeff07/libreclient.git
cd libreclient
uv sync
git config core.hooksPath .githooks
```

## Workflow

1. **Fork** the repository
2. **Branch** from `dev` (not `main`)
3. **Make changes** — write code, add tests
4. **Commit** using [Conventional Commits](https://www.conventionalcommits.org/) (the hook will validate)
5. **Push** and open a PR against `dev`

## What We're Looking For

- **New routes** — Support for future API endpoints as LibreNMS evolves
- **Bug fixes** — Found something broken? Fix it and add a regression test
- **Tests** — Increase coverage, especially functional tests
- **Documentation** — Improve docstrings, README, or examples

## Code Standards

- All code is linted and formatted by [Ruff](https://docs.astral.sh/ruff/) (CI will auto-fix minor issues)
- Maximum cognitive complexity of 15 per function (enforced by [complexipy](https://github.com/rohaquinlop/complexipy))
- Tests are required for new features and bug fixes
- Commit messages must follow Conventional Commits format (see [COMMIT_TYPES.md](COMMIT_TYPES.md) for quick reference)

## Adding a New Route

1. Create `src/libreclient/routes/myroute.py` with an async class
2. Create `src/libreclient/routes/myroute_sync.py` with `MyRouteSync = synchronizer.wrap(...)`
3. Create `src/libreclient/models/myroute.py` with Pydantic response models
4. Add exports to `models/__init__.py`
5. Wire up in `client.py` (both sync and async)
6. Run `uv run python scripts/generate_stubs.py` (regenerates stubs and `routes/__init__.py`)
7. Add unit tests in `tests/unit/routes/` and `tests/unit/models/`

## Running Tests

```bash
# Unit tests
uv run pytest tests/unit

# Functional tests (needs .env with LIBRENMS_URL and LIBRENMS_TOKEN)
uv run pytest tests/functional
```

## Questions?

Open an [issue](https://github.com/jjeff07/libreclient/issues) — happy to help you get started.


