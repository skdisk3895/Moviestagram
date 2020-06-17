from django.contrib import admin
from .models import Genre, Movie

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title']
    list_display_links = ['title']
