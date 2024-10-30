import pytest
from httpx import AsyncClient

from app import app


@pytest.mark.asyncio
async def test_create_task():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/tasks/",
            json={"title": "New Task", "description": "Task description"},
        )
    assert response.status_code == 201
    assert response.json() == {
        "message": "Task created",
        "task": {
            "id": 1,
            "title": "New Task",
            "description": "Task description",
            "completed": False,
        },
    }


@pytest.mark.asyncio
async def test_delete_task():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/tasks/",
            json={"title": "New Task", "description": "Task description"},
        )
        response = await client.delete("/tasks/1")
        print(response)
    assert response.status_code == 200
    assert response.json() == {
        "message": "Task createddeleted",
        "task": {
            "id": 1,
            "title": "New Task",
            "description": "Task description",
            "completed": False,
        },
    }
