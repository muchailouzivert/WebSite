# Create your views here.
from django.http import JsonResponse
from django.views.generic import ListView
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from PlaylistService.models import Playlist


@api_view(['GET'])
def hello_world(request, variant):
    response_data = {'message': f'Hello World {variant}'}
    return JsonResponse(response_data, status=200)


class HomePageView(ListView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    model = Playlist
    template_name = ''
    context_object_name = 'playlist'


