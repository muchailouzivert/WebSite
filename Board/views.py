# Create your views here.
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets
from .serializers import *
from .models import *


@api_view(['GET'])
def hello_world(request, variant):
    response_data = {'message': f'Hello World {variant}'}
    return JsonResponse(response_data, status=200)


def handle_bad_request(serializer):
    return Response({
        'error': 'Bad Request',
        'detail': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


class VacancyController(viewsets.ReadOnlyModelViewSet):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer

    def list(self, request, *args, **kwargs):
        vacancies = Vacancy.objects.all()
        serializer = self.get_serializer(vacancies, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        vacancy = self.get_object()
        serializer = self.get_serializer(vacancy)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = VacancySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return handle_bad_request(serializer)

    def update(self, request, *args, **kwargs):
        vacancy = self.get_object()
        serializer = VacancySerializer(vacancy, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return handle_bad_request(serializer)

    def destroy(self, request, *args, **kwargs):
        vacancy = self.get_object()
        vacancy.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ApplicationController(viewsets.ReadOnlyModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    def list(self, request, *args, **kwargs):
        applications = Application.objects.all()
        serializer = self.get_serializer(applications, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        application = self.get_object()
        serializer = self.get_serializer(application)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = ApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return handle_bad_request(serializer)

    def destroy(self, request, *args, **kwargs):
        application = self.get_object()
        application.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AppUserController(viewsets.ReadOnlyModelViewSet):
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer

    @swagger_auto_schema(operation_description='List all app users')
    def list(self, request, *args, **kwargs):
        app_users = AppUser.objects.all()
        serializer = self.get_serializer(app_users, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(operation_description='Get by id')
    def retrieve(self, request, *args, **kwargs):
        app_user = self.get_object()
        serializer = self.get_serializer(app_user)
        return Response(serializer.data)

    @swagger_auto_schema(operation_description='Create user')
    def create(self, request, *args, **kwargs):
        serializer = AppUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return handle_bad_request(serializer)

    @swagger_auto_schema(operation_description='Delete user')
    def destroy(self, request, *args, **kwargs):
        app_user = self.get_object()
        app_user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)