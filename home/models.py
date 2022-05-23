from django.db import models


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


class PostalCode(models.Model):
    postal_code = models.CharField(max_length=16)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    models.UniqueConstraint(
        name='unique_postal_code',
        fields=['postal_code', 'country']
    )


class Entertainer(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    maximum_capacity = models.IntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)


class Category(models.Model):
    name = models.CharField(max_length=255)
    # models.UniqueConstraint(
    #     models.Lower('name').desc(),
    #     'category',
    #     name='unique_lower_name_category')


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


class TicketType(models.Model):
    description = models.CharField(max_length=255)


class Ticket(models.Model):
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.IntegerField()
