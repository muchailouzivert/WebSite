from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views.view_comment import CommentViewSet
from .views.view_pages import HomePageView
from .views.view_song import SongViewSet
from .views.view_user import RegisterView, LoginView, logout_request
from .views.views_playlist import (
    PlaylistViewSet,
    get_all_user_playlist,
    all_songs_view,
    PrivatePlaylistListAPIView,
    get_public_playlist,
    AddSongViewSet
)

router = DefaultRouter()
router.register(r'playlist', PlaylistViewSet, basename='playlist')
router.register(r'songs/control', AddSongViewSet, basename="addSong")
router.register(r'songs', SongViewSet, basename='songs')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/playlist/by_user/<int:variant>/', get_all_user_playlist, name='GetByUsersPL'),
    path('api/playlist/all/public/', get_public_playlist, name='GetPublicPL'),
    path('api/playlist/all/private/', PrivatePlaylistListAPIView.as_view(), name='GetPrivatePL'),
    path('api/playlist/all/allsongs/', all_songs_view, name='View_Song'),
    path('', HomePageView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='user-registration'),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', logout_request, name="logout")
]
