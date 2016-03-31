# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-26 20:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encuentro',
            name='responsables',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='foro',
            name='responsables',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='panel',
            name='responsables',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='seminario',
            name='responsables',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
