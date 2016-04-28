# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-26 18:06
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Encuentro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=300)),
                ('anotaciones', models.TextField(blank=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_edicion', models.DateTimeField(auto_now=True)),
                ('fecha_inicio', models.DateField(default=datetime.date.today)),
                ('fecha_fin', models.DateField(default=datetime.date.today)),
                ('pais', models.CharField(blank=True, max_length=100)),
                ('ciudad', models.CharField(blank=True, max_length=100)),
                ('responsables', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
                'ordering': ['fecha_creacion', 'nombre'],
            },
        ),
        migrations.CreateModel(
            name='Espacio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('cupo', models.PositiveIntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Foro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=300)),
                ('anotaciones', models.TextField(blank=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_edicion', models.DateTimeField(auto_now=True)),
                ('nombre_corto', models.CharField(blank=True, max_length=200)),
                ('descripcion', models.TextField(blank=True, default='')),
                ('responsables', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
                'ordering': ['fecha_creacion', 'nombre'],
            },
        ),
        migrations.CreateModel(
            name='Institucion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Nodo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_id', models.PositiveIntegerField()),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='actividades.Nodo')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('_default_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='OtraActividadSeminario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=300)),
                ('anotaciones', models.TextField(blank=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_edicion', models.DateTimeField(auto_now=True)),
                ('fecha', models.DateTimeField(blank=True, null=True)),
                ('duracion_mins', models.PositiveSmallIntegerField(default=60)),
                ('orden', models.PositiveSmallIntegerField()),
                ('responsables', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
                'ordering': ['fecha_creacion', 'nombre'],
            },
        ),
        migrations.CreateModel(
            name='Panel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=300)),
                ('anotaciones', models.TextField(blank=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_edicion', models.DateTimeField(auto_now=True)),
                ('nombre_corto', models.CharField(blank=True, max_length=200)),
                ('fecha', models.DateTimeField(blank=True, null=True)),
                ('duracion', models.PositiveSmallIntegerField(default=60)),
                ('orden', models.PositiveSmallIntegerField()),
                ('responsables', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'paneles',
            },
        ),
        migrations.CreateModel(
            name='PresentacionPonencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=300)),
                ('anotaciones', models.TextField(blank=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_edicion', models.DateTimeField(auto_now=True)),
                ('fecha', models.DateTimeField(blank=True, null=True)),
                ('duracion_mins', models.PositiveSmallIntegerField(default=60)),
                ('orden', models.PositiveSmallIntegerField()),
                ('responsables', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
                'ordering': ['fecha_creacion', 'nombre'],
            },
        ),
        migrations.CreateModel(
            name='Reunion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=300)),
                ('anotaciones', models.TextField(blank=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_edicion', models.DateTimeField(auto_now=True)),
                ('fecha', models.DateTimeField(blank=True, null=True)),
                ('duracion_mins', models.PositiveSmallIntegerField(default=180)),
                ('tipo_asistencia', models.CharField(blank=True, max_length=200)),
                ('espacio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='actividades.Espacio')),
                ('responsables', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'talleres',
            },
        ),
        migrations.CreateModel(
            name='Sede',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('encuentro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='actividades.Encuentro')),
            ],
        ),
        migrations.CreateModel(
            name='Seminario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=300)),
                ('anotaciones', models.TextField(blank=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_edicion', models.DateTimeField(auto_now=True)),
                ('nombre_corto', models.CharField(blank=True, max_length=60)),
                ('responsables', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
                'ordering': ['fecha_creacion', 'nombre'],
            },
        ),
        migrations.CreateModel(
            name='SesionEspecial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=300)),
                ('anotaciones', models.TextField(blank=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_edicion', models.DateTimeField(auto_now=True)),
                ('fecha', models.DateTimeField(blank=True, null=True)),
                ('duracion_mins', models.PositiveSmallIntegerField(default=60)),
                ('orden', models.PositiveSmallIntegerField()),
                ('responsables', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
                'ordering': ['fecha_creacion', 'nombre'],
            },
        ),
        migrations.CreateModel(
            name='Taller',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=300)),
                ('anotaciones', models.TextField(blank=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_edicion', models.DateTimeField(auto_now=True)),
                ('fecha', models.DateTimeField(blank=True, null=True)),
                ('duracion_mins', models.PositiveSmallIntegerField(default=180)),
                ('publico_objetivo', models.CharField(blank=True, max_length=200)),
                ('espacio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='actividades.Espacio')),
                ('responsables', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'talleres',
            },
        ),
        migrations.AddField(
            model_name='espacio',
            name='sede',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='actividades.Sede'),
        ),
    ]
