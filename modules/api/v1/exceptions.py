# coding=utf-8

from django.utils.translation import ugettext_lazy as _

from rest_framework.exceptions import APIException
from rest_framework import status


class DetailedAPIException(APIException):

    """Detailed API exception."""

    ERROR = 'error'

    def __init__(self, details=None, code=None):
        """Override initialization."""
        self.detail = self.default_detail
        if details:
            self.detail['details'] = details
        if code:
            self.detail['code'] = code


class BadRequestError(DetailedAPIException):

    """Exception for bad requests."""

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {
        'status': DetailedAPIException.ERROR,
        'details': _('Bad request'),
    }


class ConflictRequestError(DetailedAPIException):

    """Exception for conflict requests."""

    status_code = status.HTTP_409_CONFLICT
    default_detail = {
        'status': DetailedAPIException.ERROR,
        'details': _('Conflict request'),
    }


class ForbiddenRequestError(DetailedAPIException):

    """Exception for forbidden requests."""

    status_code = status.HTTP_403_FORBIDDEN
    default_detail = {
        'status': DetailedAPIException.ERROR,
        'details': _('API key not provided or incorrect'),
    }


class NotFoundRequestError(DetailedAPIException):

    """Exception for not found requests."""

    status_code = status.HTTP_404_NOT_FOUND
    default_detail = {
        'status': DetailedAPIException.ERROR,
        'details': _('Not found'),
    }
