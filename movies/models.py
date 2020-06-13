from django.db import models
from django.conf import settings

class Movie(models.Model):
    title = models.TextField()
    link = models.TextField()
    image = models.TextField()
    subtitle = models.TextField()
    pubDate = models.TextField()
    director = models.TextField()
    actor = models.TextField()
    userRating = models.TextField()
    movie_like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies')