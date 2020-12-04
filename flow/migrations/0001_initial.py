# Generated by Django 3.1.3 on 2020-12-03 11:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('delt', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Engine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Graph',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(default='1.0alpha', max_length=100)),
                ('name', models.CharField(default='Not Set', max_length=100, null=True)),
                ('diagram', models.JSONField()),
                ('description', models.CharField(default='Add a Description', max_length=50000)),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
            ],
        ),
        migrations.CreateModel(
            name='FlowNode',
            fields=[
                ('node_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='delt.node')),
                ('graph', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='flow.graph')),
            ],
            bases=('delt.node',),
        ),
        migrations.CreateModel(
            name='Flow',
            fields=[
                ('template_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='delt.template')),
                ('diagram', models.JSONField()),
                ('engine', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='flow.engine')),
            ],
            bases=('delt.template',),
        ),
    ]
