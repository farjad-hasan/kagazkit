"""
Input validation module for PDF Master.
Handles security checks for file inputs, ensuring only valid and safe files are processed.
"""

from pathlib import Path
from typing import List, Union


class FileValidationError(Exception):
    """Custom exception for file validation failures."""
    pass

class Validator:
    """Validator class for file security checks."""

    # Magic numbers for file type verification
    MAGIC_NUMBERS = {
        'pdf': b'%PDF',
        'png': b'\x89PNG\r\n\x1a\n',
        'jpg': b'\xff\xd8\xff',
        'jpeg': b'\xff\xd8\xff',
    }

    @staticmethod
    def validate_file(file_path: Union[str, Path]) -> bool:
        """
        Validates a single file exists and is a file.

        Args:
            file_path: Path to the file.

        Returns:
            True if valid.

        Raises:
            FileValidationError: If file does not exist or is not a file.
        """
        path = Path(file_path)
        if not path.exists():
            raise FileValidationError(f"File not found: {file_path}")
        if not path.is_file():
            raise FileValidationError(f"Path is not a file: {file_path}")
        return True

    @classmethod
    def validate_pdf(cls, file_path: Union[str, Path]) -> bool:
        """
        Validates that a file is a valid PDF using magic numbers.
        
        Args:
            file_path: Path to the PDF file.
            
        Returns:
            True if valid.
            
        Raises:
            FileValidationError: If not a valid PDF.
        """
        cls.validate_file(file_path)
        try:
            with open(file_path, 'rb') as f:
                header = f.read(4)
                if not header.startswith(cls.MAGIC_NUMBERS['pdf']):
                    raise FileValidationError(f"Invalid PDF file header: {file_path}")
        except OSError as e:
            raise FileValidationError(f"Error reading file {file_path}: {e}")
            
        return True

    @classmethod
    def validate_image(cls, file_path: Union[str, Path]) -> bool:
        """
        Validates that a file is a supported image (PNG/JPG) using magic numbers.
        
        Args:
            file_path: Path to the image file.
            
        Returns:
            True if valid.
            
        Raises:
            FileValidationError: If not a valid image.
        """
        cls.validate_file(file_path)
        path = Path(file_path)
        ext = path.suffix.lower().lstrip('.')
        
        if ext not in ['png', 'jpg', 'jpeg']:
            raise FileValidationError(f"Unsupported image extension: {ext}")
            
        magic = cls.MAGIC_NUMBERS.get(ext)
        if not magic:
             # Should be covered by extension check, but for safety
             raise FileValidationError(f"Unsupported image type: {ext}")

        read_len = len(magic)
        
        try:
            with open(file_path, 'rb') as f:
                header = f.read(read_len)
                if not header.startswith(magic):
                    raise FileValidationError(f"Invalid {ext.upper()} file header: {file_path}")
        except OSError as e:
             raise FileValidationError(f"Error reading file {file_path}: {e}")
             
        return True

    @classmethod
    def validate_paths(cls, paths: List[Union[str, Path]], file_type: str = 'pdf') -> List[Path]:
        """
        Validates a list of file paths.
        
        Args:
            paths: List of file paths.
            file_type: Type validation to apply ('pdf' or 'image').
            
        Returns:
            List of validated Path objects.
        """
        validated_paths = []
        for p in paths:
            path_obj = Path(p)
            if file_type == 'pdf':
                cls.validate_pdf(path_obj)
            elif file_type == 'image':
                cls.validate_image(path_obj)
            validated_paths.append(path_obj)
        return validated_paths
