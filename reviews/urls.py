from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('<int:movie_pk>/', views.movie_review_list, name='movie_review_list'),
    path('<int:movie_pk>/create/', views.movie_create_review, name='movie_create_review'),
    path('<int:movie_pk>/<int:review_pk>/update/', views.movie_update_review, name='movie_update_review'),
    path('<int:movie_pk>/<int:review_pk>/delete/', views.movie_delete_review, name='movie_delete_review'),
    path('<int:review_pk>/like/', views.review_like, name='review_like')
]