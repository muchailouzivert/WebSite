# views.py
from rest_framework import viewsets
from rest_framework.response import Response
from PlaylistService.models import Comment
from PlaylistService.serializers import CommentSerializer
from rest_framework import status
from rest_framework.exceptions import NotFound


class CommentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def list(self, request, *args, **kwargs):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        comment = self.get_object(pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, *args, **kwargs):
        comment = self.get_object(pk)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, *args, **kwargs):
        comment = self.get_object(pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise NotFound(detail="Comment not found", code=status.HTTP_404_NOT_FOUND)
