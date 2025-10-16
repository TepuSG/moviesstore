from django.shortcuts import render
from django.conf import settings

def map_view(request):
    template_data = {
        'title': 'Movie Map',
        'mapbox_key': settings.MAPBOX_KEY,
    }
    return render(request, 'moviemap/moviemap.html', {'template_data': template_data})

# Create your views here.
