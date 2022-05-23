from django.shortcuts import render

# Create your views here.
TEMP_EVENTS = [

    {
        "name": "Event 1",
        "date": "2019-01-01",
        "time": "12:00",
        "location": "Location 1",
        "description": "Description 1",
        "image": "https://picsum.photos/200/300/?random",
    },
    {
        "name": "Event 2",
        "date": "2019-01-02",
        "time": "12:00",
        "location": "Location 2",
        "description": "Description 2",
        "image": "https://picsum.photos/200/300/?random",
    },
    {
        "name": "Event 3",
        "date": "2019-01-03",
        "time": "12:00",
        "location": "Location 3",
        "description": "Description 3",
        "image": "https://picsum.photos/200/300/?random",
    }

]


def index(request):
    return render(request, "home/index.html", context={'events': TEMP_EVENTS})
