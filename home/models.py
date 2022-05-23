from django.db import models

from event.models import Event


class Category(models.Model):
    name = models.CharField(max_length=255)
    models.UniqueConstraint(
        models.Lower('name').desc(),
        'category',
        name='unique_lower_name_category')


class TicketType(models.Model):
    description = models.CharField(max_length=255)


class Ticket(models.Model):
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.IntegerField()
