from ast import literal_eval
from enum import Enum
from functools import lru_cache
from os import environ, getcwd
from typing import List

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

project_root = getcwd()
load_dotenv(f"{project_root}/.env")
load_dotenv("/etc/metadata")


class ENV(str, Enum):
    DEV = "dev"
    TEST = "test"
    QA = "qa"
    STG = "stg"
    PROD = "prod"


class Settings(BaseSettings):
    # General
    HOST: str = "0.0.0.0"
    APP_PORT: int = 8400
    DEBUG_PORT: int = 8401
    DEBUG_MODE: bool = bool(environ.get("DEBUG", False))
    ENVIRONMENT: ENV = ENV.DEV
    ROOT_PATH: str = ""

    # CORS Middleware
    CORS_ORIGIN: List[str] = literal_eval(environ.get("CORS_ORIGINS", '["*"]'))
    CORS_HEADER: List[str] = literal_eval(environ.get("CORS_HEADERS", '["*"]'))

    # Project
    PROJECT_NAME: str = "project-manager"
    PROJECT_VERSION: str = "not-found"
    PROJECT_DESCRIPTION: str = ""

    # Database
    DATABASE_HOST: str = "postgres-project-manager"
    DATABASE_PORT: int = 5432
    DATABASE_NAME: str = "project_manager"
    DATABASE_USER: str = "postgres"
    DATABASE_PASSWORD: str = "postgres"
    DABATABASE_ECHO: bool = False


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
