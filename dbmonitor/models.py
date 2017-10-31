# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.timezone import utc
from datetime import datetime
# Create your models here.

class Mysql_Monitor(models.Model):

    db_ip = models.CharField(max_length=32, blank=True, null=True, verbose_name='数据库ip')
    db_port = models.IntegerField(default=3306)
    db_user = models.CharField(max_length=32, blank=True, null=True, verbose_name='数据库用户')
    db_pass = models.CharField(max_length=255, blank=True, null=True, verbose_name='数据库密码')
    tag = models.CharField(max_length=32, blank=True, null=True)
    monitor = models.IntegerField(default=1)
    check_longsql = models.IntegerField(default=0)
    longsql_time = models.IntegerField(default=1200)
    longsql_autokill = models.IntegerField(default=0)
    check_active = models.IntegerField(default=0)
    active_threshold = models.IntegerField(default=30)
    check_connections = models.IntegerField(default=0)
    connection_threshold = models.IntegerField(default=1000)
    check_delay = models.IntegerField(default=0)
    delay_threshold = models.IntegerField(default=3600)
    check_slave = models.IntegerField(default=0)
    replchannel = models.CharField(max_length=32, blank=True, null=True)
    alarm_times = models.IntegerField(default=3)
    alarm_interval = models.IntegerField(default=60)
    mail_to = models.CharField(max_length=255, blank=True, null=True)

class Mysql_Processlist(models.Model):

    pid = models.IntegerField()
    db_ip = models.CharField(max_length=32, blank=True, null=True, verbose_name='数据库ip')
    db_port = models.IntegerField(default=3306)
    db_user = models.CharField(max_length=32, blank=True, null=True, verbose_name='数据库用户')
    db = models.CharField(max_length=32, blank=True, null=True, verbose_name='数据库')
    connected_host = models.CharField(max_length=32, blank=True, null=True, verbose_name='连接主机')
    command = models.CharField(max_length=32, blank=True, null=True, verbose_name='命令')
    state = models.CharField(max_length=32, blank=True, null=True, verbose_name='状态')
    info = models.CharField(max_length=32, blank=True, null=True, verbose_name='信息')
    create_time = models.DateTimeField(default=datetime.now().replace(tzinfo=utc))

class Mysql_Replication(models.Model):

    db_ip = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'数据库ip')
    db_port = models.IntegerField()
    is_master = models.IntegerField(default=0)
    is_slave = models.IntegerField(default=0)
    read_only = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'只读')
    gtid_mode = models.CharField(max_length=32, blank=True, null=True)
    master_server = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'主服务器')
    master_user = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'主服务用户')
    master_port = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'主服务器端口')
    slave_io_run = models.CharField(max_length=32,null=True)
    slave_sql_run = models.CharField(max_length=32,null=True)
    delay = models.CharField(max_length=32,null=True)
    current_binlog_file = models.CharField(max_length=32,null=True)
    current_binlog_pos = models.CharField(max_length=32,null=True)
    master_binlog_file = models.CharField(max_length=32,null=True)
    master_binlog_pos = models.CharField(max_length=32,null=True)
    master_binlog_space = models.IntegerField(default=0)
    slave_sql_running_state = models.CharField(max_length=100,null=True)
    create_time = models.DateTimeField(default=datetime.now().replace(tzinfo=utc))

class Mysql_Connection(models.Model):

    db_ip = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'数据库ip')
    db_port = models.IntegerField()
    connect_count = models.CharField(max_length=32, null=True, verbose_name=u'连接总数')
    thead_connect = models.CharField(max_length=32, null=True, verbose_name=u'当前连接数')
    max_connect = models.CharField(max_length=32, null=True, verbose_name=u'最大连接数')
    create_time = models.DateTimeField(default=datetime.now().replace(tzinfo=utc))

