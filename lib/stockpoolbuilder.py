#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import os
import sys
import re

sys.path.append(os.path.dirname(os.path.split(os.path.realpath(__file__))[0]))

from lib.stock  import StockInfo
from lib.indicator import Indicator
from model.stock_data import StockData
from lib.stock import StockPool

class StockPoolBuilder(object):
    def __init__(self, stock_condition, indicator_list, start, end):
        self._stock_condition = stock_condition
        self._indicator_list = indicator_list
        self._start = start
        self._sp_start = self.generate_sp_start(self._start, self._indicator_list)
        self._sp_end = end
        self._stock_list = self.generate_stock_list()
        self._sp = ''
        self._ind = ''
    
    def count_stock_num(self):
        return len(self._stock_list)
    
 #   def generate_stock_pool_start_end(self):
 #       #self._sp_end = self._stock_condition['date']
 #       #self._sp_start = self.generate_sp_start(self._start, indicator_list)
 #       return self.generate_sp_start(self._start, self._indicator_list), self._stock_condition['end']
        
    def generate_sp_start(self, start, indicator_list):
        '''
        find max days number in indicator_list and Multiplied by 2
        '''
        
        delta_day = self.find_max_day(indicator_list)*2
        return start - datetime.timedelta(days=delta_day)
        
    def find_max_day(self, indicator_list):
        max_day = 0
        for i in indicator_list:
            m = re.match(r'^(MA)(\d+)', i)
            if m:
                if int(m.group(2)) > max_day:
                    max_day = int(m.group(2))
                else:
                    continue
        return max_day

    def find_recent_trade_day(self, dat):
        days = StockData.mgr().get_trade_day(self._sp_start.strftime('%Y-%m-%d'),self._sp_end.strftime('%Y-%m-%d'))[:]
        trade_days = [i['Date'].date() for i in days]
        if dat in trade_days:
            return dat
        else:
            return trade_days[-1]    
        
    def generate_stock_list(self):
        sc_type = self._stock_condition.get_stock_condition_type()
        sc_term = self._stock_condition.get_stock_condition_term()
        if sc_type == 'condition':
            res = []
            date = sc_term['date']
            conditions = sc_term['condition']
            date = self.find_recent_trade_day(date)
            stock_list = StockData.mgr().generate_stock_list_by_condition(date,conditions)[:]
            for i in stock_list:
                res.append(StockInfo(i))
            return res
        elif sc_type == 'total':
            print sc_type
        elif sc_type == 'stocks':
            res = []
            stock_list = sc_term
            for i in stock_list:
                res.append(StockInfo(i))
            return res
        
    def build_stock_pool_indicator(self):
        print "init stock number in stock pool: ",len(self._stock_list)
        self._sp = StockPool(self._stock_list,self._sp_start,self._sp_end)
        self._ind = Indicator(self._sp,self._start,self._indicator_list)
    
    def delete_incompleted_data(self):
        for stock in self._ind._useful_ind_format_data:
            for dat in stock['chart']:
                for ind in self._indicator_list:
                    if False == stock['chart'][dat][ind]:
                        try:
                            #self._ind._useful_ind_format_data.remove(stock)   # extremely violent
                            del self._ind._useful_ind_format_data[stock]['chart'][dat]             
                        except Exception:
                            pass
                        #print self._ind._useful_ind_format_data
        print "complete stock number: ",len(self._ind._useful_ind_format_data)
    
        #print self._ind._useful_ind_format_data
    
    def get_useful_ind_format_data(self):
        return self._ind._useful_ind_format_data
    
    
    