import pytest
from httpx import AsyncClient
import io


@pytest.mark.asyncio
async def test_create_artwork_success(client: AsyncClient):
    # Create a simple in-memory image for testing
    from PIL import Image
    img = Image.new("RGB", (100, 100))
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="JPEG")
    img_bytes.seek(0) 

    response = await client.post(
        "/artworks/",
        data={
            "title": "Test Artwork",
            "comments": "Test comment",
            "tags": "oil,abstract",
        },
        files={"image": ("test.jpg", img_bytes, "image/jpeg")},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Artwork"
    assert len(data["tags"]) == 2


@pytest.mark.asyncio
async def test_create_artwork_invalid_file(client: AsyncClient):
    response = await client.post(
        "/artworks/",
        data={"title": "Bad", "tags": "bad"},
        files={"image": ("bad.txt", b"text", "text/plain")},
    )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_list_artworks(client: AsyncClient):
    response = await client.get("/artworks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_delete_artwork(client: AsyncClient):
    # Create artwork first
    from PIL import Image
    img = Image.new("RGB", (100, 100))
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="JPEG")
    img_bytes.seek(0) 

    create = await client.post(
        "/artworks/",
        data={
            "title": "Test Artwork",
            "comments": "Test comment",
            "tags": "oil,abstract",
        },
        files={"image": ("test.jpg", img_bytes, "image/jpeg")},
    )

    artwork_id = create.json()["id"]

    delete = await client.delete(f"/artworks/{artwork_id}")
    assert delete.status_code == 204

    delete_again = await client.delete(f"/artworks/{artwork_id}")
    assert delete_again.status_code == 404