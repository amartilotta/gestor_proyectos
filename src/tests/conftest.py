from os.path import abspath, dirname, join
from sys import path

path.append(abspath(join(dirname(__file__), "..")))
import pytest
from fastapi.testclient import TestClient
from sqlalchemy_utils import create_database, database_exists
from sqlmodel import SQLModel

# from api.requests_manager import SessionRequestManager
from app import app
from config.settings import ENV, settings
from database.connection import engine


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


# @pytest.fixture
# def session():
#     with Session(engine) as session:
#         yield session


# @pytest.fixture
# def client(session: Session):
#     def get_session_override():
#         return session

#     app.dependency_overrides[get_session] = get_session_override
#     client = TestClient(app)
#     yield client
#     app.dependency_overrides.clear()


def pytest_sessionstart(session):
    """
    Called before any tests are collected or run. It is
    called only once.
    """
    settings.ENVIRONMENT = ENV.TEST
    settings.DATABASE_NAME = settings.DATABASE_NAME + "-test"

    engine_db = engine()
    if not database_exists(engine_db.url):
        create_database(engine_db.url)

    SQLModel.metadata.create_all(bind=engine_db)
    # SessionRequestManager.set_engine_db(engine_db)


def pytest_sessionfinish(session, exitstatus):
    """
    Called after whole test run finished, right before
    returning the exit status to the system.
    """
    # engine_db = SessionRequestManager.get_engine_db()
    engine_db = engine()
    SQLModel.metadata.drop_all(bind=engine_db)
