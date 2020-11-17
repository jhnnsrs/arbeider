# Generated by Django 3.1.3 on 2020-11-13 15:40

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('delt', '0029_auto_20201015_1402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignation',
            name='token',
            field=models.CharField(blank=True, default=uuid.UUID('7d48f2d6-7956-485e-9018-989962c1de66'), help_text='The Token that created this Provision', max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='provision',
            name='token',
            field=models.CharField(blank=True, default=uuid.UUID('b2f902e2-de70-4f28-a107-94b67ee336c6'), help_text='The Token that created this Provision', max_length=1000),
        ),
    ]