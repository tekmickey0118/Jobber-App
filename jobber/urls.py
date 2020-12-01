from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url, include
from rest_framework import routers, serializers, viewsets
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer
from .swagger_schema import SwaggerSchemaView
from .views import save_medical

schema_view = get_schema_view(title='Jobber API', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])


urlpatterns = [
    url(r'^swagger/', SwaggerSchemaView.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('api/v1/users/', include('users.urls')),
    path('api/v1/work/', include('jobberwork.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
