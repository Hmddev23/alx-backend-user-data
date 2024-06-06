#!/usr/bin/env python3
"""
define the UserSession class, which inherits from the Base class.
"""

from models.base import Base


class UserSession(Base):
    """
    UserSession class for handling user session management.
    Attributes:
        user_id (str): Unique identifier for the user.
        session_id (str): Unique identifier for the session.
    """

    def __init__(self, *args: list, **kwargs: dict):
        """
        initialize a new UserSession instance.
        Args:
            *args (list): Additional arguments to be passed to the Base class.
            **kwargs (dict): Keyword arguments for user_id and session_id.
        Keyword Args:
            user_id (str): Unique identifier for the user.
            session_id (str): Unique identifier for the session.
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
