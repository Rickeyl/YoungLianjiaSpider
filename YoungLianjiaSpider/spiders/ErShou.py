# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
from YoungLianjiaSpider.items import SellingHouseItem,SoldHouseItem

class ErshouSpider(scrapy.Spider):
    name = 'ErShou'
    allowed_domains = ['hrb.lianjia.com']
    # start_urls = [ 'https://hrb.lianjia.com/ershoufang/c{0}'.format(x) for x in pd.read_csv('data/xiaoqu.csv').id.as_matrix()]
    start_urls = ['https://hrb.lianjia.com/xiaoqu/{0}/'.format(x) for x in pd.read_csv('data/xiaoqu.csv').id.as_matrix()]
    selling_index = 0
    sold_index = 0

    def parse(self, response):

        selling_url = 'https://hrb.lianjia.com/ershoufang/pg{0}c'.format(1) + response.url.split('/')[-2]
        yield scrapy.Request(url=selling_url, callback=self.paser_selling_list)

        sold_url = 'https://hrb.lianjia.com/chengjiao/pg{0}c'.format(1) + response.url.split('/')[-2]
        yield scrapy.Request(url=sold_url, callback=self.paser_sold_list)


    def paser_selling_list(self,response):
        total_selling = int(response.xpath('//*[@class="leftContent"]/div[@class="resultDes clear"]/h2/span/text()').extract_first())
        url_list = response.xpath('//*[@class="sellListContent"]/li/div[@class="info clear"]/div[@class="title"]/a/@href').extract()

        for url in url_list:
            self.selling_index += 1
            yield scrapy.Request(url=url,callback=self.paser_selling_house)

        if self.selling_index < total_selling:
            page_index = int(self.selling_index / 30) + 1
            url = 'https://hrb.lianjia.com/ershoufang/pg{0}c'.format(page_index) + response.url.split('/')[-2]
            yield scrapy.Request(url=url, callback=self.paser_selling_list)

    def paser_sold_list(self,response):
        total_sold = int(response.xpath('//*[@class="leftContent"]/div[@class="resultDes clear"]/div[@class="total fl"]/span/text()').extract_first())
        url_list = response.xpath('//*[@class="listContent"]/li/div[@class="info"]/div[@class="title"]/a/@href').extract()
        title_list = response.xpath('//*[@class="listContent"]/li/div[@class="info"]/div[@class="title"]/a/text()').extract()
        deal_date_list = response.xpath('//*[@class="listContent"]/li/div[@class="info"]/div[@class="address"]/div[@class="dealDate"]/text()').extract()
        for i,url in enumerate(url_list):
            self.sold_index += 1
            yield scrapy.Request(url=url,meta={'title':title_list[i],'deal_date':deal_date_list[i]},callback=self.paser_sold_house)

        if self.sold_index < total_sold:
            page_index = int(self.sold_index / 30) + 1
            url = 'https://hrb.lianjia.com/chengjiao/pg{0}c'.format(page_index) + response.url.split('/')[-2]
            yield scrapy.Request(url=url, callback=self.paser_sold_list)

    def paser_selling_house(self,response):
        item = SellingHouseItem()
        item['title'] = response.xpath('//*[@class="sellDetailHeader"]/div/div/div[@class="title"]/h1/text()').extract_first()
        item['sub_title'] = response.xpath('//*[@class="sellDetailHeader"]/div/div/div[@class="title"]/div/text()').extract_first()
        item['total_price'] = response.xpath('//*[@class="overview"]/div[@class="content"]/div[@class="price "]/span[@class="total"]/text()').extract_first()
        item['unit_price'] = response.xpath('//*[@class="overview"]/div[@class="content"]/div[@class="price "]/div[@class="text"]/div[@class="unitPrice"]/span/text()').extract_first()
        item['community_name'] = response.xpath('//*[@class="aroundInfo"]/div[@class="communityName"]/a/text()').extract_first()
        item['area_name'] = ' '.join(response.xpath('//*[@class="aroundInfo"]/div[@class="areaName"]/span[@class="info"]/a/text()').extract())

        base_info_values = response.xpath('//*[@id="introduction"]/div/div[@class="introContent"]/div[@class="base"]/div[@class="content"]/ul/li/text()').extract()
        base_info_keys = response.xpath('//*[@id="introduction"]/div/div[@class="introContent"]/div[@class="base"]/div[@class="content"]/ul/li/span/text()').extract()

        item['house_type'] = base_info_values[0]
        item['house_floor'] = base_info_values[1]
        item['house_area'] = base_info_values[2]
        item['house_structure'] = base_info_values[3]
        item['used_area'] = base_info_values[4]
        item['building_type'] = base_info_values[5]
        item['house_direction'] = base_info_values[6]
        item['building_structure'] = base_info_values[7]
        item['ren_condition'] = base_info_values[8]
        item['ladder_ratio'] = base_info_values[9]
        item['is_elevator'] = base_info_values[10]
        item['property_age'] = base_info_values[11]

        transaction_info_values = response.xpath('//*[@id="introduction"]/div/div[@class="introContent"]/div[@class="transaction"]/div[@class="content"]/ul/li/span[2]/text()').extract()
        transaction_info_keys = response.xpath('//*[@id="introduction"]/div/div[@class="introContent"]/div[@class="transaction"]/div[@class="content"]/ul/li/span[1]/text()').extract()

        item['listing_time'] = transaction_info_values[0]
        item['transaction_authority'] = transaction_info_values[1]
        item['last_transaction'] = transaction_info_values[2]
        item['house_purposes'] = transaction_info_values[3]
        item['house_age'] = transaction_info_values[4]
        item['house_ownership'] = transaction_info_values[5]
        item['mortgage_info'] = transaction_info_values[6]
        item['room_parts'] = transaction_info_values[7]

        return item

    def paser_sold_house(self,response):

        item = SoldHouseItem()

        item['title'] = response.meta['title']
        item['deal_date'] = response.meta['deal_date']
        item['deal_price'] = response.xpath('//*[@class="wrapper"]/div[@class="overview"]/div[@class="info fr"]/div[@class="price"]/span[@class="dealTotalPrice"]/i/text()').extract_first()
        item['unit_price'] = response.xpath('//*[@class="wrapper"]/div[@class="overview"]/div[@class="info fr"]/div[@class="price"]/b/text()').extract_first()

        item['msg_list'] = response.xpath('//*[@class="wrapper"]/div[@class="overview"]/div[@class="info fr"]/div[@class="msg"]/span/label/text()').extract()

        base_info_values = response.xpath(
            '//*[@id="introduction"]/div[@class="introContent"]/div[@class="base"]/div[@class="content"]/ul/li/text()').extract()
        base_info_keys = response.xpath(
            '//*[@id="introduction"]/div[@class="introContent"]/div[@class="base"]/div[@class="content"]/ul/li/span/text()').extract()

        item['house_type'] = base_info_values[0]
        item['house_floor'] = base_info_values[1]
        item['house_area'] = base_info_values[2]
        item['house_structure'] = base_info_values[3]
        item['used_area'] = base_info_values[4]
        item['building_type'] = base_info_values[5]
        item['house_direction'] = base_info_values[6]
        item['house_age'] = base_info_values[7]
        item['ren_condition'] = base_info_values[8]
        item['building_structure'] = base_info_values[9]
        item['heating_method'] = base_info_values[10]
        item['ladder_ratio'] = base_info_values[11]
        item['property_age'] = base_info_values[12]
        item['is_elevator'] = base_info_values[13]

        transaction_info_values = response.xpath(
            '//*[@id="introduction"]/div[@class="introContent"]/div[@class="transaction"]/div[@class="content"]/ul/li/text()').extract()
        transaction_info_keys = response.xpath(
            '//*[@id="introduction"]/div[@class="introContent"]/div[@class="transaction"]/div[@class="content"]/ul/li/span/text()').extract()

        item['lianjia_id'] = transaction_info_values[0]
        item['transaction_authority'] = transaction_info_values[1]
        item['listing_time'] = transaction_info_values[2]
        item['house_purposes'] = transaction_info_values[3]
        item['house_ownership'] = transaction_info_values[4]

        return item