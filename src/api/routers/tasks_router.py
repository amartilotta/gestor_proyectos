from controller.task_controller import TaskController
from fastapi import APIRouter

from tools.custom_logger import Logger

router = APIRouter()

logger = Logger("app_log", "app_folder", severity="info")


router.add_api_route("/tasks/", TaskController.create_task, methods=["POST"])
router.add_api_route("/tasks/", TaskController.get_task, methods=["GET"])
router.add_api_route(
    "/tasks/{id}", TaskController.get_task_by_id, methods=["GET"]
)
router.add_api_route(
    "/tasks/{id}", TaskController.updated_task, methods=["PUT"]
)
router.add_api_route(
    "/tasks/{id}", TaskController.delete_task_by_id, methods=["DELETE"]
)
