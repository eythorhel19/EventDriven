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


def create_where_cond_event(search_params):
    where_cond = ""
    where_params = []
    search_fields = ['EVEE.title', 'HCITY.name', 'HLC.name', 'HCONT.name']

    for key, val in search_params.items():
        if key == 'categories':
            where_cond += "HCAT.name = '{}' AND ".format(val)

        if key == 'date_from':
            where_cond += "EVEE.start_date >= '{}' AND ".format(val)

        if key == 'date_to':
            where_cond += "EVEE.start_date <= '{}' AND ".format(val)

        if key == 'search_input_field':
            where_cond += "("
            for i, field in enumerate(search_fields):
                if i > 0:
                    where_cond += " OR "

                where_cond += "LOWER({}) LIKE %s".format(field)
                where_params.append('%{}%'.format(val.lower()))
            
            where_cond += ") AND "

    return where_cond, where_params

def create_where_cond_entertainer(search_params):
    where_cond = ""
    where_params = []
    search_fields = ['X.name']

    for key, val in search_params.items():
        if key == 'date_from':
            where_cond += "X.start_date >= '{}' AND ".format(val)

        if key == 'date_to':
            where_cond += "X.start_date <= '{}' AND ".format(val)

        if key == 'search_input_field':
            where_cond += "("
            for i, field in enumerate(search_fields):
                if i > 0:
                    where_cond += " OR "

                where_cond += "LOWER({}) LIKE %s".format(field)
                where_params.append('%{}%'.format(val.lower()))
            
            where_cond += ") AND "

    return where_cond, where_params


def search(request):
    user_details = get_user_details(request.user)

    search_params = {}
    available_params = ['categories', 'date_from', 'date_to', 'search_input_field']
    for param, value in request.GET.items():
        if param in available_params:
            if value != 'All':
                search_params[param] = value

    where_cond_1, where_params_1 = create_where_cond_event(search_params)
    
    where_cond_2, where_params_2 = create_where_cond_entertainer(search_params)

    query = '''   
        SELECT DISTINCT(X.*)
        FROM (  
            SELECT EVEE.*
            FROM 
                EVENTS_EVENT AS EVEE
                JOIN HOME_EVENTCATEGORY AS HEC
                ON EVEE.ID = HEC.EVENT_ID
                JOIN HOME_CATEGORY AS HCAT
                ON HCAT.ID = HEC.CATEGORY_ID
                JOIN HOME_LOCATION AS HLC
                ON HLC.ID = EVEE.LOCATION_ID
                JOIN HOME_CITY AS HCITY
                ON HCITY.ID = HLC.CITY_ID
                JOIN HOME_COUNTRY AS HCONT
                ON HCONT.ID = HCITY.COUNTRY_ID
            WHERE {} EVEE.START_DATE >= CURRENT_DATE
            ORDER BY 
                EVEE.START_DATE
            ) AS X;
        '''.format(where_cond_1)

    searched_events = Event.objects.raw(query, where_params_1)

    query2 = '''
        SELECT *
        FROM (
            SELECT DISTINCT ON (ENT.id)
                ENT.id,
                ENT.name,
                ENT.description,
                ENT.image_url,
                EVEE.title,
                EVEE.start_date,
                MIN(EVEE.start_date) AS next_event_date,
                HLOC.name AS location_name
            FROM 
                ENTERTAINERS_ENTERTAINER AS ENT
                JOIN HOME_EVENTENTERTAINER AS HEVENT
                ON ENT.id = HEVENT.entertainer_id
                JOIN EVENTS_EVENT AS EVEE
                ON EVEE.id = HEVENT.event_id
                JOIN HOME_LOCATION AS HLOC 
                ON HLOC.id = EVEE.location_id
            GROUP BY 
                ENT.id, ENT.name, ENT.description, ENT.image_url, EVEE.title, HLOC.name, EVEE.start_date
            ) AS X
        WHERE {} X.start_date >= CURRENT_DATE;
        '''.format(where_cond_2)

    searched_entertainers = Entertainer.objects.raw(query2, where_params_2)

    return render(request, 'pages/search.html', context={
        'searched_events': searched_events,
        'searched_entertainers': searched_entertainers,
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
