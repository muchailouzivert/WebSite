from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views.view_comment import CommentViewSet
from .views.view_pages import hello_world, HomePageView
from .views.view_song import SongViewSet
from .views.view_user import RegisterView, LoginView
from .views.user_view_crud import UserViewSet
from .views.views_playlist import (
    PlaylistViewSet,
    get_all_user_playlist,
    PrivatePlaylistListAPIView,
    get_public_playlist,
    AddSongViewSet
)

router = DefaultRouter()
router.register(r'playlist', PlaylistViewSet, basename='playlist')
router.register(r'songs/control', AddSongViewSet, basename="addSong")
router.register(r'songs', SongViewSet, basename='songs')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'users', UserViewSet)

urlpatterns = [
    path('api/v1/hello-world-<int:variant>/', hello_world, name='hello_world'),
    path('api/', include(router.urls)),
    path('api/playlist/by_user/<int:variant>/', get_all_user_playlist, name='GetByUsersPL'),
    path('api/playlist/all/public/', get_public_playlist, name='GetPublicPL'),
    path('api/playlist/all/private/', PrivatePlaylistListAPIView.as_view(), name='GetPublicPL'),
    path('', HomePageView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='user-registration'),
    path("login/", LoginView.as_view(), name="login"),
]
