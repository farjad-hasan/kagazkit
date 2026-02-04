"""Tests for pyproject.toml configuration."""

import tomli
from pathlib import Path

import pytest


class TestPyprojectConfiguration:
    """Test pyproject.toml configuration is valid and complete."""

    @pytest.fixture
    def pyproject_data(self):
        """Load and parse pyproject.toml."""
        pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
        with open(pyproject_path, "rb") as f:
            return tomli.load(f)

    def test_pyproject_file_exists(self):
        """Test that pyproject.toml exists."""
        pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
        assert pyproject_path.exists()
        assert pyproject_path.is_file()

    def test_build_system_configured(self, pyproject_data):
        """Test that build-system is properly configured."""
        assert "build-system" in pyproject_data
        build_system = pyproject_data["build-system"]
        assert "requires" in build_system
        assert "build-backend" in build_system
        assert build_system["build-backend"] == "setuptools.build_meta"

    def test_project_metadata(self, pyproject_data):
        """Test that project metadata is complete."""
        assert "project" in pyproject_data
        project = pyproject_data["project"]

        # Required fields
        assert "name" in project
        assert project["name"] == "kagazkit"
        assert "version" in project
        assert "description" in project
        assert len(project["description"]) > 0

    def test_project_version_format(self, pyproject_data):
        """Test that version follows semantic versioning."""
        project = pyproject_data["project"]
        version = project["version"]

        parts = version.split(".")
        assert len(parts) >= 2, "Version should have at least major.minor"
        assert parts[0].isdigit(), "Major version should be numeric"
        assert parts[1].isdigit(), "Minor version should be numeric"

    def test_project_version_matches_init(self, pyproject_data):
        """Test that version in pyproject.toml matches __init__.py."""
        import kagazkit
        project = pyproject_data["project"]
        assert project["version"] == kagazkit.__version__

    def test_project_authors(self, pyproject_data):
        """Test that authors are specified."""
        project = pyproject_data["project"]
        assert "authors" in project
        assert len(project["authors"]) > 0
        # Each author should have at least a name
        for author in project["authors"]:
            assert "name" in author

    def test_project_license(self, pyproject_data):
        """Test that license is specified."""
        project = pyproject_data["project"]
        assert "license" in project
        assert "file" in project["license"]

    def test_project_readme(self, pyproject_data):
        """Test that readme is specified."""
        project = pyproject_data["project"]
        assert "readme" in project
        assert project["readme"] == "README.md"

        # Verify README.md exists
        readme_path = Path(__file__).parent.parent / "README.md"
        assert readme_path.exists()

    def test_project_classifiers(self, pyproject_data):
        """Test that classifiers are specified."""
        project = pyproject_data["project"]
        assert "classifiers" in project
        classifiers = project["classifiers"]
        assert len(classifiers) > 0

        # Check for important classifiers
        assert any("Python :: 3" in c for c in classifiers)
        assert any("License" in c for c in classifiers)

    def test_python_version_requirement(self, pyproject_data):
        """Test that Python version requirement is specified."""
        project = pyproject_data["project"]
        assert "requires-python" in project
        requires_python = project["requires-python"]
        assert requires_python.startswith(">=")

    def test_project_dependencies(self, pyproject_data):
        """Test that dependencies are specified."""
        project = pyproject_data["project"]
        assert "dependencies" in project
        dependencies = project["dependencies"]
        assert len(dependencies) > 0

        # Check for required dependencies
        dep_names = [dep.split(">=")[0].split("==")[0] for dep in dependencies]
        assert "customtkinter" in dep_names
        assert "Pillow" in dep_names
        assert "PyPDF2" in dep_names

    def test_project_urls(self, pyproject_data):
        """Test that project URLs are specified."""
        project = pyproject_data["project"]
        assert "urls" in project
        urls = project["urls"]

        assert "Homepage" in urls
        assert "Bug Tracker" in urls
        assert urls["Homepage"].startswith("http")
        assert urls["Bug Tracker"].startswith("http")

    def test_project_scripts(self, pyproject_data):
        """Test that project scripts are configured."""
        project = pyproject_data["project"]
        assert "scripts" in project
        scripts = project["scripts"]

        assert "kagazkit" in scripts
        assert scripts["kagazkit"] == "kagazkit.main:main"

    def test_setuptools_configuration(self, pyproject_data):
        """Test that setuptools is properly configured."""
        assert "tool" in pyproject_data
        tool = pyproject_data["tool"]
        assert "setuptools" in tool
        setuptools = tool["setuptools"]

        assert "packages" in setuptools
        packages = setuptools["packages"]
        assert "find" in packages
        assert packages["find"]["where"] == ["src"]

    def test_pytest_configuration(self, pyproject_data):
        """Test that pytest is properly configured."""
        tool = pyproject_data["tool"]
        assert "pytest" in tool
        pytest_config = tool["pytest"]

        assert "ini_options" in pytest_config
        ini_options = pytest_config["ini_options"]
        assert "minversion" in ini_options
        assert "testpaths" in ini_options
        assert "tests" in ini_options["testpaths"]

    def test_ruff_configuration(self, pyproject_data):
        """Test that ruff linter is properly configured."""
        tool = pyproject_data["tool"]
        assert "ruff" in tool
        ruff = tool["ruff"]

        assert "select" in ruff
        assert "ignore" in ruff
        assert "line-length" in ruff
        assert "target-version" in ruff

    def test_ruff_format_configuration(self, pyproject_data):
        """Test that ruff formatter is properly configured."""
        tool = pyproject_data["tool"]
        ruff = tool["ruff"]

        assert "format" in ruff
        ruff_format = ruff["format"]
        assert "quote-style" in ruff_format
        assert "indent-style" in ruff_format

    def test_dependencies_have_version_constraints(self, pyproject_data):
        """Test that dependencies have proper version constraints."""
        project = pyproject_data["project"]
        dependencies = project["dependencies"]

        for dep in dependencies:
            # Each dependency should have either >= or == version constraint
            assert ">=" in dep or "==" in dep, f"Dependency {dep} should have version constraint"

    def test_no_duplicate_dependencies(self, pyproject_data):
        """Test that there are no duplicate dependencies."""
        project = pyproject_data["project"]
        dependencies = project["dependencies"]

        dep_names = [dep.split(">=")[0].split("==")[0] for dep in dependencies]
        assert len(dep_names) == len(set(dep_names)), "Found duplicate dependencies"

    def test_build_requirements_exist(self, pyproject_data):
        """Test that build requirements are specified."""
        build_system = pyproject_data["build-system"]
        requires = build_system["requires"]

        assert len(requires) > 0
        assert any("setuptools" in req for req in requires)

    def test_line_length_reasonable(self, pyproject_data):
        """Test that configured line length is reasonable."""
        tool = pyproject_data["tool"]
        ruff = tool["ruff"]
        line_length = ruff["line-length"]

        assert 79 <= line_length <= 120, "Line length should be between 79 and 120"

    def test_target_python_version_matches(self, pyproject_data):
        """Test that ruff target version matches requires-python."""
        project = pyproject_data["project"]
        requires_python = project["requires-python"]

        tool = pyproject_data["tool"]
        ruff = tool["ruff"]
        target_version = ruff["target-version"]

        # Extract major.minor from requires-python (e.g., ">=3.9" -> "3.9")
        python_version = requires_python.replace(">=", "").strip()
        expected_target = f"py{python_version.replace('.', '')}"

        assert target_version == expected_target