from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('releases/', views.release_list, name='release_list'),
    path('releases/<int:pk>/', views.release_detail, name='release_detail'),
    path('databaze/interpreti/', views.db_artists_list, name='db_artists'),
    
    path('databaze/alba/', views.db_releases_list, name='db_releases'),
    path('login/spotify/', views.spotify_login, name='spotify_login'),
    path('spotify/callback/', views.spotify_callback, name='spotify_callback'),
    path('spotify/stats/', views.spotify_stats, name='spotify_stats'),
    path('logout/spotify/', views.spotify_logout, name='spotify_logout'),
]