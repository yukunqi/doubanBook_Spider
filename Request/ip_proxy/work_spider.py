# -*- coding: utf-8 -*-

import sys

# 这里写你自己的地址
sys.path.append('F:\PycharmProjects\DEMO1')


from ip_spider.threads import start, work_queue, save_queue
from ip_spider.log_format import logger

from ip_proxy.get_proxies_base_spider import SpiderMain


class WorkSpider(SpiderMain):
    def __init__(self):
        super(WorkSpider, self).__init__()

    # 重写run方法,
    # 若请求的函数为自定义, 则可以在crawl函数中设置: request=your_request_function, 默认为框架中的request
    def run(self):
        start()
        self.craw()

def execute_spider():
    work_spider = WorkSpider()

    work_spider.run()

    # Blocking
    work_queue.join()
    save_queue.join()

    # Done
    logger.info('All Job Finishing, Please Check!')

if __name__ == '__main__':
    work_spider = WorkSpider()

    work_spider.run()

    # Blocking
    work_queue.join()
    save_queue.join()

    # Done
    logger.info('All Job Finishing, Please Check!')
