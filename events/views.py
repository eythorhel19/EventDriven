from django.shortcuts import render
from events.models import Event, EventImage

# Create your views here.


def event(request, event_id):

    the_event = Event.objects.get(pk=event_id)
    event_image = EventImage.objects.get(event_id=event_id, main=True)
    day_month = the_event.start_date.strftime("%d %b")
    hour = the_event.start_date.strftime("%H:%M")
    year = the_event.start_date.strftime("%Y")
    # print('day_month', day_month)
    # print('hour', hour)
    # print('year', year)

    return render(request, "pages/event/index.html", context={'event': day_month, "day_month": day_month, "hour": hour, "year": year, 'event_image': event_image})
