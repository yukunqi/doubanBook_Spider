import pymongo
import random
import time
import requests
from config import *
from ip_spider.log_format import logger
from pymongo.errors import ServerSelectionTimeoutError
from pymongo.errors import ConnectionFailure
from ip_spider.UAS import *
from ip_proxy.delete_not_update_ip import check
from ip_proxy.work_spider import execute_spider


class MainRequest(object):
    def __init__(self,mongo_instance=None,current_ip_proxy=None,ipList=None):
        self.mongo=mongo_instance
        self.current_ip=current_ip_proxy
        self.ipList=ipList
        self.host=host
        self.port=port
        self.database=database_name
        self.collection_name=collection_name
        self._connect()

    def _connect(self):
        try:
            self.client = pymongo.MongoClient(self.host,self.port, serverSelectionTimeoutMS=database_connect_time_out,connectTimeoutMS=database_connect_time_out)
            self.client.server_info()
            msg = 'host: {}  port:  {}  database_name : {}   MongoDB数据库连接成功'.format(host, port, self.database)
            logger.info(msg)

            self.db = self.client[self.database]
            self.get_all_IP(self.collection_name)
            self.getRandomOne()
        except ServerSelectionTimeoutError as e:
            msg = 'host: {}  port:  {}  database_name : {}   MongoDB数据库连接失败 原因: 可能配置文件出错或者连接超时  超时时间为:  {} 毫秒'.format(host, port, self.database, database_connect_time_out)
            raise ConnectionFailure(msg)

    def get_all_IP(self,collection_name):
        collection = self.db[collection_name]
        data = collection.find().sort("insert_time", pymongo.DESCENDING).sort("response_time", pymongo.ASCENDING)
        ips = []
        for i in data:
            ips.append(i.get('ip'))

        if len(ips) == 0:
            logger.info("数据库内暂无IP")
            self.update_ip_pool()

        self.ipList=ips
        return ips

    def getRandomOne(self):
        self.current_ip=random.choice(self.ipList)
        return self.current_ip

    def get_one(self,index):
        len=self.getSize()

        if self.ipList is None or len == 0:
            raise IndexError

        if index >= len:
            index = 0

        return self.ipList[index]

    def getSize(self):
        if self.ipList is None:
            raise Exception
        return len(self.ipList)

    def update_ipList(self):
        self.get_all_IP(self.collection_name)

    def update_ip_pool(self):
        logger.info("开始执行更新IP代理池中的IP并从网上抓取新的IP放入池中")
        start_time = time.time()
        check()
        execute_spider()
        end_time = time.time()
        logger.info("刷新数据库中IP带内存中来")
        self.update_ipList()
        logger.info("IP代理池更新完毕..  使用时间为 {} 秒".format(end_time - start_time))

    def _request_with_proxy(self,url,use_proxy):

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "User-Agent": random.choice(PC_USER_AGENTS)
        }

        # 获取进入while循环的初始时间
        start_time = time.time()
        while True:

            # 获取当前时间和之前的初始时间做比较，如果超出自定义的时间则raise requests.exceptions.ProxyError
            end_time = time.time()
            if int(end_time - start_time) > proxy_timeout:
                logger.info(
                    "request with proxy 方法时间执行过长 可能原因： IP池内IP全部失效或被目标网站封掉IP其他异常错误  当前ip为 {} 程序进行休息状态 休息时长为: {} 秒".format(
                        self.current_ip, proxy_timeout))
                time.sleep(proxy_timeout)
                self.update_ip_pool()
                msg = "IP代理池休息完毕并更新 请重新进行数据抓取 可能原因： 查找历史日志   当前ip为 {}".format(self.current_ip)
                raise requests.exceptions.ProxyError(msg)
            proxy = {
                'http': self.current_ip,
                'https': self.current_ip
            }

            if use_proxy:
                try:
                    response = requests.get(url, proxies=proxy, timeout=request_timeout, headers=headers)
                    code = response.status_code
                    msg = "doing http request successfully current proxy ip is {} status_code :{}".format(self.current_ip, code)
                    logger.info(msg)

                    if code == 404:
                        msg = " 404 Client Error: Not Found for url:{}".format(url)
                        logger.info(msg)
                        return response

                    response.raise_for_status()
                    if code == 200 and custom_filter_str != '' and custom_filter_str in response.text:
                        raise Exception

                    return response
                except requests.HTTPError as e:
                    logger.info(e)
                    self.current_ip = self.getRandomOne()
                    msg = "random pick a ip from ipList new ip is {}".format(self.current_ip)
                    logger.info(msg)
                except Exception as e:
                    print(e)
                    msg = "ip is {} can't use ".format(self.current_ip)
                    logger.info(msg)
                    self.current_ip = self.getRandomOne()
                    msg = "random pick a ip from ipList new ip is {}".format(self.current_ip)
                    logger.info(msg)
            else:
                try:
                    response = requests.get(url, timeout=request_timeout, headers=headers)
                    return response
                except Exception as e:
                    msg = "ip is {} can't use ".format(self.current_ip)
                    logger.info(msg)
                    self.current_ip = self.getRandomOne()
                    msg = "random pick a ip from ipList new ip is {}".format(self.current_ip)
                    logger.info(msg)



