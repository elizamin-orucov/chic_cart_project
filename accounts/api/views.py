from rest_framework import generics
from django.utils.encoding import smart_str
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import (
    LoginSerializer, RegisterSerializer, ActivationSerializer, ResetPasswordSerializer,
    ResetPasswordCompleteSerializer, PasswordChangeSerializer, UpdateUserProfileSerializer,
    ResetPasswordCheckSerializer, DeleteAccountSerializer, AccountDeleteCheckSerializer,
)


User = get_user_model()


class LoginView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class ActivationView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ActivationSerializer
    lookup_field = "uuid"

    def get_object(self):
        uuid = self.kwargs.get(self.lookup_field)
        id_ = smart_str(urlsafe_base64_decode(uuid))
        return User.objects.get(id=id_)

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, instance=self.get_object())
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, instance=self.get_object())
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ResetPasswordView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = ResetPasswordSerializer


class ResetPasswordCheckView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ResetPasswordCheckSerializer
    lookup_field = "uuid"

    def get_object(self):
        uuid = self.kwargs.get("uuid")
        id_ = smart_str(urlsafe_base64_decode(uuid))
        return User.objects.get(id=id_)


class ResetPasswordCompleteView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ResetPasswordCompleteSerializer
    lookup_field = "uuid"

    def get_object(self):
        uuid = self.kwargs.get(self.lookup_field)
        id_ = smart_str(urlsafe_base64_decode(uuid))
        user = User.objects.get(id=id_)
        return user

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, instance=self.get_object())
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class PasswordChangeView(generics.UpdateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = PasswordChangeSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        return self.request.user

    def put(self, *args, **kwargs):
        user = self.get_object()
        serializer = self.serializer_class(data=self.request.data, context={"user": self.get_object()})
        serializer.is_valid(raise_exception=True)

        user.set_password(serializer.validated_data.get('password'))

        user.save()

        token_data = {"email": user.email}

        token = RefreshToken.for_user(user)
        token_data["token"] = {"refresh": str(token), "access": str(token.access_token)}

        return Response({**token_data})


class UpdateUserProfileView(generics.UpdateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UpdateUserProfileSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, instance=self.get_object())
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class DeleteAccountView(generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = DeleteAccountSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"user": request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class DeleteAccountCheckView(generics.UpdateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = AccountDeleteCheckSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "uuid"

    def get_object(self):
        uuid = self.kwargs.get("uuid")
        id_ = smart_str(urlsafe_base64_decode(uuid))
        return User.objects.get(id=int(id_))