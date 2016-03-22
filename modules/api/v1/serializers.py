# coding=utf-8

from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers, exceptions
from rest_framework.authtoken.models import Token

from users.models import Confirmation
from users.tasks import send_confirmation_email, send_restore_password_email


class RegistrationSerializer(serializers.ModelSerializer):

    """Registration serializer."""

    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'name', 'surname', 'password')

    def create(self, data):
        user = get_user_model().objects.create_user(**data)
        confirmation = Confirmation.objects.create(user=user)
        send_confirmation_email(confirmation)
        return user


class UserSerializer(serializers.ModelSerializer):

    """User serializer."""

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'name', 'surname')


class RegistrationConfirmationSerializer(serializers.Serializer):

    """Registration confirmation serializer."""

    USER_NOT_FOUND = _('User not found')
    CODES_NOT_MATCH = _('Codes don\'t match')

    email = serializers.EmailField(write_only=True)
    code = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            user = get_user_model().objects.get(email=data['email'])
        except get_user_model().DoesNotExist:
            raise serializers.ValidationError(self.USER_NOT_FOUND)

        try:
            confirmation = user.confirmations.get(code=data['code'])
        except Confirmation.DoesNotExist:
            raise serializers.ValidationError(self.CODES_NOT_MATCH)

        data['user'] = user
        confirmation.delete()

        return data

    def save(self):
        user = self.validated_data['user']
        user.is_active = True
        user.save()


class ReconfirmationSerializer(serializers.Serializer):

    """Reconfirmation serializer."""

    USER_NOT_FOUND = _('User not found')

    email = serializers.EmailField(write_only=True)

    def validate(self, data):
        try:
            data['user'] = get_user_model().objects.get(email=data['email'])
        except get_user_model().DoesNotExist:
            raise serializers.ValidationError(self.USER_NOT_FOUND)

        return data

    def create(self, data):
        confirmation = Confirmation.objects.create(user=data['user'])
        send_confirmation_email(confirmation)
        return confirmation


class RestorePasswordRequestSerializer(serializers.Serializer):

    """Restore password request serializer."""

    USER_NOT_FOUND = _('User not found')

    email = serializers.EmailField(write_only=True)

    def validate(self, data):
        try:
            data['user'] = get_user_model().objects.get(email=data['email'])
        except get_user_model().DoesNotExist:
            raise serializers.ValidationError(self.USER_NOT_FOUND)

        return data

    def create(self, data):
        confirmation = Confirmation.objects.create(user=data['user'])
        send_restore_password_email(confirmation)
        return confirmation


class RestorePasswordSerializer(serializers.Serializer):

    """Restore password serializer."""

    USER_NOT_FOUND = _('User not found')
    CODES_NOT_MATCH = _('Codes don\'t match')

    email = serializers.EmailField(write_only=True)
    code = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            user = get_user_model().objects.get(email=data['email'])
        except get_user_model().DoesNotExist:
            raise serializers.ValidationError(self.USER_NOT_FOUND)

        try:
            confirmation = user.confirmations.get(code=data['code'])
        except Confirmation.DoesNotExist:
            raise serializers.ValidationError(self.CODES_NOT_MATCH)

        data['user'] = user
        confirmation.delete()

        return data

    def save(self):
        user = self.validated_data['user']

        user.set_password(self.validated_data['password'])
        user.save()


class ChangePasswordSerializer(serializers.ModelSerializer):

    """Change password serializer."""

    PASSWORD_INCORRECT = _('Password incorrect')

    class Meta:
        model = get_user_model()
        fields = ('current_password', 'password')

    current_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate_current_password(self, value):
        if not self.instance.check_password(value):
            raise exceptions.ValidationError(self.PASSWORD_INCORRECT)

    def update(self, instance, data):
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
        try:
            user = get_user_model().objects.get(email=data['email'])
            if not user.check_password(data['password']):
                raise ValueError()
        except (get_user_model().DoesNotExist, ValueError):
            raise exceptions.ValidationError(self.USER_NOT_FOUND)

        if not user.is_active:
            raise exceptions.ValidationError(self.USER_INACTIVE)

        data['token'] = Token.objects.get_or_create(user=user)[0].key
        return data
