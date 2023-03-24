import scrapy
from selenium import webdriver
from tencent.items import TencentItem


class TencentSpider(scrapy.Spider):
    name = "tencent"
    allowed_domains = ["qq.com"]
    start_urls = ["https://www.qq.com/"]
    models_urls = []  # 存储相应板块对应详情页的url

    # 实例化一个浏览器对象
    def __init__(self):
        self.bro = webdriver.ChromiumEdge(executable_path='msedgedriver.exe')

    def parse(self, response):
        li_list = response.xpath('/html/body/div[1]/div[3]/div/ul/li')
        alist = [2,3]  # 所需要得财经、科技板块所在位置
        for index in alist:
            model_url = li_list[index].xpath('./a/@href').extract_first()
            self.models_urls.append(model_url)

        # 依次对每一个板块对应的页面进行请求
        for url in self.models_urls:  # 对每一个板块url进行请求发送
            yield scrapy.Request(url, callback=self.parse_model)

    # 每个板块的新闻都是动态加载出来的，所以必须要处理response
    def parse_model(self, response):  # 解析每一个板块页面中对应的新闻内容的url
        li_list = response.xpath('/html/body/div[1]/div[4]/div[2]/div/div/ul/li')
        for li in li_list:
            news_detail = li.xpath('./div/h3/a/@href').extract_first()
            # 对新闻的具体内容发出请求
            yield scrapy.Request(url=news_detail, callback=self.parse_detail())

    def parse_detail(self, response):  # 解析新闻内容
        content = response.xpath('/html/body/div[3]/div[1]/div[1]/div[2]//text()').extract()
        content = ''.join(content)
        item = TencentItem()
        item['content'] = content
        yield item

    def closed(self, spider):
        self.bro.quit()
