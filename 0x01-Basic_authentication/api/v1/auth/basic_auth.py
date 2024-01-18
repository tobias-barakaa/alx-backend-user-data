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

    def user_object_from_credentials(self,
                                     user_email: str, user_pwd: str
                                    ) -> TypeVar('User'):
    """Returns the User instance based on the email and password.

    Args:
        user_email (str): The user's email.
        user_pwd (str): The user's password.

    Returns:
        User: The User instance or None if the user is not found or the
        password is invalid.
    """
    # Check if user_email or user_pwd is None or not a string
    if not isinstance(user_email, str) or not isinstance(user_pwd, str):
        return None

    try:
        # Search for the user in the database
        users = User.search(attributes={'email': user_email})
    except Exception:
        return None

    # Return None if there is no user in the database with the given email
    if not users:
        return None

    # Get the first user from the search results
    user = users[0]

    # Return None if the password is invalid
    if not user.is_valid_password(user_pwd):
        return None

    # Return the user instance
    return user

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieve User instance.
        """
        if request is None:
            return None
        auth_header = self.authorization_header(request)
        base64_auth_header = self.extract_base64_authorization_header(
            auth_header)
        decoded_auth_header = self.decode_base64_authorization_header(
            base64_auth_header)
        user_email, user_pwd = self.extract_user_credentials(
            decoded_auth_header)
        return self.user_object_from_credentials(user_email, user_pwd)
