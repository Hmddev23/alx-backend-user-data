#!/usr/bin/env python3
"""
provide functionalities for hashing passwords
and verifying them using bcrypt.
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    hash a password using bcrypt.
    Args:
        password (str): The password to be hashed.
    Returns:
        bytes: The hashed password.
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    verify a password against its hashed value using bcrypt.
    Args:
        hashed_password (bytes): The hashed password.
        password (str): The plaintext password to verify.
    Returns:
        bool: True if the password matches the hashed password.
    """
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
