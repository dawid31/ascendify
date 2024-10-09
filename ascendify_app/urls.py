from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'), 
    path('register', views.register, name='register'), 
    path('logout', views.logoutUser, name='logout'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('edit-profile', views.edit_profile, name='edit-profile'),
    path('find-spots', views.find_spots, name='find-spots'),
    path('community', views.community, name='community'),
    path('events', views.events, name='events'),
    path('forum/', views.forum, name='forum'),
    path('forum/channel/<int:channel_id>/', views.channel_discussion_view, name='channel_discussion'), 
    path('forum/send_message/<int:channel_id>/', views.send_message, name='send_message'),
    path('search/', views.search, name='search'),
    path('find-spots/', views.find_spots, name='find_spots'),
]
