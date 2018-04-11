# -*- coding: utf-8 -*-


import sys

sys.path.append('F:\PycharmProjects\DEMO1\IP_POOL')

import pymongo
from config import *
from ip_spider.log_format import logger
from pymongo.errors import ServerSelectionTimeoutError
from pymongo.errors import ConnectionFailure

class Pipeline(object):

    def __init__(self,database=database_name):
        self.host = host
        self.port = port
        self.database = database
        if connect:
            self._connect()

    def _connect(self):
        try:
            self.client = pymongo.MongoClient(self.host,self.port, serverSelectionTimeoutMS=database_connect_time_out,connectTimeoutMS=database_connect_time_out)
            self.client.server_info()
            msg = 'host: {}  port:  {}  database_name : {}   MongoDB数据库连接成功'.format(host, port, self.database)
            logger.info(msg)

            self.db = self.client[self.database]
        except ServerSelectionTimeoutError as e:
            msg = 'host: {}  port:  {}  database_name : {}   MongoDB数据库连接失败 原因: 可能配置文件出错或者连接超时  超时时间为:  {} 毫秒'.format(host, port, self.database, database_connect_time_out)
            raise ConnectionFailure(msg)

    def process_item(self, item, collection_name, use_id=True):
        collection = self.db[collection_name]
        msg = 'insert data into collection: [%s]' %collection_name
        logger.info(msg)
        if use_id:
            collection.update({'_id':item['_id']}, dict(item), True)
        else:
            collection.insert(dict(item))

        # self.client.close()


    def find_recent_item(self,collection_name,limit_size):
        collection=self.db[collection_name]
        data=collection.find().sort("insert_time",pymongo.DESCENDING).sort("response_time",pymongo.ASCENDING).limit(limit_size)
        ips=[]
        for i in data:
            ips.append(i.get('ip'))

        return  ips

    def get_all_IP(self,collection_name):
        collection = self.db[collection_name]
        data = collection.find().sort("insert_time", pymongo.DESCENDING).sort("response_time", pymongo.ASCENDING)
        ips = []
        for i in data:
            ips.append(i.get('ip'))

        return ips

pipeline = Pipeline()