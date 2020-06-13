from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('search/', views.movie_search, name='movie_search'),
    path('<str:movie_title>/', views.movie_list, name='movie_list'),
]