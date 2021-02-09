from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import GetFileView, PostFileView

schema_view = get_schema_view(
   openapi.Info(
      title="File Upload API",
      default_version='v1.0',
      description="Test Exercise",
      contact=openapi.Contact(email="jwbarnette@icloud.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('upload/', PostFileView.as_view(), name='post-upload'),
    path('upload/<upload_id>', GetFileView.as_view(), name='get-upload'),
]