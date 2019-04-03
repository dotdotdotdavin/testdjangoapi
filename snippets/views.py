from django.shortcuts import render

# snippets/views.py
from rest_framework import generics
from .models import Snippet
from .models import FaceImage
from .serializers import SnippetSerializer
from django.http import HttpResponse
from django.conf import settings

import json
import os


class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


def face1(request):
    if request.method == 'POST' or request.method == 'GET':
        path = "media/result/resultgif.gif"
        file_path = os.path.join(settings.MEDIA_ROOT, path)
        with open(path,'rb') as fh:
            response = HttpResponse(fh.read(), content_type="image/gif")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response