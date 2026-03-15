from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from PIL import Image
from pypdf import PdfReader, PdfWriter

from kagazkit.core.actions import PDFActionError, PDFManager


def create_pdf(path: Path, pages: int = 1) -> Path:
    writer = PdfWriter()
    for _ in range(pages):
        writer.add_blank_page(width=200, height=200)
    with open(path, "wb") as fh:
        writer.write(fh)
    return path


class TestPDFManager:
    @patch("kagazkit.core.validators.Validator.validate_paths")
    @patch("kagazkit.core.actions.PdfWriter")
    def test_merge_pdfs_success(self, mock_writer, mock_validator, tmp_path):
        # Setup mocks
        mock_validator.return_value = [Path("a.pdf"), Path("b.pdf")]
        mock_writer_instance = mock_writer.return_value
        
        output = tmp_path / "merged.pdf"
        
        # Execute
        result = PDFManager.merge_pdfs(["a.pdf", "b.pdf"], output)
        
        # Verify
        assert result == output
        assert mock_writer_instance.append.call_count == 2
        mock_writer_instance.write.assert_called_once()
        mock_writer_instance.close.assert_called_once()

    def test_merge_pdfs_real_files(self, tmp_path):
        first_pdf = create_pdf(tmp_path / "one.pdf", pages=1)
        second_pdf = create_pdf(tmp_path / "two.pdf", pages=2)
        output = tmp_path / "merged.pdf"

        result = PDFManager.merge_pdfs([first_pdf, second_pdf], output)

        assert result == output
        assert output.exists()
        assert len(PdfReader(output).pages) == 3

    def test_merge_pdfs_rejects_invalid_pdf(self, tmp_path):
        bad_pdf = tmp_path / "bad.pdf"
        bad_pdf.write_bytes(b"not a pdf")

        with pytest.raises(PDFActionError, match="Validation failed: File does not look like a valid PDF"):
            PDFManager.merge_pdfs([bad_pdf], tmp_path / "merged.pdf")

    @patch("kagazkit.core.actions.PdfWriter")
    @patch("kagazkit.core.actions.PdfReader")
    def test_split_pdf_success(self, mock_reader, mock_writer, tmp_path):
        # Mock behavior
        mock_pdf = MagicMock()
        mock_pdf.pages = [MagicMock(), MagicMock(), MagicMock()] # 3 pages
        mock_reader.return_value = mock_pdf
        
        input_pdf = tmp_path / "test.pdf"
        input_pdf.write_bytes(b"%PDF-1.4 dummy content")
        
        # Execute
        result = PDFManager.split_pdf(input_pdf, tmp_path)
        
        # Verify
        assert len(result) == 3

    def test_split_pdf_real_file(self, tmp_path):
        source_pdf = create_pdf(tmp_path / "source.pdf", pages=3)

        result = PDFManager.split_pdf(source_pdf, tmp_path / "split")

        assert len(result) == 3
        assert all(path.exists() for path in result)
        assert all(path.read_bytes().startswith(b"%PDF") for path in result)

    @patch("kagazkit.core.actions.PdfReader")
    @patch("kagazkit.core.actions.PdfWriter")
    def test_rotate_pdf_success(self, mock_writer, mock_reader, tmp_path):
        # Mock behavior
        mock_pdf = MagicMock()
        mock_pdf.pages = [MagicMock()]
        mock_reader.return_value = mock_pdf
        
        mock_writer_instance = mock_writer.return_value
        
        input_pdf = tmp_path / "test.pdf"
        input_pdf.write_bytes(b"%PDF-1.4 dummy content")
        output_pdf = tmp_path / "rotated.pdf"
        
        # Execute
        result = PDFManager.rotate_pdf(input_pdf, output_pdf, 90)
        
        # Verify
        assert result == output_pdf
        mock_writer_instance.add_page.assert_called()
        mock_writer_instance.write.assert_called()

    def test_rotate_pdf_real_file(self, tmp_path):
        input_pdf = create_pdf(tmp_path / "input.pdf")
        output_pdf = tmp_path / "rotated.pdf"

        result = PDFManager.rotate_pdf(input_pdf, output_pdf, 90)

        assert result == output_pdf
        assert output_pdf.exists()
        assert PdfReader(output_pdf).pages[0].get("/Rotate") == 90

    @patch("kagazkit.core.validators.Validator.validate_paths")
    def test_convert_images_no_images(self, mock_validator):
        mock_validator.return_value = []
        with pytest.raises(PDFActionError, match="No valid images provided"):
            PDFManager.convert_images_to_pdf([], "out.pdf")

    @patch("kagazkit.core.validators.Validator.validate_paths")
    @patch("PIL.Image.open")
    def test_convert_images_success(self, mock_img_open, mock_validator, tmp_path):
        # Mock paths
        p1 = Path("1.png")
        p2 = Path("2.jpg")
        mock_validator.return_value = [p1, p2]
        
        # Mock Images
        img1 = MagicMock()
        img1.mode = "RGB"
        img1.copy.return_value = img1

        img2 = MagicMock()
        img2.mode = "RGBA"
        converted_img2 = MagicMock()
        img2.convert.return_value = converted_img2

        cm1 = MagicMock()
        cm1.__enter__.return_value = img1
        cm1.__exit__.return_value = False

        cm2 = MagicMock()
        cm2.__enter__.return_value = img2
        cm2.__exit__.return_value = False

        mock_img_open.side_effect = [cm1, cm2]
        
        output = tmp_path / "images.pdf"
        
        # Execute
        result = PDFManager.convert_images_to_pdf(["1.png", "2.jpg"], output)
        
        # Verify
        assert result == output
        mock_img_open.assert_any_call(p1)
        mock_img_open.assert_any_call(p2)
        # Ensure RGB images are copied before the file handle closes
        img1.copy.assert_called_once()
        # Ensure conversion to RGB happened for RGBA image
        img2.convert.assert_called_with("RGB")
        # Ensure save was called on first image
        img1.save.assert_called_once()
        mock_validator.assert_called_once_with(["1.png", "2.jpg"], mode="image")

    def test_convert_images_creates_valid_pdf_from_real_images(self, tmp_path):
        jpg_path = tmp_path / "sample.jpg"
        png_path = tmp_path / "sample.png"
        output_path = tmp_path / "sample.pdf"

        Image.new("RGB", (32, 32), color=(255, 0, 0)).save(jpg_path, "JPEG")
        Image.new("RGB", (32, 32), color=(0, 0, 255)).save(png_path, "PNG")

        result = PDFManager.convert_images_to_pdf([jpg_path, png_path], output_path)

        assert result == output_path
        assert output_path.exists()
        assert output_path.read_bytes().startswith(b"%PDF")
        assert len(PdfReader(output_path).pages) == 2

    def test_convert_images_rejects_unsupported_format(self, tmp_path):
        unsupported_path = tmp_path / "sample.webp"
        unsupported_path.write_bytes(b"fake webp content")

        with pytest.raises(PDFActionError, match="Unsupported image format"):
            PDFManager.convert_images_to_pdf([unsupported_path], tmp_path / "sample.pdf")

    def test_convert_images_rejects_corrupted_jpeg(self, tmp_path):
        corrupted_path = tmp_path / "broken.jpg"
        corrupted_path.write_bytes(b"not a valid jpeg")

        with pytest.raises(PDFActionError, match="corrupted"):
            PDFManager.convert_images_to_pdf([corrupted_path], tmp_path / "sample.pdf")
