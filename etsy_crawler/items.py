# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class EtsyCrawlerItem(Item):
    # define the fields for your item here like:
    product_name = Field()
    link = Field()
    image_urls = Field()
    images = Field()
    image_paths = Field()
    shop = Field()
    price = Field()
    shipping_fee_to_cali = Field()
    screenshot = Field()
    id = Field()



