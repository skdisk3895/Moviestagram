from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.db.models import Count, Q
from movies.models import Movie

@require_GET
@login_required
def home(request):
    movies = request.user.like_movies.values('title')
    genres_count = request.user.like_movies.values('genres').annotate(dcount=Count('genres'))
    genres_count_order = genres_count.order_by('-dcount')
    recommendations = []
    recommendation_genre = []
    if genres_count_order.count() > 4:
        for genre in genres_count_order[:3]:
            recommendation_genre += [genre.get('genres')]    
        recommendation_movies = Movie.objects.filter(Q(genres=recommendation_genre[0])|Q(genres=recommendation_genre[1])|Q(genres=recommendation_genre[2])).annotate(like_count=Count('like_users')).order_by('-like_count')
        for recom_movie in recommendation_movies:
            if len(recommendations) >= 5:
                break
            if recom_movie not in request.user.like_movies.all():
                recommendations += [recom_movie]
    else:       
        recommendation_movies = Movie.objects.annotate(like_count=Count('like_users')).order_by('-like_count')
        for recom_movie in recommendation_movies:
            if len(recommendations) >= 5:
                break
            if recom_movie not in request.user.like_movies.all():
                recommendations += [recom_movie]
    print(recommendations)
        
    reviews = request.user.like_movie_reviews.order_by('-created_at')
    context = {
        'movies': movies,
        'reviews': reviews,
        'recommendations': recommendations
    }
    return render(request, 'home/home.html', context)
