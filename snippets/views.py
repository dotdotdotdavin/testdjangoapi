from django.shortcuts import render

# snippets/views.py
from rest_framework import generics
from .models import Snippet
from .models import FaceImage
from .serializers import SnippetSerializer
import json


class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


def face1(request):
    if request.method == 'POST' or request.method == 'GET':
        faceimg = FaceImage
        faceimg2 = FaceImage
        # body_unicode = request.body.decode('utf-8')
        # body = json.loads(body_unicode)
        # print(body['sources'][0]['image_url'])
        
        return render(request,'simple.html')