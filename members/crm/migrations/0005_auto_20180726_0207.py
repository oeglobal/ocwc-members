# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-26 02:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0004_auto_20180726_0206'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='initiative_title1',
            field=models.CharField(blank=True, default=b'', max_length=255, verbose_name=b'Title'),
        ),
        migrations.AddField(
            model_name='organization',
            name='initiative_title2',
            field=models.CharField(blank=True, default=b'', max_length=255, verbose_name=b'Title'),
        ),
        migrations.AddField(
            model_name='organization',
            name='initiative_title3',
            field=models.CharField(blank=True, default=b'', max_length=255, verbose_name=b'Title'),
        ),
    ]
