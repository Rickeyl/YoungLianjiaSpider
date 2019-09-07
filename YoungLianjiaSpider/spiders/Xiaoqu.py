# -*- coding: utf-8 -*-
import scrapy


class XiaoquSpider(scrapy.Spider):
    name = 'Xiaoqu'
    allowed_domains = ['hrb.lianjia.com']
    start_urls = ['http://hrb.lianjia.com/']

    def parse(self, response):
        pass
