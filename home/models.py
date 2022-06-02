from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from events.models import Event
from entertainers.models import Entertainer

# BASE TABLES

#   Location


class Country(models.Model):
    name = models.CharField(max_length=255)
    iso3_code = models.CharField(max_length=3)
    phone_country_code = models.CharField(max_length=5)

    def __str__(self):
        return "{} (+{})".format(self.name, self.phone_country_code)


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return "{}".format(self.name)

class Location(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    capacity = models.IntegerField()
    map_url = models.CharField(max_length=510, default="")

    def __str__(self):
        return "{}, {}".format(self.name, self.city.name)

#   Category


class Category(models.Model):
    name = models.CharField(max_length=255)
    models.UniqueConstraint(
        models.functions.Lower('name').desc(),
        'Category',
        name='unique_lower_name_category'
    )

#   Ticket


class TicketType(models.Model):
    description = models.CharField(max_length=255)


class Ticket(models.Model):
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    DELIVERY_METHODS = [
        ('E', 'Electronic'),
        ('P', 'Postal'),
    ]
    delivery_method = models.CharField(
        max_length=1, choices=DELIVERY_METHODS, default='E'
    )

    email = models.EmailField(max_length=255, blank=True, null=True)

    TICKET_STATUS = [
        ('U', 'Unreleased'),
        ('R', 'Released'),
        ('S', 'Sold'),
    ]
    status = models.CharField(max_length=1, choices=TICKET_STATUS, default='U')
    phone_country = models.ForeignKey(Country, null=True, on_delete=models.SET_NULL)
    phone_number = models.CharField(max_length=32)

    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)

    street_name = models.CharField(max_length=255, blank=True, null=True)
    house_number = models.IntegerField(blank=True, null=True)
    postal_code = models.CharField(max_length=16, blank=True, null=True)


# RELATION TABLES

#    Event


class EventCategory(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='unique_event_category',
                fields=['event', 'category']
            )
        ]


class EventEntertainer(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    entertainer = models.ForeignKey(Entertainer, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='unique_event_entertainer',
                fields=['event', 'entertainer']
            )
        ]

# Ticket


class EventTicketTypePrice(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE)
    price = models.FloatField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='unique_event_ticket_type',
                fields=['event', 'ticket_type']
            )
        ]

#    User


class UserFavoriteCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='unique_user_category',
                fields=['user', 'category']
            )
        ]


class UserFavoriteEntertainer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    entertainer = models.ForeignKey(Entertainer, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='unique_user_favorite_entertainer',
                fields=['user', 'entertainer']
            )
        ]
