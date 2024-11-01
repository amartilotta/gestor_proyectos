from inspect import getmembers
from typing import Any, List, Optional, Tuple

from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from utilities.modules import get_modules_from_import

from api import errors


class ExceptionTemplate(Exception):
    """Base class for exceptions."""

    message: str | None = None
    internal_code: Optional[int] = None
    status_code: int = status.HTTP_409_CONFLICT

    def __init__(self, *args, **kwargs):
        self.errors = []
        args and self.add_error(args)
        kwargs and self.add_error(kwargs)

        super().__init__(*args)

    def add_error(self, error: Any | List[str] | Tuple[str]):
        if not isinstance(error, (list, tuple)):
            self.errors.append(error)
            return self

        for item in error:
            if isinstance(item, (list, tuple)):
                self.add_error(item)
                continue
            self.errors.append(
                str(item) if isinstance(item, Exception) else item
            )
        return self

    def get_errors(self) -> list:
        return self.errors

    @classmethod
    async def handler(
        cls, request: Request, exception: "ExceptionTemplate"
    ) -> JSONResponse:

        message = exception.get_message()
        errors = exception.get_errors()

        return JSONResponse(
            status_code=cls.status_code,
            content=jsonable_encoder(
                {
                    "message": message,
                    "response": errors,
                    "internal_code": cls.internal_code,
                }
            ),
        )

    def get_message(self) -> str:
        if not self.message:
            raise NotImplementedError(
                "You must define a message attribute in the exception class"
            )
        return self.message


def exception_handlers():
    error_class = []

    for module in get_modules_from_import(errors):
        for class_name, resource_class in getmembers(module):
            if not isinstance(resource_class, type) or not hasattr(
                resource_class, "handler"
            ):
                continue

            error_class.append((resource_class, resource_class.handler))
    return error_class
