#!/usr/bin/env python3
"""App Module
"""

from flask import Flask, jsonify, request, abort, redirect, url_for
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def welcome() -> str:
    """GET /
    Return:
      - Welcome message
    """
    return jsonify({"message": "Bienvenue"}), 200


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """POST /users
    JSON body:
      - email
      - password
    Return:
      - User object JSON represented
    """
    try:
        email = request.form['email']
        password = request.form['password']
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


def valid_login(email: str, password: str) -> bool:
    """Check if login is valid
    """
    try:
        user = AUTH.find_user_by(email=email)
        return user.is_valid_password(password)
    except Exception:
        return False


@app.route('/sessions', methods=['POST'])
def login() -> str:
    """POST /sessions
    JSON body:
      - email
      - password
    Return:
      - Session ID as JSON
    """
    data = request.form
    email = data.get('email')
    password = data.get('password')
    if Auth.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie('session_id', session_id)
        return response
    else:
        abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
