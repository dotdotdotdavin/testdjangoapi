from django.contrib import admin

# Register your models here.
# snippets/admin.py
from django.contrib import admin
from . models import Snippet

admin.site.register(Snippet)