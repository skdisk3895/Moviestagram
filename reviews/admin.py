from django.contrib import admin
from .models import Review, Image, Comment

admin.site.register(Image)
admin.site.register(Comment)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['movie_title', 'author', 'created_at']
    list_display_links = ['movie_title', 'author']

    def movie_title(self, obj):
        return obj.movie.title
