# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-06-08

### Added

- Async client (`LibreClientAsync`) and sync client (`LibreClientSync`)
- Pydantic response models for all API routes
- Route namespaces: Alerts, ARP, Bills, DeviceGroups, Devices, Index, Inventory, Locations, Logs, PollerGroups, Pollers, PortGroups, PortSecurity, Portgroups, Ports, Routing, Services, Switching, System
- Auto-generated `.pyi` type stubs for IDE support (`generate_stubs.py`)
- Configuration via environment variables using `pydantic-settings`
- Full unit test suite (137 tests)

[Unreleased]: https://github.com/jjeff07/py-librenms/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/jjeff07/py-librenms/releases/tag/v0.1.0

