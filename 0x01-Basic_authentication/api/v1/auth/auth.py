#!/usr/bin/env python3
"""
define the Auth class for handling
authentication-related functionalities.
"""

from flask import request
from typing import (
    List,
    TypeVar
)


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
        if path is None:
            return True
        elif excluded_paths is None or excluded_paths == []:
            return True
        elif path in excluded_paths:
            return False
        else:
            for i in excluded_paths:
                if i.startswith(path):
                    return False
                if path.startswith(i):
                    return False
                if i[-1] == "*":
                    if path.startswith(i[:-1]):
                        return False
        return True

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
        header = request.headers.get('Authorization')
        if header is None:
            return None
        return header

    def current_user(self, request=None) -> TypeVar('User'):
        """
        placeholder for method to get the current user from the request.
        Args:
            request (flask.Request, optional): The request object.
        Returns:
            User: Always returns None for now, to be implemented in subclasses
        """
        return None
