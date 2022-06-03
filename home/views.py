from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from events.models import Event
from entertainers.models import Entertainer
from home.models import Category, Ticket, UserFavoriteCategory, UserFavoriteEntertainer
from user.views import get_user_details
from constants import progress_data
from eventdriven.shared_functions import run_query


def index(request):
    user_details = get_user_details(request.user)

    events_with_category = run_query(
        Event,
        'home/queries/events_with_category.sql'
    )

    # Categorizing Events
    event_cat_categorised = []
    current_ev_id_cat = []
    last_event_cat_id = -1

    for event_what_cat in events_with_category:
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


def help_page(request):
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

    searched_events = run_query(
        Event,
        'home/queries/event_search.sql',
        options={'where_cond': where_cond_1},
        params=where_params_1
    )

    searched_entertainers = run_query(
        Entertainer,
        'home/queries/entertainer_search.sql',
        options={'where_cond': where_cond_2},
        params=where_params_2
    )

    return render(request, 'pages/search.html', context={
        'searched_events': searched_events,
        'progress_data': progress_data,
        'searched_entertainers': searched_entertainers,
        'categories': Category.objects.all(),
        'user_details': user_details
    })


@login_required
def dashboard(request):
    user_details = get_user_details(request.user)

    # Getting user tickets
    user_tickets = run_query(
        Ticket,
        'home/queries/user_tickets.sql',
        options={'user_id': request.user.id}
    )

    # Getting events matching favorites
    events_matching_favorites = run_query(
        Event,
        'home/queries/events_matching_favorites.sql',
        options={'user_id': request.user.id}
    )

    # Getting selected favorites categories
    this_users_selected_categories = UserFavoriteCategory.objects.filter(
        user_id=request.user.id
    )

    user_fav_cate = []
    rest_fav_cate = []
    this_users_selected_categories_list = []
    for i in this_users_selected_categories:
        this_users_selected_categories_list.append(i.category_id)

    for i in Category.objects.all():
        if i.id in this_users_selected_categories_list:
            user_fav_cate.append(i)
        else:
            rest_fav_cate.append(i)

    # Getting selected favorites entertainers
    this_users_selected_entertainers = UserFavoriteEntertainer.objects.filter(
        user_id=request.user.id
    )

    user_fav_ent = []
    rest_fav_ent = []
    this_users_selected_ent_list = []
    for i in this_users_selected_entertainers:
        this_users_selected_ent_list.append(i.entertainer_id)

    for i in Entertainer.objects.all():
        if i.id in this_users_selected_ent_list:
            user_fav_ent.append(i)
        else:
            rest_fav_ent.append(i)

    return render(request, 'pages/dashboard.html', context={
        'user_tickets': user_tickets,
        "events_matching_favorites": events_matching_favorites,
        'progress_data': progress_data,
        "user_fav_cate": user_fav_cate,
        "rest_fav_cate": rest_fav_cate,
        "user_fav_ent": user_fav_ent,
        "rest_fav_ent": rest_fav_ent,
        "user_details": user_details
    })
