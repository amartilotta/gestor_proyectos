from fastapi.responses import JSONResponse

from api.errors.error_template import exception_handlers
from api.routers.tasks_router import router as tasks_router
from manage import start_application

app = start_application()


for exception_type, handler in exception_handlers():
    app.exception_handler(exception_type)(handler)

app.include_router(tasks_router)


@app.get("/health", tags=["Health Check"])
async def health():
    return JSONResponse(
        {
            "message": f"Service {app.title} is up and running",
            "response": f"Active version: {app.version}",
            "internal_code": 2000,
        }
    )
