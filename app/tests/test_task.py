from httpx import AsyncClient
from app.main import app
import pytest

@pytest.mark.asyncio
async def test_create_task():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/tasks/", json={"title": "New Task", "description": "Task description"})
    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "title": "New Task",
        "description": "Task description",
        "completed": False
    }
