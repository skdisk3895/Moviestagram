from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    path('admin/create/', views.movie_create, name='movie_create'),
]