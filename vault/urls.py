from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('releases/', views.release_list, name='release_list'),
    path('releases/<int:pk>/', views.release_detail, name='release_detail'),
]