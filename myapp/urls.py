# myapp/urls.py
from django.urls import path
from .views import index, detect_crater_or_boulder_view

urlpatterns = [
    path('', index, name='index'),  # Index page
    path('detect/', detect_crater_or_boulder_view, name='detect_crater_or_boulder'),  # Detection endpoint
]
