import logging
from logging.handlers import TimedRotatingFileHandler
from os import makedirs, umask
from pathlib import Path
from typing import Literal

Severities = Literal[
    "critical", "fatal", "error", "warn", "warning", "info", "debug", "notset"
]


class Logger(logging.Logger):
    """
    Custom logger class to create log files with different severity levels.
    Example:
    ```
        from tools.custom_logger import Logger
        logger = Logger("filename", "optional_folder")
        logger.info("This is an info message")
        logger.error("This is an error message")
    ```

    """

    base_folder = "/tmp/logs"

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance._initialize(*args, **kwargs)
        return instance._logger

    def _initialize(
        self,
        logfile: str,
        directory_to_export: str = "",
        severity: Severities = "debug",
    ):
        assert (
            logfile != "access" and " " not in logfile
        ), "Logfile name cannot have spaces or be 'access'"

        assert (
            " " not in directory_to_export
        ), "Directory name cannot have spaces"

        self.folder = f"{self.base_folder}/{directory_to_export.strip('/')}"
        self.directory = f"{self.folder.rstrip('/')}/{logfile}.log"
        umask(0o000)
        Path(self.folder).mkdir(parents=True, exist_ok=True)

        log_name = (
            f"{directory_to_export}_{logfile}"
            if directory_to_export
            else f"{self.__class__.__name__}_{logfile}"
        )
        logger = logging.getLogger(log_name)
        file_handler = TimedRotatingFileHandler(
            self.directory, when="W0", interval=1, backupCount=1
        )

        logger.setLevel(getattr(logging, severity.upper()))
        if logger.handlers:
            logger.handlers = []

        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(filename)s] - Line: %(lineno)d : %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(formatter)
        file_handler.namer = (
            lambda name: self.directory
        )  # remove the backupCount

        logger.addHandler(file_handler)
        self._logger = logger

    @classmethod
    def uvicorn_log_config(cls):
        from uvicorn.config import LOGGING_CONFIG

        umask(0o000)
        makedirs(cls.base_folder, exist_ok=True)
        LOGGING_CONFIG["formatters"]["logfile"] = {
            "format": "[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }

        LOGGING_CONFIG["handlers"]["logfile"] = {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "logfile",
            "filename": f"{cls.base_folder}/access.log",
        }

        LOGGING_CONFIG["loggers"]["uvicorn"]["handlers"].append("logfile")
        LOGGING_CONFIG["loggers"]["uvicorn.access"]["handlers"].append(
            "logfile"
        )

        return LOGGING_CONFIG
