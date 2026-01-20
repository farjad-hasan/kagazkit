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
python -m build
python -m twine check dist/*
```

## 4) Draft a GitHub release

- Create a new release draft in GitHub.
- Use the same version number as `pyproject.toml` (e.g., `v0.1.3`).
- Add a brief changelog for the release.

## 5) Publish to PyPI

```bash
python -m twine upload dist/*
```

## 6) Finalize the GitHub release

- Publish the release draft after PyPI upload succeeds.
