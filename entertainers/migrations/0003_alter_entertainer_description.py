# Generated by Django 4.0.4 on 2022-05-25 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entertainers', '0002_entertainer_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entertainer',
            name='description',
            field=models.CharField(max_length=1020),
        ),
    ]
