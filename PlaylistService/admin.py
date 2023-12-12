from django.contrib import admin
from .models import Playlist, Song, Comment
from django.contrib.auth.models import Group, Permission

admin.site.register(Playlist)
admin.site.register(Song)
admin.site.register(Comment)

