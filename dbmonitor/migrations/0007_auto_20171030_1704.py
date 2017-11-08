# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-30 09:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbmonitor', '0006_auto_20171030_1633'),
    ]

    operations = [
        migrations.AddField(
            model_name='mysql_monitor',
            name='db_pass',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='\u6570\u636e\u5e93\u5bc6\u7801'),
        ),
        migrations.AddField(
            model_name='mysql_monitor',
            name='db_user',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='\u6570\u636e\u5e93\u7528\u6237'),
        ),
        migrations.AlterField(
            model_name='mysql_monitor',
            name='db_ip',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='\u6570\u636e\u5e93ip'),
        ),
    ]