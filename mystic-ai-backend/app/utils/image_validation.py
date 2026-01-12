"""
Image validation utilities
"""

from fastapi import UploadFile, HTTPException, status
from PIL import Image
import io
from typing import Tuple

from app.config import settings


def validate_image_file(file: UploadFile) -> None:
    """
    Validate uploaded image file

    Args:
        file: Uploaded file

    Raises:
        HTTPException: If validation fails
    """
    # Check content type
    if file.content_type not in settings.ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed types: {', '.join(settings.ALLOWED_IMAGE_TYPES)}"
        )

    # Check file size
    file.file.seek(0, 2)  # Seek to end
    file_size = file.file.tell()
    file.file.seek(0)  # Reset to beginning

    if file_size > settings.MAX_UPLOAD_SIZE:
        max_mb = settings.MAX_UPLOAD_SIZE / (1024 * 1024)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Maximum size: {max_mb}MB"
        )

    if file_size == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Empty file"
        )


def validate_image_content(file_content: bytes) -> Tuple[int, int]:
    """
    Validate image content and get dimensions

    Args:
        file_content: Image binary content

    Returns:
        Tuple of (width, height)

    Raises:
        HTTPException: If image is invalid or corrupted
    """
    try:
        image = Image.open(io.BytesIO(file_content))

        # Verify it's actually an image
        image.verify()

        # Reopen to get dimensions (verify() closes the file)
        image = Image.open(io.BytesIO(file_content))
        width, height = image.size

        # Check minimum dimensions (optional)
        min_dimension = 200
        if width < min_dimension or height < min_dimension:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Image too small. Minimum dimensions: {min_dimension}x{min_dimension}px"
            )

        # Check maximum dimensions (optional)
        max_dimension = 4096
        if width > max_dimension or height > max_dimension:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Image too large. Maximum dimensions: {max_dimension}x{max_dimension}px"
            )

        return width, height

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid or corrupted image: {str(e)}"
        )


def optimize_image(file_content: bytes, max_size: int = 1920) -> bytes:
    """
    Optimize image for storage (resize if too large, compress)

    Args:
        file_content: Original image content
        max_size: Maximum width/height

    Returns:
        Optimized image content
    """
    try:
        image = Image.open(io.BytesIO(file_content))

        # Convert RGBA to RGB if needed
        if image.mode == 'RGBA':
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[3])
            image = background

        # Resize if too large
        width, height = image.size
        if width > max_size or height > max_size:
            # Calculate new dimensions maintaining aspect ratio
            if width > height:
                new_width = max_size
                new_height = int(height * (max_size / width))
            else:
                new_height = max_size
                new_width = int(width * (max_size / height))

            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Save optimized image
        output = io.BytesIO()
        image.save(output, format='JPEG', quality=85, optimize=True)
        output.seek(0)

        return output.read()

    except Exception as e:
        # If optimization fails, return original
        return file_content


def get_image_info(file_content: bytes) -> dict:
    """
    Get image information

    Args:
        file_content: Image binary content

    Returns:
        Dictionary with image info
    """
    try:
        image = Image.open(io.BytesIO(file_content))
        return {
            "format": image.format,
            "mode": image.mode,
            "size": image.size,
            "width": image.size[0],
            "height": image.size[1]
        }
    except Exception:
        return {}
