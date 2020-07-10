# Generated by Django 2.2.14 on 2020-07-10 12:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('delt', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='KanalPod',
            fields=[
                ('pod_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='delt.Pod')),
                ('channel', models.CharField(help_text='The Channel this Node listenes to', max_length=1000, unique=True)),
            ],
            bases=('delt.pod',),
        ),
    ]
