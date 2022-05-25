from django.urls import path
from . import views

urlpatterns = [
    path('<event_id>', views.event, name="event")
]
