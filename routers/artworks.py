"""
Artwork router module.

This module defines HTTP endpoints responsible for
handling artwork-related operations (CRUD).
It acts as the API layer between client requests
and the persistence layer.
"""
from email.mime import image
from typing import List
from services.tag_service import process_tags_fast
from fastapi import (APIRouter, Depends, HTTPException, 
                     status, UploadFile, File, Form, UploadFile, Query, Request)
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from models.tag import Tag
from database.database import get_db
from models.artwork import Artwork
from schemas.artwork_schema import ArtworkCreate, ArtworkResponse

import os
import uuid
from PIL import Image
import io
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="/artworks",
    tags=["Artworks"],
)


UPLOAD_DIR = "static/uploads"
MAX_SIZE = (800, 800)  # Max width/height


async def save_resized_image(image: UploadFile, filename: str) -> str:
    contents = await image.read()

    img = Image.open(io.BytesIO(contents))

    # Maintain aspect ratio
    img.thumbnail(MAX_SIZE)

    file_path = os.path.join(UPLOAD_DIR, filename)

    img.save(file_path)

    return filename


@router.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request):
    return templates.TemplateResponse(
        "admin.html",
        {"request": request},
    )


@router.post(
    "/",
    response_model=ArtworkResponse,
    status_code=status.HTTP_201_CREATED,
)


async def create_artwork(
    title: str = Form(...),
    comments: str | None = Form(None),
    tags: str = Form(None),
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

    # Save file to disk
    await save_resized_image(image, unique_filename)
    
    # Save record in database
    db_artwork = Artwork(
        title=title,
        comments=comments,
        tags = await process_tags_fast(db, tags),
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


@router.get("/", response_class=HTMLResponse)
async def gallery(
    request: Request,
    tag: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    # Base query
    query = select(Artwork).order_by(desc(Artwork.id))

    # If tag search is provided
    if tag:
        query = (
            query
            .join(Artwork.tags)
            .where(Tag.name.ilike(f"%{tag.lower()}%"))
        )

    result = await db.execute(query)
    artworks = result.scalars().unique().all()

    return templates.TemplateResponse(
        "gallery.html",
        {
            "request": request,
            "artworks": artworks,
            "tag": tag,
        },
    )


UPLOAD_DIR = "static/uploads"


@router.delete(
    "/{artwork_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_artwork(
    artwork_id: int,
    db: AsyncSession = Depends(get_db),
) -> None:
    """
    Delete an artwork and its associated image file.
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

    # Build file path
    file_path = os.path.join(UPLOAD_DIR, artwork.image_filename)

    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"Error deleting file: {e}")

    # Delete database record
    await db.delete(artwork)
    await db.commit()