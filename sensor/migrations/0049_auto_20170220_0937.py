# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-20 08:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0048_auto_20170219_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rawdata',
            name='status',
            field=models.IntegerField(choices=[(0, b'Valid'), (5, b'Sensor offline')], default=0),
        ),
    ]
