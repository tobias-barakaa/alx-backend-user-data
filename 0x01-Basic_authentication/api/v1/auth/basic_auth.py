#!/usr/bin/env python3
""" Oauth module
"""
from flask import request
from typing import List, TypeVar
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ BasicAuth class
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ extract_base64_authorization_header
        """
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if authorization_header[:6] != "Basic ":
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """ decode_base64_authorization_header
        """
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            import base64
            base64_bytes = base64_authorization_header.encode('utf-8')
            sample_string_bytes = base64.b64decode(base64_bytes)
            sample_string = sample_string_bytes.decode('utf-8')
            return sample_string
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """ extract_user_credentials
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if type(decoded_base64_authorization_header) is not str:
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """Return the User instance based on email and password."""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        from models.user import User
        users = User.search({"email": user_email})
        if not users:
            return None
        for user in users:
            return user.is_valid_password(user_pwd):
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieve User instance for a request."""
        if request is None: return None
        auth_header = self.authorization_header(request)
        base64_auth_header = self.extract_base64_authorization_header(auth_header)
        decoded_auth_header = self.decode_base64_authorization_header(
            base64_auth_header)
        user_email, user_pwd = self.extract_user_credentials(decoded_auth_header)
        return self.user_object_from_credentials(user_email, user_pwd)
