from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'), 
    path('register', views.register, name='register'), 
    path('logout', views.logoutUser, name='logout'),
    path('profile', views.profile, name='profile'),
    path('edit-profile', views.edit_profile, name='edit-profile'),
    path('find-spots', views.find_spots, name='find-spots'),
    path('community', views.community, name='community'),
    path('events', views.events, name='events'),

]
