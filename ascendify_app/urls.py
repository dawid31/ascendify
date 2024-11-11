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
    path('community', views.community, name='community'),
    path('events/', views.event_list, name='events'),
    path('events/create/', views.create_event, name='create_event'),
    path('events/join/<int:event_id>/', views.join_event, name='join_event'),
    path('events/leave/<int:event_id>/', views.leave_event, name='leave_event'),
    path('forum/', views.forum, name='forum'),
    path('forum/channel/<int:channel_id>/', views.channel_discussion_view, name='channel_discussion'), 
    path('forum/send_message/<int:channel_id>/', views.send_message, name='send_message'),
    path('search/', views.search, name='search'),
    path('find-indoor-spots/', views.find_indoor_spots, name='find-indoor-spots'),
    path('find-outdoor-spots/', views.find_outdoor_spots, name='find-outdoor-spots'),
    
]
