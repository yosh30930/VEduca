# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-12 22:21
from __future__ import unicode_literals

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_participante'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participante',
            name='pais',
            field=django_countries.fields.CountryField(blank=True, default='', max_length=2),
            preserve_default=False,
        ),
    ]
