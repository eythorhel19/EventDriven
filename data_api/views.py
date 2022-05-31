from django.http import JsonResponse
from django.forms.models import model_to_dict

from events.models import Event
from home.models import Ticket, TicketType
from home.models import Country, City

from rest_framework.decorators import api_view

# Create your views here.


@api_view(['GET'])
def event(request, event_id):

    if not event_id.isdigit():
        return JsonResponse(status=400, data={'message': 'event_id must be a integer!'})

    events = Event.objects.raw('''
        SELECT
            E.id,
            E.title,
            E.description,
            E.start_date,
            E.end_date,
            CONCAT(L.name,', ',C.name) AS location_name,
            E.main_image_url
        FROM events_event AS E
        INNER JOIN home_location AS L
        ON E.location_id = L.id
        INNER JOIN home_city AS C
        ON L.city_id = C.id
        WHERE E.id = {};
    '''.format(event_id))

    ticket_types_result = TicketType.objects.raw('''
    SELECT
        TT.*,
        ETTP.price,
        CONCAT(TT.description,' - ', ETTP.price) AS option_description
    FROM
        home_tickettype AS TT
        INNER JOIN home_eventtickettypeprice AS ETTP
        ON TT.id = ETTP.ticket_type_id
    WHERE
        ETTP.event_id = {};
    '''.format(event_id))

    ticket_types = []
    for tt in ticket_types_result:
        ticket_types.append({
            'ticket_type_id': tt.id,
            'description': tt.description,
            'option_description': tt.option_description,
            'price': tt.price
        })

    if len(events) == 0:
        return JsonResponse(status=400, data={'message': 'Event not found!'})
    else:
        event_dict = model_to_dict(events[0])

        event_dict['location_name'] = events[0].location_name
        event_dict['ticket_types'] = ticket_types

        if events[0].start_date == events[0].end_date:
            event_dict['date_description'] = "{}".format(
                events[0].start_date.strftime("%d. %B"))
        else:
            event_dict['date_description'] = "{} to {}".format(
                events[0].start_date.strftime("%d. %B"),
                events[0].end_date.strftime("%d. %B")
            )
        return JsonResponse(event_dict)


@api_view(['GET'])
def countries(request):
    c = Country.objects.values()

    country_list = []
    for elem in c:
        country_list.append(elem)

    return JsonResponse(country_list, safe=False)


@api_view(['GET'])
def cities(request):

    country_id = request.GET.get("country_id", -1)

    print(country_id)

    if country_id == -1:
        c = City.objects.values()
    else:
        c = City.objects.filter(country_id=country_id).values()

    city_list = []
    for elem in c:
        city_list.append(elem)

    return JsonResponse(city_list, safe=False)


@api_view(['POST'])
def book_ticket(request):
    ticket = Ticket.objects.create(

    )

    return JsonResponse({"it": "works!"})


@api_view(['PUT'])
def user_categories(request):
    print('user_categories', request)

    return JsonResponse(status=200, data={'message': 'OK'})


@api_view(['PUT'])
def user_entertainers(request):
    print('user_entertainers', request)

    return JsonResponse(200, data={'message': 'OK'})
