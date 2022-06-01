from django.urls import path
from . import views

urlpatterns = [
    path('create_event', views.create_event, name="create_event"),
    path('create_event/<event_id>', views.create_event_more_info,
         name="create_event_more_info"),
    path('<event_id>', views.event, name="event")
]
