from django.db import models
from entertainer.models import Entertainer
from home.models import Category
from location.models import Location


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    maximum_capacity = models.IntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)


class EventImage(models.Model):
    image_url = models.CharField(max_length=9999)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)


class EventCategory(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    models.UniqueConstraint(
        name='unique_event_category',
        fields=['event', 'category']
    )


class EventEntertainer(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    entertainer = models.ForeignKey(Entertainer, on_delete=models.CASCADE)
