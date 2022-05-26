from django.http import HttpResponse
from django.shortcuts import render
from entertainers.models import Entertainer
from home.models import Category

# Create your views here.


def entertainers(request):
    entertainer = Entertainer.objects.all()

    return render(request, 'pages/entertainers/index.html', context={"entertainer": entertainer, 'categories': Category.objects.all()})


def entertainer(request, entertainer_id):
    if not entertainer_id.isdigit():
        return HttpResponse(status=400, content="Invalid ID")

    entertainer_events = Entertainer.objects.raw('''
        SELECT EVE.*
        FROM ENTERTAINERS_ENTERTAINER AS ENT
        JOIN HOME_EVENTENTERTAINER AS HEE ON ENT.ID = HEE.ENTERTAINER_ID
        JOIN EVENTS_EVENT AS EVE ON HEE.EVENT_ID = EVE.ID
        WHERE ENT.ID = {}
        ORDER BY EVE.START_DATE'''.format(entertainer_id)
    )
    entertainer_info = Entertainer.objects.get(pk=entertainer_id)
    return render(request, 'pages/entertainers/entertainer.html', context={'entertainer_info': entertainer_info, "entertainer_events": entertainer_events})
