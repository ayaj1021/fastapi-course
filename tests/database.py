from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
import pytest
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.database import get_db, Base
from app.database import Base



# The reason we are creating a separate database url for testing is because
# we don't want to mess up with our development database while testing
# So we create a separate database for testing


# SQLALCHEMY_DATABASE_URL = (
#     "postgresql://postgress:14hs1021@localhost:5432/fastapi_test_db"
# )
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://postgres:14hs1021@localhost:{settings.database_port}/fastapi_test"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Create the database tables

# Base.metadata.create_all(bind=engine)


# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# @app.get("/")
# async def read_root():
#     return {"message": "Hello World"}


# client = TestClient(app)


@pytest.fixture()
def session():
    # Run our code before we run our test
    print("my session fixture ran")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    # Run our code after our test


@pytest.fixture()
def client(session):
    # Run our code before we run our test
    # This is using sqlachemy to create our tables
    # Base.metadata.drop_all(bind=engine)
    # Base.metadata.create_all(bind=engine)

    # This is using alembic to create our tables
    # alembic_cfg = Config("alembic.ini")

    # # Reset and reapply migrations
    # command.downgrade(alembic_cfg, "base")
    # command.upgrade(alembic_cfg, "head")
    def override_get_db():

        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    # Run our code after our test

