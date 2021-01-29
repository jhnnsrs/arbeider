# Generated by Django 3.1.5 on 2021-01-29 11:53

import delt.fields
import delt.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import oauth2_provider.generators
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DataPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('installed_at', models.DateTimeField(auto_created=True, auto_now_add=True)),
                ('host', models.CharField(help_text='Where are we storing this??', max_length=100)),
                ('inward', models.CharField(default='arbeider', help_text='The Microservice way', max_length=100)),
                ('name', models.CharField(help_text='A unique identifier for this datapoint, will be prepeneded to the Model it hosts', max_length=100, unique=True)),
                ('port', models.IntegerField(help_text='the port this point lives on')),
                ('type', models.CharField(choices=[('graphql', 'graphql'), ('rest', 'rest')], help_text='The Type of API', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(editable=False, help_text='A unique identifier of this Node on this Platform, calculated hashing the package and interface', max_length=1000, unique=True)),
                ('variety', models.CharField(help_text='Is this Node a Frontend, Backend, DaskExlusiv Node?', max_length=1000)),
                ('realm', models.CharField(help_text='The realm this Node was registered to?', max_length=1000)),
                ('package', models.CharField(help_text='The Package this Node belongs to', max_length=1000)),
                ('interface', models.CharField(help_text='The unique interface of this Node within the Package', max_length=1000)),
                ('publishers', delt.fields.PublishersField(default=dict, help_text='The publishers thie Node will send to')),
                ('name', models.CharField(help_text='The Package that channel belongs to', max_length=1000)),
                ('description', models.TextField(help_text='A Short description for the Node')),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('inputs', delt.fields.InputsField(default=list)),
                ('outputs', delt.fields.OutputsField(default=list)),
                ('nodeclass', models.CharField(default='classic-node', max_length=400)),
            ],
        ),
        migrations.CreateModel(
            name='Pod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('podclass', models.CharField(default='classic-pod', max_length=400)),
                ('status', models.CharField(default='pending', max_length=300)),
                ('unique', models.UUIDField(default=uuid.uuid4, help_text='The Unique identifier of this POD', unique=True)),
                ('policy', models.CharField(default='*', max_length=5000)),
            ],
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('installed_at', models.DateTimeField(auto_created=True, auto_now_add=True)),
                ('name', models.CharField(help_text='This Providers Name', max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=delt.utils.generate_random_name, help_text='The name of this template', max_length=1000)),
                ('params', models.JSONField(blank=True, null=True)),
                ('identifier', models.CharField(default=uuid.uuid4, help_text='A unique identifier for this template', max_length=500, unique=True)),
                ('version', models.CharField(help_text='A short descriptor for the kind of version', max_length=400)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('node', models.ForeignKey(help_text='The Node this Template Belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='templates', to='delt.node')),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='delt.provider')),
            ],
        ),
        migrations.CreateModel(
            name='Selector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kwargs', delt.fields.KwargsField(blank=True, help_text='The Specific inputs this selector needs and their types', null=True)),
                ('provider', models.ForeignKey(help_text='The provider these kwargs belong to', on_delete=django.db.models.deletion.CASCADE, related_name='selectors', to='delt.provider')),
            ],
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(editable=False, help_text='A unique identifier of this Route on this Platform, calculated hashing the package and interface', max_length=1000, unique=True)),
                ('url', models.URLField(help_text='The url to the Route', max_length=1000)),
                ('package', models.CharField(help_text='The Package this Node belongs to', max_length=1000)),
                ('provider', models.CharField(help_text='The Provider of this Route', max_length=1000)),
                ('interface', models.CharField(help_text='The unique interface of this Node within the Package', max_length=1000)),
                ('name', models.CharField(help_text='The Package that channel belongs to', max_length=1000)),
                ('description', models.TextField(help_text='A Short description for the Node')),
                ('node', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='routes', to='delt.node')),
            ],
        ),
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='A unique identifier of this Repository on this Platform, calculated hashing the package and interface', max_length=1000)),
                ('type', models.CharField(help_text='What sort of repository is this', max_length=300)),
                ('creator', models.ForeignKey(blank=True, help_text='The Person that created this repository', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Provision',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kwargs', models.JSONField(blank=True, help_text='Kwargs for the Provider', null=True)),
                ('reference', models.CharField(default=uuid.uuid4, help_text='The Unique identifier of this Provision', max_length=1000, unique=True)),
                ('status', models.CharField(blank=True, help_text='This provisions status', max_length=1000)),
                ('statusmessage', models.CharField(blank=True, help_text='This provisions status', max_length=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('token', models.CharField(blank=True, default=uuid.UUID('7a9379c6-6a17-40b7-9c1d-032eba3d42b8'), help_text='The Token that created this Provision', max_length=1000)),
                ('node', models.ForeignKey(help_text='The node this provision connects', on_delete=django.db.models.deletion.CASCADE, related_name='provisions', to='delt.node')),
                ('parent', models.ForeignKey(blank=True, help_text='The Provisions parent', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='delt.provision')),
                ('pod', models.ForeignKey(blank=True, help_text='The pod this provision connects', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='provisions', to='delt.pod')),
                ('provider', models.ForeignKey(help_text='The provider we might want', on_delete=django.db.models.deletion.CASCADE, to='delt.provider')),
                ('user', models.ForeignKey(help_text='This provision creator', max_length=1000, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProviderSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_created=True, auto_now_add=True)),
                ('active', models.BooleanField(default=True, help_text='Is this provider active or no longer active?')),
                ('provider', models.ForeignKey(help_text='The implemented Provider!', on_delete=django.db.models.deletion.CASCADE, to='delt.provider')),
            ],
        ),
        migrations.AddField(
            model_name='pod',
            name='template',
            field=models.ForeignKey(help_text='The template used to create this pod', on_delete=django.db.models.deletion.CASCADE, related_name='pods', to='delt.template'),
        ),
        migrations.AddField(
            model_name='node',
            name='repository',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='nodes', to='delt.repository'),
        ),
        migrations.CreateModel(
            name='DataModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('installed_at', models.DateTimeField(auto_created=True, auto_now_add=True)),
                ('identifier', models.CharField(help_text=' A unique identifier for this model in its Datapoint', max_length=100)),
                ('extenders', models.JSONField(blank=True, help_text='Unique identifiers for a Datamodel, good for introspection', null=True)),
                ('point', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='models', to='delt.datapoint')),
            ],
        ),
        migrations.CreateModel(
            name='Assignation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inputs', delt.fields.InputsField(blank=True, help_text='The Inputs', null=True)),
                ('reference', models.CharField(default=uuid.uuid4, help_text='The Unique identifier of this Assignation', max_length=1000, unique=True)),
                ('status', models.CharField(help_text='This assignations status', max_length=1000)),
                ('statusmessage', models.CharField(blank=True, help_text='This assignation status message', max_length=1000)),
                ('outputs', delt.fields.OutputsField(blank=True, help_text='The Outputs', null=True)),
                ('callback', models.CharField(help_text='The Callback queue once the Assignation has finished', max_length=1000)),
                ('progress', models.CharField(help_text='The Progress queue once the Assignation has finished', max_length=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('token', models.CharField(blank=True, default=uuid.UUID('c99fd2c9-1100-4a20-b546-e53f9938e4f3'), help_text='The Token that created this Provision', max_length=1000)),
                ('creator', models.ForeignKey(help_text='This provision creator', max_length=1000, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('node', models.ForeignKey(blank=True, help_text='The Node this assignation is having', null=True, on_delete=django.db.models.deletion.CASCADE, to='delt.node')),
                ('pod', models.ForeignKey(blank=True, help_text='The pod this provision connects', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assignations', to='delt.pod')),
                ('template', models.ForeignKey(blank=True, help_text='The Node this assignation is having', null=True, on_delete=django.db.models.deletion.CASCADE, to='delt.template')),
            ],
            options={
                'permissions': (('can_assign', 'Assign Job'),),
            },
        ),
        migrations.CreateModel(
            name='ArnheimApplication',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('client_id', models.CharField(db_index=True, default=oauth2_provider.generators.generate_client_id, max_length=100, unique=True)),
                ('redirect_uris', models.TextField(blank=True, help_text='Allowed URIs list, space separated')),
                ('client_type', models.CharField(choices=[('confidential', 'Confidential'), ('public', 'Public')], max_length=32)),
                ('authorization_grant_type', models.CharField(choices=[('authorization-code', 'Authorization code'), ('implicit', 'Implicit'), ('password', 'Resource owner password-based'), ('client-credentials', 'Client credentials')], max_length=32)),
                ('client_secret', models.CharField(blank=True, db_index=True, default=oauth2_provider.generators.generate_client_secret, max_length=255)),
                ('name', models.CharField(blank=True, max_length=255)),
                ('skip_authorization', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='delt_arnheimapplication', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
