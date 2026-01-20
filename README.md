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

## Installation

### Via pip (Recommended)

KagazKit is available on PyPI and can be installed directly using pip:

```bash
pip install kagazkit
```

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

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Releasing

See [RELEASE.md](RELEASE.md) for the release checklist, including drafting a GitHub release and publishing to PyPI.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
