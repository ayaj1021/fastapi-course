from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
import pytest
from sqlalchemy.orm import sessionmaker
from app.oauth2 import create_access_token
from app.config import settings
from app.database import get_db, Base
from app.database import Base
from app import models


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


@pytest.fixture
def test_user(client):
    user_data = {"email": "joey@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    print(res.json())
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def test_user2(client):
    user_data = {"email": "sam@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    print(res.json())
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": str(test_user["id"])})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client


@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [
        {
            "title": "first title",
            "content": "first content",
            "user_id": test_user["id"],
        },
        {
            "title": "second title",
            "content": "second content",
            "user_id": test_user["id"],
        },
        {
            "title": "third title",
            "content": "third content",
            "user_id": test_user["id"],
        },
        {
            "title": "fourth title",
            "content": "fourth content",
            "user_id": test_user2["id"],
        },
    ]

    def create_post_model(post):
        return models.Post(**post)

    post_models = map(create_post_model, posts_data)
    posts = list(post_models)

    session.add_all(posts)
    # session.add_all(
    #     [
    #         models.Post(
    #             title="first title", content="first content", owner_id=test_user["id"]
    #         ),
    #         models.Post(
    #             title="second title", content="second content", owner_id=test_user["id"]
    #         ),
    #         models.Post(
    #             title="third title", content="third content", owner_id=test_user["id"]
    #         ),
    #     ]
    # )
    session.commit()
    # session.query(models.Post).all()
    posts = session.query(models.Post).all()
    return posts
