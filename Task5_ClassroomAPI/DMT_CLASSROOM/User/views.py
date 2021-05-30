from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework.authentication import SessionAuthentication

from rest_framework import status
from rest_framework.response import Response

from User.serializers import UserDetailSerializer, LoginSerializer

from  User.jsonrenderer import UserJSONRenderer


# Create your views here.

class UserCreateView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserDetailSerializer

class UserLoginView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def get(self, request):
        user = request.data.get('user', {})
        print(request.data)
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=200)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})

        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)



