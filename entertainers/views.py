from django.http import HttpResponse
from django.shortcuts import render

from constants import progress_data
from entertainers.models import Entertainer
from eventdriven.shared_functions import run_query
from home.models import Category
from user.views import get_user_details


def entertainers(request):
    user_details = get_user_details(request.user)

    entertainer_ = run_query(Entertainer, 'entertainers/queries/entertainer_card.sql')

    return render(request, 'pages/entertainers/index.html', context={
        "entertainer": entertainer_,
        "categories": Category.objects.all(),
        "user_details": user_details
    })


def entertainer(request, entertainer_id):
    user_details = get_user_details(request.user)

    if not entertainer_id.isdigit():
        return HttpResponse(status=400, content="Invalid ID")

    entertainer_events = run_query(
        Entertainer, 
        'entertainers/queries/entertainer_events.sql', 
        {'entertainer_id': entertainer_id}
    )
    
    entertainer_info = Entertainer.objects.get(pk=entertainer_id)

    return render(request, 'pages/entertainers/entertainer.html', context={
        'entertainer_info': entertainer_info,
        "entertainer_events": entertainer_events,
        "user_details": user_details,
        "progress_data": progress_data
    })
