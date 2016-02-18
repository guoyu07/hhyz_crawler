# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ContentItem(scrapy.Item):
    title = scrapy.Field()#标题
    special_title = scrapy.Field()#特殊标题
    tags = scrapy.Field()#标签
    link = scrapy.Field()#链接
    content = scrapy.Field()#内容
    categories = scrapy.Field()#分类
    img=scrapy.Field()#文章图片
    store=scrapy.Field()#商城
    from_name=scrapy.Field()#来自网站
    from_url=scrapy.Field()#来自网址



