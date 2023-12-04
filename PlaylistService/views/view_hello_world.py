# Create your views here.
from django.http import JsonResponse
from django.views.generic import ListView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from PlaylistService.models import Playlist


@api_view(['GET'])
def hello_world(request, variant):
    response_data = {'message': f'Hello World {variant}'}
    return JsonResponse(response_data, status=200)


class HomePageView(ListView):
    model = Playlist
    template_name = 'home.html'
    context_object_name = 'playlist'


