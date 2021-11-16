from django.urls import path

from . import views

urlpatterns = [
    path('', views.front_page, name='front-page'),
    path('content/', views.all_content_menu, name='all-content-menu'),
    path('<id>/', views.tag_or_content, name='tag-or-content'),
    path('<tag>/<id>/', views.content, name='content'),
]