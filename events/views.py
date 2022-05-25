from django.shortcuts import render
from events.models import Event, EventImage

# Create your views here.


def event(request, event_id):

    the_event = Event.objects.get(pk=event_id)

    return render(request, "pages/event/index.html", context={'event': the_event})
