# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XiaoquItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    address = scrapy.Field()
    unit_price = scrapy.Field()
    sold_count = scrapy.Field()
    selling_count = scrapy.Field()
    renting_count = scrapy.Field()
    house_type = scrapy.Field()
    property_costs = scrapy.Field()
    property_company = scrapy.Field()
    developer = scrapy.Field()
    buiding_count = scrapy.Field()
    door_count = scrapy.Field()
    unit_price_desc = scrapy.Field()
