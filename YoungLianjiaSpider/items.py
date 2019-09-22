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

class SellingHouseItem(scrapy.Item):
    title = scrapy.Field()
    sub_title = scrapy.Field()
    total_price = scrapy.Field()
    unit_price = scrapy.Field()
    community_name = scrapy.Field()
    area_name = scrapy.Field()

    house_type = scrapy.Field()
    house_floor = scrapy.Field()
    house_area = scrapy.Field()
    house_structure = scrapy.Field()
    used_area = scrapy.Field()
    building_type = scrapy.Field()
    house_direction = scrapy.Field()
    ren_condition = scrapy.Field()
    building_structure = scrapy.Field()
    ladder_ratio = scrapy.Field()
    property_age = scrapy.Field()
    is_elevator = scrapy.Field()

    listing_time = scrapy.Field()
    transaction_authority = scrapy.Field()
    last_transaction = scrapy.Field()
    house_purposes = scrapy.Field()
    house_age = scrapy.Field()
    house_ownership = scrapy.Field()
    mortgage_info = scrapy.Field()
    room_parts = scrapy.Field()


class SoldHouseItem(scrapy.Item):
    title = scrapy.Field()
    deal_date = scrapy.Field()
    deal_price = scrapy.Field()
    unit_price = scrapy.Field()
    msg_list = scrapy.Field()

    house_type = scrapy.Field()
    house_floor = scrapy.Field()
    house_area = scrapy.Field()
    house_structure = scrapy.Field()
    used_area = scrapy.Field()
    building_type = scrapy.Field()
    house_direction = scrapy.Field()
    house_age = scrapy.Field()
    ren_condition = scrapy.Field()
    building_structure = scrapy.Field()
    heating_method = scrapy.Field()
    ladder_ratio = scrapy.Field()
    property_age = scrapy.Field()
    is_elevator = scrapy.Field()

    lianjia_id = scrapy.Field()
    transaction_authority = scrapy.Field()
    listing_time = scrapy.Field()
    house_purposes = scrapy.Field()
    house_ownership = scrapy.Field()
