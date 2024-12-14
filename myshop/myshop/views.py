from django.shortcuts import render
import os
from rest_framework_simplejwt.exceptions import TokenError
from dotenv import load_dotenv
from distutils.util import strtobool
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import AuthenticationFailed
import subprocess
from django.http import JsonResponse
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
import subprocess

def index(request):
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
        if not refresh:
            return Response({'error': 'Refresh token is required'}, status=400)
        
        try:
            token = RefreshToken(refresh)
            new_access_token = {
                'access': str(token.access_token),
            }
            return Response(new_access_token)
        except TokenError as e:
            print(f"Error details: {str(e)}")
            raise AuthenticationFailed(f"Token refresh failed: {str(e)}")
        
class RedisPerformanceView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        try:
            # Run the management command and capture the output
            output = subprocess.check_output(['python', 'manage.py', 'redis_perfomance'], text=True)
            output_lines = output.splitlines()

            # Return the command output as JSON
            return Response({
                'status': 'success',
                'output': output_lines,
            })

        except subprocess.CalledProcessError as e:
            # Capture and return the specific error output for debugging
            return Response({
                'status': 'error',
                'message': e.output or str(e),  # Use the output attribute for more details if available
            }, status=500)

        except Exception as e:
            # General exception handler for unexpected errors
            return Response({
                'status': 'error',
                'message': f"An unexpected error occurred: {str(e)}",
            }, status=500)

class DatabasePerformanceView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        try:
            # Run the management command
            output = subprocess.check_output(['python', 'manage.py', 'db_perfomance'], text=True)
            output_lines = output.splitlines()

            # Return the output as JSON
            return Response({
                'status': 'success',
                'output': output_lines,
            })

        except subprocess.CalledProcessError as e:
            return Response({
                'status': 'error',
                'message': e.output or str(e),
            }, status=500)

        except Exception as e:
            return Response({
                'status': 'error',
                'message': f"An unexpected error occurred: {str(e)}",
            }, status=500)



class S3PerformanceView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        try:
            # Run the management command
            output = subprocess.check_output(['python', 'manage.py', 's3_perfomance'], text=True)
            output_lines = output.splitlines()

            # Return the output as JSON
            return Response({
                'status': 'success',
                'output': output_lines,
            })

        except subprocess.CalledProcessError as e:
            return Response({
                'status': 'error',
                'message': e.output or str(e),
            }, status=500)

        except Exception as e:
            return Response({
                'status': 'error',
                'message': f"An unexpected error occurred: {str(e)}",
            }, status=500)
