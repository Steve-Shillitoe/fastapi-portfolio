"""
Artwork router module.

This module defines HTTP endpoints responsible for
handling artwork-related operations (CRUD).
It acts as the API layer between client requests
and the persistence layer.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_db
from models.artwork import Artwork
from schemas.artwork_schema import ArtworkCreate, ArtworkResponse

import os
import uuid

UPLOAD_DIR = "static/uploads"

router = APIRouter(
    prefix="/artworks",
    tags=["Artworks"],
)


@router.post(
    "/",
    response_model=ArtworkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_artwork(
    title: str = Form(...),
    comments: str | None = Form(None),
    image: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
) -> ArtworkResponse:
    """
    Create a new artwork with image upload.
    """

    # Validate file type
    if image.content_type not in ["image/jpeg", "image/png", "image/webp"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid image type. Only JPEG, PNG, WEBP allowed.",
        )

    # Generate safe unique filename to prevent filename collisions and ensure security
    file_extension = image.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"

    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    # Save file to disk
    with open(file_path, "wb") as buffer:
        content = await image.read()
        buffer.write(content)

    # Save record in database
    db_artwork = Artwork(
        title=title,
        comments=comments,
        image_filename=unique_filename,
    )

    db.add(db_artwork)
    await db.commit()
    await db.refresh(db_artwork)

    return db_artwork


@router.get(
    "/",
    response_model=List[ArtworkResponse],
)
async def list_artworks(
    db: AsyncSession = Depends(get_db),
) -> List[ArtworkResponse]:
    """
    Retrieve all artworks from the database.
    """

    result = await db.execute(select(Artwork))
    artworks = result.scalars().all()

    return artworks


@router.get(
    "/{artwork_id}",
    response_model=ArtworkResponse,
)
async def get_artwork(
    artwork_id: int,
    db: AsyncSession = Depends(get_db),
) -> ArtworkResponse:
    """
    Retrieve a single artwork by its ID.
    """

    result = await db.execute(
        select(Artwork).where(Artwork.id == artwork_id)
    )
    artwork = result.scalars().first()

    if artwork is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artwork not found",
        )

    return artwork


@router.delete(
    "/{artwork_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_artwork(
    artwork_id: int,
    db: AsyncSession = Depends(get_db),
) -> None:
    """
    Delete an artwork by ID.
    """

    result = await db.execute(
        select(Artwork).where(Artwork.id == artwork_id)
    )
    artwork = result.scalars().first()

    if artwork is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artwork not found",
        )

    await db.delete(artwork)
    await db.commit()