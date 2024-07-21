# isrodjango/urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from myapp.views import index, detect_crater_or_boulder_view

urlpatterns = [
    path('', index, name='index'),
    path('detect/', detect_crater_or_boulder_view, name='detect_crater_or_boulder'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
