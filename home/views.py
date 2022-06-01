from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from events.models import Event
from entertainers.models import Entertainer
from home.models import Category, UserFavoriteCategory, UserFavoriteEntertainer
from user.views import get_user_details
from constants import progress_data


def index(request):
    user_details = get_user_details(request.user)

    query_for_cat_hom = '''
        SELECT HCAT.ID AS CATEGORY_ID, HCAT.NAME AS CATEGORY_NAME, EEV.*
        FROM EVENTS_EVENT AS EEV
        JOIN HOME_EVENTCATEGORY AS HEVC ON EEV.ID = HEVC.EVENT_ID
        JOIN HOME_CATEGORY AS HCAT ON HCAT.ID = HEVC.CATEGORY_ID
        WHERE EEV.START_DATE >= CURRENT_DATE
        ORDER BY HEVC.CATEGORY_ID, EEV.START_DATE
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
    event_cat_categorised.append(current_ev_id_cat)

    return render(request, "pages/home.html", context={
        'event_cat_categorised': event_cat_categorised,
        'progress_data': progress_data,
        'categories': Category.objects.all(),
        'user_details': user_details
    })


def help(request):
    user_details = get_user_details(request.user)
    return render(request, 'pages/help.html', context={
        'user_details': user_details
    })


def search(request):
    user_details = get_user_details(request.user)

    categories = request.GET["categories"]
    date_to = request.GET["date_to"]
    date_from = request.GET["date_from"]
    search_input_field = request.GET["search_input_field"]
    if categories == "All":
        categories_events = "true"
    else:
        categories_events = "HCAT.NAME='{}'".format(categories)

    if date_to == "All" and date_from == "All":
        date_to_events = "true"
    elif date_to == "All" and date_from != "All":
        date_to_events = "'{}' <= EEV.START_DATE".format(date_from)
    elif date_to != "All" and date_from == "All":
        date_to_events = "'{}' >= EEV.START_DATE".format(date_to)
    else:
        date_to_events = "'{}'<=EVEE.START_DATE AND EVEE.START_DATE<='{}'".format(
            date_from, date_to)

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
        search_input_field_events12 = "LOWER(HCONT.NAME) = LOWER('{}')".format(
            search_input_field)

    query = '''   
        SELECT DISTINCT(EVEE.*)
        FROM (  
            SELECT EVEE.*
            FROM EVENTS_EVENT AS EVEE
            JOIN HOME_EVENTCATEGORY AS HEC  ON EVEE.ID = HEC.EVENT_ID
            JOIN HOME_CATEGORY AS HCAT ON HCAT.ID = HEC.CATEGORY_ID
			JOIN HOME_LOCATION AS HLC ON HLC.ID = EVEE.LOCATION_ID
			JOIN HOME_CITY AS HCITY ON HCITY.ID = HLC.CITY_ID
			JOIN HOME_COUNTRY AS HCONT ON HCONT.ID = HCITY.COUNTRY_ID
            WHERE {} AND {} AND ({} OR {} OR {} OR {} OR {} OR {} OR {}) AND EVEE.START_DATE >= CURRENT_DATE
            ORDER BY EVEE.START_DATE
            ) AS EVEE
        '''.format(categories_events, date_to_events, search_input_field_events, search_input_field_events2, search_input_field_events3, search_input_field_events4, search_input_field_events9, search_input_field_events10, search_input_field_events12)

    searched_events = Event.objects.raw(query)

    query2 = '''
        SELECT ENT.*, MIN(EVEE.START_DATE) AS NEXT_EVENT_DATE, HLOC.NAME AS LOCATION_NAME
        FROM ENTERTAINERS_ENTERTAINER AS ENT
        JOIN HOME_EVENTENTERTAINER AS HEVENT ON ENT.ID = HEVENT.ENTERTAINER_ID
        JOIN EVENTS_EVENT AS EVEE ON EVEE.ID = HEVENT.EVENT_ID
        JOIN HOME_LOCATION AS HLOC ON HLOC.ID = EVEE.LOCATION_ID
        GROUP BY (ENT.ID, ENT.NAME, ENT.DESCRIPTION, ENT.IMAGE_URL, HLOC.NAME, EVEE.START_DATE)
        HAVING ({} or {} or {} or {}) AND {} AND EVEE.START_DATE >= CURRENT_DATE
        '''.format(search_input_field_events5, search_input_field_events6, search_input_field_events7, search_input_field_events8, date_to_events)

    searched_events_later = Entertainer.objects.raw(query2)

    return render(request, 'pages/search.html', context={
        'searched_events': searched_events,
        'searched_events_later': searched_events_later,
        'categories': Category.objects.all(),
        'user_details': user_details
    })


@login_required
def dashboard(request):
    user_details = get_user_details(request.user)

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
    WHERE EEVE.START_DATE >= CURRENT_DATE AND HEVECAT.CATEGORY_ID IN
            (SELECT HUFC.CATEGORY_ID
    FROM HOME_USERFAVORITECATEGORY AS HUFC
    WHERE HUFC.USER_ID = {}) OR HEENT.ENTERTAINER_ID IN(SELECT HUFENT.ENTERTAINER_ID
                                                    FROM HOME_USERFAVORITEENTERTAINER AS HUFENT
                                                    WHERE HUFENT.USER_ID = {})
                
        '''.format(request.user.id, request.user.id)

    query_dashboard_user_fav_cat_ent_events_res = Event.objects.raw(
        query_dashboard_user_fav_cat_ent_events)

    this_users_selected_categories = UserFavoriteCategory.objects.filter(
        user_id=request.user.id)
    this_users_selected_entertainers = UserFavoriteEntertainer.objects.filter(
        user_id=request.user.id)

    user_fav_cate = []
    rest_fav_cate = []
    this_users_selected_categories_list = []
    for i in this_users_selected_categories:
        this_users_selected_categories_list.append(i.category_id)

    for i in Category.objects.all():
        if(i.id in this_users_selected_categories_list):
            user_fav_cate.append(i)
        else:
            rest_fav_cate.append(i)

    user_fav_ent = []
    rest_fav_ent = []
    this_users_selected_ent_list = []
    for i in this_users_selected_entertainers:
        this_users_selected_ent_list.append(i.entertainer_id)

    for i in Entertainer.objects.all():
        if(i.id in this_users_selected_ent_list):
            user_fav_ent.append(i)
        else:
            rest_fav_ent.append(i)

    return render(request, 'pages/dashboard.html', context={
        'query_dashboard_user_tickets_results': query_dashboard_user_tickets_results,
        "query_dashboard_user_fav_cat_ent_events_res": query_dashboard_user_fav_cat_ent_events_res,
        "user_fav_cate": user_fav_cate,
        "rest_fav_cate": rest_fav_cate,
        "user_fav_ent": user_fav_ent,
        "rest_fav_ent": rest_fav_ent,
        "user_details": user_details
    })
