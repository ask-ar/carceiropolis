# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-08-19 14:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0007_auto_20180715_0801'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='field',
            name='choices_en',
        ),
        migrations.RemoveField(
            model_name='field',
            name='default_en',
        ),
        migrations.RemoveField(
            model_name='field',
            name='help_text_en',
        ),
        migrations.RemoveField(
            model_name='field',
            name='label_en',
        ),
        migrations.RemoveField(
            model_name='field',
            name='placeholder_text_en',
        ),
        migrations.RemoveField(
            model_name='form',
            name='button_text_en',
        ),
        migrations.RemoveField(
            model_name='form',
            name='content_en',
        ),
        migrations.RemoveField(
            model_name='form',
            name='email_message_en',
        ),
        migrations.RemoveField(
            model_name='form',
            name='email_subject_en',
        ),
        migrations.RemoveField(
            model_name='form',
            name='response_en',
        ),
    ]
