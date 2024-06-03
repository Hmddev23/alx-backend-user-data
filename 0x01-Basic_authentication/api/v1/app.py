#!/usr/bin/env python3
"""
Route module for the API
"""

import os
from os import getenv
from flask import Flask, jsonify, abort, request, abort
from flask_cors import CORS, cross_origin
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


auth = None
if os.getenv("AUTH_TYPE") == "basic_auth":
    auth = BasicAuth()
elif os.getenv("AUTH_TYPE") == "auth":
    auth = Auth()


@app.before_request
def before_request_func():
    """
    function to be executed before each request.
    Returns:
        None
    """
    if auth is None:
        return
    if not auth.require_auth(request.path, ['/api/v1/status/',
                                            '/api/v1/unauthorized/',
                                            '/api/v1/forbidden/']):
        return
    if auth.authorization_header(request) is None:
        abort(401)
    if auth.current_user(request) is None:
        abort(403)


@app.errorhandler(401)
def unauthorized(error) -> str:
    """
    Error handler for 401 Unauthorized error.
    Args:
        error: The error object
    Returns:
        str: JSON response with error message and status code 401.
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error):
    """
    Error handler for 403 Forbidden error.
    Args:
        error: The error object
    Returns:
        str: JSON response with error message and status code 403.
    """
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(404)
def not_found(error) -> str:
    """
    Error handler for 404 Not Found error.
    Args:
        error: The error object
    Returns:
        str: JSON response with error message and status code 404.
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)