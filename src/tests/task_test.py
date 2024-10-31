from fastapi import status
from fastapi.testclient import TestClient


class TestTaskApi:
    """Task API Controller - Endpoints"""

    def test_post_create_task(self, client: TestClient) -> None:
        response = client.post(
            "/tasks/",
            json={"title": "New Task", "description": "Task description"},
        )

        assert response.status_code == status.HTTP_201_CREATED

        assert response.json() == {
            "message": "Task created",
            "task": {
                "id": 1,
                "title": "New Task",
                "description": "Task description",
                "completed": False,
            },
        }

    def test_get_all_task(self, client: TestClient) -> None:
        response = client.get("/tasks/")

        assert response.status_code == status.HTTP_200_OK

        assert response.json() == {
            "message": "Tasks",
            "tasks": [
                {
                    "id": 1,
                    "title": "New Task",
                    "description": "Task description",
                    "completed": False,
                },
            ],
        }

    def test_get_task_by_id(self, client: TestClient) -> None:
        response = client.get("/tasks/1")

        assert response.status_code == status.HTTP_200_OK

        assert response.json() == {
            "message": "Task",
            "task": {
                "id": 1,
                "title": "New Task",
                "description": "Task description",
                "completed": False,
            },
        }

    def test_update_task_by_id(self, client: TestClient) -> None:
        response = client.put(
            "/tasks/1",
            json={"description": "updated description", "completed": True},
        )

        assert response.status_code == status.HTTP_200_OK

        assert response.json() == {
            "message": "Task updated",
            "task": {
                "id": 1,
                "title": "New Task",
                "description": "updated description",
                "completed": True,
            },
        }

    def test_delete_task_by_id(self, client: TestClient) -> None:
        response = client.delete("/tasks/1")

        assert response.status_code == status.HTTP_200_OK

        assert response.json() == {
            "message": "Task deleted successfully",
            "task": {
                "id": 1,
                "title": "New Task",
                "description": "updated description",
                "completed": True,
            },
        }
