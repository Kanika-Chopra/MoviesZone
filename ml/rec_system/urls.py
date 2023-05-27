from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('/signup', signup, name='signup'),
    path('/recommend', recommend, name='recommend'),
]
