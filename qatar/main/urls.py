from main import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('matches/', views.match_list, name='match-list'),
]