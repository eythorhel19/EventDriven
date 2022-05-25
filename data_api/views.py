from django.shortcuts import render
import json
from django.http import JsonResponse
from events.models import Event
from django.forms.models import model_to_dict
# Create your views here.


def event(request, event_id):

    if not event_id.isdigit():
        return JsonResponse(status=400, data={'message': 'event_id must be a integer!'})


    events = Event.objects.raw('''
        SELECT
            E.id,
            E.title,
            E.description,
            E.start_date,
            CONCAT(L.name,', ',C.name) AS location_name,
            E.main_image_url
        FROM events_event AS E
        INNER JOIN home_location AS L
        ON E.location_id = L.id
        INNER JOIN home_city AS C
        ON L.city_id = C.id
        WHERE E.id = {};
    '''.format(event_id))

    if len(events) == 0:
        return JsonResponse(status=400, data={'message': 'Event not found!'})
    else:
        event_dict = model_to_dict(events[0])
        return JsonResponse(event_dict)
