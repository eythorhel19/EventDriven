from django.shortcuts import render
from events.models import Event


def index(request):
    events = Event.objects.raw('''
    SELECT
        E.id,
        E.title,
        E.description,
        E.start_date,
        E.main_image_url,
        CONCAT(L.name,', ',C.name) AS location_name
    FROM events_event AS E
    INNER JOIN home_location AS L
    ON E.location_id = L.id
    INNER JOIN home_city AS C
    ON L.city_id = C.id;
    ''')

    progress_data = [
        {'id': 1, 'description': 'Your Booking'},
        {'id': 2, 'description': 'Delivery Method'},
        {'id': 3, 'description': 'Delivery Info'},
        {'id': 4, 'description': 'Payment'},
        {'id': 5, 'description': 'Confirm'}
    ]

    return render(request, "pages/home.html", context={
        'events': events,
        'progress_data': progress_data
    })


def help(request):
    return render(request, 'pages/help.html')


# Create your views here.
TEMP_EVENTS = [

    {
        'id': 1,
        "name": "Event 1",
        "date": "2019-01-01",
        "time": "12:00",
        "location": "Location 1",
        "description": "Description 1",
        "image": "https://picsum.photos/200/300/?random",
    },
    {
        'id': 2,
        "name": "Event 2",
        "date": "2019-01-02",
        "time": "12:00",
        "location": "Location 2",
        "description": "Description 2",
        "image": "https://picsum.photos/200/300/?random",
    },
    {
        'id': 3,
        "name": "Event 3",
        "date": "2019-01-03",
        "time": "12:00",
        "location": "Location 3",
        "description": "Description 3",
        "image": "https://picsum.photos/200/300/?random",
    },
    {
        'id': 4,
        "name": "Event 4",
        "date": "2019-01-03",
        "time": "12:00",
        "location": "Location 4",
        "description": "Description 4",
        "image": "https://picsum.photos/200/300/?random",
    },
    {
        'id': 5,
        "name": "Event 5",
        "date": "2019-01-03",
        "time": "12:00",
        "location": "Location 5",
        "description": "Description 5",
        "image": "https://picsum.photos/200/300/?random",
    },
    {
        'id': 6,
        "name": "Event 6",
        "date": "2019-01-03",
        "time": "12:00",
        "location": "Location 6",
        "description": "Description 6",
        "image": "https://picsum.photos/200/300/?random",
    },
    {
        'id': 7,
        "name": "Event 6",
        "date": "2019-01-03",
        "time": "12:00",
        "location": "Location 6",
        "description": "Description 6",
        "image": "https://picsum.photos/200/300/?random",
    },
    {
        'id': 8,
        "name": "Event 7",
        "date": "2019-01-03",
        "time": "12:00",
        "location": "Location 7",
        "description": "Description 7",
        "image": "https://picsum.photos/200/300/?random",
    }


]
