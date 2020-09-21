# Generated by Django 2.2.14 on 2020-09-14 11:12

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('delt', '0007_auto_20200908_1026'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='assignation',
            name='token',
            field=models.CharField(blank=True, default=uuid.UUID('a025b363-cc5a-4e55-8564-d165230d8871'), help_text='The Token that created this Provision', max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='provision',
            name='token',
            field=models.CharField(blank=True, default=uuid.UUID('a8dec8e5-11b8-40cb-bab1-4b413d80462a'), help_text='The Token that created this Provision', max_length=1000),
        ),
    ]