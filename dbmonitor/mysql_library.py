# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils import timezone
from .models import Mysql_Status, Mysql_Replication, Mysql_Connection, Mysql_Monitor

def status_update_or_create(dataset, ip, port):
    record = Mysql_Status.objects.filter(db_ip=ip)
    if record:
        record.update(db_ip=ip, db_port=port, connect='', role='', uptime=dataset['Uptime'], connections=dataset['Connections'], \
            aborted_clients=dataset['Aborted_clients'], aborted_connects=dataset['Aborted_connects'], max_used_connections=dataset['Max_used_connections'], \
            open_files=dataset['Open_files'], open_table_definitions=dataset['Open_table_definitions'], open_tables=dataset['Open_tables'], opened_files=dataset['Opened_files'], \
            opened_tables=dataset['Opened_tables'], opened_table_definitions=dataset['Opened_table_definitions'], threads_connected=dataset['Threads_connected'], \
            threads_running=dataset['Threads_running'], threads_created=dataset['Threads_created'], threads_cached=dataset['Threads_cached'], bytes_received=dataset['Bytes_received'], \
            bytes_sent=dataset['Bytes_sent'], com_select=dataset['Com_select'], com_insert=dataset['Com_insert'], com_update=dataset['Com_update'], com_delete=dataset['Com_delete'], com_commit=dataset['Com_commit'], com_rollback=dataset['Com_rollback'], questions=dataset['Questions'], \
            queries=dataset['Queries'], key_blocks_not_flushed=dataset['Key_blocks_not_flushed'], \
            key_blocks_unused=dataset['Key_blocks_unused'], key_blocks_used=dataset['Key_blocks_used'], key_read_requests=dataset['Key_read_requests'], key_reads=dataset['Key_reads'], key_write_requests=dataset['Key_write_requests'], \
            key_writes=dataset['Key_writes'], innodb_doublewrite=dataset['Innodb_dblwr_writes'], innodb_buffer_pool_bytes_data=dataset['Innodb_buffer_pool_bytes_data'], innodb_buffer_pool_bytes_dirty=dataset['Innodb_buffer_pool_bytes_dirty'], \
            innodb_buffer_pool_pages_total=dataset['Innodb_buffer_pool_pages_total'], innodb_buffer_pool_pages_data=dataset['Innodb_buffer_pool_pages_data'], innodb_buffer_pool_pages_dirty=dataset['Innodb_buffer_pool_pages_dirty'], innodb_buffer_pool_pages_flushed=dataset['Innodb_buffer_pool_pages_flushed'], \
            innodb_buffer_pool_pages_free=dataset['Innodb_buffer_pool_pages_free'], innodb_buffer_pool_pages_misc=dataset['Innodb_buffer_pool_pages_misc'], innodb_page_size=dataset['Innodb_page_size'], innodb_pages_created=dataset['Innodb_pages_created'], innodb_pages_read=dataset['Innodb_pages_read'], \
            innodb_pages_written=dataset['Innodb_pages_written'], innodb_row_lock_current_waits=dataset['Innodb_row_lock_current_waits'], innodb_rows_read=dataset['Innodb_rows_read'], innodb_rows_inserted=dataset['Innodb_rows_inserted'], innodb_rows_updated=dataset['Innodb_rows_updated'], \
            innodb_rows_deleted=dataset['Innodb_rows_deleted'], innodb_data_read=dataset['Innodb_data_read'], innodb_data_reads=dataset['Innodb_data_reads'], innodb_data_writes=dataset['Innodb_data_writes'], innodb_data_written=dataset['Innodb_data_written'], innodb_data_fsyncs=dataset['Innodb_data_fsyncs'],\
            qcache_free_blocks=dataset['Qcache_free_blocks'], qcache_free_memory=dataset['Qcache_free_memory'], select_full_join=dataset['Select_full_join'], select_full_range_join=dataset['Select_full_range_join'], select_scan=dataset['Select_scan'], sort_scan=dataset['Sort_scan'], sort_rows=dataset['Sort_rows'], \
            table_locks_immediate=dataset['Table_locks_immediate'], table_locks_waited=dataset['Table_locks_waited'], table_open_cache_hits=dataset['Table_open_cache_hits'], table_open_cache_misses=dataset['Table_open_cache_misses'], table_open_cache_overflows=dataset['Table_open_cache_overflows'])
    else:
        Mysql_Status.objects.create(db_ip=ip, db_port=port, connect='', role='', uptime=dataset[u'Uptime'], connections=dataset[u'Connections'], \
            aborted_clients=dataset[u'Aborted_clients'], aborted_connects=dataset[u'Aborted_connects'], max_used_connections=dataset[u'Max_used_connections'], \
            open_files=dataset['Open_files'], open_table_definitions =dataset['Open_table_definitions'], open_tables=dataset['Open_tables'], opened_files=dataset['Opened_files'], \
            opened_tables=dataset['Opened_tables'], opened_table_definitions =dataset['Opened_table_definitions'], threads_connected=dataset['Threads_connected'], \
            threads_running=dataset['Threads_running'], threads_created =dataset['Threads_created'], threads_cached=dataset['Threads_cached'], bytes_received=dataset['Bytes_received'], \
            bytes_sent=dataset['Bytes_sent'], com_select =dataset['Com_select'], com_insert=dataset['Com_insert'], com_update=dataset['Com_update'], com_delete=dataset['Com_delete'], com_commit=dataset['Com_commit'], com_rollback=dataset['Com_rollback'], questions=dataset['Questions'], \
            queries=dataset['Queries'], key_blocks_not_flushed=dataset['Key_blocks_not_flushed'], \
            key_blocks_unused=dataset['Key_blocks_unused'], key_blocks_used =dataset['Key_blocks_used'], key_read_requests=dataset['Key_read_requests'], key_reads=dataset['Key_reads'], key_write_requests=dataset['Key_write_requests'], \
            key_writes=dataset['Key_writes'], innodb_doublewrite =dataset['Innodb_dblwr_writes'], innodb_buffer_pool_bytes_data=dataset['Innodb_buffer_pool_bytes_data'], innodb_buffer_pool_bytes_dirty=dataset['Innodb_buffer_pool_bytes_dirty'], \
            innodb_buffer_pool_pages_total=dataset['Innodb_buffer_pool_pages_total'], innodb_buffer_pool_pages_data=dataset['Innodb_buffer_pool_pages_data'], innodb_buffer_pool_pages_dirty=dataset['Innodb_buffer_pool_pages_dirty'], innodb_buffer_pool_pages_flushed=dataset['Innodb_buffer_pool_pages_flushed'], \
            innodb_buffer_pool_pages_free=dataset['Innodb_buffer_pool_pages_free'], innodb_buffer_pool_pages_misc=dataset['Innodb_buffer_pool_pages_misc'], innodb_page_size=dataset['Innodb_page_size'], innodb_pages_created =dataset['Innodb_pages_created'], innodb_pages_read=dataset['Innodb_pages_read'], \
            innodb_pages_written=dataset['Innodb_pages_written'], innodb_row_lock_current_waits=dataset['Innodb_row_lock_current_waits'], innodb_rows_read=dataset['Innodb_rows_read'], innodb_rows_inserted=dataset['Innodb_rows_inserted'], innodb_rows_updated=dataset['Innodb_rows_updated'], \
            innodb_rows_deleted=dataset['Innodb_rows_deleted'], innodb_data_read=dataset['Innodb_data_read'], innodb_data_reads=dataset['Innodb_data_reads'], innodb_data_writes=dataset['Innodb_data_writes'], innodb_data_written=dataset['Innodb_data_written'], innodb_data_fsyncs=dataset['Innodb_data_fsyncs'],\
            qcache_free_blocks=dataset['Qcache_free_blocks'], qcache_free_memory=dataset['Qcache_free_memory'], select_full_join=dataset['Select_full_join'], select_full_range_join=dataset['Select_full_range_join'], select_scan=dataset['Select_scan'], sort_scan=dataset['Sort_scan'], sort_rows=dataset['Sort_rows'], \
            table_locks_immediate=dataset['Table_locks_immediate'], table_locks_waited=dataset['Table_locks_waited'], table_open_cache_hits=dataset['Table_open_cache_hits'], table_open_cache_misses=dataset['Table_open_cache_misses'], table_open_cache_overflows=dataset['Table_open_cache_overflows'])

