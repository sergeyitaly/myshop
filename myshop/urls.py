from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib import admin

# Schema view for API documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Djoser API",
        default_version="v1",
        description="REST implementation of Django authentication system.",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # API documentation URLs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # Authentication URLs
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('djoser.urls.authtoken')),

    # App-specific URLs
    path('', include('accounts.urls')),  # Example: /accounts/
    path('', include('shop.urls')),      # Example: /products/
    path('admin/', admin.site.urls),     # Admin URLs: /admin/

    # Debug view
    path('debug/', TemplateView.as_view(template_name='base.html'), name='debug'),

    # Default URL (index.html)
    path('index/', TemplateView.as_view(template_name='index.html'), name='index'),
]

# Serve media and static files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
