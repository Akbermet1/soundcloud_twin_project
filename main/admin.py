from django.contrib import admin
from .models import Comment, Genre, Audio

admin.site.register(Genre)
admin.site.register(Audio)
admin.site.register(Comment)

