# views.py
from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from PlaylistService.models import Song
from PlaylistService.serializers import SongSerializer, get_playlist_by_id
from rest_framework import status

class SongViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def list(self, request, *args, **kwargs):
        songs = Song.objects.all()
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        song = self.get_object(pk)
        serializer = SongSerializer(song)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = SongSerializer(data=request.data)
        if serializer.is_valid():
            playlist = serializer.validated_data.get('playlist')
            if playlist.owner != request.user:
                return Response({'success': False, 'errors': 'Unauthorized Playlist!'},
                                status=status.HTTP_401_UNAUTHORIZED)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, *args, **kwargs):
        song = self.get_object(pk)
        serializer = SongSerializer(song, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, *args, **kwargs):
        song = self.get_object(pk)
        song.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self, pk):
        try:
            return Song.objects.get(pk=pk)
        except Song.DoesNotExist:
            raise NotFound(detail="Song not found", code=status.HTTP_404_NOT_FOUND)
