from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from places.models import Place


def show_index_page(request):
    places = Place.objects.all()

    features = []
    for place in places:
        details_url = reverse('places:place_detail_api', args=[place.id])

        features.append({
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [place.longitude,
                                place.latitude],
            },
            'properties': {
                'title': place.title,
                'placeId': place.id,
                'detailsUrl': details_url
            }
        })

    places_geojson = {
        'type': 'FeatureCollection',
        'features': features
    }

    context = {
        'places_geojson': places_geojson
    }

    template = 'index.html'

    return render(request, template, context)


def place_detail_api_view(request, place_id):
    place = get_object_or_404(
        Place.objects.prefetch_related('images'),
        pk=place_id
    )

    place_details = {
        'title': place.title,
        'imgs': [img.image.url for img in place.images.all()],
        'description_short': place.short_description,
        'description_long': place.long_description,
        'coordinates': {
            'lat': place.latitude,
            'lng': place.longitude
        }
    }

    return JsonResponse(
        place_details,
        json_dumps_params={'ensure_ascii': False, 'indent': 4}
    )
