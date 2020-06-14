from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST, require_http_methods 
from django.db import transaction
from movies.models import Movie
from .models import Review, Comment, Image
from .forms import ReviewForm, CommentForm, ImageFormSet
from django.http import JsonResponse

@require_GET
@login_required
def movie_review_list(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    reviews = movie.movie_reviews.all()
    context = {
        'reviews': reviews,
        'movie': movie,
    }
    return render(request, 'reviews/review_list.html', context)

@login_required
@require_http_methods(['GET', 'POST'])
def movie_create_review(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        image_formset = ImageFormSet(request.POST, request.FILES)
        if form.is_valid() and image_formset.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.movie = movie
            with transaction.atomic():
                review.save()
                image_formset.instance = review
                image_formset.save()
                return redirect('reviews:movie_review_list', movie.pk)
    else:
        form =ReviewForm()
        image_formset = ImageFormSet()
    context = {
        'form': form,
        'image_formset': image_formset,
    }
    return render(request, 'reviews/review_form.html', context)

@login_required
@require_http_methods(['GET', 'POST'])
def movie_update_review(request, movie_pk, review_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        image_formset = ImageFormSet(request.POST, request.FILES, instance=review)
        if form.is_valid() and image_formset.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.movie = movie
            with transaction.atomic():
                review.save()
                image_formset.instance = review
                image_formset.save()
                return redirect('reviews:movie_review_list', movie.pk)
    else:
        form =ReviewForm(instance=review)
        image_formset = ImageFormSet(instance=review)
    context = {
        'form': form,
        'image_formset': image_formset,
    }
    return render(request, 'reviews/review_form.html', context)

@require_POST
@login_required
def movie_delete_review(request, movie_pk, review_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    review = get_object_or_404(Review, pk=review_pk)
    review.delete()
    return redirect('reviews:movie_review_list', movie.pk)

@require_GET
@login_required
def review_like(request, review_pk):
    user = request.user
    review = get_object_or_404(Review, pk=review_pk)
    if review.like_users.filter(pk=user.pk).exists():
        review.like_users.remove(user)
        is_liked = False
    else:
        review.like_users.add(user)
        is_liked = True

    data = {
        'is_liked' : is_liked,
        'like_count' : review.like_users.count()
    }
    return JsonResponse(data)