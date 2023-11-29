from django.urls import path
from .views import hello_world
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('api/v1/hello-world-<int:variant>/', hello_world, name='hello_world'),
]
