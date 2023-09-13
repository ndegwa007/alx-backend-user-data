#!/usr/bin/env python3
"""module uses bcrypt to hash password"""
import bcrypt
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """hash a password"""
    byte = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_pass = bcrypt.hashpw(byte, salt)
    return hashed_pass


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register user with hashed password"""
        self.email = email
        check_user = self._db.find_user_by(email=self.email)
        if check_user:
            raise ValueError(f"User {email} already exist")
        else:
            self.password = _hash_password(password)
            self.user = self._db.add_user(
                    email=self.email,
                    hashed_password=self.password)
            return self.user