def status_create(dataset, ip, port):
    try:
        Mysql_Status.objects.create(db_ip=ip, db_port=port, connect='', role='', uptime=dataset[u'Uptime'], connections=dataset[u'Connections'], \
            aborted_clients=dataset[u'Aborted_clients'], aborted_connects=dataset[u'Aborted_connects'], max_used_connections=dataset[u'Max_used_connections'], \
            open_files=dataset['Open_files'], open_table_definitions =dataset['Open_table_definitions'], open_tables=dataset['Open_tables'], opened_files=dataset['Opened_files'], \
            opened_tables=dataset['Opened_tables'], opened_table_definitions =dataset['Opened_table_definitions'], threads_connected=dataset['Threads_connected'], \
            threads_running=dataset['Threads_running'], threads_created =dataset['Threads_created'], threads_cached=dataset['Threads_cached'], bytes_received=dataset['Bytes_received'], \
            bytes_sent=dataset['Bytes_sent'], com_select =dataset['Com_select'], com_insert=dataset['Com_insert'], com_update=dataset['Com_update'], com_delete=dataset['Com_delete'], com_commit=dataset['Com_commit'], com_rollback=dataset['Com_rollback'], questions=dataset['Questions'], \
            queries=dataset['Queries'], key_blocks_not_flushed=dataset['Key_blocks_not_flushed'], \
            key_blocks_unused=dataset['Key_blocks_unused'], key_blocks_used =dataset['Key_blocks_used'], key_read_requests=dataset['Key_read_requests'], key_reads=dataset['Key_reads'], key_write_requests=dataset['Key_write_requests'], \
            key_writes=dataset['Key_writes'], innodb_doublewrite =dataset['Innodb_dblwr_writes'], innodb_buffer_pool_bytes_data=dataset['Innodb_buffer_pool_bytes_data'], innodb_buffer_pool_bytes_dirty=dataset['Innodb_buffer_pool_bytes_dirty'], \
            innodb_buffer_pool_pages_total=dataset['Innodb_buffer_pool_pages_total'], innodb_buffer_pool_pages_data=dataset['Innodb_buffer_pool_pages_data'], innodb_buffer_pool_pages_dirty=dataset['Innodb_buffer_pool_pages_dirty'], innodb_buffer_pool_pages_flushed=dataset['Innodb_buffer_pool_pages_flushed'], \
            innodb_buffer_pool_pages_free=dataset['Innodb_buffer_pool_pages_free'], innodb_buffer_pool_pages_misc=dataset['Innodb_buffer_pool_pages_misc'], innodb_page_size=dataset['Innodb_page_size'], innodb_pages_created =dataset['Innodb_pages_created'], innodb_pages_read=dataset['Innodb_pages_read'], \
            innodb_pages_written=dataset['Innodb_pages_written'], innodb_row_lock_current_waits=dataset['Innodb_row_lock_current_waits'], innodb_rows_read=dataset['Innodb_rows_read'], innodb_rows_inserted=dataset['Innodb_rows_inserted'], innodb_rows_updated=dataset['Innodb_rows_updated'], \
            innodb_rows_deleted=dataset['Innodb_rows_deleted'], innodb_data_read=dataset['Innodb_data_read'], innodb_data_reads=dataset['Innodb_data_reads'], innodb_data_writes=dataset['Innodb_data_writes'], innodb_data_written=dataset['Innodb_data_written'], innodb_data_fsyncs=dataset['Innodb_data_fsyncs'],\
            qcache_free_blocks=dataset['Qcache_free_blocks'], qcache_free_memory=dataset['Qcache_free_memory'], select_full_join=dataset['Select_full_join'], select_full_range_join=dataset['Select_full_range_join'], select_scan=dataset['Select_scan'], sort_scan=dataset['Sort_scan'], sort_rows=dataset['Sort_rows'], \
            table_locks_immediate=dataset['Table_locks_immediate'], table_locks_waited=dataset['Table_locks_waited'], table_open_cache_hits=dataset['Table_open_cache_hits'], table_open_cache_misses=dataset['Table_open_cache_misses'], table_open_cache_overflows=dataset['Table_open_cache_overflows'])
    except Exception as e:
        print e

