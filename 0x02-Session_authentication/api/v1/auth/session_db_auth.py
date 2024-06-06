#!/usr/bin/env python3
"""
implement session-based authentication
with session data stored in a database.
"""

from models.user_session import UserSession
from .session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """
    SessionDBAuth class to handle session-based authentication
    with session data stored in a database.
    """

    def create_session(self, user_id=None):
        """
        create a session ID for a given user ID and stores the session.
        Args:
            user_id (str): The user ID for which the session is created.
        Returns:
            str: The session ID if user_id is valid, otherwise None.
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        kw = {
            "user_id": user_id,
            "session_id": session_id
        }
        user = UserSession(**kw)
        user.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        retrieve the user ID associated with a given session ID.
        Args:
            session_id (str): The session ID.
        Returns:
            str: The user ID if session_id is found in the database.
        """
        user_id = UserSession.search({"session_id": session_id})
        if user_id:
            return user_id
        return None

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
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_session = UserSession.search({"session_id": session_id})
        if user_session:
            user_session[0].remove()
            return True
        return False
