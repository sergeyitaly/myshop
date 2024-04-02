from urllib import response
from django.shortcuts import redirect
from rest_framework.generics import (ListCreateAPIView,RetrieveUpdateDestroyAPIView,)
from . import permission
from myshop.settings import REST_FRAMEWORK
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import *
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.authentication import JWTAuthentication
from djoser.views import UserViewSet
from rest_framework.response import Response
from rest_framework import status
 
class ActivateUser(UserViewSet):
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        kwargs['data'] = {"uid": self.kwargs['uid'], "token": self.kwargs['token']}
        return serializer_class(*args, **kwargs)

 
    def activation(self, request, uid, token, *args, **kwargs):
        super().activation(request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def login(request: Request):
    serializer = LoginRequestSerializer(data=request.data)
    if serializer.is_valid():
        authenticated_user = authenticate(**serializer.validated_data)
        if authenticated_user is not None:
            login(request, authenticated_user)
            return Response({'status': 'Success'})
        else:
            return Response({'error': 'Invalid credentials'}, status=403)
    else:
        return Response(serializer.errors, status=400)

class UserView(APIView):
    permission_classes= [IsAuthenticated]
    def get(self, request):
        return Response({'data': 'Booo! You are inside the account'})

@api_view(['POST'])
@permission_classes([AllowAny])
def registration_view(request):
    if request.method == 'POST':
        serializer= UserSerializer(data=request.data)
        data={}
        if serializer.is_valid():
            customuser = serializer.save()
            data['response'] = 'Succesfully registered new user!!!'
            data['email'] = customuser.email
            data['username'] = customuser.username
        else:
            data=serializer.errors
        return Response(data)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)