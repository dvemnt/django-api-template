# coding=utf-8

from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from push_notifications.api.rest_framework import (
    APNSDeviceAuthorizedViewSet, GCMDeviceAuthorizedViewSet
)
from push_notifications.models import APNSDevice, GCMDevice

from . import serializers, mixins


class CustomAPNSDeviceAuthorizedViewSet(APNSDeviceAuthorizedViewSet):

    def create(self, request, *args, **kwargs):
        registration_id = request.data['registration_id']
        try:
            APNSDevice.objects.get(registration_id=registration_id)
        except APNSDevice.DoesNotExist:
            response = super(CustomAPNSDeviceAuthorizedViewSet, self).create(
                request, *args, **kwargs
            )

        try:
            device = APNSDevice.objects.get(registration_id=registration_id)
        except APNSDevice.DoesNotExist:
            return response

        device.user = request.user
        device.save()

        return Response(self.serializer_class(device).data)


class CustomGCMDeviceAuthorizedViewSet(GCMDeviceAuthorizedViewSet):

    def create(self, request, *args, **kwargs):
        registration_id = request.data['registration_id']
        try:
            GCMDevice.objects.get(registration_id=registration_id)
        except GCMDevice.DoesNotExist:
            response = super(CustomGCMDeviceAuthorizedViewSet, self).create(
                request, *args, **kwargs
            )

        try:
            device = GCMDevice.objects.get(registration_id=registration_id)
        except GCMDevice.DoesNotExist:
            return response

        device.user = request.user
        device.save()

        return Response(self.serializer_class(device).data)


class RegistrationView(mixins.SerializerViewMixin, APIView):

    """Registration."""

    serializer_class = serializers.RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


class ConfirmationView(mixins.SerializerViewMixin, APIView):

    """Confirmation."""

    serializer_class = serializers.RegistrationConfirmationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ReconfirmationView(mixins.SerializerViewMixin, APIView):

    """Reconfirmation."""

    serializer_class = serializers.ReconfirmationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class RestorePasswordRequestView(mixins.SerializerViewMixin, APIView):

    """Restore password request."""

    serializer_class = serializers.RestorePasswordRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class RestorePasswordView(mixins.SerializerViewMixin, APIView):

    """Restore password."""

    serializer_class = serializers.RestorePasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class AuthenticationView(mixins.SerializerViewMixin, APIView):

    """Authentication."""

    serializer_class = serializers.AuthenticationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class ProfileView(mixins.SerializerViewMixin, APIView):

    """Profile."""

    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = self.serializer_class(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ChangePasswordView(mixins.SerializerViewMixin, APIView):

    """Change password."""

    serializer_class = serializers.ChangePasswordSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
