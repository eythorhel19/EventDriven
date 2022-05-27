from django.db import models
from django.contrib.auth.models import User

#   User


class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image_url = models.CharField(max_length=9999)