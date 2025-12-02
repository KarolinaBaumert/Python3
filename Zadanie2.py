import pytest
from fastapi.testclient import TestClient
from Zadanie1 import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Zadanie1 import Base
from datetime import datetime, timedelta
import jwt

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def client():
    client = TestClient(app)
    yield client


SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(username: str, roles: list,
                        expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)) -> str:
    to_encode = {"sub": username, "roles": roles}
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def test_login_success(client, db_session):
    user_data = {"username": "admin", "password": "secret_password_123"}

    response = client.post("/login", json=user_data)

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["message"] == "Zalogowano pomyślnie"


def test_login_failure(client):
    user_data = {"username": "admin", "password": "wrong_password"}

    response = client.post("/login", json=user_data)

    assert response.status_code == 401
    assert "detail" in response.json()
    assert response.json()["detail"] == "Nieprawidłowy login lub hasło"


def test_create_user_with_admin_role(client, db_session):
    admin_token = create_access_token("admin", ["ROLE_ADMIN"])

    new_user_data = {
        "username": "new_user",
        "password": "new_password",
        "email": "new_user@example.com",
        "roles": ["ROLE_USER"]
    }

    response = client.post(
        "/users",
        json=new_user_data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 201
    assert response.json()["message"] == "Użytkownik został dodany pomyślnie"
    assert response.json()["username"] == "new_user"


def test_create_user_without_admin_role(client, db_session):
    user_token = create_access_token("jan_kowalski", ["ROLE_USER"])

    new_user_data = {
        "username": "new_user_without_admin",
        "password": "new_password",
        "email": "new_user_without_admin@example.com",
        "roles": ["ROLE_USER"]
    }

    response = client.post(
        "/users",
        json=new_user_data,
        headers={"Authorization": f"Bearer {user_token}"}
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Brak uprawnień do wykonania tej akcji"


def test_user_details_success(client, db_session):
    admin_token = create_access_token("admin", ["ROLE_ADMIN"])

    response = client.get(
        "/user_details",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200
    assert response.json()["username"] == "admin"
    assert "ROLE_ADMIN" in response.json()["roles"]


def test_user_details_no_token(client, db_session):
    response = client.get("/user_details")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_user_details_invalid_token(client, db_session):
    response = client.get(
        "/user_details",
        headers={"Authorization": "Bearer invalid_token"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Błędny token"

