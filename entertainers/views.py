from django.http import HttpResponse
from django.shortcuts import render
from entertainers.models import Entertainer
from home.models import Category
from user.views import get_user_details
from constants import progress_data

# Create your views here.


def entertainers(request):
    user_details = get_user_details(request.user)

    query_for_entertainers_card = '''
        SELECT *
        FROM (
        SELECT DISTINCT ON (EENT.ID) EENT.ID, EENT.NAME, EENT.DESCRIPTION, EENT.IMAGE_URL, MIN(EVE.START_DATE) AS NEXT_EVENT_DATE, HLOC.NAME AS LOCATION_NAME
        FROM ENTERTAINERS_ENTERTAINER AS EENT
        JOIN HOME_EVENTENTERTAINER AS HEVENT ON EENT.ID = HEVENT.ENTERTAINER_ID
        JOIN EVENTS_EVENT AS EVE ON EVE.ID = HEVENT.EVENT_ID
        JOIN HOME_LOCATION AS HLOC ON HLOC.ID = EVE.LOCATION_ID
        WHERE EVE.START_DATE >= CURRENT_DATE
        GROUP BY EENT.ID, EENT.NAME, EENT.DESCRIPTION, EENT.IMAGE_URL, HLOC.NAME, EVE.ID, EVE.START_DATE
        ) AS FRO_GROUP_BY
        ORDER BY FRO_GROUP_BY.NEXT_EVENT_DATE
    '''
    entertainer = Entertainer.objects.raw(query_for_entertainers_card)
    for i in entertainer:
        print(i.next_event_date)

    return render(request, 'pages/entertainers/index.html', context={
        "entertainer": entertainer,
        "categories": Category.objects.all(),
        "user_details": user_details
    })


def entertainer(request, entertainer_id):
    user_details = get_user_details(request.user)

    if not entertainer_id.isdigit():
        return HttpResponse(status=400, content="Invalid ID")

    entertainer_events = Entertainer.objects.raw('''
        SELECT EVE.*, HLOC.NAME AS LOCATION
        FROM ENTERTAINERS_ENTERTAINER AS ENT
        JOIN HOME_EVENTENTERTAINER AS HEE ON ENT.ID = HEE.ENTERTAINER_ID
        JOIN EVENTS_EVENT AS EVE ON HEE.EVENT_ID = EVE.ID
        JOIN HOME_LOCATION AS HLOC ON HLOC.ID = EVE.LOCATION_ID
        WHERE ENT.ID = {} AND EVE.START_DATE >= CURRENT_DATE
        ORDER BY EVE.START_DATE'''.format(entertainer_id)
    )
    entertainer_info = Entertainer.objects.get(pk=entertainer_id)

    return render(request, 'pages/entertainers/entertainer.html', context={
        'entertainer_info': entertainer_info,
        "entertainer_events": entertainer_events,
        "user_details": user_details,
        "progress_data": progress_data
    })
