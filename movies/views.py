from django.shortcuts import render
from .models import Movie

def home(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies,
    }
    return render(request, 'movies/home.html', context)

def movie_list(request):
    title = request.GET.get('movieTitle')
    movies = Movie.objects.filter(title__icontains=title)
    print(movies)
    context = {
        'movies': movies,
    }
    return render(request, 'movies/movie_list.html', context)