from urllib.parse import quote

from sqlalchemy.engine.base import Engine
from sqlmodel import Session, create_engine

from config.settings import settings


def database_url() -> str:
    DATABASE_DOMAIN = settings.DATABASE_HOST + (
        f":{settings.DATABASE_PORT}" if settings.DATABASE_PORT else ""
    )
    encoded_password = quote(settings.DATABASE_PASSWORD.replace("%", "%%"))

    return f"postgresql://{settings.DATABASE_USER}:{encoded_password}@{DATABASE_DOMAIN}/{settings.DATABASE_NAME}"


def engine() -> Engine:
    DATABASE_URL = database_url()
    return create_engine(DATABASE_URL, echo=bool(settings.DABATABASE_ECHO))


def get_session():
    with Session(engine()) as session:
        yield session
