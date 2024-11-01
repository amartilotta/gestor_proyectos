from controller.task_controller import TaskController
from fastapi import APIRouter

from schemas.task_schema import TaskOutput

router = APIRouter()


router.add_api_route("/tasks/", TaskController.create_task, methods=["POST"],responses={
    200:{"model":TaskOutput}  # TODO: Make this in all of ones and do the schemas
})
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
