# Help Wanted

KagazKit is currently maintained by one person. Contributions are welcome, especially where they reduce operational risk or make the project easier for users to adopt.

## High-Value Areas

### 1. Packaging and Release Confidence

Useful contributions:

- Windows `.exe` smoke testing improvements
- release automation hardening
- reproducible build validation
- better failure reporting for packaging issues

Why it matters:

The packaged Windows app is one of the main user distribution paths, so release confidence has an outsized impact.

### 2. Real-World File Workflow Testing

Useful contributions:

- add regression tests for corrupted PDFs or malformed images
- expand coverage around merge, split, rotate, and image conversion edge cases
- improve error messages when validation fails

Why it matters:

Most user-facing failures happen around real files, not mocked paths.

### 3. Documentation and Troubleshooting

Useful contributions:

- step-by-step usage examples
- screenshots or short demo GIFs
- troubleshooting entries for common install or conversion failures
- clearer guidance for `.exe` users vs `pip` users

Why it matters:

Good docs reduce support load and make the project easier to trust.

### 4. UI and Accessibility Polish

Useful contributions:

- keyboard navigation improvements
- drag-and-drop reliability fixes
- better status and error messaging
- layout polish for different screen sizes

Why it matters:

KagazKit is a desktop app, so perceived quality depends heavily on usability details.

## Good First Contributions

Good entry points for new contributors:

- improve or expand an existing test
- document a bug reproduction clearly
- fix a typo, broken link, or unclear README/support text
- add a troubleshooting note for a real user error
- improve one small workflow without broad refactoring

## How To Signal Interest

- open or comment on a GitHub issue before starting large changes
- mention your environment, install method, and the workflow you are touching
- keep pull requests focused and include verification notes

## Labels

When available, these labels are the best contributor entry points:

- `good first issue`
- `help wanted`
- `needs reproduction`
- `documentation`
- `tests`

If labels are missing on an issue you want to work on, leave a comment and ask before doing larger work.
