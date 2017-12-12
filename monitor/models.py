# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.timezone import utc
from datetime import datetime
# Create your models here.


class MonitorCpuLoad(models.Model):
    serverId = models.IntegerField()
    avg1 = models.BigIntegerField()
    avg5 = models.BigIntegerField()
    avg15 = models.BigIntegerField()
    createdate = models.DateTimeField(default=datetime.now().replace(tzinfo=utc))

    class Meta:
        managed = False
        db_table = 'monitor_cpu_load'


class MonitorFunction(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True)
    createdate = models.DateTimeField(default=datetime.now().replace(tzinfo=utc))

    class Meta:
        managed = False
        db_table = 'monitor_function'


class MonitorHddStat(models.Model):
    serverId = models.IntegerField(blank=True, null=True)
    disk = models.CharField(max_length=255, blank=True, null=True)
    total = models.BigIntegerField(blank=True, null=True)
    used = models.BigIntegerField(blank=True, null=True)
    free = models.BigIntegerField(blank=True, null=True)
    percent = models.CharField(max_length=255, blank=True, null=True)
    createdate = models.DateTimeField(default=datetime.now().replace(tzinfo=utc))

    class Meta:
        managed = False
        db_table = 'monitor_hdd_stat'


class MonitorMemStat(models.Model):
    serverId = models.IntegerField()
    available = models.BigIntegerField()
    total = models.BigIntegerField()
    createdate = models.DateTimeField(default=datetime.now().replace(tzinfo=utc))

    class Meta:
        managed = False
        db_table = 'monitor_mem_stat'


class MonitorMysqlConnection(models.Model):
    serverId = models.IntegerField()
    port = models.IntegerField()
    connect_count = models.CharField(max_length=32, blank=True, null=True)
    max_connect = models.CharField(max_length=32, blank=True, null=True)
    thead_connect = models.CharField(max_length=32, blank=True, null=True)
    createdate = models.DateTimeField(default=datetime.now().replace(tzinfo=utc))

    class Meta:
        managed = False
        db_table = 'monitor_mysql_connection'


class MonitorMysqlProcesslist(models.Model):
    serverId = models.IntegerField(blank=True, null=True)
    port = models.IntegerField(blank=True, null=True)
    pid = models.IntegerField(blank=True, null=True)
    db = models.CharField(max_length=255, blank=True, null=True)
    command = models.CharField(max_length=255, blank=True, null=True)
    info = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    createdate = models.DateTimeField(default=datetime.now().replace(tzinfo=utc))

    class Meta:
        managed = False
        db_table = 'monitor_mysql_processlist'


class MonitorMysqlReplication(models.Model):
    serverId = models.IntegerField(blank=True, null=True)
    port = models.IntegerField()
    is_master = models.IntegerField()
    is_slave = models.IntegerField()
    read_only = models.CharField(max_length=32, blank=True, null=True)
    gtid_mode = models.CharField(max_length=32, blank=True, null=True)
    master_server = models.CharField(max_length=32, blank=True, null=True)
    master_user = models.CharField(max_length=32, blank=True, null=True)
    master_port = models.CharField(max_length=32, blank=True, null=True)
    slave_io_run = models.CharField(max_length=32, blank=True, null=True)
    slave_sql_run = models.CharField(max_length=32, blank=True, null=True)
    delay = models.CharField(max_length=32, blank=True, null=True)
    current_binlog_file = models.CharField(max_length=32, blank=True, null=True)
    current_binlog_pos = models.CharField(max_length=32, blank=True, null=True)
    master_binlog_file = models.CharField(max_length=32, blank=True, null=True)
    master_binlog_pos = models.CharField(max_length=32, blank=True, null=True)
    master_binlog_space = models.IntegerField()
    slave_sql_running_state = models.CharField(max_length=100, blank=True, null=True)
    createdate = models.DateTimeField(default=datetime.now().replace(tzinfo=utc))

    class Meta:
        managed = False
        db_table = 'monitor_mysql_replication'


