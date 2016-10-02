# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-10-02 18:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('blog', '0002_auto_20150527_1555'),
    ]

    operations = [
        migrations.CreateModel(
            name='AreaDeAtuacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_da_area', models.CharField(max_length=250, unique=True)),
                ('descricao', models.TextField()),
                ('ordem', models.IntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Especialidade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_da_especialidade', models.CharField(max_length=80, unique=True)),
                ('descricao', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Especialista',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=250)),
                ('email', models.EmailField(max_length=254)),
                ('telefone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128)),
                ('mini_bio', models.CharField(blank=True, max_length=250)),
                ('instituicao', models.CharField(max_length=250)),
                ('area_de_atuacao', models.ManyToManyField(to='carceropolis.AreaDeAtuacao')),
                ('especialidades', models.ManyToManyField(to='carceropolis.Especialidade')),
            ],
        ),
        migrations.CreateModel(
            name='Publicacao',
            fields=[
                ('blogpost_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='blog.BlogPost')),
                ('arquivo_publicacao', models.FileField(upload_to=b'publicacoes/', verbose_name=b'Arquivo da Publica\xc3\xa7\xc3\xa3o')),
                ('categorias', models.ManyToManyField(to='carceropolis.AreaDeAtuacao')),
            ],
            options={
                'verbose_name_plural': 'Publica\xe7\xf5es',
            },
            bases=('blog.blogpost',),
        ),
    ]
