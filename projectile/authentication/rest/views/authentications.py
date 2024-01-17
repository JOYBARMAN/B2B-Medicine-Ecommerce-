"""Views for authentication"""

from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status

from authentication.rest.serializers.authentications import (
    RegistrationSerializer,
    LoginSerializer,
    ActivateAccountSerializer,
    ChangePasswordSerializer,
    PasswordResetMailSerializer,
    PasswordResetSerializer,
)
from core.permissions import IsAuthenticated
from common.renderers import ErrorRenderers


class RegistrationView(CreateAPIView):
    serializer_class = RegistrationSerializer
    renderer_classes = [
        ErrorRenderers,
    ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_data = serializer.save()

        return Response(response_data, status=status.HTTP_201_CREATED)


class LoginView(CreateAPIView):
    serializer_class = LoginSerializer
    renderer_classes = [
        ErrorRenderers,
    ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_data = serializer.save()

        return Response(response_data, status=status.HTTP_200_OK)


class ActiveAccountView(CreateAPIView):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = ActivateAccountSerializer
    renderer_classes = [
        ErrorRenderers,
    ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_data = serializer.save()

        return Response(response_data, status=status.HTTP_200_OK)


class ChangePasswordView(CreateAPIView):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = ChangePasswordSerializer
    renderer_classes = [
        ErrorRenderers,
    ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_data = serializer.save()

        return Response(response_data, status=status.HTTP_200_OK)


class PasswordResetMailView(CreateAPIView):
    serializer_class = PasswordResetMailSerializer
    renderer_classes = [
        ErrorRenderers,
    ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_data = serializer.save()

        return Response(response_data, status=status.HTTP_200_OK)


class PasswordResetView(CreateAPIView):
    serializer_class = PasswordResetSerializer
    renderer_classes = [
        ErrorRenderers,
    ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            context={"uid": kwargs.get("uid"), "token": kwargs.get("token")},
        )
        serializer.is_valid(raise_exception=True)
        response_data = serializer.save()

        return Response(response_data, status=status.HTTP_200_OK)
