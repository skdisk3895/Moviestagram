from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_http_methods
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

@login_required
@require_http_methods(['GET', 'POST'])
def movie_create(request):
    if request.user.username != 'admin':
        return redirect('home:home')
    if request.method == 'POST':
        title = request.POST.get('title')
        Movie.movie_search(title, 1)
        return redirect('home:home')
    else:
        context = {}
        return render(request, 'movies/movie_create.html', context)
    
    



