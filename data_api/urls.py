from django.urls import path
from . import views

urlpatterns = [
    path('event/<event_id>', views.event, name="get event"),
    path('country', views.countries, name="get countries"),
    path('city', views.cities, name="get cities"),
    path('generatetickets', views.generate_tickets, name="generating tickets"),
    path('releasetickets', views.release_tickets, name="release tickets"),
    path('booktickets', views.book_tickets, name="booking a tickets"),
    path('user_categories', views.user_categories, name="posting new users fav categories"),
    path('user_entertainers', views.user_entertainers, name="posting new users fav entertainer"),
    path('user_info', views.user_info, name="get user info"),
    path('event_categories', views.event_categories, name="create event categories"),
    path('event_entertainers', views.event_entertainers, name="create event entertainers")
]
