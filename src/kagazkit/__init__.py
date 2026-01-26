"""Top-level package for KagazKit."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("kagazkit")
except PackageNotFoundError:
    __version__ = "0.1.4"

__all__ = ["__version__"]
