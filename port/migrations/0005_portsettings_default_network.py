# Generated by Django 3.1.3 on 2020-12-10 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('port', '0004_portsettings'),
    ]

    operations = [
        migrations.AddField(
            model_name='portsettings',
            name='default_network',
            field=models.CharField(default='dev', max_length=100),
        ),
    ]