class MonitorMysqlStatus(models.Model):
    serverId = models.IntegerField(blank=True, null=True)
    db_port = models.CharField(max_length=32, blank=True, null=True)
    connect = models.CharField(max_length=32, blank=True, null=True)
    role = models.CharField(max_length=32, blank=True, null=True)
    uptime = models.CharField(max_length=32, blank=True, null=True)
    open_table_definitions = models.CharField(max_length=32, blank=True, null=True)
    max_used_connections = models.CharField(max_length=32, blank=True, null=True)
    opened_tables = models.CharField(max_length=32, blank=True, null=True)
    open_files = models.CharField(max_length=32, blank=True, null=True)
    qcache_free_memory = models.CharField(max_length=32, blank=True, null=True)
    open_tables = models.CharField(max_length=32, blank=True, null=True)
    opened_table_definitions = models.CharField(max_length=32, blank=True, null=True)
    opened_files = models.CharField(max_length=32, blank=True, null=True)
    key_writes = models.CharField(max_length=32, blank=True, null=True)
    threads_connected = models.CharField(max_length=32, blank=True, null=True)
    threads_running = models.CharField(max_length=32, blank=True, null=True)
    threads_created = models.CharField(max_length=32, blank=True, null=True)
    threads_cached = models.CharField(max_length=32, blank=True, null=True)
    connections = models.CharField(max_length=32, blank=True, null=True)
    aborted_clients = models.CharField(max_length=32, blank=True, null=True)
    aborted_connects = models.CharField(max_length=32, blank=True, null=True)
    connections_persecond = models.CharField(max_length=32, blank=True, null=True)
    bytes_received_persecond = models.CharField(max_length=32, blank=True, null=True)
    bytes_sent_persecond = models.CharField(max_length=32, blank=True, null=True)
    com_select_persecond = models.CharField(max_length=32, blank=True, null=True)
    com_insert_persecond = models.CharField(max_length=32, blank=True, null=True)
    com_update_persecond = models.CharField(max_length=32, blank=True, null=True)
    com_delete_persecond = models.CharField(max_length=32, blank=True, null=True)
    com_commit_persecond = models.CharField(max_length=32, blank=True, null=True)
    com_rollback_persecond = models.CharField(max_length=32, blank=True, null=True)
    questions_persecond = models.CharField(max_length=32, blank=True, null=True)
    queries_persecond = models.CharField(max_length=32, blank=True, null=True)
    queries = models.CharField(max_length=32, blank=True, null=True)
    com_commit = models.CharField(max_length=32, blank=True, null=True)
    bytes_received = models.CharField(max_length=32, blank=True, null=True)
    bytes_sent = models.CharField(max_length=32, blank=True, null=True)
    table_locks_immediate_persecond = models.CharField(max_length=32, blank=True, null=True)
    table_locks_waited_persecond = models.CharField(max_length=32, blank=True, null=True)
    key_read_requests = models.CharField(max_length=32, blank=True, null=True)
    qcache_free_blocks = models.CharField(max_length=32, blank=True, null=True)
    innodb_rows_updated = models.CharField(max_length=32, blank=True, null=True)
    key_blocks_not_flushed = models.CharField(max_length=32, blank=True, null=True)
    key_blocks_unused = models.CharField(max_length=32, blank=True, null=True)
    key_blocks_used = models.CharField(max_length=32, blank=True, null=True)
    key_read_requests_persecond = models.CharField(max_length=32, blank=True, null=True)
    key_reads = models.CharField(max_length=32, blank=True, null=True)
    key_write_requests_persecond = models.CharField(max_length=32, blank=True, null=True)
    key_write_requests = models.CharField(max_length=32, blank=True, null=True)
    com_delete = models.CharField(max_length=32, blank=True, null=True)
    com_update = models.CharField(max_length=32, blank=True, null=True)
    innodb_doublewrite = models.CharField(max_length=32, blank=True, null=True)
    innodb_buffer_pool_bytes_dirty = models.CharField(max_length=32, blank=True, null=True)
    innodb_data_fsyncs = models.CharField(max_length=32, blank=True, null=True)
    innodb_data_read = models.CharField(max_length=32, blank=True, null=True)
    innodb_data_reads = models.CharField(max_length=32, blank=True, null=True)
    innodb_rows_read = models.CharField(max_length=32, blank=True, null=True)
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
    innodb_row_lock_current_waits = models.CharField(max_length=128, blank=True, null=True)
    com_insert = models.CharField(max_length=32, blank=True, null=True)
    com_rollback = models.CharField(max_length=32, blank=True, null=True)
    com_select = models.CharField(max_length=32, blank=True, null=True)
    innodb_buffer_pool_bytes_data = models.CharField(max_length=32, blank=True, null=True)
    innodb_rows_deleted = models.CharField(max_length=32, blank=True, null=True)
    innodb_data_written = models.CharField(max_length=32, blank=True, null=True)
    innodb_rows_inserted = models.CharField(max_length=32, blank=True, null=True)
    innodb_data_writes = models.CharField(max_length=32, blank=True, null=True)
    questions = models.CharField(max_length=32, blank=True, null=True)
    select_full_join = models.CharField(max_length=32, blank=True, null=True)
    select_full_range_join = models.CharField(max_length=32, blank=True, null=True)
    select_scan = models.CharField(max_length=32, blank=True, null=True)
    sort_rows = models.CharField(max_length=32, blank=True, null=True)
    sort_scan = models.CharField(max_length=32, blank=True, null=True)
    table_locks_immediate = models.CharField(max_length=32, blank=True, null=True)
    table_locks_waited = models.CharField(max_length=32, blank=True, null=True)
    table_open_cache_hits = models.CharField(max_length=32, blank=True, null=True)
    table_open_cache_misses = models.CharField(max_length=32, blank=True, null=True)
    table_open_cache_overflows = models.CharField(max_length=32, blank=True, null=True)
    createdate = models.DateTimeField(default=datetime.now().replace(tzinfo=utc))

    class Meta:
        managed = False
        db_table = 'monitor_mysql_status'


