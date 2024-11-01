from fastapi import status

from api.errors.error_template import ExceptionTemplate


class TaskNotFoundError(ExceptionTemplate):
    """Raised when a Task is not found in a model."""

    internal_code = 4005
    message = "Task not found in database"
    status_code = status.HTTP_404_NOT_FOUND
