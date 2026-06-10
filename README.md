# libreclient

[![PyPI](https://img.shields.io/pypi/v/libreclient)](https://pypi.org/project/libreclient/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/downloads/)
[![CI](https://github.com/jjeff07/libreclient/actions/workflows/ci.yml/badge.svg)](https://github.com/jjeff07/libreclient/actions)
[![Documentation](https://img.shields.io/badge/docs-online-blue)](https://jjeff07.github.io/libreclient/)

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Niquests](https://img.shields.io/badge/niquests-HTTP%2F3-blueviolet)](https://github.com/jawah/niquests)
[![Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://docs.pydantic.dev/latest/)
[![complexipy](https://img.shields.io/badge/complexipy-max%2015-orange)](https://github.com/rohaquinlop/complexipy)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)](https://conventionalcommits.org)

Async and sync Python client for the [LibreNMS](https://www.librenms.org/) API.

- **Dual interface** — use `LibreClientAsync` for async/await or `LibreClientSync` for traditional blocking calls.
- **Typed responses** — all endpoints return Pydantic models with full IDE autocomplete.
- **Environment-driven config** — configure via `LIBRENMS_URL` and `LIBRENMS_TOKEN` env vars or pass values directly.

## Installation

```bash
pip install libreclient
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv add libreclient
```

## Quick Start

### Synchronous

```python
from libreclient import LibreClientSync

client = LibreClientSync(url="https://librenms.example.com", token="your-api-token")

# List all devices
response = client.devices.list_devices()
for device in response.devices:
    print(device["hostname"])

# Get a specific alert
alert = client.alerts.get_alert(42)
```

### Asynchronous

```python
import asyncio
from libreclient import LibreClientAsync


async def main():
    client = LibreClientAsync(url="https://librenms.example.com", token="your-api-token")

    response = await client.devices.list_devices()
    for device in response.devices:
        print(device["hostname"])

    await client.close()


asyncio.run(main())
```

### Context Manager

```python
# Sync
with LibreClientSync(url="https://librenms.example.com", token="your-api-token") as client:
    print(client.system.ping())

# Async
async with LibreClientAsync(url="https://librenms.example.com", token="your-api-token") as client:
    print(await client.system.ping())
```

## Configuration

Configuration is handled by [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/). You can
pass values directly or set environment variables:

| Env Variable           | Description                        | Default      |
|------------------------|------------------------------------|--------------|
| `LIBRENMS_URL`         | Base URL of your LibreNMS instance | *(required)* |
| `LIBRENMS_TOKEN`       | API token (`X-Auth-Token`)         | *(required)* |
| `LIBRENMS_VERIFY_SSL`  | Verify TLS certificates            | `true`       |
| `LIBRENMS_API_VERSION` | API version path segment           | `v0`         |

A `.env` file in your working directory is also supported. Copy the included sample to get started:

```bash
cp sample.env .env
# Edit .env with your LibreNMS URL and API token
```

## Available Route Namespaces

All route namespaces are accessible as properties on the client:

| Property               | Description                                |
|------------------------|--------------------------------------------|
| `client.alerts`        | Alert management and alert rules/templates |
| `client.arp`           | ARP table lookups                          |
| `client.bills`         | Billing data and graphs                    |
| `client.device_groups` | Device group management                    |
| `client.devices`       | Device CRUD, discovery, components, graphs |
| `client.index`         | List available API endpoints               |
| `client.inventory`     | Hardware inventory                         |
| `client.locations`     | Location management                        |
| `client.logs`          | Event, syslog, alert, and auth logs        |
| `client.poller_groups` | Poller group info                          |
| `client.pollers`       | Poller status                              |
| `client.port_groups`   | Port group management                      |
| `client.port_security` | Port security (802.1X/MAB)                 |
| `client.ports`         | Port info, search, and descriptions        |
| `client.routing`       | BGP, OSPF, VRF, MPLS, IPsec                |
| `client.services`      | Service monitoring                         |
| `client.switching`     | VLANs, links, FDB, NAC                     |
| `client.system`        | Ping and system info                       |

---

## Contributing

Contributions are welcome! We're actively looking for contributors to help with:

- 🐛 Bug fixes and edge case handling
- ✨ Support for new routes as LibreNMS adds API endpoints
- 📖 Documentation improvements
- 🧪 Test coverage expansion
- 🔧 Tooling and CI improvements

**Getting started:**

1. Fork the repo and create a branch from `dev`
2. Follow the [Development](#development) setup below
3. Make your changes with tests
4. Open a PR against `dev` — CI will lint, test, and auto-fix formatting

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines, or just open an issue to discuss your idea first.

---

## Development

This section covers everything you need to set up a local development environment and contribute code to libreclient.

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (package manager)

### Setup

```bash
git clone https://github.com/jjeff07/libreclient.git
cd libreclient
uv sync
```

#### Git Hooks

This project uses custom git hooks in the `.githooks/` directory.

**Setup (once per clone):**

```bash
git config core.hooksPath .githooks
```

| Hook         | Purpose                                                                                                                                            |
|--------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| `pre-commit` | Runs `ruff check --fix` and `ruff format` on staged `.py` files, re-stages fixes, then runs `complexipy` to enforce max cognitive complexity (15). |
| `commit-msg` | Validates commit messages against Conventional Commits format via commitizen.                                                                      |

### Running Tests

```bash
# Unit tests
uv run pytest tests/unit

# Functional tests (requires .env with LIBRENMS_URL and LIBRENMS_TOKEN)
uv run pytest tests/functional
```

### Linting & Formatting

This project uses [Ruff](https://docs.astral.sh/ruff/) for both linting and formatting:

```bash
# Check for lint issues
uv run ruff check

# Auto-fix lint issues
uv run ruff check --fix

# Format code
uv run ruff format

# Check formatting without changing files
uv run ruff format --check
```

### Complexity Checks

[complexipy](https://github.com/rohaquinlop/complexipy) is used to enforce a maximum cognitive complexity of 15 per
function:

```bash
uv run complexipy .
```

Results are output to `complexipy-results.json`. Any function exceeding the threshold will cause the check to fail.

### Architecture

The project uses a single-implementation pattern: each route is written **once** as an async class.
The [synchronicity](https://github.com/modal-com/synchronicity) library then wraps each async class to produce a
synchronous counterpart at runtime.

```
src/libreclient/routes/
├── alerts.py           ← async implementation (the only code you write)
└── alerts_sync.py      ← sync wrapper (imports Alerts, wraps with synchronizer)
```

This means:

- You only maintain one implementation per route.
- Both `LibreClientAsync` and `LibreClientSync` share the same logic.
- No code duplication between sync and async interfaces.

### Type Stubs

Because `synchronicity` generates wrapper classes dynamically, IDEs can't infer their method signatures. To restore full
autocomplete and type checking, `.pyi` stub files are auto-generated.

**Regenerate stubs locally:**

```bash
uv run python scripts/generate_stubs.py
```

Stubs are generated automatically during the GitHub Actions release workflow, so you don't need to commit them — they're
in `.gitignore`.

### Adding a New Route

1. Create `src/libreclient/routes/myroute.py` with an async class.
2. Create `src/libreclient/routes/myroute_sync.py` with `MyRouteSync = synchronizer.wrap(...)`.
3. Create `src/libreclient/models/myroute.py` with Pydantic response models.
4. Add exports to `src/libreclient/models/__init__.py`.
5. Wire up the route in `src/libreclient/client.py` (both sync and async clients).
6. Run `uv run python scripts/generate_stubs.py` to regenerate stubs and `__init__` files.
7. Add tests in `tests/unit/routes/test_myroute.py` and `tests/unit/models/test_myroute.py`.

### Commit Convention

This project enforces [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) via
[commitizen](https://commitizen-tools.github.io/commitizen/). A git hook validates every commit message automatically.

**Format:**

```
type(scope)?: description

[optional body]
[optional footer]
```

**Allowed types:** `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`, `bump`

> See [COMMIT_TYPES.md](COMMIT_TYPES.md) for full definitions and scope conventions.

**Examples:**

```
feat(routing): add OSPFv3 port listing
fix: handle empty response from list_devices
docs: add upstream tracking section to README
test: add functional tests for switching routes
```

### Upstream API Tracking

This project tracks which LibreNMS release tag the route implementations are based on. The pinned version is stored in
`upstream_tracking.toml`.

```bash
# Check if upstream has a newer release
python scripts/check_upstream.py

# See which API doc files changed
python scripts/check_upstream.py --diff

# See full unified diffs of changed docs
python scripts/check_upstream.py --full

# Compare against a specific tag instead of latest
python scripts/check_upstream.py --diff --tag 26.6.0

# Bump the pinned tag after reviewing changes
python scripts/check_upstream.py --bump
```

### Project Structure

```
libreclient/
├── src/libreclient/
│   ├── __init__.py            # Public API exports
│   ├── client.py              # LibreClientSync & LibreClientAsync
│   ├── config.py              # Pydantic-settings configuration
│   ├── _base_client.py        # Shared HTTP transport logic
│   ├── models/                # Pydantic response models
│   └── routes/                # Route namespaces (async + sync wrappers)
│       ├── _types.py          # ClientProtocol & utilities
│       ├── _synchronicity.py  # Shared Synchronizer instance
│       ├── alerts.py          # Async route implementation
│       ├── alerts_sync.py     # Sync wrapper
│       └── ...
├── tests/
│   ├── unit/
│   │   ├── models/            # Model validation tests
│   │   └── routes/            # Route logic tests (MockClient)
│   └── functional/            # Live API tests (requires .env)
├── scripts/
│   ├── check_upstream.py      # Detect upstream API doc changes
│   └── generate_stubs.py      # .pyi stub generator
├── .githooks/
│   ├── pre-commit             # Ruff lint & format
│   └── commit-msg             # Conventional commit validation
├── upstream_tracking.toml     # Pinned LibreNMS release tag
├── pyproject.toml
├── CHANGELOG.md
└── LICENSE
```

## License

[MIT](LICENSE)

