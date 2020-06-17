from django.db import models
from django.conf import settings
import requests
import config

class Genre(models.Model):
    name = models.CharField(max_length=200)

class Movie(models.Model):
    title = models.CharField(max_length=200)
    original_title = models.CharField(max_length=200)
    release_date = models.DateField()
    popularity = models.FloatField()
    vote_count = models.IntegerField()
    vote_average = models.FloatField()
    adult = models.BooleanField()
    overview = models.TextField()
    original_language = models.CharField(max_length=200)
    poster_path = models.CharField(max_length=200)
    backdrop_path = models.CharField(max_length=200)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies')
    genres = models.ManyToManyField(Genre, related_name='genre_movies')

    @classmethod
    def movie_search(cls, title, page):
        print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
        for n in range(page):
            api_key = config.API_KEY
            movies = requests.get(
                f'https://api.themoviedb.org/3/search/movie?api_key=' + api_key + '&query='+ title
            ).json().get('results')
            # print(movies)
            for movie in movies:      
                print(movie)           
                if  Movie.objects.filter(pk=movie.get('id')).exists():
                    continue
                m, created = cls.objects.get_or_create(
                    id=movie.get('id'),
                    title=movie.get('title'),
                    original_title=movie.get('original_title'),
                    release_date=movie.get('release_date'),
                    popularity=movie.get('popularity'),
                    vote_count=movie.get('vote_count'),
                    vote_average=movie.get('vote_average'),
                    adult=movie.get('adult'),
                    overview=movie.get('overview'),
                    original_language=movie.get('original_language'),
                    poster_path=movie.get('poster_path') if movie.get('poster_path') else '',
                    backdrop_path=movie.get('backdrop_path') if movie.get('backdrop_path') else '',
                )
                if created:
                    for genre_id in movie.get('genre_ids'):
                        g = Genre.objects.get(pk=genre_id)
                        m.genres.add(g)
        print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')