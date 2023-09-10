#!/usr/bin/env python3
"""a basic auth class"""
from api.v1.auth.auth import Auth
from typing import Union, TypeVar
import base64
from models.user import User


class BasicAuth(Auth):
    """ basic authorization """
    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> Union[str, None]:
        """return Base64 part of the Authorization header"""
        basic_len = len('Basic ')
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if authorization_header.startswith('Basic '):
            return authorization_header[basic_len:]

        return None

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> Union[str, None]:
        """decode value of a base64 string"""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_string = base64.b64decode(base64_authorization_header)
            return decoded_string.decode('utf-8')
        except base64.binascii.Error:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> (str, str):
        """returns user and password from Base64 decoded value"""
        result = (None, None)
        if decoded_base64_authorization_header is None:
            return result
        if not isinstance(decoded_base64_authorization_header, str):
            return result
        if ":" not in decoded_base64_authorization_header:
            return result
        decoded_64 = decoded_base64_authorization_header
        if (decoded_64 and isinstance(decoded_64, str)) and ":" in decoded_64:
            res = decoded_64.split(':', 1)
            return (res[0], res[1])
        return result

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """validate user_email and password from user instance"""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({"email": user_email})
            if not users or users == []:
                return None
            for u in users:
                if u.is_valid_password(user_pwd):
                    return u
            return u
        except Exception as err:
            return err

    def current_user(self, request=None) -> TypeVar('User'):
        """check user credentials and validate"""
        auth_header = self.authorization_header(request)
        if auth_header is not None:
            token = self.extract_base64_authorization_header(auth_header)
            if token is not None:
                user_detail = self.decode_base64_authorization_header(token)
                if user_detail is not None:
                    user_email, user_pwd = self.extract_user_credentials(
                        user_detail)
                    if user_email is not None or user_pwd is not None:
                        user = self.user_object_from_credentials(
                            user_email, user_pwd)
                        return user
