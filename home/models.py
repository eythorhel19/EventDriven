from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from events.models import Event
from entertainers.models import Entertainer

# BASE TABLES

#   Location


class Country(models.Model):
    name = models.CharField(max_length=255)
    phone_country_code = models.CharField(max_length=5)


class State(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)


class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)


class Location(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    capacity = models.IntegerField()

    def __str__(self):
        return "{}, {}".format(self.name, self.city.name)

#   Address


class PostalCode(models.Model):
    postal_code = models.CharField(max_length=16)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    models.UniqueConstraint(
        name='unique_postal_code',
        fields=['postal_code', 'country']
    )

#   Category


class Category(models.Model):
    name = models.CharField(max_length=255)
    models.UniqueConstraint(
        models.functions.Lower('name').desc(),
        'Category',
        name='unique_lower_name_category')

#   User


class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image_url = models.CharField(max_length=9999)

#   Ticket


class TicketType(models.Model):
    description = models.CharField(max_length=255)


class Ticket(models.Model):
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    DELIVERY_METHODS = [
        ('E', 'Electronic'),
        ('P', 'Postal'),
    ]
    delivery_method = models.CharField(
        max_length=1, choices=DELIVERY_METHODS, default='E'
    )

    email = models.EmailField(max_length=255)

    TICKET_STATUS = [
        ('U', 'Unreleased'),
        ('R', 'Released'),
        ('S', 'Sold'),
    ]
    status = models.CharField(max_length=1, choices=TICKET_STATUS, default='U')

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    street_name = models.CharField(max_length=255)
    house_number = models.IntegerField()
    postal_code_id = models.ForeignKey(PostalCode, on_delete=models.CASCADE)


# RELATION TABLES

#    Event


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
    models.UniqueConstraint(
        name='unique_event_entertainer',
        fields=['event', 'entertainer']
    )

# Ticket


class EventTicketTypePrice(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE)
    price = models.FloatField()
    models.UniqueConstraint(
        name='unique_event_ticket_type',
        fields=['event', 'ticket_type']
    )

#    User


class UserFavoriteCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    models.UniqueConstraint(
        name='unique_user_category',
        fields=['user', 'category']
    )
