# Changelog

All notable changes to KagazKit will be documented in this file.

This project follows a simple, release-based changelog.

## [0.1.6] - 2026-03-15

### Changed

- Cleaned the Windows PyInstaller build by removing a stale Pillow hidden import.
- Added regression coverage for image-to-PDF validation and a real image-to-PDF conversion test.
- Improved release and project metadata for packaging, security reporting, and contributor guidance.

## [0.1.5] - 2026-02-05

### Fixed

- Corrected image-to-PDF validation so image inputs are validated as images instead of PDFs.
