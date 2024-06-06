#!/usr/bin/env python3
"""
implement session-based authentication with session expiration.
"""

import os
from datetime import (
    datetime,
    timedelta
)
from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """
    SessionExpAuth class to handle session-based
    authentication with expiration.
    """
    def __init__(self):
        """
        initialize the SessionExpAuth instance.
        """
        try:
            duration = int(os.getenv('SESSION_DURATION'))
        except Exception:
            duration = 0
        self.session_duration = duration

    def create_session(self, user_id=None):
        """
        create a session ID for a given user ID and stores the creation time.
        Args:
            user_id (str): The user ID for which the session is created.
        Returns:
            str: The session ID if user_id is valid, otherwise None.
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        retrieve the user ID associated with a given session ID.
        Args:
            session_id (str): The session ID.
        Returns:
            str: The user ID if session_id is valid and not expired.
        """
        if session_id is None:
            return None
        user_details = self.user_id_by_session_id.get(session_id)
        if user_details is None:
            return None
        if "created_at" not in user_details.keys():
            return None
        if self.session_duration <= 0:
            return user_details.get("user_id")
        created_at = user_details.get("created_at")
        allowed_window = created_at + timedelta(seconds=self.session_duration)
        if allowed_window < datetime.now():
            return None
        return user_details.get("user_id")
