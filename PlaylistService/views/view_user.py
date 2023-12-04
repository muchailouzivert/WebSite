# playlists/views.py
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from rest_framework import serializers, status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from PlaylistService.forms.Log_in_form import NewUserForm, CustomAuthenticationForm
from PlaylistService.serializers import UserRegistrationSerializer


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

    def get(self, request, *args, **kwargs):
        form = CustomAuthenticationForm()
        return render(request, self.template_name, {'register_form': form})

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return Response({'success': True, 'message': f"You are now logged in as {username}"})
            else:
                return Response({'success': False, 'message': "Invalid username or password"},
                                status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'success': False, 'message': "Invalid username or password"},
                            status=status.HTTP_400_BAD_REQUEST)
