# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-29 03:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0004_auto_20160328_2104'),
    ]

    operations = [
        migrations.RenameField(
            model_name='panel',
            old_name='end',
            new_name='fecha_fin',
        ),
    ]
