# Third-party imports
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# Local imports
from app.models.base import Base
from app.dependencies.session import get_db
from app.main import app


@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="session")
def SessionLocal(db_engine):
    return sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=db_engine
    )

@pytest.fixture(scope="function")
def db_session(db_engine, SessionLocal):
    connection = db_engine.connect()
    trans = connection.begin()
    session = SessionLocal(bind=connection)
    yield session
    session.close()
    trans.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
