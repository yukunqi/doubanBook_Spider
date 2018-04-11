# -*- coding: utf-8 -*-


import random
from ip_spider.data_save import pipeline
from ip_proxy.proxy_basic_config import collection_name
import json
class DB(object):
    def __init__(self, collection):
        self.collection = collection

    def get_one(self):
        _ips = []
        for _ in self.collection.find():
            _ips.append(_.get('ip'))
        return random.choice(_ips)

    def get_all(self):
        _ips = []
        for _ in self.collection.find():
            _ips.append(_.get('ip'))
        return _ips

    def delete_one(self, ip):
        self.collection.delete_one({'_id': ip})

    def total(self):
        return self.collection.count()


if __name__ == '__main__':
    db = DB(pipeline.db[collection_name])
    json_str=db.get_all()
    json_string = json.dumps(json_str, ensure_ascii=False, indent=4)
    print(json_string)