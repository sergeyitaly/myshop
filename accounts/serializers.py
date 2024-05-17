import email
from rest_framework.serializers import Serializer, ModelSerializer, CharField
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from .models import CustomUser

from django.contrib.auth import authenticate, get_user_model
from djoser.conf import settings
from djoser.serializers import TokenCreateSerializer

AuthUser = get_user_model()

class CustomTokenCreateSerializer(TokenCreateSerializer):

    def validate(self, attrs):
        password = attrs.get("password")
        params = {settings.LOGIN_FIELD: attrs.get(settings.LOGIN_FIELD)}
        self.user = authenticate(
            request=self.context.get("request"), **params, password=password
        )
        if not self.user:
            self.user = AuthUser.objects.filter(**params).first()
            if self.user and not self.user.check_password(password):
                self.fail("invalid_credentials")
        # We changed only below line
        if self.user: # and self.user.is_active: 
            return attrs
        self.fail("invalid_credentials")

class UserSerializer(ModelSerializer):
    password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    re_password = serializers.CharField(style={'input_type':'re_password'}, write_only=True)

    class Meta:
         model = CustomUser
         fields = ['email', 'username', 'password', 're_password']

    def save(self):
        new_customuser= CustomUser(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )
        password = self.validated_data['password']
        re_password = self.validated_data['re_password']
        if re_password != password:
            raise serializers.ValidationError({'password': 'Passwords must match...'})
    
        new_customuser.set_password(password)
        new_customuser.save()
        return new_customuser

class LoginRequestSerializer(Serializer):
    model = User
    username = CharField(required=True)
    password = CharField(required=True)

class TokenSeriazliser(ModelSerializer):
    class Meta:
        model = Token
        fields = ['key']
