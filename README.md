# KagazKit

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)

> **Note**: This project is currently under active development.

**KagazKit** (“Kagaz” means paper) is a modern, secure, and professional PDF toolkit built with Python and CustomTkinter. It provides an elegant interface for merging PDFs, converting images to PDFs, splitting, rotating, and more.

## Features

- **Modern UI**: Dark mode support, professional design using CustomTkinter.
- **Secure**: Validation of file inputs and safe handling of file operations.
- **Merge PDFs**: Combine multiple PDF files with ease.
- **Image to PDF**: Convert standard image formats (JPG, PNG) to PDF.
- **Tools**: Split and Rotate PDFs functionality.
- **Drag & Drop**: Intuitive file management.

## Supported Platforms

| Platform | Install Method | Status |
| --- | --- | --- |
| Windows 10/11 | Packaged `.exe` release | Supported |
| Windows 10/11 | `pip install kagazkit` | Supported |
| Linux | Source install | Best effort |
| macOS | Source install | Best effort |

| Python | Status |
| --- | --- |
| 3.9 | Supported |
| 3.10 | Supported |
| 3.11 | Supported |

## Supported File Types

| Workflow | Supported Inputs | Output |
| --- | --- | --- |
| Merge PDFs | `.pdf` | merged `.pdf` |
| Images to PDF | `.png`, `.jpg`, `.jpeg` | `.pdf` |
| Split PDF | `.pdf` | one `.pdf` per page |
| Rotate PDF | `.pdf` | rotated `.pdf` |

## Installation

### Via pip (Recommended)

KagazKit is available on PyPI and can be installed directly using pip:

```bash
pip install kagazkit
```

### Windows `.exe`

Download the latest packaged Windows build from the [GitHub Releases](https://github.com/farjad-hasan/kagazkit/releases) page when you want a no-Python install.

- The Windows build is currently unsigned, so Microsoft Defender SmartScreen may show an "unrecognized app" warning.
- Download `KagazKit.exe` only from the official GitHub Releases page.
- Each release also includes `KagazKit.exe.sha256` so you can verify the download before running it.
- In PowerShell, run `Get-FileHash .\KagazKit.exe -Algorithm SHA256` and compare the result to the value in `KagazKit.exe.sha256`.

### From Source

1.  Clone the repository:
    ```bash
    git clone https://github.com/farjad-hasan/kagazkit.git
    cd kagazkit
    ```

2.  Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4.  Install the package in editable mode:
    ```bash
    pip install -e .
    ```

## Usage

Run the application:

```bash
kagazkit
# Or directly via python
python src/kagazkit/main.py
```

For concrete workflows and expected inputs, see [docs/usage.md](docs/usage.md).
For planned product direction and upcoming feature priorities, see [ROADMAP.md](ROADMAP.md).
For common failures and packaging-specific guidance, see [docs/troubleshooting.md](docs/troubleshooting.md).

## Troubleshooting

- If image-to-PDF fails, confirm the file is `.png`, `.jpg`, or `.jpeg` and not a renamed unsupported format.
- If you are using the Windows `.exe`, compare its version against the latest GitHub release before reporting a conversion issue.
- If packaging commands fail locally with `No module named build.__main__`, follow the parent-directory build instructions in [RELEASE.md](RELEASE.md).
- For step-by-step fixes and bug-reporting prep, see [docs/troubleshooting.md](docs/troubleshooting.md).

## Project Status

KagazKit is an actively maintained single-maintainer open-source project. The project is releaseable and documented, but reviews and support still depend on one primary maintainer.

For maintainer ownership and expectations, see [MAINTAINERS.md](MAINTAINERS.md).

## Maintainer and Support

KagazKit is currently maintained by Farjad Hasan.

- Pull requests and issues are reviewed on a best-effort basis.
- Security reports should follow [SECURITY.md](SECURITY.md) instead of public issues.
- General usage questions and bug reports should go through [GitHub Issues](https://github.com/farjad-hasan/kagazkit/issues) or the guidance in [SUPPORT.md](SUPPORT.md).
- Acknowledgement targets:
  - security reports: within 48 hours
  - standard issues and pull requests: best effort, typically within 7 days

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Help Wanted

KagazKit is open to outside contributions, especially in areas that reduce single-maintainer risk or improve user experience.

- Windows packaged-app testing and release automation
- GUI-focused end-to-end smoke tests
- documentation improvements and troubleshooting guides
- bug reproduction for file conversion edge cases
- polish for onboarding, accessibility, and release notes

For contributor entry points, see [docs/help-wanted.md](docs/help-wanted.md).

## Releasing

See [RELEASE.md](RELEASE.md) for the release checklist, including drafting a GitHub release and publishing to PyPI.

## Product Roadmap

See [ROADMAP.md](ROADMAP.md) for the current product roadmap, including near-term and later feature priorities.

## Project Hygiene

- Changelog: [CHANGELOG.md](CHANGELOG.md)
- Maintainers: [MAINTAINERS.md](MAINTAINERS.md)
- Product roadmap: [ROADMAP.md](ROADMAP.md)
- Security policy: [SECURITY.md](SECURITY.md)
- Support policy: [SUPPORT.md](SUPPORT.md)
- Usage examples: [docs/usage.md](docs/usage.md)
- Troubleshooting: [docs/troubleshooting.md](docs/troubleshooting.md)
- Help wanted: [docs/help-wanted.md](docs/help-wanted.md)
- Issue tracker: [GitHub Issues](https://github.com/farjad-hasan/kagazkit/issues)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
