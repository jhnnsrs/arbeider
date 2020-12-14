# Generated by Django 3.1.3 on 2020-12-14 12:45

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('delt', '0004_auto_20201214_0949'),
    ]

    operations = [
        migrations.AddField(
            model_name='datapoint',
            name='port',
            field=models.IntegerField(default=8000, help_text='the port this point lives on'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='assignation',
            name='token',
            field=models.CharField(blank=True, default=uuid.UUID('530d3081-c30f-4359-a047-fc210dd79740'), help_text='The Token that created this Provision', max_length=1000),
        ),
        migrations.AlterField(
            model_name='datamodel',
            name='point',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='models', to='delt.datapoint'),
        ),
        migrations.AlterField(
            model_name='provision',
            name='token',
            field=models.CharField(blank=True, default=uuid.UUID('ff90c308-921c-4a29-b497-7c2981825070'), help_text='The Token that created this Provision', max_length=1000),
        ),
    ]
