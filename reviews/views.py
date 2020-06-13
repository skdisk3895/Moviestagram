from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST, require_http_methods 
from movies.models import Movie
from .models import Review
from .forms import ReviewForm

@require_GET
def movie_review_list(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    reviews = movie.movie_reviews.all()
    context = {
        'reviews': reviews,
        'movie': movie,
    }
    return render(request, 'reviews/review_list.html', context)

@require_http_methods(['GET', 'POST'])
def movie_create_review(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.save()
            return redirect('reviews:movie_review_list', movie.pk)
    else:
        form =ReviewForm()
    context = {
        'form': form
    }
    return render(request, 'reviews/review_form.html', context)

@require_http_methods(['GET', 'POST'])
def movie_update_review(request, movie_pk, review_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        form.save()
        return redirect('reviews:movie_review_list', movie.pk)
    else:
        form =ReviewForm(instance=review)
    context = {
        'form': form
    }
    return render(request, 'reviews/review_form.html', context)

@require_POST
def movie_delete_review(request, movie_pk, review_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    review = get_object_or_404(Review, pk=review_pk)
    review.delete()
    return redirect('reviews:movie_review_list', movie.pk)