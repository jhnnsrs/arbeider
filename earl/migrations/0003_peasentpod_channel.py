# Generated by Django 3.1.5 on 2021-01-29 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('earl', '0002_remove_peasentpod_peasent'),
    ]

    operations = [
        migrations.AddField(
            model_name='peasentpod',
            name='channel',
            field=models.CharField(default='none', help_text='The channel where the Pod listens to', max_length=5000),
        ),
    ]
