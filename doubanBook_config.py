# 保存设置
# 当你定义好了host,port,database_name之后再将connect改为True
connect = True
host = 'localhost'
port = 27017
#数据库连接超时时间 单位:毫秒
database_connect_time_out=500
book_database_name='data'
book_data_collection_name='book_jinjie'
#更换ip的时间  每多少秒重新选择IP 无论此时ip是否正常 防止ip被封 单位:秒
changeIP_seconds=60
#request_with_proxy()方法超时时间 单位：秒  每次对一个http请求的超时时间 一次http请求可能会因为多次request超时 导致方法阻塞
proxy_timeout=900
#request模块下的代理超时时间 每次代理的超时
request_timeout=5
#停用词词典文件名
stopwords_file_name='stopwords.txt'
#黑名单词词典文件名
blackwords_file_name='blackwords.txt'
#返回状态码200但是要过滤的页面 因为豆瓣的页面当IP被限制时，会返回一个200状态码的页面，但是此页面的信息告诉我IP被封，所以我需要过滤掉，算这次请求是一次不成功的请求
custom_filter_str='<script>var d=[navigator.platform,navigator.userAgent,navigator.vendor].join("|");window.location.href="https://sec.douban.com/'
# 豆瓣评分  限制只抓取设置的评分以上的书籍
limit_douban_rate=7