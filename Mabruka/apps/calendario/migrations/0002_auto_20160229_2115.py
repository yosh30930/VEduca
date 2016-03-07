# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-01 03:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('calendario', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Foro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=60)),
                ('padre_id', models.PositiveIntegerField()),
                ('nombre_corto', models.CharField(max_length=60)),
                ('padre_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Panel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=60)),
                ('padre_id', models.PositiveIntegerField()),
                ('allDay', models.NullBooleanField(default=True)),
                ('start', models.DateTimeField(auto_now_add=True)),
                ('end', models.DateTimeField(null=True)),
                ('calId', models.CharField(max_length=60)),
                ('padre_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name_plural': 'Paneles',
            },
        ),
        migrations.CreateModel(
            name='Seminario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=60)),
                ('padre_id', models.PositiveIntegerField()),
                ('padre_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='Actividad',
        ),
        migrations.CreateModel(
            name='EncuentroInternacional',
            fields=[
                ('evento_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='calendario.Evento')),
            ],
            options={
                'verbose_name_plural': 'Encuentros Internacionales',
            },
            bases=('calendario.evento',),
        ),
    ]
