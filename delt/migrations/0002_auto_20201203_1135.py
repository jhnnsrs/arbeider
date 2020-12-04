# Generated by Django 3.1.3 on 2020-12-03 11:35

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('delt', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignation',
            name='token',
            field=models.CharField(blank=True, default=uuid.UUID('6ef0b16a-85b5-484e-b467-6c46f57740f9'), help_text='The Token that created this Provision', max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='provision',
            name='token',
            field=models.CharField(blank=True, default=uuid.UUID('83741ffb-1d6d-4ea2-ad98-277f041882b3'), help_text='The Token that created this Provision', max_length=1000),
        ),
    ]