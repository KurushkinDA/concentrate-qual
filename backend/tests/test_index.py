from httpx import AsyncClient, ASGITransport
from app.main import app
import pytest

@pytest.mark.asyncio
async def test_ping():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "hello"}