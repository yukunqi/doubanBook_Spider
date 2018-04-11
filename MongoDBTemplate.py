# -*- coding: utf-8 -*-

from doubanBook_config import *
import pymongo
import logging
from pymongo.errors import ServerSelectionTimeoutError
from pymongo.errors import ConnectionFailure


logger=logging.getLogger("MongoDBTemplate")

class MongoDBTemplate(object):

    def __init__(self,database_name,collection_name):
        self.host=host
        self.port=port
        self.database=database_name
        self.collection=collection_name
        if connect:
            self._connect()

    def _connect(self):
        try:
            self.client = pymongo.MongoClient(self.host,self.port, serverSelectionTimeoutMS=database_connect_time_out,connectTimeoutMS=database_connect_time_out,connect=False)
            self.client.admin.command("ismaster")
            msg = 'host: {}  port:  {}  database_name : {}   MongoDB数据库连接成功'.format(host, port, self.database)
            logger.info(msg)

            self.db = self.client[self.database]
        except ServerSelectionTimeoutError as e:
            msg = 'host: {}  port:  {}  database_name : {}   MongoDB数据库连接失败 原因: 可能配置文件出错或者连接超时  超时时间为:  {} 毫秒'.format(host, port, self.database, database_connect_time_out)
            raise ConnectionFailure(msg)

    def _disconnect(self):
        self.client.close()

    def _insert(self,data):
        collection=self.db[self.collection]
        collection.insert(data)

    def find_one(self,kv):
        collection=self.db[self.collection]
        return collection.find_one(kv)

    def page_query(self,query_filter=None,projection=None,page_size=5,pageNo=1):
        skip=page_size*(pageNo-1)
        collection=self.db[self.collection]
        record=collection.find(filter=query_filter,projection=projection).limit(page_size).skip(skip)
        return record

    def get_collection(self):
        return self.db[self.collection]

    def get_collection_by_collectionName(self,collection_name):
        return self.db[collection_name]