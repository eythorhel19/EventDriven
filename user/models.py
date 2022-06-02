from django.db import models
from django.contrib.auth.models import User
from home.models import Country, City
#   User


class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image_url = models.CharField(max_length=9999)
    
    phone_country = models.ForeignKey(Country, blank=True, null=True, on_delete=models.SET_NULL)
    phone_number = models.CharField(max_length=32, blank=True, null=True)

    postal_country = models.ForeignKey(
        Country,
        blank=True, null=True, on_delete=models.SET_NULL, related_name='postal_country')
    postal_city = models.ForeignKey(City, blank=True, null=True, on_delete=models.SET_NULL)
    postal_code = models.CharField(max_length=16, blank=True, null=True)
    street_name = models.CharField(max_length=255, blank=True, null=True)
    house_number = models.IntegerField(blank=True, null=True)