class MonitorNetworkLoad(models.Model):
    serverId = models.IntegerField(blank=True, null=True)
    private_incoming = models.FloatField(blank=True, null=True)
    private_outgoing = models.FloatField(blank=True, null=True)
    global_incoming = models.FloatField(blank=True, null=True)
    global_outgoing = models.FloatField(blank=True, null=True)
    createdate = models.DateTimeField(default=datetime.now().replace(tzinfo=utc))

    class Meta:
        managed = False
        db_table = 'monitor_network_load'


class MonitorNginxStatus(models.Model):
    serverId = models.IntegerField(blank=True, null=True)
    active = models.IntegerField(blank=True, null=True)
    reading = models.IntegerField(blank=True, null=True)
    writing = models.IntegerField(blank=True, null=True)
    waiting = models.IntegerField(blank=True, null=True)
    createdate = models.DateTimeField(default=datetime.now().replace(tzinfo=utc))

    class Meta:
        managed = False
        db_table = 'monitor_nginx_status'


class MonitorOnlineUser(models.Model):
    serverId = models.IntegerField(blank=True, null=True)
    username = models.CharField(max_length=32, blank=True, null=True)
    pid = models.IntegerField(blank=True, null=True)
    ip = models.CharField(max_length=32, blank=True, null=True)
    chn = models.CharField(max_length=32, blank=True, null=True)
    uptime = models.DateTimeField(blank=True, null=True)
    createdate = models.DateTimeField(default=datetime.now().replace(tzinfo=utc))

    class Meta:
        managed = False
        db_table = 'monitor_online_user'


class MonitorTcpStatus(models.Model):
    serverId = models.IntegerField(blank=True, null=True)
    listen = models.IntegerField(blank=True, null=True)
    established = models.IntegerField(blank=True, null=True)
    time_wait = models.IntegerField(blank=True, null=True)
    close_wait = models.IntegerField(blank=True, null=True)
    closed = models.IntegerField(blank=True, null=True)
    syn_sent = models.IntegerField(blank=True, null=True)
    syn_received = models.IntegerField(blank=True, null=True)
    last_ack = models.IntegerField(blank=True, null=True)
    createdate = models.DateTimeField(default=datetime.now().replace(tzinfo=utc))

    class Meta:
        managed = False
        db_table = 'monitor_tcp_status'


