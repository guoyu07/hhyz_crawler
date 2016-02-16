# encoding=utf-8
import scrapy
from scrapy.contrib.loader import ItemLoader
from scrapy.selector import Selector
from scrapy.http import Request
from ..items import ContentItem
from ..imgtools import get_img_path
from BeautifulSoup import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
class SmzdmSpider(scrapy.spiders.Spider):
    name='smzdm'
    allowed_domains=['www.smzdm.com']
    start_urls=['http://www.smzdm.com/']
    file=open('content.txt','a')
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
            path=imglist[0]
            real_path=get_img_path(path)
            content+='<img src="'+real_path+'" width=400 height=300 class=""/>'
        self.file.write(content)
        item['content']=content
        #进行标签判断
        if not item.get('tags'):
            item['tags']=u''
        return item
    def parse(self,response):
        lists=response.xpath('//div[contains(@class,"leftWrap")]/div[contains(@class,"list")]/div/h4[contains(@class,"itemName")]/a/@href')
        for list in lists:
            yield Request(list.extract(),callback=self.parse_item)
