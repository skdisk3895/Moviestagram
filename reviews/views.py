from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST, require_http_methods 
from django.http import JsonResponse, HttpResponse
from django.db import transaction
from movies.models import Movie
from .models import Review, Comment, Image
from .forms import ReviewForm, CommentForm, ImageFormSet

import json, config
import urllib.request

@require_GET
@login_required
def movie_review_list(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    genres = movie.genres.all()
    reviews = movie.movie_reviews.all()
    client_id = config.CLIENT_ID
    client_secret = config.NAVER_SECRET_KEY
    encText = urllib.parse.quote(movie.title)
    url = "https://openapi.naver.com/v1/search/movie?query=" + encText
    movie_api_request = urllib.request.Request(url)
    movie_api_request.add_header("X-Naver-Client-Id",client_id)
    movie_api_request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(movie_api_request)
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        result = json.loads(response_body.decode('utf-8'))
        items = result.get('items')
        # print(items[0])
    score_cnt = movie.movie_reviews.count()
    score_sum = 0
    for review in reviews:
        score_sum += review.score
    if score_sum == 0:
        avg_score = 0
    else:
        avg_score = round(score_sum / score_cnt, 2)
    form = CommentForm()
    context = {
        'reviews': reviews,
        'movie': movie,
        'form': form,
        'avg_score': avg_score,
        'genres': genres,
        'subtitle': items[0]['subtitle'],
        'date': items[0]['pubDate'],
        'director': items[0]['director'][:-1],
        'actor': items[0]['actor'][:-1],
    }
    return render(request, 'reviews/review_list.html', context)

@login_required
@require_http_methods(['GET', 'POST'])
def movie_create_review(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        image_formset = ImageFormSet(request.POST, request.FILES)
        rating = request.POST.get('star-input')
        movie = Movie.objects.get(pk=movie_pk)
        if form.is_valid() and image_formset.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.movie = movie
            review.score = rating
            with transaction.atomic():
                review.save()
                image_formset.instance = review
                image_formset.save()
                for user in movie.like_users.all():
                    if user == request.user: continue
                    user.like_movie_reviews.add(review)
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
        rating = request.POST.get('star-input')
        if form.is_valid() and image_formset.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.movie = movie
            review.score = rating
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
def review_like(request, movie_pk, review_pk):
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
        'like_count' : review.like_users.count(),
    }
    return JsonResponse(data)

@require_POST
@login_required
def comment_create(request, movie_pk, review_pk):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, pk=movie_pk)
        review = get_object_or_404(Review, pk=review_pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.movie = movie
            comment.review = review
            comment.save()
        data = {
            'movie_pk' : movie_pk,
            'review_pk' : review_pk,
            'opinion' : comment.opinion,
            'author' : request.user.username,
            'date' : comment.created_at,
            'like_users' : comment.like_users.count(),
            'comment_pk' : comment.pk,
        }
        return JsonResponse(data)

@require_GET
@login_required
def comment_delete(request, movie_pk, review_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user == comment.author:
        comment.delete()
        data = {
        }
        return JsonResponse(data)
    return HttpResponse(status=401)

@require_GET
@login_required
def comment_like(request, movie_pk, review_pk, comment_pk):
    user = request.user
    comment = get_object_or_404(Comment, pk=comment_pk)
    if comment.like_users.filter(pk=user.pk).exists():
        comment.like_users.remove(user)
        is_liked = False
    else:
        comment.like_users.add(user)
        is_liked = True

    data = {
        'is_liked' : is_liked,
        'like_count' : comment.like_users.count(),
    }
    return JsonResponse(data)

@require_GET
@login_required
def movie_like(request, movie_pk):
    user = request.user
    movie = get_object_or_404(Movie, pk=movie_pk)
    reviews = movie.movie_reviews.all()
    if movie.like_users.filter(pk=user.pk).exists():
        for review in reviews:
            user.like_movie_reviews.remove(review)
        movie.like_users.remove(user)
        is_liked = False
    else:
        for review in reviews:
            if review.author == request.user: continue
            user.like_movie_reviews.add(review)
        movie.like_users.add(user)
        is_liked = True

    data = {
        'is_liked' : is_liked,
        'like_count' : movie.like_users.count(),
    }
    return JsonResponse(data)