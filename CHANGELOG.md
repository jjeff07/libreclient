# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2026-06-11

### Changed

- ci: Fix autorelease to find commits in squashed message. (#31)
- Correct Adding Device function (#30)
- docs: Fix docs ci. (#27)
- docs: Fix docs ci. (#26)
- docs: Fix docs ci. (#25)
- docs: Fix docs ci. (#24)

## [0.1.3] - 2026-06-10

### Changed

- Refactor stubs and Docs (#22)
- ci: Fix CI issues. (#18)
- ci: Fix CI issues. (#16)

## [0.1.2] - 2026-06-09

### Changed

- Test new CI Workflow (#14)

## [0.1.1] - 2026-06-09

### Changed

- ci: Fix CI/CD.
- ci: Fix CI/CD.
- fix: Response statuses were not raised. (#2) (#3)
- fix: Response statuses were not raised. (#2)
- style: Fix format.
- fix: Response statuses were not raised.

## [0.1.0] - 2026-06-09

### Added

- Initial release on [PyPI](https://pypi.org/project/libreclient/)
- Async client (`LibreClientAsync`) and sync client (`LibreClientSync`)
- Pydantic response models for all API routes
- Route namespaces: Alerts, ARP, Bills, DeviceGroups, Devices, Index, Inventory, Locations, Logs, PollerGroups, Pollers, PortGroups, PortSecurity, Portgroups, Ports, Routing, Services, Switching, System
- Auto-generated `.pyi` type stubs for IDE support (`generate_stubs.py`)
- Configuration via environment variables using `pydantic-settings`
- Conventional Commits enforcement via commitizen
- Upstream API tracking (`check_upstream.py`) pinned to LibreNMS 26.5.1
- Full unit test suite (140 tests) and functional test suite (41 tests)

[Unreleased]: https://github.com/jjeff07/libreclient/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/jjeff07/libreclient/compare/v0.1.3...v0.2.0
[0.1.3]: https://github.com/jjeff07/libreclient/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/jjeff07/libreclient/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/jjeff07/libreclient/compare/0.1.0...v0.1.1
[0.1.0]: https://github.com/jjeff07/libreclient/releases/tag/v0.1.0

