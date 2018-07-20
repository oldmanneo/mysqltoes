# -*- coding: utf-8 -*-
import os
import traceback
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import json


class esLib(object):
    def __init__(self, esconfig):
        self.esconfig = esconfig
        self.es = Elasticsearch(self.esconfig["hosts"])

    def createAllIndex(self, dbconfig, basepath):
        try:
            mappingBody = self.loadMappings(basepath)
            for indexname in dbconfig.keys():
                print '\nInitialization Elasticsearch Index : %s' % indexname
                if self.es.indices.exists(index=indexname):
                    print 'Index Exists                       : %s' % indexname
                else:
                    print 'Creating Index                     : %s' % indexname
                    self.es.indices.create(index=indexname, body=mappingBody)
        except Exception,e:
            print traceback.print_exc()
            os._exit(100)

    def loadMappings(self, basepath):
        try:
            mapping_file = '%s/config/mapping.json' % basepath
            file_obj = open(mapping_file, "r")
            mapping_dict = json.load(file_obj)
            return mapping_dict
        except Exception,e:
            print traceback.print_exc()
            os._exit(100)

    def doc_index(self, indexname, typename, es_id, databody):
        try:
            print  self.es.index(index=indexname, doc_type=typename, id=es_id, body=databody)
        except Exception,e:
            print traceback.print_exc()

    def doc_delete(self, indexname, typename, es_id):
        try:
            print  self.es.delete(index=indexname, doc_type=typename, id=es_id)
        except Exception,e:
            print traceback.print_exc()
