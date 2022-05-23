from django.db import models

# Create your models here.


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
