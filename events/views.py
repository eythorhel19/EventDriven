from django.http import JsonResponse
from django.shortcuts import render
from events.models import Event, EventImage
from user.views import get_user_details
from constants import progress_data


def event(request, event_id):
    user_details = get_user_details(request.user)

    the_event = Event.objects.get(pk=event_id)
    extra_event_images = EventImage.objects.filter(event = the_event)
    day_month = the_event.start_date.strftime("%d %b")
    hour = the_event.start_date.strftime("%H:%M")
    year = the_event.start_date.strftime("%Y")
    day_month_to = the_event.end_date.strftime("%d %b")
    hour_to = the_event.end_date.strftime("%H:%M")
    year_to = the_event.end_date.strftime("%Y")
    # the_artists = Entertainers.objects.filter(event=the_event)

    event_images = [the_event.main_image_url]
    for ei in extra_event_images:
        event_images.append(ei.image_url)
    
    print(event_images)

    if not event_id.isdigit():
        return JsonResponse(status=400, data={"message": "Invalid ID"})

    events_entertainers = Event.objects.raw('''
        SELECT *
        FROM (
        SELECT DISTINCT ON (EENT.ID) EENT.ID, EENT.NAME, EENT.DESCRIPTION, EENT.IMAGE_URL, MIN(EVE.START_DATE) AS NEXT_EVENT_DATE, HLOC.NAME AS LOCATION_NAME
        FROM ENTERTAINERS_ENTERTAINER AS EENT
        JOIN HOME_EVENTENTERTAINER AS HEVENT ON EENT.ID = HEVENT.ENTERTAINER_ID
        JOIN EVENTS_EVENT AS EVE ON EVE.ID = HEVENT.EVENT_ID
        JOIN HOME_LOCATION AS HLOC ON HLOC.ID = EVE.LOCATION_ID
        WHERE EVE.START_DATE >= CURRENT_DATE
        GROUP BY EENT.ID, EENT.NAME, EENT.DESCRIPTION, EENT.IMAGE_URL, HLOC.NAME, EVE.ID, EVE.START_DATE
        HAVING EVE.ID = {}) AS FRO_GROUP_BY
        ORDER BY FRO_GROUP_BY.NEXT_EVENT_DATE'''.format(event_id)
                                            )

    event_map_url = ('''
        SELECT *
        FROM HOME_LOCATION AS HLOC
        WHERE HLOC.ID = {}
        '''.format(the_event.location.id)
    )
    event_map_url = Event.objects.raw(event_map_url)

    map_url = event_map_url[0].map_url

    event_price_and_ticket_type = Event.objects.raw('''
    SELECT *
    FROM HOME_EVENTTICKETTYPEPRICE AS HETT
    JOIN HOME_TICKETTYPE AS HTT ON HTT.ID = HETT.TICKET_TYPE_ID
    WHERE HETT.EVENT_ID = {}
    '''.format(event_id))

    return render(request, "pages/event/index.html", context={
        "event": the_event,
        "event_images": event_images,
        "day_month": day_month,
        "hour": hour,
        "year": year,
        "day_month_to": day_month_to,
        "hour_to": hour_to,
        "year_to": year_to,
        "events_entertainers": events_entertainers,
        "map_url": map_url,
        "user_details": user_details,
        "event_price_and_ticket_type": event_price_and_ticket_type,
        'progress_data': progress_data
    })
