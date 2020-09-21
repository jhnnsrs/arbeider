# Generated by Django 2.2.14 on 2020-07-21 08:23

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('delt', '0002_auto_20200713_1439'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignation',
            name='token',
            field=models.CharField(blank=True, default=uuid.UUID('d83791de-a7e6-4706-8468-f3d5c9a17610'), help_text='The Token that created this Provision', max_length=1000),
        ),
        migrations.AddField(
            model_name='provision',
            name='token',
            field=models.CharField(blank=True, default=uuid.UUID('768425c1-15c1-4813-a1be-233b87b58f9e'), help_text='The Token that created this Provision', max_length=1000),
        ),
    ]