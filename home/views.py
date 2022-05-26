from asyncio import constants
from django.shortcuts import render
from events.models import Event
from home.models import Category
from entertainers.models import Entertainer


def index(request):
    events = Event.objects.all()

    return render(request, "pages/home.html", context={'events': events, 'categories': Category.objects.all()})


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

    query = '''   
        SELECT DISTINCT(EVEE.*)
        FROM (  
            SELECT EVEE.*
            FROM EVENTS_EVENT AS EVEE
            JOIN HOME_EVENTCATEGORY AS HEC  ON EVEE.ID = HEC.EVENT_ID
            JOIN HOME_CATEGORY AS HCAT ON HCAT.ID = HEC.CATEGORY_ID
            WHERE {} AND {} AND ({} OR {} OR {} OR {})) AS EVEE
        '''.format(categories_events, date_options_events, search_input_field_events, search_input_field_events2, search_input_field_events3, search_input_field_events4)

    searched_events = Event.objects.raw(query)

    query2 = '''
        SELECT ENT.*
        FROM ENTERTAINERS_ENTERTAINER AS ENT
        WHERE {} or {} or {} or {}
        '''.format(search_input_field_events5, search_input_field_events6, search_input_field_events7, search_input_field_events8)
    print(query2)
    searched_events_later = Entertainer.objects.raw(query2)

    return render(request, 'pages/search.html', context={'searched_events': searched_events, 'searched_events_later': searched_events_later,  'categories': Category.objects.all()})
# Coachella
#

# Create your views here.

#
