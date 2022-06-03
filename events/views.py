from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from constants import progress_data
from events.forms.event_form import EventForm
from events.forms.event_ticket_price_form import EventTicketTypePriceForm
from events.models import Event, EventImage
from entertainers.models import Entertainer
from eventdriven.shared_functions import run_query
from user.views import get_user_details
from home.models import Category, EventCategory, EventEntertainer, Location, EventTicketTypePrice


def event(request, event_id):
    if not event_id.isdigit():
        return JsonResponse(status=400, data={"message": "Invalid ID"})

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

    events_entertainers = run_query(
        Entertainer, 
        'events/queries/events_entertainers.sql', 
        {'event_id': event_id}
    )

    event_map_url = run_query(
        Location,
        'events/queries/event_map_url.sql',
        {'location_id': the_event.location.id}
    )

    if len(event_map_url) > 0:
        map_url = event_map_url[0].map_url
    else:
        map_url = ''

    event_price_and_ticket_type = run_query(
        EventTicketTypePrice,
        'events/queries/event_ticket_type_price.sql',
        {'event_id': event_id}
    )

    most_similar_events = run_query(
        Event,
        'events/queries/similar_events.sql',
        {'event_id': event_id}
    )



    return render(request, "pages/event/index.html", context={
        "event": the_event,
        "is_past": the_event.end_date < timezone.now(),
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
                return redirect('/event/create_event/' + str(event_.id))
            
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

    if request.user.is_superuser:
        the_event = Event.objects.get(pk=event_id)
        user_details = get_user_details(request.user)
        if request.method == 'POST':
            event_ticket_price_form = EventTicketTypePriceForm(request.POST)
            
            if event_ticket_price_form.is_valid():
                event_ticket_price_form.save()
                return redirect('/event/create_event/' + str(event_id))
            else:
                event_ticket_type_price = EventTicketTypePrice.objects.filter(
                    ticket_type_id=request.POST['ticket_type'],
                    event_id=request.POST['event']
                ).first()

                event_ticket_price_form2 = EventTicketTypePriceForm(instance=event_ticket_type_price, data=request.POST)
                if event_ticket_price_form2.is_valid():
                    event_ticket_price_form2.save()
                    return redirect('/event/create_event/' + str(event_id))
        
        else:
            event_ticket_price_form = EventTicketTypePriceForm(
                initial={'event': the_event}
            )
            
            day_month = the_event.start_date.strftime("%d %b")
            hour = the_event.start_date.strftime("%H:%M")
            year = the_event.start_date.strftime("%Y")
            day_month_to = the_event.end_date.strftime("%d %b")
            hour_to = the_event.end_date.strftime("%H:%M")
            year_to = the_event.end_date.strftime("%Y")

            events_entertainers = run_query(
                Event, 
                'events/queries/events_entertainers.sql', 
                {'event_id': event_id}
            )

            event_map_url = run_query(
                Location,
                'events/queries/event_map_url.sql',
                {'location_id': the_event.location.id}
            )

            if len(event_map_url) > 0:
                map_url = event_map_url[0].map_url
            else:
                map_url = ''

            event_price_and_ticket_type = run_query(
                EventTicketTypePrice,
                'events/queries/event_ticket_type_price.sql',
                {'event_id': event_id}
            )

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
                if i.id in this_events_selected_categories_list:
                    events_cate.append(i)
                else:
                    rest_events_cate.append(i)

            events_ent = []
            rest_events_ent = []
            this_events_selected_entertainers_list = []
            for i in this_events_selected_entertainers:
                this_events_selected_entertainers_list.append(i.entertainer_id)

            for i in Entertainer.objects.all():
                if i.id in this_events_selected_entertainers_list:
                    events_ent.append(i)
                else:
                    rest_events_ent.append(i)

            this_event_ticket_type_price = EventTicketTypePrice.objects.filter(
                event_id=event_id
            ).select_related('ticket_type')

            return render(request, 'pages/event/create_event_more_info.html', context={
                'event_ticket_price_form': event_ticket_price_form,
                "this_event_ticket_type_price": this_event_ticket_type_price,
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
