# Generated by Django 3.1.3 on 2020-12-10 16:02

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('delt', '0020_auto_20201210_1530'),
    ]

    operations = [
        migrations.AddField(
            model_name='provision',
            name='statusmessage',
            field=models.CharField(blank=True, help_text='This provisions status', max_length=1000),
        ),
        migrations.AlterField(
            model_name='assignation',
            name='token',
            field=models.CharField(blank=True, default=uuid.UUID('845d4f93-e467-47c6-80e3-9f5321f5b8a8'), help_text='The Token that created this Provision', max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='provision',
            name='token',
            field=models.CharField(blank=True, default=uuid.UUID('1abf4fc3-ccc2-48f8-9b20-81bd309d073a'), help_text='The Token that created this Provision', max_length=1000),
        ),
    ]
