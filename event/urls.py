from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('/<event_id>', views.index, name="index")
]
