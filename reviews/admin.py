from django.contrib import admin
from .models import Review, Image, Comment

admin.site.register(Image)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['movie_title', 'author', 'created_at']
    list_display_links = ['movie_title', 'author']

    def movie_title(self, obj):
        return obj.movie.title

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['opinion', 'author']
    list_display_links = ['opinion', 'author']
