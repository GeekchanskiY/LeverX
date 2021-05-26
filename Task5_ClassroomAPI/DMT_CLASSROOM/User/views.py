from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView

from rest_framework.authentication import SessionAuthentication


from User.serializers import UserDetailSerializer
# Create your views here.

class UserCreateView(generics.CreateAPIView):
    serializer_class = UserDetailSerializer

