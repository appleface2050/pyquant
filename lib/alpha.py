#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import os
import sys

sys.path.append(os.path.dirname(os.path.split(os.path.realpath(__file__))[0]))

from conf.settings import TRIGGER_OP_LIST
from model.stock_data import StockData
from model.test_res_data import TestOrderData
from lib.position import Position
from lib.strategyRecorder import StrategyRecorder
from lib.stockpoolbuilder import StockPoolBuilder

class Alpha(object):
    def __init__(self, sim_start, sim_end, stock_condition, indicator_list):
        if sim_start > sim_end:
            print "sim time error"
            return False
        else:
            now = datetime.datetime.now()
            self._sim_start = sim_start
            self._sim_end = sim_end
            self._sim_end = self.find_recent_trade_day()
            self._indicator_list = indicator_list
            self._stock_condition = stock_condition
            self._spb = StockPoolBuilder(self._stock_condition,self._indicator_list,self._sim_start,self._sim_end)
            self._spb.build_stock_pool_indicator()
            self._spb.delete_incompleted_data()
            print 'Initializing Stock Pool done, time used:  ',datetime.datetime.now()-now
            print 'Start Simulating Strategy......'
            self._sp = self._spb.get_useful_ind_format_data()
            self._strategy_name = ""
            self._strategy_desc = ""
            self._trade_day_list = []
            self._trade_order_list = []
            self._position = Position()
            self._strategy_recorder = StrategyRecorder()
    
    def get_strategy_recorder(self):
        return self._strategy_recorder
    
    def get_sim_end(self):
        return self._sim_end
    
    def get_sim_start(self):
        return self._sim_start
    
    def add_order(self, trade):
        self._trade_order_list.append(trade)

    def find_trade_day(self):
        days = StockData.mgr().get_trade_day(self._sim_start.strftime('%Y-%m-%d'),self._sim_end.strftime('%Y-%m-%d'))[:]
        return [i['Date'].date() for i in days]

    def strategy_desc(self):
        return self._strategy_desc
    
    def strategy_calculating(self, start):
        """
        implement in child class
        """
        return True
    
    def get_position(self):
        return self._position
        #return self._position.get_position_table()
    
    def running(self):
        self._trade_day_list = self.find_trade_day()
        print "sim days(trade day): ",len(self._trade_day_list)
        for dat in self._trade_day_list:
            #print 'start sim...',dat.strftime('%Y-%m-%d')
            self.execute()
            self.get_strategy_recorder().record(dat,self.get_position())
            self.strategy_calculating(dat)
            
        self.clear_position()
        
    def report(self):
        print '-----------------------------------------------------'
        print "Reporting......"
        print "trade order history record:"
        self.report_order_table()
        print '-----------------------------------------------------'
        print 'trade result:'
        self.report_positioin_table('nocp')
        print '-----------------------------------------------------'
        print 'strategy record:'
        self.report_strategy_record()
        print '-----------------------------------------------------'
        #print self.get_position()
        #self.trade_order_desc()
        
    def report_positioin_table(self, type=None):
        if not type:
            self._position.desc_position_table_result()
        elif type == 'nocp':
            self._position.desc_position_table_result_no_current_position()
    
    def report_strategy_record(self):
        self.get_strategy_recorder().report(self.get_position(),self._trade_day_list)
    
    def report_order_table(self):
        self._position.desc_table_order_result()

    def clear_position(self):
        self._position.clear_position(self.get_sim_end())
        
    def clear_stock(self, date, stock_info):
        self._position.clear_stock(date, stock_info)
        
    def trade_order_desc(self):
        self._position.desc()
        
    def get_trade_order_list(self):
        return self._position.get_table_list()
    
    def execute(self):
        if not self._trade_order_list:
            return False
        else:
            while(self._trade_order_list):
                self._position.add(self._trade_order_list.pop(0))    #first in first out
                #self._position.desc()
            return True
    
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
            #print start,yest,"this day do not hive stock data in mysql"
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

    def find_recent_trade_day(self):
        days = StockData.mgr().get_trade_day(self._sim_start.strftime('%Y-%m-%d'),self._sim_end.strftime('%Y-%m-%d'))[:]
        trade_days = [i['Date'].date() for i in days]
        if self._sim_end in trade_days:
            return self._sim_end
        else:
            return trade_days[-1]  
        
    def find_last_trade_day(self, start):
        #print start
        if start not in self._trade_day_list:
            print "ERROR, find last trade day error 1"
            exit(2)
        inde = self._trade_day_list.index(start)
        if inde != 0:
            return  self._trade_day_list[inde-1]
        elif inde == 0:
            return False
        else:
            print "ERROR, find last trade day error 2"
            exit(2)
    
    def find_next_trade_day(self, start):
        if start not in self._trade_day_list:
            print "ERROR, find next trade day error1"
            exit(2)
        inde = self._trade_day_list.index(start)
        if (inde+1) != len(self._trade_day_list):
            return self._trade_day_list[inde+1]
        elif (inde+1) == len(self._trade_day_list):
            return False
        else:
            print "ERROR, find next trade day error2"
            exit(2)

class AlphaFullAmount(Alpha):
    def __init__(self, sim_start, sim_end, stock_condition, indicator_list):
        super(AlphaFullAmount, self).__init__(sim_start, sim_end, stock_condition, indicator_list)
        
    def running(self):
        self._trade_day_list = self.find_trade_day()
        print "sim days(trade day): ",len(self._trade_day_list)
        for dat in self._trade_day_list:
            self.execute()
            #self.get_strategy_recorder().record(dat,self.get_position())
            self.strategy_calculating(dat)
        self.clear_position()
    
    def data2db(self):
        order_table = self._position.get_table_list()
        if not order_table:
            return True
        for i in order_table:
            deal_date = i.get_deal_time()
            code = i.get_stock().get_stockinfo_code()
            exch = i.get_stock().get_stockinfo_exch()
            direction = i.get_direction()
            price = i.get_price()
            quantity = i.get_quantity()
            try:
                s = TestOrderData.new()
                s.strategy = 'TFLT0001FA'
                s.code = str(code)
                s.exchange = str(exch)
                s.deal_date = deal_date
                s.direction = str(direction)
                s.price = float(price)
                s.quantity = int(quantity)
                s.save()
            except Exception,e:
                print e

        


if __name__ == '__main__':
    now = datetime.datetime.now()
    yest = now.date() - datetime.timedelta(days=1)
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
    
    
    
    
    
    
    