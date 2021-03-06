import json
from django.http import JsonResponse, HttpResponse
from django.forms.models import model_to_dict
from django.contrib.auth.models import AnonymousUser
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required

from events.models import Event
from eventdriven.shared_functions import run_query
from home.models import Ticket, TicketType, EventTicketTypePrice, Country, City, UserFavoriteCategory, \
    UserFavoriteEntertainer, EventCategory, EventEntertainer
from user.views import get_user_details


def check_required_fields(req_body, required_fields):
    for key in required_fields:
        if key not in req_body:
            return 400, 'Request body missing field "{}"!'.format(key)

    if len(req_body.keys()) != len(required_fields):
        return 400, 'Request body includes to many fields!'

    return 200, ''


@api_view(['GET'])
def event(request, event_id):

    if not event_id.isdigit():
        return JsonResponse(status=400, data={'message': 'event_id must be a integer!'})

    # Getting the event info
    event_info = run_query(
        Event,
        'data_api/queries/event_info.sql',
        options={'event_id': event_id}
    )

    # Getting the events ticket types
    ticket_types_result = run_query(
        TicketType,
        'data_api/queries/event_ticket_types.sql',
        options={'event_id': event_id}
    )

    ticket_types = []
    for tt in ticket_types_result:
        ticket_types.append({
            'ticket_type_id': tt.id,
            'description': tt.description,
            'option_description': tt.option_description,
            'price': tt.price
        })

    if len(event_info) == 0:
        return JsonResponse(status=400, data={'message': 'Event not found!'})
    else:
        event_dict = model_to_dict(event_info[0])

        event_dict['location_name'] = event_info[0].location_name
        if event_info[0].tickets_sold is None:
            event_dict['tickets_sold'] = 0
        else:
            event_dict['tickets_sold'] = event_info[0].tickets_sold
            event_dict['tickets_available'] = True

        if event_info[0].available_tickets is None:
            event_dict['tickets_available'] = False
        else:
            event_dict['tickets_available'] = True

        event_dict['ticket_types'] = ticket_types

        if event_info[0].start_date == event_info[0].end_date:
            event_dict['date_description'] = "{}".format(
                event_info[0].start_date.strftime("%d. %B"))
        else:
            event_dict['date_description'] = "{} to {}".format(
                event_info[0].start_date.strftime("%d. %B"),
                event_info[0].end_date.strftime("%d. %B")
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

    if country_id == -1:
        c = City.objects.values()
    else:
        c = City.objects.filter(country_id=country_id).values()

    city_list = []
    for elem in c:
        city_list.append(elem)

    return JsonResponse(city_list, safe=False)


@api_view(['POST'])
def generate_tickets(request):
    if request.headers['Content-Type'] != 'application/json':
        return JsonResponse(status=400, data={'message': 'Request body should be of type json!'})

    req_body = json.loads(request.body)

    required_fields = ['event_id', 'ticket_type_id', 'quantity']
    status, msg = check_required_fields(req_body, required_fields)
    if status != 200:
        return JsonResponse(status=status, data={'message': msg})

    # Checks for event id
    if not isinstance(req_body['event_id'], int):
        return JsonResponse(status=400, data={'message': 'Field "event_id" should be an integer!'})

    the_event = Event.objects.filter(pk=req_body['event_id']).first()

    if the_event is None:
        return JsonResponse(status=400, data={'message': 'Event with id {} not found!'.format(req_body['event_id'])})

    # Checks for ticket type id
    if not isinstance(req_body['ticket_type_id'], int):
        return JsonResponse(status=400, data={'message': 'Field "ticket_type_id" should be an integer!'})

    ticket_type = EventTicketTypePrice.objects.filter(
        event_id=req_body['event_id'],
        ticket_type_id=req_body['ticket_type_id']
    ).first()

    if ticket_type is None:
        return HttpResponse('Ticket type {} is not defined for event {}'.format(
            req_body['ticket_type_id'],
            req_body['event_id'])
        )

    # Checks for quantity
    if not isinstance(req_body['quantity'], int):
        return JsonResponse(status=400, data={'message': 'Field "quantity" should be an integer'})

    current_ticket_count = len(
        Ticket.objects.filter(event_id=req_body['event_id']))

    if req_body['quantity'] > (the_event.maximum_capacity - current_ticket_count):
        return JsonResponse(
            status=400,
            data={
                'message': 'Tickets not available, maximum tickets available are {}'.format(
                    the_event.maximum_capacity - current_ticket_count
                )
            }
        )

    # Creating the tickets
    tickets = []
    for _ in range(req_body['quantity']):
        t = Ticket(
            ticket_type_id=req_body['ticket_type_id'],
            event_id=req_body['event_id']
        )
        tickets.append(t)

    Ticket.objects.bulk_create(tickets)

    return JsonResponse(status=200, data={'message': 'Successfully created {} tickets'.format(req_body['quantity'])})


@api_view(['PATCH'])
def release_tickets(request):
    if request.headers['Content-Type'] != 'application/json':
        return JsonResponse(status=400, data={'message': 'Request body should be of type json!'})

    req_body = json.loads(request.body)

    required_fields = ['event_id']
    status, msg = check_required_fields(req_body, required_fields)
    if status != 200:
        return HttpResponse(msg, status=status)

    # Checks for event id
    if not isinstance(req_body['event_id'], int):
        return JsonResponse(status=400, data={'message': 'Field "event_id" should be an integer!'})

    the_event = Event.objects.filter(pk=req_body['event_id']).first()

    if the_event is None:
        return JsonResponse(status=400, data={'message': 'Event with id {} not found!'.format(req_body['event_id'])})

    the_tickets = Ticket.objects.filter(
        event_id=req_body['event_id'], status='U')

    for t in the_tickets:
        t.status = 'R'

    Ticket.objects.bulk_update(the_tickets, fields=['status'])

    return JsonResponse(status=200, data={'message': 'Successfully released {} tickets!'.format(len(the_tickets))})


@api_view(['PATCH'])
def book_tickets(request):
    if isinstance(request.user, AnonymousUser):
        user = None
    else:
        user = request.user

    # Finding a ticket for the event
    if request.headers['Content-Type'] != 'application/json':
        return JsonResponse(status=400, data={'message': 'Request body should be of type json!'})

    req_body = json.loads(request.body)

    if 'delivery_method' not in req_body:
        return JsonResponse(status=400, data={'message': 'Request body missing field "delivery_method"!'})

    if req_body['delivery_method'] == 'E':
        required_fields = ['ticket_type_id', 'event_id', 'delivery_method',
                           'email', 'first_name', 'last_name', 'quantity', 'phone_country', 'phone_number']
        status, msg = check_required_fields(req_body, required_fields)
        if status != 200:
            return JsonResponse(status=status, data={'message': msg})

        available_tickets = Ticket.objects.filter(
            event_id=req_body['event_id'],
            ticket_type_id=req_body['ticket_type_id'],
            status='R'
        )

        if req_body['quantity'] > 10:
            return JsonResponse(
                status=400,
                data={
                    'message': 'Quantity is too large, only a maximum of 10 tickets can be bought!'
                }
            )

        if len(available_tickets) < req_body['quantity']:
            return JsonResponse(status=400, data={'message': 'Quantity is too large, only {} tickets available.'.format(
                len(available_tickets))}
            )

        booked_tickets = []
        for i, t in enumerate(available_tickets):
            if i >= req_body['quantity']:
                break
            else:
                if user is not None:
                    t.user = user

                t.delivery_method = req_body['delivery_method']
                t.email = req_body['email']
                t.status = 'S'
                t.first_name = req_body['first_name']
                t.last_name = req_body['last_name']
                t.phone_country_id = req_body['phone_country']
                t.phone_number = req_body['phone_number']
                t.save()
                booked_tickets.append(t)

        return_dict = []
        for ticket in booked_tickets:
            return_dict.append(model_to_dict(ticket))

        return JsonResponse(return_dict, safe=False)

    elif req_body['delivery_method'] == 'P':
        required_fields = ['ticket_type_id', 'event_id', 'delivery_method', 'email',
                           'first_name', 'last_name', 'street_name', 'house_number',
                           'postal_code', 'quantity', 'phone_country', 'phone_number']

        status, msg = check_required_fields(req_body, required_fields)
        if status != 200:
            return HttpResponse(msg, status=status)

        available_tickets = Ticket.objects.filter(
            event_id=req_body['event_id'],
            ticket_type_id=req_body['ticket_type_id'],
            status='R'
        )

        if req_body['quantity'] > 10:
            return JsonResponse(
                status=400,
                data={
                    'message': 'Quantity is too large, only a maximum of 10 tickets can be bought!'
                }
            )

        if len(available_tickets) < req_body['quantity']:
            return JsonResponse(
                status=400,
                data={
                    'message': 'Quantity is too large, only {} tickets available.'.format(len(available_tickets))
                }
            )

        booked_tickets = []
        for i, t in enumerate(available_tickets):
            if i >= req_body['quantity']:
                break
            else:
                if user is not None:
                    t.user = user
                t.delivery_method = req_body['delivery_method']
                t.email = req_body['email']
                t.status = 'S'
                t.first_name = req_body['first_name']
                t.last_name = req_body['last_name']
                t.street_name = req_body['street_name']
                t.house_number = req_body['house_number']
                t.postal_code = req_body['postal_code']
                t.phone_country_id = req_body['phone_country']
                t.phone_number = req_body['phone_number']
                t.save()
                booked_tickets.append(t)

        return_dict = []
        for ticket in booked_tickets:
            return_dict.append(model_to_dict(ticket))

        return JsonResponse(return_dict, safe=False)

    else:
        return JsonResponse(
            status=400,
            data={
                'message': 'Delivery method "{}" not available!'.format(req_body['delivery_method'])
            }
        )


@api_view(['PUT'])
def user_categories(request):
    if request.headers['Content-Type'] != 'application/json':
        return HttpResponse('Request body should be of type json!', status=400)

    UserFavoriteCategory.objects.filter(user_id=request.user.id).delete()

    req_body = json.loads(request.body)
    for i in req_body["users_fav_cat_selected"]:
        UserFavoriteCategory.objects.create(
            user_id=request.user.id,
            category_id=i['id']
        )

    return JsonResponse(status=200, data={'message': 'OK'})


@api_view(['PUT'])
def user_entertainers(request):

    if request.headers['Content-Type'] != 'application/json':
        return HttpResponse('Request body should be of type json!', status=400)

    UserFavoriteEntertainer.objects.filter(user_id=request.user.id).delete()
    req_body = json.loads(request.body)

    for i in req_body['select_entertainers']:
        UserFavoriteEntertainer.objects.create(
            user_id=request.user.id,
            entertainer_id=i['id']
        )

    return JsonResponse(status=200, data={'message': 'OK'})


@api_view(['GET'])
def user_info(request):
    user_details = get_user_details(request.user)

    if user_details is None:
        return JsonResponse(status=404, data={'message': 'User not found!'})
    else:
        user_details_dict = model_to_dict(user_details)
        user_details_dict['first_name'] = request.user.first_name
        user_details_dict['last_name'] = request.user.last_name
        user_details_dict['email'] = request.user.email
        del user_details_dict['id']
        del user_details_dict['user']
        del user_details_dict['profile_image_url']
        return JsonResponse(status=200, data=user_details_dict)


@api_view(['PUT'])
@login_required
def event_categories(request):

    if request.headers['Content-Type'] != 'application/json':
        return HttpResponse('Request body should be of type json!', status=400)

    req_body = json.loads(request.body)
    EventCategory.objects.filter(event_id=req_body['event_id']).delete()

    for i in req_body['event_categories']:
        EventCategory.objects.create(
            event_id=req_body['event_id'],
            category_id=i['id']
        )

    return JsonResponse(status=200, data={'message': 'OK'})


@api_view(['PUT'])
@login_required
def event_entertainers(request):

    if request.headers['Content-Type'] != 'application/json':
        return HttpResponse('Request body should be of type json!', status=400)

    req_body = json.loads(request.body)
    EventEntertainer.objects.filter(event_id=req_body['event_id']).delete()

    for i in req_body['event_entertainers']:
        EventEntertainer.objects.create(
            event_id=req_body['event_id'],
            entertainer_id=i['id']
        )

    return JsonResponse(status=200, data={'message': 'OK'})
