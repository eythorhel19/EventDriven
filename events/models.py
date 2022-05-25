from django.db import models

# Create your models here.


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1020)
    maximum_capacity = models.IntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.ForeignKey('home.Location', on_delete=models.CASCADE)
    main_image_url = models.CharField(max_length=1020, default='https://upload.wikimedia.org/wikipedia/commons/b/b1/Missing-image-232x150.png')


class EventImage(models.Model):
    image_url = models.CharField(max_length=9999)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
