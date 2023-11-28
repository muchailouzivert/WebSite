# Create your views here.
from django.http import JsonResponse
from rest_framework.decorators import api_view


@api_view(['GET'])
def hello_world(request, variant):
    response_data = {'message': f'Hello World {variant}'}
    return JsonResponse(response_data, status=200)

