from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib import admin
from dotenv import load_dotenv
from . import views
from django.views.generic import RedirectView
from .views import CustomTokenObtainPairView, CustomTokenRefreshView
from django.conf.urls.i18n import i18n_patterns
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.contrib import admin
from dotenv import load_dotenv
from drf_spectacular.views import SpectacularRedocView
from django.views.decorators.cache import cache_page
from .views import *

load_dotenv()
schema_view = get_schema_view(
    openapi.Info(
        title="KOLORYT API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # Authentication URLs
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('djoser.urls.authtoken')),

    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # App-specific URLs
    path('api/', include('accounts.urls')), 
    path('api/', include('shop.urls')), 
    path('api/', include('order.urls')),
    path('api/', include('team.urls')),
    path('api/', include('brand.urls')),
    path('api/', include('comments.urls')),
    path('api/', include('intro.urls')),
    path('api/', include('technologies.urls')),
    path('api/', include('feedback.urls')),
    path('api/', include('logs.urls')),
    path('api/', include('mycelery.urls')),

    path('admin/', admin.site.urls),
    path('rosetta/', include('rosetta.urls')), 
#    path("", cache_page(60 * 15)(views.index), name="index"),  
#    path("", views.index, name="index"),  
    path("", cache_page(60 * 15)(views.index), name="index"),
    path('redis/', RedisPerformanceView.as_view(), name='redis_performance'),
    path('db/', DatabasePerformanceView.as_view(), name='database_performance'),
    path('s3/', S3PerformanceView.as_view(), name='s3_performance'),


#    re_path(r'^(?:.*)/?$', views.index),  # Catch all other routes and serve the same view
    path('i18n/', include('django.conf.urls.i18n')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    if len(settings.STATICFILES_DIRS) > 1:
        urlpatterns += static('/assets/', document_root=settings.STATICFILES_DIRS[1])

# Catch-all URL pattern fnor handling unmatched URLs
urlpatterns += [
#    re_path(r'^.*$', RedirectView.as_view(url='/')),
re_path(r'^(?:.*)/?$', views.index)
]
