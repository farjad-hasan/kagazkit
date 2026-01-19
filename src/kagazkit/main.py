"""
Entry point for KagazKit application.
"""
import os
import sys

# Ensure src is in pythonpath
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from kagazkit.ui.app import PDFMasterApp


def main():
    app = PDFMasterApp()
    app.mainloop()


if __name__ == "__main__":
    main()
