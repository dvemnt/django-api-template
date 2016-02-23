# coding=utf-8

from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from users.models import Verification
from users.tasks import send_verification_email, send_restore_password_email

from . import exceptions


class RegistrationSerializer(serializers.ModelSerializer):

    """User serializer."""

    NOT_UNIQUE_EMAIL = _('Email must be unique')

    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'name', 'surname', 'password')

    def create(self, data):
        """Create.

        :param data: `dict` validated data.
        """
        user = get_user_model().objects.create_user(**data)
        verification = Verification.objects.create(user=user)
        send_verification_email(verification)
        return user


class UserSerializer(serializers.ModelSerializer):

    """User serializer."""

    NOT_UNIQUE_EMAIL = _('Email must be unique')

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'name', 'surname')


class VerificationSerializer(serializers.Serializer):

    """Verification serializer."""

    USER_NOT_FOUND = _('User not found')
    CODES_NOT_MATCH = _('Codes don\'t match')

    code = serializers.CharField(write_only=True)

    def validate(self, data):
        """Validate data.

        :param value: `dict` data.
        :returns: `dict` validated data.
        """
        try:
            verification = Verification.objects.get(code=data['code'])
        except Verification.DoesNotExist:
            raise exceptions.NotFoundRequestError(self.USER_NOT_FOUND)

        if verification.code != data['code']:
            raise exceptions.ConflictRequestError(self.CODES_NOT_MATCH)

        verification.user.is_active = True
        verification.user.save()
        verification.delete()

        return data


class ReverificationSerializer(serializers.Serializer):

    """Reverification serializer."""

    USER_NOT_FOUND = _('User not found')

    email = serializers.EmailField(write_only=True)

    def validate(self, data):
        """Validate data.

        :param value: `dict` data.
        :returns: `dict` validated data.
        """
        try:
            user = get_user_model().objects.get(email=data['email'])
        except get_user_model().DoesNotExist:
            raise exceptions.NotFoundRequestError(self.USER_NOT_FOUND)

        verification = Verification.objects.create(user=user)
        send_verification_email(verification)

        return data


class RestorePasswordRequestSerializer(serializers.Serializer):

    """Restore password request serializer."""

    USER_NOT_FOUND = _('User not found')

    email = serializers.EmailField(write_only=True)

    def validate(self, data):
        """Validate data.

        :param value: `dict` data.
        :returns: `dict` validated data.
        """
        try:
            user = get_user_model().objects.get(email=data['email'])
        except get_user_model().DoesNotExist:
            raise exceptions.NotFoundRequestError(self.USER_NOT_FOUND)

        verification = Verification.objects.create(user=user)
        send_restore_password_email(verification)

        return data


class RestorePasswordSerializer(serializers.Serializer):

    """Restore password serializer."""

    USER_NOT_FOUND = _('User not found')
    CODES_NOT_MATCH = _('Codes don\'t match')

    code = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """Validate data.

        :param value: `dict` data.
        :returns: `dict` validated data.
        """
        try:
            verification = Verification.objects.get(code=data['code'])
        except Verification.DoesNotExist:
            raise exceptions.NotFoundRequestError(self.USER_NOT_FOUND)

        if verification.code != data['code']:
            raise exceptions.ConflictRequestError(self.CODES_NOT_MATCH)

        verification.user.set_password(data['password'])
        verification.user.save()
        verification.delete()

        return data


class ChangePasswordSerializer(serializers.ModelSerializer):

    """Change password serializer."""

    PASSWORD_INCORRECT = _('Password incorrect')

    class Meta:
        model = get_user_model()
        fields = ('current_password', 'password')

    current_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate_current_password(self, value):
        """Validate current password.

        :param value: `str` password.
        :returns: `str` validated value.
        """
        if not self.instance.check_password(value):
            raise exceptions.ConflictRequestError(self.PASSWORD_INCORRECT)

    def update(self, instance, data):
        """Update instance.

        :param instance: user instance.
        :param data: `dict` validated data.
        """
        instance.set_password(data['password'])
        instance.save()
        return instance

class AuthenticationSerializer(serializers.Serializer):

    """Authentication serializer."""

    USER_NOT_FOUND = _('User not found')
    USER_INACTIVE = _('User not active')

    token = serializers.CharField(read_only=True)

    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """Validate data.

        :param value: `dict` data.
        :returns: `dict` validated data.
        """
        try:
            user = get_user_model().objects.get(email=data['email'])
            if not user.check_password(data['password']):
                raise ValueError()
        except (get_user_model().DoesNotExist, ValueError):
            raise exceptions.NotFoundRequestError(self.USER_NOT_FOUND)

        if not user.is_active:
            raise exceptions.ForbiddenRequestError(self.USER_INACTIVE)

        data['token'] = Token.objects.get_or_create(user=user)[0].key
        return data
