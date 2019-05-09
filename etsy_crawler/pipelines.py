# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import pymongo


# from redis import StrictRedis


class EtsyCrawlerPipeline(object):
    def process_item(self, item, spider):
        return item

class ScreenShotPipeline(object):

    def process_item(self, item, spider):
        file_path = r'/home/fu/crawler_project/etsy_crawler/screen_shot/' + item['id'] + '.png'
        ScreenShot = dict(item).pop('screenshot')
        with open(file_path, "wb") as f:  # w is write mode and b is binary mode
            f.write(ScreenShot)
            return item


class MyEstyImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for i, image_url in enumerate(item['image_urls']):
            yield scrapy.Request(image_url,
                                 headers={'Referer': 'https://www.etsy.com/c/jewelry?explicit=1'},
                                 meta={'filename': item['id'] + '_0' + str(i)}     # filename field is pass to file_path for naming each image file
                                 )

    '''
    These requests will be processed by the 
    pipeline and, when they have finished downloading, 
    the results will be sent to the item_completed() method, 
    as a list of 2-element tuples. Each tuple will contain 
    (success, file_info_or_error) 
    '''

    def item_completed(self, results, item, info):
        # ok is referred success , if ok means for ok to be true , while x is referred the file_info_or_error
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item

    def file_path(self, request, response=None, info=None):
        return request.meta.get('filename', '')

class MongoPipeline(object):
    """
    write items to Mongodb
    """

    def __init__(self, mongo_url, mongo_db, mongo_collection):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db
        self.mongo_collection = mongo_collection

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_url=crawler.settings.get('MONGO_URL'),
            mongo_db=crawler.settings.get('MONGO_DATABASE'),
            mongo_collection=crawler.settings.get('MONGO_COLLECTION')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]

    def close_spider(self,spider):
        self.client.close()

    def process_item(self, item, spider):
        d = dict(item)
        del d['screenshot']
        self.db[self.mongo_collection].insert_one(d)
        return item



"""
Alternatively , We can write itmes to Redis in the local machine 

class RedisPipeline(object):

    def __init__(self, port, db):
        self.port = port
        self.db = db

    def from_crawler(cls, crawler):
        redis_port = crawler.settings.get('REDIS_PORT')
        redis_db = crawler.settings.get('REDIS_DUP_DB')

        return cls(redis_port, redis_db)

    def open_spider(self, spider):
        self.redis = StrictRedis(port=self.port, db=self.db)

    def process_item(self, item, spider):
        item_dict = dict(item)
        name = item_dict.pop('id')
        self.redis.hmset(name,item_dict)
        return item
"""
