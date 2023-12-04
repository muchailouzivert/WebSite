# views.py
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.exceptions import NotFound
from PlaylistService.models import Playlist
from PlaylistService.serializers import PlaylistSerializer


class GetPublicPlaylists(APIView):
    def get(self, request, *args, **kwargs):
        public_playlists = Playlist.objects.filter(is_public=True)
        serializer = PlaylistSerializer(public_playlists, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def get_all_user_playlist(request, variant):
    # Get all playlists by user ID
    user_playlists = Playlist.objects.filter(owner__id=variant)
    serializer = PlaylistSerializer(user_playlists, many=True)
    return Response(serializer.data)


class PlaylistViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

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
        serializer = PlaylistSerializer(playlist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
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

