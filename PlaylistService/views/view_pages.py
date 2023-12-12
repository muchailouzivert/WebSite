# Create your views here.
from django.http import JsonResponse
from django.views.generic import ListView
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from PlaylistService.models import Playlist


class HomePageView(ListView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    model = Playlist
    template_name = 'home.html'
    context_object_name = 'playlist'


class MyPlaylistView(ListView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    model = Playlist
    template_name = 'main/MyPlaylist.html'
    context_object_name = 'playlist'


class Songs(ListView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    model = Playlist
    template_name = 'main/all_songs.html'
    context_object_name = 'song'
