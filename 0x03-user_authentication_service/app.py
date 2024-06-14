#!/usr/bin/env python3
"""
This is a Flask web application for handling user authentication.
"""

from auth import Auth
from flask import Flask, jsonify, request, make_response
from flask import abort, Response, redirect

app = Flask(__name__)
AUTH = Auth()


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> Response:
    """
    POST /sessions
    Log in a user by creating a session ID cookie.
    Request form data:
    - email: User's email address
    - password: User's password
    Returns:
    - 200 OK with a JSON message if login is successful
    - 401 Unauthorized if login fails
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if AUTH.valid_login(email, password):
        jsoni = jsonify({"email": email, "message": "logged in"}), 200
        response = make_response(jsoni)
        response.set_cookie("session_id", AUTH.create_session(email))
        return response

    abort(401)


@app.route("/users", methods=["POST"])
def users() -> Response:
    """
    POST /users
    Register a new user.
    Request form data:
    - email: User's email address
    - password: User's password
    Returns:
    - 200 OK with a JSON message if registration is successful
    - 400 Bad Request if the email is already registered
    """
    email = request.form["email"]
    password = request.form["password"]
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/", methods=["GET"])
def welcome() -> Response:
    """
    GET /
    Welcome message.
    Returns:
    - 200 OK with a JSON welcome message
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> Response:
    """
    DELETE /sessions
    Log out a user by destroying their session.
    Requires:
    - session_id cookie
    Returns:
    - 302 Found redirect to the root URL if logout is successful
    - 403 Forbidden if session ID is invalid
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> Response:
    """
    GET /profile
    Get the profile of the logged-in user.
    Requires:
    - session_id cookie
    Returns:
    - 200 OK with the user's email in JSON if session ID is valid
    - 403 Forbidden if session ID is invalid
    """
    session_id = request.cookies.get("session_id")

    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)

    return jsonify({"email": user.email}), 200


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """
    POST /reset_password
    Request a password reset token.
    Request form data:
    - email: User's email address
    Returns:
    - 200 OK with the email and reset token in JSON if the email is valid
    - 403 Forbidden if the email is invalid
    """
    email = request.form.get("email")

    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "reset_token": reset_token}), 200


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """
    PUT /reset_password
    Update the user's password using the reset token.
    Request form data:
    - email: User's email address
    - reset_token: Password reset token
    - new_password: New password
    Returns:
    - 200 OK with a JSON message if the password is successfully updated
    - 403 Forbidden if the reset token is invalid
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "message": "Password updated"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
