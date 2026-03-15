# Release Checklist

Use this checklist to publish a new KagazKit release and keep the GitHub
release page aligned with PyPI.

## 1) Update version

- Bump the version in `pyproject.toml`.
- Ensure `kagazkit.__version__` reflects the same version (if used).

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

## 4) Draft a GitHub release

- Create a new release draft in GitHub.
- Use the same version number as `pyproject.toml` (e.g., `v0.1.3`).
- Add a brief changelog for the release.

## 5) Publish to PyPI

```bash
python -m twine upload release-dist/*
```

## 6) Finalize the GitHub release

- Attach the latest `KagazKit.exe` if you are publishing the Windows binary.
- Publish the release draft after PyPI upload succeeds.
