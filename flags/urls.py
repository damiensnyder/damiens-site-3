from django.urls import path
from . import views


app_name = "flags"

urlpatterns = [
    path('', views.vote, name='vote'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]