# playlists/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from rest_framework import serializers, status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from PlaylistService.forms.Log_in_form import NewUserForm, CustomLoginForm
from PlaylistService.serializers import UserRegistrationSerializer, UserLoginSerializer


class RegisterView(CreateAPIView):
    template_name = "main/register.html"
    serializer_class = UserRegistrationSerializer

    def get(self, request, *args, **kwargs):
        form = NewUserForm()
        return render(request, self.template_name, {'register_form': form})

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            return Response({'success': False, 'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'success': True, 'message': 'User created successfully'}, status=status.HTTP_201_CREATED,
                        headers=headers)


class LoginView(CreateAPIView):
    template_name = "main/login.html"
    serializer_class = UserLoginSerializer

    def get(self, request, *args, **kwargs):
        form = CustomLoginForm()
        return render(request, self.template_name, {'login_form': form})

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, partial=True)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                token = RefreshToken.for_user(user)
                access_token = str(token.access_token)


                return Response({'success': True, 'message': f"You are now logged in as {username}",
                                 'token': access_token})
            else:
                return Response({'success': False, 'message': "Invalid username or password"},
                                status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'success': False, 'message': "Invalid username or password"},
                            status=status.HTTP_400_BAD_REQUEST)


class UserLogoutAPIView(GenericAPIView):
    """
    An endpoint to logout users.
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
