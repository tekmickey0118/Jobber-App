from rest_framework.renderers import JSONRenderer

class UTF8JSONRender(JSONRenderer):
    charset = 'utf-8'
