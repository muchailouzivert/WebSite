# views.py
from django.shortcuts import render
from rest_framework.decorators import api_view, action, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework import status, viewsets, generics
from rest_framework.exceptions import NotFound
from rest_framework_simplejwt.authentication import JWTAuthentication

from PlaylistService.models import Playlist, Song
from PlaylistService.serializers import PlaylistSerializer, SongSerializer, AddSongSerializer

serializer_class = PlaylistSerializer


@api_view(['GET'])
def get_all_user_playlist(request, variant):
    # Get all playlists by user ID
    user_playlists = Playlist.objects.filter(owner__id=variant)
    serializer = PlaylistSerializer(user_playlists, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_public_playlist(request):
    public_playlists = Playlist.objects.filter(is_public=True)
    serializer = PlaylistSerializer(public_playlists, many=True)
    return Response(serializer.data)


class PrivatePlaylistListAPIView(generics.ListAPIView):
    serializer_class = PlaylistSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'home.html'

    def list(self, request, *args, **kwargs):
        private_playlists = Playlist.objects.filter(owner=request.user, is_public=False)
        serializers = PlaylistSerializer(private_playlists, many=True)
        return Response({'object_list': serializers.data})


class PlaylistViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def list(self, request, *args, **kwargs):
        playlists = Playlist.objects.all()
        serializer = PlaylistSerializer(playlists, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        playlist = self.get_object(pk)
        serializer = PlaylistSerializer(playlist)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = PlaylistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, *args, **kwargs):
        playlist = self.get_object(pk)
        serializer = PlaylistSerializer(playlist, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, *args, **kwargs):
        playlist = self.get_object(pk)
        playlist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self, pk):
        try:
            return Playlist.objects.get(pk=pk)
        except Playlist.DoesNotExist:
            raise NotFound(detail="Playlist not found", code=status.HTTP_404_NOT_FOUND)


class AddSongViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AddSongSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return None

    @action(detail=False, methods=['post'])
    def add_song(self, request):
        playlist_id = request.data.get('playlist_id')
        song_id = request.data.get('song_id')

        try:
            playlist = Playlist.objects.get(pk=playlist_id)
            song = Song.objects.get(pk=song_id)

            if song not in playlist.songs.all():
                playlist.songs.add(song)
                serializer = self.get_serializer(playlist)
                return Response(serializer.data)
            else:
                return Response({"error": "Song is already in the playlist."}, status=400)

        except Playlist.DoesNotExist:
            return Response({"error": "Playlist does not exist."}, status=400)
        except Song.DoesNotExist:
            return Response({"error": "Song does not exist."}, status=400)

    @action(detail=False, methods=['delete'])
    def remove_song(self, request):
        playlist_id = request.data.get('playlist_id')
        playlist = Playlist.objects.get(pk=playlist_id)
        song_id = request.data.get('song_id')

        try:
            song = Song.objects.get(pk=song_id)

            if song in playlist.songs.all():
                playlist.songs.remove(song)
                return Response({"message": "Song removed from the playlist successfully."})
            else:
                return Response({"error": "Song is not in the playlist."}, status=400)

        except Song.DoesNotExist:
            return Response({"error": "Song does not exist."}, status=400)
