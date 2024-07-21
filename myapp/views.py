# myapp/views.py
from django.http import JsonResponse
from django.shortcuts import render
from .detect_crater_boulder import detect_crater_or_boulder
import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request, 'base.html')

@csrf_exempt  # Optional: Use this decorator to bypass CSRF checks for testing purposes
def detect_crater_or_boulder_view(request):
    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_file = request.FILES['image']
        file_path = default_storage.save(uploaded_file.name, uploaded_file)
        absolute_file_path = os.path.join(settings.MEDIA_ROOT, file_path)
        
        output_file_path = os.path.join(settings.MEDIA_ROOT, 'output_' + uploaded_file.name)
        
        # Call your crater/boulder detection function
        output_image_path, message = detect_crater_or_boulder(absolute_file_path, output_file_path)
        
        # Construct the URL for the output image
        output_image_url = default_storage.url(output_image_path)

        # Return the result as JSON
        return JsonResponse({'image_url': output_image_url, 'message': message})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
