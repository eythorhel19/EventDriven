from django.urls import path
from . import views

urlpatterns = [
    path('event/<event_id>', views.event, name="get event"),
    path('country', views.countries, name="get countries"),
    path('city', views.cities, name="get cities"),
    path('generatetickets', views.generate_tickets, name="generating tickets"),
    path('releasetickets', views.release_tickets, name="release tickets"),
    path('booktickets', views.book_tickets, name="booking a tickets")
]
