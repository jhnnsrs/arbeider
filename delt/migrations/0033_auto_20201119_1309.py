# Generated by Django 3.1.3 on 2020-11-19 13:09

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('delt', '0032_auto_20201119_1305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignation',
            name='token',
            field=models.CharField(blank=True, default=uuid.UUID('533fffcb-0ce3-4752-80ec-6643210ef6ef'), help_text='The Token that created this Provision', max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='provision',
            name='token',
            field=models.CharField(blank=True, default=uuid.UUID('d2ae0ed0-6d21-4dd8-af0a-44a766031f96'), help_text='The Token that created this Provision', max_length=1000),
        ),
    ]
