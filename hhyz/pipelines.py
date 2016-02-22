# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
from scrapy.exceptions import DropItem
class ItemFilterPipeline(object):
    def process_item(self, item, spider):
        if item.get('title')==None or item.get('img')==None or \
            item.get('special_title')==None or item.get('content')==None \
            or item.get('link')==None or item.get('classification')==None or item.get('category')==None:
            raise DropItem('drop a item ',item)
        if item.get('tags')==None:
            item['tags']=u''
        return item

class ItemSavePipeline(object):
    def __init__(self, host, username,passwd,port,db):
        self.host=host
        self.username=username
        self.passwd=passwd
        self.port=port
        self.db=db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            username=crawler.settings.get('MYSQL_USERNAME'),
            passwd=crawler.settings.get('MYSQL_PASSWD'),
            port=crawler.settings.get('MYSQL_PORT'),
            db=crawler.settings.get('MYSQL_DB')
        )

    def open_spider(self, spider):
        self.conn=MySQLdb.connect(host=self.host,
                     port=self.port,
                     user=self.username,
                     passwd=self.passwd,
                     db=self.db)


    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        cur=self.conn.cursor()
        try:
            cur.execute('select id from classification where name=%s',[item['classification']])
            _id=cur.fetchone()[0]
            cur.execute('insert into posts(title,special_title,tags,link,content,category,img,store,from_name,'
                        'from_url,classification_id,up,down,timestamp) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW())',
                        [item['title'],item['special_title'],item['tags'],item['link'],item['content'],
                         item['category'],item['img'],item['store'],item['from_name'],item['from_url'],_id,0,0]);
            cur.close()
            self.conn.commit()
        except Exception,e:
            print e
            self.conn.rollback()

