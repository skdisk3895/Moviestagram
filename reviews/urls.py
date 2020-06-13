from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('<int:movie_pk>/list/', views.review_list, name='review_list'),
    path('<int:movie_pk>/create/', views.create_review, name='create_review'),
    path('<int:movie_pk>/update/<int:review_pk>/', views.update_review, name='update_review'),
    path('<int:movie_pk>/delete/<int:review_pk>/', views.delete_review, name='delete_review'),
]