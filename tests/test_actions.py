from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from kagazkit.core.actions import PDFActionError, PDFManager


class TestPDFManager:
    @patch('kagazkit.core.validators.Validator.validate_paths')
    @patch('kagazkit.core.actions.PdfMerger')
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

    @patch('kagazkit.core.actions.PdfWriter')
    @patch('kagazkit.core.actions.PdfReader')
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
        # Should verify output files exist, but we mock PdfReader/Writer so no files written
        # Check call count could be good

    @patch('kagazkit.core.actions.PdfReader')
    @patch('kagazkit.core.actions.PdfWriter')
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

    @patch('kagazkit.core.validators.Validator.validate_paths')
    def test_convert_images_no_images(self, mock_validator):
        mock_validator.return_value = []
        with pytest.raises(PDFActionError, match="No valid images provided"):
            PDFManager.convert_images_to_pdf([], "out.pdf")

    @patch('kagazkit.core.validators.Validator.validate_paths')
    @patch('PIL.Image.open')
    def test_convert_images_success(self, mock_img_open, mock_validator, tmp_path):
        # Mock paths
        p1 = Path("1.png")
        p2 = Path("2.jpg")
        mock_validator.return_value = [p1, p2]
        
        # Mock Images
        img1 = MagicMock()
        img1.mode = 'RGB'
        img2 = MagicMock()
        img2.mode = 'RGBA'
        
        mock_img_open.side_effect = [img1, img2]
        
        output = tmp_path / "images.pdf"
        
        # Execute
        result = PDFManager.convert_images_to_pdf(["1.png", "2.jpg"], output)
        
        # Verify
        assert result == output
        mock_img_open.assert_any_call(p1)
        mock_img_open.assert_any_call(p2)
        # Ensure conversion to RGB happened for RGBA image
        img2.convert.assert_called_with('RGB')
        # Ensure save was called on first image
        img1.save.assert_called_once()
