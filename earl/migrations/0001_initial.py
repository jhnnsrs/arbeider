# Generated by Django 3.1.5 on 2021-01-29 11:53

from django.db import migrations, models
import django.db.models.deletion
import namegenerator


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('delt', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Peasent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=namegenerator.gen, max_length=300, unique=True)),
                ('application', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='delt.arnheimapplication')),
            ],
        ),
        migrations.CreateModel(
            name='PeasentTemplate',
            fields=[
                ('template_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='delt.template')),
                ('peasent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='earl.peasent')),
            ],
            bases=('delt.template',),
        ),
        migrations.CreateModel(
            name='PeasentPod',
            fields=[
                ('pod_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='delt.pod')),
                ('peasent', models.ForeignKey(blank=True, help_text='Which Peasent is in charge of hosting this Peasent?', null=True, on_delete=django.db.models.deletion.CASCADE, to='earl.peasent')),
            ],
            bases=('delt.pod',),
        ),
    ]
