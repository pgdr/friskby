# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-24 18:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0063_rawdata_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rawdata',
            name='processed',
        ),
    ]
