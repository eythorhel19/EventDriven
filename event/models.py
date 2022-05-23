from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    maximum_capacity = models.IntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()


class EventImage(models.Model):
    image_url = models.CharField(max_length=9999)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)

# CREATE TABLE Event (
#     event_id SERIAL PRIMARY KEY,
#     title VARCHAR NOT NULL,
#     description VARCHAR NOT NULL,
#     maximum_capacity VARCHAR,
#     start_date TIMESTAMP,
#     end_date TIMESTAMP,
#     location_id INT REFERENCES Location (location_id)
# );

# CREATE TABLE EventImage(
#     event_image_id SERIAL PRIMARY KEY,
#     event_id INT REFERENCES Event (event_id),
#     image_url VARCHAR NOT NULL,
#     description VARCHAR,
#     main_image BOOLEAN NOT NULL DEFAULT FALSE
# );
