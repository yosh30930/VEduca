# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-01 21:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0004_auto_20160501_1653'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='apellido_materno',
            field=models.CharField(blank=True, max_length=100, verbose_name='apellido materno'),
        ),
    ]