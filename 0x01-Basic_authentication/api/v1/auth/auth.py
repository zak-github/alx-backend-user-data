#!/usr/bin/env python3
"""
Authentication Class
"""
import re
from typing import List, TypeVar

from flask import request


class Auth:
    """Class Authentication of an API"""

    def require_auth(self, path: str, exclude_paths: List[str]) -> bool:
        """
        Require authentication for all paths inclusive

        Return:
            - True if the path is not in the list of strings exclude_paths
        """
        if path is None or exclude_paths is None or exclude_paths == []:
            return True
        path = path + '/' if path[-1] != '/' else path
        for exclude_path in exclude_paths:
            exclude_path = exclude_path.replace('/', '\\/').replace('*', '.*')
            regex = re.compile(exclude_path)
            if regex.search(path):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Return:
            - the value of the header request Authorization or None
        """
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Return:
            - the current user
        """
        return None
