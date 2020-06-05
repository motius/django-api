from django.conf import settings
from django.conf.urls import include
from django.urls import path
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin

from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
import health_check

# API Routes
router = DefaultRouter()

schema_view = get_schema_view(
   openapi.Info(
      title="API Documentation",
      default_version='v1',
      # Add a project description here
      description="Description",
      # Update the email
      contact=openapi.Contact(email="info@motius.de"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('api/docs/',schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^api/docs/swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # See https://github.com/encode/django-rest-framework/pull/5609
    # TODO: Switch when DRF can use namepsaces correctly
    # path('api/', include(router.urls, namespace='api')),
    path('api/', include((router.urls, 'api'), namespace='api')),
    path('api/auth/', include('rest_auth.urls')),
    path('api/auth/registration/', include('rest_auth.registration.urls')),
    url(r'^status/', include('health_check.urls')),
]

# Static routes
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
