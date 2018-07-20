# -*- coding: utf-8 -*-
import sys
import os
import traceback
from selflib.loadconfig import *
from selflib.kafka_func import kafkaFunc
from selflib.run_message_func import runMessage
from selflib.Eslib import esLib

reload(sys)
sys.setdefaultencoding('utf-8')

bathpath = sys.path[0]

class runIndex(object):
    def __init__(self):
        self.cfgconfig = self.__makeCfgConfig()
        self.dbconfig = self.__makeDbConfig()
        self.kafkaconfig = self.__makeKafkaConfig()
        self.esconfig = self.__makeEsConfig()
        self.mysqlconfig = self.__makeMysqlConfig()

    def __makeCfgConfig(self):
        try:
            status, result = loadCfgConfig(bathpath)
            if status == 0:
                return result
            else:
                print 'config.yaml Config Load Faild'
                os._exit(100)
        except Exception,e:
            print traceback.print_exc()
            os._exit(100)

    def __makeMysqlConfig(self):
        try:
            return self.cfgconfig["mysql"]
        except Exception,e:
            print traceback.print_exc()
            os._exit(100)

    def __makeKafkaConfig(self):
        try:
            return self.cfgconfig["kafka"]
        except Exception,e:
            print traceback.print_exc()
            os._exit(100)

    def __makeEsConfig(self):
        try:
            return self.cfgconfig["elasticsearch"]
        except Exception,e:
            print traceback.print_exc()
            os._exit(100)

    def __makeDbConfig(self):
        try:
            status, result = loadDbConfig(bathpath)
            if status == 0:
                return result
            else:
                print 'DB Config Load Faild'
                os._exit(100)
        except Exception,e:
            print traceback.print_exc()
            os._exit(100)

    def __runCheck(self):
        initDoneFile = '%s/logs/done.lock' % bathpath
        if os.path.exists(initDoneFile):
            return True
        else:
            return False

    def run_index(self):
        try:
            if self.__runCheck():
                esobj = esLib(self.esconfig)
                kafkaobj = kafkaFunc(self.kafkaconfig, esobj, self.dbconfig)
                kafkaobj.runKafkaConsumer(runMessage)
            else:
                print 'ERROR : Please Init before Index'
        except Exception,e:
            print traceback


if __name__ == '__main__':
    a = runIndex()
    a.run_index()