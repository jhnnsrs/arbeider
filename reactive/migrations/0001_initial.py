# Generated by Django 3.1.5 on 2021-01-29 11:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('flow', '0001_initial'),
        ('port', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RxCompiler',
            fields=[
                ('compiler_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='flow.compiler')),
            ],
            bases=('flow.compiler',),
        ),
        migrations.CreateModel(
            name='RxGraph',
            fields=[
                ('executiongraph_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='flow.executiongraph')),
                ('value', models.JSONField()),
            ],
            bases=('flow.executiongraph',),
        ),
        migrations.CreateModel(
            name='RxPod',
            fields=[
                ('portpod_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='port.portpod')),
            ],
            bases=('port.portpod',),
        ),
        migrations.CreateModel(
            name='RxTemplate',
            fields=[
                ('containertemplate_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='port.containertemplate')),
                ('graph', models.ForeignKey(help_text='The RxGraph atached to this potential Worker', on_delete=django.db.models.deletion.CASCADE, to='reactive.rxgraph')),
            ],
            bases=('port.containertemplate',),
        ),
        migrations.CreateModel(
            name='RxSettings',
            fields=[
                ('portsettings_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='port.portsettings')),
                ('engine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='port.container')),
            ],
            bases=('port.portsettings',),
        ),
    ]
