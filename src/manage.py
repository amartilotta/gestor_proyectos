from argparse import ArgumentParser

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run as uvicorn_run

# from api.utilities.modules import get_modules_from_import
from config.settings import settings
from tools.custom_logger import Logger


def run_server():
    if settings.DEBUG_MODE:
        import debugpy

        debugpy.listen((settings.HOST, settings.DEBUG_PORT))
        print(
            "\n\n ⏳ VS Code debugger can now be attached, press F5 in VS Code ⏳ \n\n"
        )

    uvicorn_run(
        "app:app",
        host=settings.HOST,
        port=settings.APP_PORT,
        log_level="info",
        reload=settings.DEBUG_MODE,
        workers=1,
        log_config=Logger.uvicorn_log_config(),
    )


def start_application():
    app = FastAPI(
        title=settings.PROJECT_NAME.replace("-", " ").title(),
        description=settings.PROJECT_DESCRIPTION,
        version=settings.PROJECT_VERSION,
        root_path=settings.ROOT_PATH,
        debug=settings.DEBUG_MODE,
        # swagger_ui_init_oauth={
        #     "clientId": settings.SSO_CLIENT_ID,
        #     "clientSecret": settings.SSO_CLIENT_SECRET,
        # },
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGIN,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=settings.CORS_HEADER,
    )

    return app


def define_args():
    parser = ArgumentParser(
        description="Run the FastAPI application or a specific a seeder"
    )
    parser.add_argument(
        "command",
        choices=["runserver", "runseeder"],
        help="Command to run",
    )
    # parser.add_argument(
    #     "job_name",
    #     nargs="?",
    #     help="Name of the job to run (if command is 'seeders')",
    # )
    # parser.add_argument(
    #     "function_name",
    #     nargs="?",
    #     help="Optional - Name of the function to run (if command is 'seeders')",
    #     default=None,
    # )

    return parser.parse_args()


if __name__ == "__main__":
    args = define_args()

    if args.command == "runserver":
        run_server()
    # elif args.command == "runseeder":
    #     import database.seeders as seeders

    #     for module in get_modules_from_import(seeders):
    #         file = args.job_name
    #         function = args.function_name or "run"
    #         module_name = module.__name__.split(".")[-1]

    #         if file and file != module_name:
    #             continue
    #         if not hasattr(module, function):
    #             raise SystemExit(f"'{function}' not found in '{module_name}'")
    #         print(f"- Running '{module_name}' with function '{function}'...")
    #         getattr(module, function)()
