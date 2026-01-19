"""
Core actions module for PDF Master.
Contains the business logic for merging PDFs and converting images to PDFs.
"""

from pathlib import Path
from typing import List, Union
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from PIL import Image
from .validators import Validator, FileValidationError

class PDFActionError(Exception):
    """Custom exception for action failures."""
    pass

class PDFManager:
    """Manager class for PDF operations."""

    @staticmethod
    def merge_pdfs(file_paths: List[Union[str, Path]], output_path: Union[str, Path]) -> Path:
        """
        Merges multiple PDFs into a single file.

        Args:
            file_paths: List of paths to the PDF files to merge.
            output_path: Path where the merged PDF should be saved.

        Returns:
            Path to the output file.

        Raises:
            PDFActionError: If merging fails.
            FileValidationError: If input files are invalid.
        """
        # Validate inputs
        try:
            validated_paths = Validator.validate_paths(file_paths, file_type='pdf')
        except FileValidationError as e:
            raise PDFActionError(f"Validation failed: {e}")

        merger = PdfMerger()
        
        try:
            for path in validated_paths:
                merger.append(str(path))
            
            output_path = Path(output_path)
            # Ensure output directory exists (though UI should handle this)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            merger.write(str(output_path))
            merger.close()
            return output_path
            
        except Exception as e:
            try:
                merger.close()
            except: 
                pass
            raise PDFActionError(f"Failed to merge PDFs: {e}")

    @staticmethod
    def convert_images_to_pdf(image_paths: List[Union[str, Path]], output_path: Union[str, Path]) -> Path:
        """
        Converts a list of images to a single PDF.

        Args:
            image_paths: List of paths to image files.
            output_path: Path for the output PDF.

        Returns:
            Path to the output file.
            
        Raises:
            PDFActionError: If conversion fails.
        """
        try:
            validated_paths = Validator.validate_paths(image_paths, file_type='image')
        except FileValidationError as e:
            raise PDFActionError(f"Validation failed: {e}")

        if not validated_paths:
             raise PDFActionError("No valid images provided.")

        try:
            # Open images and convert to RGB (required for PDF)
            images = []
            for path in validated_paths:
                img = Image.open(path)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                images.append(img)

            # Save first image and append the rest
            first_image = images[0]
            rest_images = images[1:]
            
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            first_image.save(
                str(output_path), 
                "PDF", 
                resolution=100.0, 
                save_all=True, 
                append_images=rest_images
            )
            
            # Close images to free resources
            for img in images:
                img.close()
                
            return output_path

        except Exception as e:
            raise PDFActionError(f"Failed to convert images to PDF: {e}")
            
    @staticmethod
    def split_pdf(file_path: Union[str, Path], output_dir: Union[str, Path]) -> List[Path]:
        """
        Splits a PDF into individual pages.
        
        Args:
            file_path: Path to the source PDF.
            output_dir: Directory to save the pages.
            
        Returns:
            List of paths to the generated files.
        """
        try:
            Validator.validate_pdf(file_path)
        except FileValidationError as e:
            raise PDFActionError(f"Validation failed: {e}")
            
        src_path = Path(file_path)
        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        
        generated_files = []
        
        try:
            reader = PdfReader(src_path)
            base_name = src_path.stem
            
            for i, page in enumerate(reader.pages):
                writer = PdfWriter()
                writer.add_page(page)
                
                out_filename = out_dir / f"{base_name}_page_{i+1}.pdf"
                with open(out_filename, "wb") as out_file:
                    writer.write(out_file)
                
                generated_files.append(out_filename)
                
            return generated_files
            
        except Exception as e:
            raise PDFActionError(f"Failed to split PDF: {e}")

    @staticmethod
    def rotate_pdf(file_path: Union[str, Path], output_path: Union[str, Path], rotation: int) -> Path:
        """
        Rotates all pages of a PDF.
        
        Args:
            file_path: Path to source PDF.
            output_path: Path to save result.
            rotation: Degrees to rotate (90, 180, 270).
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
