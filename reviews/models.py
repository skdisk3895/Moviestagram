from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from movies.models import Movie

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_reviews')
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='my_reviews')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_reviews')
    like_movie_reviews_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movie_reviews') 
    score = models.IntegerField()

def image_path(instance, filename):
    return f'reviews/{instance.review.content}/{filename}'

class Image(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='review_images')
    image_files = ProcessedImageField(
            upload_to = image_path,
            processors = [ResizeToFill(600, 600)],
            format = 'JPEG',
            options = {'quality': 90},)

class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='review_comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='my_comments')
    opinion = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_comments')