from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from kagazkit.core.actions import PDFActionError, PDFManager


class TestPDFManager:
    @patch("kagazkit.core.validators.Validator.validate_paths")
    @patch("kagazkit.core.actions.PdfMerger")
    def test_merge_pdfs_success(self, mock_merger, mock_validator, tmp_path):
        # Setup mocks
        mock_validator.return_value = [Path("a.pdf"), Path("b.pdf")]
        mock_merger_instance = mock_merger.return_value
        
        output = tmp_path / "merged.pdf"
        
        # Execute
        result = PDFManager.merge_pdfs(["a.pdf", "b.pdf"], output)
        
        # Verify
        assert result == output
        assert mock_merger_instance.append.call_count == 2
        mock_merger_instance.write.assert_called_once()
        mock_merger_instance.close.assert_called_once()

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
        img2 = MagicMock()
        img2.mode = "RGBA"
        
        mock_img_open.side_effect = [img1, img2]
        
        output = tmp_path / "images.pdf"
        
        # Execute
        result = PDFManager.convert_images_to_pdf(["1.png", "2.jpg"], output)
        
        # Verify
        assert result == output
        mock_img_open.assert_any_call(p1)
        mock_img_open.assert_any_call(p2)
        # Ensure conversion to RGB happened for RGBA image
        img2.convert.assert_called_with("RGB")
        # Ensure save was called on first image
        img1.save.assert_called_once()

    @patch("kagazkit.core.validators.Validator.validate_paths")
    def test_merge_pdfs_validation_error(self, mock_validator):
        """Test merge_pdfs raises PDFActionError when validation fails."""
        from kagazkit.core.validators import FileValidationError
        mock_validator.side_effect = FileValidationError("Invalid file")

        with pytest.raises(PDFActionError, match="Validation failed"):
            PDFManager.merge_pdfs(["bad.pdf"], "output.pdf")

    @patch("kagazkit.core.validators.Validator.validate_paths")
    @patch("kagazkit.core.actions.PdfMerger")
    def test_merge_pdfs_merge_error(self, mock_merger, mock_validator):
        """Test merge_pdfs handles errors during merging."""
        mock_validator.return_value = [Path("a.pdf")]
        mock_merger.return_value.append.side_effect = Exception("Merge failed")

        with pytest.raises(PDFActionError, match="Failed to merge PDFs"):
            PDFManager.merge_pdfs(["a.pdf"], "output.pdf")

    @patch("kagazkit.core.validators.Validator.validate_paths")
    @patch("kagazkit.core.actions.PdfMerger")
    def test_merge_pdfs_empty_list(self, mock_merger, mock_validator, tmp_path):
        """Test merge_pdfs with empty file list."""
        mock_validator.return_value = []
        mock_merger_instance = mock_merger.return_value

        output = tmp_path / "merged.pdf"
        result = PDFManager.merge_pdfs([], output)

        assert result == output
        # Should not call append for empty list
        mock_merger_instance.append.assert_not_called()

    @patch("kagazkit.core.validators.Validator.validate_paths")
    @patch("kagazkit.core.actions.PdfMerger")
    def test_merge_pdfs_single_file(self, mock_merger, mock_validator, tmp_path):
        """Test merge_pdfs with a single file."""
        mock_validator.return_value = [Path("single.pdf")]
        mock_merger_instance = mock_merger.return_value

        output = tmp_path / "merged.pdf"
        result = PDFManager.merge_pdfs(["single.pdf"], output)

        assert result == output
        assert mock_merger_instance.append.call_count == 1

    def test_split_pdf_validation_error(self, tmp_path):
        """Test split_pdf raises PDFActionError when validation fails."""
        bad_file = tmp_path / "bad.pdf"
        bad_file.write_bytes(b"not a pdf")

        with pytest.raises(PDFActionError, match="Validation failed"):
            PDFManager.split_pdf(bad_file, tmp_path)

    @patch("kagazkit.core.actions.PdfReader")
    def test_split_pdf_read_error(self, mock_reader, tmp_path):
        """Test split_pdf handles errors during reading."""
        input_pdf = tmp_path / "test.pdf"
        input_pdf.write_bytes(b"%PDF-1.4 dummy content")

        mock_reader.side_effect = Exception("Read failed")

        with pytest.raises(PDFActionError, match="Failed to split PDF"):
            PDFManager.split_pdf(input_pdf, tmp_path)

    @patch("kagazkit.core.actions.PdfWriter")
    @patch("kagazkit.core.actions.PdfReader")
    def test_split_pdf_empty_pdf(self, mock_reader, mock_writer, tmp_path):
        """Test split_pdf with a PDF that has no pages."""
        mock_pdf = MagicMock()
        mock_pdf.pages = []
        mock_reader.return_value = mock_pdf

        input_pdf = tmp_path / "empty.pdf"
        input_pdf.write_bytes(b"%PDF-1.4 dummy content")

        result = PDFManager.split_pdf(input_pdf, tmp_path)

        assert len(result) == 0

    @patch("kagazkit.core.actions.PdfWriter")
    @patch("kagazkit.core.actions.PdfReader")
    def test_split_pdf_creates_output_directory(self, mock_reader, mock_writer, tmp_path):
        """Test split_pdf creates output directory if it doesn't exist."""
        mock_pdf = MagicMock()
        mock_pdf.pages = [MagicMock()]
        mock_reader.return_value = mock_pdf

        input_pdf = tmp_path / "test.pdf"
        input_pdf.write_bytes(b"%PDF-1.4 dummy content")

        output_dir = tmp_path / "new_dir" / "nested"
        result = PDFManager.split_pdf(input_pdf, output_dir)

        assert output_dir.exists()
        assert output_dir.is_dir()

    def test_rotate_pdf_validation_error(self, tmp_path):
        """Test rotate_pdf raises PDFActionError when validation fails."""
        bad_file = tmp_path / "bad.pdf"
        bad_file.write_bytes(b"not a pdf")
        output = tmp_path / "rotated.pdf"

        with pytest.raises(PDFActionError, match="Validation failed"):
            PDFManager.rotate_pdf(bad_file, output, 90)

    @patch("kagazkit.core.actions.PdfReader")
    def test_rotate_pdf_read_error(self, mock_reader, tmp_path):
        """Test rotate_pdf handles errors during reading."""
        input_pdf = tmp_path / "test.pdf"
        input_pdf.write_bytes(b"%PDF-1.4 dummy content")
        output_pdf = tmp_path / "rotated.pdf"

        mock_reader.side_effect = Exception("Read failed")

        with pytest.raises(PDFActionError, match="Failed to rotate PDF"):
            PDFManager.rotate_pdf(input_pdf, output_pdf, 90)

    @patch("kagazkit.core.actions.PdfReader")
    @patch("kagazkit.core.actions.PdfWriter")
    def test_rotate_pdf_various_angles(self, mock_writer, mock_reader, tmp_path):
        """Test rotate_pdf with different rotation angles."""
        mock_pdf = MagicMock()
        mock_page = MagicMock()
        mock_pdf.pages = [mock_page]
        mock_reader.return_value = mock_pdf

        mock_writer_instance = mock_writer.return_value

        input_pdf = tmp_path / "test.pdf"
        input_pdf.write_bytes(b"%PDF-1.4 dummy content")

        for angle in [90, 180, 270, -90]:
            output_pdf = tmp_path / f"rotated_{angle}.pdf"
            result = PDFManager.rotate_pdf(input_pdf, output_pdf, angle)

            assert result == output_pdf
            mock_page.rotate.assert_called_with(angle)

    @patch("kagazkit.core.actions.PdfReader")
    @patch("kagazkit.core.actions.PdfWriter")
    def test_rotate_pdf_multiple_pages(self, mock_writer, mock_reader, tmp_path):
        """Test rotate_pdf with multiple pages."""
        mock_pdf = MagicMock()
        mock_pages = [MagicMock() for _ in range(5)]
        mock_pdf.pages = mock_pages
        mock_reader.return_value = mock_pdf

        mock_writer_instance = mock_writer.return_value

        input_pdf = tmp_path / "test.pdf"
        input_pdf.write_bytes(b"%PDF-1.4 dummy content")
        output_pdf = tmp_path / "rotated.pdf"

        result = PDFManager.rotate_pdf(input_pdf, output_pdf, 90)

        # Verify all pages were rotated and added
        assert mock_writer_instance.add_page.call_count == 5
        for page in mock_pages:
            page.rotate.assert_called_once_with(90)

    @patch("kagazkit.core.validators.Validator.validate_paths")
    @patch("PIL.Image.open")
    def test_convert_images_single_image(self, mock_img_open, mock_validator, tmp_path):
        """Test convert_images_to_pdf with a single image."""
        p1 = Path("single.png")
        mock_validator.return_value = [p1]

        img1 = MagicMock()
        img1.mode = "RGB"
        mock_img_open.return_value = img1

        output = tmp_path / "single.pdf"
        result = PDFManager.convert_images_to_pdf(["single.png"], output)

        assert result == output
        # With only one image, append_images should be empty list
        img1.save.assert_called_once()

    @patch("kagazkit.core.validators.Validator.validate_paths")
    @patch("PIL.Image.open")
    def test_convert_images_all_need_conversion(self, mock_img_open, mock_validator, tmp_path):
        """Test convert_images_to_pdf where all images need RGB conversion."""
        paths = [Path("1.png"), Path("2.png")]
        mock_validator.return_value = paths

        # All images are RGBA
        img1 = MagicMock()
        img1.mode = "RGBA"
        img2 = MagicMock()
        img2.mode = "RGBA"

        mock_img_open.side_effect = [img1, img2]

        output = tmp_path / "images.pdf"
        result = PDFManager.convert_images_to_pdf(["1.png", "2.png"], output)

        assert result == output
        img1.convert.assert_called_with("RGB")
        img2.convert.assert_called_with("RGB")

    @patch("kagazkit.core.validators.Validator.validate_paths")
    @patch("PIL.Image.open")
    def test_convert_images_cleanup_on_success(self, mock_img_open, mock_validator, tmp_path):
        """Test that images are properly closed after conversion."""
        p1 = Path("1.png")
        mock_validator.return_value = [p1]

        img1 = MagicMock()
        img1.mode = "RGB"
        mock_img_open.return_value = img1

        output = tmp_path / "images.pdf"
        PDFManager.convert_images_to_pdf(["1.png"], output)

        # Verify image was closed
        img1.close.assert_called_once()

    @patch("kagazkit.core.validators.Validator.validate_paths")
    @patch("PIL.Image.open")
    def test_convert_images_error_during_conversion(self, mock_img_open, mock_validator):
        """Test convert_images_to_pdf handles errors during image processing."""
        p1 = Path("1.png")
        mock_validator.return_value = [p1]

        mock_img_open.side_effect = Exception("Cannot open image")

        with pytest.raises(PDFActionError, match="Failed to convert images"):
            PDFManager.convert_images_to_pdf(["1.png"], "output.pdf")

    @patch("kagazkit.core.validators.Validator.validate_paths")
    @patch("PIL.Image.open")
    def test_convert_images_mixed_modes(self, mock_img_open, mock_validator, tmp_path):
        """Test convert_images_to_pdf with images in different color modes."""
        paths = [Path("1.png"), Path("2.jpg"), Path("3.png")]
        mock_validator.return_value = paths

        # Mix of RGB, RGBA, and L (grayscale) modes
        img1 = MagicMock()
        img1.mode = "RGB"
        img2 = MagicMock()
        img2.mode = "RGBA"
        img3 = MagicMock()
        img3.mode = "L"

        mock_img_open.side_effect = [img1, img2, img3]

        output = tmp_path / "mixed.pdf"
        result = PDFManager.convert_images_to_pdf(paths, output)

        assert result == output
        # Only non-RGB images should be converted
        img1.convert.assert_not_called()
        img2.convert.assert_called_with("RGB")
        img3.convert.assert_called_with("RGB")

    def test_pdf_action_error_inheritance(self):
        """Test that PDFActionError inherits from Exception."""
        assert issubclass(PDFActionError, Exception)

    def test_pdf_action_error_message(self):
        """Test PDFActionError can be raised with a message."""
        error_msg = "Test error message"
        try:
            raise PDFActionError(error_msg)
        except PDFActionError as e:
            assert str(e) == error_msg

    @patch("kagazkit.core.validators.Validator.validate_paths")
    @patch("kagazkit.core.actions.PdfMerger")
    def test_merge_pdfs_returns_path_object(self, mock_merger, mock_validator, tmp_path):
        """Test that merge_pdfs returns a Path object, not a string."""
        mock_validator.return_value = [Path("a.pdf")]
        mock_merger_instance = mock_merger.return_value

        output = tmp_path / "merged.pdf"
        result = PDFManager.merge_pdfs(["a.pdf"], output)

        assert isinstance(result, Path)

    @patch("kagazkit.core.actions.PdfWriter")
    @patch("kagazkit.core.actions.PdfReader")
    def test_split_pdf_returns_list_of_paths(self, mock_reader, mock_writer, tmp_path):
        """Test that split_pdf returns a list of Path objects."""
        mock_pdf = MagicMock()
        mock_pdf.pages = [MagicMock(), MagicMock()]
        mock_reader.return_value = mock_pdf

        input_pdf = tmp_path / "test.pdf"
        input_pdf.write_bytes(b"%PDF-1.4 dummy content")

        result = PDFManager.split_pdf(input_pdf, tmp_path)

        assert isinstance(result, list)
        assert all(isinstance(p, Path) for p in result)