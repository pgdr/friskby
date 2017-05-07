# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-19 05:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0061_device_channel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='altitude',
            field=models.FloatField(default=0, verbose_name=b'Altitude'),
            preserve_default=False,
        ),
    ]