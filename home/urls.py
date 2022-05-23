from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('help', views.help, name="help"),
    path('event/<event_id>', views.event, name="event"),
    path('entertainers', views.entertainers, name="entertainers"),
    path('entertainer/<entertainer_id>', views.entertainer, name="entertainer"),
]
