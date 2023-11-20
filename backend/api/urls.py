from django.urls import path, include
from .views import create_file


urlpatterns = [
    path('create_file/', create_file, name='create_file'),
]
