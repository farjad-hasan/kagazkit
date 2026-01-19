
import pytest

from kagazkit.core.validators import FileValidationError, Validator


class TestValidator:
    def test_validate_file_exists(self, tmp_path):
        f = tmp_path / "test.txt"
        f.touch()
        assert Validator.validate_file(f) is True

    def test_validate_file_not_found(self):
        with pytest.raises(FileValidationError, match="File not found"):
            Validator.validate_file("non_existent_file.txt")

    def test_validate_pdf_valid(self, tmp_path):
        f = tmp_path / "test.pdf"
        f.write_bytes(b"%PDF-1.4 header")
        assert Validator.validate_pdf(f) is True

    def test_validate_pdf_invalid_header(self, tmp_path):
        f = tmp_path / "fake.pdf"
        f.write_bytes(b"NOT_A_PDF_HEADER")
        with pytest.raises(FileValidationError, match="Invalid PDF file header"):
            Validator.validate_pdf(f)

    def test_validate_image_valid_png(self, tmp_path):
        f = tmp_path / "test.png"
        f.write_bytes(b"\x89PNG\r\n\x1a\ncontent")
        assert Validator.validate_image(f) is True

    def test_validate_image_valid_jpg(self, tmp_path):
        f = tmp_path / "test.jpg"
        f.write_bytes(b"\xff\xd8\xffcontent")
        assert Validator.validate_image(f) is True

    def test_validate_image_invalid_extension(self, tmp_path):
        f = tmp_path / "test.txt"
        f.touch()
        with pytest.raises(FileValidationError, match="Unsupported image extension"):
            Validator.validate_image(f)

    def test_validate_image_invalid_magic(self, tmp_path):
        f = tmp_path / "test.png"
        f.write_bytes(b"BAD_MAGIC")
        with pytest.raises(FileValidationError, match="Invalid PNG file header"):
            Validator.validate_image(f)
