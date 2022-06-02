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
            SELECT DISTINCT ON (EENT.id) EENT.id, 
                EENT.name, 
                EENT.description, 
                EENT.image_url, 
                MIN(EVE.start_date) AS next_event_date, 
                HLOC.name AS location_name
            FROM 
                ENTERTAINERS_ENTERTAINER AS EENT
                JOIN HOME_EVENTENTERTAINER AS HEVENT 
                ON EENT.ID = HEVENT.ENTERTAINER_ID
                JOIN EVENTS_EVENT AS EVE 
                ON EVE.ID = HEVENT.EVENT_ID
                JOIN HOME_LOCATION AS HLOC 
                ON HLOC.ID = EVE.LOCATION_ID
            WHERE 
                EVE.START_DATE >= CURRENT_DATE
            GROUP BY 
                EENT.id, EENT.name, EENT.description, EENT.image_url, HLOC.name, EVE.id, EVE.start_date
            ) AS FRO_GROUP_BY
        ORDER BY 
            FRO_GROUP_BY.next_event_date;
    '''

    entertainer_ = Entertainer.objects.raw(query_for_entertainers_card)

    return render(request, 'pages/entertainers/index.html', context={
        "entertainer": entertainer_,
        "categories": Category.objects.all(),
        "user_details": user_details
    })


def entertainer(request, entertainer_id):
    user_details = get_user_details(request.user)

    if not entertainer_id.isdigit():
        return HttpResponse(status=400, content="Invalid ID")

    entertainer_events = Entertainer.objects.raw('''
        SELECT 
            EVE.*, 
            HLOC.name AS location
        FROM 
            ENTERTAINERS_ENTERTAINER AS ENT
            JOIN HOME_EVENTENTERTAINER AS HEE 
            ON ENT.id = HEE.entertainer_id
            JOIN EVENTS_EVENT AS EVE 
            ON HEE.event_id = EVE.id
            JOIN HOME_LOCATION AS HLOC 
            ON HLOC.id = EVE.location_id
        WHERE 
            ENT.id = {} AND EVE.start_date >= CURRENT_DATE
        ORDER BY 
            EVE.start_date;'''.format(entertainer_id)
    )

    entertainer_info = Entertainer.objects.get(pk=entertainer_id)

    return render(request, 'pages/entertainers/entertainer.html', context={
        'entertainer_info': entertainer_info,
        "entertainer_events": entertainer_events,
        "user_details": user_details,
        "progress_data": progress_data
    })
