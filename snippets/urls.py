# snippets/urls.py
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views
from django.conf.urls import url

urlpatterns = [
    path('snippets/', views.SnippetList.as_view()),
    # path('snippets/<int:pk>/', views.SnippetDetail.as_view()),
    path('face1',views.face1)
   
]

urlpatterns = format_suffix_patterns(urlpatterns)