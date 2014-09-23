#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import os
import sys

sys.path.append(os.path.dirname(os.path.split(os.path.realpath(__file__))[0]))

from lib.stock  import StockInfo
from lib.indicator import Indicator
from conf.settings import TECH_ANALY_IND,DIRECTION_LIST,TRADE_PRICE_ORDER_LIST
from model.stock_data import StockData
from lib.stock import StockPool
      
        


class StockPoolBuilder(object):
    def __init__(self, stock_condition, indicator_list, start):
        self._stock_condition = stock_condition
        self._indicator_list = indicator_list
        self._start = start
        self._sp_start = ''
        self._sp_end = ''
        self._stock_list = self.generate_stock_list()
        #self._sp = StockPool(self._stock_list,start,end)
        
    def generate_stock_pool_start_end(self):
        self._sp_end = self._stock_condition['date']
        self._sp_start = self.generate_sp_start(self, start, indicator_list)
        
    def generate_sp_start(self, start, indicator_list):
        pass
        
    def generate_stock_list(self,):
        date = self._stock_condition['date']
        conditions = self._stock_condition['condition']
        stock_list = StockData.mgr().generate_stock_list_by_condition(date,conditions)[:]
        return stock_list
        
    def build_stock_pool(self):
        pass
    
if __name__ == '__main__':
    now = datetime.datetime.now()
    yest = now.date() - datetime.timedelta(days=1)
    print yest
    stock_condition = {'date':yest,'condition':[{'item':'Close','min':15.0,'max':25.0},
                                                 {'item':'Volume','min':1000000,'max':''}]}
    indicator_list = ['MA5']
    start = yest
    spb = StockPoolBuilder(stock_condition,indicator_list,start)
    sp = spb.build_stock_pool()
    
    
    
    
    
    
    
    
    