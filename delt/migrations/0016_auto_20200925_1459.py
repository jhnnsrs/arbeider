# Generated by Django 2.2.16 on 2020-09-25 14:59

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('delt', '0015_auto_20200924_1310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignation',
            name='token',
            field=models.CharField(blank=True, default=uuid.UUID('2c086a24-26ab-47de-8acd-909c2b85b570'), help_text='The Token that created this Provision', max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='provision',
            name='token',
            field=models.CharField(blank=True, default=uuid.UUID('ce610e2f-37ed-4b13-9979-34d0612c1ad4'), help_text='The Token that created this Provision', max_length=1000),
        ),
    ]
