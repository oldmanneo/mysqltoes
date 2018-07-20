# -*- coding: utf-8 -*-
import traceback
import json
import datetime
from dateutil import parser

def runMessage(message, listenDbTables, esobj):
    try:
        change_dict = json.loads(message.value)
        database = change_dict["database"]
        table = change_dict["table"]
        db_table = '%s.%s' % (database, table)
        if db_table in listenDbTables:
            data = change_dict["data"]
            es_key = listenDbTables[db_table]["es_key"]
            es_keys = es_key.split(';')
            es_id = ''
            for x in es_keys:
                es_id += str(data[x])

            es_id = es_id.lower()

            format_list = listenDbTables[db_table]["format"]
            for xx,yy in format_list.items():
                if yy == 'datetime':
                    the_datetime = data[xx]
                    if the_datetime != None:
                        datetimeobj = parser.parse(the_datetime)
                        new_datetime = datetimeobj+datetime.timedelta(hours=-8)
                        data[xx] = new_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

            update_type = change_dict["type"]

            datenow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print '\n[ %s ]' % datenow
            print 'KAFKA  OFFSET : %d' % message.offset
            print 'ES     _id    : %s' % es_id
            print 'DB     TABLE  : %s' % db_table
            print 'UPDATE TYPE  : %s' % update_type
            print json.dumps(data)
            print 'ES result:'
            __dorun(esobj, db_table, update_type, es_id, data)
        else:
            print '\nKAFKA  OFFSET : %d    (PASS)  %s' % (message.offset, db_table)
    except Exception,e:
        print traceback.print_exc()

def __dorun(esobj, indexname, update_type, es_id, data):
    try:
        if update_type == "insert" or update_type == "update":
            esobj.doc_index(indexname, 'doc', es_id, data)
        elif update_type == "delete":
            esobj.doc_delete(indexname, 'doc', es_id)
        else:
            print 'Warning UPDATE TYPE not in (insert / update / delete)'
    except Exception,e:
        print traceback.print_exc()
