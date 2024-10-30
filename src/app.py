from fastapi.responses import JSONResponse

from api.tasks_router import router as tasks_router

# from api.middlewares import AuthMiddleware, SessionMiddleware
# from api.v1.error_handler import exception_handlers, global_exception_handler
# from api.v1.router import base_api as router_v1
# from api.v1.router import legacy_core, storage
from manage import start_application

app = start_application()

# app.add_middleware(
#     SessionMiddleware,
#     handler=global_exception_handler if not settings.DEBUG_MODE else None,
# )
# app.add_middleware(AuthenticationMiddleware, backend=AuthMiddleware())

# for exception_type, handler in exception_handlers:
#     app.exception_handler(exception_type)(handler)

app.include_router(tasks_router)


@app.get("/health", tags=["Health Check"])
async def health():
    return JSONResponse(
        {
            "message": f"Service {app.title} is up and running",
            "response": f"Active version: {app.version}",
            "models_name": None,
            "pagination": None,
            "internal_code": 2000,
        }
    )
