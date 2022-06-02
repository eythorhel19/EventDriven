from django.http import JsonResponse
from django.shortcuts import render
from events.models import Event, EventImage
from user.views import get_user_details
from constants import progress_data
from django.contrib.auth.decorators import login_required
from events.forms.event_form import EventForm
# from events.forms.event_category_form import EventCategory
# from events.forms.event_entertainers_form import EventEntertainer
from events.forms.event_ticket_price_form import EventTicketTypePriceForm
from django.shortcuts import redirect
from home.models import Category, EventCategory, EventEntertainer
from entertainers.models import Entertainer
from home.models import EventTicketTypePrice, TicketType


def event(request, event_id):
    user_details = get_user_details(request.user)

    the_event = Event.objects.get(pk=event_id)
    extra_event_images = EventImage.objects.filter(event=the_event)
    day_month = the_event.start_date.strftime("%d %b")
    hour = the_event.start_date.strftime("%H:%M")
    year = the_event.start_date.strftime("%Y")
    day_month_to = the_event.end_date.strftime("%d %b")
    hour_to = the_event.end_date.strftime("%H:%M")
    year_to = the_event.end_date.strftime("%Y")

    event_images = [the_event.main_image_url]
    for ei in extra_event_images:
        event_images.append(ei.image_url)

    if not event_id.isdigit():
        return JsonResponse(status=400, data={"message": "Invalid ID"})

    events_entertainers = Event.objects.raw('''
        SELECT *
        FROM (
            SELECT DISTINCT ON (EENT.id) 
                EENT.id, 
                EENT.name, 
                EENT.description, 
                EENT.image_url, 
                MIN(EVE.start_date) AS next_event_id, 
                HLOC.name AS location_name
            FROM 
                ENTERTAINERS_ENTERTAINER AS EENT
                JOIN HOME_EVENTENTERTAINER AS HEVENT 
                ON EENT.id = HEVENT.entertainer_id
                JOIN EVENTS_EVENT AS EVE 
                ON EVE.id = HEVENT.event_id
                JOIN HOME_LOCATION AS HLOC 
                ON HLOC.id = EVE.location_id
            WHERE 
                EVE.start_date >= CURRENT_DATE
            GROUP BY 
                EENT.id, EENT.name, EENT.description, EENT.image_url, HLOC.name, EVE.id, EVE.start_date
            HAVING 
                EVE.ID = {}) AS FRO_GROUP_BY
        ORDER BY 
            FRO_GROUP_BY.next_event_id;'''.format(event_id)
    )

    event_map_url = ('''
        SELECT *
        FROM HOME_LOCATION AS HLOC
        WHERE HLOC.id = {}
        '''.format(the_event.location.id)
    )
    event_map_url = Event.objects.raw(event_map_url)

    map_url = event_map_url[0].map_url

    event_price_and_ticket_type = Event.objects.raw('''
    SELECT *
    FROM HOME_EVENTTICKETTYPEPRICE AS HETT
    JOIN HOME_TICKETTYPE AS HTT ON HTT.id = HETT.ticket_type_id
    WHERE HETT.event_id = {}
    '''.format(event_id))

    most_similar_events = Event.objects.raw('''
    SELECT *
    FROM (
        SELECT 
            THIS_EVENT.id, 
            THIS_EVENT.title, 
            THIS_EVENT.description, 
            THIS_EVENT.maximum_capacity, 
            THIS_EVENT.start_date, 
            THIS_EVENT.end_date, 
            THIS_EVENT.location_id, 
            THIS_EVENT.main_image_url, 
            COUNT(*) as apperances
        FROM
            EVENTS_EVENT AS THIS_EVENT
            -- Joining on event entertainer table
            JOIN HOME_EVENTENTERTAINER AS HEENT 
            ON HEENT.event_id = THIS_EVENT.id
            
            -- Joining on event category table
            JOIN HOME_EVENTCATEGORY AS HECAT 
            ON HECAT.event_id = THIS_EVENT.id
        WHERE
            HEENT.entertainer_id IN (
                SELECT HEENT.entertainer_id
                FROM EVENTS_EVENT AS EEVE
                JOIN HOME_EVENTENTERTAINER AS HEENT ON HEENT.event_id = EEVE.id
                JOIN HOME_EVENTCATEGORY AS HECAT ON HECAT.event_id = EEVE.id
                WHERE 
                    EEVE.id = {}
            ) OR 
            HECAT.category_id IN (
                SELECT HECAT.category_id
                FROM EVENTS_EVENT AS EEVE
                JOIN HOME_EVENTENTERTAINER AS HEENT 
                ON HEENT.event_id = EEVE.id
                JOIN HOME_EVENTCATEGORY AS HECAT 
                ON HECAT.event_id = EEVE.id
                WHERE EEVE.id = {}
            ) AND THIS_EVENT.id != {}
        GROUP BY 
            THIS_EVENT.id, 
            THIS_EVENT.title, 
            THIS_EVENT.description, 
            THIS_EVENT.maximum_capacity, 
            THIS_EVENT.start_date, 
            THIS_EVENT.end_date, 
            THIS_EVENT.location_id, 
            THIS_EVENT.main_image_url
        ORDER BY 
            apperances DESC
        ) AS MOST_SIMILAR_EVENTS
        JOIN HOME_LOCATION AS HLOC 
        ON HLOC.id = MOST_SIMILAR_EVENTS.location_id;
    '''.format(event_id, event_id, event_id))

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
        'progress_data': progress_data,
        "most_similar_events": most_similar_events
    })


