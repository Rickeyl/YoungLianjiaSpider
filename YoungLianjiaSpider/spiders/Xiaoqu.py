# -*- coding: utf-8 -*-
import scrapy
from YoungLianjiaSpider.items import XiaoquItem

class XiaoquSpider(scrapy.Spider):
    name = 'Xiaoqu'
    allowed_domains = ['hrb.lianjia.com']
    base_url = 'https://hrb.lianjia.com/xiaoqu/pg{0}'
    start_urls = [base_url.format(1)]
    total_number = 0
    index = 0
    def parse(self, response):
        self.total_number = int(response.xpath('//*[@class="total fl"]/span/text()').extract_first())

        xiaoqu_list = response.xpath('//*[@class="listContent"]/li/div[@class="info"]/div[@class="title"]/a/@href').extract()
        sold90day_count_list = response.xpath('//*[@class="listContent"]/li/div[@class="info"]/div[@class="houseInfo"]/a[1]/text()').extract()
        renting_count_list = response.xpath('//*[@class="listContent"]/li/div[@class="info"]/div[@class="houseInfo"]/a[2]/text()').extract()
        selling_count_list = response.xpath('//*[@class="listContent"]/li/div[@class="xiaoquListItemRight"]/div[@class="xiaoquListItemSellCount"]/a/span/text()').extract()

        for i,url in enumerate(xiaoqu_list):
            meta = {'sold90day_count':sold90day_count_list[i],
                    'renting_count':renting_count_list[i],
                    'selling_count':selling_count_list[i],
                    'url': url,
                    'id':url.split('/')[-2]}
            self.index += 1
            yield scrapy.Request(url=url,meta=meta,callback=self.xiaoqu_parse)

        if self.index < self.total_number:
            page_index = int(self.index / 30) + 1
            yield scrapy.Request(url=self.base_url.format(page_index), callback=self.parse)

    def xiaoqu_parse(self,response):
        item = XiaoquItem()
        item['name'] = response.xpath('//*[@class="xiaoquDetailHeader"]/div/div/*[@class="detailTitle"]/text()').extract_first()
        item['address'] = response.xpath('//*[@class="xiaoquDetailHeader"]/div/div/*[@class="detailDesc"]/text()').extract_first()
        unit_price = response.xpath('//*[@class="xiaoquOverview"]/div[@class="xiaoquDescribe fr"]/div[@class="xiaoquPrice clear"]/div/span[1]/text()').extract_first()
        unit_price_desc = response.xpath('//*[@class="xiaoquOverview"]/div[@class="xiaoquDescribe fr"]/div[@class="xiaoquPrice clear"]/div/span[2]/text()').extract_first()
        item['unit_price'] = unit_price_desc + unit_price+'元/m'
        info_label = response.xpath('//*[@class="xiaoquInfo"]/div[@class="xiaoquInfoItem"]/span[@class="xiaoquInfoLabel"]/text()').extract()
        info_content = response.xpath(
            '//*[@class="xiaoquInfo"]/div[@class="xiaoquInfoItem"]/span[@class="xiaoquInfoContent"]/text()').extract()

        item['house_type'] = info_content[0]
        item['property_costs'] = info_content[1]
        item['property_company'] = info_content[2]
        item['developer'] = info_content[3]
        item['buiding_count'] = info_content[4]
        item['door_count'] = info_content[5]

        item['sold_count'] = response.meta['sold90day_count']
        item['renting_count'] = response.meta['renting_count']
        item['selling_count'] = response.meta['selling_count']

        item['url'] = response.meta['url']
        item['id'] = response.meta['id']
        return item

