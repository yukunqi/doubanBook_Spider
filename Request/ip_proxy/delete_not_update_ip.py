# -*- coding: utf-8 -*-

"""

按照ip的插入时间距离现在的时间, 大于阀值时间的拿出来进行检测, 若已经无法使用, 则删除;若还可以使用,则更新插入的时间;

"""
import sys

# 这里写你自己的框架保存地址
sys.path.append('F:/PycharmProjects/DEMO1/AiSpider')
from config import log_folder_name
from config import host, port, database_name,database_connect_time_out
from ip_proxy.proxy_basic_config import collection_name, over_time
import pymongo
import time
from urllib import parse
from ip_proxy._request import valid
from ip_spider.log_format import logger
from pymongo.errors import ServerSelectionTimeoutError
from pymongo.errors import ConnectionFailure

diy_header = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}
log_name = 'delete_not_update_ip'
file_folder = log_folder_name
delete_existed_log = False




def connect_to_mongodb():
    try:
        client = pymongo.MongoClient(host, port,serverSelectionTimeoutMS=database_connect_time_out,connectTimeoutMS=database_connect_time_out)
        client.server_info()
        msg = 'host: {}  port:  {}  database_name : {}   MongoDB数据库连接成功'.format(host, port, database_name)
        logger.info(msg)
    except ServerSelectionTimeoutError as e:
        msg = 'host: {}  port:  {}  database_name : {}   MongoDB数据库连接失败 原因: 可能配置文件出错或者连接超时  超时时间为:  {} 毫秒'.format(host, port, database_name,database_connect_time_out)
        raise ConnectionFailure(msg)

    db = client[database_name]
    collection = db[collection_name]
    return collection


def format_time_to_timestamp(foramt_time):
    st = time.strptime(foramt_time, '%Y-%m-%d %H:%M:%S')
    return time.mktime(st)

def timestamp_to_format_time(timestamp):
    return time.strftime('%Y-%m-%d %H:%M:%S',timestamp)

def check(when=time.time):
    collection = connect_to_mongodb()
    for data in collection.find():
        ip = data.get('ip')
        target_url = data.get('target_url')
        ip_stamp = format_time_to_timestamp(data.get('insert_time'))

        has_existed = int(when() - ip_stamp)
        if has_existed > over_time:
            diy_header['Host'] = parse.urlparse(target_url).netloc

            _args = {
                "url": target_url,
                "diy_header": diy_header,
                "time_out": 10,
                "_ip": ip,
            }

            _id = ip + '_' + target_url
            # 调用验证函数
            result1, result2 = valid(_args, False)
            if result1 is None:
                msg = 'delete ip: [{ip}], target_url is [{target_url}]'.format(ip=ip, target_url=target_url)
                logger.info(msg)
                collection.delete_one({'_id': _id})
            else:
                msg = 'update ip: [{ip}], target_url is [{target_url}]'.format(ip=ip, target_url=target_url)
                logger.info(msg)
                collection.update_one({'_id': _id}, {'$set':{'insert_time': timestamp_to_format_time(time.localtime(when())),
                                                             'response_time': result1}})

if __name__ == '__main__':
    check(time.time)
