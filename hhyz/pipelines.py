# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb

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
            port=crawler.settings.get('MYSQL_DB'),
            db=crawler.settings.get('MYSQL_PORT')
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
        cur.execute('insert into users(title,special_title,tags,link,content,categories,img,store)'
                    ' values(%s,%s,%s,%s,%s,%s,%s,%s,)',
                    [item['title'],item['special_title'],item['tags'],item['link'],item['content'],
                     item['categories'],item['img'],item['store'],]);
        cur.close()
        self.conn.commit()


