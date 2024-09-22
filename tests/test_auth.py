from sqlalchemy.orm import Session
from app.crud import get_user_by_email
from app.tests.util import random_email, random_lower_string
from app.tests.user import create_random_user


def test_create_user(test_client, db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    
    data = {"email": email, "password": password}
    response = test_client.post("/users", json=data)
    
    assert response.status_code == 200  
    created_user = response.json()
    db_user = get_user_by_email(db, email=email)
    
    assert db_user.email == email  
    assert db_user.is_active is True  

def test_get_access_token(test_client, db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user = create_random_user(db, email=email, password=password)
    data = {"username": user.email, "password": password}
    r = test_client.post("/token", data=data)
    tokens = r.json()
    assert r.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]

def test_use_access_token(test_client, db: Session, user_token_headers: tuple) -> None:
    user, headers = user_token_headers
    r = test_client.get("/users/me", headers=headers)
    result = r.json()
    assert r.status_code == 200
    assert "email" in result

def test_login_invalid_credentials(test_client) -> None:
    data = {"username": "invalid@example.com", "password": "wrongpassword"}
    r = test_client.post("/token", data=data)
    assert r.status_code == 401
    assert "Incorrect username or password" in r.json()["detail"]
