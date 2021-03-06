# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-07-15 15:09
from __future__ import unicode_literals

from django_extensions.db.fields import AutoSlugField
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carceropolis', '0008_auto_20180212_2319'),
    ]

    operations = [
        migrations.AddField(
            model_name='areadeatuacao',
            name='descricao_en',
            field=models.TextField(null=True, verbose_name='Descrição'),
        ),
        migrations.AddField(
            model_name='areadeatuacao',
            name='descricao_pt_br',
            field=models.TextField(null=True, verbose_name='Descrição'),
        ),
        migrations.AddField(
            model_name='areadeatuacao',
            name='nome_en',
            field=models.CharField(max_length=250, null=True, unique=True, verbose_name='Nome da área'),
        ),
        migrations.AddField(
            model_name='areadeatuacao',
            name='nome_pt_br',
            field=models.CharField(max_length=250, null=True, unique=True, verbose_name='Nome da área'),
        ),
        migrations.AlterField(
            model_name='areadeatuacao',
            name='slug',
            field=AutoSlugField(editable=False, populate_from='nome_pt_br'),
        ),
    ]
