# coding=utf-8

from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from push_notifications.api.rest_framework import (
    APNSDeviceAuthorizedViewSet, GCMDeviceAuthorizedViewSet
)
from push_notifications.models import APNSDevice, GCMDevice

from . import serializers, exceptions


class CustomAPNSDeviceAuthorizedViewSet(APNSDeviceAuthorizedViewSet):

    def create(self, request, *args, **kwargs):
        """Create."""
        registration_id = request.data['registration_id']
        response = super(CustomAPNSDeviceAuthorizedViewSet, self).create(
            request, *args, **kwargs
        )
        try:
            device = APNSDevice.objects.get(registration_id=registration_id)
            device.user = request.user
            device.save()
        except APNSDevice.DoesNotExist:
            pass

        return response


class CustomGCMDeviceAuthorizedViewSet(GCMDeviceAuthorizedViewSet):

    def create(self, request, *args, **kwargs):
        """Create."""
        registration_id = request.data['registration_id']
        response = super(CustomGCMDeviceAuthorizedViewSet, self).create(
            request, *args, **kwargs
        )
        try:
            device = GCMDevice.objects.get(registration_id=registration_id)
            device.user = request.user
            device.save()
        except APNSDevice.DoesNotExist:
            pass

        return response


class RegistrationView(APIView):

    """Registration."""

    serializer_class = serializers.RegistrationSerializer

    def get_serializer_class(self):
        """Get serializer class."""
        return self.serializer_class

    def post(self, request):
        """POST request handler."""
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except ValidationError as e:
            raise exceptions.BadRequestError(details=str(e))
        return Response(serializer.data, status.HTTP_201_CREATED)


class VerificationView(APIView):

    """Verification."""

    serializer_class = serializers.VerificationSerializer

    def get_serializer_class(self):
        """Get serializer class."""
        return self.serializer_class

    def post(self, request):
        """POST request handler."""
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            raise exceptions.BadRequestError(details=str(e))
        return Response(serializer.data)


class ReverificationView(APIView):

    """Reverification."""

    serializer_class = serializers.ReverificationSerializer

    def get_serializer_class(self):
        """Get serializer class."""
        return self.serializer_class

    def post(self, request):
        """POST request handler."""
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            raise exceptions.BadRequestError(details=str(e))
        return Response(serializer.data)


class RestorePasswordRequestView(APIView):

    """Restore password request."""

    serializer_class = serializers.RestorePasswordRequestSerializer

    def get_serializer_class(self):
        """Get serializer class."""
        return self.serializer_class

    def post(self, request):
        """POST request handler."""
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            raise exceptions.BadRequestError(details=str(e))
        return Response(serializer.data)


class RestorePasswordView(APIView):

    """Restore password."""

    serializer_class = serializers.RestorePasswordSerializer

    def get_serializer_class(self):
        """Get serializer class."""
        return self.serializer_class

    def post(self, request):
        """POST request handler."""
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            raise exceptions.BadRequestError(details=str(e))
        return Response(serializer.data)


class AuthenticationView(APIView):

    """Authentication."""

    serializer_class = serializers.AuthenticationSerializer

    def get_serializer_class(self):
        """Get serializer class."""
        return self.serializer_class

    def post(self, request):
        """POST request handler."""
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            raise exceptions.BadRequestError(details=str(e))
        return Response(serializer.data)


class ProfileView(APIView):

    """Profile."""

    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        """Get serializer class."""
        return self.serializer_class

    def get(self, request):
        """GET request handler."""
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)

    def put(self, request):
        """PUT request handler."""
        serializer = self.serializer_class(
            request.user, data=request.data, partial=True
        )
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except ValidationError as e:
            raise exceptions.BadRequestError(details=str(e))
        return Response(serializer.data)


class ChangePasswordView(APIView):

    """Change password."""

    serializer_class = serializers.ChangePasswordSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        """Get serializer class."""
        return self.serializer_class

    def post(self, request):
        """POST request handler."""
        serializer = self.serializer_class(request.user, data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except ValidationError as e:
            raise exceptions.BadRequestError(details=str(e))
        return Response(serializer.data)
