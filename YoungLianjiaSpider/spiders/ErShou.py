# -*- coding: utf-8 -*-
import scrapy
import pandas as pd

class ErshouSpider(scrapy.Spider):
    name = 'ErShou'
    allowed_domains = ['hrb.lianjia.com']
    start_urls = [ 'https://hrb.lianjia.com/ershoufang/c{0}'.format(x) for x in pd.read_csv('data/xiaoqu.csv').id.as_matrix()]
    selling_index = 0

    def parse(self, response):
        total_selling = response.xpath('//*[@class="leftContent"]/div[@class="resultDes clear"]/h2/span/text()').extract_first()
        url = 'https://hrb.lianjia.com/ershoufang/pg{0}'.format(1) + response.url.split('/')[-2]
        yield scrapy.Request(url=url,meta={'total_selling':int(total_selling)},callback=self.paser_xiaoqu)


    def paser_xiaoqu(self,response):

        url_list = response.xpath('//*[@class="sellListContent"]/li/div[@class="info clear"]/div[@class="title"]/a/@href').extract()

        for i in url_list:
            self.selling_index += 1
            yield scrapy.Request(url=i,callback=self.paser_house)

        if self.selling_index < response.meta['total_selling']:
            page_index = int(self.selling_index / 30) + 1
            url = 'https://hrb.lianjia.com/ershoufang/pg{0}'.format(page_index) + response.url.split('/')[-2]
            yield scrapy.Request(url=url,meta={'total_selling':response.meta['total_selling']}, callback=self.paser_xiaoqu)

    def paser_house(self,response):
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