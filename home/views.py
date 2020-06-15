from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET

@require_GET
@login_required
def home(request):
    movies = request.user.like_movies.values('title')
    context = {
        'movies': movies,
    }
    return render(request, 'home/home.html', context)
