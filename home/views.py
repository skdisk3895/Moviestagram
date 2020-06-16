from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.db.models import Count
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
        flag = 1
        while len(recommendations) <5 and flag:
            for r_genre in recommendation_genre:
                if len(recommendations) >= 5:
                    flag = 0
                    break
                recommendation_movie = Movie.objects.filter(genres=r_genre).annotate(like_count=Count('like_users')).order_by('-like_count')[:1]
                recommendations += recommendation_movie
    else:
        recommendations = Movie.objects.annotate(like_count=Count('like_users')).order_by('-like_count')[:5]
    print(recommendations)
        
    reviews = request.user.like_movie_reviews.order_by('-created_at')
    context = {
        'movies': movies,
        'reviews': reviews,
        'recommendations': recommendations
    }
    return render(request, 'home/home.html', context)