def status_querySet(datas):
    dataset = {}

    for data in datas:
        if data['Variable_name'] == 'Connections':
            # print int(data[u'Value'])
            dataset['Connections'] = data[u'Value']
        elif data['Variable_name'] == 'Uptime':
            dataset['Uptime'] = data[u'Value']
        elif data['Variable_name'] == 'Aborted_connects':
            dataset['Aborted_connects'] = data[u'Value']
        elif data['Variable_name'] == 'Aborted_clients':
            dataset['Aborted_clients'] = data[u'Value']
        elif data['Variable_name'] == 'Bytes_received':
            dataset['Bytes_received'] = data[u'Value']
        elif data['Variable_name'] == 'Bytes_sent':
            dataset['Bytes_sent'] = data[u'Value']
        elif data['Variable_name'] == 'Bytes_sent':
            dataset['Bytes_sent'] = data[u'Value']
        elif data['Variable_name'] == 'Max_used_connections':
            dataset['Max_used_connections'] = data[u'Value']
        elif data['Variable_name'] == 'Open_files':
            dataset['Open_files'] = data[u'Value']
        elif data['Variable_name'] == 'Open_table_definitions':
            dataset['Open_table_definitions'] = data[u'Value']
        elif data['Variable_name'] == 'Open_tables':
            dataset['Open_tables'] = data[u'Value']
        elif data['Variable_name'] == 'Opened_files':
            dataset['Opened_files'] = data[u'Value']
        elif data['Variable_name'] == 'Opened_tables':
            dataset['Opened_tables'] = data[u'Value']
        elif data['Variable_name'] == 'Opened_table_definitions':
            dataset['Opened_table_definitions'] = data[u'Value']
        elif data['Variable_name'] == 'Threads_connected':
            dataset['Threads_connected'] = data[u'Value']
        elif data['Variable_name'] == 'Threads_running':
            dataset['Threads_running'] = data[u'Value']
        elif data['Variable_name'] == 'Threads_created':
            dataset['Threads_created'] = data[u'Value']
        elif data['Variable_name'] == 'Threads_cached':
            dataset['Threads_cached'] = data[u'Value']
        elif data['Variable_name'] == 'Com_select':
            dataset['Com_select'] = data[u'Value']
        elif data['Variable_name'] == 'Com_insert':
            dataset['Com_insert'] = data[u'Value']
        elif data['Variable_name'] == 'Com_update':
            dataset['Com_update'] = data[u'Value']
        elif data['Variable_name'] == 'Com_delete':
            dataset['Com_delete'] = data[u'Value']
        elif data['Variable_name'] == 'Com_commit':
            dataset['Com_commit'] = data[u'Value']
        elif data['Variable_name'] == 'Com_rollback':
            dataset['Com_rollback'] = data[u'Value']
        elif data['Variable_name'] == 'Questions':
            dataset['Questions'] = data[u'Value']
        elif data['Variable_name'] == 'Queries':
            dataset['Queries'] = data[u'Value']
        elif data['Variable_name'] == 'Table_locks_immediate':
            dataset['Table_locks_immediate'] = data[u'Value']
        elif data['Variable_name'] == 'Table_locks_waited':
            dataset['Table_locks_waited'] = data[u'Value']
        elif data['Variable_name'] == 'Key_blocks_not_flushed':
            dataset['Key_blocks_not_flushed'] = data[u'Value']
        elif data['Variable_name'] == 'Key_blocks_unused':
            dataset['Key_blocks_unused'] = data[u'Value']
        elif data['Variable_name'] == 'Key_blocks_used':
            dataset['Key_blocks_used'] = data[u'Value']
        elif data['Variable_name'] == 'Key_read_requests':
            dataset['Key_read_requests'] = data[u'Value']
        elif data['Variable_name'] == 'Key_reads':
            dataset['Key_reads'] = data[u'Value']
        elif data['Variable_name'] == 'Key_write_requests':
            dataset['Key_write_requests'] = data[u'Value']
        elif data['Variable_name'] == 'Key_writes':
            dataset['Key_writes'] = data[u'Value']
        elif data['Variable_name'] == 'Innodb_dblwr_writes':
            dataset['Innodb_dblwr_writes'] = data[u'Value']
        elif data['Variable_name'] == 'Innodb_buffer_pool_bytes_data':
            dataset['Innodb_buffer_pool_bytes_data'] = data[u'Value']
        elif data['Variable_name'] == 'Innodb_buffer_pool_bytes_dirty':
            dataset['Innodb_buffer_pool_bytes_dirty'] = data[u'Value']
        elif data['Variable_name'] == 'Innodb_buffer_pool_pages_total':
            dataset['Innodb_buffer_pool_pages_total'] = data[u'Value']
        elif data['Variable_name'] == 'Innodb_buffer_pool_pages_data':
            dataset['Innodb_buffer_pool_pages_data'] = data[u'Value']
        elif data['Variable_name'] == 'Innodb_buffer_pool_pages_dirty':
            dataset['Innodb_buffer_pool_pages_dirty'] = data[u'Value']
        elif data['Variable_name'] == 'Innodb_buffer_pool_pages_flushed':
            dataset['Innodb_buffer_pool_pages_flushed'] = data[u'Value']
        elif data['Variable_name'] == 'Innodb_buffer_pool_pages_free':
            dataset['Innodb_buffer_pool_pages_free'] = data[u'Value']
        elif data['Variable_name'] == 'Innodb_buffer_pool_pages_misc':
            dataset['Innodb_buffer_pool_pages_misc'] = data[u'Value']
        elif data['Variable_name'] == 'Innodb_page_size':
            dataset['Innodb_page_size'] = data[u'Value']
        elif data['Variable_name'] == 'Innodb_pages_created':
            dataset['Innodb_pages_created'] = data[u'Value']
        elif data['Variable_name'] == 'Innodb_pages_read':
            dataset['Innodb_pages_read'] = data[u'Value']
        elif data['Variable_name'] == 'Innodb_pages_written':
            dataset['Innodb_pages_written'] = data[u'Value']
        elif data['Variable_name'] == 'Innodb_row_lock_current_waits':
            dataset['Innodb_row_lock_current_waits'] = data[u'Value']
        elif data['Variable_name'] == 'Innodb_rows_read':
            dataset['Innodb_rows_read'] = data[u'Value']
        elif data['Variable_name'] == 'Innodb_rows_inserted':
            dataset['Innodb_rows_inserted'] = data[u'Value']
        elif data['Variable_name'] == 'Innodb_rows_updated':
            dataset['Innodb_rows_updated'] = data[u'Value']
        elif data['Variable_name'] == 'Innodb_rows_deleted':
            dataset['Innodb_rows_deleted'] = data[u'Value']
        elif data['Variable_name'] == 'Innodb_data_read':
            dataset['Innodb_data_read'] = data[u'Value']
        elif data['Variable_name'] == 'Innodb_data_reads':
            dataset['Innodb_data_reads'] = data[u'Value']
        elif data['Variable_name'] == 'Innodb_data_writes':
            dataset['Innodb_data_writes'] = data[u'Value']
        elif data['Variable_name'] == 'Innodb_data_written':
            dataset['Innodb_data_written'] = data[u'Value']
        elif data['Variable_name'] == 'Innodb_data_fsyncs':
            dataset['Innodb_data_fsyncs'] = data[u'Value']
        elif data['Variable_name'] == 'Qcache_free_blocks':
            dataset['Qcache_free_blocks'] = data[u'Value']
        elif data['Variable_name'] == 'Qcache_free_memory':
            dataset['Qcache_free_memory'] = data[u'Value']
        elif data['Variable_name'] == 'Select_full_join':
            dataset['Select_full_join'] = data[u'Value']
        elif data['Variable_name'] == 'Select_full_range_join':
            dataset['Select_full_range_join'] = data[u'Value']
        elif data['Variable_name'] == 'Select_scan':
            dataset['Select_scan'] = data[u'Value']
        elif data['Variable_name'] == 'Sort_scan':
            dataset['Sort_scan'] = data[u'Value']
        elif data['Variable_name'] == 'Sort_rows':
            dataset['Sort_rows'] = data[u'Value']
        elif data['Variable_name'] == 'Table_locks_immediate':
            dataset['Table_locks_immediate'] = data[u'Value']
        elif data['Variable_name'] == 'Table_locks_waited':
            dataset['Table_locks_waited'] = data[u'Value']
        elif data['Variable_name'] == 'Table_open_cache_hits':
            dataset['Table_open_cache_hits'] = data[u'Value']
        elif data['Variable_name'] == 'Table_open_cache_misses':
            dataset['Table_open_cache_misses'] = data[u'Value']
        elif data['Variable_name'] == 'Table_open_cache_overflows':
            dataset['Table_open_cache_overflows'] = data[u'Value']
        else:
            continue

    return dataset

