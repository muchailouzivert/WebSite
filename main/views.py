from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse


def hello_world(request, variant):
    response_data = {'message': f'Hello World {variant}'}
    return JsonResponse(response_data, status=200)
