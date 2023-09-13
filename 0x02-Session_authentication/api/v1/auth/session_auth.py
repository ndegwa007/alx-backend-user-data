#!/usr/bin/env python3
"""module contains a session auth class"""
from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """session auth class"""
    user_id_by_session_id = {}

    def create_session(self, user_id=None) -> str:
        """creates session id for a user_id"""
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str) -> str:
        """returns user_id based on session_id"""
        if session_id is None or not isinstance(session_id, str):
            return None
        user_id = SessionAuth.user_id_by_session_id.get(session_id, None)
        return user_id

    def current_user(self, request=None) -> User:
        """returns user based on a cookie value"""
        self.session_id = self.session_cookie(request)
        self.user_id = self.user_id_for_session_id(self.session_id)
        return User.get(self.user_id)
