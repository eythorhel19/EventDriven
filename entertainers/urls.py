from django.urls import path
from . import views

urlpatterns = [
    path('', views.entertainers, name="entertainers"),
    path('<entertainer_id>', views.entertainer, name="entertainer"),
]
