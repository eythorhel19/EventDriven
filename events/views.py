from django.shortcuts import render
from events.models import Event
# from entertainers.models import Entertainers
# Create your views here.


def event(request, event_id):

    the_event = Event.objects.get(pk=event_id)
    day_month = the_event.start_date.strftime("%d %b")
    hour = the_event.start_date.strftime("%H:%M")
    year = the_event.start_date.strftime("%Y")
    # the_artists = Entertainers.objects.filter(event=the_event)

    if not event_id.isdigit():
        return HttpResponse(status=400, content="Invalid ID")

    events_entertainers = Event.objects.raw('''
        SELECT ENT.*
        FROM ENTERTAINERS_ENTERTAINER AS ENT
        JOIN HOME_EVENTENTERTAINER AS HEE ON ENT.ID = HEE.ENTERTAINER_ID
        JOIN EVENTS_EVENT AS EVE ON HEE.EVENT_ID = EVE.ID
        WHERE EVE.ID = {}
        ORDER BY EVE.START_DATE'''.format(event_id)
    )

    return render(request, "pages/event/index.html", context={'event': the_event, "day_month": day_month, "hour": hour, "year": year, "events_entertainers": events_entertainers})
