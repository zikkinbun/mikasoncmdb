# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-31 06:59
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dbmonitor', '0009_auto_20171031_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mysql_connection',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 31, 14, 59, 8, 362927, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='mysql_replication',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 31, 14, 59, 8, 360746, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='mysql_status',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 31, 14, 59, 8, 372646, tzinfo=utc)),
        ),
    ]