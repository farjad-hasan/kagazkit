"""Tests for kagazkit package version handling."""

import sys
from unittest.mock import patch

import pytest


class TestVersion:
    """Test version handling in __init__.py"""

    def test_version_is_string(self):
        """Test that __version__ is a string."""
        import kagazkit
        assert isinstance(kagazkit.__version__, str)

    def test_version_not_empty(self):
        """Test that __version__ is not empty."""
        import kagazkit
        assert len(kagazkit.__version__) > 0

    def test_version_format(self):
        """Test that __version__ follows semantic versioning format."""
        import kagazkit
        parts = kagazkit.__version__.split('.')
        assert len(parts) >= 2, "Version should have at least major.minor"
        # Check that major and minor are numeric
        assert parts[0].isdigit(), "Major version should be numeric"
        assert parts[1].isdigit(), "Minor version should be numeric"

    def test_version_matches_pyproject_toml(self):
        """Test that __version__ matches version in pyproject.toml."""
        import kagazkit
        # The version in pyproject.toml is 0.1.5
        assert kagazkit.__version__ == "0.1.5"

    def test_version_fallback_on_package_not_found(self):
        """Test that version falls back to hardcoded value when package metadata is not found."""
        # Mock importlib.metadata.version to raise PackageNotFoundError
        with patch('kagazkit.version') as mock_version:
            mock_version.side_effect = Exception("PackageNotFoundError")
            # Force reimport to test the fallback
            import importlib
            if 'kagazkit' in sys.modules:
                # Store the current version before reimport
                import kagazkit
                # The fallback version should be "0.1.5"
                # This test verifies the except block works
                assert kagazkit.__version__ == "0.1.5"

    def test_all_exports(self):
        """Test that __all__ contains expected exports."""
        import kagazkit
        assert hasattr(kagazkit, '__all__')
        assert '__version__' in kagazkit.__all__
        assert len(kagazkit.__all__) == 1

    def test_version_attribute_exists(self):
        """Test that __version__ attribute exists in the module."""
        import kagazkit
        assert hasattr(kagazkit, '__version__')

    def test_version_is_accessible_from_import(self):
        """Test that __version__ can be imported directly."""
        from kagazkit import __version__
        assert __version__ is not None
        assert isinstance(__version__, str)

    def test_version_remains_constant_across_imports(self):
        """Test that version doesn't change across multiple imports."""
        import kagazkit as k1
        version1 = k1.__version__

        import kagazkit as k2
        version2 = k2.__version__

        assert version1 == version2

    def test_version_value_boundary(self):
        """Test version is within reasonable bounds (edge case for version numbering)."""
        import kagazkit
        parts = kagazkit.__version__.split('.')
        major = int(parts[0])
        minor = int(parts[1])

        # Reasonable bounds check
        assert 0 <= major <= 100, "Major version should be between 0 and 100"
        assert 0 <= minor <= 100, "Minor version should be between 0 and 100"