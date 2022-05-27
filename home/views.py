from asyncio import constants

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from events.models import Event
from home.models import Category
from entertainers.models import Entertainer


def index(request):

    query_for_cat_hom = '''
        SELECT HCAT.ID AS CATEGORY_ID, HCAT.NAME AS CATEGORY_NAME, EEV.*
        FROM EVENTS_EVENT AS EEV
        JOIN HOME_EVENTCATEGORY AS HEVC ON EEV.ID = HEVC.EVENT_ID
        JOIN HOME_CATEGORY AS HCAT ON HCAT.ID = HEVC.CATEGORY_ID
        ORDER BY HEVC.CATEGORY_ID
        '''
    events_wit_cat = Event.objects.raw(query_for_cat_hom)

    event_cat_categorised = []
    current_ev_id_cat = []
    last_event_cat_id = -1
    for event_what_cat in events_wit_cat:
        if event_what_cat.category_id == last_event_cat_id:
            current_ev_id_cat.append(event_what_cat)
        else:
            if last_event_cat_id != -1:
                event_cat_categorised.append(current_ev_id_cat)
                current_ev_id_cat = []
            current_ev_id_cat.append(event_what_cat)
            last_event_cat_id = event_what_cat.category_id

    # events = Event.objects.all()
    # for i in events:
    #     print(i)

    # return render(request, "pages/home.html", context={, 'categories': Category.objects.all()})
    progress_data = [
        {'id': 1, 'tag_id': 'booking_modal_pp_1', 'description': 'Your Booking'},
        {'id': 2, 'tag_id': 'booking_modal_pp_2',
            'description': 'Delivery Method'},
        {'id': 3, 'tag_id': 'booking_modal_pp_3', 'description': 'Delivery Info'},
        {'id': 4, 'tag_id': 'booking_modal_pp_4', 'description': 'Payment'},
        {'id': 5, 'tag_id': 'booking_modal_pp_5', 'description': 'Confirm'}
    ]

    return render(request, "pages/home.html", context={
        'event_cat_categorised': event_cat_categorised,
        'progress_data': progress_data,
        'categories': Category.objects.all()
    })


def help(request):
    return render(request, 'pages/help.html')


