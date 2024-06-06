#!/usr/bin/env python3
"""
implement session-based authentication.
"""

import base64
from uuid import uuid4
from typing import TypeVar
from .auth import Auth
from models.user import User


class SessionAuth(Auth):
    """
    SessionAuth class to handle session-based authentication.
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        create a session ID for a given user ID.
        Args:
            user_id (str): The user ID for which the session is created.
        Returns:
            str: The session ID if user_id is valid, otherwise None.
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        id = uuid4()
        self.user_id_by_session_id[str(id)] = user_id
        return str(id)

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        retrieve the user ID associated with a given session ID.
        Args:
            session_id (str): The session ID.
        Returns:
            str: The user ID if session_id is valid, otherwise None.
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        retrieve the current user based on the session cookie.
        Args:
            request: The request object containing the session cookie.
        Returns:
            User: The User object if a valid session is found, otherwise None.
        """
        session_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_cookie)
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        """
        destroy the session associated with the request.
        Args:
            request: The request object containing the session cookie.
        Returns:
            bool: True if the session was successfully destroyed.
        """
        if request is None:
            return False
        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return False
        user_id = self.user_id_for_session_id(session_cookie)
        if user_id is None:
            return False
        del self.user_id_by_session_id[session_cookie]
        return True
