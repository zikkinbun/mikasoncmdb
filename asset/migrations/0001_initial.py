# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-07 12:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IDC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=32, verbose_name='\u673a\u623f\u540d\u79f0')),
                ('LinkName', models.CharField(max_length=32, verbose_name='\u8054\u7cfb\u4eba')),
                ('LinkPhone', models.CharField(max_length=32, verbose_name='\u8054\u7cfb\u7535\u8bdd')),
                ('Network', models.TextField(blank=True, default='', null=True, verbose_name='IP\u5730\u5740')),
                ('DateAdd', models.DateField(auto_now=True, null=True)),
                ('Comment', models.CharField(blank=True, default='', max_length=128, null=True, verbose_name='\u5907\u6ce8')),
            ],
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(blank=True, max_length=32, null=True, verbose_name='\u4e3b\u673a\u540d')),
                ('System', models.CharField(blank=True, max_length=128, null=True, verbose_name='\u7cfb\u7edf\u5e73\u53f0')),
                ('GlobalIpAddr', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u4e3b\u673a\u516c\u7f51IP')),
                ('PrivateIpAddr', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u4e3b\u673a\u79c1\u7f51IP')),
                ('CpuStat', models.CharField(choices=[('16Core', '16'), ('8Core', '8'), ('4Core', '4'), ('2Core', '2')], max_length=32, verbose_name='CPU')),
                ('MemoryStat', models.CharField(choices=[('32G', '32'), ('16G', '16'), ('8G', '8'), ('4G', '4')], max_length=32, verbose_name='\u5185\u5b58')),
                ('HDDStorage', models.CharField(blank=True, max_length=32, null=True, verbose_name='\u786c\u76d8')),
                ('NetCard', models.CharField(blank=True, max_length=32, null=True, verbose_name='\u7f51\u5361\u5e26\u5bbd')),
                ('Status', models.CharField(choices=[('Online', 'ON'), ('Offline', 'OFF')], max_length=20, verbose_name='\u662f\u5426\u6fc0\u6d3b')),
                ('CreateTime', models.DateTimeField(auto_now=True, null=True)),
                ('comment', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u5907\u6ce8')),
            ],
        ),
    ]
