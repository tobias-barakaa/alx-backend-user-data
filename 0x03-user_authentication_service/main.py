#!/usr/bin/env python3
"""App Module
"""
import requests

def register_user(email: str, password: str) -> None:
    """Register user
    """
    url = "http://your-web-server-base-url"
    data = {"email": email, "password": password}
    response = requests.post(url + "/users", data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}
    
def log_in_wrong_password(email: str, password: str) -> None:
    """Log in with wrong password
    """
    url = "http://your-web-server-base-url"
    data = {"email": email, "password": password}
    response = requests.post(url + "/sessions", data=data)
    assert response.status_code == 401
    assert response.json() == {"message": "wrong password"}

def profile_unlogged() -> None:
    """Profile of unlogged user
    """
    url = "http://your-web-server-base-url"
    response = requests.get(url + "/profile")
    assert response.status_code == 403
    assert response.json() == {"message": "Missing auth token"}

def log_in(email: str, password: str) -> str:
    """Log in
    """
    url = "http://your-web-server-base-url"
    data = {"email": email, "password": password}
    response = requests.post(url + "/sessions", data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "logged in"}
    session_id = response.cookies.get("session_id")
    assert session_id is not None
    return session_id

def profile_logged(session_id: str) -> None:
    """Profile of logged user
    """
    url = "http://your-web-server-base-url"
    response = requests.get(url + "/profile", cookies={"session_id": session_id})
    assert response.status_code == 200
    assert response.json() == {"email": email}

def log_out(session_id: str) -> None:
    """Log out
    """
    url = "http://your-web-server-base-url"
    response = requests.delete(url + "/sessions", cookies={"session_id": session_id})
    assert response.status_code == 200
    assert response.json() == {}
    session_id = response.cookies.get("session_id")
    assert session_id is None

def reset_password_token(email: str) -> str:
    """Reset password token
    """
    url = "http://your-web-server-base-url"
    data = {"email": email}
    response = requests.post(url + "/reset_password", data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Reset password sent"}
    reset_token = response.json()["reset_token"]
    assert reset_token is not None
    return reset_token

def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update password
    """
    url = "http://your-web-server-base-url"
    data = {"email": email, "reset_token": reset_token, "new_password": new_password}
    response = requests.put(url + "/reset_password", data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}
