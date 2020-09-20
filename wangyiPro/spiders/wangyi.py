import scrapy
from selenium import webdriver
from wangyiPro.items import WangyiproItem


class WangyiSpider(scrapy.Spider):
    name = 'wangyi'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://news.163.com/']
    urls = []
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bro = webdriver.Chrome(executable_path=r'E:\python\my_spider\wangyiPro\chromedriver.exe')

    def parse(self, response, **kwargs):
        detail_url = response.xpath('//*[@id="index2016_wrap"]/div[1]/div[2]/div[2]/div[2]/div[2]/div/ul/li[4]/a/@href').extract_first()
        print('-------------------------1---------------------------------------------------')
        self.urls.append(detail_url)
        yield scrapy.Request(detail_url, callback=self.parse_detail)

    def parse_detail(self, response):
        div_list = response.xpath('/html/body/div/div[3]/div[4]/div[1]/div/div/ul/li/div/div')
        for div in div_list:
            title = div.xpath('./div/div[1]/h3/a/text()').extract_first()
            content_url = div.xpath('./div/div[1]/h3/a/@href').extract_first()
            print(title+'\n'+'==================================================2=================================')
            print(content_url)
            print('===================================================3===================================')

            item = WangyiproItem()
            item['title'] = title

            yield scrapy.Request(url=content_url, meta={'key': item}, callback=self.parse_content)

    def parse_content(self, response):
        content = response.xpath('//*[@id="endText"]//text()').extract()
        content = ''.join(content)
        print('=================================================4=============================================')
        item = response.meta['key']
        item['content'] = content
        yield item

    def close(self, spider):
        self.bro.close()
