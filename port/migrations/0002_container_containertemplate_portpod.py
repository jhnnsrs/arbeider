# Generated by Django 3.1.3 on 2020-12-10 12:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('delt', '0010_auto_20201210_1231'),
        ('port', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Container',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.CharField(max_length=100)),
                ('tag', models.CharField(max_length=100)),
                ('repository', models.CharField(default='dockerhub', max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='PortPod',
            fields=[
                ('pod_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='delt.pod')),
                ('container_id', models.CharField(max_length=2000)),
            ],
            bases=('delt.pod',),
        ),
        migrations.CreateModel(
            name='ContainerTemplate',
            fields=[
                ('template_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='delt.template')),
                ('container', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='port.container')),
            ],
            bases=('delt.template',),
        ),
    ]