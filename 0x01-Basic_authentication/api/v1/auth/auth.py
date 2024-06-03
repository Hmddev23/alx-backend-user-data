
#!/usr/bin/env python3
"""
define the Auth class for handling
authentication-related functionalities.
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """
    Auth class to manage the authentication of requests.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        determine if authentication is required for a given path.
        Args:
            path (str): The request path to check.
            excluded_paths (List[str]): A list of unauthenticated paths.
        Returns:
            bool: True if authentication is required, False otherwise.
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path[-1] != "/":
            path += "/"

        return path not in excluded_paths

    def authorization_header(self, request=None) -> str:
        """
        retrieve the value of the Authorization header from the request.
        Args:
            request (flask.Request, optional): The request object.
        Returns:
            str: The value of the Authorization header.
        """
        if request is None:
            return None
        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar("User"):
        """
        placeholder for method to get the current user from the request.
        Args:
            request (flask.Request, optional): The request object.
        Returns:
            User: Always returns None for now, to be implemented in subclasses
        """
        return None