def search(request):
    categories = request.GET["categories"]
    date_options = request.GET["date_options"]
    search_input_field = request.GET["search_input_field"]
    if categories == "All":
        categories_events = "true"
    else:
        categories_events = "HCAT.NAME='{}'".format(categories)

    if date_options == "All":
        date_options_events = "true"
    else:
        date_options_events = "EVEE.START_DATE<='{}'".format(date_options)

    if search_input_field == "All":
        search_input_field_events = "true"
        search_input_field_events2 = "true"
        search_input_field_events3 = "true"
        search_input_field_events4 = "true"
        search_input_field_events5 = "true"
        search_input_field_events6 = "true"
        search_input_field_events7 = "true"
        search_input_field_events8 = "true"
        search_input_field_events9 = "true"
        search_input_field_events10 = "true"
        search_input_field_events11 = "true"
        search_input_field_events12 = "true"
    else:
        search_input_field_events = "LOWER(EVEE.TITLE) LIKE LOWER('_{}_')".format(
            search_input_field)
        search_input_field_events2 = "LOWER(EVEE.TITLE) LIKE LOWER('{}_')".format(
            search_input_field)
        search_input_field_events3 = "LOWER(EVEE.TITLE) LIKE LOWER('_{}')".format(
            search_input_field)
        search_input_field_events4 = "LOWER(EVEE.TITLE) = LOWER('{}')".format(
            search_input_field)
        search_input_field_events5 = "LOWER(ENT.NAME) LIKE LOWER('_{}_')".format(
            search_input_field)
        search_input_field_events6 = "LOWER(ENT.NAME) LIKE LOWER('{}_')".format(
            search_input_field)
        search_input_field_events7 = "LOWER(ENT.NAME) LIKE LOWER('_{}')".format(
            search_input_field)
        search_input_field_events8 = "LOWER(ENT.NAME) = LOWER('{}')".format(
            search_input_field)
        search_input_field_events9 = "LOWER(HLC.NAME) = LOWER('{}')".format(
            search_input_field)
        search_input_field_events10 = "LOWER(HCITY.NAME) = LOWER('{}')".format(
            search_input_field)
        search_input_field_events11 = "LOWER(HSTATE.NAME) = LOWER('{}')".format(
            search_input_field)
        search_input_field_events12 = "LOWER(HCONT.NAME) = LOWER('{}')".format(
            search_input_field)

    query = '''   
        SELECT DISTINCT(EVEE.*)
        FROM (  
            SELECT *
            FROM EVENTS_EVENT AS EVEE
            JOIN HOME_EVENTCATEGORY AS HEC  ON EVEE.ID = HEC.EVENT_ID
            JOIN HOME_CATEGORY AS HCAT ON HCAT.ID = HEC.CATEGORY_ID
			JOIN HOME_LOCATION AS HLC ON HLC.ID = EVEE.LOCATION_ID
			JOIN HOME_CITY AS HCITY ON HCITY.ID = HLC.CITY_ID
			JOIN HOME_STATE AS HSTATE ON HSTATE.ID = HCITY.STATE_ID
			JOIN HOME_COUNTRY AS HCONT ON HCONT.ID = HSTATE.COUNTRY_ID
            WHERE {} AND {} AND ({} OR {} OR {} OR {} OR {} OR {} OR {} OR {})
            ORDER BY EVEE.START_DATE
            ) AS EVEE
        '''.format(categories_events, date_options_events, search_input_field_events, search_input_field_events2, search_input_field_events3, search_input_field_events4, search_input_field_events9, search_input_field_events10, search_input_field_events11, search_input_field_events12)

    print('query', query)

    searched_events = Event.objects.raw(query)

    query2 = '''
        SELECT ENT.*
        FROM ENTERTAINERS_ENTERTAINER AS ENT
        WHERE {} or {} or {} or {}
        '''.format(search_input_field_events5, search_input_field_events6, search_input_field_events7, search_input_field_events8)

    searched_events_later = Entertainer.objects.raw(query2)

    return render(request, 'pages/search.html', context={'searched_events': searched_events, 'searched_events_later': searched_events_later,  'categories': Category.objects.all()})


@login_required
def dashboard(request):

    query_dashboard_user_tickets = '''
        SELECT HT.*, EEVE.TITLE AS EVENT_TITLE, EEVE.START_DATE AS EVENT_START_DATE, EEVE.MAIN_IMAGE_URL, HLOC.NAME AS EVENT_LOCATION_NAME
        FROM HOME_TICKET AS HT 
        JOIN EVENTS_EVENT AS EEVE ON HT.EVENT_ID = EEVE.ID
        JOIN HOME_LOCATION AS HLOC ON HLOC.ID = EEVE.LOCATION_ID
        WHERE HT.USER_ID = {}
        '''.format(request.user.id)
    query_dashboard_user_tickets_results = Event.objects.raw(
        query_dashboard_user_tickets)

    query_dashboard_user_fav_cat_ent_events = '''

SELECT DISTINCT(EEVE.*)
FROM EVENTS_EVENT AS EEVE
JOIN HOME_EVENTCATEGORY AS HEVECAT ON HEVECAT.EVENT_ID = EEVE.ID
JOIN HOME_EVENTENTERTAINER AS HEENT ON HEENT.EVENT_ID = EEVE.ID
WHERE HEVECAT.ID IN
		(SELECT HUFC.CATEGORY_ID
FROM HOME_USERFAVORITECATEGORY AS HUFC
WHERE HUFC.USER_ID = {}) OR HEENT.ID IN(SELECT HUFENT.ENTERTAINER_ID
												 FROM HOME_USERFAVORITEENTERTAINER AS HUFENT
												 WHERE HUFENT.USER_ID = {})
			
        '''.format(request.user.id, request.user.id)

    query_dashboard_user_fav_cat_ent_events_res = Event.objects.raw(
        query_dashboard_user_fav_cat_ent_events)

    return render(request, 'pages/dashboard.html', context={'query_dashboard_user_tickets_results': query_dashboard_user_tickets_results, "query_dashboard_user_fav_cat_ent_events_res": query_dashboard_user_fav_cat_ent_events_res})
