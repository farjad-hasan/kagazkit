"""Import-only checks to ensure modules load without side effects."""

def test_import_main_module():
    __import__("kagazkit.main")


def test_import_pdf_master_app():
    from kagazkit.ui.app import PDFMasterApp  # noqa: F401
