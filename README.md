# doubanBook_Spider

豆瓣图书爬虫，爬取豆瓣图书上的大部分和书籍相关的数据。同时爬取了每本书籍的评论和书评。

使用了另一个github项目(https://github.com/yukunqi/ProxySpider)
上的代理IP作为数据抓取的网络请求方法

可以直接运行爬取豆瓣书籍数据用来作为项目展示或者进行数据分析

本项目特点：

1.结合代理IP请求，解决IP被封问题。

2.自定义爬取书籍的页数，开始页等

3.详细的日志记录，充分考虑爬取过程中的各种异常。

4.以标签为起点进行爬取，数据存储在MongoDB中

**欢迎star和使用这个github项目，也欢迎提各种issue和与我交流。**

## 使用方法
1.安装Request中所需要的类库和MongoDB数据库，使得网络请求函数能够正常运行

2.直接运行main方法即可开始抓取，第一个参数是要爬取的标签，第二个参数是排除在外的书籍集合（因为爬虫可能由于程序错误或者主动关闭导致爬到一半就中断，排除已存在数据库中的书籍，可以防止数据重复）
后两个就是限制爬取的页数和开始爬取的页数
![](https://github.com/yukunqi/doubanBook_Spider/blob/master/%E4%BD%BF%E7%94%A8%E6%88%AA%E5%9B%BE.jpg)



