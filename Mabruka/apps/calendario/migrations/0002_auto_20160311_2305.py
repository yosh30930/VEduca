# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-12 05:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calendario', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='relacion',
            name='hijo_type',
        ),
        migrations.RemoveField(
            model_name='relacion',
            name='padre_type',
        ),
        migrations.RemoveField(
            model_name='foro',
            name='relacion',
        ),
        migrations.RemoveField(
            model_name='panel',
            name='relacion',
        ),
        migrations.RemoveField(
            model_name='seminario',
            name='relacion',
        ),
        migrations.DeleteModel(
            name='Relacion',
        ),
    ]
