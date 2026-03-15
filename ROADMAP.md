# Roadmap

This roadmap describes where KagazKit should go as a product, not just as a repository. It is intentionally focused on features that make the desktop app more useful, more polished, and more competitive with lightweight PDF utilities.

## Product Direction

KagazKit should become a focused desktop PDF utility that is:

- easy to use for common document tasks
- safe and predictable with real-world files
- polished enough that Windows users can rely on the packaged `.exe`
- narrow in scope, rather than trying to become an all-purpose enterprise PDF suite

## Planning Principles

- polish the current workflows before expanding too broadly
- prioritize features that reduce user friction in merge, split, rotate, and image-to-PDF
- prefer features that fit a desktop drag-and-drop workflow
- keep the roadmap realistic for a single-maintainer project

## Near Term

### v0.1.7

Goal: ship a clean public baseline after the `pypdf` migration and recent OSS/readiness work.

Planned outcomes:

- release the dependency migration from `PyPDF2` to `pypdf`
- confirm the GitHub vulnerability signal clears after release
- keep Windows `.exe` packaging stable and reproducible
- tighten error messaging for current workflows where failures are still vague

### v0.2

Goal: make the current core workflows feel complete instead of minimal.

Feature priorities:

- page range support for merge jobs
- extract selected pages instead of only split-all-pages behavior
- rotate selected pages, not just full-document flows
- reorder input files or pages before saving
- improve completion, progress, and error dialogs

Why this matters:

These are the missing controls users expect before they trust a PDF utility for everyday work.

## Mid Term

### v0.3

Goal: make KagazKit feel like a serious desktop tool instead of a basic wrapper around file operations.

Feature priorities:

- page thumbnail previews before export
- image reorder controls for image-to-PDF conversion
- page size, orientation, and margin options for image-to-PDF
- recent files and recent output folder shortcuts
- "open output folder" and better post-run summaries
- batch-friendly workflow improvements for larger jobs

Why this matters:

This is the stage where the product becomes more convenient than a generic command-line or web utility for repeated use.

## Later

### v0.4

Goal: expand from core PDF operations into higher-value document tooling.

Feature priorities:

- watermark PDF
- add page numbers
- password-protect PDF
- unlock PDF when supported by the dependency stack
- compress PDF where output quality and expectations can be explained clearly

Why this matters:

These features broaden KagazKit from "basic utility" into "daily-use desktop toolkit."

## Nice-To-Have Backlog

These are useful, but should follow the roadmap above rather than interrupt it:

- keyboard shortcuts for major actions
- accessibility improvements across the desktop UI
- better drag-and-drop queue management
- mixed-input jobs that combine images and PDFs into one output flow
- small workflow presets for recurring tasks

## Non-Goals For Now

These are intentionally out of scope until the core product is stronger:

- cloud sync or account features
- browser-based or hosted conversion service
- OCR and full document scanning pipeline
- advanced editing features that require building a full PDF editor
- plugin systems or major extensibility layers

## Contributor Alignment

If you want to contribute, the most roadmap-aligned areas today are:

- real-file regression tests around current workflows
- better UX for merge, split, rotate, and image-to-PDF
- packaging and Windows release confidence
- docs and troubleshooting that support the current and next roadmap stages

See [docs/help-wanted.md](docs/help-wanted.md) for contribution entry points.