class MonitorMysqlUser(models.Model):
    serverId = models.IntegerField(blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    tag = models.CharField(max_length=32, blank=True, null=True)
    createdate = models.DateTimeField(default=datetime.now().replace(tzinfo=utc))

    class Meta:
        managed = False
        db_table = 'monitor_mysql_user'


class MonitorMysqlSlowQueryHis(models.Model):
    serverId = models.IntegerField(blank=True, null=True)
    hostname_max = models.CharField(max_length=64, blank=True, null=True)
    db_max = models.CharField(max_length=64, blank=True, null=True),
    checksum = models.BigIntegerField(20)
    sample = models.CharField(max_length=64, blank=True, null=True)
    ts_min = models.DateTimeField()
    ts_max = models.DateTimeField()
    ts_cnt = models.FloatField()
    Query_time_sum = models.FloatField()
    Query_time_min = models.FloatField()
    Query_time_max = models.FloatField()
    Query_time_pct_95 = models.FloatField()
    Query_time_stddev = models.FloatField()
    Query_time_median = models.FloatField()
    Lock_time_sum = models.FloatField()
    Lock_time_min = models.FloatField()
    Lock_time_max = models.FloatField()
    Lock_time_pct_95 = models.FloatField()
    Lock_time_stddev = models.FloatField()
    Lock_time_median = models.FloatField()
    Rows_sent_sum = models.FloatField()
    Rows_sent_min = models.FloatField()
    Rows_sent_max = models.FloatField()
    Rows_sent_pct_95 = models.FloatField()
    Rows_sent_stddev = models.FloatField()
    Rows_sent_median = models.FloatField()
    Rows_examined_sum = models.FloatField()
    Rows_examined_min = models.FloatField()
    Rows_examined_max = models.FloatField()
    Rows_examined_pct_95 = models.FloatField()
    Rows_examined_stddev = models.FloatField()
    Rows_examined_median = models.FloatField()
    Rows_affected_sum = models.FloatField()
    Rows_affected_min = models.FloatField()
    Rows_affected_max = models.FloatField()
    Rows_affected_pct_95 = models.FloatField()
    Rows_affected_stddev = models.FloatField()
    Rows_affected_median = models.FloatField()
    Rows_read_sum = models.FloatField()
    Rows_read_min = models.FloatField()
    Rows_read_max = models.FloatField()
    Rows_read_pct_95 = models.FloatField()
    Rows_read_stddev = models.FloatField()
    Rows_read_median = models.FloatField()
    Merge_passes_sum = models.FloatField()
    Merge_passes_min = models.FloatField()
    Merge_passes_max = models.FloatField()
    Merge_passes_pct_95 = models.FloatField()
    Merge_passes_stddev = models.FloatField()
    Merge_passes_median = models.FloatField()
    InnoDB_IO_r_ops_min = models.FloatField()
    InnoDB_IO_r_ops_max = models.FloatField()
    InnoDB_IO_r_ops_pct_95 = models.FloatField()
    InnoDB_IO_r_bytes_pct_95 = models.FloatField()
    InnoDB_IO_r_bytes_stddev = models.FloatField()
    InnoDB_IO_r_bytes_median = models.FloatField()
    InnoDB_IO_r_wait_min = models.FloatField()
    InnoDB_IO_r_wait_max = models.FloatField()
    InnoDB_IO_r_wait_pct_95 = models.FloatField()
    InnoDB_IO_r_ops_stddev = models.FloatField()
    InnoDB_IO_r_ops_median = models.FloatField()
    InnoDB_IO_r_bytes_min = models.FloatField()
    InnoDB_IO_r_bytes_max = models.FloatField()
    InnoDB_IO_r_wait_stddev = models.FloatField()
    InnoDB_IO_r_wait_median = models.FloatField()
    InnoDB_rec_lock_wait_min = models.FloatField()
    InnoDB_rec_lock_wait_max = models.FloatField()
    InnoDB_rec_lock_wait_pct_95 = models.FloatField()
    InnoDB_rec_lock_wait_stddev = models.FloatField()
    InnoDB_rec_lock_wait_median = models.FloatField()
    InnoDB_queue_wait_min = models.FloatField()
    InnoDB_queue_wait_max = models.FloatField()
    InnoDB_queue_wait_pct_95 = models.FloatField()
    InnoDB_queue_wait_stddev = models.FloatField()
    InnoDB_queue_wait_median = models.FloatField()
    InnoDB_pages_distinct_min = models.FloatField()
    InnoDB_pages_distinct_max = models.FloatField()
    InnoDB_pages_distinct_pct_95 = models.FloatField()
    InnoDB_pages_distinct_stddev = models.FloatField()
    InnoDB_pages_distinct_median = models.FloatField()
    QC_Hit_cnt = models.FloatField()
    QC_Hit_sum = models.FloatField()
    Full_scan_cnt = models.FloatField()
    Full_scan_sum = models.FloatField()
    Full_join_cnt = models.FloatField()
    Full_join_sum = models.FloatField()
    Tmp_table_cnt = models.FloatField()
    Tmp_table_sum = models.FloatField()
    Filesort_cnt = models.FloatField()
    Filesort_sum = models.FloatField()
    Tmp_table_on_disk_cnt = models.FloatField()
    Tmp_table_on_disk_sum = models.FloatField()
    Filesort_on_disk_cnt = models.FloatField()
    Filesort_on_disk_sum = models.FloatField()
    Bytes_sum = models.FloatField()
    Bytes_min = models.FloatField()
    Bytes_max = models.FloatField()
    Bytes_pct_95 = models.FloatField()
    Bytes_stddev = models.FloatField()
    Bytes_median = models.FloatField()

    class Meta:
        managed = False
        db_table = 'monitor_mysql_slow_query_his'
