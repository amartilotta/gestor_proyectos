from argparse import ArgumentParser

from fastapi import FastAPI
from uvicorn import run as uvicorn_run

from config.settings import settings


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
    )


def start_application():
    app = FastAPI(
        title=settings.PROJECT_NAME.replace("-", " ").title(),
        description=settings.PROJECT_DESCRIPTION,
        version=settings.PROJECT_VERSION,
        root_path=settings.ROOT_PATH,
        debug=settings.DEBUG_MODE,
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

    return parser.parse_args()


if __name__ == "__main__":
    args = define_args()

    if args.command == "runserver":
        run_server()
