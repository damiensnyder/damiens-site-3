from django.urls import path

from . import views

urlpatterns = [
    path('', views.front_page, name='front-page'),
    path('signup/', views.signup, name='signup'),
    path('content/', views.all_content_menu, name='all-content-menu'),
    path('content/<int:page_num>/', views.all_content_menu, name='content-paginated'),
    path('shortform/', views.all_shortform_menu, name='all-shortform-menu'),
    path('shortform/<int:page_num>/', views.all_shortform_menu, name='shortform-paginated'),
    path('<id>/', views.tag_or_content, name='tag-or-content'),
    path('<id>/<int:page_num>/', views.tag_or_content, name='tag-paginated'),
    path('<tag>/<id>/', views.content, name='content')
]