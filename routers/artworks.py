"""
Artwork router module.

This module defines HTTP endpoints responsible for
handling artwork-related operations (CRUD).
It acts as the API layer between client requests
and the persistence layer.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_db
from models.artwork import Artwork
from schemas.artwork_schema import ArtworkCreate, ArtworkResponse


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
    artwork: ArtworkCreate,
    db: AsyncSession = Depends(get_db),
) -> ArtworkResponse:
    """
    Create a new artwork record.

    Accepts validated input data via ArtworkCreate schema,
    persists it to the database, and returns the stored record.
    """

    db_artwork = Artwork(
        title=artwork.title,
        comments=artwork.comments,
        image_filename="placeholder.jpg",  # Will be replaced when upload is implemented
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