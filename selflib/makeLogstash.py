# -*- coding: utf-8 -*-
import os
import traceback
import json
import re

def makeLogstash(mysqlconfig, dbconfig, esconfig, basepath):
    try:
        filedir = '%s/logs/logstash' % basepath
        tempfile = '%s/config/logstash.conf.template' % basepath
        if not os.path.exists(filedir):
            os.makedirs(filedir)
        for key,value in dbconfig.items():
            filename = '%s.conf' % key
            print 'Create Logstash Config: %s' % filename
            filepath = '%s/%s' % (filedir, filename)
            key_list = key.split('.')
            database = key_list[0]
            table = key_list[1]
            es_key = value["es_key"]
            value_list = es_key.split(';')
            doc_id = ''
            for x in value_list:
                doc_id += '%%{%s}' % x

            format_list = value["format"]
            jdbc_tracking = value["jdbc_tracking"]
            if len(jdbc_tracking) > 0:
                run_jdbc_template = '    last_run_metadata_path => "/tmp/sql_last_value.%s"\n' % jdbc_tracking["column"]
                run_jdbc_template += '    use_column_value => true\n'
                run_jdbc_template += '    tracking_column => "%s"\n' % jdbc_tracking["column"].lower()
                run_jdbc_template += '    tracking_column_type => "%s"\n' % jdbc_tracking["type"]
                if jdbc_tracking["type"] == "timestamp":
                    run_jdbc_template += '    statement => "SELECT * FROM `%s` where `%s` > :sql_last_value and `%s` <= DATE_ADD(:sql_last_value, INTERVAL 45 DAY)"'
                else:
                    run_jdbc_template += '    statement => "SELECT * FROM `%s` where `%s` > :sql_last_value and `%s` <= :sql_last_value+200000"' % (
                    table, jdbc_tracking["column"], jdbc_tracking["column"])
            else:
                run_jdbc_template = '    statement => "SELECT * FROM `%s`"' % table
            filter_template = ''
            if len(format_list) > 0:
                filter_template += 'filter {\n'
                filter_template += '  mutate {\n'
                filter_template += '    convert => {\n'
                for xx, yy in format_list.items():
                    if yy != 'datetime':
                        filter_template += '      "%s" => "%s"\n' % (xx, yy)
                filter_template += '    }\n'
                filter_template += '  }\n'
                filter_template += '}\n'
            jdbc_connection_string_template = 'jdbc:mysql://%s:%s/%s?zeroDateTimeBehavior=round' % (mysqlconfig["host"], mysqlconfig["port"], database)
            jdbc_user_template = mysqlconfig["user"]
            jdbc_password_template = mysqlconfig["password"]
            jdbc_driver_library_template = '%s/library/mysql-connector-java-5.1.46-bin.jar' % basepath
            statement_table_template = table
            es_host_list = esconfig["hosts"]
            hosts_template = json.dumps(es_host_list)
            index_template = key
            document_id_template = doc_id.lower()
            temp_list = [
                "jdbc_connection_string_template",
                "jdbc_user_template",
                "jdbc_password_template",
                "jdbc_driver_library_template",
                "run_jdbc_template",
                "statement_table_template",
                "hosts_template",
                "index_template",
                "document_id_template",
                "filter_template"
            ]
            with open(tempfile, 'r') as fileobj:
                temp_str = fileobj.read()
                for y in temp_list:
                    exec('temp_str = re.sub("%s", %s, temp_str)' % (y, y))
            with open(filepath, 'w') as f:
                f.write(temp_str)

    except Exception,e:
        print traceback.print_exc()
        os._exit(100)