# encoding=utf-8
import scrapy
import pymongo
from scrapy.http import Request
from ..items import ContentItem
from ..tools import get_img_path,is_low_price
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
        if len(response.xpath('//h1[contains(@class,"soldOut")]'))!=0:#如果过期了,直接返回
            return item
        item['title']=response.xpath('//h1[contains(@class,"article_title ")]/text()').extract()[0]
        item['special_title']=response.xpath('//h1[contains(@class,"article_title ")]/span/text()').extract()[0]
        item['store']=response.xpath('//div[contains(@class,"article_meta")][2]/span[1]/a/text()').extract()[0]
        classification=response.xpath('//span[contains(@itemprop,"title")][2]/text()').extract()
        if len(classification)!=0:
            item['classification']=classification[0]
        #处理链接
        link=response.xpath('//div[contains(@class,"buy")]/a/@href[1]').extract()
        if len(link)!=0:
            item['link']=link[0]
        #处理图片
        img=response.xpath('//div[contains(@class,"article-top-box clearfix")]/a/img/@src').extract()[0]
        item['img']=get_img_path(img)
        #处理标签
        tags=response.xpath('//span[contains(@class,"tags")]/a/text()').extract()
        if len(tags)!=0:
            item['tags']=tags[0]
        #处理内容
        content=''
        list=response.xpath('//div[contains(@class,"inner-block")]/p/text()').extract()
        for p in list:
            content+='<p>'+p+'</p>'
        imglist=response.xpath('//div[contains(@class,"bigImgContent")]//img/@src').extract()
        if len(imglist)!=0:
            url=imglist[0]
            real_path=get_img_path(url)
            content+='<img src="'+real_path+'"  class="content-img"/>'
        else:
            real_path=get_img_path(item['img'])
            content+='<img src="'+real_path+'" class="content-img"/>'

        item['content']=content
        item['category']=response.xpath('//div[contains(@class,"yhjingxuan")]/span/text()').extract()[0]
        if is_low_price(item['special_title']):
            item['category']=u'白菜价'
        item['from_name']=u'什么值得买'
        item['from_url']=u'http://www.smzdm.com/'
        self.add_url(response.url)
        return item
    def parse(self,response):
        if not hasattr(self,'client'):
            self.client=pymongo.MongoClient(self.settings.get("MONGO_URI"),self.settings.get("MONGO_PORT"))
            self.db=self.client[self.settings.get('MONGO_DB')]
        urls=response.xpath('//div[contains(@class,"leftWrap")]/div[contains(@class,"list")]/div/h4[contains(@class,"itemName")]/a/@href')
        for url in urls:
            if not self.is_used_url(url.extract()):
                yield Request(url.extract(),callback=self.parse_item)

    def close(self):
        self.client.close()#关闭连接

