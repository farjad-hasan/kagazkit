# Usage Examples

## Launch the app

```bash
kagazkit
```

Or from a source checkout:

```bash
python src/kagazkit/main.py
```

## Merge PDFs

1. Open KagazKit.
2. Go to the merge page.
3. Add two or more PDF files.
4. Arrange them in the desired order.
5. Save the merged output as a new PDF.

## Convert Images to PDF

1. Open the Images to PDF page.
2. Add `.png`, `.jpg`, or `.jpeg` files.
3. Choose an output location.
4. Save the generated PDF.

Notes:

- Unsupported image types such as `.webp` or `.heic` are rejected.
- Corrupted images are rejected during validation.

## Split a PDF

1. Open the tools page.
2. Choose a PDF to split.
3. Select an output directory.
4. KagazKit writes one PDF per page.

## Rotate a PDF

1. Open the tools page.
2. Choose a PDF file.
3. Select the rotation amount.
4. Save the rotated output as a new PDF.

## Common Limitations

- KagazKit currently supports standard PDF workflows plus image-to-PDF for PNG and JPEG inputs.
- The packaged Windows `.exe` is the recommended option for Windows users who do not want a Python environment.
- Source installs on Linux and macOS are best-effort until dedicated packaging and UI validation are added.
