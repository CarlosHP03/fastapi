# from fastapi.testclient import TestClient
# from app.main import app
# from app.config import settings
# from app.database import get_db, Base
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# import pytest


# SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}_test'

# engine = create_engine(SQLALCHEMY_DATABASE_URL)

# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# @pytest.fixture(scope="function")
# def session():
#     Base.metadata.drop_all(bind=engine)
#     Base.metadata.create_all(bind=engine)
    
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally: db.close()

# @pytest.fixture(scope="function")
# def client(session):
#     def override_get_db():
#         try:
#             yield session
#         finally: session.close()

#     app.dependency_overrides[get_db] = override_get_db
#     yield TestClient(app)