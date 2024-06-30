
# views.py


from django.shortcuts import render
from dotenv import load_dotenv
from distutils.util import strtobool
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import redirect


def index(request):
    return render(request, "index.html")

def redirect_to_vercel_domain(request):
    # Replace with your Vercel domain
    return redirect('https://your-vercel-domain.vercel.app')

def redirect_to_aws_frontend(request):
    # Replace with your AWS frontend domain
    return redirect('https://your-aws-frontend-domain.com')

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

