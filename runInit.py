# -*- coding: utf-8 -*-
import sys
import os
from runIndex import runIndex
from selflib.Eslib import esLib
from selflib.makeLogstash import makeLogstash
import traceback

bathpath = sys.path[0]

class runInit(object):
    def __init__(self):
        self.__checkConfig()
        self.runindex = runIndex()

    def __checkConfig(self):
        try:
            print 'Checking Config File ......'
            config_list = [
                'config.yaml',
                'db.yaml',
                'logstash.config.template',
                'mapping.json'
            ]
            config_path = '%s/config' % bathpath
            for x in config_list:
                thepath = '%s/%s' % (config_path, x)
                if not os.path.exists(thepath):
                    print 'Error Config Not Found: config/%s' % x
                    os._exit(100)
        except Exception,e:
            print traceback.print_exc()
            os._exit(100)

    def getInput(self):
        try:
            mysqlHost = raw_input('请输入MySQL Host(127.0.0.1):')
            if mysqlHost == '':
                mysqlHost = '127.0.0.1'

            mysqlPort = raw_input('请输入MySQL Port(3306):')
            if mysqlPort == '':
                mysqlPort = '3306'

            mysqlUser = raw_input('请输入MySQL User(root):')
            if mysqlUser == '':
                mysqlUser = 'root'

            mysqlPasswd = ''
            while mysqlPasswd == '':
                mysqlPasswd = raw_input('请输入MySQL Password(不能为空):')

            return {"mysqlHost": mysqlHost, "mysqlPort": mysqlPort, "mysqlUser": mysqlUser, "mysqlPasswd": mysqlPasswd}
        except Exception,e:
            print traceback.print_exc()
            os._exit(100)

    def __makeInitDone(self):
        try:
            donefile_path = '%s/logs' % bathpath
            if not os.path.exists(donefile_path):
                os.makedirs(donefile_path)
            donefile = '%s/done.lock' % donefile_path
            f = open(donefile, 'w')
            f.close()
        except Exception,e:
            print traceback.print_exc()

    def run_init(self):
        try:
            #input_dict = self.getInput()
            makeLogstash(self.runindex.mysqlconfig, self.runindex.dbconfig, self.runindex.esconfig, bathpath)
            esobj = esLib(self.runindex.esconfig)
            esobj.createAllIndex(self.runindex.dbconfig, bathpath)
            self.__makeInitDone()
        except Exception,e:
            print traceback.print_exc()
            os._exit(100)

if __name__ == '__main__':
    a = runInit()
    a.run_init()