# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime

import dataset

from pytz import timezone

class StorePipeline(object):
    def __init__(self, sqlite_url, authors_table, articles_table, names_table,
                 my_timezone):
        self.sqlite_url = sqlite_url
        self.authors_table = authors_table
        self.articles_table = articles_table
        self.names_table = names_table
        self.dt = datetime.now(timezone(my_timezone)).replace(
            microsecond=0).isoformat()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            sqlite_url=crawler.settings.get('SQLITE_URL'),
            authors_table=crawler.settings.get('SQLITE_AUTHORS_TABLE'),
            articles_table=crawler.settings.get('SQLITE_ARTICLES_TABLE'),
            names_table=crawler.settings.get('SQLITE_NAMES_TABLE'),
            my_timezone=crawler.settings.get('TIMEZONE')
        )

    def open_spider(self, spider):
        self.db = dataset.connect(self.sqlite_url)

    def get_gender(self, author):
        name_table = self.db[self.names_table]
        name = author.split()[0]
        transform_tuples = [('á', 'a'), ('é', 'e'), ('í', 'i'), ('ó', 'o'),
                            ('ú', 'u'), ('ñ', 'n'), ('Á', 'A'), ('É', 'E'),
                            ('Í', 'I'), ('Ó', 'O'), ('Ú', 'U'), ('Ñ', 'N')]
        name_no_accents = name
        for x, y in transform_tuples:
            if x in name_no_accents:
                name_no_accents = name_no_accents.replace(x, y)



        if name_table.count(name=name) == 0 and name_table.count(
                name=name_no_accents) == 0:
            return None
        elif name_table.count(name=name) == 1:
            return name_table.find_one(name=name)['gender']
        else:
            return name_table.find_one(name=name_no_accents)['gender']

    def process_item(self, item, spider):
        """
        Store data to DB
        """
        # stores author if new
        author_table = self.db[self.authors_table]

        author = item['author'][0].strip()
        item.pop('author')

        count_asterisks = 0
        for char in author[::-1]:
            if char == '*':
                count_asterisks += 1
        if count_asterisks > 0:
            author = author[0:-count_asterisks]
        author = author.strip()

        if ' y ' in author:
            gender = '+'
        else:
            gender = self.get_gender(author)

        if author_table.count(author=author) == 0:
            author_item = dict()
            author_item['author'] = author
            author_item['gender'] = gender
            author_table.insert_ignore(author_item, ['author'])

            # create flag file for DM, currently not in use
            if gender is None or gender == 'A':
                open('dmneeded2.flag', 'a').close()
            else:
                open('dmnotneeded.flag', 'a').close()

        item['author_id'] = author_table.find_one(author=author)['id']

        # stores article if new
        article_table = self.db[self.articles_table]
        item['title'] = item['title'][0]
        item['url'] = item['url'][0]
        item['site'] = spider.name
        item['added'] = self.dt
        article_table.insert_ignore(item, ['author_id', 'site', 'url'])

        # updates last_seen if article exists
        item['last_seen'] = self.dt
        article_table.update(dict(author_id=item['author_id'],
                                  site=item['site'],
                                  url=item['url'],
                                  last_seen=item['last_seen']),
                             ['author_id', 'site', 'url'])

        return item


class StoreNames(object):
    # pipeline to create name DB used by "nombres.py" spider
    def __init__(self, sqlite_url, names_table):
        self.sqlite_url = sqlite_url
        self.names_table = names_table

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            sqlite_url=crawler.settings.get('SQLITE_URL'),
            names_table=crawler.settings.get('SQLITE_NAMES_TABLE'),
        )

    def open_spider(self, spider):
        self.db = dataset.connect(self.sqlite_url)

    def process_item(self, item, spider):
        table = self.db[self.names_table]
        item['name'] = item['name']
        item['gender'] = item['gender']
        table.insert_ignore(item, ['name'])
        return item
