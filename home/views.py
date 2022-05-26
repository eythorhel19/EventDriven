from django.shortcuts import render
from events.models import Event


def index(request):
    events = Event.objects.all()

    return render(request, "pages/home.html", context={'events': events})


def help(request):
    return render(request, 'pages/help.html')


# Create your views here.
