# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
from scrapy.exceptions import DropItem

import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi

class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['asin'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['asin'])
            return item

'''
class JsonWriterPipeline(object):

    def __init__(self):
        self.file = codecs.open('amaz_data_utf8.json', 'wb', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + ",\n"
        self.file.write(line)
        return item

'''
class AmazPipeline(object):

    def __init__(self):
        self.file = codecs.open('amaz_data_utf8.json', 'wb', encoding='utf-8')
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
            db = 'amaz',
            user = 'root',
            passwd = 'shuaiwei',
            cursorclass = MySQLdb.cursors.DictCursor,
            charset = 'utf8',
            use_unicode = False
        )

    def process_item(self, item, spider):

        line = json.dumps(dict(item)) + ',\n'
        # print line
        self.file.write(line.decode("unicode_escape"))

        query = self.dbpool.runInteraction(self._conditional_insert, item)


        return item

    def _conditional_insert(self, tx, item):
        tx.execute('insert into price(asin,title,price) values (%s, %s, %s)', (item['asin'], item['title'], item['price']))

'''
class SQLPipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
            db = 'amaz',
            user = 'root',
            passwd = 'shuaiwei',
            cursorclass = MySQLdb.cursors.DictCursor,
            charset = 'utf8',
            use_unicode = False
        )
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        return item

    def _conditional_insert(self, tx, item):
        if item.get('title'):
            for i in range(len(item['title'])):
                tx.execute('insert into book values (%s, %s)', (item['title'][i], item['link'][i]))
'''