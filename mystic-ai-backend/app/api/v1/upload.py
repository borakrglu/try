"""
Upload API endpoints - Image upload for readings
"""

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from typing import List
from pydantic import BaseModel

from app.models.user import User
from app.api.deps import get_current_user
from app.services.storage_service import StorageService
from app.utils.image_validation import (
    validate_image_file,
    validate_image_content,
    optimize_image
)

router = APIRouter()


class ImageUploadResponse(BaseModel):
    """Response for image upload"""
    url: str
    width: int
    height: int
    file_size: int


class MultipleImageUploadResponse(BaseModel):
    """Response for multiple image uploads"""
    images: List[ImageUploadResponse]


@router.post("/image", response_model=ImageUploadResponse)
async def upload_single_image(
    file: UploadFile = File(..., description="Image file to upload"),
    image_type: str = "reading",
    current_user: User = Depends(get_current_user)
):
    """
    Upload a single image

    **Supported formats:** JPEG, PNG, WebP
    **Max size:** 10MB
    **Min dimensions:** 200x200px
    **Max dimensions:** 4096x4096px

    **Image types:**
    - `reading`: For coffee cup, tarot, palm readings
    - `profile`: For user profile pictures

    **Returns:** Uploaded image URL and metadata

    **Example:**
    ```bash
    curl -X POST "http://localhost:8000/api/v1/upload/image" \
      -H "Authorization: Bearer YOUR_TOKEN" \
      -F "file=@coffee_cup.jpg" \
      -F "image_type=reading"
    ```
    """
    # Validate file
    validate_image_file(file)

    # Read file content
    file_content = await file.read()

    # Validate image content and get dimensions
    width, height = validate_image_content(file_content)

    # Optimize image
    optimized_content = optimize_image(file_content)

    # Upload to storage
    storage_service = StorageService()
    url = storage_service.upload_image(
        file_content=optimized_content,
        filename=file.filename,
        content_type=file.content_type,
        user_id=current_user.id,
        image_type=image_type
    )

    return ImageUploadResponse(
        url=url,
        width=width,
        height=height,
        file_size=len(optimized_content)
    )


@router.post("/images", response_model=MultipleImageUploadResponse)
async def upload_multiple_images(
    files: List[UploadFile] = File(..., description="Multiple image files"),
    image_type: str = "reading",
    current_user: User = Depends(get_current_user)
):
    """
    Upload multiple images (for coffee reading: 3 images)

    **Limit:** Maximum 5 files per request

    **Returns:** List of uploaded image URLs

    **Example:**
    ```bash
    curl -X POST "http://localhost:8000/api/v1/upload/images" \
      -H "Authorization: Bearer YOUR_TOKEN" \
      -F "files=@cup_interior.jpg" \
      -F "files=@cup_saucer.jpg" \
      -F "files=@cup_side.jpg" \
      -F "image_type=reading"
    ```
    """
    # Validate number of files
    if len(files) > 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum 5 files allowed per upload"
        )

    if len(files) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No files provided"
        )

    uploaded_images = []
    storage_service = StorageService()

    for file in files:
        # Validate file
        validate_image_file(file)

        # Read file content
        file_content = await file.read()

        # Validate image content
        width, height = validate_image_content(file_content)

        # Optimize image
        optimized_content = optimize_image(file_content)

        # Upload to storage
        url = storage_service.upload_image(
            file_content=optimized_content,
            filename=file.filename,
            content_type=file.content_type,
            user_id=current_user.id,
            image_type=image_type
        )

        uploaded_images.append(
            ImageUploadResponse(
                url=url,
                width=width,
                height=height,
                file_size=len(optimized_content)
            )
        )

    return MultipleImageUploadResponse(images=uploaded_images)


@router.delete("/image")
async def delete_image(
    url: str,
    current_user: User = Depends(get_current_user)
):
    """
    Delete an uploaded image

    **Query Parameter:**
    - `url`: Full URL of the image to delete

    **Note:** Only images uploaded by the current user can be deleted

    **Returns:** Success message
    """
    # TODO: Verify that the image belongs to the current user
    # For now, we trust the URL contains user_id path

    if f"/{current_user.id}/" not in url:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own images"
        )

    storage_service = StorageService()
    success = storage_service.delete_image(url)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found or already deleted"
        )

    return {"message": "Image deleted successfully", "url": url}
