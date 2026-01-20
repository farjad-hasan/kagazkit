from pathlib import Path
from typing import List, Union

from PIL import Image


class FileValidationError(Exception):
    pass


class Validator:
    """
    Utility class for validating file types and paths.
    """
    ALLOWED_PDF_HEADER = b"%PDF"
    ALLOWED_IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg'}

    @staticmethod
    def is_pdf(file_path: Union[str, Path]) -> bool:
        """
        Checks if a file is a valid PDF by checking its header.
        """
        path = Path(file_path)
        if not path.exists():
            return False
        
        try:
            with open(path, "rb") as f:
                header = f.read(4)
                return header == Validator.ALLOWED_PDF_HEADER
        except Exception:
            return False

    @staticmethod
    def is_image(file_path: Union[str, Path]) -> bool:
        """
        Checks if a file is a valid image (JPG/PNG).
        """
        path = Path(file_path)
        if not path.exists():
            return False
            
        if path.suffix.lower() not in Validator.ALLOWED_IMAGE_EXTENSIONS:
            return False
            
        try:
            with Image.open(path) as img:
                img.verify()
                return img.format in {"PNG", "JPEG"}
        except Exception:
            try:
                with Image.open(path) as img:
                    return img.format in {"PNG", "JPEG"}
            except Exception:
                return False

    @staticmethod
    def validate_pdf(file_path: Union[str, Path]):
        """
        Validates a single PDF file. Raises FileValidationError if invalid.
        """
        if not Validator.is_pdf(file_path):
            raise FileValidationError(f"File {file_path} is not a valid PDF")

    @staticmethod
    def validate_paths(file_paths: List[Union[str, Path]], mode="pdf") -> List[Path]:
        """
        Validates a list of file paths.
        
        Args:
            file_paths: List of paths to validate.
            mode: "pdf" or "image"
        """
        validated = []
        for p in file_paths:
            path = Path(p)
            if mode == "pdf":
                if Validator.is_pdf(path):
                    validated.append(path)
                else:
                    raise FileValidationError(f"Invalid PDF: {path}")
            elif mode == "image":
                if Validator.is_image(path):
                    validated.append(path)
                else:
                    raise FileValidationError(f"Invalid Image: {path}")
        return validated
