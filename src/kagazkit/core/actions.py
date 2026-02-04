from pathlib import Path
from typing import List, Union

from PIL import Image
from PyPDF2 import PdfMerger, PdfReader, PdfWriter

from .validators import FileValidationError, Validator


class PDFActionError(Exception):
    pass


class PDFManager:
    @staticmethod
    def merge_pdfs(file_paths: List[Union[str, Path]], output_path: Union[str, Path]) -> Path:
        """
        Merges multiple PDFs into a single file.
        """
        try:
            Validator.validate_paths(file_paths)
        except FileValidationError as e:
            raise PDFActionError(f"Validation failed: {e}")

        try:
            merger = PdfMerger()
            for path in file_paths:
                merger.append(str(path))

            output_path = Path(output_path)
            merger.write(str(output_path))
            merger.close()
            return output_path
        except Exception as e:
            raise PDFActionError(f"Failed to merge PDFs: {e}")

    @staticmethod
    def convert_images_to_pdf(image_paths: List[Union[str, Path]], output_path: Union[str, Path]) -> Path:
        """
        Converts multiple images into a single PDF.
        """
        try:
            valid_paths = Validator.validate_paths(image_paths, mode="image")
            if not valid_paths:
                raise PDFActionError("No valid images provided")

            images = []
            for path in valid_paths:
                img = Image.open(path)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                images.append(img)

            output_path = Path(output_path)
            if images:
                images[0].save(
                    output_path,
                    save_all=True,
                    append_images=images[1:]
                )

            # Cleanup
            for img in images:
                img.close()

            return output_path
        except Exception as e:
            raise PDFActionError(f"Failed to convert images: {e}")

    @staticmethod
    def split_pdf(file_path: Union[str, Path], output_dir: Union[str, Path]) -> List[Path]:
        """
        Splits a PDF into individual pages.
        """
        try:
            Validator.validate_pdf(file_path)
        except FileValidationError as e:
            raise PDFActionError(f"Validation failed: {e}")

        try:
            reader = PdfReader(file_path)
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            output_files = []
            for i, page in enumerate(reader.pages):
                writer = PdfWriter()
                writer.add_page(page)
                output_path = output_dir / f"page_{i+1}.pdf"
                with open(output_path, "wb") as f:
                    writer.write(f)
                output_files.append(output_path)
                
            return output_files
        except Exception as e:
            raise PDFActionError(f"Failed to split PDF: {e}")

    @staticmethod
    def rotate_pdf(file_path: Union[str, Path], output_path: Union[str, Path], rotation: int) -> Path:
        """
        Rotates all pages of a PDF.
        """
        try:
            Validator.validate_pdf(file_path)
        except FileValidationError as e:
            raise PDFActionError(f"Validation failed: {e}")
            
        try:
            reader = PdfReader(file_path)
            writer = PdfWriter()
            
            for page in reader.pages:
                page.rotate(rotation)
                writer.add_page(page)
                
            output_path = Path(output_path)
            with open(output_path, "wb") as f:
                writer.write(f)
                
            return output_path
        except Exception as e:
            raise PDFActionError(f"Failed to rotate PDF: {e}")
