# Generated by Django 4.0.4 on 2022-05-27 13:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_delete_userdetails'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticket',
            old_name='postal_code_id',
            new_name='postal_code',
        ),
    ]
