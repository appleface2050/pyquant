#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import os
import sys
import re

sys.path.append(os.path.dirname(os.path.split(os.path.realpath(__file__))[0]))

from lib.stock  import StockInfo
from lib.indicator import Indicator
from conf.settings import TRIGGER_OP_LIST
from model.stock_data import StockData
from lib.stock import StockPool

class Alpha(object):
    def __init__(self, sim_start, sim_end, sp):
        print "initqq"
        if sim_start > sim_end:
            print "sim time error"
            return False
        else:
            self._sim_start = sim_start
            self._sim_end = sim_end
            self._sp = sp
            self._strategy_desc = ""
            self._trade_day_list = []
            
    def find_trade_day(self):
        days = StockData.mgr().get_trade_day(self._sim_start.strftime('%Y-%m-%d'),self._sim_end.strftime('%Y-%m-%d'))[:]
        return [i['Date'].date() for i in days]
    
    def strategy_desc(self):
        return self._strategy_desc
    
    def strategy(self, start):
        """
        for child class
        """
        return True
    
    def running(self):
        self._trade_day_list = self.find_trade_day()
        print "sim days: ",len(self._trade_day_list)
        for dat in self._trade_day_list:
            #print 'start sim...',dat.strftime('%Y-%m-%d')
            self.strategy(dat)



    def trigger_overtake(self, item1, item2, op, stock_data, start):
        """
        trigger
        item: indicator or stock raw item 
        op: operator eg: up, down
        """
        assert op in TRIGGER_OP_LIST

        yest = self.find_last_trade_day(start)
        stock_data_date_list = stock_data.keys()
        if (start not in stock_data_date_list) or (yest not in stock_data_date_list):
            print start,yest,"this day do not hive stock data in mysql"
            return False
        
        if yest == False:         # the first day in self._trade_day_list, do not cal
            return False
        elif item1 and item2 and stock_data:
            if op == 'up':
                return stock_data[start][item1] > stock_data[start][item2] and stock_data[yest][item1] <= stock_data[yest][item2]
            elif op == 'down':
                return stock_data[start][item1] < stock_data[start][item2] and stock_data[yest][item1] >= stock_data[yest][item2]
            else:
                print "op error"
                exit(2)

    def find_last_trade_day(self, start):
        #print start
        if start not in self._trade_day_list:
            print "ERROR, find last trade day error"
            exit(2)
        inde = self._trade_day_list.index(start)
        if inde != 0:
            return  self._trade_day_list[inde-1]
        elif inde == 0:
            return False
        else:
            print "ERROR, find last trade day error"
            exit(2)
        
        
class StockPoolBuilder(object):
    def __init__(self, stock_condition, indicator_list, start):
        self._stock_condition = stock_condition
        self._indicator_list = indicator_list
        self._start = start
        self._sp_start, self._sp_end = self.generate_stock_pool_start_end()
        self._stock_list = self.generate_stock_list()
        #self._sp = StockPool(self._stock_list,start,end)
        
        self._sp = ''
        self._ind = ''
    
    def count_stock_num(self):
        return len(self._stock_list)
    
    def generate_stock_pool_start_end(self):
        #self._sp_end = self._stock_condition['date']
        #self._sp_start = self.generate_sp_start(self._start, indicator_list)
        return self.generate_sp_start(self._start, self._indicator_list), self._stock_condition['date']
        
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
        
    def generate_stock_list(self,):
        res = []
        date = self._stock_condition['date']
        conditions = self._stock_condition['condition']
        stock_list = StockData.mgr().generate_stock_list_by_condition(date,conditions)[:]
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
                        #print stock['chart'][dat][ind]
                        try:
                            self._ind._useful_ind_format_data.remove(stock)   # extremely violent
                        except Exception:
                            pass
                        #print self._ind._useful_ind_format_data
        print "complete stock number: ",len(self._ind._useful_ind_format_data)
    
        #print self._ind._useful_ind_format_data
    
    def get_useful_ind_format_data(self):
        return self._ind._useful_ind_format_data
            
if __name__ == '__main__':
    now = datetime.datetime.now()
    yest = now.date() - datetime.timedelta(days=1)
    print yest
    #stock_condition = {'date':yest,'condition':[{'item':'Close','min':18.0,'max':22.0},{'item':'Volume','min':'','max':1000000}]}
    stock_condition = {'date':yest,'condition':[{'item':'code','min':'600882','max':'600882'}]}
    indicator_list = ['MA120','MA240']
    start = yest
    spb = StockPoolBuilder(stock_condition,indicator_list,datetime.datetime.strptime('2014-09-01','%Y-%m-%d').date())
    print "stocknum:",spb.count_stock_num()
    spb.build_stock_pool_indicator()
    spb.delete_incompleted_data()
    #for stock in spb.get_useful_ind_format_data():
    #    print stock
    
    print "used time: ",datetime.datetime.now()-now
    
    
    
    
    
    
    