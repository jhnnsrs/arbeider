# Generated by Django 2.2.14 on 2020-09-21 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elements', '0002_representation_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='representation',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
