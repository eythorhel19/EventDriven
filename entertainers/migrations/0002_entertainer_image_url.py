# Generated by Django 4.0.4 on 2022-05-25 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entertainers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='entertainer',
            name='image_url',
            field=models.CharField(default='https://upload.wikimedia.org/wikipedia/commons/b/b1/Missing-image-232x150.png', max_length=999),
        ),
    ]
