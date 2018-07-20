# -*- coding: utf-8 -*-
import traceback
import yaml

def loadDbConfig(bathpath):
    try:
        config_file = '%s/config/db.yaml' % bathpath
        with open(config_file, "r") as file_obj:
            the_dict = yaml.load(file_obj)
            return_dict = {}
            for dbname, tablelist in the_dict.items():
                for i in tablelist:
                    return_key = '%s.%s' % (dbname, i['tablename'])
                    es_key = ";".join(i["es_key"])
                    format_list = {}
                    jdbc_tracking = {}
                    if 'format' in i:
                        format_list = i["format"]
                    if 'jdbc_tracking' in i:
                        jdbc_tracking = i["jdbc_tracking"]
                    return_dict[return_key] = {"es_key":es_key, "format":format_list, "jdbc_tracking":jdbc_tracking}
            return 0, return_dict
    except Exception,e:
        print traceback.print_exc()
        return 100, str(e)

def loadCfgConfig(bathpath):
    try:
        config_file = '%s/config/config.yaml' % bathpath
        with open(config_file, "r") as file_obj:
            the_dict = yaml.load(file_obj)
            return 0, the_dict
    except Exception,e:
        print traceback.print_exc()
        return 100, str(e)