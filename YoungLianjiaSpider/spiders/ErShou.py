# -*- coding: utf-8 -*-
import scrapy
import pandas as pd

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
        title = response.xpath('//*[@class="sellDetailHeader"]/div/div/div[@class="title"]/h1/text()').extract_first()
        sub_title = response.xpath('//*[@class="sellDetailHeader"]/div/div/div[@class="title"]/div/text()').extract_first()
        total_price = response.xpath('//*[@class="overview"]/div[@class="content"]/div[@class="price "]/span[@class="total"]/text()').extract_first()
        unit_price = response.xpath('//*[@class="overview"]/div[@class="content"]/div[@class="price "]/div[@class="text"]/div[@class="unitPrice"]/span/text()').extract_first()
        community_name = response.xpath('//*[@class="aroundInfo"]/div[@class="communityName"]/a/text()').extract_first()
        area_name = ' '.join(response.xpath('//*[@class="aroundInfo"]/div[@class="areaName"]/span[@class="info"]/a/text()').extract())
        base_info_values = response.xpath('//*[@id="introduction"]/div/div[@class="introContent"]/div[@class="base"]/div[@class="content"]/ul/li/text()').extract()
        base_info_keys = response.xpath('//*[@id="introduction"]/div/div[@class="introContent"]/div[@class="base"]/div[@class="content"]/ul/li/span/text()').extract()

        transaction_info_values = response.xpath('//*[@id="introduction"]/div/div[@class="introContent"]/div[@class="transaction"]/div[@class="content"]/ul/li/span[2]/text()').extract()
        transaction_info_keys = response.xpath('//*[@id="introduction"]/div/div[@class="introContent"]/div[@class="transaction"]/div[@class="content"]/ul/li/span[1]/text()').extract()
        pass

    def paser_sold_house(self,response):

        title = response.meta['title']
        deal_date = response.meta['deal_date']
        deal_price = response.xpath('//*[@class="wrapper"]/div[@class="overview"]/div[@class="info fr"]/div[@class="price"]/span[@class="dealTotalPrice"]/i/text()').extract_first()
        unit_price = response.xpath('//*[@class="wrapper"]/div[@class="overview"]/div[@class="info fr"]/div[@class="price"]/b/text()').extract_first()

        pass