class Mysql_Status(models.Model):
    db_ip = models.CharField(max_length=32, blank=True, null=True)
    db_port = models.CharField(max_length=32, blank=True, null=True)
    connect = models.CharField(max_length=32, blank=True, null=True)
    role = models.CharField(max_length=32, blank=True, null=True)
    uptime = models.CharField(max_length=32, blank=True, null=True)

    connections = models.CharField(max_length=32, blank=True, null=True)
    aborted_clients = models.CharField(max_length=32, blank=True, null=True)
    aborted_connects = models.CharField(max_length=32, blank=True, null=True)

    max_used_connections = models.CharField(max_length=32, blank=True, null=True)
    open_files = models.CharField(max_length=32, blank=True, null=True)
    open_table_definitions = models.CharField(max_length=32, blank=True, null=True)
    open_tables = models.CharField(max_length=32, blank=True, null=True)
    opened_files = models.CharField(max_length=32, blank=True, null=True)
    opened_tables = models.CharField(max_length=32, blank=True, null=True)
    opened_table_definitions = models.CharField(max_length=32, blank=True, null=True)

    threads_connected = models.CharField(max_length=32, blank=True, null=True)
    threads_running = models.CharField(max_length=32, blank=True, null=True)
    threads_created = models.CharField(max_length=32, blank=True, null=True)
    threads_cached = models.CharField(max_length=32, blank=True, null=True)

    connections_persecond = models.CharField(max_length=32, blank=True, null=True)
    bytes_received = models.CharField(max_length=32, blank=True, null=True)
    bytes_received_persecond = models.CharField(max_length=32, blank=True, null=True)
    bytes_sent = models.CharField(max_length=32, blank=True, null=True)
    bytes_sent_persecond = models.CharField(max_length=32, blank=True, null=True)

    com_select = models.CharField(max_length=32, blank=True, null=True)
    com_select_persecond = models.CharField(max_length=32, blank=True, null=True)
    com_insert = models.CharField(max_length=32, blank=True, null=True)
    com_insert_persecond = models.CharField(max_length=32, blank=True, null=True)
    com_update = models.CharField(max_length=32, blank=True, null=True)
    com_update_persecond = models.CharField(max_length=32, blank=True, null=True)
    com_delete = models.CharField(max_length=32, blank=True, null=True)
    com_delete_persecond = models.CharField(max_length=32, blank=True, null=True)
    com_commit = models.CharField(max_length=32, blank=True, null=True)
    com_commit_persecond = models.CharField(max_length=32, blank=True, null=True)
    com_rollback = models.CharField(max_length=32, blank=True, null=True)
    com_rollback_persecond = models.CharField(max_length=32, blank=True, null=True)

    questions = models.CharField(max_length=32, blank=True, null=True)
    questions_persecond = models.CharField(max_length=32, blank=True, null=True)
    queries = models.CharField(max_length=32, blank=True, null=True)
    queries_persecond = models.CharField(max_length=32, blank=True, null=True)

    table_locks_immediate_persecond = models.CharField(max_length=32, blank=True, null=True)
    table_locks_waited_persecond = models.CharField(max_length=32, blank=True, null=True)

    key_blocks_not_flushed = models.CharField(max_length=32, blank=True, null=True)
    key_blocks_unused = models.CharField(max_length=32, blank=True, null=True)
    key_blocks_used = models.CharField(max_length=32, blank=True, null=True)
    key_read_requests_persecond = models.CharField(max_length=32, blank=True, null=True)
    key_read_requests = models.CharField(max_length=32, blank=True, null=True)
    key_reads = models.CharField(max_length=32, blank=True, null=True)
    key_write_requests_persecond = models.CharField(max_length=32, blank=True, null=True)
    key_write_requests = models.CharField(max_length=32, blank=True, null=True)
    key_writes = models.CharField(max_length=32, blank=True, null=True)

    innodb_doublewrite = models.CharField(max_length=32)
    innodb_buffer_pool_bytes_data = models.CharField(max_length=32, blank=True, null=True)
    innodb_buffer_pool_bytes_dirty = models.CharField(max_length=32, blank=True, null=True)
    innodb_buffer_pool_pages_total = models.CharField(max_length=32, blank=True, null=True)
    innodb_buffer_pool_pages_data = models.CharField(max_length=32, blank=True, null=True)
    innodb_buffer_pool_pages_dirty = models.CharField(max_length=32, blank=True, null=True)
    innodb_buffer_pool_pages_flushed = models.CharField(max_length=32, blank=True, null=True)
    innodb_buffer_pool_pages_free = models.CharField(max_length=32, blank=True, null=True)
    innodb_buffer_pool_pages_misc = models.CharField(max_length=32, blank=True, null=True)
    innodb_page_size = models.CharField(max_length=32, blank=True, null=True)
    innodb_pages_created = models.CharField(max_length=32, blank=True, null=True)
    innodb_pages_read = models.CharField(max_length=32, blank=True, null=True)
    innodb_pages_written = models.CharField(max_length=32, blank=True, null=True)
    innodb_row_lock_current_waits = models.CharField(max_length=128)
    innodb_rows_read = models.CharField(max_length=32, blank=True, null=True)
    innodb_rows_inserted = models.CharField(max_length=32, blank=True, null=True)
    innodb_rows_updated = models.CharField(max_length=32, blank=True, null=True)
    innodb_rows_deleted = models.CharField(max_length=32, blank=True, null=True)
    innodb_data_read = models.CharField(max_length=32, blank=True, null=True)
    innodb_data_reads = models.CharField(max_length=32, blank=True, null=True)
    innodb_data_writes = models.CharField(max_length=32, blank=True, null=True)
    innodb_data_written = models.CharField(max_length=32, blank=True, null=True)
    innodb_data_fsyncs = models.CharField(max_length=32, blank=True, null=True)

    qcache_free_blocks = models.CharField(max_length=32, blank=True, null=True)
    qcache_free_memory = models.CharField(max_length=32, blank=True, null=True)

    select_full_join = models.CharField(max_length=32, blank=True, null=True)
    select_full_range_join = models.CharField(max_length=32, blank=True, null=True)
    select_scan = models.CharField(max_length=32, blank=True, null=True)

    sort_scan = models.CharField(max_length=32, blank=True, null=True)
    sort_rows = models.CharField(max_length=32, blank=True, null=True)

    table_locks_immediate = models.CharField(max_length=32, blank=True, null=True)
    table_locks_waited = models.CharField(max_length=32, blank=True, null=True)
    table_open_cache_hits = models.CharField(max_length=32, blank=True, null=True)
    table_open_cache_misses = models.CharField(max_length=32, blank=True, null=True)
    table_open_cache_overflows = models.CharField(max_length=32, blank=True, null=True)

    create_time = models.DateTimeField(default=datetime.now().replace(tzinfo=utc))
