#!/usr/bin/env python3
"""
define a User model using SQLAlchemy's ORM system.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    User class represents a user in the system.
    Attributes:
        id (int): The primary key for the user.
        email (str): The email address of the user.
        hashed_password (str): The hashed password for the user.
        session_id (str): An optional session ID for the user.
        reset_token (str): An optional reset token for the user.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
