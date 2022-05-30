from django.urls import path
from . import views

urlpatterns = [
    path('event/<event_id>', views.event, name="get event"),
    path('country', views.countries, name="get countries"),
    path('city', views.cities, name="get cities"),
    path('bookticket', views.book_ticket, name="booking a ticket")
]
