from django.db import models

# Create your models here.


class Entertainer(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1020)
    image_url = models.CharField(
        max_length=999, default='https://upload.wikimedia.org/wikipedia/commons/b/b1/Missing-image-232x150.png')

    def __str__(self):
        return self.name
