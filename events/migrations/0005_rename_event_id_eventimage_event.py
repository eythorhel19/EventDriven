# Generated by Django 4.0.4 on 2022-05-25 00:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_eventimage_main'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eventimage',
            old_name='event_id',
            new_name='event',
        ),
    ]
