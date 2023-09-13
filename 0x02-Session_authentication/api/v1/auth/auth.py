#!/usr/bin/env python3
"""module has a class that manages API authentication"""
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """manage routes paths"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns bool check on path"""
        if path is None or excluded_paths == [] or excluded_paths is None:
            return True
        normalized_paths = [p.rstrip('/') for p in excluded_paths]

        if path.rstrip('/') in normalized_paths:
            return False
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """returns the flask request object"""
        if request is None:
            return None
        header_key = 'Authorization'
        if header_key in request.headers:
            header_value = request.headers[header_key]
        else:
            return None
        return header_value

    def current_user(self, request=None) -> TypeVar('User'):
        """auth the curr user"""
        return None

    def session_cookie(self, request=None):
        """return cookie value from a request"""
        if request is None:
            return None
        self.r = request
        cookie = os.getenv('SESSION_NAME')
        return self.r.cookies.get(cookie)
