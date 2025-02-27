from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from app import models


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally: db.close()

@pytest.fixture(scope="function")
def client(session):
    def override_get_db():
        try:
            yield session
        finally: session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture
def test_user(client):
    user_data = {"email": "car@gmail.com",
                 "password": "123"}
    
    res = client.post("/users/", json=user_data)

    new_user = res.json()
    new_user['password'] = user_data['password']

    assert res.status_code == 201

    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email": "lucy@gmail.com",
                 "password": "123"}
    
    res = client.post("/users/", json=user_data)

    new_user = res.json()
    new_user['password'] = user_data['password']

    assert res.status_code == 201

    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client

@pytest.fixture
def test_posts(test_user, test_user2, session):
    posts_data = [{
    "title": "France",
    "content": "Je mange un croissant",
    "user_id": test_user['id']
    }, {
    "title": "Barcelona",
    "content": "Viendo al Barca golear",
    "user_id": test_user['id']
    }, {
    "title": "Lausanne",
    "content": "C'est la vie",
    "user_id": test_user['id']
    },
    {
    "title": "Geneve",
    "content": "Je mange un eclair",
    "user_id": test_user2['id']
    }]

    def creat_post_model(post):
        return models.Post(**post)
    
    post_map = map(creat_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)
    session.commit()
    posts = session.query(models.Post).all()

    return posts