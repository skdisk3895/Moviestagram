from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('<int:movie_pk>/', views.movie_review_list, name='movie_review_list'),
    path('<int:movie_pk>/create/', views.movie_create_review, name='movie_create_review'),
    path('<int:movie_pk>/<int:review_pk>/update/', views.movie_update_review, name='movie_update_review'),
    path('<int:movie_pk>/<int:review_pk>/delete/', views.movie_delete_review, name='movie_delete_review'),
    path('<int:movie_pk>/<int:review_pk>/like/', views.review_like, name='review_like'),
    path('<int:movie_pk>/<int:review_pk>/comments/', views.comment_create, name='comment_create'),
    path('<int:movie_pk>/<int:review_pk>/<int:comment_pk>/delete/', views.comment_delete, name='comment_delete'),
    path('<int:movie_pk>/<int:review_pk>/<int:comment_pk>/like/', views.comment_like, name='comment_like'),
]