# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-13 16:36
from __future__ import unicode_literals

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0003_auto_20160412_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participante',
            name='pais',
            field=django_countries.fields.CountryField(blank=True, max_length=2, null=True),
        ),
    ]
