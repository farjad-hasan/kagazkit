from pathlib import Path

import pytest

from kagazkit.core.validators import FileValidationError, Validator


class TestValidator:
    def test_is_pdf_valid(self, tmp_path):
        f = tmp_path / "test.pdf"
        f.write_bytes(b"%PDF-1.4")
        assert Validator.is_pdf(f) is True

    def test_is_pdf_invalid(self, tmp_path):
        f = tmp_path / "not_a.pdf"
        f.write_bytes(b"not a pdf")
        assert Validator.is_pdf(f) is False

    def test_is_pdf_nonexistent(self):
        assert Validator.is_pdf("ghost.pdf") is False

    def test_is_image_valid(self, tmp_path):
        # We'd need a real header for imghdr.what, but we can mock or just check suffix
        f = tmp_path / "img.png"
        f.write_bytes(b"\x89PNG\r\n\x1a\n") # Real PNG header
        assert Validator.is_image(f) is True

    def test_is_image_invalid_ext(self, tmp_path):
        f = tmp_path / "img.txt"
        f.write_text("hello")
        assert Validator.is_image(f) is False

    def test_validate_pdf_success(self, tmp_path):
        f = tmp_path / "valid.pdf"
        f.write_bytes(b"%PDF")
        Validator.validate_pdf(f) # Should not raise

    def test_validate_pdf_fail(self, tmp_path):
        f = tmp_path / "bad.pdf"
        f.write_bytes(b"bad")
        with pytest.raises(FileValidationError):
            Validator.validate_pdf(f)

    def test_validate_paths_pdf(self, tmp_path):
        p1 = tmp_path / "1.pdf"
        p2 = tmp_path / "2.pdf"
        p1.write_bytes(b"%PDF")
        p2.write_bytes(b"%PDF")
        
        result = Validator.validate_paths([p1, p2], mode="pdf")
        assert len(result) == 2
        assert all(isinstance(r, Path) for r in result)

    def test_validate_paths_fail(self, tmp_path):
        p1 = tmp_path / "1.pdf"
        p1.write_bytes(b"not pdf")
        with pytest.raises(FileValidationError):
            Validator.validate_paths([p1], mode="pdf")