# Changelog

## 3.0.0-rc.2

Compatible with and only with Nautobot version 2.0.0-rc.2.

## 3.0.0-beta.1

Compatible with and only with Nautobot version 2.0.0-beta.2.

### Added

- Possibility to use `invoke logs` to view container logs (#52)

### Changed

- Added compatibility with Nautobot 2.0, removed Nautobot 1.0 compatibility (#52)
- Updated Ubuntu version in CI to 22.04

### Removed

- Metrics for (deprecated) RQ workers (#52)
- Django management command for RQ worker metrics (#52)

## 2.0.0

### Changed

- Migrated from Travis-CI to GitHub Actions (#27)
- Updated `mkdocs` version in `docs/requirements.txt` from 1.1.2 to 1.3.0 (#30)

### Removed

- Removed `nautobot_job_task_stats` metric (#29)

## 1.1.0

### Added

- Added support for GitRepository sync metrics (#24).

## 1.0.1

### Changed

- Updated to support configuration changes in Nautobot 1.0.0
