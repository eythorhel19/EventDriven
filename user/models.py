from django.db import models
from django.contrib.auth.models import User

#   User


class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image_url = models.CharField(max_length=9999)
    # phone_country = models.ForeignKey('home_country', blank=True, null=True, on_delete=models.SET_NULL)
    # phone_number = models.CharField(max_length=32)
    # name_on_card = models.CharField(max_length=128)
