"""
Entry point for KagazKit application.
"""
import os
import sys
from pathlib import Path

# Ensure src is in pythonpath
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from kagazkit.ui.app import PDFMasterApp


def _run_smoke_test(app: PDFMasterApp) -> int:
    smoke_result = os.environ.get("KAGAZKIT_SMOKE_TEST_FILE")
    if not smoke_result:
        return 1

    result_path = Path(smoke_result)
    try:
        app.update_idletasks()
        app.update()

        expected_pages = {"merge", "image", "tools"}
        if set(app.pages.keys()) != expected_pages:
            raise RuntimeError(f"Unexpected page set: {sorted(app.pages.keys())}")
        if app.logo_label.cget("text") != "KagazKit":
            raise RuntimeError("Sidebar branding did not initialize correctly")

        result_path.write_text("ok", encoding="utf-8")
        return 0
    except Exception as exc:
        result_path.write_text(f"error: {exc}", encoding="utf-8")
        return 1
    finally:
        app.destroy()


def main():
    app = PDFMasterApp()
    if os.environ.get("KAGAZKIT_SMOKE_TEST_FILE"):
        raise SystemExit(_run_smoke_test(app))
    app.mainloop()


if __name__ == "__main__":
    main()
