from django.urls import path

from . import views

urlpatterns = [
    path('', views.front_page, name='front-page'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('content/', views.all_content_menu, name='all-content-menu'),
    path('content/<int:page_num>/', views.all_content_menu, name='content-paginated'),
    path('shortform/', views.all_shortform_menu, name='all-shortform-menu'),
    path('shortform/<int:page_num>/', views.all_shortform_menu, name='shortform-paginated'),
    path('<url>/', views.tag_or_content, name='tag-or-content'),
    path('<url>/<int:page_num>/', views.tag_or_content, name='tag-paginated'),
    path('<tag_url>/<post_url>/', views.content, name='content'),
    path('<tag_url>/<post_url>/message/', views.send_message, name='send_message')
]