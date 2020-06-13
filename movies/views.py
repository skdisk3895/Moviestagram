import json
import urllib.request
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET
from .models import Movie

# @require_GET
# def movie_search(request):
#     client_id = "C6LNcmNSIQIEwWVSi6V4"
#     client_secret = "k0SlcrKOPe"
#     encText = urllib.parse.quote("기생충")
#     url = "https://openapi.naver.com/v1/search/blog?query=" + encText + "&" # json 결과
#     movie_api_request = urllib.request.Request(url)
#     movie_api_request.add_header("X-Naver-Client-Id",client_id)
#     movie_api_request.add_header("X-Naver-Client-Secret",client_secret)
#     response = urllib.request.urlopen(movie_api_request)
#     rescode = response.getcode()
#     if(rescode==200):
#         response_body = response.read()
#         result = json.loads(response_body.decode('utf-8'))
#         items = result.get('items')
#         context = {
#             'items': items
#         }
#         return render(request, 'movies/search.html', context=context)
#     else:
#         print("Error Code:" + rescode)

@require_GET
def movie_search(request):
    title = request.GET.get('movieTitle')
    print(title)
    return redirect('movies:movie_list', title)

@require_GET
def movie_list(request, movie_title):
    print(movie_title)
    movies = Movie.objects.filter(title__contains='movie_title')
    context = {
        'movies': movies
    }
    return render(request, 'movies/movie_list.html', context)
    