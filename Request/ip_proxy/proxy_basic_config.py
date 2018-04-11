# -*- coding: utf-8 -*-


"""

代理网址及解析字典

status 代理状态, 若不想爬取此网站,可以将status设置为非active的任意值
request_method , 请求方法, 必写, 当为post的时候, 必须定义提交的post_data, 否则会报错.因项目的特殊性, 提交的数据中会带有页码数据, 所以在这里将
post_data 定义为列表, 里面的数据为字典格式
url 代理网址

parse_type  解析类型,默认提供: xpath, re

(1) xpath
ip_port_together ip地址和ip的端口是否在一个字段中
若为地址与端口在一起,则建议key为ip_address_and_port
若为地址与端口不在一起,则建议key为ip_address, ip_port

(2) re
若解析的类型为re, 则ip_port_together可以为任意的值
parse_method中只有一个键: _pattern

parse_func 解析函数, 默认值为system, 当需要使用自定义的解析函数的时候, 需要显式的定义该字段为自定义的解析函数
解析函数要有四个参数, 分别为value, html_content, parse_type, website_name

header 因网址较多, 所以在这里可以自定义头
"""


# 定义检测的目标网站
target_urls = ['https://www.baidu.com', 'https://httpbin.org/get']

# 数据库集合名
collection_name = 'proxy'

# 数据库中IP存活时间阀值, 超过及对其重新检测
over_time = 1800

url_parse_dict = {
    # data5u
    'data5u': {
        'status':'active',
        'request_method':'get',
        'url': ['http://www.data5u.com/free/{tag}/index.shtml'.format(tag=tag) for tag in ['gngn', 'gnpt', 'gwgn', 'gwpt']],
        'parse_type': 'xpath',
        'ip_port_together': False,
        'parse_method':{
            'ip_address': '//ul[@class="l2"]/span[1]/li/text()',
            'ip_port': '//ul[@class="l2"]/span[2]/li/text()',
        },
        'parse_func': 'system'
    },

    # xicidaili
    'xicidaili': {
        'status': 'active',
        'request_method': 'get',
        'url': ['http://www.xicidaili.com/nn/{page}'.format(page=page) for page in range(1, 20)],
        'parse_type': 'xpath',
        'ip_port_together': False,
        'parse_method': {
            'ip_address': '//tr[@class="odd"]/td[2]/text()',
            'ip_port': '//tr[@class="odd"]/td[3]/text()',
        },
        'parse_func': 'system'

    },

    # 66ip
    '66ip': {
        'status': 'active',
        'request_method': 'get',
        'url': ['http://m.66ip.cn/{page}.html'.format(page=page) for page in range(1, 5)],
        'parse_type': 're',
        'ip_port_together': False,
        'parse_method': {
            '_pattern': '<tr><td>([\d\.]*?)</td><td>(.*?)</td>',
        },
        'parse_func': 'system'

    }
}

