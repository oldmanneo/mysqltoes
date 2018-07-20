# -*- coding: utf-8 -*-
import sys
import os
import traceback
from pykafka import KafkaClient
from pykafka.simpleconsumer import OffsetType

class kafkaFunc(object):
    def __init__(self, kafkaconfig, esobj, dbconfig):
        self.kafkaconfig = kafkaconfig
        self.dbconfig = dbconfig
        self.esobj = esobj

    def __kafkaConnection(self):
        try:
            print self.kafkaconfig["bootstrap.servers"]
            self.kafkaclient = KafkaClient(hosts=self.kafkaconfig["bootstrap.servers"])
            self.kafkatopic = self.kafkaclient.topics[self.kafkaconfig["topic"]]
        except Exception,e:
            print traceback.print_exc()
            os._exit(100)

    def runKafkaConsumer(self, runFunc):
        try:
            exec('auto_offset_reset = OffsetType.%s' % self.kafkaconfig["auto_offset_reset"])
            reset_offset_on_start = self.kafkaconfig["reset_offset_on_start"]
            self.__kafkaConnection()
            consumer = self.kafkatopic.get_balanced_consumer(
                consumer_group=self.kafkaconfig["consumer_group"],
                auto_offset_reset=auto_offset_reset,
                reset_offset_on_start=reset_offset_on_start,
                auto_commit_enable=True,
                zookeeper_connect=self.kafkaconfig["zookeeper.servers"]
            )
            for message in consumer:
                if message is not None:
                    runFunc(message, self.dbconfig, self.esobj)
        except Exception,e:
            print traceback.print_exc()