def repl_update_or_create(data, ip, port):

    record = Mysql_Replication.objects.filter(db_ip=ip)
    if record:
        record.update(db_ip=ip, db_port=port, is_slave=1, \
            master_server=data[0]['Master_Host'], master_user=data[0]['Master_User'], master_port=data[0]['Master_Port'], \
            slave_io_run=data[0]['Slave_IO_Running'], slave_sql_run=data[0]['Slave_SQL_Running'], delay=data[0]['SQL_Delay'], \
            current_binlog_file=data[0]['Relay_Log_File'], current_binlog_pos=data[0]['Relay_Log_Pos'], master_binlog_file=data[0]['Master_Log_File'], \
            master_binlog_pos=data[0]['Read_Master_Log_Pos'], master_binlog_space=data[0]['Relay_Log_Space'], slave_sql_running_state=data[0]['Slave_SQL_Running_State'])
    else:
        Mysql_Replication.objects.create(db_ip=ip, db_port=port, is_slave=1, \
            master_server=data[0]['Master_Host'], master_user=data[0]['Master_User'], master_port=data[0]['Master_Port'], \
            slave_io_run=data[0]['Slave_IO_Running'], slave_sql_run=data[0]['Slave_SQL_Running'], delay=data[0]['SQL_Delay'], \
            current_binlog_file=data[0]['Relay_Log_File'], current_binlog_pos=data[0]['Relay_Log_Pos'], master_binlog_file=data[0]['Master_Log_File'], \
            master_binlog_pos=data[0]['Read_Master_Log_Pos'], master_binlog_space=data[0]['Relay_Log_Space'], slave_sql_running_state=data[0]['Slave_SQL_Running_State'])

