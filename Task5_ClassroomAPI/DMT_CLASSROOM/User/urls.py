from django.contrib import admin
from django.urls import path, include
from User.views import *


app_name = 'User manipulations'
urlpatterns = [
    path('create/', UserCreateView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('user', UserRetrieveUpdateAPIView.as_view())
]