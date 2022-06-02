# Generated by Django 4.0.4 on 2022-06-01 13:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_ticket_phone_country_ticket_phone_number'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetails',
            name='phone_country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.country'),
        ),
        migrations.AddField(
            model_name='userdetails',
            name='phone_number',
            field=models.CharField(default=7777777, max_length=32),
            preserve_default=False,
        ),
    ]
