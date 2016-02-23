# coding=utf-8

from rest_framework import authentication, exceptions

from .exceptions import ForbiddenRequestError

class TokenAuthentication(authentication.TokenAuthentication):

    """Custom token authentication."""

    def authenticate(self, request):
        """Authenticate."""
        try:
            return super(TokenAuthentication, self).authenticate(request)
        except exceptions.AuthenticationFailed:
            raise ForbiddenRequestError()
