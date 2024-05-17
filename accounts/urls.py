
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView, TokenVerifyView
from . import views

urlpatterns = [

    path('me/', views.MeView.as_view(), name='me'),
    path("api/user",views.UserView.as_view(),name="user"),
    path('api/token/obtain', TokenObtainPairView.as_view(), name='token_obtain'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    #path('activate/<uid>/<token>', views.ActivateUser.as_view({'get': 'activation'}), name='activation'),
    #path('register/', views.registration_view, name='register'),
]
