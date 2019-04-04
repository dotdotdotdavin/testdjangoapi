from django.shortcuts import render

# snippets/views.py
from rest_framework import generics
from .models import Snippet
from .models import FaceImage
from .serializers import SnippetSerializer
from django.http import HttpResponse
from django.conf import settings
from . import faceMorphCustom as fMC

import json
import os


class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


class FaceImage():
    def face1(request):
        if request.method == 'POST' or request.method == 'GET':
            path = "media/result/resultgif.gif"
            file_path = os.path.join(settings.MEDIA_ROOT, path)
            with open(path,'rb') as fh:
                response = HttpResponse(fh.read(), content_type="image/gif")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response

    def face2(request):
        if request.method == 'POST' or request.method == 'GET':
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            print(body)
            
            if body['sources'] and len(body['sources']) == 2:
                dastr = fMC.faceMorph(body['sources'][0]['image_url'],body['sources'][1]['image_url'])
                path1 = dastr
                file_path1 = os.path.join(settings.MEDIA_ROOT, path1)
                with open(path1,'rb') as fh:
                    response1 = HttpResponse(fh.read(), content_type="image/gif")
                    response1['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path1)
                    return response1
            else:
                return render(request,"simple.html")



