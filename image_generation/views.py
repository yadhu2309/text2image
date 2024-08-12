from django.shortcuts import render, HttpResponse
from image_generation.task import generate_image_task
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view



# Create your views here.
@api_view(['GET'])
def generate_image(request):
   
    result = generate_image_task.delay()
    return Response({'result': 'success'}, status=status.HTTP_200_OK)
