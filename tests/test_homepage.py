import pytest


@pytest.mark.asyncio
async def test_homepage_loads(client):
    response = await client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


@pytest.mark.asyncio
async def test_homepage_tag_filter(client):
    response = await client.get("/?tag=oil")
    assert response.status_code == 200