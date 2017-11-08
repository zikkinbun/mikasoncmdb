# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-30 08:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbmonitor', '0005_auto_20171030_1419'),
    ]

    operations = [
        migrations.AddField(
            model_name='mysql_monitor',
            name='db_ip',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='mysql_monitor',
            name='db_port',
            field=models.IntegerField(default=3306),
        ),
    ]