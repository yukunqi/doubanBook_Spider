# -*- coding: utf-8 -*-



# 爬虫名称
spider_name = 'get_ip'

# 日志设置
log_folder_name = '%s_logs' % spider_name
delete_existed_logs = False

# 请求参数设置
thread_num = 50
sleep_time = 0.5
retry_times = 10
time_out = 5
# 当use_proxy为True时，必须在请求的args中或者在配置文件中定义ip, eg: ip="120.52.72.58:80", 否则程序将报错
use_proxy = False
ip = None

# 移动端设置为 ua_type = 'mobile'
ua_type = 'pc'

# 队列顺序
FIFO = 0
# 默认提供的浏览器头包括user_agent  host, 若需要更丰富的header,可自行定定义新的header,并赋值给diy_header

diy_header = None

# 定义状态码,不在其中的均视为请求错误或异常
status_code = [200, 304, 404]

# 保存设置
# 当你定义好了host,port,database_name之后再将connect改为True
connect = True

host = 'localhost'

port = 27017

#ip存放的数据库名称
database_name = 'free_ip'
#ip存放的集合名称
collection_name = 'proxy'

#数据库连接超时时间 单位:毫秒
database_connect_time_out=3000
#request_with_proxy()方法超时时间 单位：秒  每次对一个http请求的超时时间 一次http请求可能会因为多次request超时 导致方法阻塞
proxy_timeout=900
#request模块下的代理超时时间 每次代理的超时
request_timeout=5
#返回状态码200但是要过滤的页面 有时候网站会返回IP被限制的响应内容，此时需要自定义过滤掉。算这次请求是一次不成功的请求
custom_filter_str=''
