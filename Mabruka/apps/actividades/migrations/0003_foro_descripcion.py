# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-26 23:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0002_auto_20160326_1421'),
    ]

    operations = [
        migrations.AddField(
            model_name='foro',
            name='descripcion',
            field=models.TextField(default=''),
        ),
    ]
