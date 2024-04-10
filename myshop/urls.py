from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib import admin
import debug_toolbar


schema_view = get_schema_view(
    openapi.Info(
        title="Djoser API",
        default_version="v1",
        description="REST implementation of Django authentication system. djoser library provides a set of Django Rest Framework views to handle basic actions such as registration, login, logout, password reset and account activation. It works with custom user model.",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path("admin/", include("admin.urls")),  # Include admin URLs

    # Include API documentation URLs
    path('swagger<format>/', include('schema_view.without_ui(cache_timeout=0)'), name='schema-json'),
    path('swagger/', include('schema_view.with_ui('swagger', cache_timeout=0)'), name='schema-swagger-ui'),
    path('redoc/', include('schema_view.with_ui('redoc', cache_timeout=0)'), name='schema-redoc'),

    # Include app-specific URLs (e.g., shop, accounts, auth)
    path('', include('shop.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('accounts.urls')),

    # Debug URL
    path('debug/', TemplateView.as_view(template_name='base.html'), name='debug'),

    # Catch-all URL to serve index.html for frontend routes
    path('', TemplateView.as_view(template_name='frontend/index.html'), name='frontend'),
]

if settings.DEBUG:
    # Serve static and media files during development
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)