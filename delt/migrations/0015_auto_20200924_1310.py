# Generated by Django 2.2.16 on 2020-09-24 13:10

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('delt', '0014_auto_20200921_1226'),
    ]

    operations = [
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='A unique identifier of this Repository on this Platform, calculated hashing the package and interface', max_length=1000, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='assignation',
            name='token',
            field=models.CharField(blank=True, default=uuid.UUID('08a4cc5e-3c4f-4f31-967b-c2e9a1d624ca'), help_text='The Token that created this Provision', max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='provision',
            name='token',
            field=models.CharField(blank=True, default=uuid.UUID('917c3976-ec03-4b36-b4d2-8d2df4016d5e'), help_text='The Token that created this Provision', max_length=1000),
        ),
        migrations.AddField(
            model_name='node',
            name='repository',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='delt.Repository'),
        ),
    ]
