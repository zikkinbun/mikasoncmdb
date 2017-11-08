# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-03 10:32
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Network_Monitor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('server_id', models.IntegerField(blank=True, null=True)),
                ('check_tcp', models.IntegerField(default=0)),
                ('check_ng', models.IntegerField(default=0)),
                ('check_tty', models.IntegerField(default=0)),
                ('check_netload', models.IntegerField(default=0)),
                ('check_proc', models.IntegerField(default=0)),
                ('create_time', models.DateTimeField(default=datetime.datetime(2017, 11, 3, 18, 32, 33, 553960, tzinfo=utc))),
            ],
        ),
        migrations.RenameField(
            model_name='online_user',
            old_name='count',
            new_name='pid',
        ),
        migrations.AddField(
            model_name='online_user',
            name='chn',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='online_user',
            name='uptime',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='online_user',
            name='user_name',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='network_load',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 3, 18, 32, 33, 559444, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='nginx_status',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 3, 18, 32, 33, 556904, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='online_user',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 3, 18, 32, 33, 557978, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='tcp_status',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 3, 18, 32, 33, 555602, tzinfo=utc)),
        ),
    ]