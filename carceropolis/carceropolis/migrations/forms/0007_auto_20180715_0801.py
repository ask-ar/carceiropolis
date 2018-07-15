# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-07-15 11:01
from __future__ import unicode_literals

from django.db import migrations, models
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0006_auto_20170425_2225'),
    ]

    operations = [
        migrations.AddField(
            model_name='field',
            name='choices_en',
            field=models.CharField(blank=True, help_text='Comma separated options where applicable. If an option itself contains commas, surround the option with `backticks`.', max_length=1000, null=True, verbose_name='Choices'),
        ),
        migrations.AddField(
            model_name='field',
            name='choices_pt_br',
            field=models.CharField(blank=True, help_text='Comma separated options where applicable. If an option itself contains commas, surround the option with `backticks`.', max_length=1000, null=True, verbose_name='Choices'),
        ),
        migrations.AddField(
            model_name='field',
            name='default_en',
            field=models.CharField(blank=True, max_length=2000, null=True, verbose_name='Default value'),
        ),
        migrations.AddField(
            model_name='field',
            name='default_pt_br',
            field=models.CharField(blank=True, max_length=2000, null=True, verbose_name='Default value'),
        ),
        migrations.AddField(
            model_name='field',
            name='help_text_en',
            field=models.TextField(blank=True, null=True, verbose_name='Help text'),
        ),
        migrations.AddField(
            model_name='field',
            name='help_text_pt_br',
            field=models.TextField(blank=True, null=True, verbose_name='Help text'),
        ),
        migrations.AddField(
            model_name='field',
            name='label_en',
            field=models.TextField(null=True, verbose_name='Label'),
        ),
        migrations.AddField(
            model_name='field',
            name='label_pt_br',
            field=models.TextField(null=True, verbose_name='Label'),
        ),
        migrations.AddField(
            model_name='field',
            name='placeholder_text_en',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Placeholder Text'),
        ),
        migrations.AddField(
            model_name='field',
            name='placeholder_text_pt_br',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Placeholder Text'),
        ),
        migrations.AddField(
            model_name='form',
            name='button_text_en',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Button text'),
        ),
        migrations.AddField(
            model_name='form',
            name='button_text_pt_br',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Button text'),
        ),
        migrations.AddField(
            model_name='form',
            name='content_en',
            field=mezzanine.core.fields.RichTextField(null=True, verbose_name='Content'),
        ),
        migrations.AddField(
            model_name='form',
            name='content_pt_br',
            field=mezzanine.core.fields.RichTextField(null=True, verbose_name='Content'),
        ),
        migrations.AddField(
            model_name='form',
            name='email_message_en',
            field=models.TextField(blank=True, help_text='Emails sent based on the above options will contain each of the form fields entered. You can also enter a message here that will be included in the email.', null=True, verbose_name='Message'),
        ),
        migrations.AddField(
            model_name='form',
            name='email_message_pt_br',
            field=models.TextField(blank=True, help_text='Emails sent based on the above options will contain each of the form fields entered. You can also enter a message here that will be included in the email.', null=True, verbose_name='Message'),
        ),
        migrations.AddField(
            model_name='form',
            name='email_subject_en',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Subject'),
        ),
        migrations.AddField(
            model_name='form',
            name='email_subject_pt_br',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Subject'),
        ),
        migrations.AddField(
            model_name='form',
            name='response_en',
            field=mezzanine.core.fields.RichTextField(null=True, verbose_name='Response'),
        ),
        migrations.AddField(
            model_name='form',
            name='response_pt_br',
            field=mezzanine.core.fields.RichTextField(null=True, verbose_name='Response'),
        ),
    ]
