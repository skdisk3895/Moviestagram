from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from movies.models import Movie

@require_GET
@login_required
def review_list(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    reviews = movie.movie_reviews.all()
    context = {
        'reviews': reviews,
    }
    return render(request, 'reviews/reviews.html', context)

@login_required
@require_http_methods(['GET', 'POST'])
def create_review(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == 'POST':
        pass
    else:
        pass
    context = {

    }
    return render(request, 'reviews/form.html', context)

def update_review(request):
    pass

def delete_review(request):
    pass