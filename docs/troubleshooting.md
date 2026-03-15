# Troubleshooting

This page collects the most common KagazKit failure modes and the fastest ways to diagnose them.

## Image To PDF Fails

### Unsupported image type

Symptom:

- KagazKit reports that an image is invalid or unsupported.

What to check:

- KagazKit currently supports only `.png`, `.jpg`, and `.jpeg` inputs for image-to-PDF.
- Renaming another format, such as `.webp` or `.heic`, to `.jpg` does not make it valid.

What to do:

- convert the image to PNG or JPEG first
- retry with the converted file

### Corrupted or unreadable image

Symptom:

- KagazKit reports that an image could not be opened or is corrupted.

What to check:

- confirm the file opens in another image viewer
- confirm the file transfer or download completed successfully

What to do:

- export the image again from the source app
- re-download or re-copy the file

### Old Windows `.exe`

Symptom:

- image-to-PDF fails in the packaged app even though the same file should be supported

What to check:

- compare the app version against the latest [GitHub release](https://github.com/farjad-hasan/kagazkit/releases)

What to do:

- download the latest Windows `.exe`
- if the issue persists on the newest release, open a bug report with the version number and a safe-to-share sample file when possible

## Merge, Split, Or Rotate Fails

### Invalid PDF

Symptom:

- KagazKit reports that the file is not a valid PDF

What to check:

- confirm the file extension is really `.pdf`
- confirm the file starts as a real PDF and is not an HTML download, image, or renamed file
- try opening it in a regular PDF viewer

What to do:

- re-export the file as PDF from the source app
- if the file opens normally elsewhere but KagazKit still rejects it, report the issue

### Corrupted PDF

Symptom:

- validation passes but a merge, split, or rotate action still fails

What to check:

- the input file may have a valid PDF header but broken internal structure

What to do:

- open and re-save the PDF in another viewer or editor
- retry the workflow with the re-saved file

## Build Or Packaging Problems

### Windows protected your PC / SmartScreen

Symptom:

- Windows shows `Windows protected your PC`
- Microsoft Defender SmartScreen says KagazKit is an unrecognized app

What it means:

- KagazKit is currently unsigned, so SmartScreen may warn even when the app is the official release build.
- This warning does not by itself mean KagazKit was identified as malware.

What to check:

- confirm you downloaded `KagazKit.exe` from the official [GitHub Releases](https://github.com/farjad-hasan/kagazkit/releases) page
- confirm the release also includes `KagazKit.exe.sha256`
- in PowerShell, run `Get-FileHash .\KagazKit.exe -Algorithm SHA256`
- compare the SHA256 output to the value stored in `KagazKit.exe.sha256`

What to do:

- if the hash matches, you have the official published build for that release
- if the hash does not match, delete the file and download it again from the release page
- if you prefer not to run unsigned binaries, use the PyPI package or build from source instead

### `No module named build.__main__`

Symptom:

- packaging commands fail while building release artifacts

What to check:

- whether you are running the build from inside a directory named `build`

What to do:

- follow the parent-directory instructions in [RELEASE.md](../RELEASE.md)

### Windows `.exe` exits immediately

Symptom:

- the packaged app launches and disappears

What to check:

- whether the build completed successfully
- whether the executable was produced from the current source tree

What to do:

- rebuild with `python build_app.py`
- use the smoke-check process documented in CI and release steps

## Before Reporting A Bug

Include:

- KagazKit version
- install method: Windows `.exe`, `pip install kagazkit`, or source checkout
- OS and Python version when applicable
- exact steps to reproduce
- expected behavior
- actual behavior
- screenshots or sample files when safe to share

Use:

- [GitHub Issues](https://github.com/farjad-hasan/kagazkit/issues) for regular bugs and feature requests
- [SECURITY.md](../SECURITY.md) for security problems
