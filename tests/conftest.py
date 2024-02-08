
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from database import Base
from deps import get_session
from main import app


@fixture
def client():
    return TestClient(app=app)


@fixture(scope="session")
def engine():
    SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_test_app.db"
    # SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

    return create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )


@fixture(scope="session")
def migrate(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@fixture
def dbsession(engine, migrate):
    """Returns an sqlalchemy session, and after the test tears down everything properly."""
    connection = engine.connect()
    # begin the nested transaction
    transaction = connection.begin()
    # use the connection with the already started transaction
    session = Session(bind=connection)
    app.dependency_overrides[get_session] = lambda: session
    yield session

    session.close()
    # roll back the broader transaction
    transaction.rollback()
    # put back the connection to the connection pool
    connection.close()



def after(*args, **kwargs):
    return datetime.utcnow() + timedelta(*args, **kwargs)


def before(*args, **kwargs):
    return datetime.utcnow() - timedelta(*args, **kwargs)
