
# views.py


from django.shortcuts import render
import os
from dotenv import load_dotenv
from distutils.util import strtobool
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView


load_dotenv()
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
USE_S3 = bool(strtobool(os.getenv('USE_S3', 'True')))
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_TEMPLATES =f'https://{AWS_S3_CUSTOM_DOMAIN}/templates/'


def index(request):
    if USE_S3 == False:
        # Render the local template
        return render(request, "index.html")
    else:
        # Render the template from S3 bucket
        #s3_template_url = f"{AWS_TEMPLATES}index.html"
        #return render(request, s3_template_url)
    
        return render(request, "index.html")


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh_token = response.data.get('refresh')
        access_token = response.data.get('access')
        return Response({
            'refresh_token': refresh_token,
            'access_token': access_token,
        })

class CustomTokenRefreshView(APIView):
    authentication_classes = (JWTAuthentication,)

    def post(self, request, *args, **kwargs):
        refresh = request.data.get('refresh')
        token = RefreshToken(refresh)

        new_access_token = {
            'access': str(token.access_token),
        }

        return Response(new_access_token)

