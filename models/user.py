#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import hashlib


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship(
                "Place", backref="user", cascade='all, delete, delete-orphan'
                )
        reviews = relationship(
                "Review", backref="user", cascade='all, delete, delete-orphan'
                )
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

        if 'password' in kwargs:
            self.set_password(kwargs['password'])

    def set_password(self, password):
        """Hashes the password using MD5"""
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        self.password = hashed_password
