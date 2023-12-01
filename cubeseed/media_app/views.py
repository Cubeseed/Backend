# Create your views here.
from django.conf import settings
from django.http import HttpResponse, Http404
from django.views.static import serve

def serve_media(request, path):
    # Delegate to Django's built-in serve view for serving media files
    return serve(request, path, document_root=settings.MEDIA_ROOT)