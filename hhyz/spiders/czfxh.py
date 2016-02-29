# encoding=utf-8
import scrapy
import pymongo
from scrapy.http import Request
from ..items import ContentItem
from ..tools import get_img_path, is_low_price
import sys

reload(sys)
sys.setdefaultencoding("utf-8")
'''
超值分享惠的网站爬虫
网址:http://www.czfxh.com/
'''


class CzfxhSpider(scrapy.spiders.Spider):
    name = 'czfxh'
    allowed_domains = ['www.czfxh.com']
    start_urls = ['http://www.czfxh.com/']

    # 将访问过的url添加到数据库中
    def add_url(self, url):
        self.db[self.name].insert({'url': url})

    # 如果访问过该url就跳过
    def is_used_url(self, url):
        if self.db[self.name].find_one({'url': url}) != None:
            return True
        else:
            return False

    def parse_item(self, response):
        # 填充基本数据
        is_overseas=False
        item = ContentItem()
        if len(response.xpath('//h1[contains(@class,"soldOut")]')) != 0:  # 如果过期了,直接返回
            return item

        titles = response.xpath('//h2/text()').extract()[0]
        index = titles.rfind(' ')
        item['title'] = titles[0:index]
        item['special_title'] = titles[index + 1:]
        item['store'] = response.xpath('//div[contains(@class,"content")]/p/a/text()').extract()[0]
        classification = response.xpath('//a[contains(@rel,"category tag")]/text()').extract()
        if len(classification) != 0 and len(classification)==1:
            item['classification'] = self.mapping[classification[0]]
        else:
            is_overseas=True
            item['classification'] = self.mapping[classification[1]]
        # 处理链接
        item['link'] = response.xpath('//div[contains(@class,"buy_button")]/a/@href').extract()[0]
        # 处理图片
        img = response.xpath('//div[contains(@class,"post_thumb")]/a/img/@src').extract()[0]
        item['img'] = get_img_path(img)
        # 处理标签
        tags = response.xpath('//span[contains(@class,"tags")]/a/text()').extract()
        if len(tags) != 0:
            item['tags'] = tags
        # 处理内容
        content = ''
        list = response.xpath('//div[contains(@class,"content")]/p/text()').extract()
        for p in list:
            content += '<p>' + p + '</p>'
        img_path = response.xpath('//div[contains(@class,"content")]/p/img/@src').extract()[0]
        content += '<img src="' + img_path + '"  class="content-img"/>'
        item['content'] = content
        item['category']=u'国内优惠'
        if is_low_price(item['special_title']):
            item['category'] = u'白菜价'
        if is_overseas:
            item['category'] = u'海淘精选'
        item['from_name'] = u'超值分享惠'
        item['from_url'] = u'http://www.czfxh.com/'
        self.add_url(response.url)
        return item

    def parse(self, response):
        if not hasattr(self, 'client'):
            self.client = pymongo.MongoClient(self.settings.get("MONGO_URI"), self.settings.get("MONGO_PORT"))
            self.db = self.client[self.settings.get('MONGO_DB')]
        urls = response.xpath('//a[contains(@class,"title")]/@href').extract()
        for url in urls:
            if not self.is_used_url(url):
                yield Request(url, callback=self.parse_item)

    def close(self):
        self.client.close()  # 关闭连接

    mapping = {u'个护化妆': u'个护化妆',
               u'图书音像': u'图书音像',
               u'家用电器': u'家用电器',
               u'手机数码': u'电脑数码',
               u'日用百货': u'日用百货',
               u'服饰鞋包': u'服饰鞋包',
               u'海外精品': u'其他分类',
               u'电脑办公': u'电脑数码',
               u'钟表珠宝': u'礼品钟表',
               u'食品饮料': u'食品保健',
               }
