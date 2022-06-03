from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('help', views.help_page, name="help"),
    path('search', views.search, name="search"),
    path('dashboard', views.dashboard, name="dashboard")
]
