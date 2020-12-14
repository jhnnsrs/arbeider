# Generated by Django 3.1.3 on 2020-12-14 09:21

import delt.enums
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('delt', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('installed_at', models.DateTimeField(auto_created=True, auto_now_add=True)),
                ('identifier', models.CharField(help_text=' A unique identifier for this model in its Datapoint', max_length=100)),
                ('extenders', models.JSONField(blank=True, help_text='Unique identifiers for a Datamodel, good for introspection', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DataPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('installed_at', models.DateTimeField(auto_created=True, auto_now_add=True)),
                ('name', models.CharField(help_text='A unique identifier for this datapoint, will be prepeneded to the Model it hosts', max_length=100)),
                ('type', models.CharField(choices=[(delt.enums.Endpoint['GRAPHQL'], 'graphql'), (delt.enums.Endpoint['REST'], 'rest')], help_text='The Type of API', max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='assignation',
            name='token',
            field=models.CharField(blank=True, default=uuid.UUID('4697a0e1-d49b-4c6a-ab73-a0c742493b03'), help_text='The Token that created this Provision', max_length=1000),
        ),
        migrations.AlterField(
            model_name='provision',
            name='token',
            field=models.CharField(blank=True, default=uuid.UUID('fbf4383e-f5f4-41c1-b6e6-831e228486d8'), help_text='The Token that created this Provision', max_length=1000),
        ),
    ]
