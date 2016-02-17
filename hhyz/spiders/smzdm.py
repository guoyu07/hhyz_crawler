# encoding=utf-8
import scrapy
import pymongo
from scrapy.http import Request
from ..items import ContentItem
from ..imgtools import get_img_path
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
'''
什么值得买的网站爬虫
网址:http://www.smzdm.com/
'''

class SmzdmSpider(scrapy.spiders.Spider):
    name='smzdm'
    allowed_domains=['www.smzdm.com']
    start_urls=['http://www.smzdm.com/']
    file=open('content.txt','a')
    def __init__(self):
        super(SmzdmSpider,self).__init__()
        self.client=pymongo.MongoClient(self.settings.get("MONGO_URI"))
        self.db=self.client[self.settings.get('MONGO_DB')]
    #将访问过的url添加到数据库中
    def add_url(self,url):
        self.db[self.name].insert({'url':url})
    #如果访问过该url就跳过
    def is_used_url(self,url):
        if self.db[self.name].find_one({'url':url})!=None:
            return True
        else:
            return False
    def parse_item(self,response):
        # 填充基本数据
        item=ContentItem()
        item['img']=response.xpath('//a[contains(@class,"pic-Box")]/img/@src').extract()[0]
        item['title']=response.xpath('//h1[contains(@class,"article_title ")]/text()').extract()[0]
        item['special_title']=response.xpath('//h1[contains(@class,"article_title ")]/span/text()').extract()[0]
        item['link']=response.xpath('//div[contains(@class,"buy")]/a/@href[1]').extract()[0]
        item['tags']=response.xpath('//span[contains(@class,"tags")]/a/text()').extract()[0]
        item['store']=response.xpath('//div[contains(@class,"article_meta")][2]/span[1]/a/text()').extract()[0]
        #处理内容
        content=''
        list=response.xpath('//div[contains(@class,"inner-block")]/p/text()').extract()
        for p in list:
            content+='<p>'+p+'</p>'
        imglist=response.xpath('//div[contains(@class,"bigImgContent")]/img/@src').extract()
        if len(imglist)!=0:
            url=imglist[0]
            real_path=get_img_path(url)

            content+='<img src="'+real_path+'" width=400 height=300 class=""/>'
        self.file.write(content)
        item['content']=content
        #进行标签判断
        if not item.get('tags'):
            item['tags']=u''
        return item
    def parse(self,response):
        urls=response.xpath('//div[contains(@class,"leftWrap")]/div[contains(@class,"list")]/div/h4[contains(@class,"itemName")]/a/@href')
        for url in urls:
            if not self.is_used_url(url.extract()[0]):
                yield Request(url.extract(),callback=self.parse_item)

    def close(self):
        self.client.close()

