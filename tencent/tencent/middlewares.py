# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from time import sleep

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from scrapy.http import HtmlResponse

class TencentDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    #通过该方法对响应对象进行拦截，篡改后使其返回动态加载之后的响应对象
    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest

        #由于我们只需要它处理板块内的响应对象，所以需要判断一下是不是需要处理的
        #response对应request，request对应url
        bro=spider.bro#获取了在爬虫类中定义的浏览器对象
        if request.url in spider.models_urls:
            bro.get(request.url)#不同板块所对应的url进行请求
            sleep(2)
            page_text=bro.page_source
            #针对定位到的这些response进行篡改
            #实例化一个新的响应对象，要包含动态加载出来的新闻内容
            new_response=HtmlResponse(url=request.url,body=page_text,encoding='utf-8',request=request)
            #我们需要用selenium来得到包含动态加载内容的
            #所以需要实例化一个浏览器对象
            #不可能每执行一次函数就实例化一次
            #所以去爬虫主文件里去写
            return new_response
        else:
            return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass
