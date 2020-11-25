from rest_framework.response import Response
from rest_framework import renderers, schemas
from rest_framework.decorators import api_view, renderer_classes
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer

@api_view()
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer, renderers.CoreJSONRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='AVRIL API')
    return Response(generator.get_schema(request=request))