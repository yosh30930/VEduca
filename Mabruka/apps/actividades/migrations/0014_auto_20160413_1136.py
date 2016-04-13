# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-13 16:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0004_auto_20160413_1136'),
        ('actividades', '0013_auto_20160409_1604'),
    ]

    operations = [
        migrations.AddField(
            model_name='panel',
            name='coordinador',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='coordiandor_panel', to='usuarios.Participante'),
        ),
        migrations.AddField(
            model_name='panel',
            name='intervienen',
            field=models.ManyToManyField(blank=True, to='usuarios.Participante'),
        ),
        migrations.AddField(
            model_name='panel',
            name='moderador',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='moderador_panel', to='usuarios.Participante'),
        ),
    ]
