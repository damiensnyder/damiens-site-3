from django.urls import path
from . import views


app_name = "flags"

urlpatterns = [
    path('', views.vote, name='vote'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('favorites/', views.favorites, name='favorites'),
    path('reported/', views.reported_flags, name='reported_flags'),
    path('info/<int:flag_id>/', views.flag_info, name='flag_info'),
    path('pin/', views.pin_flag, name='pin_flag'),
    path('unpin/', views.unpin_flag, name='unpin_flag'),
    path('report/', views.report_flag, name='report_flag'),
    path('delete/', views.delete_flag, name='delete_flag'),
]