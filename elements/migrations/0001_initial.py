# Generated by Django 2.2.12 on 2020-05-28 15:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import elements.models
import herre.storage.s3
import matrise.defaults
import matrise.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('age', models.CharField(max_length=400)),
                ('type', models.CharField(max_length=500)),
                ('creator', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=1000)),
                ('description_long', models.TextField(blank=True, null=True)),
                ('linked_paper', models.URLField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='experiment_banner')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ExperimentalGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The experimental groups name', max_length=200)),
                ('description', models.CharField(help_text='A brief summary of applied techniques in this group', max_length=1000)),
                ('iscontrol', models.BooleanField(help_text='Is this Experimental Group a ControlGroup?')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('experiment', models.ForeignKey(help_text='The experiment this Group belongs too', on_delete=django.db.models.deletion.CASCADE, to='elements.Experiment')),
            ],
        ),
        migrations.CreateModel(
            name='Representation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store', matrise.fields.StoreField(blank=True, help_text='The location of the Array on the Storage System (S3 or Media-URL)', null=True, storage=herre.storage.s3.ZarrStorage(), upload_to='zarr', verbose_name='store')),
                ('shape', matrise.fields.ShapeField(base_field=models.IntegerField(), help_text='The arrays shape', size=None)),
                ('dims', matrise.fields.DimsField(base_field=models.CharField(max_length=100), help_text='The arrays dimension', size=None)),
                ('name', models.CharField(blank=True, help_text='Cleartext name', max_length=1000, null=True)),
                ('signature', models.CharField(blank=True, help_text='The arrays unique signature (check Doc on: Signatures)', max_length=300, null=True)),
                ('unique', models.UUIDField(default=uuid.uuid4, editable=False, help_text='A unique identifier for this array')),
                ('fileversion', models.CharField(default=matrise.defaults.get_default_file_version, help_text='The File Version of this Array', max_length=1000)),
                ('type', models.CharField(blank=True, help_text='The Representation can have varying types, consult your API', max_length=400, null=True)),
                ('chain', models.CharField(blank=True, max_length=9000, null=True)),
                ('nodeid', models.CharField(blank=True, max_length=400, null=True)),
                ('creator', models.ForeignKey(help_text='The Person that created this representation', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('origin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='derived', related_query_name='derived', to='elements.Representation')),
            ],
            options={
                'permissions': [('download_representation', 'Can download Presentation')],
                'base_manager_name': 'objects',
                'default_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='ROI',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nodeid', models.CharField(blank=True, max_length=400, null=True)),
                ('vectors', models.CharField(help_text='A json dump of the ROI Vectors (specific for each type)', max_length=3000)),
                ('color', models.CharField(blank=True, max_length=100, null=True)),
                ('signature', models.CharField(blank=True, max_length=300, null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('experimentalgroup', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='elements.ExperimentalGroup')),
                ('representation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rois', to='elements.Representation')),
            ],
            options={
                'base_manager_name': 'objects',
                'default_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filepath', models.FilePathField(max_length=400)),
                ('vid', models.CharField(max_length=1000)),
                ('type', models.CharField(max_length=100)),
                ('compression', models.CharField(blank=True, max_length=300, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store', matrise.fields.StoreField(blank=True, help_text='The location of the Array on the Storage System (S3 or Media-URL)', null=True, storage=herre.storage.s3.ZarrStorage(), upload_to='zarr', verbose_name='store')),
                ('shape', matrise.fields.ShapeField(base_field=models.IntegerField(), help_text='The arrays shape', size=None)),
                ('dims', matrise.fields.DimsField(base_field=models.CharField(max_length=100), help_text='The arrays dimension', size=None)),
                ('name', models.CharField(blank=True, help_text='Cleartext name', max_length=1000, null=True)),
                ('signature', models.CharField(blank=True, help_text='The arrays unique signature (check Doc on: Signatures)', max_length=300, null=True)),
                ('unique', models.UUIDField(default=uuid.uuid4, editable=False, help_text='A unique identifier for this array')),
                ('fileversion', models.CharField(default=matrise.defaults.get_default_file_version, help_text='The File Version of this Array', max_length=1000)),
                ('nodeid', models.CharField(blank=True, max_length=400, null=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('inputtransformation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='elements.Transformation')),
                ('representation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transformations', to='elements.Representation')),
                ('roi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transformations', to='elements.ROI')),
            ],
            options={
                'base_manager_name': 'objects',
                'default_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('nodeid', models.CharField(blank=True, max_length=400, null=True)),
                ('animal', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='elements.Animal')),
                ('creator', models.ForeignKey(on_delete=models.SET(elements.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
                ('experiment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='elements.Experiment')),
                ('experimentalgroup', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='elements.ExperimentalGroup')),
            ],
        ),
        migrations.AddField(
            model_name='representation',
            name='sample',
            field=models.ForeignKey(help_text='The Sample this representation belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='representations', to='elements.Sample'),
        ),
        migrations.CreateModel(
            name='FileMatchString',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('regexp', models.CharField(max_length=4000)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Antibody',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('creator', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='animal',
            name='experiment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='elements.Experiment'),
        ),
        migrations.AddField(
            model_name='animal',
            name='experimentalgroup',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='elements.ExperimentalGroup'),
        ),
    ]