@login_required
def create_event(request):
    if request.user.is_superuser:
        user_details = get_user_details(request.user)
        if request.method == 'POST':
            event_form = EventForm(request.POST)
            if event_form.is_valid():
                event_ = event_form.save()
                return redirect('event/create_event/' + str(event_.id))
        else:
            event_form = EventForm()
        return render(request, 'pages/event/create_event.html', context={
            'event_form': event_form,
            'user_details': user_details
        })
    else:
        return redirect('dashboard')


@login_required
def create_event_more_info(request, event_id):
    the_event = Event.objects.get(pk=event_id)
    day_month = the_event.start_date.strftime("%d %b")
    hour = the_event.start_date.strftime("%H:%M")
    year = the_event.start_date.strftime("%Y")
    day_month_to = the_event.end_date.strftime("%d %b")
    hour_to = the_event.end_date.strftime("%H:%M")
    year_to = the_event.end_date.strftime("%Y")

    events_entertainers = Event.objects.raw('''
        SELECT *
        FROM (
            SELECT DISTINCT ON (EENT.ID) EENT.id, 
                EENT.name,
                EENT.description, 
                EENT.image_url, 
                MIN(EVE.start_date) AS NEXT_EVENT_DATE, 
                HLOC.name AS LOCATION_NAME
            FROM 
                ENTERTAINERS_ENTERTAINER AS EENT
                JOIN HOME_EVENTENTERTAINER AS HEVENT 
                ON EENT.id = HEVENT.entertainer_id
                JOIN EVENTS_EVENT AS EVE 
                ON EVE.id = HEVENT.event_id
                JOIN HOME_LOCATION AS HLOC 
                ON HLOC.id = EVE.location_id
            WHERE 
                EVE.start_date >= CURRENT_DATE
            GROUP BY
                EENT.id, EENT.name, EENT.description, EENT.image_url, HLOC.name, EVE.id, EVE.start_date
            HAVING 
                EVE.id = {}
            ) AS FRO_GROUP_BY
        ORDER BY 
            FRO_GROUP_BY.next_event_date;'''.format(event_id)
    )

    event_map_url = ('''
        SELECT *
        FROM HOME_LOCATION AS HLOC
        WHERE HLOC.id = {}
        '''.format(the_event.location.id)
    )
    event_map_url = Event.objects.raw(event_map_url)
    map_url = event_map_url[0].map_url

    event_price_and_ticket_type = Event.objects.raw('''
    SELECT *
    FROM HOME_EVENTTICKETTYPEPRICE AS HETT
    JOIN HOME_TICKETTYPE AS HTT ON HTT.id = HETT.ticket_type_id
    WHERE HETT.event_id = {}
    '''.format(event_id))

    if request.user.is_superuser:
        user_details = get_user_details(request.user)
        if request.method == 'POST':
            #     event_category_form = EventCategory(request.POST)
            #     event_entertainer_form = EventEntertainer(request.POST)
            event_ticket_price_form = EventTicketTypePriceForm(request.POST)
            #     if event_category_form.is_valid():
            #         event_category_form.save()
            #         return redirect('/event/create_event/'+str(event_id))
            #     elif event_entertainer_form.is_valid():
            #         event_entertainer_form.save()
            #         return redirect('/event/create_event/'+str(event_id))
            if event_ticket_price_form.is_valid():
                event_ticket_price_form.save()
                return redirect('/event/create_event/'+str(event_id))
        else:
            #     event_category_form = EventCategory(initial={'event': the_event})
            #     event_entertainer_form = EventEntertainer(
            #         initial={'event': the_event})
            event_ticket_price_form = EventTicketTypePriceForm(
                initial={'event': the_event})

        this_events_selected_categories = EventCategory.objects.filter(
            event_id=event_id)
        this_events_selected_entertainers = EventEntertainer.objects.filter(
            event_id=event_id)

        events_cate = []
        rest_events_cate = []
        this_events_selected_categories_list = []
        for i in this_events_selected_categories:
            this_events_selected_categories_list.append(i.category_id)

        for i in Category.objects.all():
            if(i.id in this_events_selected_categories_list):
                events_cate.append(i)
            else:
                rest_events_cate.append(i)

        events_ent = []
        rest_events_ent = []
        this_events_selected_entertainers_list = []
        for i in this_events_selected_entertainers:

            this_events_selected_entertainers_list.append(i.entertainer_id)

        for i in Entertainer.objects.all():
            if(i.id in this_events_selected_entertainers_list):
                events_ent.append(i)
            else:
                rest_events_ent.append(i)

        return render(request, 'pages/event/create_event_more_info.html', context={
            # 'event_category_form': event_category_form,
            # 'event_entertainer_form': event_entertainer_form,
            'event_ticket_price_form': event_ticket_price_form,
            "this_event_ticket_type_price": EventTicketTypePrice.objects.filter(event_id=event_id),
            'user_details': user_details,
            "event_id": event_id,
            "event": the_event,
            "day_month": day_month,
            "hour": hour,
            "year": year,
            "day_month_to": day_month_to,
            "hour_to": hour_to,
            "year_to": year_to,
            "events_entertainers": events_entertainers,
            "map_url": map_url,
            "event_price_and_ticket_type": event_price_and_ticket_type,
            'progress_data': progress_data,
            "Category": rest_events_cate,
            "EventCategory": events_cate,
            "Entertainer": rest_events_ent,
            "EventEntertainer": events_ent,

        })
    else:
        return redirect('dashboard')
