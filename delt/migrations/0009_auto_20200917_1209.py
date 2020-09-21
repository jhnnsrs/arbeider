# Generated by Django 2.2.14 on 2020-09-17 12:09

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('delt', '0008_auto_20200914_1112'),
    ]

    operations = [
        migrations.AddField(
            model_name='provision',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='provision',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='assignation',
            name='token',
            field=models.CharField(blank=True, default=uuid.UUID('05b8975b-8ed3-4562-8655-78d53d7c8870'), help_text='The Token that created this Provision', max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='provision',
            name='token',
            field=models.CharField(blank=True, default=uuid.UUID('ff15abe9-e5c2-4b9c-885e-d11ae9e63247'), help_text='The Token that created this Provision', max_length=1000),
        ),
    ]