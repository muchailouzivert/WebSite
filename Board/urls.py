from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .adminviews import register_user
from .views import (
    hello_world,
    VacancyController,
    ApplicationController,
    AppUserController
)

router = DefaultRouter()
router.register(r'vacancies', VacancyController, basename='vacancies')
router.register(r'application', ApplicationController, basename='application')
router.register(r'app_user', AppUserController, basename='app_user')


urlpatterns = [
    path('api/v1/hello-world-<int:variant>/', hello_world, name='hello_world'),
    path('api/', include(router.urls)),
    path('register/', register_user, name='register')
]
