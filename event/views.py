from django.shortcuts import render

# Create your views here.


def index(request, event_id):
    return render(request, "event/index.html", context={'event_id': event_id})
