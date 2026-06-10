# Commit Types Reference

This project uses [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/). Every commit message must
follow the format:

```
type(scope)?: description

[optional body]
[optional footer]
```

## Allowed Types

| Type       | Description                                                                 |
|------------|-----------------------------------------------------------------------------|
| `feat`     | A new feature or user-facing enhancement                                    |
| `fix`      | A bug fix                                                                   |
| `docs`     | Documentation-only changes (README, docstrings, comments)                   |
| `style`    | Code style changes that do not affect logic (formatting, whitespace)        |
| `refactor` | Code restructuring that neither fixes a bug nor adds a feature              |
| `perf`     | Performance improvements                                                    |
| `test`     | Adding or updating tests (no production code changes)                       |
| `build`    | Changes to the build system or dependencies (pyproject.toml, uv.lock, etc.) |
| `ci`       | Changes to CI/CD configuration (GitHub Actions, workflows)                  |
| `chore`    | Routine maintenance tasks that don't modify src or test files               |
| `revert`   | Reverts a previous commit                                                   |
| `bump`     | Version bump                                                                |

## Examples

```
feat(routing): add OSPFv3 port listing
fix: handle empty response from list_devices
docs: add upstream tracking section to README
test: add functional tests for switching routes
refactor(models): simplify base response inheritance
perf(devices): reduce redundant API calls in list_devices
build: bump pydantic to 2.14.0
ci: add Python 3.13 to test matrix
chore: remove unused test fixtures
style: fix trailing whitespace in routes module
revert: revert "feat(ports): add port graph endpoint"
bump: 0.1.3
```

## Scope (Optional)

The scope provides additional context about what area of the codebase is affected. Common scopes in this project:

| Scope           | Usage                         |
|-----------------|-------------------------------|
| `alerts`        | Alert routes or models        |
| `arp`           | ARP routes or models          |
| `bills`         | Billing routes or models      |
| `devices`       | Device routes or models       |
| `device_groups` | Device group routes or models |
| `inventory`     | Inventory routes or models    |
| `locations`     | Location routes or models     |
| `logs`          | Log routes or models          |
| `ports`         | Port routes or models         |
| `port_groups`   | Port group routes or models   |
| `routing`       | Routing routes or models      |
| `services`      | Service routes or models      |
| `switching`     | Switching routes or models    |
| `system`        | System routes or models       |
| `models`        | Cross-cutting model changes   |
| `routes`        | Cross-cutting route changes   |
| `config`        | Configuration changes         |
| `client`        | Client class changes          |

## Validation

Commit messages are validated automatically by a `commit-msg` git hook using
[commitizen](https://commitizen-tools.github.io/commitizen/). If your message doesn't match the format, the commit will
be rejected with an error explaining what went wrong.

**Setup the hook (once per clone):**

```bash
git config core.hooksPath .githooks
```