def connection_querySet(datas):

    dataset = {}
    for data in datas:
        if data['Variable_name'] == 'Connections':
            dataset['Connections'] = data['Value']
        elif data['Variable_name'] == 'Max_used_connections':
            dataset['Max_used_connections'] = data['Value']
        elif data['Variable_name'] == 'Threads_connected':
            dataset['Threads_connected'] = data['Value']
        else:
            continue

    return dataset

def connection_create(dataset, ip, port):
    try:
        # print timezone.localtime(timezone.now())
        Mysql_Connection.objects.create(db_ip=ip, db_port=port, connect_count=dataset['Connections'], thead_connect=dataset['Threads_connected'], \
            max_connect=dataset['Max_used_connections'])
    except Exception as e:
        print e

def connection_update_or_create(dataset, ip, port):

    record = Mysql_Connection.objects.filter(db_ip=ip)
    if record:
        record.update(db_ip=ip, db_port=port, connect_count=dataset['Connections'], thead_connect=dataset['Threads_connected'], \
            max_connect=dataset['Max_used_connections'])
    else:
        Mysql_Connection.objects.create(db_ip=ip, db_port=port, connect_count=dataset['Connections'], thead_connect=dataset['Threads_connected'], \
            max_connect=dataset['Max_used_connections'])
