# Changelog

All notable changes to KagazKit will be documented in this file.

This project follows a simple, release-based changelog.

## [Unreleased]

### Changed

- Automated Windows release assets now include a `KagazKit.exe.sha256` checksum sidecar and SmartScreen guidance in release notes.
- Added official SmartScreen/checksum verification guidance to the README, troubleshooting docs, and release checklist.

## [0.1.7] - 2026-03-15

### Changed

- Expanded project governance, contributor guidance, support policy, and release documentation.
- Added stronger CI expectations for package validation and Windows release confidence.
- Increased real-file test coverage for core PDF and image workflows.
- Migrated from `PyPDF2` to `pypdf` and added a Windows executable GUI smoke check in CI.
- Documented the project's honest single-maintainer model and added clearer contributor entry points.
- Added a product-focused roadmap with concrete version targets and feature priorities.
- Added a dedicated troubleshooting guide and improved validation error messages for broken or unsupported files.

## [0.1.6] - 2026-03-15

### Changed

- Cleaned the Windows PyInstaller build by removing a stale Pillow hidden import.
- Added regression coverage for image-to-PDF validation and a real image-to-PDF conversion test.
- Improved release and project metadata for packaging, security reporting, and contributor guidance.

## [0.1.5] - 2026-02-05

### Fixed

- Corrected image-to-PDF validation so image inputs are validated as images instead of PDFs.
