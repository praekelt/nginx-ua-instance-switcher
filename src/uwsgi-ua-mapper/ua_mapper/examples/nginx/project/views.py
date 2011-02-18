from django.shortcuts import render_to_response

def home(request):
    """
    Simple view demonstrating how the same view can utilize different templates (via instance specific TEMPLATE_DIRS setting)
    without the need to make view specific code changes.
    """
    return render_to_response('home.html')
