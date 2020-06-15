from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from .models import Movie

@require_GET
@login_required
def movie_list(request):
    title = request.GET.get('movieTitle')
    movies = Movie.objects.filter(title__icontains=title)
    context = {
        'movies': movies,
    }
    return render(request, 'movies/movie_list.html', context)
