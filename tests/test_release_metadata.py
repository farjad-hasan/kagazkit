import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _extract_version_from_pyproject() -> str:
    text = (PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    match = re.search(r'^version = "([^"]+)"$', text, re.MULTILINE)
    assert match, "pyproject.toml is missing a project version"
    return match.group(1)


def _extract_fallback_version() -> str:
    text = (PROJECT_ROOT / "src" / "kagazkit" / "__init__.py").read_text(encoding="utf-8")
    match = re.search(r'__version__ = "([^"]+)"', text)
    assert match, "__init__.py is missing a fallback __version__"
    return match.group(1)


def test_fallback_version_matches_project_version():
    assert _extract_fallback_version() == _extract_version_from_pyproject()
