# Release Checklist

Use this checklist to publish a new KagazKit release and keep GitHub Releases,
the Windows binary, and PyPI aligned.

## 1) Update version

- Bump the version in `pyproject.toml`.
- Ensure `kagazkit.__version__` reflects the same version (if used).
- Add or update the matching entry in `CHANGELOG.md`.

## 2) Validate locally (optional but recommended)

```bash
python -m pip install -e .
python -m pytest
```

## 3) Build the distribution

```bash
python -m pip install --upgrade build twine
```

If you are building from a working tree that already contains the local PyInstaller
`build/` directory, run the packaging build from the parent directory so the
repository's `build/` folder does not shadow the `build` Python module:

```bash
cd ..
path\to\python -m build --outdir kagazkit/release-dist kagazkit
path\to\python -m twine check kagazkit/release-dist/*
```

## 4) Push the release tag

- Push the matching tag (for example, `v0.1.8`).
- The tag triggers the release workflow that:
  - publishes the Python package to PyPI
  - builds `KagazKit.exe`
  - runs the packaged GUI smoke test
  - generates `KagazKit.exe.sha256`
  - publishes a GitHub release with both Windows assets attached

## 5) Verify the published release

- Confirm the GitHub release includes:
  - `KagazKit.exe`
  - `KagazKit.exe.sha256`
- Confirm the release notes mention:
  - the Windows `.exe` is unsigned, so SmartScreen may warn
  - users should download only from the official release page
  - users can verify the SHA256 checksum in PowerShell
- Confirm the PyPI release is available for the same version tag.

## 6) Release acceptance checklist

- `pytest` passes on the release candidate.
- Package build succeeds.
- `twine check` passes for the built artifacts.
- Windows `.exe` build succeeds.
- The packaged GUI smoke test passes.
- The GitHub release has the correct tag and release notes.
- The GitHub release includes both `KagazKit.exe` and `KagazKit.exe.sha256`.
- The checksum file uses the format `<sha256>  KagazKit.exe`.
- The tag-triggered PyPI workflow succeeds.
