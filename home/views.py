from django.shortcuts import render


def index(request):
    return render(request, "pages/home.html", context={'events': TEMP_EVENTS})


def help(request):
    return render(request, 'pages/help.html')


def event(request, event_id):
    return render(request, "pages/event/index.html", context={'event_id': event_id})


def entertainers(request):
    return render(request, 'pages/entertainers/index.html')


def entertainer(request, entertainer_id):
    return render(request, 'pages/entertainers/index.html')


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
