# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-29 03:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0003_foro_descripcion'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='panel',
            options={'verbose_name_plural': 'paneles'},
        ),
        migrations.RenameField(
            model_name='panel',
            old_name='start',
            new_name='fecha_inicio',
        ),
        migrations.RemoveField(
            model_name='panel',
            name='allDay',
        ),
        migrations.AlterField(
            model_name='foro',
            name='descripcion',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='foro',
            name='nombre_corto',
            field=models.CharField(blank=True, max_length=60),
        ),
    ]