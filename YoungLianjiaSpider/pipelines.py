# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pandas as pd
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

class ToCsvPipeline(object):
    def __init__(self):
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        try:
            self.df = pd.read_csv('data/xiaoqu.csv')
            self.colums = self.df.columns
        except Exception as e:
            print(e)
            self.df = None
            self.colums = ["id","url","name",'address','sold_count',
                              'selling_count','renting_count','house_type','property_costs',
                              'property_company','developer','buiding_count','door_count']
        self.datas = []

    def process_item(self, item, spider):
        if self.query_item(item):
            if item['unit_price_desc'] != self.colums[-1]:
                self.colums.append(item['unit_price_desc'])
                self.update_item(item)
            else:
                print('Skip {0}'.format(item['name']))
        else:
            self.insert_item(item)
        return item

    def spider_closed(self, spider):
        if self.datas != None and len(self.datas) > 0:
            new_data = pd.DataFrame(self.datas)
            new_data.to_csv('data/xiaoqu.csv', header=self.colums, index=True)
        print('end ')

    def query_item(self,item):
        return isinstance(self.df,pd.DataFrame) and self.df['id'].isin([item['id']]).any()


    def update_item(self,item):
        old = self.df.loc(self.df['id'].isin([item['id']]))
        data = []
        for k in self.colums:
            if k == self.colums[-1]:
                data.append(item['unit_price'])
            try:
                data.append(item[k])
            except:
                data.append(old[k])
        self.datas.append(data)
        pass


    def insert_item(self,item):
        data = []
        for k in self.colums:
            try:
                data.append(item[k])
            except:
                if k == self.colums[-1]:
                    data.append(item['unit_price'])
                else:
                    data.append(-1)
        self.datas.append(data)
        print(self.datas)