# Generated by Django 2.2.12 on 2020-04-20 13:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delt', '0002_auto_20200420_1215'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pod',
            old_name='provisioner',
            new_name='provider',
        ),
    ]