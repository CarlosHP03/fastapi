from fastapi.testclient import TestClient
from app.main import app
from app import schemas
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: db.close()


client = TestClient(app)

def test_root():
    res = client.get("/")

    assert res.status_code == 200
    assert res.json().get('message') == 'Welcome to my API'

def test_create_user():
    res = client.post("/users", json={"email": "car@gmail.com", "password": "123"})
    new_user = schemas.UserOut(**res.json())
    assert res.status_code == 201
    assert new_user.email == "car@gmail.com"